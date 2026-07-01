from pathlib import Path
import json

import pytest

from nautilus_account_console.account_mirror import AccountMirrorStore
from nautilus_account_console.source_bridge import (
    DEFAULT_ARTIFACT_DIR,
    SourceBridgeError,
    load_capability_bundles,
    load_source_artifact,
    validate_route_context,
)


def test_source_bridge_emits_ready_read_only_bundles() -> None:
    bundles = load_capability_bundles()
    account_ids = {bundle["account"]["account_id"] for bundle in bundles}

    assert account_ids == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
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


def test_source_bridge_bundles_project_through_account_mirror() -> None:
    projections = AccountMirrorStore().list_projections_from_bundles(load_capability_bundles())

    assert {projection.account_id for projection in projections} == {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
        "simulated-001",
    }
    states = {projection.account_id: projection.source_health["state"] for projection in projections}
    assert states["acct.nautilus.paper.demo"] == "ready"
    assert states["simulated-001"] == "ready"
    assert states["acct.ctp.paper.19053"] == "blocked"
    assert states["acct.ctp.live.025292"] == "blocked"


def test_source_bridge_rejects_command_bearing_source_artifact() -> None:
    with pytest.raises(SourceBridgeError):
        load_source_artifact(Path(DEFAULT_ARTIFACT_DIR) / "invalid_direct_command_source.json")


def test_source_bridge_rejects_missing_route_context_instead_of_fallback(tmp_path: Path) -> None:
    source_path = Path(DEFAULT_ARTIFACT_DIR) / "nautilus_paper_demo_source.json"
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    payload.pop("route_context", None)
    candidate = tmp_path / "missing-route-context.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SourceBridgeError, match="route_context"):
        load_source_artifact(candidate)


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
