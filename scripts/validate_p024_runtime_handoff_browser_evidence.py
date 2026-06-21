from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-handoff-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-handoff-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024RuntimeHandoffEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeHandoffEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "live_armed=true"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_handoff(payload: dict[str, Any], action: str) -> None:
    require(payload["schema_version"] == "account_command.owner_runtime_run_request.v1", f"{action} schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", f"{action} proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, f"{action} account mismatch")
    require(payload["action"] == action, f"{action} action mismatch")
    require(payload["mode"] == "paper_armed", f"{action} mode mismatch")
    require(payload["status"] == "blocked_until_owner_runtime_invocation", f"{action} status mismatch")
    require(payload["owner_runtime_owner_ref"] == "owner://nautilus_ctp_adapter", f"{action} owner mismatch")
    require(payload["owner_runtime_repo_ref"] == "owner-repo://nautilus_ctp_adapter", f"{action} repo mismatch")
    entrypoint = str(payload["owner_runtime_entrypoint_ref"])
    if action == "submit":
        require(entrypoint.endswith("ctp_guarded_paper_order_loop.py"), "submit entrypoint mismatch")
        require("readback_ref" not in payload or payload["readback_ref"] is None, "submit readback should be absent")
    else:
        require(entrypoint.endswith("ctp_guarded_paper_cancel_loop.py"), "cancel entrypoint mismatch")
        require(str(payload["readback_ref"]).endswith("post_submit_readback.json"), "cancel readback mismatch")
    require(payload["owner_runtime_config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", f"{action} config mismatch")
    require(payload["runtime_invocation_attempted"] is False, f"{action} runtime invocation mismatch")
    require(payload["browser_triggered_broker_order"] is False, f"{action} browser trigger mismatch")
    require(payload["gateway_send_attempted"] is False, f"{action} gateway flag mismatch")
    require(payload["broker_order_created"] is False, f"{action} broker order flag mismatch")
    require(payload["raw_secret_values_recorded"] is False, f"{action} raw secret mismatch")
    require(payload["raw_broker_endpoint_recorded"] is False, f"{action} raw endpoint mismatch")
    require(payload["external_write_approval_required"] is True, f"{action} write approval mismatch")
    require(str(payload["run_request_checksum"]).startswith("sha256:"), f"{action} checksum mismatch")
    blocker_types = {blocker["type"] for blocker in payload["blockers"]}
    require(
        blocker_types
        == {"owner_runtime_invocation_required", "external_write_approval_required", "post_run_ingest_required"},
        f"{action} blockers mismatch",
    )
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_send_broker_order_from_browser",
        "does_not_store_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_make_gateway_ack_final_state",
    ]:
        require(claim in non_claims, f"{action} non-claim missing: {claim}")


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.runtime-handoff-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    validate_handoff(payload["submit_handoff"], "submit")
    validate_handoff(payload["cancel_handoff"], "cancel")
    checks = payload.get("browser_checks") or {}
    for check in [
        "handoff_panel_visible",
        "submit_handoff_displayed",
        "cancel_handoff_displayed",
        "runtime_invocation_displayed_false",
        "browser_trigger_displayed_false",
        "live_ready_wording_absent",
    ]:
        require(checks.get(check) is True, f"browser check missing: {check}")


def validate_backend_endpoints() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    expected = {
        "/api/commands/accounts/{account_id}/runtime-run-requests/submit": {"POST"},
        "/api/commands/accounts/{account_id}/runtime-run-requests/cancel": {"POST"},
    }
    routes = {route.path: route.methods for route in app.routes if isinstance(route, APIRoute)}
    for path, methods in expected.items():
        require(path in routes, f"missing route: {path}")
        require(routes[path] == methods, f"{path}: method mismatch")

    client = TestClient(app)
    submit_intent = {
        "schema_version": "account_command.order_intent.v1",
        "intent_id": "intent.p024.handoff.submit.validator",
        "account_id": ACCOUNT_ID,
        "mode": "paper_armed",
        "action": "submit",
        "instrument": "rb2610",
        "exchange": "SHFE",
        "side": "BUY",
        "quantity": 1,
        "order_type": "LIMIT",
        "limit_price": 24910,
        "time_in_force": "GFD",
        "offset": "OPEN",
        "idempotency_key": "p024-handoff-submit-validator",
        "operator_ref": "operator://local/p024-validator",
        "preflight_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/closeout_manifest.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    cancel_intent = {
        "schema_version": "account_command.cancel_intent.v1",
        "intent_id": "intent.p024.handoff.cancel.validator",
        "account_id": ACCOUNT_ID,
        "mode": "paper_armed",
        "action": "cancel",
        "instrument": "rb2610",
        "exchange": "SHFE",
        "client_order_id": "p024-handoff-rb2610-001",
        "venue_order_id": "ctp19053-handoff-order-001",
        "order_ref": "37",
        "front_id": 1,
        "session_id": 1,
        "idempotency_key": "p024-handoff-cancel-validator",
        "operator_ref": "operator://local/p024-validator",
        "readback_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    submit_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/submit", json=submit_intent)
    cancel_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/cancel", json=cancel_intent)
    require(submit_response.status_code == 202, "submit handoff API status mismatch")
    require(cancel_response.status_code == 202, "cancel handoff API status mismatch")
    validate_handoff(submit_response.json(), "submit")
    validate_handoff(cancel_response.json(), "cancel")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeRunRequestPanel",
        "account-runtime-handoff-panel",
        "account-runtime-handoff-invoked",
        "account-runtime-handoff-web-trigger",
        "prepareSubmitRuntimeRunRequest",
        "prepareCancelRuntimeRunRequest",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["prepareSubmitRuntimeRunRequest", "prepareCancelRuntimeRunRequest", "runtime-run-requests"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require("interface CommandRuntimeRunRequest" in types_text, "frontend type missing CommandRuntimeRunRequest")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime handoff screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoints()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK: "
        "runtime_handoff=pass runtime_invocation_attempted=false browser_triggered_broker_order=false"
    )


if __name__ == "__main__":
    main()
