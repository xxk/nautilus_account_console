from __future__ import annotations

import argparse
import importlib.util
import json
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"
DEFAULT_IBAPI_RUNTIME = ROOT / "output" / "runtime" / "python"


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def add_runtime_path(path: Path) -> str | None:
    if path.exists():
        sys.path.insert(0, str(path))
        return _source_ref(path)
    return None


def tcp_open(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def build_probe(timeout: float, ibapi_runtime: Path) -> dict[str, Any]:
    # Keep raw endpoint values out of evidence; these are well-known local TWS/Gateway port slots.
    candidate_ports = {
        "tws_live_default": 7496,
        "tws_paper_default": 7497,
        "gateway_live_default": 4001,
        "gateway_paper_default": 4002,
    }
    port_results = {
        port_ref: {"checked": True, "open": tcp_open("127.0.0.1", port, timeout)}
        for port_ref, port in candidate_ports.items()
    }
    runtime_ref = add_runtime_path(ibapi_runtime)
    ibapi_available = importlib.util.find_spec("ibapi") is not None
    any_port_open = any(item["open"] for item in port_results.values())
    ready = ibapi_available and any_port_open

    blocker_reasons: list[str] = []
    if not ibapi_available:
        blocker_reasons.append("python_ibapi_module_missing")
    if not any_port_open:
        blocker_reasons.append("local_tws_api_socket_not_open")
    retry_parts: list[str] = []
    if not ibapi_available:
        retry_parts.append("install or activate the worktree-approved IB API runtime")
    if not any_port_open:
        retry_parts.append("enable the already logged-in TWS/Gateway API socket")
    retry_condition = " and ".join(retry_parts) + ", then rerun this readiness probe before any funds/positions query."

    return {
        "schema": "account-console.p019-tws-api-readiness-probe.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "observed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "probe_kind": "local_tws_api_readiness",
        "evidence_kind": "api_readiness_probe",
        "ibapi_available": ibapi_available,
        "ibapi_runtime_ref": runtime_ref,
        "host_ref": "localhost_tws_api",
        "candidate_port_refs": port_results,
        "ready_for_tws_api_funds_positions_query": ready,
        "typed_blocker": None
        if ready
        else {
            "blocker_id": "tws_api_readiness_missing",
            "blocker_kind": "local_api_readiness_blocker",
            "reasons": blocker_reasons,
            "retry_condition": retry_condition,
        },
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "tws_api_account_query_sent": False,
            "funds_positions_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
        "explicit_non_claims": [
            "does_not_prove_account_truth",
            "does_not_prove_funds_truth",
            "does_not_prove_positions_truth",
            "does_not_accept_adr0005",
            "does_not_authorize_order_action",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe local TWS API readiness for P019 without querying account values.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Evidence JSON output path")
    parser.add_argument("--timeout", type=float, default=0.75, help="TCP connect timeout per local port slot")
    parser.add_argument("--ibapi-runtime", type=Path, default=DEFAULT_IBAPI_RUNTIME, help="Worktree-local IB API runtime path")
    args = parser.parse_args()

    payload = build_probe(timeout=args.timeout, ibapi_runtime=args.ibapi_runtime)
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked", "output": str(output)}, ensure_ascii=False))
    return 0 if payload["ready_for_tws_api_funds_positions_query"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
