from __future__ import annotations

import argparse
import importlib.util
import json
import queue
import socket
import sys
import threading
import time
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCOUNT_ID = "acct.ib.live.u3028269"
DISPLAY_ALIAS = "U3028269"
DEFAULT_OUTPUT_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
READINESS_PROBE = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"
DEFAULT_IBAPI_RUNTIME = ROOT / "output" / "runtime" / "python"
PORT_REFS = {
    "tws_live_default": 7496,
    "tws_paper_default": 7497,
    "gateway_live_default": 4001,
    "gateway_paper_default": 4002,
}


class CollectError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_checksum(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(encoded).hexdigest()


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _add_runtime_path(path: Path) -> str | None:
    if path.exists():
        sys.path.insert(0, str(path))
        return _source_ref(path)
    return None


def _tcp_open(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _load_readiness(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _select_port(readiness: dict[str, Any], explicit_port_ref: str | None) -> tuple[str | None, int | None]:
    if explicit_port_ref:
        return explicit_port_ref, PORT_REFS[explicit_port_ref]
    for port_ref, result in readiness.get("candidate_port_refs", {}).items():
        if result.get("open") is True and port_ref in PORT_REFS:
            return port_ref, PORT_REFS[port_ref]
    return None, None


def _base_query(kind: str, *, success: bool, started_at: str, completed_at: str) -> dict[str, Any]:
    return {
        "schema": "account-console.ib-tws-api-query.v1",
        "account_id": ACCOUNT_ID,
        "display_alias": DISPLAY_ALIAS,
        "query_kind": kind,
        "source_kind": "ib_tws_api",
        "success": success,
        "tws_api_login_confirmed": success,
        "query_started_at": started_at,
        "query_completed_at": completed_at,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "screenshot_used_for_values": False,
        "order_action_sent": False,
        "account_ref": "ib-account-ref://U3028269",
    }


def _blocked_query(kind: str, reason: str, readiness_ref: str) -> dict[str, Any]:
    observed = _now()
    payload = _base_query(kind, success=False, started_at=observed, completed_at=observed)
    payload.update(
        {
            "blocker_id": "tws_api_readiness_missing",
            "blocker_reason": reason,
            "readiness_probe_ref": readiness_ref,
            "balances": [] if kind == "account_summary" else None,
            "positions": [] if kind == "positions" else None,
            "executions": [] if kind == "executions" else None,
            "commissions": [] if kind == "executions" else None,
            "execution_report_rows": 0 if kind == "executions" else None,
            "readonly_query": _readonly_executions_metadata()
            if kind == "executions"
            else _readonly_open_orders_metadata()
            if kind == "open_orders"
            else None,
            "open_orders": [] if kind == "open_orders" else None,
            "open_order_rows": 0 if kind == "open_orders" else None,
            "explicit_non_claims": [
                "does_not_prove_account_truth",
                "does_not_prove_funds_truth",
                "does_not_prove_positions_truth",
                "does_not_authorize_order_action",
            ],
        }
    )
    for field, expected_kind in [
        ("balances", "account_summary"),
        ("positions", "positions"),
        ("executions", "executions"),
        ("commissions", "executions"),
        ("execution_report_rows", "executions"),
        ("readonly_query", kind if kind in {"executions", "open_orders"} else "executions"),
        ("open_orders", "open_orders"),
        ("open_order_rows", "open_orders"),
    ]:
        if kind != expected_kind:
            payload.pop(field)
    payload["query_checksum"] = _source_checksum({**payload, "query_checksum": "sha256:pending"})
    return payload


def _readonly_executions_metadata() -> dict[str, Any]:
    return {
        "api_call": "reqExecutions",
        "filter_type": "ExecutionFilter",
        "filter_account_ref": "ib-account-ref://U3028269",
        "filter_account_raw_value_recorded": False,
        "query_scope": "current_tws_session_matching_account_filter",
        "request_id": "exec-readonly-9002",
        "order_action_sent": False,
        "complete_history_claimed": False,
    }


def _readonly_open_orders_metadata() -> dict[str, Any]:
    return {
        "api_call": "reqAllOpenOrders",
        "api_calls": ["reqAutoOpenOrders", "reqOpenOrders", "reqAllOpenOrders"],
        "callback_rows": ["openOrder", "orderStatus", "openOrderEnd"],
        "query_scope": "current_tws_session_open_orders_visible_to_api_client",
        "client_id_policy": "client_id_0_binds_tws_manual_orders_when_available",
        "order_action_sent": False,
        "cancel_order_sent": False,
        "replace_order_sent": False,
        "complete_history_claimed": False,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_blocked(output_dir: Path, reason: str, readiness_probe: Path) -> None:
    readiness_ref = _source_ref(readiness_probe)
    _write_json(output_dir / "account_summary.json", _blocked_query("account_summary", reason, readiness_ref))
    _write_json(output_dir / "positions.json", _blocked_query("positions", reason, readiness_ref))
    _write_json(output_dir / "executions.json", _blocked_query("executions", reason, readiness_ref))
    _write_json(output_dir / "open_orders.json", _blocked_query("open_orders", reason, readiness_ref))


def _as_optional_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if abs(number) > 1e100:
        return None
    return number


def _open_order_key(*, order_id: Any, perm_id: Any, instrument: Any, side: Any, quantity: Any, limit_price: Any) -> str:
    perm = str(perm_id or "")
    if perm and perm != "0":
        return f"perm:{perm}"
    return "|".join(
        [
            f"order:{order_id}",
            f"instrument:{instrument}",
            f"side:{side}",
            f"qty:{quantity}",
            f"limit:{limit_price}",
        ]
    )


def _collect_with_ibapi(
    *, host: str, port: int, client_id: int, timeout: float
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    from ibapi.client import EClient
    from ibapi.contract import Contract
    from ibapi.execution import ExecutionFilter
    from ibapi.wrapper import EWrapper

    class ReadOnlyApp(EWrapper, EClient):
        def __init__(self) -> None:
            EClient.__init__(self, self)
            self.events: queue.Queue[str] = queue.Queue()
            self.summary: dict[tuple[str, str], str] = {}
            self.account_values: dict[tuple[str, str], str] = {}
            self.positions: list[dict[str, Any]] = []
            self.executions: list[dict[str, Any]] = []
            self.commissions: list[dict[str, Any]] = []
            self.open_orders: dict[str, dict[str, Any]] = {}
            self.order_statuses_by_key: dict[str, dict[str, Any]] = {}
            self.order_statuses_by_order_id: dict[str, dict[str, Any]] = {}
            self.errors: list[dict[str, Any]] = []
            self.managed_accounts: list[str] = []

        def managedAccounts(self, accountsList: str) -> None:  # noqa: N802 - IB API callback name
            self.managed_accounts = [item for item in accountsList.split(",") if item]
            self.events.put("managedAccounts")

        def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str) -> None:  # noqa: N802
            if account == DISPLAY_ALIAS or account.endswith(DISPLAY_ALIAS):
                self.summary[(tag, currency or "BASE")] = value

        def accountSummaryEnd(self, reqId: int) -> None:  # noqa: N802
            self.events.put("accountSummaryEnd")

        def updateAccountValue(self, key: str, val: str, currency: str, accountName: str) -> None:  # noqa: N802
            if accountName == DISPLAY_ALIAS or accountName.endswith(DISPLAY_ALIAS):
                self.account_values[(key, currency or "BASE")] = val

        def accountDownloadEnd(self, accountName: str) -> None:  # noqa: N802
            if accountName == DISPLAY_ALIAS or accountName.endswith(DISPLAY_ALIAS):
                self.events.put("accountDownloadEnd")

        def position(self, account: str, contract: Contract, position: float, avgCost: float) -> None:  # noqa: N802
            if account == DISPLAY_ALIAS or account.endswith(DISPLAY_ALIAS):
                self.positions.append(
                    {
                        "instrument": getattr(contract, "symbol", "") or getattr(contract, "localSymbol", ""),
                        "exchange": getattr(contract, "exchange", None),
                        "net_qty": float(position),
                        "avg_cost": float(avgCost),
                        "unrealized_pnl": None,
                    }
                )

        def positionEnd(self) -> None:  # noqa: N802
            self.events.put("positionEnd")

        def execDetails(self, reqId: int, contract: Contract, execution: Any) -> None:  # noqa: N802
            account = str(getattr(execution, "acctNumber", "") or "")
            if account and account != DISPLAY_ALIAS and not account.endswith(DISPLAY_ALIAS):
                return
            self.executions.append(
                {
                    "exec_id": str(getattr(execution, "execId", "") or ""),
                    "order_id": str(getattr(execution, "orderId", "") or ""),
                    "perm_id": str(getattr(execution, "permId", "") or ""),
                    "client_id": str(getattr(execution, "clientId", "") or ""),
                    "account_ref": "ib-account-ref://U3028269",
                    "symbol": str(getattr(contract, "symbol", "") or getattr(contract, "localSymbol", "") or ""),
                    "instrument_id": str(getattr(contract, "localSymbol", "") or getattr(contract, "symbol", "") or ""),
                    "exchange": str(getattr(execution, "exchange", "") or getattr(contract, "exchange", "") or ""),
                    "side": str(getattr(execution, "side", "") or ""),
                    "shares": float(getattr(execution, "shares", 0.0) or 0.0),
                    "price": float(getattr(execution, "price", 0.0) or 0.0),
                    "time": str(getattr(execution, "time", "") or ""),
                    "order_ref": str(getattr(execution, "orderRef", "") or ""),
                    "liquidation": int(getattr(execution, "liquidation", 0) or 0),
                }
            )

        def execDetailsEnd(self, reqId: int) -> None:  # noqa: N802
            self.events.put("execDetailsEnd")

        def commissionReport(self, commissionReport: Any) -> None:  # noqa: N802
            self.commissions.append(
                {
                    "exec_id": str(getattr(commissionReport, "execId", "") or ""),
                    "commission": None
                    if getattr(commissionReport, "commission", None) is None
                    else float(getattr(commissionReport, "commission")),
                    "currency": str(getattr(commissionReport, "currency", "") or ""),
                    "realized_pnl": None
                    if getattr(commissionReport, "realizedPNL", None) is None
                    else float(getattr(commissionReport, "realizedPNL")),
                    "yield_value": None
                    if getattr(commissionReport, "yield_", None) is None
                    else float(getattr(commissionReport, "yield_")),
                }
            )

        def openOrder(self, orderId: int, contract: Contract, order: Any, orderState: Any) -> None:  # noqa: N802
            account = str(getattr(order, "account", "") or "")
            if account and account != DISPLAY_ALIAS and not account.endswith(DISPLAY_ALIAS):
                return
            perm_id = str(getattr(order, "permId", "") or "")
            instrument = str(getattr(contract, "localSymbol", "") or getattr(contract, "symbol", "") or "")
            side = str(getattr(order, "action", "") or "")
            quantity = _as_optional_float(getattr(order, "totalQuantity", None))
            limit_price = _as_optional_float(getattr(order, "lmtPrice", None))
            row_key = _open_order_key(
                order_id=orderId,
                perm_id=perm_id,
                instrument=instrument,
                side=side,
                quantity=quantity,
                limit_price=limit_price,
            )
            self.open_orders[row_key] = {
                "order_id": str(orderId),
                "perm_id": perm_id,
                "client_id": str(getattr(order, "clientId", "") or ""),
                "account_ref": "ib-account-ref://U3028269",
                "instrument": instrument,
                "symbol": str(getattr(contract, "symbol", "") or getattr(contract, "localSymbol", "") or ""),
                "exchange": str(getattr(contract, "exchange", "") or ""),
                "destination": str(getattr(order, "orderRef", "") or getattr(contract, "exchange", "") or ""),
                "side": side,
                "order_type": str(getattr(order, "orderType", "") or ""),
                "limit_price": limit_price,
                "aux_price": _as_optional_float(getattr(order, "auxPrice", None)),
                "quantity": quantity,
                "time_in_force": str(getattr(order, "tif", "") or ""),
                "status": str(getattr(orderState, "status", "") or ""),
            }

        def orderStatus(  # noqa: N802
            self,
            orderId: int,
            status: str,
            filled: float,
            remaining: float,
            avgFillPrice: float,
            permId: int,
            parentId: int,
            lastFillPrice: float,
            clientId: int,
            whyHeld: str,
            mktCapPrice: float,
        ) -> None:
            perm_id = str(permId or "")
            status_row = {
                "status": str(status or ""),
                "filled_quantity": _as_optional_float(filled),
                "remaining_quantity": _as_optional_float(remaining),
                "avg_fill_price": _as_optional_float(avgFillPrice),
                "last_fill_price": _as_optional_float(lastFillPrice),
                "perm_id": perm_id,
                "client_id": str(clientId or ""),
                "why_held": str(whyHeld or ""),
            }
            if perm_id and perm_id != "0":
                self.order_statuses_by_key[f"perm:{perm_id}"] = status_row
            self.order_statuses_by_order_id[str(orderId)] = status_row

        def openOrderEnd(self) -> None:  # noqa: N802
            self.events.put("openOrderEnd")

        def error(self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson: str = "") -> None:  # noqa: N802
            self.errors.append({"req_id": reqId, "code": errorCode, "message_ref": "ibapi_error_redacted"})

    app = ReadOnlyApp()
    started = _now()
    app.connect(host, port, clientId=client_id)
    thread = threading.Thread(target=app.run, name="p019-ibapi-readonly", daemon=True)
    thread.start()
    time.sleep(1.0)
    if not app.isConnected():
        raise CollectError("ibapi_connect_failed")

    app.reqManagedAccts()
    app.reqAccountSummary(
        9001,
        "All",
        "NetLiquidation,AvailableFunds,MaintMarginReq,UnrealizedPnL,$LEDGER",
    )
    app.reqAccountUpdates(True, DISPLAY_ALIAS)
    app.reqPositions()
    execution_filter = ExecutionFilter()
    execution_filter.acctCode = DISPLAY_ALIAS
    app.reqExecutions(9002, execution_filter)
    app.reqAutoOpenOrders(True)
    app.reqOpenOrders()
    app.reqAllOpenOrders()

    deadline = time.monotonic() + timeout
    seen: set[str] = set()
    required_events = {"accountSummaryEnd", "accountDownloadEnd", "positionEnd", "execDetailsEnd", "openOrderEnd"}
    while time.monotonic() < deadline and required_events - seen:
        try:
            seen.add(app.events.get(timeout=0.25))
        except queue.Empty:
            pass
    app.cancelAccountSummary(9001)
    app.reqAccountUpdates(False, DISPLAY_ALIAS)
    app.cancelPositions()
    app.disconnect()
    completed = _now()
    if required_events - seen:
        raise CollectError("ibapi_readonly_query_timeout")

    balances = []
    merged_summary = dict(app.summary)
    merged_summary.update(app.account_values)
    currencies = {
        currency
        for tag, currency in merged_summary
        if currency and currency != "BASE" or tag in {"NetLiquidation", "AvailableFunds", "MaintMarginReq", "UnrealizedPnL"}
    }
    for currency in sorted(currencies):
        net_liquidation = merged_summary.get(("NetLiquidation", currency))
        ledger_net_liquidation = merged_summary.get(("NetLiquidationByCurrency", currency))
        cash_balance = merged_summary.get(("CashBalance", currency))
        total_cash_balance = merged_summary.get(("TotalCashBalance", currency))
        available_funds = merged_summary.get(("AvailableFunds", currency))
        balances.append(
            {
                "currency": currency,
                "net_liquidation": float(net_liquidation or ledger_net_liquidation or 0.0),
                "available_funds": float(available_funds or total_cash_balance or cash_balance or 0.0),
                "cash_balance": None if cash_balance is None else float(cash_balance),
                "total_cash_balance": None if total_cash_balance is None else float(total_cash_balance),
                "net_liquidation_by_currency": None
                if ledger_net_liquidation is None
                else float(ledger_net_liquidation),
                "margin_used": float(merged_summary.get(("MaintMarginReq", currency), 0.0)),
                "unrealized_pnl": float(merged_summary.get(("UnrealizedPnL", currency), 0.0)),
                "exchange_rate": None
                if merged_summary.get(("ExchangeRate", currency)) is None
                else float(merged_summary[("ExchangeRate", currency)]),
            }
        )
    account_summary = _base_query("account_summary", success=True, started_at=started, completed_at=completed)
    account_summary["balances"] = balances
    account_summary["query_checksum"] = _source_checksum({**account_summary, "query_checksum": "sha256:pending"})

    positions = _base_query("positions", success=True, started_at=started, completed_at=completed)
    positions["positions"] = app.positions
    positions["query_checksum"] = _source_checksum({**positions, "query_checksum": "sha256:pending"})

    executions = _base_query("executions", success=True, started_at=started, completed_at=completed)
    executions["executions"] = app.executions
    executions["commissions"] = app.commissions
    executions["execution_report_rows"] = len(app.executions)
    executions["readonly_query"] = _readonly_executions_metadata()
    executions["empty_state"] = "not_available_or_no_matching_executions" if not app.executions else None
    executions["explicit_non_claims"] = [
        "does_not_prove_complete_order_history",
        "does_not_authorize_order_action",
        "does_not_prove_durable_store_reload_parity",
    ]
    executions["query_checksum"] = _source_checksum({**executions, "query_checksum": "sha256:pending"})

    open_order_rows = []
    for index, (row_key, row) in enumerate(sorted(app.open_orders.items()), start=1):
        status = app.order_statuses_by_key.get(row_key) or app.order_statuses_by_order_id.get(str(row.get("order_id"))) or {}
        merged = {**row, **{key: value for key, value in status.items() if value not in {"", None}}}
        quantity = merged.get("quantity")
        filled = merged.get("filled_quantity")
        remaining = merged.get("remaining_quantity")
        if remaining is None and quantity is not None and filled is not None:
            remaining = float(quantity) - float(filled)
        open_order_rows.append(
            {
                **merged,
                "filled_quantity": 0.0 if filled is None else filled,
                "remaining_quantity": remaining,
                "sequence": index,
            }
        )
    open_orders = _base_query("open_orders", success=True, started_at=started, completed_at=completed)
    open_orders["open_orders"] = open_order_rows
    open_orders["open_order_rows"] = len(open_order_rows)
    open_orders["readonly_query"] = _readonly_open_orders_metadata()
    open_orders["empty_state"] = "no_open_orders_returned" if not open_order_rows else None
    open_orders["explicit_non_claims"] = [
        "does_not_authorize_order_action",
        "does_not_prove_complete_order_history",
        "does_not_reproduce_tws_cancel_controls",
    ]
    open_orders["cancel_order_sent"] = False
    open_orders["replace_order_sent"] = False
    open_orders["query_checksum"] = _source_checksum({**open_orders, "query_checksum": "sha256:pending"})
    return account_summary, positions, executions, open_orders


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only IB U3028269 account summary and positions through TWS API.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--readiness-probe", type=Path, default=READINESS_PROBE)
    parser.add_argument("--port-ref", choices=sorted(PORT_REFS))
    parser.add_argument("--client-id", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--ibapi-runtime", type=Path, default=DEFAULT_IBAPI_RUNTIME)
    parser.add_argument("--allow-blocked", action="store_true", help="Write blocked query artifacts when readiness is missing")
    args = parser.parse_args()

    _add_runtime_path(args.ibapi_runtime)
    readiness = _load_readiness(args.readiness_probe)
    port_ref, port = _select_port(readiness, args.port_ref)
    ibapi_available = importlib.util.find_spec("ibapi") is not None
    readiness_ok = readiness.get("ready_for_tws_api_funds_positions_query") is True and ibapi_available and port is not None
    if port is not None:
        readiness_ok = readiness_ok and _tcp_open("127.0.0.1", port, timeout=0.75)

    if not readiness_ok:
        if not args.allow_blocked:
            raise SystemExit("TWS_API_COLLECT_BLOCKED: rerun readiness probe and pass --allow-blocked to write blocker artifacts")
        _write_blocked(args.output_dir, "tws_api_readiness_missing", args.readiness_probe)
        print(json.dumps({"status": "blocked", "blocker_id": "tws_api_readiness_missing", "output_dir": str(args.output_dir)}, ensure_ascii=False))
        return 0

    account_summary, positions, executions, open_orders = _collect_with_ibapi(host="127.0.0.1", port=port, client_id=args.client_id, timeout=args.timeout)
    _write_json(args.output_dir / "account_summary.json", account_summary)
    _write_json(args.output_dir / "positions.json", positions)
    _write_json(args.output_dir / "executions.json", executions)
    _write_json(args.output_dir / "open_orders.json", open_orders)
    print(json.dumps({"status": "ready", "port_ref": port_ref, "output_dir": str(args.output_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
