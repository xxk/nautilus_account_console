from __future__ import annotations

from copy import deepcopy

from fastapi.testclient import TestClient

from nautilus_account_console.main import app


def submit_intent() -> dict:
    return {
        "schema_version": "account_command.order_intent.v1",
        "intent_id": "intent.p024.submit.rb2610.001",
        "account_id": "acct.ctp.paper.19053",
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
        "idempotency_key": "p024-submit-rb2610-001",
        "operator_ref": "operator://local/p024-contract-test",
        "preflight_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/closeout_manifest.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }


def cancel_intent() -> dict:
    return {
        "schema_version": "account_command.cancel_intent.v1",
        "intent_id": "intent.p024.cancel.rb2610.001",
        "account_id": "acct.ctp.paper.19053",
        "mode": "paper_armed",
        "action": "cancel",
        "instrument": "rb2610",
        "exchange": "SHFE",
        "client_order_id": "p024-rb2610-001",
        "venue_order_id": "ctp19053-order-001",
        "order_ref": "37",
        "front_id": 1,
        "session_id": 1,
        "idempotency_key": "p024-cancel-rb2610-001",
        "operator_ref": "operator://local/p024-contract-test",
        "readback_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }


def assert_pre_gateway_result(payload: dict, action: str) -> None:
    assert payload["schema_version"] == "account_command.command_api_result.v1"
    assert payload["proposal_id"] == "p024-account-console-paper-command-controls"
    assert payload["account_id"] == "acct.ctp.paper.19053"
    assert payload["action"] == action
    assert payload["mode"] == "paper_armed"
    assert payload["status"] == "accepted_for_risk"
    assert payload["command_id"].startswith(f"command.p024.{action}.")
    assert payload["intent_ref"].startswith("api://p024/acct-ctp-paper-19053/")
    assert payload["idempotency_enforced"] is True
    assert payload["next_required_stage"] == "risk_decision"
    assert {blocker["type"] for blocker in payload["blockers"]} == {
        "risk_decision_required",
        "approval_decision_required",
    }
    assert payload["gateway_event_refs"] == []
    assert payload["gateway_ack_is_final_state"] is False
    assert payload["gateway_send_attempted"] is False
    assert payload["broker_order_created"] is False
    assert payload["runtime_duplicate_send_attempted"] is False
    assert payload["raw_secret_values_recorded"] is False
    assert payload["raw_broker_endpoint_recorded"] is False


def test_submit_intent_accepts_paper_armed_contract_without_gateway_send() -> None:
    client = TestClient(app)
    response = client.post("/api/commands/accounts/acct.ctp.paper.19053/submit-intents", json=submit_intent())

    assert response.status_code == 202
    payload = response.json()
    assert_pre_gateway_result(payload, "submit")
    assert "risk_decision_ref" not in payload
    assert "approval_decision_ref" not in payload
    assert payload["readback_refs"] == []


def test_submit_intent_is_idempotent_by_key() -> None:
    client = TestClient(app)
    first = client.post("/api/commands/accounts/acct.ctp.paper.19053/submit-intents", json=submit_intent())
    second = client.post("/api/commands/accounts/acct.ctp.paper.19053/submit-intents", json=submit_intent())

    assert first.status_code == 202
    assert second.status_code == 202
    assert second.json() == first.json()
    assert second.json()["runtime_duplicate_send_attempted"] is False


def test_cancel_intent_requires_readback_identity_and_stays_pre_gateway() -> None:
    client = TestClient(app)
    response = client.post("/api/commands/accounts/acct.ctp.paper.19053/cancel-intents", json=cancel_intent())

    assert response.status_code == 202
    payload = response.json()
    assert_pre_gateway_result(payload, "cancel")
    assert payload["readback_refs"] == [
        "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json"
    ]


def test_runtime_closeout_reads_reconciled_owner_artifacts_without_browser_send() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/commands/accounts/acct.ctp.paper.19053/runtime-closeouts/p023-armed-20260621t0748z"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "account_command.runtime_closeout.v1"
    assert payload["proposal_id"] == "p024-account-console-paper-command-controls"
    assert payload["account_id"] == "acct.ctp.paper.19053"
    assert payload["run_id"] == "p023-armed-20260621t0748z"
    assert payload["mode"] == "paper_armed"
    assert payload["status"] == "reconciled"
    assert payload["runtime_gateway_send_observed"] is True
    assert payload["broker_order_created"] is True
    assert payload["browser_triggered_broker_order"] is False
    assert payload["gateway_ack_is_final_state"] is False
    assert payload["raw_secret_values_recorded"] is False
    assert payload["raw_broker_endpoint_recorded"] is False
    assert len(payload["intent_refs"]) == 2
    assert len(payload["risk_decision_refs"]) == 2
    assert len(payload["approval_decision_refs"]) == 2
    assert len(payload["gateway_event_refs"]) == 2
    assert len(payload["readback_refs"]) == 2
    assert payload["reconciliation_ref"].endswith("reconciliation_result.json")
    assert payload["closeout_manifest_checksum"].startswith("sha256:")
    assert payload["command_audit_checksum"].startswith("sha256:")
    assert payload["artifact_checksums"][payload["command_audit_ref"]] == payload["command_audit_checksum"]
    assert "web_ui_trigger_of_new_runtime_order_still_pending" in payload["explicit_non_claims"]


def test_runtime_closeout_rejects_scope_and_unsafe_run_id() -> None:
    client = TestClient(app)
    wrong_account = client.get(
        "/api/commands/accounts/acct.ctp.live.025292/runtime-closeouts/p023-armed-20260621t0748z"
    )
    assert wrong_account.status_code == 403

    unsafe = client.get("/api/commands/accounts/acct.ctp.paper.19053/runtime-closeouts/bad%20run")
    assert unsafe.status_code == 400


def assert_runtime_run_request(payload: dict, action: str) -> None:
    assert payload["schema_version"] == "account_command.owner_runtime_run_request.v1"
    assert payload["proposal_id"] == "p024-account-console-paper-command-controls"
    assert payload["account_id"] == "acct.ctp.paper.19053"
    assert payload["action"] == action
    assert payload["mode"] == "paper_armed"
    assert payload["status"] == "blocked_until_owner_runtime_invocation"
    assert payload["command_id"].startswith(f"command.p024.{action}.")
    assert payload["intent_ref"].startswith("api://p024/acct-ctp-paper-19053/")
    assert payload["owner_runtime_owner_ref"] == "owner://nautilus_ctp_adapter"
    assert payload["owner_runtime_repo_ref"] == "owner-repo://nautilus_ctp_adapter"
    assert payload["owner_runtime_config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json"
    assert payload["runtime_invocation_attempted"] is False
    assert payload["browser_triggered_broker_order"] is False
    assert payload["gateway_send_attempted"] is False
    assert payload["broker_order_created"] is False
    assert payload["raw_secret_values_recorded"] is False
    assert payload["raw_broker_endpoint_recorded"] is False
    assert payload["external_write_approval_required"] is True
    assert payload["run_request_checksum"].startswith("sha256:")
    assert {blocker["type"] for blocker in payload["blockers"]} == {
        "owner_runtime_invocation_required",
        "external_write_approval_required",
        "post_run_ingest_required",
    }
    assert "does_not_invoke_owner_runtime" in payload["explicit_non_claims"]
    assert "does_not_send_broker_order_from_browser" in payload["explicit_non_claims"]


def test_submit_runtime_run_request_prepares_owner_handoff_without_invocation() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/commands/accounts/acct.ctp.paper.19053/runtime-run-requests/submit",
        json=submit_intent(),
    )

    assert response.status_code == 202
    payload = response.json()
    assert_runtime_run_request(payload, "submit")
    assert payload["owner_runtime_entrypoint_ref"] == "scripts/ctp_guarded_paper_order_loop.py"
    assert payload["source_preflight_ref"] == submit_intent()["preflight_ref"]
    assert "readback_ref" not in payload


def test_cancel_runtime_run_request_prepares_owner_handoff_without_invocation() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/commands/accounts/acct.ctp.paper.19053/runtime-run-requests/cancel",
        json=cancel_intent(),
    )

    assert response.status_code == 202
    payload = response.json()
    assert_runtime_run_request(payload, "cancel")
    assert payload["owner_runtime_entrypoint_ref"] == "scripts/ctp_guarded_paper_cancel_loop.py"
    assert payload["source_preflight_ref"] == cancel_intent()["readback_ref"]
    assert payload["readback_ref"] == cancel_intent()["readback_ref"]


def test_runtime_invocation_readiness_projects_external_approval_blocker() -> None:
    client = TestClient(app)
    response = client.get("/api/commands/accounts/acct.ctp.paper.19053/runtime-invocation-readiness")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1"
    assert payload["status"] == "blocked_waiting_for_external_owner_runtime_write_approval"
    assert payload["owner_runtime"]["owner_ref"] == "owner://nautilus_ctp_adapter"
    assert payload["owner_runtime"]["config_raw_content_read"] is False
    assert payload["external_write_approval_request"]["required"] is True
    assert payload["external_write_approval_request"]["obtained"] is False
    assert payload["negative_assertions"]["runtime_invocation_attempted"] is False
    assert payload["negative_assertions"]["owner_repo_write_attempted"] is False
    assert payload["negative_assertions"]["browser_triggered_broker_order"] is False
    assert {blocker["type"] for blocker in payload["blockers"]} == {
        "external_write_approval_required",
        "owner_runtime_artifacts_missing",
    }


def test_runtime_execution_approval_packet_projects_exact_operator_gate() -> None:
    client = TestClient(app)
    response = client.get("/api/commands/accounts/acct.ctp.paper.19053/runtime-execution-approval-packet")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1"
    assert payload["status"] == "phase4a_owner_runtime_execution_approval_packet_ready"
    assert payload["verdict"] == "approval_packet_ready_runtime_not_invoked"
    assert payload["required_operator_approval"]["required"] is True
    assert payload["required_operator_approval"]["obtained"] is False
    assert payload["required_operator_approval"]["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter"
    assert "I approve writes to D:/Nautilus/nautilus_ctp_adapter" in payload["required_operator_approval"]["exact_approval_text"]
    assert payload["planned_execution"]["runtime_invocation_attempted"] is False
    assert payload["planned_execution"]["owner_repo_write_attempted"] is False
    assert {entrypoint["armed_flag"] for entrypoint in payload["entrypoints"]} == {
        "--arm-paper-send",
        "--arm-cancel-send",
    }
    assert payload["negative_assertions"]["runtime_invocation_attempted"] is False
    assert payload["negative_assertions"]["broker_order_created"] is False
    assert {blocker["type"] for blocker in payload["blockers"]} == {
        "external_write_approval_required",
        "owner_runtime_artifacts_missing",
    }


def test_runtime_execution_handoff_bundle_projects_blocked_operator_sequence() -> None:
    client = TestClient(app)
    response = client.get("/api/commands/accounts/acct.ctp.paper.19053/runtime-execution-handoff-bundle")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1"
    assert payload["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready"
    assert payload["verdict"] == "handoff_bundle_ready_runtime_not_invoked"
    assert payload["execution_guard"]["execution_allowed"] is False
    assert payload["execution_guard"]["approval_required"] is True
    assert payload["execution_guard"]["approval_obtained"] is False
    assert payload["negative_assertions"]["runtime_invocation_attempted"] is False
    assert payload["negative_assertions"]["owner_repo_write_attempted"] is False
    assert payload["negative_assertions"]["broker_order_created"] is False
    assert {item["field"] for item in payload["runtime_input_requirements"]} >= {
        "owner_pre_snapshot_ref",
        "owner_post_snapshot_ref",
        "instrument",
        "side",
        "qty",
        "price",
        "readback_order_identity",
    }
    assert [item["step"] for item in payload["operator_sequence"]][:3] == [
        "pre_approval_gate",
        "owner_repo_context",
        "submit_runtime",
    ]
    assert {blocker["type"] for blocker in payload["blockers"]} == {
        "external_write_approval_required",
        "runtime_inputs_required",
        "owner_runtime_artifacts_missing",
    }


def test_partial_fill_runtime_execution_approval_packet_projects_exact_operator_gate() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/commands/accounts/acct.ctp.paper.19053/partial-fill-runtime-execution-approval-packet"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.partial-fill-runtime-execution-approval-packet.v1"
    assert payload["status"] == "phase4j_partial_fill_runtime_execution_approval_packet_ready"
    assert payload["required_operator_approval"]["required"] is True
    assert payload["required_operator_approval"]["obtained"] is False
    assert "P024 partial-fill acceptance" in payload["required_operator_approval"]["exact_approval_text"]
    assert payload["attempt_constraints"]["risk_shape"] == "exposure_reduction_only"
    assert payload["attempt_constraints"]["maximum_submit_attempts"] == 1
    assert payload["attempt_constraints"]["maximum_order_quantity"] == 3
    assert payload["attempt_constraints"]["partial_fill_success_formula"] == "0 < filled_quantity < submitted_quantity"
    assert payload["planned_execution"]["runtime_invocation_attempted"] is False
    assert payload["planned_execution"]["owner_repo_write_attempted"] is False
    assert payload["planned_execution"]["new_order_submitted"] is False
    assert payload["planned_execution"]["cancel_sent"] is False
    assert payload["negative_assertions"]["approval_obtained"] is False
    assert payload["negative_assertions"]["new_order_submitted"] is False
    assert payload["negative_assertions"]["browser_fixture_promoted_to_runtime_truth"] is False


def test_partial_fill_runtime_execution_handoff_bundle_projects_blocked_sequence() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/commands/accounts/acct.ctp.paper.19053/partial-fill-runtime-execution-handoff-bundle"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1"
    assert payload["status"] == "phase4k_partial_fill_runtime_execution_handoff_bundle_ready"
    assert payload["execution_guard"]["execution_allowed"] is False
    assert payload["execution_guard"]["approval_required"] is True
    assert payload["execution_guard"]["approval_obtained"] is False
    assert "P024 partial-fill acceptance" in payload["execution_guard"]["exact_approval_text_required"]
    inputs = {item["field"]: item for item in payload["runtime_input_requirements"]}
    assert inputs["quantity"]["allowed_values"] == [2, 3]
    assert [item["step"] for item in payload["operator_sequence"]][:3] == [
        "pre_approval_gate",
        "owner_pre_snapshot",
        "submit_partial_fill_attempt",
    ]
    assert "0 < filled_quantity < submitted_quantity" in payload["success_criteria"]["non_ui_runtime"]
    assert "cancel pending is not rendered as final" in payload["success_criteria"]["web_ui_runtime"]
    assert set(payload["fallback_classifications"]) == {
        "fully_filled_not_partial_fill_then_cancel",
        "cancelled_without_fill_not_partial_fill",
        "rejected_or_timeout_not_partial_fill",
        "owner_runtime_artifact_incomplete",
    }
    assert payload["negative_assertions"]["execution_allowed"] is False
    assert payload["negative_assertions"]["new_order_submitted"] is False
    assert payload["negative_assertions"]["cancel_sent"] is False
    assert payload["negative_assertions"]["full_acceptance_claimed"] is False


def test_runtime_execution_gap_audit_projects_final_acceptance_blocker() -> None:
    client = TestClient(app)
    response = client.get("/api/commands/accounts/acct.ctp.paper.19053/runtime-execution-gap-audit")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.runtime-execution-gap-audit.v1"
    assert payload["status"] == "phase4e_final_runtime_execution_gap_audited"
    assert payload["verdict"] == "blocked_pending_owner_runtime_execution"
    assert "A4" not in payload["accepted_scenarios"]
    assert [item["id"] for item in payload["not_accepted_scenarios"]] == ["A4"]
    assert payload["external_write_approval"]["required"] is True
    assert payload["external_write_approval"]["obtained"] is False
    assert payload["negative_assertions"]["final_acceptance_claimed"] is False
    assert payload["negative_assertions"]["runtime_invocation_attempted"] is False
    assert payload["negative_assertions"]["owner_repo_write_attempted"] is False
    assert payload["negative_assertions"]["broker_order_created"] is False
    assert {blocker["type"] for blocker in payload["residual_blockers"]} == {
        "external_write_approval_required",
        "owner_runtime_artifacts_missing",
        "owner_runtime_partial_fill_state_missing",
    }


def test_partial_fill_owner_repair_plan_projects_no_retry_gate() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/commands/accounts/acct.ctp.paper.19053/partial-fill-owner-repair-implementation-plan"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema"] == "account-console.p024.partial-fill-owner-repair-implementation-plan.v1"
    assert payload["status"] == "phase4r_owner_close_offset_repair_implementation_plan_ready"
    assert payload["verdict"] == "owner_repair_plan_ready_no_owner_write_attempted"
    assert payload["owner_read_context"]["owner_repo_write_attempted"] is False
    assert len(payload["planned_owner_changes_after_exact_approval"]) == 3
    assert [item["change_id"] for item in payload["planned_owner_changes_after_exact_approval"]] == [
        "owner_rule_generalize_close_offset_submit_observed",
        "owner_rule_wording_include_close_yesterday",
        "focused_close_yesterday_test",
    ]
    assert {item["stage"] for item in payload["post_repair_validator_sequence"]} == {
        "owner_unit_focus",
        "owner_integration_regression",
        "account_console_repair_plan_gate",
        "account_console_design_gate",
    }
    assert payload["post_repair_runtime_attempt_gate"]["runtime_attempt_allowed_by_this_plan"] is False
    assert payload["negative_assertions"]["owner_repo_write_attempted_by_this_plan"] is False
    assert payload["negative_assertions"]["runtime_retry_authorized"] is False
    assert payload["negative_assertions"]["partial_fill_claimed"] is False


def test_command_api_rejects_live_mode_and_account_mismatch() -> None:
    client = TestClient(app)
    live = deepcopy(submit_intent())
    live["mode"] = "live_armed"
    live_response = client.post("/api/commands/accounts/acct.ctp.paper.19053/submit-intents", json=live)
    assert live_response.status_code == 403
    assert "paper_armed" in live_response.json()["detail"]

    mismatch = deepcopy(submit_intent())
    mismatch_response = client.post("/api/commands/accounts/acct.ctp.live.025292/submit-intents", json=mismatch)
    assert mismatch_response.status_code == 409


def test_command_api_rejects_missing_idempotency_or_cancel_identity() -> None:
    client = TestClient(app)
    missing_idempotency = deepcopy(submit_intent())
    missing_idempotency.pop("idempotency_key")
    idempotency_response = client.post(
        "/api/commands/accounts/acct.ctp.paper.19053/submit-intents",
        json=missing_idempotency,
    )
    assert idempotency_response.status_code == 422

    missing_identity = deepcopy(cancel_intent())
    missing_identity.pop("venue_order_id")
    identity_response = client.post(
        "/api/commands/accounts/acct.ctp.paper.19053/cancel-intents",
        json=missing_identity,
    )
    assert identity_response.status_code == 422


def test_account_mirror_routes_remain_read_only() -> None:
    client = TestClient(app)
    response = client.post("/api/mirror/accounts/acct.ctp.paper.19053/orders", json={})
    assert response.status_code == 405
