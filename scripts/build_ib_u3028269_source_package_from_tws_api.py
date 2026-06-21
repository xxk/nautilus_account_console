from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCOUNT_ID = "acct.ib.live.u3028269"
DISPLAY_ALIAS = "U3028269"
DEFAULT_INPUT_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
DEFAULT_OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
READINESS_PROBE = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"


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


def _artifact_checksum(payload: dict[str, Any]) -> str:
    for key in ["query_checksum", "source_checksum"]:
        value = payload.get(key)
        if isinstance(value, str) and value.startswith("sha256:"):
            return value
    return _checksum_payload(payload)


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _check_no_sensitive_material(value: Any) -> None:
    forbidden_keys = {"password", "passwd", "auth_code", "authcode", "token", "secret", "session_password", "api_key"}
    allowed_boundary_keys = {
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "screenshot_used_for_values",
        "screenshot_used_for_funds_positions",
        "order_action_sent",
    }
    forbidden_fragments = ["password=", "passwd=", "auth_code=", "api_key=", "secret=", "127.0.0.1:"]
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            _require(
                normalized in allowed_boundary_keys
                or (normalized not in forbidden_keys and "password" not in normalized and "secret" not in normalized),
                f"sensitive key not allowed: {key}",
            )
            _check_no_sensitive_material(item)
    elif isinstance(value, list):
        for item in value:
            _check_no_sensitive_material(item)
    elif isinstance(value, str):
        lowered = value.lower()
        hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
        _require(not hits, f"sensitive/raw endpoint fragment not allowed: {hits}")


def _validate_common_query(payload: dict[str, Any], *, expected_kind: str) -> None:
    _check_no_sensitive_material(payload)
    _require(payload.get("schema") == "account-console.ib-tws-api-query.v1", f"{expected_kind}: schema mismatch")
    _require(payload.get("account_id") == ACCOUNT_ID, f"{expected_kind}: account_id mismatch")
    _require(payload.get("display_alias") == DISPLAY_ALIAS, f"{expected_kind}: display_alias mismatch")
    _require(payload.get("query_kind") == expected_kind, f"{expected_kind}: query_kind mismatch")
    _require(payload.get("source_kind") == "ib_tws_api", f"{expected_kind}: source_kind mismatch")
    _require(payload.get("success") is True, f"{expected_kind}: query did not pass")
    _require(payload.get("tws_api_login_confirmed") is True, f"{expected_kind}: TWS API login not confirmed")
    _require(payload.get("raw_secret_values_recorded") is False, f"{expected_kind}: raw secrets recorded")
    _require(payload.get("screenshot_used_for_values") is False, f"{expected_kind}: screenshot used for values")
    _require(payload.get("order_action_sent") is False, f"{expected_kind}: order action sent")


def _extract_balances(account_summary: dict[str, Any]) -> list[dict[str, Any]]:
    _validate_common_query(account_summary, expected_kind="account_summary")
    rows = account_summary.get("balances")
    _require(isinstance(rows, list), "account_summary: balances must be list")
    balances: list[dict[str, Any]] = []
    for row in rows:
        _require(isinstance(row, dict), "balance row must be object")
        currency = str(row.get("currency") or "")
        _require(currency, "balance row missing currency")
        for field in ["net_liquidation", "available_funds"]:
            _require(isinstance(row.get(field), (int, float)), f"balance row missing numeric {field}")
        balances.append(
            {
                "currency": currency,
                "equity": float(row["net_liquidation"]),
                "available_cash": float(row["available_funds"]),
                "cash": None if row.get("cash_balance") is None else float(row["cash_balance"]),
                "total_cash": None if row.get("total_cash_balance") is None else float(row["total_cash_balance"]),
                "net_liquidation_by_currency": None
                if row.get("net_liquidation_by_currency") is None
                else float(row["net_liquidation_by_currency"]),
                "margin_used": float(row.get("margin_used") or 0.0),
                "unrealized_pnl": float(row.get("unrealized_pnl") or 0.0),
                "exchange_rate": None if row.get("exchange_rate") is None else float(row["exchange_rate"]),
            }
        )
    return balances


def _extract_positions(positions_query: dict[str, Any]) -> list[dict[str, Any]]:
    _validate_common_query(positions_query, expected_kind="positions")
    rows = positions_query.get("positions")
    _require(isinstance(rows, list), "positions: positions must be list")
    positions: list[dict[str, Any]] = []
    for row in rows:
        _require(isinstance(row, dict), "position row must be object")
        instrument = str(row.get("instrument") or "")
        _require(instrument, "position row missing instrument")
        net_qty = float(row.get("net_qty") or 0.0)
        positions.append(
            {
                "instrument": instrument,
                "exchange": row.get("exchange"),
                "direction": "long" if net_qty >= 0 else "short",
                "net_qty": net_qty,
                "available_qty": net_qty,
                "avg_price": None if row.get("avg_cost") is None else float(row["avg_cost"]),
                "unrealized_pnl": None if row.get("unrealized_pnl") is None else float(row["unrealized_pnl"]),
            }
        )
    return positions


def _extract_fills(executions_query: dict[str, Any] | None) -> list[dict[str, Any]]:
    if executions_query is None:
        return []
    _validate_common_query(executions_query, expected_kind="executions")
    rows = executions_query.get("executions")
    _require(isinstance(rows, list), "executions: executions must be list")
    commissions = {
        str(row.get("exec_id") or ""): row
        for row in executions_query.get("commissions", [])
        if isinstance(row, dict)
    }
    fills: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        _require(isinstance(row, dict), "execution row must be object")
        exec_id = str(row.get("exec_id") or "")
        _require(exec_id, "execution row missing exec_id")
        commission = commissions.get(exec_id, {})
        source_ref = f"output/account_capability/ib-live-u3028269/tws-api/executions.json#execution-{index}"
        fills.append(
            {
                "report_id": f"report.ib.u3028269.fill.{index:06d}",
                "nautilus_report_type": "FillReport",
                "trade_id": exec_id,
                "client_order_id": str(row.get("order_ref") or row.get("order_id") or "unknown"),
                "venue_order_id": str(row.get("perm_id") or row.get("order_id") or "unknown"),
                "instrument_id": str(row.get("instrument_id") or row.get("symbol") or "unknown"),
                "instrument": str(row.get("symbol") or row.get("instrument_id") or "unknown"),
                "exchange": row.get("exchange"),
                "side": str(row.get("side") or "UNKNOWN").upper(),
                "quantity": float(row.get("shares") or 0.0),
                "filled_quantity": float(row.get("shares") or 0.0),
                "remaining_quantity": 0.0,
                "last_px": float(row.get("price") or 0.0),
                "last_qty": float(row.get("shares") or 0.0),
                "price": float(row.get("price") or 0.0),
                "commission": commission.get("commission"),
                "commission_currency": commission.get("currency"),
                "realized_pnl": commission.get("realized_pnl"),
                "event_timestamp": str(row.get("time") or ""),
                "sequence": index,
                "source_ref": source_ref,
                "source_checksum": str(executions_query["query_checksum"]),
            }
        )
    return fills


def _extract_orders(open_orders_query: dict[str, Any] | None) -> list[dict[str, Any]]:
    if open_orders_query is None:
        return []
    _validate_common_query(open_orders_query, expected_kind="open_orders")
    readonly = open_orders_query.get("readonly_query")
    _require(isinstance(readonly, dict), "open_orders: readonly query metadata missing")
    _require(readonly.get("api_call") == "reqAllOpenOrders", "open_orders: readonly api mismatch")
    _require(readonly.get("order_action_sent") is False, "open_orders: order action sent")
    _require(readonly.get("cancel_order_sent") is False, "open_orders: cancel sent")
    _require(readonly.get("replace_order_sent") is False, "open_orders: replace sent")
    _require(readonly.get("complete_history_claimed") is False, "open_orders: complete history claimed")
    rows = open_orders_query.get("open_orders")
    _require(isinstance(rows, list), "open_orders: open_orders must be list")
    orders: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        _require(isinstance(row, dict), "open order row must be object")
        order_id = str(row.get("order_id") or "")
        _require(order_id, "open order row missing order_id")
        source_ref = f"output/account_capability/ib-live-u3028269/tws-api/open_orders.json#open-order-{index}"
        orders.append(
            {
                "report_id": f"report.ib.u3028269.open_order.{index:06d}",
                "nautilus_report_type": "OrderStatusReport",
                "client_order_id": str(row.get("order_ref") or order_id),
                "venue_order_id": str(row.get("perm_id") or order_id),
                "instrument_id": str(row.get("instrument") or row.get("symbol") or "unknown"),
                "instrument": str(row.get("symbol") or row.get("instrument") or "unknown"),
                "exchange": row.get("exchange"),
                "destination": row.get("destination") or row.get("exchange"),
                "side": str(row.get("side") or "UNKNOWN").upper(),
                "order_type": str(row.get("order_type") or "UNKNOWN").upper(),
                "quantity": None if row.get("quantity") is None else float(row["quantity"]),
                "filled_quantity": None if row.get("filled_quantity") is None else float(row["filled_quantity"]),
                "remaining_quantity": None if row.get("remaining_quantity") is None else float(row["remaining_quantity"]),
                "limit_price": None if row.get("limit_price") is None else float(row["limit_price"]),
                "price": None if row.get("limit_price") is None else float(row["limit_price"]),
                "time_in_force": str(row.get("time_in_force") or ""),
                "status": str(row.get("status") or "unknown"),
                "order_status": str(row.get("status") or "unknown"),
                "sequence": int(row.get("sequence") or index),
                "source_ref": source_ref,
                "source_checksum": str(open_orders_query["query_checksum"]),
                "report_provenance_ref": source_ref,
            }
        )
    return orders


def _executions_readonly_query_health(executions_query: dict[str, Any] | None) -> dict[str, Any] | None:
    if executions_query is None:
        return None
    readonly = executions_query.get("readonly_query")
    _require(isinstance(readonly, dict), "executions: readonly query metadata missing")
    _require(readonly.get("api_call") == "reqExecutions", "executions: readonly api mismatch")
    _require(readonly.get("filter_type") == "ExecutionFilter", "executions: filter type mismatch")
    _require(readonly.get("filter_account_ref") == "ib-account-ref://U3028269", "executions: filter account ref mismatch")
    _require(readonly.get("filter_account_raw_value_recorded") is False, "executions: raw account filter recorded")
    _require(readonly.get("order_action_sent") is False, "executions: order action sent")
    _require(readonly.get("complete_history_claimed") is False, "executions: complete history claimed")
    return {
        "api_call": readonly["api_call"],
        "filter_type": readonly["filter_type"],
        "filter_account_ref": readonly["filter_account_ref"],
        "filter_account_raw_value_recorded": False,
        "query_scope": readonly.get("query_scope"),
        "complete_history_claimed": False,
        "order_action_sent": False,
    }


def _open_orders_readonly_query_health(open_orders_query: dict[str, Any] | None) -> dict[str, Any] | None:
    if open_orders_query is None:
        return None
    readonly = open_orders_query.get("readonly_query")
    _require(isinstance(readonly, dict), "open_orders: readonly query metadata missing")
    _require(readonly.get("api_call") == "reqAllOpenOrders", "open_orders: readonly api mismatch")
    _require(readonly.get("order_action_sent") is False, "open_orders: order action sent")
    _require(readonly.get("cancel_order_sent") is False, "open_orders: cancel sent")
    _require(readonly.get("replace_order_sent") is False, "open_orders: replace sent")
    _require(readonly.get("complete_history_claimed") is False, "open_orders: complete history claimed")
    return {
        "api_call": readonly["api_call"],
        "callback_rows": readonly.get("callback_rows", []),
        "query_scope": readonly.get("query_scope"),
        "complete_history_claimed": False,
        "order_action_sent": False,
        "cancel_order_sent": False,
        "replace_order_sent": False,
    }


def _blocked_package(output_path: Path, readiness_probe_path: Path, reason: str) -> dict[str, Any]:
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_ref = _source_ref(output_path)
    readiness_ref = _source_ref(readiness_probe_path)
    payload: dict[str, Any] = {
        "schema_version": "account_source_artifact.v1",
        "artifact_id": f"source.ib.live.u3028269.blocked.{datetime.now(UTC):%Y%m%d%H%M%S}",
        "account_id": ACCOUNT_ID,
        "display_alias": DISPLAY_ALIAS,
        "source_owner": "account-console-broker-observation-session",
        "source_kind": "ib_tws_observation",
        "source_mode": "live_observation_blocked",
        "account_domain": "live",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": datetime.now(UTC).date().isoformat(),
        "query_window_id": f"ib-u3028269.blocked.{datetime.now(UTC):%Y%m%d%H%M%S}",
        "query_started_at": observed_at,
        "query_completed_at": observed_at,
        "observed_at": observed_at,
        "source_ref": source_ref,
        "source_checksum": "sha256:pending",
        "source_inputs": {
            "readiness_probe": readiness_ref,
            "account_summary_query": None,
            "positions_query": None,
            "executions_query": None,
            "open_orders_query": None,
        },
        "source_input_checksums": {
            "readiness_probe": "sha256:pending",
            "account_summary_query": None,
            "positions_query": None,
            "executions_query": None,
            "open_orders_query": None,
        },
        "balances": [],
        "positions": [],
        "orders": [],
        "fills": [],
        "source_health": {
            "state": "blocked",
            "blocker_id": "tws_api_readiness_missing",
            "reason": reason,
            "readiness_probe_ref": readiness_ref,
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "raw_secret_values_recorded": False,
            "screenshot_used_for_values": False,
            "api_transport": "ib_tws_api",
        },
        "blockers": [
            {
                "blocker_id": "tws_api_readiness_missing",
                "type": "source_unavailable",
                "owner": "account-console-broker-observation-session",
                "next_action": (
                    "Enable the logged-in TWS/Gateway API socket, collect account_summary.json and positions.json "
                    "through TWS API, then rebuild this source package."
                ),
                "source_ref": readiness_ref,
                "checksum": "sha256:pending",
            }
        ],
        "boundaries": {
            "raw_secret_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "tws_api_account_query_required": True,
            "order_action_sent": False,
        },
    }
    checksum = _checksum_payload({**payload, "source_checksum": "sha256:pending"})
    payload["source_checksum"] = checksum
    payload["blockers"][0]["checksum"] = checksum
    return payload


def build_source_package(
    *,
    account_summary_path: Path,
    positions_path: Path,
    executions_query_path: Path | None,
    open_orders_query_path: Path | None,
    readiness_probe_path: Path,
    output_path: Path,
    allow_blocked: bool,
) -> dict[str, Any]:
    readiness = _read_json(readiness_probe_path) if readiness_probe_path.exists() else {}
    if not readiness.get("ready_for_tws_api_funds_positions_query"):
        _require(allow_blocked, "TWS API readiness missing; rerun with --allow-blocked to write a typed blocker package")
        return _blocked_package(output_path, readiness_probe_path, "tws_api_readiness_missing")
    if not account_summary_path.exists() or not positions_path.exists():
        _require(allow_blocked, "TWS API query inputs missing; rerun with --allow-blocked to write a typed blocker package")
        return _blocked_package(output_path, readiness_probe_path, "tws_api_query_inputs_missing")

    account_summary = _read_json(account_summary_path)
    positions_query = _read_json(positions_path)
    executions_query = _read_json(executions_query_path) if executions_query_path and executions_query_path.exists() else None
    open_orders_query = _read_json(open_orders_query_path) if open_orders_query_path and open_orders_query_path.exists() else None
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_inputs = {
        "readiness_probe": _source_ref(readiness_probe_path),
        "account_summary_query": _source_ref(account_summary_path),
        "positions_query": _source_ref(positions_path),
        "executions_query": _source_ref(executions_query_path) if executions_query_path and executions_query_path.exists() else None,
        "open_orders_query": _source_ref(open_orders_query_path) if open_orders_query_path and open_orders_query_path.exists() else None,
    }
    source_input_checksums = {
        "readiness_probe": _artifact_checksum(readiness),
        "account_summary_query": _artifact_checksum(account_summary),
        "positions_query": _artifact_checksum(positions_query),
        "executions_query": _artifact_checksum(executions_query) if executions_query else None,
        "open_orders_query": _artifact_checksum(open_orders_query) if open_orders_query else None,
    }
    fills = _extract_fills(executions_query)
    orders = _extract_orders(open_orders_query)
    payload: dict[str, Any] = {
        "schema_version": "account_source_artifact.v1",
        "artifact_id": f"source.ib.live.u3028269.{datetime.now(UTC):%Y%m%d%H%M%S}",
        "account_id": ACCOUNT_ID,
        "display_alias": DISPLAY_ALIAS,
        "source_owner": "account-console-broker-observation-session",
        "source_kind": "ib_tws_observation",
        "source_mode": "live_observation",
        "account_domain": "live",
        "observation_mode": "snapshot",
        "event_stream": "not_implemented",
        "trading_day": datetime.now(UTC).date().isoformat(),
        "query_window_id": f"ib-u3028269.{datetime.now(UTC):%Y%m%d%H%M%S}",
        "query_started_at": observed_at,
        "query_completed_at": observed_at,
        "observed_at": observed_at,
        "source_ref": _source_ref(output_path),
        "source_checksum": "sha256:pending",
        "source_inputs": source_inputs,
        "source_input_checksums": source_input_checksums,
        "balances": _extract_balances(account_summary),
        "positions": _extract_positions(positions_query),
        "orders": orders,
        "fills": fills,
        "source_health": {
            "state": "ready",
            "lag_ms": 0,
            "observation_mode": "snapshot",
            "event_stream": "not_implemented",
            "readiness_probe_ref": source_inputs["readiness_probe"],
            "account_summary_query_ref": source_inputs["account_summary_query"],
            "positions_query_ref": source_inputs["positions_query"],
            "executions_query_ref": source_inputs["executions_query"],
            "open_orders_query_ref": source_inputs["open_orders_query"],
            "executions_query_success": executions_query.get("success") is True if executions_query else False,
            "executions_readonly_query": _executions_readonly_query_health(executions_query),
            "execution_report_rows": len(fills),
            "execution_report_state": "available" if fills else "not_available_or_empty",
            "open_orders_query_success": open_orders_query.get("success") is True if open_orders_query else False,
            "open_orders_readonly_query": _open_orders_readonly_query_health(open_orders_query),
            "open_order_rows": len(orders),
            "open_orders_state": "available" if orders else "empty",
            "raw_secret_values_recorded": False,
            "screenshot_used_for_values": False,
            "api_transport": "ib_tws_api",
        },
        "blockers": [],
        "boundaries": {
            "raw_secret_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "tws_api_account_query_required": True,
            "order_action_sent": False,
            "cancel_order_sent": False,
            "replace_order_sent": False,
        },
    }
    payload["source_checksum"] = _checksum_payload({**payload, "source_checksum": "sha256:pending"})
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build IB U3028269 Account Console source package from read-only TWS API query artifacts.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--account-summary", type=Path)
    parser.add_argument("--positions", type=Path)
    parser.add_argument("--executions", type=Path)
    parser.add_argument("--open-orders", type=Path)
    parser.add_argument("--readiness-probe", type=Path, default=READINESS_PROBE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--allow-blocked", action="store_true", help="Write a typed blocker package when readiness/query inputs are missing")
    args = parser.parse_args()

    account_summary = args.account_summary or args.input_dir / "account_summary.json"
    positions = args.positions or args.input_dir / "positions.json"
    executions = args.executions or args.input_dir / "executions.json"
    open_orders = args.open_orders or args.input_dir / "open_orders.json"
    payload = build_source_package(
        account_summary_path=account_summary,
        positions_path=positions,
        executions_query_path=executions,
        open_orders_query_path=open_orders,
        readiness_probe_path=args.readiness_probe,
        output_path=args.output,
        allow_blocked=args.allow_blocked,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    status = "blocked" if payload["source_health"]["state"] == "blocked" else "ready"
    print(f"IB_U3028269_SOURCE_PACKAGE_BUILT: status={status} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
