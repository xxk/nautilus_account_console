from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-remaining-acceptance-state-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-remaining-acceptance-state-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"
EXPECTED_REQUIREMENTS = {
    "R1_owner_repair_approval",
    "R2_owner_close_offset_repair",
    "R3_owner_validators",
    "R4_post_repair_partial_fill_runtime",
    "R5_web_ui_real_partial_fill_projection",
}


class P024RemainingAcceptanceStateBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RemainingAcceptanceStateBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-remaining-acceptance-state-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    state = payload["api_remaining_acceptance_state"]
    require(state["schema"] == "account-console.p024.partial-fill-remaining-acceptance-current-state.v1", "API schema mismatch")
    require(state["status"] == "phase4q_remaining_acceptance_current_state_audited", "API status mismatch")
    require(state["requirement_count"] == 5, "requirement count mismatch")
    require(set(state["missing_requirement_ids"]) == EXPECTED_REQUIREMENTS, "requirement ids mismatch")
    require(state["accepted_evidence_group_count"] == 4, "accepted evidence group count mismatch")
    require(state["owner_code_repair_allowed"] is False, "owner repair allowed mismatch")
    require(state["owner_runtime_retry_allowed"] is False, "runtime retry mismatch")
    require(state["full_acceptance_claimed"] is False, "full claim mismatch")
    require(state["real_partial_fill_claimed"] is False, "real partial fill claim mismatch")
    require(state["web_ui_real_partial_fill_claimed"] is False, "Web UI partial fill claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "remaining_panel_visible",
        "r1_to_r5_displayed",
        "all_requirements_displayed_missing",
        "evidence_groups_displayed",
        "owner_repair_allowed_displayed_false",
        "runtime_retry_displayed_false",
        "full_acceptance_displayed_false",
        "real_partial_fill_claimed_displayed_false",
        "web_ui_real_partial_fill_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-remaining-acceptance-current-state"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "remaining acceptance route must be GET-only")
    require(found, "remaining acceptance route missing")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-remaining-acceptance-current-state")
    require(response.status_code == 200, "remaining acceptance API does not return 200")
    payload = response.json()
    requirements = {item["requirement_id"]: item for item in payload["remaining_acceptance_requirements"]}
    require(set(requirements) == EXPECTED_REQUIREMENTS, "API requirement ids mismatch")
    require(all(item["current_status"] == "missing" for item in requirements.values()), "API requirement state mismatch")
    require(payload["negative_assertions"]["full_acceptance_claimed"] is False, "API full claim mismatch")
    require(payload["negative_assertions"]["web_ui_real_partial_fill_claimed"] is False, "API Web UI claim mismatch")


def validate_frontend_contract() -> None:
    frontend_type = (ROOT / "frontend" / "src" / "types.ts").read_text(encoding="utf-8")
    frontend_app = (ROOT / "frontend" / "src" / "App.tsx").read_text(encoding="utf-8")
    require("interface CommandPartialFillRemainingAcceptanceCurrentState" in frontend_type, "frontend type missing remaining state")
    require("account-partial-fill-remaining-acceptance-panel" in frontend_app, "frontend panel test id missing")
    require("fetchCommandPartialFillRemainingAcceptanceCurrentState" in frontend_app, "frontend fetch missing")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    validate_frontend_contract()
    print(
        "P024_PARTIAL_FILL_REMAINING_ACCEPTANCE_STATE_BROWSER_EVIDENCE_OK: "
        "ui=pass requirements=5 full_acceptance=false"
    )


if __name__ == "__main__":
    main()
