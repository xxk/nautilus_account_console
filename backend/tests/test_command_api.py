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
