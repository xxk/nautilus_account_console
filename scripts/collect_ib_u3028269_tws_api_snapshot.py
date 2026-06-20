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
            "explicit_non_claims": [
                "does_not_prove_account_truth",
                "does_not_prove_funds_truth",
                "does_not_prove_positions_truth",
                "does_not_authorize_order_action",
            ],
        }
    )
    if kind == "account_summary":
        payload.pop("positions")
    else:
        payload.pop("balances")
    payload["query_checksum"] = _source_checksum({**payload, "query_checksum": "sha256:pending"})
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_blocked(output_dir: Path, reason: str, readiness_probe: Path) -> None:
    readiness_ref = _source_ref(readiness_probe)
    _write_json(output_dir / "account_summary.json", _blocked_query("account_summary", reason, readiness_ref))
    _write_json(output_dir / "positions.json", _blocked_query("positions", reason, readiness_ref))


def _collect_with_ibapi(*, host: str, port: int, client_id: int, timeout: float) -> tuple[dict[str, Any], dict[str, Any]]:
    from ibapi.client import EClient
    from ibapi.contract import Contract
    from ibapi.wrapper import EWrapper

    class ReadOnlyApp(EWrapper, EClient):
        def __init__(self) -> None:
            EClient.__init__(self, self)
            self.events: queue.Queue[str] = queue.Queue()
            self.summary: dict[tuple[str, str], str] = {}
            self.positions: list[dict[str, Any]] = []
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
    app.reqAccountSummary(9001, "All", "NetLiquidation,AvailableFunds,MaintMarginReq,UnrealizedPnL")
    app.reqPositions()

    deadline = time.monotonic() + timeout
    seen: set[str] = set()
    while time.monotonic() < deadline and {"accountSummaryEnd", "positionEnd"} - seen:
        try:
            seen.add(app.events.get(timeout=0.25))
        except queue.Empty:
            pass
    app.cancelAccountSummary(9001)
    app.cancelPositions()
    app.disconnect()
    completed = _now()
    if {"accountSummaryEnd", "positionEnd"} - seen:
        raise CollectError("ibapi_readonly_query_timeout")

    balances = []
    currencies = {currency for _tag, currency in app.summary}
    for currency in sorted(currencies):
        balances.append(
            {
                "currency": currency,
                "net_liquidation": float(app.summary.get(("NetLiquidation", currency), 0.0)),
                "available_funds": float(app.summary.get(("AvailableFunds", currency), 0.0)),
                "margin_used": float(app.summary.get(("MaintMarginReq", currency), 0.0)),
                "unrealized_pnl": float(app.summary.get(("UnrealizedPnL", currency), 0.0)),
            }
        )
    account_summary = _base_query("account_summary", success=True, started_at=started, completed_at=completed)
    account_summary["balances"] = balances
    account_summary["query_checksum"] = _source_checksum({**account_summary, "query_checksum": "sha256:pending"})

    positions = _base_query("positions", success=True, started_at=started, completed_at=completed)
    positions["positions"] = app.positions
    positions["query_checksum"] = _source_checksum({**positions, "query_checksum": "sha256:pending"})
    return account_summary, positions


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only IB U3028269 account summary and positions through TWS API.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--readiness-probe", type=Path, default=READINESS_PROBE)
    parser.add_argument("--port-ref", choices=sorted(PORT_REFS))
    parser.add_argument("--client-id", type=int, default=9909)
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

    account_summary, positions = _collect_with_ibapi(host="127.0.0.1", port=port, client_id=args.client_id, timeout=args.timeout)
    _write_json(args.output_dir / "account_summary.json", account_summary)
    _write_json(args.output_dir / "positions.json", positions)
    print(json.dumps({"status": "ready", "port_ref": port_ref, "output_dir": str(args.output_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
