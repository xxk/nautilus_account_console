from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-approval-packet-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-approval-packet-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-runtime-execution-approval-packet.spec.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024RuntimeApprovalPacketEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeApprovalPacketEvidenceError(message)


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
    require(payload["schema"] == "account-console.p024.runtime-approval-packet-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    packet = payload["api_approval_packet"]
    require(
        packet["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1",
        "API approval packet schema mismatch",
    )
    require(
        packet["status"] == "phase4a_owner_runtime_execution_approval_packet_ready",
        "API approval packet status mismatch",
    )
    require(packet["verdict"] == "approval_packet_ready_runtime_not_invoked", "API verdict mismatch")
    require(packet["approval_required"] is True, "approval required flag mismatch")
    require(packet["approval_obtained"] is False, "approval obtained flag mismatch")
    require(packet["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(packet["exact_approval_text_present"] is True, "exact approval text missing")
    require(packet["entrypoint_count"] == 2, "entrypoint count mismatch")
    require(packet["blocker_count"] == 2, "blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(packet[key] is False, f"approval packet negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "approval_packet_panel_visible",
        "owner_path_displayed",
        "exact_approval_text_displayed",
        "approval_required_displayed_true",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "broker_order_displayed_false",
        "entrypoints_displayed",
        "blockers_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_create_broker_order",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_real_runtime_execution",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_backend_endpoint() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/runtime-execution-approval-packet"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "approval packet route must be GET-only")
    require(found, "approval packet route missing")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-approval-packet")
    require(response.status_code == 200, "approval packet API does not return 200")
    payload = response.json()
    require(payload["status"] == "phase4a_owner_runtime_execution_approval_packet_ready", "API status mismatch")
    require(payload["required_operator_approval"]["required"] is True, "API approval required mismatch")
    require(payload["required_operator_approval"]["obtained"] is False, "API approval obtained mismatch")
    require(
        "I approve writes to D:/Nautilus/nautilus_ctp_adapter"
        in payload["required_operator_approval"]["exact_approval_text"],
        "API exact approval text mismatch",
    )
    negative = payload["negative_assertions"]
    require(negative["runtime_invocation_attempted"] is False, "API invocation flag mismatch")
    require(negative["owner_repo_write_attempted"] is False, "API owner write flag mismatch")
    require(negative["broker_order_created"] is False, "API broker order flag mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeExecutionApprovalPacketPanel",
        "account-runtime-approval-packet-panel",
        "account-runtime-approval-packet-status",
        "account-runtime-approval-packet-exact-text",
        "account-runtime-approval-packet-obtained",
        "account-runtime-approval-packet-invoked",
        "account-runtime-approval-packet-broker-order",
        "account-runtime-approval-packet-blocker",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["fetchCommandRuntimeExecutionApprovalPacket", "runtime-execution-approval-packet"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require(
        "interface CommandRuntimeExecutionApprovalPacket" in types_text,
        "frontend type missing approval packet interface",
    )
    for phrase in [
        "p024-runtime-approval-packet-ui.png",
        "runtime-approval-packet-ui.json",
        "exact_approval_text_displayed",
        "does_not_close_real_runtime_execution",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime approval packet screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK: "
        "runtime_approval_packet_ui=pass approval_obtained=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
