from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.account_mirror import AccountMirrorStore  # noqa: E402
from nautilus_account_console.source_bridge import (  # noqa: E402
    DEFAULT_ARTIFACT_DIR,
    SourceBridgeError,
    load_capability_bundles,
    load_source_artifact,
)


EXPECTED_ACCOUNTS = {
    "acct.nautilus.paper.demo",
    "acct.ctp.paper.19053",
    "acct.ctp.live.025292",
    "simulated-001",
}


def main() -> None:
    bundles = load_capability_bundles()
    account_ids = {bundle["account"]["account_id"] for bundle in bundles}
    missing = EXPECTED_ACCOUNTS - account_ids
    if missing:
        raise AssertionError(f"missing bridged source bundles: {sorted(missing)}")

    for bundle in bundles:
        command = bundle["capabilities"]["command"]
        assert command["enabled"] is False, bundle["account"]["account_id"]
        assert command["mode"] == "disabled", bundle["account"]["account_id"]
        assert bundle["observations"]["source_health"]["source_ref"], bundle["account"]["account_id"]
        if bundle["account"]["account_id"] == "acct.ctp.paper.19053":
            health = bundle["observations"]["source_health"]
            assert health["state"] in {"ready", "blocked"}
            if health["state"] == "blocked":
                assert not bundle["observations"]["balances"]
                assert not bundle["observations"]["positions"]
                assert bundle["observations"]["blockers"][0]["blocker_id"] == "ctp19053_real_login_source_unavailable"
        if bundle["account"]["account_id"] == "acct.ctp.live.025292":
            health = bundle["observations"]["source_health"]
            assert health["state"] in {"ready", "blocked"}
            if health["state"] == "blocked":
                assert not bundle["observations"]["balances"]
                assert not bundle["observations"]["positions"]
                assert bundle["observations"]["blockers"][0]["blocker_id"] == "ctp025292_real_login_source_unavailable"
        if bundle["account"]["account_id"] == "simulated-001":
            health = bundle["observations"]["source_health"]
            assert health["account_uid"] == "sandbox-paper.simulated-001"
            assert health["account_type"] == "sandbox_paper"
            assert health["ledger_type"] == "simulated_sandbox_ledger"
            assert health["market_data_account_id"] == "025292"
            assert health["market_data_role"] == "market_data_only"
            assert health["execution_target"] == "Nautilus Sandbox Paper"
            assert health["orders_scope"] == "simulated ledger only"
            assert health["broker_order_submission"] is False
            assert health["trading_adapter"] == "disabled"
            assert health["stage"] == "R1/P079 Stage 2"
            assert health["account_console_writes_truth"] is False
        for bucket in ["balances", "positions", "orders", "fills"]:
            for row in bundle["observations"][bucket]:
                assert row["source_ref"], (bundle["account"]["account_id"], bucket)
                assert row["checksum"].startswith("sha256:"), (bundle["account"]["account_id"], bucket)
                if bundle["account"]["account_id"] == "acct.ctp.paper.19053" and bucket == "orders":
                    assert row["report_provenance_ref"], "19053 order report provenance required"
                    assert row["report_msg_ref"], "19053 order report msg ref required"
                    assert row["report_msg_checksum"].startswith("sha256:"), "19053 order report checksum required"

    projections = AccountMirrorStore().list_projections_from_bundles(bundles)
    projected_ids = {projection.account_id for projection in projections}
    if projected_ids != account_ids:
        raise AssertionError(f"projection mismatch: {sorted(projected_ids)} != {sorted(account_ids)}")
    for projection in projections:
        payload = projection.to_dict()
        assert payload["capabilities"]["command"]["enabled"] is False, projection.account_id
        assert payload["boundaries"]["read_only_projection"] is True, projection.account_id
        assert payload["boundaries"]["order_action"] is False, projection.account_id
        if projection.account_id == "acct.ctp.paper.19053":
            assert payload["source_health"]["state"] in {"ready", "blocked"}, projection.account_id
        elif projection.account_id == "acct.ctp.live.025292":
            assert payload["source_health"]["state"] in {"ready", "blocked"}, projection.account_id
        else:
            assert payload["source_health"]["state"] == "ready", projection.account_id

    invalid_path = DEFAULT_ARTIFACT_DIR / "invalid_direct_command_source.json"
    try:
        load_source_artifact(invalid_path)
    except SourceBridgeError:
        pass
    else:
        raise AssertionError("invalid command-bearing source artifact unexpectedly passed")

    print(f"ACCOUNT_SOURCE_BRIDGES_OK: bundles={len(bundles)} projections={len(projections)}")


if __name__ == "__main__":
    main()
