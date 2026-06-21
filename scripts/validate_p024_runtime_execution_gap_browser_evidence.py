from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-execution-gap-audit-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-execution-gap-audit-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-runtime-execution-gap-audit.spec.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024RuntimeExecutionGapBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeExecutionGapBrowserEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.runtime-execution-gap-audit-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    audit = payload["api_gap_audit"]
    require(audit["schema"] == "account-console.p024.runtime-execution-gap-audit.v1", "API schema mismatch")
    require(audit["status"] == "phase4e_final_runtime_execution_gap_audited", "API status mismatch")
    require(audit["verdict"] == "blocked_pending_owner_runtime_execution", "API verdict mismatch")
    require(audit["accepted_scenario_count"] == 14, "accepted scenario count mismatch")
    require(audit["not_accepted_scenario_count"] == 1, "not accepted scenario count mismatch")
    require(audit["required_before_goal_complete_count"] == 8, "required-before count mismatch")
    require(audit["required_owner_artifact_count"] == 14, "artifact count mismatch")
    require(audit["blocker_count"] == 3, "blocker count mismatch")
    for key in [
        "final_acceptance_claimed",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(audit[key] is False, f"API negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "gap_panel_visible",
        "verdict_displayed_blocked",
        "final_acceptance_claimed_displayed_false",
        "a4_not_accepted_displayed",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "broker_order_displayed_false",
        "required_items_displayed",
        "blocker_items_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_claim_all_acceptance_complete",
        "does_not_invoke_owner_runtime",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_create_broker_order",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_use_screenshot_as_order_or_runtime_truth",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_backend_endpoint() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/runtime-execution-gap-audit"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "gap audit route must be GET-only")
    require(found, "gap audit route missing")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-gap-audit")
    require(response.status_code == 200, "gap audit API does not return 200")
    payload = response.json()
    require(payload["status"] == "phase4e_final_runtime_execution_gap_audited", "API status mismatch")
    require(payload["verdict"] == "blocked_pending_owner_runtime_execution", "API verdict mismatch")
    require(payload["external_write_approval"]["obtained"] is False, "API approval flag mismatch")
    negative = payload["negative_assertions"]
    require(negative["final_acceptance_claimed"] is False, "API final claim mismatch")
    require(negative["runtime_invocation_attempted"] is False, "API invocation flag mismatch")
    require(negative["owner_repo_write_attempted"] is False, "API owner write flag mismatch")
    require(negative["broker_order_created"] is False, "API broker order flag mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeExecutionGapAuditPanel",
        "account-runtime-execution-gap-panel",
        "account-runtime-execution-gap-status",
        "account-runtime-execution-gap-final-claimed",
        "account-runtime-execution-gap-not-accepted",
        "account-runtime-execution-gap-approval-obtained",
        "account-runtime-execution-gap-invoked",
        "account-runtime-execution-gap-owner-write",
        "account-runtime-execution-gap-broker-order",
        "account-runtime-execution-gap-blocker",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["fetchCommandRuntimeExecutionGapAudit", "runtime-execution-gap-audit"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require(
        "interface CommandRuntimeExecutionGapAudit" in types_text,
        "frontend type missing gap audit interface",
    )
    for phrase in [
        "p024-runtime-execution-gap-audit-ui.png",
        "runtime-execution-gap-audit-ui.json",
        "does_not_claim_all_acceptance_complete",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime execution gap audit screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK: "
        "verdict=blocked_pending_owner_runtime_execution final_acceptance_claimed=false"
    )


if __name__ == "__main__":
    main()
