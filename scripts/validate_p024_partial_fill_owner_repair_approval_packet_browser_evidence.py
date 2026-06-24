from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-approval-packet-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-approval-packet-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024OwnerRepairApprovalPacketBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRepairApprovalPacketBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-owner-repair-approval-packet-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    packet = payload["api_owner_repair_approval_packet"]
    require(packet["schema"] == "account-console.p024.partial-fill-owner-repair-approval-packet.v1", "API schema mismatch")
    require(packet["status"] == "phase4p_owner_close_offset_repair_approval_packet_ready", "API status mismatch")
    require(packet["verdict"] == "owner_repair_approval_required_before_retry", "API verdict mismatch")
    require(packet["approval_obtained"] is False, "approval obtained mismatch")
    require(packet["current_approval_matches_next_action"] is False, "current approval match mismatch")
    require(packet["exact_approval_text_present"] is True, "exact approval text missing")
    require(packet["owner_change_count"] == 3, "owner change count mismatch")
    require(packet["owner_validator_count"] == 2, "owner validator count mismatch")
    require(packet["blocker_count"] == 3, "blocker count mismatch")
    require(packet["runtime_retry_allowed"] is False, "runtime retry mismatch")
    require(packet["additional_order_authorized"] is False, "additional order mismatch")
    require(packet["owner_repo_write_attempted"] is False, "owner write mismatch")
    require(packet["partial_fill_claimed"] is False, "partial fill claim mismatch")
    require(packet["full_acceptance_claimed"] is False, "full claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "approval_packet_panel_visible",
        "exact_approval_text_displayed",
        "owner_changes_displayed",
        "validators_displayed",
        "blockers_displayed",
        "approval_obtained_displayed_false",
        "current_approval_matches_displayed_false",
        "runtime_retry_displayed_false",
        "owner_write_displayed_false",
        "additional_order_displayed_false",
        "partial_fill_claimed_displayed_false",
        "full_acceptance_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-approval-packet"
    require(all(getattr(item, "path", "") != route for item in app.routes), "approval packet route should be retired")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-approval-packet")
    require(response.status_code == 404, "approval packet API retirement mismatch")


def validate_frontend_contract() -> None:
    frontend_type = (ROOT / "frontend" / "src" / "types-historical-p024.ts").read_text(encoding="utf-8")
    frontend_app = (ROOT / "frontend" / "src" / "App.tsx").read_text(encoding="utf-8")
    frontend_api = (ROOT / "frontend" / "src" / "api.ts").read_text(encoding="utf-8")
    require("interface CommandPartialFillOwnerRepairApprovalPacket" in frontend_type, "frontend type missing approval packet")
    require("account-partial-fill-owner-repair-approval-packet-panel" not in frontend_app, "retired frontend panel should be removed")
    require("fetchCommandPartialFillOwnerRepairApprovalPacket" not in frontend_api, "retired frontend API fetch should be removed")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    validate_frontend_contract()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET_BROWSER_EVIDENCE_OK: "
        "ui=archive_only_historical_evidence route=retired_404 approval=false runtime_retry=false owner_write=false"
    )


if __name__ == "__main__":
    main()
