from __future__ import annotations

import sys
from pathlib import Path

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.main import app  # noqa: E402


ACCOUNT_ID = "acct.ctp.paper.19053"
ALLOWED_COMMAND_ROUTES = {
    "/api/commands/accounts/{account_id}/submit-intents",
    "/api/commands/accounts/{account_id}/cancel-intents",
}


class P024CommandApiValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024CommandApiValidationError(message)


def submit_intent() -> dict:
    return {
        "schema_version": "account_command.order_intent.v1",
        "intent_id": "intent.p024.submit.validator.001",
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
        "idempotency_key": "p024-validator-submit-001",
        "operator_ref": "operator://local/p024-validator",
        "preflight_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/closeout_manifest.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }


def cancel_intent() -> dict:
    return {
        "schema_version": "account_command.cancel_intent.v1",
        "intent_id": "intent.p024.cancel.validator.001",
        "account_id": ACCOUNT_ID,
        "mode": "paper_armed",
        "action": "cancel",
        "instrument": "rb2610",
        "exchange": "SHFE",
        "client_order_id": "p024-validator-rb2610-001",
        "venue_order_id": "ctp19053-validator-order-001",
        "order_ref": "37",
        "front_id": 1,
        "session_id": 1,
        "idempotency_key": "p024-validator-cancel-001",
        "operator_ref": "operator://local/p024-validator",
        "readback_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }


def validate_route_boundary() -> None:
    routes = [route for route in app.routes if isinstance(route, APIRoute)]
    route_paths = {route.path for route in routes}
    require(ALLOWED_COMMAND_ROUTES.issubset(route_paths), "P024 command API routes missing")
    for route in routes:
        path = route.path
        methods = route.methods or set()
        if path in ALLOWED_COMMAND_ROUTES:
            require(methods == {"POST"}, f"{path}: command route must be POST-only")
        elif path.startswith("/api/commands"):
            raise P024CommandApiValidationError(f"unexpected command route: {path}")
        if path.startswith("/api/mirror/"):
            require(methods == {"GET"}, f"{path}: mirror route must remain GET-only")


def validate_api_behavior() -> None:
    client = TestClient(app)

    submit_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/submit-intents", json=submit_intent())
    require(submit_response.status_code == 202, f"submit status mismatch: {submit_response.status_code}")
    submit_payload = submit_response.json()
    require(submit_payload["schema_version"] == "account_command.command_api_result.v1", "submit schema mismatch")
    require(submit_payload["proposal_id"] == "p024-account-console-paper-command-controls", "submit proposal mismatch")
    require(submit_payload["status"] == "accepted_for_risk", "submit must stop at risk gate")
    require(submit_payload["gateway_send_attempted"] is False, "submit must not send gateway in Phase 1")
    require(submit_payload["broker_order_created"] is False, "submit must not create broker order in Phase 1")
    require(submit_payload["gateway_ack_is_final_state"] is False, "submit must not mark ack final")
    require({row["type"] for row in submit_payload["blockers"]} == {"risk_decision_required", "approval_decision_required"}, "submit blockers mismatch")

    replay_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/submit-intents", json=submit_intent())
    require(replay_response.status_code == 202, "submit replay status mismatch")
    require(replay_response.json() == submit_payload, "submit idempotency result drifted")

    cancel_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/cancel-intents", json=cancel_intent())
    require(cancel_response.status_code == 202, f"cancel status mismatch: {cancel_response.status_code}")
    cancel_payload = cancel_response.json()
    require(cancel_payload["status"] == "accepted_for_risk", "cancel must stop at risk gate")
    require(cancel_payload["gateway_send_attempted"] is False, "cancel must not send gateway in Phase 1")
    require(cancel_payload["readback_refs"], "cancel must carry readback identity ref")

    live_intent = submit_intent()
    live_intent["mode"] = "live_armed"
    live_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/submit-intents", json=live_intent)
    require(live_response.status_code == 403, "live_armed must be rejected")

    mirror_post = client.post(f"/api/mirror/accounts/{ACCOUNT_ID}/orders", json={})
    require(mirror_post.status_code == 405, "Account Mirror orders route must reject POST")


def main() -> None:
    validate_route_boundary()
    validate_api_behavior()
    print(
        "P024_PAPER_COMMAND_API_OK: "
        "phase=1 routes=2 status=accepted_for_risk gateway_send_attempted=false mirror_read_only=true"
    )


if __name__ == "__main__":
    main()
