from copy import deepcopy
import json
from pathlib import Path

from nautilus_account_console.account_mirror import AccountMirrorStore


ROOT = Path(__file__).resolve().parents[2]


def test_account_mirror_lists_phase1_capability_projections() -> None:
    store = AccountMirrorStore()
    projections = store.list_projections()

    assert {projection.account_id for projection in projections} >= {
        "acct.nautilus.paper.demo",
        "acct.ctp.paper.19053",
        "acct.ctp.live.025292",
    }


def test_ctp_live_025292_projection_is_blocked_read_only() -> None:
    store = AccountMirrorStore()
    projection = store.get_projection("acct.ctp.live.025292")

    assert projection is not None
    payload = projection.to_dict()
    assert payload["capabilities"]["command"] == {
        "enabled": False,
        "mode": "disabled",
    }
    assert payload["source_health"]["state"] == "blocked"
    assert payload["blockers"]
    assert payload["boundaries"]["read_only_projection"] is True
    assert payload["boundaries"]["order_action"] is False


def test_command_status_is_projected_and_checksum_bound() -> None:
    source_path = ROOT / "contracts" / "ui" / "fixtures" / "account_capability" / "acct_ctp_paper_19053_capability.json"
    bundle = json.loads(source_path.read_text(encoding="utf-8"))
    command_status = {
        "schema_version": "account_command.ui_status_projection.v1",
        "status": "reconciled",
        "command_audit_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/command_audit.json",
        "gateway_ack_is_final_state": False,
        "readback_refs": ["output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/post_submit_readback.json"],
        "reconciliation_ref": "output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/reconciliation_result.json",
    }
    bundle["command_status"] = command_status

    projection = AccountMirrorStore().project_bundle(bundle, "test://command-status")
    payload = projection.to_dict()

    assert payload["command_status"] == command_status
    changed = deepcopy(bundle)
    changed["command_status"]["status"] = "blocked"
    changed_projection = AccountMirrorStore().project_bundle(changed, "test://command-status")
    assert changed_projection.projection_checksum != projection.projection_checksum
