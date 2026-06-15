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


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Account Console CTP 19053 source package from real-login read-only queries.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--account-query", type=Path)
    parser.add_argument("--position-query", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    account_query = args.account_query or args.input_dir / "account_query.json"
    position_query = args.position_query or args.input_dir / "position_query.json"
    payload = build_source_package(account_query, position_query, args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CTP19053_SOURCE_PACKAGE_BUILT: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
