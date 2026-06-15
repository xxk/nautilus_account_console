from fastapi.testclient import TestClient

from nautilus_account_console.main import app


def test_mirror_accounts_api_lists_bridged_accounts() -> None:
    client = TestClient(app)
    response = client.get("/api/mirror/accounts")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "account_mirror_list.v1"
    assert {row["account_id"] for row in payload["accounts"]} == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
        "simulated-001",
    }


def test_mirror_account_detail_is_read_only_and_provenanced() -> None:
    client = TestClient(app)
    response = client.get("/api/mirror/accounts/acct.ctp.paper.19053")

    assert response.status_code == 200
    payload = response.json()
    assert payload["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}
    assert payload["capabilities"]["observation"]["mirror_state"] == "blocked"
    assert payload["source_ref"].endswith("output/account_capability/ctp-paper-19053/source-package.json")
    assert payload["blockers"][0]["blocker_id"] == "ctp19053_real_login_source_unavailable"
    assert payload["positions"] == []
    assert payload["orders"] == []
    assert payload["boundaries"]["read_only_projection"] is True
    assert payload["boundaries"]["order_action"] is False


def test_mirror_api_shows_unbridged_live_025292_as_blocked_projection() -> None:
    client = TestClient(app)
    response = client.get("/api/mirror/accounts/acct.ctp.live.025292")

    assert response.status_code == 200
    payload = response.json()
    assert payload["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}
    assert payload["capabilities"]["observation"]["mirror_state"] == "blocked"
    assert payload["blockers"][0]["type"] == "source_unavailable"
    assert payload["blockers"][0]["blocker_id"] == "ctp025292_real_login_source_unavailable"
    assert payload["source_ref"].endswith("output/account_capability/ctp-live-025292/source-package.json")
    assert payload["boundaries"]["order_action"] is False


def test_simulated_001_is_stage2_market_data_only_sandbox_paper_projection() -> None:
    client = TestClient(app)
    response = client.get("/api/mirror/accounts/simulated-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["account_id"] == "simulated-001"
    assert payload["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}
    assert payload["boundaries"]["order_action"] is False
    health = payload["source_health"]
    assert health["account_uid"] == "sandbox-paper.simulated-001"
    assert health["account_type"] == "sandbox_paper"
    assert health["ledger_type"] == "simulated_sandbox_ledger"
    assert health["market_data_account_id"] == "025292"
    assert health["market_data_role"] == "market_data_only"
    assert health["execution_target"] == "Nautilus Sandbox Paper"
    assert health["orders_scope"] == "simulated ledger only"
    assert health["broker_order_submission"] is False
    assert health["trading_adapter"] == "disabled"
    assert health["account_console_writes_truth"] is False


def test_mirror_source_health_and_evidence_are_structured() -> None:
    client = TestClient(app)

    health = client.get("/api/mirror/accounts/acct.ctp.paper.19053/source-health")
    assert health.status_code == 200
    health_payload = health.json()
    assert health_payload["schema_version"] == "account_mirror_source_health.v1"
    assert health_payload["state"] == "blocked"
    assert health_payload["source_ref"].endswith("output/account_capability/ctp-paper-19053/source-package.json")
    assert health_payload["boundaries"]["order_action"] is False

    evidence = client.get("/api/mirror/accounts/acct.ctp.paper.19053/evidence")
    assert evidence.status_code == 200
    evidence_payload = evidence.json()
    assert evidence_payload["schema_version"] == "account_mirror_evidence.v1"
    assert {item["kind"] for item in evidence_payload["evidence"]} >= {
        "source_package",
        "mirror_projection",
    }
    assert evidence_payload["projection_checksum"].startswith("sha256:")
    assert evidence_payload["boundaries"]["read_only_projection"] is True
