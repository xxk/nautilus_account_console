from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p023-openctp-19053-command"
EVIDENCE = EVIDENCE_DIR / "ui-status-evidence.json"
REQUIRED_SCREENSHOTS = [
    "command-status-reconciled.png",
    "command-status-blocked.png",
]


class P023UiStatusBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P023UiStatusBrowserEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "OrderInsert", "OrderAction"]
    matches: list[str] = []
    for item in path.glob("ui-status-evidence.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_stage(stage: dict[str, Any]) -> None:
    stage_id = str(stage["stage"])
    browser = stage["browser"]
    api = stage["api"]
    require(stage["verdict"] == "pass", f"{stage_id}: verdict mismatch")
    require(str(api["command_audit_ref"]).endswith("command_audit.json"), f"{stage_id}: audit ref missing")
    gateway_refs = api.get("gateway_event_refs") or []
    require(len(gateway_refs) == 1 and str(gateway_refs[0]).endswith("submit_gateway_event.json"), f"{stage_id}: gateway ref missing")
    require("command_audit.json" in str(browser["audit_ref_seen"]), f"{stage_id}: browser audit ref missing")
    require("submit_gateway_event.json" in str(browser["gateway_ref_seen"]), f"{stage_id}: browser gateway ref missing")
    if stage_id == "reconciled":
        require(api["status"] == "reconciled", "reconciled: status mismatch")
        require(api["gateway_ack_is_final_state"] is False, "reconciled: gateway ack final-state claim")
        require(len(api.get("readback_refs") or []) == 1, "reconciled: readback ref missing")
        require(str(api.get("reconciliation_ref") or "").endswith("reconciliation_result.json"), "reconciled: reconciliation missing")
        require(browser["gateway_final_state"] == "false", "reconciled: browser gateway final mismatch")
        require(browser["readback_ref_count"] == 1, "reconciled: browser readback missing")
        require(browser["reconciliation_ref_count"] == 1, "reconciled: browser reconciliation missing")
        require(browser["blocker_count"] == 0, "reconciled: blockers should be absent")
    elif stage_id == "gateway_ack_only_blocked":
        require(api["status"] == "blocked", "blocked: status mismatch")
        require(api["gateway_ack_is_final_state"] is True, "blocked: expected invalid gateway final-state fixture")
        require(api.get("readback_refs") == [], "blocked: readback refs must be absent")
        require(api.get("reconciliation_ref") is None, "blocked: reconciliation must be absent")
        require(browser["gateway_final_state"] == "invalid", "blocked: browser did not reject gateway final state")
        require(browser["readback_ref_count"] == 0, "blocked: browser readback should be absent")
        require(browser["reconciliation_ref_count"] == 0, "blocked: browser reconciliation should be absent")
        require(browser["blocker_count"] >= 3, "blocked: browser blockers missing")
    else:
        raise P023UiStatusBrowserEvidenceError(f"unexpected stage: {stage_id}")


def validate(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p023.ui-status-evidence.v1", "schema mismatch")
    require(payload["proposal_id"] == "p023-openctp-19053-paper-command-capability", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["ui09_status_evidence_verdict"] == "pass", "verdict mismatch")
    require(payload["gateway_ack_final_state_rejected"] is True, "gateway final-state rejection missing")
    require(payload["command_controls_enabled"] is False, "command controls must remain disabled")
    require(payload["command_mode"] == "disabled", "command mode mismatch")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_submit_orders",
        "does_not_cancel_orders",
        "does_not_enable_command_controls",
        "does_not_treat_gateway_ack_as_final_state",
        "does_not_use_screenshot_as_command_truth",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")
    stages = payload.get("stages")
    require(isinstance(stages, list) and len(stages) == 2, "must contain reconciled and blocked stages")
    seen = {str(stage["stage"]) for stage in stages}
    require(seen == {"reconciled", "gateway_ack_only_blocked"}, f"stage set mismatch: {seen}")
    for stage in stages:
        validate_stage(stage)


def main() -> None:
    for screenshot in REQUIRED_SCREENSHOTS:
        require((EVIDENCE_DIR / screenshot).exists(), f"missing browser screenshot: {screenshot}")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive/action fragments found: {leaks}")
    validate(load(EVIDENCE))
    print("P023_UI_STATUS_BROWSER_EVIDENCE_OK: ui_status=pass gateway_ack_final_state=rejected")


if __name__ == "__main__":
    main()
