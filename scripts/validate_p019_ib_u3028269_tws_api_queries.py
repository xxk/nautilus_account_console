from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUERY_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
ACCOUNT_SUMMARY = QUERY_DIR / "account_summary.json"
POSITIONS = QUERY_DIR / "positions.json"
EXECUTIONS = QUERY_DIR / "executions.json"
OPEN_ORDERS = QUERY_DIR / "open_orders.json"
COLLECTOR = ROOT / "scripts" / "collect_ib_u3028269_tws_api_snapshot.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class TwsApiQueryError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TwsApiQueryError(message)


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


def validate_common(payload: dict[str, Any], kind: str) -> None:
    require(payload["schema"] == "account-console.ib-tws-api-query.v1", f"{kind}: schema drifted")
    require(payload["account_id"] == "acct.ib.live.u3028269", f"{kind}: account mismatch")
    require(payload["display_alias"] == "U3028269", f"{kind}: alias mismatch")
    require(payload["query_kind"] == kind, f"{kind}: query kind mismatch")
    require(payload["source_kind"] == "ib_tws_api", f"{kind}: source kind mismatch")
    require(payload["raw_secret_values_recorded"] is False, f"{kind}: raw secrets recorded")
    require(payload["raw_broker_endpoint_recorded"] is False, f"{kind}: raw endpoint recorded")
    require(payload["screenshot_used_for_values"] is False, f"{kind}: screenshot used for values")
    require(payload["order_action_sent"] is False, f"{kind}: order action sent")
    require(str(payload["query_checksum"]).startswith("sha256:"), f"{kind}: checksum missing")


def validate_executions_readonly_metadata(executions: dict[str, Any]) -> None:
    metadata = executions["readonly_query"]
    require(metadata["api_call"] == "reqExecutions", "executions readonly api mismatch")
    require(metadata["filter_type"] == "ExecutionFilter", "executions filter type mismatch")
    require(metadata["filter_account_ref"] == "ib-account-ref://U3028269", "executions account ref mismatch")
    require(metadata["filter_account_raw_value_recorded"] is False, "executions raw account filter recorded")
    require(metadata["query_scope"] == "current_tws_session_matching_account_filter", "executions query scope mismatch")
    require(metadata["request_id"] == "exec-readonly-9002", "executions request id mismatch")
    require(metadata["order_action_sent"] is False, "executions metadata claims order action")
    require(metadata["complete_history_claimed"] is False, "executions must not claim complete history")


def validate_open_orders_readonly_metadata(open_orders: dict[str, Any]) -> None:
    metadata = open_orders["readonly_query"]
    require(metadata["api_call"] == "reqAllOpenOrders", "open orders readonly api mismatch")
    require("reqAutoOpenOrders" in metadata["api_calls"], "open orders must bind TWS manual orders")
    require("reqOpenOrders" in metadata["api_calls"], "open orders must request bound/manual orders")
    require("reqAllOpenOrders" in metadata["api_calls"], "open orders must request all visible API orders")
    require("openOrder" in metadata["callback_rows"], "open orders callback rows missing openOrder")
    require("orderStatus" in metadata["callback_rows"], "open orders callback rows missing orderStatus")
    require("openOrderEnd" in metadata["callback_rows"], "open orders callback rows missing openOrderEnd")
    require(metadata["query_scope"] == "current_tws_session_open_orders_visible_to_api_client", "open orders query scope mismatch")
    require(metadata["order_action_sent"] is False, "open orders metadata claims order action")
    require(metadata["cancel_order_sent"] is False, "open orders metadata claims cancel")
    require(metadata["replace_order_sent"] is False, "open orders metadata claims replace")
    require(metadata["complete_history_claimed"] is False, "open orders must not claim complete history")


def main() -> None:
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    executions = load(EXECUTIONS)
    open_orders = load(OPEN_ORDERS)
    collector = read(COLLECTOR)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    validate_common(account_summary, "account_summary")
    validate_common(positions, "positions")
    validate_common(executions, "executions")
    validate_common(open_orders, "open_orders")
    validate_executions_readonly_metadata(executions)
    validate_open_orders_readonly_metadata(open_orders)

    if account_summary["success"] is False or positions["success"] is False or executions["success"] is False or open_orders["success"] is False:
        require(
            account_summary["success"] is False
            and positions["success"] is False
            and executions["success"] is False
            and open_orders["success"] is False,
            "blocked query set must all be blocked",
        )
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "account summary blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "positions blocker mismatch")
        require(executions["blocker_id"] == "tws_api_readiness_missing", "executions blocker mismatch")
        require(open_orders["blocker_id"] == "tws_api_readiness_missing", "open orders blocker mismatch")
        require(account_summary["tws_api_login_confirmed"] is False, "blocked account query must not claim login")
        require(positions["tws_api_login_confirmed"] is False, "blocked positions query must not claim login")
        require(executions["tws_api_login_confirmed"] is False, "blocked executions query must not claim login")
        require(open_orders["tws_api_login_confirmed"] is False, "blocked open orders query must not claim login")
        require(account_summary["balances"] == [], "blocked account query must not invent balances")
        require(positions["positions"] == [], "blocked positions query must not invent positions")
        require(executions["executions"] == [], "blocked executions query must not invent executions")
        require(executions["execution_report_rows"] == 0, "blocked executions query must not claim report rows")
        require(open_orders["open_orders"] == [], "blocked open orders query must not invent orders")
        require(open_orders["open_order_rows"] == 0, "blocked open orders query must not claim rows")
    else:
        require(
            account_summary["success"] is True
            and positions["success"] is True
            and executions["success"] is True
            and open_orders["success"] is True,
            "ready query set must all pass",
        )
        require(account_summary["tws_api_login_confirmed"] is True, "account query must confirm TWS API login")
        require(positions["tws_api_login_confirmed"] is True, "positions query must confirm TWS API login")
        require(executions["tws_api_login_confirmed"] is True, "executions query must confirm TWS API login")
        require(open_orders["tws_api_login_confirmed"] is True, "open orders query must confirm TWS API login")
        require(isinstance(account_summary["balances"], list), "ready account query balances must be list")
        require(isinstance(positions["positions"], list), "ready positions query positions must be list")
        require(isinstance(executions["executions"], list), "ready executions query executions must be list")
        require(isinstance(executions["commissions"], list), "ready executions query commissions must be list")
        require(isinstance(open_orders["open_orders"], list), "ready open orders must be list")
        require(executions["execution_report_rows"] == len(executions["executions"]), "execution row count mismatch")
        require(open_orders["open_order_rows"] == len(open_orders["open_orders"]), "open order row count mismatch")
        if executions["execution_report_rows"] == 0:
            require(
                executions["empty_state"] == "not_available_or_no_matching_executions",
                "empty executions query must carry typed empty state",
            )
            require(
                "does_not_prove_complete_order_history" in executions["explicit_non_claims"],
                "empty executions must not claim complete order history",
            )

    forbidden_fragments = ["password=", "passwd=", "auth_code=", "api_key=", "secret=", "127.0.0.1:"]
    for label, payload in [
        ("account_summary", account_summary),
        ("positions", positions),
        ("executions", executions),
        ("open_orders", open_orders),
    ]:
        for value in walk_values(payload):
            if isinstance(value, str):
                lowered = value.lower()
                hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
                require(not hits, f"{label}: forbidden fragment {hits} in {value!r}")

    for term in [
        "reqAccountSummary",
        "reqPositions",
        "reqExecutions",
        "reqAutoOpenOrders",
        "reqOpenOrders",
        "reqAllOpenOrders",
        "ExecutionFilter",
        "_readonly_executions_metadata",
        "_readonly_open_orders_metadata",
        "openOrder",
        "orderStatus",
        "openOrderEnd",
        "cancelAccountSummary",
        "cancelPositions",
        "order_action_sent",
        "raw_broker_endpoint_recorded",
    ]:
        require(term in collector, f"collector missing guard/readonly term {term}")
    for forbidden in ["placeOrder", "cancelOrder", "reqGlobalCancel"]:
        require(forbidden not in collector, f"collector must not contain order/action API {forbidden}")

    for term in [
        "collect_ib_u3028269_tws_api_snapshot.py",
        "validate_p019_ib_u3028269_tws_api_queries.py",
        "P019_IB_U3028269_TWS_API_QUERIES_OK",
    ]:
        require(term in acceptance, f"acceptance missing query term {term}")
        require(term in phase_plan, f"phase plan missing query term {term}")

    status = "ready" if account_summary["success"] and positions["success"] and executions["success"] and open_orders["success"] else "blocked"
    print(
        "P019_IB_U3028269_TWS_API_QUERIES_OK: "
        f"status={status} executions={executions.get('execution_report_rows', 0)} "
        f"open_orders={open_orders.get('open_order_rows', 0)} "
        "order_action_sent=false screenshot_values=false"
    )


if __name__ == "__main__":
    main()
