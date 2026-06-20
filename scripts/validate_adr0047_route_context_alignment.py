from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.account_mirror import AccountMirrorStore  # noqa: E402
from nautilus_account_console.main import app  # noqa: E402
from nautilus_account_console.source_bridge import (  # noqa: E402
    SourceBridgeError,
    load_capability_bundles,
    validate_route_context,
)


EXPECTED_ROUTE_CONTEXT = {
    "acct.nautilus.paper.demo": {
        "risk_domain": "sandbox",
        "market_data_source": "not_in_scope_for_account_readback",
    },
    "acct.ctp.paper.19053": {
        "route_id": "route.ctp.paper.19053.account-readonly",
        "risk_domain": "paper",
        "account_truth": "blocked_until_pinned_source_package",
    },
    "acct.ctp.live.025292": {
        "route_id": "route.ctp.live.025292.account-readonly",
        "risk_domain": "live",
        "account_truth": "blocked_until_pinned_source_package",
    },
    "simulated-001": {
        "route_id": "route.p079.stage2.simulated-001",
        "market_data_source": "ctp_md.025292",
        "execution_adapter": "nautilus_sandbox_paper_simulated_runtime",
        "account_truth": "nautilus_sandbox_paper_simulated_ledger",
        "risk_domain": "sandbox",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_context(account_id: str, route_context: dict) -> None:
    validate_route_context(route_context, account_id)
    expected = EXPECTED_ROUTE_CONTEXT[account_id]
    for key, value in expected.items():
        require(route_context[key] == value, f"{account_id} route_context.{key} drifted")
    require(route_context["route_id"], f"{account_id} route_id missing")
    require(route_context["account_alias"], f"{account_id} account_alias missing")
    require(route_context["evidence_partition"], f"{account_id} evidence_partition missing")
    require(route_context["context_ref"], f"{account_id} context_ref missing")
    require(route_context["context_checksum"].startswith("sha256:"), f"{account_id} context checksum invalid")


def require_negative_contexts() -> None:
    bad_market_data_to_execution = {
        "state": "projected",
        "route_id": "route.bad.025292",
        "account_alias": "bad-025292",
        "market_data_source": "ctp_md.025292",
        "execution_adapter": "ctp_td.025292",
        "account_truth": "nautilus_sandbox_paper_simulated_ledger",
        "risk_domain": "sandbox",
        "evidence_partition": "bad/025292",
        "context_ref": "contracts/source_artifacts/account_sources/bad.json",
        "context_checksum": "sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "blocker_id": None,
    }
    bad_market_data_to_truth = {
        **bad_market_data_to_execution,
        "execution_adapter": "nautilus_sandbox_paper_simulated_runtime",
        "account_truth": "broker_ctp",
    }
    for bad in [bad_market_data_to_execution, bad_market_data_to_truth]:
        try:
            validate_route_context(bad, "simulated-001")
        except SourceBridgeError:
            continue
        raise AssertionError(f"invalid route context unexpectedly passed: {bad}")


def main() -> None:
    bundles = load_capability_bundles()
    account_ids = {bundle["account"]["account_id"] for bundle in bundles}
    require(account_ids == set(EXPECTED_ROUTE_CONTEXT), f"account set drifted: {sorted(account_ids)}")

    for bundle in bundles:
        account_id = bundle["account"]["account_id"]
        require_context(account_id, bundle["route_context"])
        require(bundle["boundaries"]["read_only_projection"] is True, account_id)
        for boundary in [
            "broker_truth",
            "runtime_truth",
            "account_truth",
            "order_action",
            "approval_truth",
            "capital_truth",
            "trading_readiness_truth",
        ]:
            require(bundle["boundaries"][boundary] is False, f"{account_id} boundary {boundary} drifted")

    projections = AccountMirrorStore().list_projections_from_bundles(bundles)
    for projection in projections:
        payload = projection.to_dict()
        require_context(projection.account_id, payload["route_context"])

    client = TestClient(app)
    account_list = client.get("/api/mirror/accounts")
    require(account_list.status_code == 200, "mirror list API failed")
    for row in account_list.json()["accounts"]:
        require(row["route_id"] == EXPECTED_ROUTE_CONTEXT[row["account_id"]].get("route_id", row["route_id"]), row["account_id"])
        require(row["evidence_partition"], f"{row['account_id']} list evidence_partition missing")

    for account_id in EXPECTED_ROUTE_CONTEXT:
        detail = client.get(f"/api/mirror/accounts/{account_id}")
        require(detail.status_code == 200, f"{account_id} detail API failed")
        payload = detail.json()
        require_context(account_id, payload["route_context"])
        require(payload["capabilities"]["command"]["enabled"] is False, f"{account_id} command enabled")
        require(payload["boundaries"]["trading_readiness_truth"] is False, f"{account_id} readiness truth drifted")

    require_negative_contexts()
    print("ADR0047_ROUTE_CONTEXT_ALIGNMENT_OK: accounts=4 route_contexts=4 negatives=2")


if __name__ == "__main__":
    main()
