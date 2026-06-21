from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
ACCOUNT_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "account_summary.json"
POSITIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "positions.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
OPEN_ORDERS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "open_orders.json"
BUILDER = ROOT / "scripts" / "build_ib_u3028269_source_package_from_tws_api.py"
COLLECTOR = ROOT / "scripts" / "collect_ib_u3028269_tws_api_snapshot.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class IbSourcePackageError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IbSourcePackageError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk_values(item))
    return values


def validate_readonly_query_health(health: dict[str, Any], executions: dict[str, Any]) -> None:
    readonly = health["executions_readonly_query"]
    source_readonly = executions["readonly_query"]
    require(readonly["api_call"] == "reqExecutions", "source package readonly api mismatch")
    require(readonly["filter_type"] == "ExecutionFilter", "source package filter type mismatch")
    require(readonly["filter_account_ref"] == "ib-account-ref://U3028269", "source package filter ref mismatch")
    require(readonly["filter_account_raw_value_recorded"] is False, "source package raw account filter recorded")
    require(readonly["query_scope"] == source_readonly["query_scope"], "source package query scope mismatch")
    require(readonly["complete_history_claimed"] is False, "source package must not claim complete execution history")
    require(readonly["order_action_sent"] is False, "source package readonly metadata sent order action")


def validate_open_orders_query_health(health: dict[str, Any], open_orders: dict[str, Any]) -> None:
    readonly = health["open_orders_readonly_query"]
    source_readonly = open_orders["readonly_query"]
    require(readonly["api_call"] == "reqAllOpenOrders", "source package open orders api mismatch")
    require("openOrder" in readonly["callback_rows"], "source package open orders callback mismatch")
    require(readonly["query_scope"] == source_readonly["query_scope"], "source package open orders scope mismatch")
    require(readonly["complete_history_claimed"] is False, "source package must not claim complete open-order history")
    require(readonly["order_action_sent"] is False, "source package open orders sent order action")
    require(readonly["cancel_order_sent"] is False, "source package open orders sent cancel")
    require(readonly["replace_order_sent"] is False, "source package open orders sent replace")


def main() -> None:
    payload = load(SOURCE_PACKAGE)
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    executions = load(EXECUTIONS)
    open_orders = load(OPEN_ORDERS)
    builder = read(BUILDER)
    collector = read(COLLECTOR)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema_version"] == "account_source_artifact.v1", "schema drifted")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "display alias mismatch")
    require(payload["source_owner"] == "account-console-broker-observation-session", "source owner mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(payload["source_health"]["api_transport"] == "ib_tws_api", "API transport mismatch")
    require(payload["source_ref"] == "output/account_capability/ib-live-u3028269/source-package.json", "source ref mismatch")
    require(str(payload["source_checksum"]).startswith("sha256:"), "source checksum missing")
    input_checksums = payload["source_input_checksums"]

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(boundaries["tws_api_account_query_required"] is True, "TWS API account query must be required")
    require(boundaries["order_action_sent"] is False, "order action must not be sent")

    health = payload["source_health"]
    if health["state"] == "blocked":
        require(health["blocker_id"] == "tws_api_readiness_missing", "blocked package must carry readiness blocker")
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "blocked account query blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "blocked positions query blocker mismatch")
        require(account_summary["success"] is False and positions["success"] is False, "blocked source package must align with blocked query artifacts")
        require(payload["balances"] == [], "blocked package must not invent balances")
        require(payload["positions"] == [], "blocked package must not invent positions")
        require(payload["orders"] == [] and payload["fills"] == [], "blocked package must not invent reports")
        require(payload["source_inputs"]["account_summary_query"] is None, "blocked package must not claim account query input")
        require(payload["source_inputs"]["positions_query"] is None, "blocked package must not claim positions input")
        require(payload["source_inputs"]["executions_query"] is None, "blocked package must not claim executions input")
        require(payload["source_inputs"]["open_orders_query"] is None, "blocked package must not claim open orders input")
    else:
        require(health["state"] == "ready", "source health must be ready or blocked")
        require(payload["source_mode"] == "live_observation", "ready package must be live_observation")
        require(payload["source_inputs"]["account_summary_query"], "ready package missing account summary query ref")
        require(payload["source_inputs"]["positions_query"], "ready package missing positions query ref")
        require(payload["source_inputs"]["executions_query"], "ready package missing executions query ref")
        require(payload["source_inputs"]["open_orders_query"], "ready package missing open orders query ref")
        require(input_checksums["account_summary_query"] == account_summary["query_checksum"], "account summary checksum mismatch")
        require(input_checksums["positions_query"] == positions["query_checksum"], "positions checksum mismatch")
        require(input_checksums["executions_query"] == executions["query_checksum"], "executions checksum mismatch")
        require(input_checksums["open_orders_query"] == open_orders["query_checksum"], "open orders checksum mismatch")
        require(payload["balances"], "ready package must contain TWS API balances")
        currencies = {str(row.get("currency")) for row in payload["balances"]}
        require("USD" in currencies, "ready package must include USD balance row")
        require(any(currency != "USD" for currency in currencies), "ready package must include at least one non-USD balance row")
        require(len(currencies) == len(payload["balances"]), "balance currencies must be unique")
        source_currencies = {str(row.get("currency")) for row in account_summary["balances"]}
        require(currencies == source_currencies, "source package balance currencies must match account summary query")
        for row in payload["balances"]:
            require(isinstance(row.get("currency"), str) and row["currency"], "balance row currency missing")
            require(isinstance(row.get("equity"), (int, float)), "balance row equity missing")
            require(isinstance(row.get("available_cash"), (int, float)), "balance row available cash missing")
            require("cash" in row, "balance row must preserve cash field")
            require("total_cash" in row, "balance row must preserve total cash field")
            require("exchange_rate" in row, "balance row must preserve exchange rate field")
        require(health["executions_query_success"] is True, "ready package must record executions query success")
        validate_readonly_query_health(health, executions)
        require(health["open_orders_query_success"] is True, "ready package must record open orders query success")
        validate_open_orders_query_health(health, open_orders)
        require(health["open_order_rows"] == len(payload["orders"]), "open order row count mismatch")
        require(open_orders["open_order_rows"] == len(open_orders["open_orders"]), "open orders query row count mismatch")
        require(health["open_order_rows"] == open_orders["open_order_rows"], "open orders source/package count mismatch")
        if open_orders["open_order_rows"] == 0:
            require(payload["orders"] == [], "empty open orders query must not invent orders")
            require(health["open_orders_state"] == "empty", "empty open orders state mismatch")
        else:
            require(payload["orders"], "open orders query rows must map to orders")
            require(health["open_orders_state"] == "available", "non-empty open orders state mismatch")
            for order in payload["orders"]:
                require(order["nautilus_report_type"] == "OrderStatusReport", "open order must map to OrderStatusReport")
                require(order["client_order_id"], "open order missing client id")
                require(order["source_ref"].startswith("output/account_capability/ib-live-u3028269/tws-api/open_orders.json#"), "open order source ref mismatch")
                require(str(order["source_checksum"]).startswith("sha256:"), "open order source checksum missing")
        require(health["execution_report_rows"] == len(payload["fills"]), "execution report row count mismatch")
        if executions["execution_report_rows"] == 0:
            require(payload["fills"] == [], "empty executions query must not invent fills")
            require(health["execution_report_state"] == "not_available_or_empty", "empty executions state mismatch")
        else:
            require(payload["fills"], "execution rows must map to fills")
            for fill in payload["fills"]:
                require(fill["nautilus_report_type"] == "FillReport", "fills must use FillReport")
                require(fill["trade_id"], "fill missing trade id")
                require(fill["source_ref"].startswith("output/account_capability/ib-live-u3028269/tws-api/executions.json#"), "fill source ref mismatch")
                require(str(fill["source_checksum"]).startswith("sha256:"), "fill source checksum missing")

    forbidden_fragments = ["password=", "passwd=", "auth_code=", "api_key=", "secret=", "127.0.0.1:"]
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
            require(not hits, f"source package recorded forbidden fragment {hits} in {value!r}")

    for term in [
        "account-console.ib-tws-api-query.v1",
        "screenshot_used_for_values",
        "order_action_sent",
        "executions_readonly_query",
        "open_orders_readonly_query",
        "tws_api_readiness_missing",
    ]:
        require(term in builder, f"builder missing guard term {term}")
    for term in ["$LEDGER", "reqAccountUpdates", "updateAccountValue", "accountDownloadEnd", "reqAllOpenOrders"]:
        require(term in collector, f"collector missing multi-currency term {term}")
    for term in [
        "build_ib_u3028269_source_package_from_tws_api.py",
        "validate_p019_ib_u3028269_source_package.py",
        "P019_IB_U3028269_SOURCE_PACKAGE_OK",
    ]:
        require(term in acceptance, f"acceptance missing source-package term {term}")
        require(term in phase_plan, f"phase plan missing source-package term {term}")

    status = health["state"]
    print(f"P019_IB_U3028269_SOURCE_PACKAGE_OK: status={status} api_transport=ib_tws_api screenshot_values=false")


if __name__ == "__main__":
    main()
