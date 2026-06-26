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
    "/api/commands/accounts/{account_id}/projection": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-invocation-readiness": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-approval-packet": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-gap-audit": {"GET"},
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
    require(submit_response.status_code == 403, f"submit must fail closed: {submit_response.status_code}")
    submit_payload = submit_response.json()
    require(submit_payload["detail"] == "command_capability_not_mounted", "submit blocker mismatch")

    replay_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/submit-intents", json=submit_intent())
    require(replay_response.status_code == 403, "submit replay must fail closed")
    require(replay_response.json() == submit_payload, "submit idempotency result drifted")

    cancel_response = client.post(f"/api/commands/accounts/{ACCOUNT_ID}/cancel-intents", json=cancel_intent())
    require(cancel_response.status_code == 403, f"cancel must fail closed: {cancel_response.status_code}")
    require(cancel_response.json()["detail"] == "command_capability_not_mounted", "cancel blocker mismatch")

    submit_handoff_response = client.post(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/submit",
        json=submit_intent(),
    )
    require(submit_handoff_response.status_code == 403, "submit runtime handoff must fail closed")
    require(submit_handoff_response.json()["detail"] == "command_capability_not_mounted", "submit handoff blocker mismatch")

    cancel_handoff_response = client.post(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-run-requests/cancel",
        json=cancel_intent(),
    )
    require(cancel_handoff_response.status_code == 403, "cancel runtime handoff must fail closed")
    require(cancel_handoff_response.json()["detail"] == "command_capability_not_mounted", "cancel handoff blocker mismatch")

    projection_response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/projection")
    require(projection_response.status_code == 200, f"command plane projection status mismatch: {projection_response.status_code}")
    projection_payload = projection_response.json()
    require(
        projection_payload["schema_version"] == "account_command.command_plane_projection.v1",
        "command plane projection schema mismatch",
    )
    require(
        projection_payload["projection_owner"] == "account-console-backend.mirror_projection",
        "command plane projection owner mismatch",
    )
    require(
        projection_payload["canonical_source"] == "/api/mirror/accounts/{account_id}",
        "command plane projection canonical source mismatch",
    )
    require(
        "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}" in projection_payload["legacy_read_surfaces"],
        "command plane projection legacy read surfaces mismatch",
    )
    require(
        "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet"
        not in projection_payload["legacy_read_surfaces"],
        "retired archive surface must not remain in legacy live-read inventory",
    )
    require(
        any(
            item["route"] == "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet"
            and item["archive_evidence_only"] is True
            for item in projection_payload["retired_archive_surfaces"]
        ),
        "command plane projection retired archive inventory mismatch",
    )
    require(
        "/api/commands/accounts/{account_id}/submit-intents" in projection_payload["action_surfaces"],
        "command plane projection action surfaces mismatch",
    )

    closeout_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/runtime-closeouts/p023-armed-20260621t0748z"
    )
    require(closeout_response.status_code == 409, f"runtime closeout must fail closed: {closeout_response.status_code}")
    require(
        closeout_response.json()["detail"] == "runtime closeout missing owner runtime evidence",
        "runtime closeout owner evidence blocker mismatch",
    )

    readiness_response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-invocation-readiness")
    require(readiness_response.status_code == 200, f"runtime readiness status mismatch: {readiness_response.status_code}")
    readiness_payload = readiness_response.json()
    require(
        readiness_payload["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1",
        "runtime readiness schema mismatch",
    )
    require(
        readiness_payload["status"] == "blocked_waiting_for_external_owner_runtime_write_approval",
        "runtime readiness status mismatch",
    )
    require(readiness_payload["external_write_approval_request"]["required"] is True, "runtime readiness approval required mismatch")
    require(readiness_payload["external_write_approval_request"]["obtained"] is False, "runtime readiness approval obtained mismatch")
    require(readiness_payload["negative_assertions"]["runtime_invocation_attempted"] is False, "runtime readiness invocation flag mismatch")
    require(readiness_payload["negative_assertions"]["owner_repo_write_attempted"] is False, "runtime readiness owner write flag mismatch")
    require(readiness_payload["negative_assertions"]["browser_triggered_broker_order"] is False, "runtime readiness browser trigger mismatch")

    approval_response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-approval-packet")
    require(approval_response.status_code == 200, f"runtime approval packet status mismatch: {approval_response.status_code}")
    approval_payload = approval_response.json()
    require(
        approval_payload["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1",
        "runtime approval packet schema mismatch",
    )
    require(
        approval_payload["status"] == "phase4a_owner_runtime_execution_approval_packet_ready",
        "runtime approval packet status mismatch",
    )
    require(
        approval_payload["verdict"] == "approval_packet_ready_runtime_not_invoked",
        "runtime approval packet verdict mismatch",
    )
    require(approval_payload["required_operator_approval"]["required"] is True, "runtime approval required mismatch")
    require(approval_payload["required_operator_approval"]["obtained"] is False, "runtime approval obtained mismatch")
    require(
        approval_payload["planned_execution"]["runtime_invocation_attempted"] is False,
        "runtime approval planned invocation flag mismatch",
    )
    require(
        approval_payload["planned_execution"]["owner_repo_write_attempted"] is False,
        "runtime approval planned owner write flag mismatch",
    )
    require(
        approval_payload["negative_assertions"]["broker_order_created"] is False,
        "runtime approval broker order flag mismatch",
    )

    bundle_response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-handoff-bundle")
    require(bundle_response.status_code == 200, f"runtime handoff bundle status mismatch: {bundle_response.status_code}")
    bundle_payload = bundle_response.json()
    require(
        bundle_payload["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1",
        "runtime handoff bundle schema mismatch",
    )
    require(
        bundle_payload["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready",
        "runtime handoff bundle status mismatch",
    )
    require(bundle_payload["execution_guard"]["execution_allowed"] is False, "runtime handoff execution allowed mismatch")
    require(bundle_payload["execution_guard"]["approval_obtained"] is False, "runtime handoff approval mismatch")
    require(
        bundle_payload["negative_assertions"]["runtime_invocation_attempted"] is False,
        "runtime handoff invocation flag mismatch",
    )
    require(
        bundle_payload["negative_assertions"]["broker_order_created"] is False,
        "runtime handoff broker order flag mismatch",
    )

    partial_approval_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-runtime-execution-approval-packet"
    )
    require(
        partial_approval_response.status_code == 404,
        f"partial-fill runtime approval packet retirement mismatch: {partial_approval_response.status_code}",
    )

    partial_bundle_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-runtime-execution-handoff-bundle"
    )
    require(
        partial_bundle_response.status_code == 404,
        f"partial-fill runtime handoff bundle retirement mismatch: {partial_bundle_response.status_code}",
    )

    gap_response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-gap-audit")
    require(gap_response.status_code == 200, f"runtime execution gap audit status mismatch: {gap_response.status_code}")
    gap_payload = gap_response.json()
    require(
        gap_payload["schema"] == "account-console.p024.runtime-execution-gap-audit.v1",
        "runtime execution gap audit schema mismatch",
    )
    require(
        gap_payload["status"] == "phase4e_final_runtime_execution_gap_audited",
        "runtime execution gap audit status mismatch",
    )
    require(gap_payload["verdict"] == "blocked_pending_owner_runtime_execution", "runtime execution gap verdict mismatch")
    require(gap_payload["external_write_approval"]["obtained"] is False, "runtime execution gap approval mismatch")
    require(gap_payload["negative_assertions"]["final_acceptance_claimed"] is False, "runtime execution gap final claim mismatch")
    require(
        gap_payload["negative_assertions"]["runtime_invocation_attempted"] is False,
        "runtime execution gap invocation flag mismatch",
    )

    repair_plan_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-implementation-plan"
    )
    require(
        repair_plan_response.status_code == 404,
        f"partial-fill owner repair plan retirement mismatch: {repair_plan_response.status_code}",
    )

    repair_approval_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-approval-packet"
    )
    require(
        repair_approval_response.status_code == 404,
        f"partial-fill owner repair approval packet retirement mismatch: {repair_approval_response.status_code}",
    )

    remaining_state_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-remaining-acceptance-current-state"
    )
    require(
        remaining_state_response.status_code == 404,
        f"partial-fill remaining acceptance state retirement mismatch: {remaining_state_response.status_code}",
    )

    ingest_gate_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-evidence-ingest-gate"
    )
    require(
        ingest_gate_response.status_code == 404,
        f"partial-fill owner repair ingest gate retirement mismatch: {ingest_gate_response.status_code}",
    )

    preflight_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-preflight-source-audit"
    )
    require(
        preflight_response.status_code == 404,
        f"partial-fill owner repair preflight retirement mismatch: {preflight_response.status_code}",
    )

    patch_preview_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-patch-preview"
    )
    require(
        patch_preview_response.status_code == 404,
        f"partial-fill owner repair patch preview retirement mismatch: {patch_preview_response.status_code}",
    )

    repair_handoff_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-execution-handoff-bundle"
    )
    require(
        repair_handoff_response.status_code == 404,
        f"partial-fill owner repair execution handoff retirement mismatch: {repair_handoff_response.status_code}",
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
        "phase=governed routes=13 command_capability=not_mounted command_projection=mirror_canonical runtime_handoff=blocked runtime_closeout=blocked_pending_owner_evidence runtime_readiness=blocked runtime_approval_packet=ready runtime_handoff_bundle=ready partial_fill_pre_repair_runtime_ui=retired_archive_only runtime_execution_gap=blocked owner_repair_approval=required remaining_acceptance=missing_r1_to_r5 owner_repair_plan=ready owner_repair_execution_lane_ui=retired_archive_only mirror_read_only=true"
    )


if __name__ == "__main__":
    main()
