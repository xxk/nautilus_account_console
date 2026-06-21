from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "output" / "account_capability" / "ctp-paper-19053" / "real-login-20260615"
DEFAULT_OUTPUT = ROOT / "output" / "account_capability" / "ctp-paper-19053" / "source-package.json"
ACCOUNT_ID = "acct.ctp.paper.19053"
DEFAULT_OWNER_EVIDENCE_ROOT = Path("D:/Nautilus/nautilus_ctp_adapter/output/account-console-ctp19053-readback")


class BuildError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def _checksum_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(encoded).hexdigest()


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _artifact_checksum(payload: dict[str, Any]) -> str:
    return str(payload.get("query_checksum") or _checksum_payload(payload))


def _extract_account(account_query: dict[str, Any]) -> dict[str, float | str]:
    _require(account_query.get("baseline") == "account-query-smoke-v1", "account query baseline mismatch")
    _require(account_query.get("success") is True, "account query did not pass")
    _require(account_query.get("td_login_success") is True, "account query did not prove TD login success")
    _require(account_query.get("bridge_command_kinds") == ["connect", "query_account"], "unexpected account commands")
    account = account_query.get("account")
    _require(isinstance(account, dict), "account query missing account payload")
    _require(str(account.get("account_id")) == "19053", "account query must be for 19053")
    for field in ["balance", "available", "margin"]:
        _require(isinstance(account.get(field), (int, float)), f"account query missing numeric {field}")
    return {
        "currency": "CNY",
        "equity": float(account["balance"]),
        "available_cash": float(account["available"]),
        "margin_used": float(account["margin"]),
        "frozen_cash": 0.0,
        "position_profit": float(account.get("position_profit") or 0.0),
    }


def _extract_positions(position_query: dict[str, Any]) -> list[dict[str, Any]]:
    _require(position_query.get("baseline") == "position-query-smoke-v1", "position query baseline mismatch")
    _require(position_query.get("success") is True, "position query did not pass")
    _require(position_query.get("td_login_success") is True, "position query did not prove TD login success")
    _require(position_query.get("bridge_command_kinds") == ["connect", "query_positions"], "unexpected position commands")
    rows = position_query.get("positions")
    _require(isinstance(rows, list), "position query missing positions list")
    positions = []
    for row in rows:
        _require(isinstance(row, dict), "position row must be object")
        instrument = str(row.get("venue_symbol") or "")
        direction = str(row.get("direction") or "").lower()
        net_qty = int(row.get("position_qty") or 0)
        yd_qty = int(row.get("yd_position_qty") or 0)
        td_qty = int(row.get("td_position_qty") or 0)
        positions.append(
            {
                "instrument": instrument,
                "exchange": row.get("exchange_id"),
                "direction": "long" if direction in {"long", "buy", "2"} else "short",
                "net_qty": net_qty,
                "today_qty": td_qty,
                "yesterday_qty": yd_qty,
                "available_qty": net_qty,
                "frozen_qty": 0,
                "avg_price": None if net_qty == 0 else float(row.get("position_cost") or 0.0) / net_qty,
                "unrealized_pnl": 0.0,
            }
        )
    return positions


def _extract_snapshot_positions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    _require(snapshot.get("baseline") == "ctp-paper-readonly-snapshot-v1", "snapshot baseline mismatch")
    _require(snapshot.get("success") is True, "snapshot did not pass")
    positions_payload = snapshot.get("positions")
    _require(isinstance(positions_payload, dict), "snapshot missing positions object")
    disposition = positions_payload.get("disposition", {})
    _require(disposition.get("status") == "passed", "snapshot positions did not pass")
    rows = positions_payload.get("records")
    _require(isinstance(rows, list), "snapshot positions records must be list")
    positions: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        _require(isinstance(row, dict), "snapshot position row must be object")
        instrument = str(row.get("venue_symbol") or "")
        _require(instrument, "snapshot position missing venue_symbol")
        direction = str(row.get("direction") or "").lower()
        net_qty = int(row.get("position_qty") or 0)
        yd_qty = int(row.get("yd_position_qty") or 0)
        td_qty = int(row.get("td_position_qty") or 0)
        positions.append(
            {
                "instrument": instrument,
                "exchange": row.get("exchange_id"),
                "direction": "long" if direction in {"long", "buy", "2"} else "short",
                "net_qty": net_qty,
                "today_qty": td_qty,
                "yesterday_qty": yd_qty,
                "available_qty": net_qty,
                "frozen_qty": 0,
                "avg_price": None if net_qty == 0 else float(row.get("position_cost") or 0.0) / net_qty,
                "unrealized_pnl": 0.0,
                "source_ref": "owner://nautilus_ctp_adapter/account-console-ctp19053-readback/paper_readonly_snapshot.json"
                f"#positions/{index}",
            }
        )
    return positions


def _extract_snapshot_orders(snapshot: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    order_trade = snapshot.get("order_trade")
    _require(isinstance(order_trade, dict), "snapshot missing order_trade object")
    observed = order_trade.get("observed_order_event_count")
    current = order_trade.get("current_session_order_count", observed)
    historical = order_trade.get("historical_order_count", 0)
    _require(observed in {0, None}, "snapshot order rows are not normalized yet")
    return [], {
        "state": "empty" if observed == 0 or current == 0 else "blocked",
        "observed_order_event_count": observed,
        "current_session_order_count": current,
        "historical_order_count": historical,
        "empty_state": "no_open_orders_returned" if observed == 0 or current == 0 else None,
        "complete_history_claimed": False,
    }


def _extract_snapshot_fills(snapshot: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    order_trade = snapshot.get("order_trade")
    _require(isinstance(order_trade, dict), "snapshot missing order_trade object")
    observed = order_trade.get("observed_trade_event_count")
    current = order_trade.get("current_session_trade_count", observed)
    historical = order_trade.get("historical_trade_count", 0)
    _require(observed in {0, None}, "snapshot trade rows are not normalized yet")
    return [], {
        "state": "empty" if observed == 0 or current == 0 else "blocked",
        "observed_trade_event_count": observed,
        "current_session_trade_count": current,
        "historical_trade_count": historical,
        "empty_state": "no_trade_events_returned" if observed == 0 or current == 0 else None,
        "complete_history_claimed": False,
    }


def _side_label(value: Any) -> str:
    text = str(value).strip().lower()
    return "SELL" if text in {"1", "sell", "short"} else "BUY"


def _open_order_status(row: dict[str, Any]) -> str:
    leaves_qty = int(row.get("leaves_qty") or 0)
    trade_volume = int(row.get("trade_volume") or 0)
    status = int(row.get("status") or 0)
    status_text = str(row.get("error_msg") or "").lower()
    if status == 5 or "撤" in status_text or status_text in {"cancelled", "canceled"}:
        return "canceled"
    if (status == 0 and leaves_qty == 0) or trade_volume > 0:
        return "filled"
    if leaves_qty > 0:
        return "working"
    return "unknown"


def _extract_order_trade_query(
    query: dict[str, Any] | None,
    *,
    query_path: Path | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if query is None:
        return [], [], {}
    _require(query.get("schema") == "account-console.openctp-order-trade-query.v1", "order/trade query schema mismatch")
    _require(query.get("success") is True, "order/trade query did not pass")
    _require(query.get("login_success") is True, "order/trade query did not prove login success")
    _require(query.get("ready") is True, "order/trade query did not prove ready state")
    _require(query.get("query_order_code") == 0, "order query did not pass")
    _require(query.get("query_trade_code") == 0, "trade query did not pass")
    _require(query.get("order_send_called") is False, "order/trade query must not send orders")
    _require(query.get("order_action_sent") is False, "order/trade query must not send order actions")
    _require(query.get("raw_secret_values_recorded") is False, "order/trade query recorded raw secrets")
    _require(query.get("raw_broker_endpoint_recorded") is False, "order/trade query recorded raw endpoints")
    rows = query.get("orders")
    trades = query.get("trades")
    _require(isinstance(rows, list), "order/trade query missing orders")
    _require(isinstance(trades, list), "order/trade query missing trades")
    source_ref = _source_ref_for_owner(query_path) if query_path is not None else "order_trade_query.json"
    source_checksum = _artifact_checksum(query)
    open_orders: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        _require(isinstance(row, dict), "order query row must be object")
        leaves_qty = int(row.get("leaves_qty") or 0)
        filled_qty = max(int(row.get("qty") or 0) - leaves_qty, 0)
        status = _open_order_status(row)
        if status != "working":
            continue
        order_id = str(row.get("order_id") or row.get("order_ref") or index)
        client_order_id = str(row.get("order_ref") or order_id)
        open_orders.append(
            {
                "report_id": f"ctp19053.order.{order_id}",
                "nautilus_report_type": "OrderStatusReport",
                "client_order_id": client_order_id,
                "venue_order_id": order_id,
                "instrument_id": str(row.get("symbol") or ""),
                "instrument": str(row.get("symbol") or ""),
                "exchange": "SHFE" if str(row.get("symbol") or "").startswith(("zn", "rb")) else None,
                "destination": "SHFE" if str(row.get("symbol") or "").startswith(("zn", "rb")) else None,
                "side": _side_label(row.get("side")),
                "order_type": "LIMIT",
                "quantity": int(row.get("qty") or 0),
                "filled_quantity": filled_qty,
                "remaining_quantity": leaves_qty,
                "limit_price": float(row.get("price") or 0.0),
                "price": float(row.get("price") or 0.0),
                "time_in_force": "GTC",
                "status": status,
                "order_status": row.get("error_msg") or status,
                "order_status_code": int(row.get("status") or 0),
                "sequence": index,
                "source_ref": f"{source_ref}#orders/{index}",
                "source_checksum": source_checksum,
                "report_provenance_ref": f"{source_ref}#orders/{index}",
                "report_msg_ref": f"{source_ref}#orders/{index}",
                "report_msg_checksum": source_checksum,
            }
        )
    fills: list[dict[str, Any]] = []
    for index, row in enumerate(trades, start=1):
        _require(isinstance(row, dict), "trade query row must be object")
        order_id = str(row.get("order_id") or row.get("order_ref") or index)
        client_order_id = str(row.get("order_ref") or order_id)
        fills.append(
            {
                "report_id": f"ctp19053.fill.{order_id}.{index}",
                "nautilus_report_type": "FillReport",
                "client_order_id": client_order_id,
                "venue_order_id": order_id,
                "trade_id": str(row.get("order_id") or index),
                "instrument_id": str(row.get("symbol") or ""),
                "instrument": str(row.get("symbol") or ""),
                "exchange": "SHFE" if str(row.get("symbol") or "").startswith(("zn", "rb")) else None,
                "destination": "SHFE" if str(row.get("symbol") or "").startswith(("zn", "rb")) else None,
                "side": _side_label(row.get("side")),
                "status": "filled",
                "order_status": "filled",
                "quantity": int(row.get("trade_volume") or row.get("qty") or 0),
                "filled_quantity": int(row.get("trade_volume") or row.get("qty") or 0),
                "remaining_quantity": 0,
                "last_px": float(row.get("trade_price") or row.get("price") or 0.0),
                "price": float(row.get("trade_price") or row.get("price") or 0.0),
                "sequence": index,
                "source_ref": f"{source_ref}#trades/{index}",
                "source_checksum": source_checksum,
                "report_provenance_ref": f"{source_ref}#trades/{index}",
                "report_msg_ref": f"{source_ref}#trades/{index}",
                "report_msg_checksum": source_checksum,
            }
        )
    health = {
        "order_trade_query_ref": source_ref,
        "order_trade_query_success": True,
        "order_trade_query_login_success": True,
        "order_trade_query_ready": True,
        "order_trade_query_settlement_code": query.get("settlement_code"),
        "order_trade_query_total_order_rows": len(rows),
        "order_trade_query_open_order_rows": len(open_orders),
        "order_trade_query_trade_rows": len(fills),
        "order_query_is_last_observed": query.get("order_query_is_last_observed"),
        "trade_query_is_last_observed": query.get("trade_query_is_last_observed"),
        "readonly_api_calls": query.get("readonly_api_calls"),
    }
    return open_orders, fills, health


def _source_ref_for_owner(path: Path) -> str:
    if not path.is_absolute():
        path = ROOT / path
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        pass
    try:
        owner_root = Path("D:/Nautilus/nautilus_ctp_adapter")
        return "owner://nautilus_ctp_adapter/" + str(path.relative_to(owner_root)).replace("\\", "/")
    except ValueError:
        return "owner://nautilus_ctp_adapter/" + path.name


def _read_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    _require(path.exists(), f"optional evidence missing: {path}")
    return _read_json(path)


def _order_truth_health(order_truth: dict[str, Any] | None) -> dict[str, Any]:
    if order_truth is None:
        return {}
    _require(order_truth.get("baseline") == "td-order-truth-v1", "order truth baseline mismatch")
    _require(order_truth.get("success") is True, "order truth did not pass")
    _require(order_truth.get("login_success") is True, "order truth did not prove login success")
    _require(order_truth.get("ready") is True, "order truth did not prove ready state")
    return {
        "td_order_truth_login_success": True,
        "td_order_truth_ready": True,
        "td_order_truth_settlement_code": order_truth.get("settlement_code"),
        "td_order_truth_observed_callback_count": order_truth.get("observed_callback_count"),
        "td_order_truth_observed_order_event_count": order_truth.get("observed_order_event_count"),
        "td_order_truth_observed_trade_event_count": order_truth.get("observed_trade_event_count"),
        "td_order_truth_no_callbacks_observed": order_truth.get("no_callbacks_observed"),
    }


def build_source_package(account_query_path: Path, position_query_path: Path, output_path: Path) -> dict[str, Any]:
    account_query = _read_json(account_query_path)
    position_query = _read_json(position_query_path)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    run_id = f"{account_query.get('query_request_id', 'account')}-{position_query.get('query_request_id', 'positions')}"
    source_inputs = {
        "account_query": _source_ref(account_query_path),
        "position_query": _source_ref(position_query_path),
    }
    payload: dict[str, Any] = {
        "schema_version": "account_source_artifact.v1",
        "artifact_id": f"source.ctp.paper.19053.{datetime.now(UTC):%Y%m%d}.{run_id}",
        "account_id": ACCOUNT_ID,
        "display_alias": "19053",
        "source_owner": "nautilus_ctp_adapter",
        "source_kind": "ctp_trader_api",
        "source_mode": "paper_observation",
        "account_domain": "paper",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": datetime.now(UTC).date().isoformat(),
        "query_window_id": f"ctp19053.{datetime.now(UTC):%Y%m%d}.{run_id}",
        "query_started_at": observed_at,
        "query_completed_at": observed_at,
        "observed_at": observed_at,
        "source_ref": _source_ref(output_path),
        "source_checksum": "sha256:pending",
        "source_inputs": source_inputs,
        "balances": [_extract_account(account_query)],
        "positions": _extract_positions(position_query),
        "orders": [],
        "fills": [],
        "source_health": {
            "state": "ready",
            "lag_ms": 0,
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "account_query_ref": source_inputs["account_query"],
            "position_query_ref": source_inputs["position_query"],
        },
        "blockers": [],
    }
    payload["source_checksum"] = _checksum_payload({**payload, "source_checksum": "sha256:pending"})
    return payload


def build_source_package_from_owner_snapshot(
    *,
    account_query_path: Path,
    snapshot_path: Path,
    output_path: Path,
    order_truth_path: Path | None = None,
    order_trade_query_path: Path | None = None,
) -> dict[str, Any]:
    account_query = _read_json(account_query_path)
    snapshot = _read_json(snapshot_path)
    order_truth = _read_optional_json(order_truth_path)
    order_trade_query = _read_optional_json(order_trade_query_path)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    session_label = str(account_query.get("session_label") or snapshot.get("schema", {}).get("session_label") or "unknown")
    source_inputs = {
        "account_query": _source_ref_for_owner(account_query_path),
        "paper_readonly_snapshot": _source_ref_for_owner(snapshot_path),
    }
    source_input_checksums = {
        "account_query": _artifact_checksum(account_query),
        "paper_readonly_snapshot": _artifact_checksum(snapshot),
    }
    if order_truth_path is not None and order_truth is not None:
        source_inputs["td_order_truth"] = _source_ref_for_owner(order_truth_path)
        source_input_checksums["td_order_truth"] = _artifact_checksum(order_truth)
    if order_trade_query_path is not None and order_trade_query is not None:
        source_inputs["order_trade_query"] = _source_ref_for_owner(order_trade_query_path)
        source_input_checksums["order_trade_query"] = _artifact_checksum(order_trade_query)
    snapshot_orders, order_state = _extract_snapshot_orders(snapshot)
    snapshot_fills, fill_state = _extract_snapshot_fills(snapshot)
    query_orders, query_fills, order_trade_health = _extract_order_trade_query(
        order_trade_query,
        query_path=order_trade_query_path,
    )
    orders = query_orders if order_trade_query is not None else snapshot_orders
    fills = query_fills if order_trade_query is not None else snapshot_fills
    if order_trade_query is not None:
        order_state = {
            "state": "available" if orders else "empty",
            "empty_state": None if orders else "no_open_orders_returned",
            "complete_history_claimed": False,
        }
        fill_state = {
            "state": "available" if fills else "empty",
            "empty_state": None if fills else "no_trade_events_returned",
            "complete_history_claimed": False,
        }
    order_truth_health = _order_truth_health(order_truth)
    payload: dict[str, Any] = {
        "schema_version": "account_source_artifact.v1",
        "artifact_id": f"source.ctp.paper.19053.{datetime.now(UTC):%Y%m%d%H%M%S}.{session_label}",
        "account_id": ACCOUNT_ID,
        "display_alias": "19053",
        "source_owner": "nautilus_ctp_adapter",
        "source_kind": "ctp_trader_api",
        "source_mode": "paper_observation",
        "account_domain": "paper",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": datetime.now(UTC).date().isoformat(),
        "query_window_id": f"ctp19053.{session_label}",
        "query_started_at": observed_at,
        "query_completed_at": observed_at,
        "observed_at": observed_at,
        "source_ref": _source_ref(output_path),
        "source_checksum": "sha256:pending",
        "source_inputs": source_inputs,
        "source_input_checksums": source_input_checksums,
        "balances": [_extract_account(account_query)],
        "positions": _extract_snapshot_positions(snapshot),
        "orders": orders,
        "fills": fills,
        "source_health": {
            "state": "ready",
            "lag_ms": 0,
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "account_query_ref": source_inputs["account_query"],
            "paper_readonly_snapshot_ref": source_inputs["paper_readonly_snapshot"],
            "account_query_success": account_query.get("success") is True,
            "positions_query_success": True,
            "open_orders_state": order_state["state"],
            "open_order_rows": len(orders),
            "open_orders_empty_state": order_state["empty_state"],
            "fills_state": fill_state["state"],
            "fill_rows": len(fills),
            "fills_empty_state": fill_state["empty_state"],
            "complete_order_history_claimed": False,
            "complete_trade_history_claimed": False,
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "screenshot_used_for_values": False,
            "order_action_sent": False,
            "cancel_order_sent": False,
            "replace_order_sent": False,
            "api_transport": "ctp_trader_api",
            **order_trade_health,
            **order_truth_health,
        },
        "blockers": [],
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "screenshot_used_for_values": False,
            "order_action_sent": False,
            "cancel_order_sent": False,
            "replace_order_sent": False,
        },
    }
    payload["source_checksum"] = _checksum_payload({**payload, "source_checksum": "sha256:pending"})
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Account Console CTP 19053 source package from real-login read-only queries.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--account-query", type=Path)
    parser.add_argument("--position-query", type=Path)
    parser.add_argument("--owner-session-label")
    parser.add_argument("--owner-evidence-root", type=Path, default=DEFAULT_OWNER_EVIDENCE_ROOT)
    parser.add_argument("--paper-readonly-snapshot", type=Path)
    parser.add_argument("--td-order-truth", type=Path)
    parser.add_argument("--order-trade-query", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if args.owner_session_label or args.paper_readonly_snapshot:
        owner_dir = args.owner_evidence_root / str(args.owner_session_label) if args.owner_session_label else args.owner_evidence_root
        account_query = args.account_query or owner_dir / "account_query.json"
        snapshot = args.paper_readonly_snapshot or owner_dir / "paper_readonly_snapshot.json"
        payload = build_source_package_from_owner_snapshot(
            account_query_path=account_query,
            snapshot_path=snapshot,
            output_path=args.output,
            order_truth_path=args.td_order_truth,
            order_trade_query_path=args.order_trade_query,
        )
    else:
        account_query = args.account_query or args.input_dir / "account_query.json"
        position_query = args.position_query or args.input_dir / "position_query.json"
        payload = build_source_package(account_query, position_query, args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CTP19053_SOURCE_PACKAGE_BUILT: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
