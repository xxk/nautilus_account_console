from pathlib import Path

import pytest

from nautilus_account_console.account_mirror import AccountMirrorStore
from nautilus_account_console.source_bridge import (
    DEFAULT_ARTIFACT_DIR,
    SourceBridgeError,
    load_capability_bundles,
    load_source_artifact,
    source_artifact_to_capability_bundle,
    validate_route_context,
)


def test_source_bridge_emits_ready_read_only_bundles() -> None:
    bundles = load_capability_bundles()
    account_ids = {bundle["account"]["account_id"] for bundle in bundles}

    assert account_ids == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
        "acct.ib.live.u3028269",
        "simulated-001",
    }
    for bundle in bundles:
        assert bundle["capabilities"]["command"]["enabled"] is False
        assert bundle["capabilities"]["command"]["mode"] == "disabled"
        assert bundle["boundaries"]["order_action"] is False
        assert bundle["route_context"]["route_id"]
        assert bundle["route_context"]["evidence_partition"]
        if bundle["account"]["account_id"] == "simulated-001":
            assert bundle["route_context"]["market_data_source"] == "ctp_md.025292"
            assert bundle["route_context"]["execution_adapter"] == "nautilus_sandbox_paper_simulated_runtime"
            assert bundle["route_context"]["account_truth"] == "nautilus_sandbox_paper_simulated_ledger"
            health = bundle["observations"]["source_health"]
            assert health["account_uid"] == "sandbox-paper.simulated-001"
            assert health["market_data_role"] == "market_data_only"
            assert health["broker_order_submission"] is False
            assert health["trading_adapter"] == "disabled"
            assert any(
                row["instrument"] == "ag2612" and row["net_qty"] == 1
                for row in bundle["observations"]["positions"]
            )
            assert any(
                row["client_order_id"] == "simulated-001-ag2612-buy-1-001"
                and row["instrument"] == "ag2612"
                and row["status"] == "filled"
                for row in bundle["observations"]["orders"]
            )
        if bundle["account"]["account_id"] == "acct.ib.live.u3028269":
            assert bundle["account"]["display_alias"] == "U3028269"
            assert bundle["account"]["source_kind"] == "ib_tws_observation"
            assert bundle["capabilities"]["observation"]["mirror_state"] in {"blocked", "ready"}
            assert bundle["observations"]["source_health"]["api_transport"] == "ib_tws_api"
            assert bundle["observations"]["source_health"]["screenshot_used_for_values"] is False
            assert bundle["observations"]["source_health"]["raw_secret_values_recorded"] is False
            if bundle["capabilities"]["observation"]["mirror_state"] == "ready":
                assert bundle["observations"]["source_health"]["state"] == "ready"
                assert bundle["route_context"]["account_truth"] == "ib_tws_api_source_package"
                assert bundle["observations"]["balances"]
                assert bundle["observations"]["positions"]
            else:
                assert bundle["observations"]["source_health"]["blocker_id"] == "tws_api_readiness_missing"
                assert bundle["route_context"]["account_truth"] == "blocked_until_tws_api_source_package"
                assert bundle["observations"]["balances"] == []
                assert bundle["observations"]["positions"] == []
            assert bundle["observations"]["orders"] == []
            assert bundle["observations"]["fills"] == []
            assert bundle["boundaries"]["broker_truth"] is False


def test_source_bridge_bundles_project_through_account_mirror() -> None:
    projections = AccountMirrorStore().list_projections_from_bundles(load_capability_bundles())

    assert {projection.account_id for projection in projections} == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
        "acct.ib.live.u3028269",
        "simulated-001",
    }
    states = {projection.account_id: projection.source_health["state"] for projection in projections}
    assert states["acct.nautilus.paper.demo"] == "ready"
    assert states["simulated-001"] == "ready"
    assert states["acct.ctp.paper.19053"] == "blocked"
    assert states["acct.ctp.live.025292"] == "blocked"
    assert states["acct.ib.live.u3028269"] in {"blocked", "ready"}


def test_ib_tws_ready_source_package_projects_ready_without_command() -> None:
    source_payload = {
        "schema_version": "account_source_artifact.v1",
        "artifact_id": "source.ib.live.u3028269.synthetic-ready",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "source_owner": "account-console-broker-observation-session",
        "source_kind": "ib_tws_observation",
        "source_mode": "live_observation",
        "account_domain": "live",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": "2026-06-20",
        "query_window_id": "ib-u3028269.synthetic-ready",
        "query_started_at": "2026-06-20T00:00:00Z",
        "query_completed_at": "2026-06-20T00:00:01Z",
        "observed_at": "2026-06-20T00:00:01Z",
        "source_ref": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_source.synthetic.json",
        "source_checksum": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "source_inputs": {
            "readiness_probe": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_readiness.synthetic.json",
            "account_summary_query": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_query_account_summary.synthetic.json",
            "positions_query": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_query_positions.synthetic.json",
        },
        "balances": [
            {
                "currency": "USD",
                "equity": 100000.0,
                "available_cash": 75000.0,
                "margin_used": 25000.0,
                "unrealized_pnl": 123.45,
            }
        ],
        "positions": [
            {
                "instrument": "AAPL",
                "exchange": "SMART",
                "direction": "long",
                "net_qty": 10.0,
                "available_qty": 10.0,
                "avg_price": 180.25,
                "unrealized_pnl": 42.0,
            }
        ],
        "orders": [],
        "fills": [],
        "source_health": {
            "state": "ready",
            "lag_ms": 0,
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "readiness_probe_ref": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_readiness.synthetic.json",
            "account_summary_query_ref": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_query_account_summary.synthetic.json",
            "positions_query_ref": "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_query_positions.synthetic.json",
            "raw_secret_values_recorded": False,
            "screenshot_used_for_values": False,
            "api_transport": "ib_tws_api",
        },
        "blockers": [],
        "boundaries": {
            "raw_secret_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "tws_api_account_query_required": True,
            "order_action_sent": False,
        },
    }

    bundle = source_artifact_to_capability_bundle(source_payload)
    projection = AccountMirrorStore().list_projections_from_bundles([bundle])[0].to_dict()

    assert bundle["capabilities"]["observation"]["mirror_state"] == "ready"
    assert bundle["capabilities"]["command"] == {
        "enabled": False,
        "mode": "disabled",
        "gateway_kind": None,
        "allowed_actions": [],
        "requires_risk_check": True,
        "requires_approval": True,
        "authority_ref": None,
        "capability_checksum": source_payload["source_checksum"],
    }
    assert bundle["route_context"]["account_truth"] == "ib_tws_api_source_package"
    assert bundle["route_context"]["blocker_id"] is None
    assert bundle["boundaries"]["broker_truth"] is False
    assert bundle["boundaries"]["order_action"] is False
    assert projection["capabilities"]["observation"]["mirror_state"] == "ready"
    assert projection["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}
    assert projection["source_health"]["state"] == "ready"
    assert projection["source_health"]["api_transport"] == "ib_tws_api"
    assert projection["balances"][0]["currency"] == "USD"
    assert projection["positions"][0]["instrument"] == "AAPL"
    assert projection["blockers"] == []
    assert projection["boundaries"]["broker_truth"] is False
    assert projection["boundaries"]["order_action"] is False


def test_source_bridge_rejects_command_bearing_source_artifact() -> None:
    with pytest.raises(SourceBridgeError):
        load_source_artifact(Path(DEFAULT_ARTIFACT_DIR) / "invalid_direct_command_source.json")


def test_route_context_rejects_market_data_as_account_truth() -> None:
    invalid_context = {
        "state": "projected",
        "route_id": "route.bad.025292",
        "account_alias": "bad-025292",
        "market_data_source": "ctp_md.025292",
        "execution_adapter": "ctp_td.025292",
        "account_truth": "broker_ctp",
        "risk_domain": "live",
        "evidence_partition": "bad/025292",
        "context_ref": "contracts/source_artifacts/account_sources/bad.json",
        "context_checksum": "sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "blocker_id": None,
    }

    with pytest.raises(SourceBridgeError):
        validate_route_context(invalid_context, "simulated-001")
