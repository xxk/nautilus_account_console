from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.account_mirror import AccountMirrorStore  # noqa: E402
from nautilus_account_console.source_bridge import load_capability_bundles, validate_route_context  # noqa: E402


EXPECTED_ACCOUNTS = {
    "acct.nautilus.paper.demo",
    "acct.ctp.paper.19053",
    "acct.ctp.live.025292",
}


def main() -> None:
    store = AccountMirrorStore()
    projections = store.list_projections_from_bundles(load_capability_bundles())
    account_ids = {projection.account_id for projection in projections}
    missing = EXPECTED_ACCOUNTS - account_ids
    if missing:
        raise AssertionError(f"missing mirror projections: {sorted(missing)}")

    for projection in projections:
        payload = projection.to_dict()
        assert payload["schema_version"] == "account_mirror_projection.v1", projection.account_id
        assert payload["account_id"].startswith("acct.") or payload["account_id"] == "simulated-001", projection.account_id
        assert payload["projection_checkpoint_id"].startswith("sha256:"), projection.account_id
        assert payload["projection_checksum"].startswith("sha256:"), projection.account_id
        assert payload["source_ref"], projection.account_id
        assert payload["source_checksum"].startswith("sha256:"), projection.account_id
        validate_route_context(payload["route_context"], projection.account_id)
        assert payload["route_context"]["route_id"], projection.account_id
        assert payload["route_context"]["evidence_partition"], projection.account_id
        assert payload["boundaries"]["read_only_projection"] is True, projection.account_id
        for key in [
            "broker_truth",
            "runtime_truth",
            "account_truth",
            "order_action",
            "approval_truth",
            "capital_truth",
            "trading_readiness_truth",
        ]:
            assert payload["boundaries"][key] is False, (projection.account_id, key)
        assert payload["capabilities"]["command"]["enabled"] is False, projection.account_id
        assert payload["capabilities"]["command"]["mode"] == "disabled", projection.account_id
        if projection.account_id == "acct.ctp.paper.19053":
            assert not payload["blockers"], "acct.ctp.paper.19053 should project ready read-only evidence"
            assert payload["source_health"]["state"] == "ready", "acct.ctp.paper.19053 source should be ready"
            assert payload["source_health"]["order_action_sent"] is False, "19053 mirror projection must stay read-only"
        if projection.account_id == "acct.ctp.live.025292":
            assert payload["blockers"], f"{projection.account_id} must remain blocked until pinned source package exists"
            assert payload["source_health"]["state"] == "blocked", f"{projection.account_id} source must not look healthy"
        if projection.account_id == "simulated-001":
            assert payload["route_context"]["market_data_source"] == "ctp_md.025292", projection.account_id
            assert payload["route_context"]["execution_adapter"] != "ctp_td.025292", projection.account_id
            assert payload["route_context"]["account_truth"] != "broker_ctp", projection.account_id

    print(f"ACCOUNT_MIRROR_PROJECTION_OK: projections={len(projections)}")


if __name__ == "__main__":
    main()
