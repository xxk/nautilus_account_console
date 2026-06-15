from nautilus_account_console.account_mirror import AccountMirrorStore


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
