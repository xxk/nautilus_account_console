from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TWS_API_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
ACCOUNT_SUMMARY = TWS_API_DIR / "account_summary.json"
POSITIONS = TWS_API_DIR / "positions.json"
EXECUTIONS = TWS_API_DIR / "executions.json"
OPEN_ORDERS = TWS_API_DIR / "open_orders.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
FIXTURE_DIR = ROOT / "contracts" / "broker_observation" / "fixtures"
SYNTHETIC_ACCOUNT_SUMMARY = FIXTURE_DIR / "ib_tws_u3028269_ready_query_account_summary.synthetic.json"
SYNTHETIC_POSITIONS = FIXTURE_DIR / "ib_tws_u3028269_ready_query_positions.synthetic.json"
SYNTHETIC_READINESS = FIXTURE_DIR / "ib_tws_u3028269_ready_readiness.synthetic.json"
BUILDER_PATH = ROOT / "scripts" / "build_ib_u3028269_source_package_from_tws_api.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class QuerySourceParityError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QuerySourceParityError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def import_builder():
    spec = importlib.util.spec_from_file_location("p019_ib_source_builder", BUILDER_PATH)
    require(spec is not None and spec.loader is not None, "builder module spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_boundaries(payload: dict[str, Any], label: str) -> None:
    require(payload["raw_secret_values_recorded"] is False, f"{label}: raw secrets recorded")
    require(payload["raw_broker_endpoint_recorded"] is False, f"{label}: raw endpoint recorded")
    require(payload["screenshot_used_for_values"] is False, f"{label}: screenshot used for values")
    require(payload["order_action_sent"] is False, f"{label}: order action sent")


def assert_ready_query_to_source_parity(
    account_summary: dict[str, Any],
    positions: dict[str, Any],
    executions: dict[str, Any],
    open_orders: dict[str, Any],
    package: dict[str, Any],
) -> None:
    require(account_summary["success"] is True, "ready account summary query must succeed")
    require(positions["success"] is True, "ready positions query must succeed")
    require(executions["success"] is True, "ready executions query must succeed")
    require(open_orders["success"] is True, "ready open orders query must succeed")
    require(package["source_health"]["state"] == "ready", "package must be ready")
    require(package["source_inputs"]["account_summary_query"], "package missing account summary ref")
    require(package["source_inputs"]["positions_query"], "package missing positions ref")
    require(package["source_inputs"]["executions_query"], "package missing executions ref")
    require(package["source_inputs"]["open_orders_query"], "package missing open orders ref")
    input_checksums = package["source_input_checksums"]
    require(input_checksums["account_summary_query"] == account_summary["query_checksum"], "account summary checksum mismatch")
    require(input_checksums["positions_query"] == positions["query_checksum"], "positions checksum mismatch")
    require(input_checksums["executions_query"] == executions["query_checksum"], "executions checksum mismatch")
    require(input_checksums["open_orders_query"] == open_orders["query_checksum"], "open orders checksum mismatch")

    query_balances = account_summary["balances"]
    package_balances = package["balances"]
    require(len(package_balances) == len(query_balances), "balance row count mismatch")
    for query_row, package_row in zip(query_balances, package_balances):
        require(package_row["currency"] == query_row["currency"], "balance currency mismatch")
        require(package_row["equity"] == float(query_row["net_liquidation"]), "net liquidation did not map to equity")
        require(package_row["available_cash"] == float(query_row["available_funds"]), "available funds mismatch")
        require(package_row["margin_used"] == float(query_row.get("margin_used") or 0.0), "margin used mismatch")
        require(package_row["unrealized_pnl"] == float(query_row.get("unrealized_pnl") or 0.0), "unrealized pnl mismatch")

    query_positions = positions["positions"]
    package_positions = package["positions"]
    require(len(package_positions) == len(query_positions), "position row count mismatch")
    for query_row, package_row in zip(query_positions, package_positions):
        net_qty = float(query_row.get("net_qty") or 0.0)
        require(package_row["instrument"] == query_row["instrument"], "position instrument mismatch")
        require(package_row["exchange"] == query_row.get("exchange"), "position exchange mismatch")
        require(package_row["direction"] == ("long" if net_qty >= 0 else "short"), "position direction mismatch")
        require(package_row["net_qty"] == net_qty, "position net qty mismatch")
        require(package_row["available_qty"] == net_qty, "position available qty mismatch")
        expected_avg = None if query_row.get("avg_cost") is None else float(query_row["avg_cost"])
        require(package_row["avg_price"] == expected_avg, "position avg price mismatch")
        expected_pnl = None if query_row.get("unrealized_pnl") is None else float(query_row["unrealized_pnl"])
        require(package_row["unrealized_pnl"] == expected_pnl, "position unrealized pnl mismatch")

    require(package["source_health"]["executions_query_success"] is True, "package must record executions success")
    readonly = package["source_health"]["executions_readonly_query"]
    require(readonly["api_call"] == "reqExecutions", "source package readonly api mismatch")
    require(readonly["filter_type"] == "ExecutionFilter", "source package filter type mismatch")
    require(readonly["filter_account_ref"] == "ib-account-ref://U3028269", "source package filter ref mismatch")
    require(readonly["filter_account_raw_value_recorded"] is False, "source package raw account filter recorded")
    require(readonly["query_scope"] == executions["readonly_query"]["query_scope"], "source package readonly scope mismatch")
    require(readonly["complete_history_claimed"] is False, "source package complete history claim drifted")
    require(readonly["order_action_sent"] is False, "source package readonly order action drifted")
    require(package["source_health"]["execution_report_rows"] == len(package["fills"]), "fill row count mismatch")
    require(executions["execution_report_rows"] == len(executions["executions"]), "execution query row count mismatch")
    if executions["execution_report_rows"] == 0:
        require(package["fills"] == [], "empty executions query must not invent fills")
        require(package["source_health"]["execution_report_state"] == "not_available_or_empty", "empty executions state mismatch")
    else:
        require(package["fills"], "non-empty executions must map to FillReport rows")
        require(package["source_health"]["execution_report_state"] == "available", "non-empty executions state mismatch")
        for index, (execution_row, fill_row) in enumerate(zip(executions["executions"], package["fills"]), start=1):
            commission_row = next(
                (
                    item
                    for item in executions.get("commissions", [])
                    if isinstance(item, dict) and item.get("exec_id") == execution_row.get("exec_id")
                ),
                {},
            )
            require(fill_row["nautilus_report_type"] == "FillReport", "execution row did not map to FillReport")
            require(fill_row["trade_id"] == execution_row["exec_id"], "FillReport trade_id mismatch")
            require(fill_row["client_order_id"] == str(execution_row.get("order_ref") or execution_row.get("order_id")), "FillReport client order mismatch")
            require(fill_row["venue_order_id"] == str(execution_row.get("perm_id") or execution_row.get("order_id")), "FillReport venue order mismatch")
            require(fill_row["instrument_id"] == execution_row["instrument_id"], "FillReport instrument id mismatch")
            require(fill_row["side"] == str(execution_row["side"]).upper(), "FillReport side mismatch")
            require(fill_row["last_qty"] == float(execution_row["shares"]), "FillReport last quantity mismatch")
            require(fill_row["last_px"] == float(execution_row["price"]), "FillReport last price mismatch")
            require(fill_row["commission"] == commission_row.get("commission"), "FillReport commission mismatch")
            require(fill_row["commission_currency"] == commission_row.get("currency"), "FillReport commission currency mismatch")
            require(fill_row["source_ref"].endswith(f"#execution-{index}"), "FillReport source ref sequence mismatch")
            require(fill_row["source_checksum"] == executions["query_checksum"], "FillReport source checksum mismatch")

    require(package["source_health"]["open_orders_query_success"] is True, "package must record open orders success")
    open_readonly = package["source_health"]["open_orders_readonly_query"]
    require(open_readonly["api_call"] == "reqAllOpenOrders", "source package open orders api mismatch")
    require(open_readonly["order_action_sent"] is False, "source package open orders order action drifted")
    require(open_readonly["cancel_order_sent"] is False, "source package open orders cancel drifted")
    require(open_readonly["replace_order_sent"] is False, "source package open orders replace drifted")
    require(open_readonly["complete_history_claimed"] is False, "source package open orders complete history claim drifted")
    require(package["source_health"]["open_order_rows"] == len(package["orders"]), "open order row count mismatch")
    require(open_orders["open_order_rows"] == len(open_orders["open_orders"]), "open orders query row count mismatch")
    require(open_orders["open_order_rows"] == len(package["orders"]), "open orders package row count mismatch")
    if open_orders["open_order_rows"] == 0:
        require(package["orders"] == [], "empty open orders query must not invent orders")
        require(package["source_health"]["open_orders_state"] == "empty", "empty open orders state mismatch")
    else:
        require(package["source_health"]["open_orders_state"] == "available", "non-empty open orders state mismatch")
        for index, (query_row, order_row) in enumerate(zip(open_orders["open_orders"], package["orders"]), start=1):
            require(order_row["nautilus_report_type"] == "OrderStatusReport", "open order did not map to OrderStatusReport")
            require(order_row["client_order_id"] == str(query_row.get("order_ref") or query_row.get("order_id")), "open order client id mismatch")
            require(order_row["venue_order_id"] == str(query_row.get("perm_id") or query_row.get("order_id")), "open order venue id mismatch")
            require(order_row["instrument"] == str(query_row.get("symbol") or query_row.get("instrument") or "unknown"), "open order instrument mismatch")
            require(order_row["side"] == str(query_row.get("side") or "UNKNOWN").upper(), "open order side mismatch")
            require(order_row["source_ref"].endswith(f"#open-order-{index}"), "open order source ref sequence mismatch")
            require(order_row["source_checksum"] == open_orders["query_checksum"], "open order source checksum mismatch")


def assert_checksum_drift_rejected(
    account_summary: dict[str, Any],
    positions: dict[str, Any],
    executions: dict[str, Any],
    open_orders: dict[str, Any],
    package: dict[str, Any],
) -> None:
    drifted_package = json.loads(json.dumps(package))
    drifted_package["source_input_checksums"]["executions_query"] = (
        "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    )
    try:
        assert_ready_query_to_source_parity(account_summary, positions, executions, open_orders, drifted_package)
    except QuerySourceParityError as exc:
        require("executions checksum mismatch" in str(exc), "checksum drift rejected for wrong reason")
        return
    raise QuerySourceParityError("checksum drift unexpectedly passed")


def build_synthetic_executions(*, rows: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": "account-console.ib-tws-api-query.v1",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "query_kind": "executions",
        "source_kind": "ib_tws_api",
        "success": True,
        "tws_api_login_confirmed": True,
        "query_started_at": "2026-06-20T00:00:00Z",
        "query_completed_at": "2026-06-20T00:00:00Z",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "screenshot_used_for_values": False,
        "order_action_sent": False,
        "account_ref": "ib-account-ref://U3028269",
        "executions": [],
        "commissions": [],
        "execution_report_rows": 0,
        "empty_state": "not_available_or_no_matching_executions",
        "explicit_non_claims": ["synthetic_mapping_only", "does_not_prove_real_u3028269_fill_truth"],
        "readonly_query": {
            "api_call": "reqExecutions",
            "filter_type": "ExecutionFilter",
            "filter_account_ref": "ib-account-ref://U3028269",
            "filter_account_raw_value_recorded": False,
            "query_scope": "synthetic_current_tws_session_matching_account_filter",
            "request_id": "exec-readonly-synthetic",
            "order_action_sent": False,
            "complete_history_claimed": False,
        },
        "query_checksum": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    }
    if rows:
        payload["executions"] = [
            {
                "exec_id": "SYNTH-EXEC-0001",
                "order_id": 7001,
                "perm_id": 8800001,
                "order_ref": "synthetic-readonly-map-0001",
                "instrument_id": "MSFT.NASDAQ",
                "symbol": "MSFT",
                "exchange": "NASDAQ",
                "side": "BOT",
                "shares": 3.0,
                "price": 415.25,
                "time": "2026-06-20T00:00:01Z",
            }
        ]
        payload["commissions"] = [
            {
                "exec_id": "SYNTH-EXEC-0001",
                "commission": 1.23,
                "currency": "USD",
                "realized_pnl": 0.0,
            }
        ]
        payload["execution_report_rows"] = 1
        payload["empty_state"] = None
        payload["query_checksum"] = "sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    return payload


def build_synthetic_open_orders(*, rows: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": "account-console.ib-tws-api-query.v1",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "query_kind": "open_orders",
        "source_kind": "ib_tws_api",
        "success": True,
        "tws_api_login_confirmed": True,
        "query_started_at": "2026-06-20T00:00:00Z",
        "query_completed_at": "2026-06-20T00:00:00Z",
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "screenshot_used_for_values": False,
        "order_action_sent": False,
        "cancel_order_sent": False,
        "replace_order_sent": False,
        "account_ref": "ib-account-ref://U3028269",
        "open_orders": [],
        "open_order_rows": 0,
        "empty_state": "no_open_orders_returned",
        "explicit_non_claims": ["synthetic_mapping_only", "does_not_authorize_order_action"],
        "readonly_query": {
            "api_call": "reqAllOpenOrders",
            "callback_rows": ["openOrder", "orderStatus", "openOrderEnd"],
            "query_scope": "synthetic_current_tws_session_open_orders_visible_to_api_client",
            "order_action_sent": False,
            "cancel_order_sent": False,
            "replace_order_sent": False,
            "complete_history_claimed": False,
        },
        "query_checksum": "sha256:abababababababababababababababababababababababababababababababab",
    }
    if rows:
        payload["open_orders"] = [
            {
                "order_id": "7101",
                "perm_id": "990001",
                "client_id": "0",
                "account_ref": "ib-account-ref://U3028269",
                "instrument": "MSFT",
                "symbol": "MSFT",
                "exchange": "SMART",
                "destination": "NASDAQ",
                "side": "BUY",
                "order_type": "LMT",
                "limit_price": 411.5,
                "quantity": 3.0,
                "filled_quantity": 1.0,
                "remaining_quantity": 2.0,
                "time_in_force": "GTC",
                "status": "Submitted",
                "sequence": 1,
            }
        ]
        payload["open_order_rows"] = 1
        payload["empty_state"] = None
        payload["query_checksum"] = "sha256:bcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbc"
    return payload


def main() -> None:
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    executions = load(EXECUTIONS)
    open_orders = load(OPEN_ORDERS)
    source_package = load(SOURCE_PACKAGE)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(account_summary["schema"] == "account-console.ib-tws-api-query.v1", "account summary schema mismatch")
    require(positions["schema"] == "account-console.ib-tws-api-query.v1", "positions schema mismatch")
    require(executions["schema"] == "account-console.ib-tws-api-query.v1", "executions schema mismatch")
    require(source_package["schema_version"] == "account_source_artifact.v1", "source package schema mismatch")
    assert_boundaries(account_summary, "account_summary")
    assert_boundaries(positions, "positions")
    assert_boundaries(executions, "executions")
    assert_boundaries(open_orders, "open_orders")
    require(source_package["boundaries"]["raw_secret_values_recorded"] is False, "source package recorded secrets")
    require(
        source_package["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "source package used screenshot values",
    )
    require(source_package["boundaries"]["order_action_sent"] is False, "source package sent order action")

    if source_package["source_health"]["state"] == "blocked":
        require(account_summary["success"] is False, "blocked package cannot pair with successful account summary")
        require(positions["success"] is False, "blocked package cannot pair with successful positions")
        require(executions["success"] is False, "blocked package cannot pair with successful executions")
        require(open_orders["success"] is False, "blocked package cannot pair with successful open orders")
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "account summary blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "positions blocker mismatch")
        require(executions["blocker_id"] == "tws_api_readiness_missing", "executions blocker mismatch")
        require(open_orders["blocker_id"] == "tws_api_readiness_missing", "open orders blocker mismatch")
        require(source_package["source_health"]["blocker_id"] == "tws_api_readiness_missing", "source blocker mismatch")
        require(source_package["balances"] == [], "blocked package must not invent balances")
        require(source_package["positions"] == [], "blocked package must not invent positions")
        current_status = "blocked"
    else:
        assert_ready_query_to_source_parity(account_summary, positions, executions, open_orders, source_package)
        current_status = "ready"

    builder = import_builder()
    synthetic_account_summary = load(SYNTHETIC_ACCOUNT_SUMMARY)
    synthetic_positions = load(SYNTHETIC_POSITIONS)
    with tempfile.TemporaryDirectory(prefix="p019-query-source-parity-") as tmp:
        tmp_path = Path(tmp)
        output = tmp_path / "source-package.json"
        synthetic_executions_path = tmp_path / "executions-empty.json"
        synthetic_executions = build_synthetic_executions(rows=False)
        synthetic_open_orders_path = tmp_path / "open-orders-empty.json"
        synthetic_open_orders = build_synthetic_open_orders(rows=False)
        synthetic_open_orders_path.write_text(json.dumps(synthetic_open_orders, ensure_ascii=False, indent=2), encoding="utf-8")
        synthetic_executions_path.write_text(json.dumps(synthetic_executions, ensure_ascii=False, indent=2), encoding="utf-8")
        synthetic_package = builder.build_source_package(
            account_summary_path=SYNTHETIC_ACCOUNT_SUMMARY,
            positions_path=SYNTHETIC_POSITIONS,
            executions_query_path=synthetic_executions_path,
            open_orders_query_path=synthetic_open_orders_path,
            readiness_probe_path=SYNTHETIC_READINESS,
            output_path=output,
            allow_blocked=False,
        )
        synthetic_filled_executions_path = tmp_path / "executions-filled.json"
        synthetic_filled_executions = build_synthetic_executions(rows=True)
        synthetic_filled_open_orders_path = tmp_path / "open-orders-filled.json"
        synthetic_filled_open_orders = build_synthetic_open_orders(rows=True)
        synthetic_filled_open_orders_path.write_text(
            json.dumps(synthetic_filled_open_orders, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        synthetic_filled_executions_path.write_text(
            json.dumps(synthetic_filled_executions, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        synthetic_filled_package = builder.build_source_package(
            account_summary_path=SYNTHETIC_ACCOUNT_SUMMARY,
            positions_path=SYNTHETIC_POSITIONS,
            executions_query_path=synthetic_filled_executions_path,
            open_orders_query_path=synthetic_filled_open_orders_path,
            readiness_probe_path=SYNTHETIC_READINESS,
            output_path=output,
            allow_blocked=False,
        )
    assert_ready_query_to_source_parity(
        synthetic_account_summary,
        synthetic_positions,
        synthetic_executions,
        synthetic_open_orders,
        synthetic_package,
    )
    assert_ready_query_to_source_parity(
        synthetic_account_summary,
        synthetic_positions,
        synthetic_filled_executions,
        synthetic_filled_open_orders,
        synthetic_filled_package,
    )
    assert_checksum_drift_rejected(
        synthetic_account_summary,
        synthetic_positions,
        synthetic_executions,
        synthetic_open_orders,
        synthetic_package,
    )

    for term in [
        "validate_p019_ib_u3028269_query_source_parity.py",
        "P019_IB_U3028269_QUERY_SOURCE_PARITY_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print(
        "P019_IB_U3028269_QUERY_SOURCE_PARITY_OK: "
        f"current={current_status} synthetic_ready=pass synthetic_fills=1 synthetic_open_orders=1 checksum_drift=rejected"
    )


if __name__ == "__main__":
    main()
