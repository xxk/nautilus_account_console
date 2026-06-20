from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCOUNT_ID = "acct.ctp.paper.19053"
REQUIRED_FILES = [
    "submit_intent.json",
    "submit_risk_decision.json",
    "submit_approval_decision.json",
    "submit_gateway_event.json",
    "post_submit_readback.json",
    "cancel_intent.json",
    "cancel_risk_decision.json",
    "cancel_approval_decision.json",
    "cancel_gateway_event.json",
    "post_cancel_readback.json",
    "reconciliation_result.json",
    "command_audit.json",
    "redaction_report.json",
    "closeout_manifest.json",
]


class P023CommandRunError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P023CommandRunError(message)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_checksum(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def scan_sensitive_values(path: Path) -> list[str]:
    fragments = ["tcp://", "trading.openctp", "Password", "AuthCode", "BrokerID", "UserID"]
    matches: list[str] = []
    for file in sorted(path.rglob("*")):
        if not file.is_file():
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        if any(fragment.lower() in text.lower() for fragment in fragments):
            matches.append(str(file))
    return matches


def validate_common(run_dir: Path) -> dict[str, dict[str, Any]]:
    require(run_dir.exists(), f"run dir missing: {run_dir}")
    for filename in REQUIRED_FILES:
        require((run_dir / filename).exists(), f"missing artifact: {filename}")
    leaks = scan_sensitive_values(run_dir)
    require(not leaks, f"sensitive fragments found in artifacts: {leaks}")
    payloads = {filename: read_json(run_dir / filename) for filename in REQUIRED_FILES}
    for filename, payload in payloads.items():
        require(payload.get("account_id") == ACCOUNT_ID, f"{filename}: account_id mismatch")
        if "raw_secret_values_recorded" in payload:
            require(payload["raw_secret_values_recorded"] is False, f"{filename}: raw secrets recorded")
        if "raw_broker_endpoint_recorded" in payload:
            require(payload["raw_broker_endpoint_recorded"] is False, f"{filename}: raw endpoint recorded")
        if "gateway_ack_is_final_state" in payload:
            require(payload["gateway_ack_is_final_state"] is False, f"{filename}: gateway ack marked final")

    manifest = payloads["closeout_manifest.json"]
    refs = manifest.get("artifact_refs")
    require(isinstance(refs, dict) and refs, "manifest artifact_refs missing")
    for filename, item in refs.items():
        artifact = run_dir / filename
        require(artifact.exists(), f"manifest references missing file: {filename}")
        require(item.get("checksum") == file_checksum(artifact), f"manifest checksum mismatch: {filename}")

    for filename in ["post_submit_readback.json", "post_cancel_readback.json"]:
        readback = payloads[filename]
        require(readback.get("success") is True, f"{filename}: readback did not pass")
        require(readback.get("login_success") is True, f"{filename}: login not proven")
        require(readback.get("order_send_called") is False, f"{filename}: readback sent order")
        require(readback.get("order_action_sent") is False, f"{filename}: readback sent order action")
        require(readback.get("cancel_order_sent") is False, f"{filename}: readback sent cancel")
    require(payloads["redaction_report.json"].get("status") == "passed", "redaction report not passed")
    return payloads


def validate_mode(payloads: dict[str, dict[str, Any]], *, allow_dry_run: bool) -> str:
    manifest = payloads["closeout_manifest.json"]
    mode = str(manifest.get("mode") or "")
    require(manifest.get("status") == "reconciled", "manifest status is not reconciled")
    require(payloads["command_audit.json"].get("status") == "reconciled", "command audit is not reconciled")
    require(payloads["reconciliation_result.json"].get("status") == "reconciled", "reconciliation is not reconciled")
    submit_gateway = payloads["submit_gateway_event.json"]
    cancel_gateway = payloads["cancel_gateway_event.json"]
    require(submit_gateway.get("status") == "accepted", "submit gateway not accepted")

    if mode == "live_dry_run":
        require(allow_dry_run, "dry-run artifact requires --allow-dry-run")
        require(submit_gateway.get("paper_send_armed") is False, "dry-run armed paper send")
        require(cancel_gateway.get("status") == "dry_run", "dry-run cancel status mismatch")
        require(cancel_gateway.get("cancel_send_armed") is False, "dry-run armed cancel")
        return mode

    require(mode == "paper_armed", f"unsupported mode: {mode}")
    require(submit_gateway.get("paper_send_armed") is True, "paper run did not arm submit")
    require(submit_gateway.get("live_send_armed") is True, "owner gateway did not arm live paper send")
    require(cancel_gateway.get("status") == "accepted", "cancel gateway not accepted")
    require(cancel_gateway.get("cancel_send_armed") is True, "paper run did not arm cancel")
    require(payloads["reconciliation_result.json"].get("post_cancel_order_cancelled") is True, "post-cancel readback not cancelled")
    return mode


def validate_source_package(source_package: Path, payloads: dict[str, dict[str, Any]]) -> None:
    require(source_package.exists(), f"source package missing: {source_package}")
    source = read_json(source_package)
    require(source.get("account_id") == ACCOUNT_ID, "source package account mismatch")
    require(source.get("source_health", {}).get("order_action_sent") is False, "source package claims order action")
    require(source.get("source_health", {}).get("cancel_order_sent") is False, "source package claims cancel action")
    cancel_intent = payloads["cancel_intent.json"]
    cancelled_order_ref = str(cancel_intent.get("order_ref") or "")
    projected_refs = {str(row.get("client_order_id") or row.get("venue_order_id") or "") for row in source.get("orders") or []}
    require(cancelled_order_ref not in projected_refs, "cancelled order was projected as open order")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a P023 OpenCTP 19053 command acceptance run directory.")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--allow-dry-run", action="store_true")
    parser.add_argument("--source-package", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir if args.run_dir.is_absolute() else ROOT / args.run_dir
    payloads = validate_common(run_dir)
    mode = validate_mode(payloads, allow_dry_run=args.allow_dry_run)
    if args.source_package is not None:
        source_package = args.source_package if args.source_package.is_absolute() else ROOT / args.source_package
        validate_source_package(source_package, payloads)
    print(f"P023_OPENCTP19053_COMMAND_RUN_OK: mode={mode} status=reconciled run_dir={run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
