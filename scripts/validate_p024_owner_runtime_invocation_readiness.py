from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-invocation-readiness.json"
)
DOC = ROOT / "docs" / "proposals" / "p024-account-console-paper-command-controls" / "runtime-invocation-readiness.md"
P023_CLOSEOUT = ROOT / "output" / "account_command" / "ctp-paper-19053" / "p023-armed-20260621t0748z" / "closeout_manifest.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ctp-paper-19053" / "source-package.json"
OWNER_REPO = Path("D:/Nautilus/nautilus_ctp_adapter")
OWNER_ORDER_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_order_loop.py"
OWNER_CANCEL_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_cancel_loop.py"
OWNER_CONFIG = OWNER_REPO / "cfgs" / "local" / "ctp.openctp.tts.7x24.local.json"


class P024OwnerRuntimeInvocationReadinessError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRuntimeInvocationReadinessError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "tcp://", "trading.openctp.cn", "live_armed=true"]
    matches: list[str] = []
    for item in [path, DOC]:
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "blocked_waiting_for_external_owner_runtime_write_approval",
        "status mismatch",
    )
    require(payload["verdict"] == "readiness_package_passed_runtime_not_invoked", "verdict mismatch")

    owner = payload["owner_runtime"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner repo path mismatch")
    require(owner["config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", "config ref mismatch")
    require(owner["config_file_exists_on_owner_node"] is True, "config existence flag mismatch")
    require(OWNER_CONFIG.exists(), "owner config path missing; validator checks existence only")
    require(owner["config_raw_content_read"] is False, "config raw content flag mismatch")
    require(owner["raw_secret_values_recorded"] is False, "raw secret flag mismatch")
    require(owner["raw_broker_endpoint_recorded"] is False, "raw endpoint flag mismatch")

    require(OWNER_ORDER_SCRIPT.exists(), "owner order script missing")
    require(OWNER_CANCEL_SCRIPT.exists(), "owner cancel script missing")
    entrypoints = {entry["action"]: entry for entry in payload["entrypoints"]}
    require(set(entrypoints) == {"submit", "cancel"}, "entrypoint action set mismatch")
    require(entrypoints["submit"]["checksum"] == sha256(OWNER_ORDER_SCRIPT), "submit script checksum mismatch")
    require(entrypoints["cancel"]["checksum"] == sha256(OWNER_CANCEL_SCRIPT), "cancel script checksum mismatch")
    require(entrypoints["submit"]["armed_flag"] == "--arm-paper-send", "submit armed flag mismatch")
    require(entrypoints["cancel"]["armed_flag"] == "--arm-cancel-send", "cancel armed flag mismatch")
    for action, required in {
        "submit": ["--config", "--pre-snapshot", "--limit-price", "--client-order-id", "--output-json"],
        "cancel": ["--config", "--pre-snapshot", "--order-ref", "--front-id", "--session-id", "--output-json"],
    }.items():
        args = set(entrypoints[action]["required_arguments"])
        for arg in required:
            require(arg in args, f"{action} missing required argument {arg}")

    predecessor = payload["predecessor_evidence"]
    require(P023_CLOSEOUT.exists(), "P023 closeout missing")
    require(SOURCE_PACKAGE.exists(), "source package missing")
    require(predecessor["p023_closeout_manifest_checksum"] == sha256(P023_CLOSEOUT), "P023 checksum mismatch")
    require(predecessor["ctp_source_package_checksum"] == sha256(SOURCE_PACKAGE), "source package checksum mismatch")
    require(predecessor["predecessor_runtime_reconciled"] is True, "predecessor runtime flag mismatch")
    require(
        predecessor["predecessor_is_not_new_browser_triggered_runtime"] is True,
        "predecessor non-claim mismatch",
    )

    approval = payload["external_write_approval_request"]
    require(approval["required"] is True, "approval required flag mismatch")
    require(approval["obtained"] is False, "approval obtained flag mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(approval["approval_prompt_required_before_execution"] is True, "approval prompt flag mismatch")
    require(any("paper order" in item for item in approval["expected_impact"]), "approval impact missing paper order")
    require(any("outside this worktree" in item for item in approval["expected_impact"]), "approval impact missing worktree")

    commands = {command["action"]: command for command in payload["planned_runtime_commands"]}
    require(set(commands) == {"submit", "cancel"}, "planned command set mismatch")
    require("--arm-paper-send" in commands["submit"]["command_template"], "submit template missing arm flag")
    require("--arm-cancel-send" in commands["cancel"]["command_template"], "cancel template missing arm flag")
    require("cfgs/local/ctp.openctp.tts.7x24.local.json" in commands["submit"]["command_template"], "submit config ref missing")
    require("cfgs/local/ctp.openctp.tts.7x24.local.json" in commands["cancel"]["command_template"], "cancel config ref missing")
    require(commands["submit"]["runtime_invocation_attempted"] is False, "submit attempted flag mismatch")
    require(commands["cancel"]["runtime_invocation_attempted"] is False, "cancel attempted flag mismatch")

    artifacts = set(payload["acceptance_after_owner_run"]["required_owner_artifacts"])
    for artifact in [
        "submit_intent.json",
        "submit_gateway_event.json",
        "post_submit_readback.json",
        "cancel_intent.json",
        "cancel_gateway_event.json",
        "post_cancel_readback.json",
        "reconciliation_result.json",
        "redaction_report.json",
        "command_audit.json",
        "closeout_manifest.json",
    ]:
        require(artifact in artifacts, f"missing post-run artifact requirement: {artifact}")

    negative = payload["negative_assertions"]
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")

    blockers = {blocker["type"] for blocker in payload["blockers"]}
    require(
        blockers == {"external_write_approval_required", "owner_runtime_artifacts_missing"},
        "blocker set mismatch",
    )
    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_send_broker_order_from_browser",
        "does_not_write_owner_repo",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_phase_3_runtime_execution",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_doc() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "phase3e_runtime_readiness_ui_projection_passed",
        "This is not broker execution evidence",
        "external write approval is required",
        "runtime_invocation_attempted=false",
        "owner_repo_write_attempted=false",
        "P024_OWNER_RUNTIME_INVOCATION_READINESS_OK",
        "P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK",
    ]:
        require(phrase in text, f"readiness doc missing phrase: {phrase}")


def main() -> None:
    leaks = scan_forbidden_text(EVIDENCE)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_doc()
    print(
        "P024_OWNER_RUNTIME_INVOCATION_READINESS_OK: "
        "readiness=pass runtime_invocation_attempted=false external_write_approval=required"
    )


if __name__ == "__main__":
    main()
