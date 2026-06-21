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
    "/api/commands/accounts/{account_id}/submit-intents": {"POST"},
    "/api/commands/accounts/{account_id}/cancel-intents": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-run-requests/submit": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-run-requests/cancel": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}": {"GET"},
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
    require(set(ALLOWED_COMMAND_ROUTES).issubset(route_paths), "P024 command API routes missing")
    for route in routes:
        path = route.path
        methods = route.methods or set()
        if path in ALLOWED_COMMAND_ROUTES:
            require(methods == ALLOWED_COMMAND_ROUTES[path], f"{path}: command route methods mismatch")
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

    submit_handoff_response = client.post(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/submit",
        json=submit_intent(),
    )
    require(submit_handoff_response.status_code == 202, "submit runtime handoff status mismatch")
    submit_handoff = submit_handoff_response.json()
    require(
        submit_handoff["schema_version"] == "account_command.owner_runtime_run_request.v1",
        "submit runtime handoff schema mismatch",
    )
    require(submit_handoff["status"] == "blocked_until_owner_runtime_invocation", "submit handoff status mismatch")
    require(submit_handoff["owner_runtime_entrypoint_ref"].endswith("ctp_guarded_paper_order_loop.py"), "submit handoff entrypoint mismatch")
    require(submit_handoff["runtime_invocation_attempted"] is False, "submit handoff must not invoke runtime")
    require(submit_handoff["browser_triggered_broker_order"] is False, "submit handoff browser trigger mismatch")
    require(submit_handoff["gateway_send_attempted"] is False, "submit handoff gateway flag mismatch")
    require(submit_handoff["run_request_checksum"].startswith("sha256:"), "submit handoff checksum missing")

    cancel_handoff_response = client.post(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/cancel",
        json=cancel_intent(),
    )
    require(cancel_handoff_response.status_code == 202, "cancel runtime handoff status mismatch")
    cancel_handoff = cancel_handoff_response.json()
    require(cancel_handoff["status"] == "blocked_until_owner_runtime_invocation", "cancel handoff status mismatch")
    require(cancel_handoff["owner_runtime_entrypoint_ref"].endswith("ctp_guarded_paper_cancel_loop.py"), "cancel handoff entrypoint mismatch")
    require(cancel_handoff["readback_ref"] == cancel_intent()["readback_ref"], "cancel handoff readback mismatch")
    require(cancel_handoff["runtime_invocation_attempted"] is False, "cancel handoff must not invoke runtime")
    require(cancel_handoff["browser_triggered_broker_order"] is False, "cancel handoff browser trigger mismatch")

    closeout_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-closeouts/p023-armed-20260621t0748z"
    )
    require(closeout_response.status_code == 200, f"runtime closeout status mismatch: {closeout_response.status_code}")
    closeout_payload = closeout_response.json()
    require(
        closeout_payload["schema_version"] == "account_command.runtime_closeout.v1",
        "runtime closeout schema mismatch",
    )
    require(closeout_payload["status"] == "reconciled", "runtime closeout must be reconciled")
    require(closeout_payload["runtime_gateway_send_observed"] is True, "runtime gateway send evidence missing")
    require(closeout_payload["broker_order_created"] is True, "runtime broker order evidence missing")
    require(closeout_payload["browser_triggered_broker_order"] is False, "runtime closeout must not claim browser trigger")
    require(closeout_payload["gateway_ack_is_final_state"] is False, "runtime closeout must not mark gateway ack final")
    require(closeout_payload["raw_secret_values_recorded"] is False, "runtime closeout must not record raw secrets")
    require(
        "web_ui_trigger_of_new_runtime_order_still_pending" in closeout_payload["explicit_non_claims"],
        "runtime closeout non-claim missing",
    )

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
        "phase=1 routes=5 status=accepted_for_risk runtime_handoff=blocked runtime_closeout=reconciled mirror_read_only=true"
    )


if __name__ == "__main__":
    main()
