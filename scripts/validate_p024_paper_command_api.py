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
    "/api/commands/accounts/{account_id}/runtime-invocation-readiness": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-approval-packet": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-gap-audit": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview": {"GET"},
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle": {"GET"},
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
        partial_approval_response.status_code == 200,
        f"partial-fill runtime approval packet status mismatch: {partial_approval_response.status_code}",
    )
    partial_approval_payload = partial_approval_response.json()
    require(
        partial_approval_payload["schema"]
        == "account-console.p024.partial-fill-runtime-execution-approval-packet.v1",
        "partial-fill runtime approval packet schema mismatch",
    )
    require(
        partial_approval_payload["status"] == "phase4j_partial_fill_runtime_execution_approval_packet_ready",
        "partial-fill runtime approval packet status mismatch",
    )
    require(
        partial_approval_payload["required_operator_approval"]["obtained"] is False,
        "partial-fill runtime approval obtained mismatch",
    )
    require(
        partial_approval_payload["negative_assertions"]["new_order_submitted"] is False,
        "partial-fill runtime approval new order flag mismatch",
    )
    require(
        partial_approval_payload["negative_assertions"]["cancel_sent"] is False,
        "partial-fill runtime approval cancel flag mismatch",
    )

    partial_bundle_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-runtime-execution-handoff-bundle"
    )
    require(
        partial_bundle_response.status_code == 200,
        f"partial-fill runtime handoff bundle status mismatch: {partial_bundle_response.status_code}",
    )
    partial_bundle_payload = partial_bundle_response.json()
    require(
        partial_bundle_payload["schema"] == "account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1",
        "partial-fill runtime handoff bundle schema mismatch",
    )
    require(
        partial_bundle_payload["status"] == "phase4k_partial_fill_runtime_execution_handoff_bundle_ready",
        "partial-fill runtime handoff bundle status mismatch",
    )
    require(
        partial_bundle_payload["execution_guard"]["execution_allowed"] is False,
        "partial-fill runtime handoff execution allowed mismatch",
    )
    require(
        partial_bundle_payload["negative_assertions"]["new_order_submitted"] is False,
        "partial-fill runtime handoff new order flag mismatch",
    )
    require(
        partial_bundle_payload["negative_assertions"]["cancel_sent"] is False,
        "partial-fill runtime handoff cancel flag mismatch",
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
        repair_plan_response.status_code == 200,
        f"partial-fill owner repair plan status mismatch: {repair_plan_response.status_code}",
    )
    repair_plan_payload = repair_plan_response.json()
    require(
        repair_plan_payload["schema"] == "account-console.p024.partial-fill-owner-repair-implementation-plan.v1",
        "partial-fill owner repair plan schema mismatch",
    )
    require(
        repair_plan_payload["status"] == "phase4r_owner_close_offset_repair_implementation_plan_ready",
        "partial-fill owner repair plan status mismatch",
    )
    require(
        repair_plan_payload["owner_read_context"]["owner_repo_write_attempted"] is False,
        "partial-fill owner repair plan write flag mismatch",
    )
    require(
        repair_plan_payload["post_repair_runtime_attempt_gate"]["runtime_attempt_allowed_by_this_plan"] is False,
        "partial-fill owner repair plan retry flag mismatch",
    )
    require(
        repair_plan_payload["negative_assertions"]["partial_fill_claimed"] is False,
        "partial-fill owner repair plan claim mismatch",
    )

    ingest_gate_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-evidence-ingest-gate"
    )
    require(
        ingest_gate_response.status_code == 200,
        f"partial-fill owner repair ingest gate status mismatch: {ingest_gate_response.status_code}",
    )
    ingest_gate_payload = ingest_gate_response.json()
    require(
        ingest_gate_payload["schema"] == "account-console.p024.partial-fill-owner-repair-evidence-ingest-gate.v1",
        "partial-fill owner repair ingest gate schema mismatch",
    )
    require(
        ingest_gate_payload["status"] == "phase4t_owner_repair_evidence_ingest_gate_ready",
        "partial-fill owner repair ingest gate status mismatch",
    )
    require(
        ingest_gate_payload["ingest_scope"]["runtime_retry_allowed_by_ingest_gate"] is False,
        "partial-fill owner repair ingest gate retry flag mismatch",
    )
    require(
        len(ingest_gate_payload["required_owner_repair_evidence"]) == 6,
        "partial-fill owner repair ingest gate evidence count mismatch",
    )
    require(
        ingest_gate_payload["negative_assertions"]["owner_repair_evidence_recorded"] is False,
        "partial-fill owner repair ingest gate recorded flag mismatch",
    )

    preflight_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-preflight-source-audit"
    )
    require(
        preflight_response.status_code == 200,
        f"partial-fill owner repair preflight status mismatch: {preflight_response.status_code}",
    )
    preflight_payload = preflight_response.json()
    require(
        preflight_payload["schema"] == "account-console.p024.partial-fill-owner-repair-preflight-source-audit.v1",
        "partial-fill owner repair preflight schema mismatch",
    )
    require(
        preflight_payload["status"] == "phase4v_owner_repair_preflight_source_audited",
        "partial-fill owner repair preflight status mismatch",
    )
    require(
        preflight_payload["operator_approval_delta"]["sufficient_for_owner_code_repair"] is False,
        "partial-fill owner repair preflight repair approval mismatch",
    )
    require(
        preflight_payload["operator_approval_delta"]["sufficient_for_post_repair_runtime_retry"] is False,
        "partial-fill owner repair preflight retry approval mismatch",
    )
    require(
        preflight_payload["next_required_action"]["blind_script_retry_rejected"] is True,
        "partial-fill owner repair preflight blind retry mismatch",
    )
    require(
        preflight_payload["negative_assertions"]["owner_runtime_invocation_attempted"] is False,
        "partial-fill owner repair preflight invocation flag mismatch",
    )

    patch_preview_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-patch-preview"
    )
    require(
        patch_preview_response.status_code == 200,
        f"partial-fill owner repair patch preview status mismatch: {patch_preview_response.status_code}",
    )
    patch_preview_payload = patch_preview_response.json()
    require(
        patch_preview_payload["schema"] == "account-console.p024.partial-fill-owner-repair-patch-preview.v1",
        "partial-fill owner repair patch preview schema mismatch",
    )
    require(
        patch_preview_payload["status"] == "phase4x_owner_repair_patch_preview_ready",
        "partial-fill owner repair patch preview status mismatch",
    )
    require(
        patch_preview_payload["owner_baseline"]["owner_repo_write_attempted_by_preview"] is False,
        "partial-fill owner repair patch preview write flag mismatch",
    )
    require(
        len(patch_preview_payload["previewed_owner_patch"]) == 3,
        "partial-fill owner repair patch preview patch count mismatch",
    )
    require(
        patch_preview_payload["post_patch_runtime_gate"]["runtime_retry_authorized_by_preview"] is False,
        "partial-fill owner repair patch preview retry flag mismatch",
    )
    require(
        patch_preview_payload["negative_assertions"]["owner_patch_applied"] is False,
        "partial-fill owner repair patch preview applied flag mismatch",
    )

    repair_handoff_response = client.get(
        f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-execution-handoff-bundle"
    )
    require(
        repair_handoff_response.status_code == 200,
        f"partial-fill owner repair execution handoff status mismatch: {repair_handoff_response.status_code}",
    )
    repair_handoff_payload = repair_handoff_response.json()
    require(
        repair_handoff_payload["schema"] == "account-console.p024.partial-fill-owner-repair-execution-handoff-bundle.v1",
        "partial-fill owner repair execution handoff schema mismatch",
    )
    require(
        repair_handoff_payload["status"] == "phase4z_owner_repair_execution_handoff_bundle_ready",
        "partial-fill owner repair execution handoff status mismatch",
    )
    require(
        repair_handoff_payload["execution_guard"]["execution_allowed"] is False,
        "partial-fill owner repair execution handoff execution flag mismatch",
    )
    require(
        repair_handoff_payload["execution_guard"]["owner_repo_write_allowed_by_this_bundle"] is False,
        "partial-fill owner repair execution handoff owner write flag mismatch",
    )
    require(
        repair_handoff_payload["execution_guard"]["runtime_retry_authorized_by_this_bundle"] is False,
        "partial-fill owner repair execution handoff retry flag mismatch",
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
        "phase=1 routes=16 status=accepted_for_risk runtime_handoff=blocked runtime_closeout=reconciled runtime_readiness=blocked runtime_approval_packet=ready runtime_handoff_bundle=ready partial_fill_runtime_approval_packet=ready partial_fill_runtime_handoff_bundle=ready runtime_execution_gap=blocked owner_repair_plan=ready owner_repair_ingest_gate=ready owner_repair_preflight=blind_retry_rejected owner_repair_patch_preview=ready owner_repair_execution_handoff=ready mirror_read_only=true"
    )


if __name__ == "__main__":
    main()
