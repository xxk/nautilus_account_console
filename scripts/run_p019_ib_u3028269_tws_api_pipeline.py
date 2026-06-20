from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
READINESS = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"
SOCKET_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-socket-diagnostic.json"
FIREWALL_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "windows-firewall-tws-api-diagnostic.json"
CONFIG_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
ACCOUNT_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "account_summary.json"
POSITIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "positions.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _run(args: list[str], *, allow_exit_2: bool = False) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    ok = result.returncode == 0 or (allow_exit_2 and result.returncode == 2)
    return {
        "command": "python " + " ".join(args),
        "returncode": result.returncode,
        "ok": ok,
        "stdout_tail": result.stdout.strip().splitlines()[-3:],
        "stderr_tail": result.stderr.strip().splitlines()[-3:],
    }


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the P019 IB U3028269 TWS API readiness/query/source-package pipeline.")
    parser.add_argument("--summary", type=Path, default=SUMMARY)
    args = parser.parse_args()

    started_at = _now()
    steps = [
        _run(["scripts/diagnose_p019_tws_api_socket.py"], allow_exit_2=True),
        _run(["scripts/validate_p019_tws_api_socket_diagnostic.py"]),
        _run(["scripts/diagnose_p019_windows_firewall_tws_api.py"]),
        _run(["scripts/validate_p019_windows_firewall_tws_api_diagnostic.py"]),
        _run(["scripts/diagnose_p019_tws_api_config.py"], allow_exit_2=True),
        _run(["scripts/validate_p019_tws_api_config_diagnostic.py"]),
        _run(["scripts/probe_p019_tws_api_readiness.py"], allow_exit_2=True),
        _run(["scripts/validate_p019_tws_api_readiness_probe.py"]),
        _run(["scripts/collect_ib_u3028269_tws_api_snapshot.py", "--allow-blocked"]),
        _run(["scripts/validate_p019_ib_u3028269_tws_api_queries.py"]),
        _run(["scripts/build_ib_u3028269_source_package_from_tws_api.py", "--allow-blocked"]),
        _run(["scripts/validate_p019_ib_u3028269_source_package.py"]),
        _run(["scripts/validate_account_mirror_api.py"]),
    ]
    readiness = _load(READINESS)
    socket_diagnostic = _load(SOCKET_DIAGNOSTIC)
    firewall_diagnostic = _load(FIREWALL_DIAGNOSTIC)
    config_diagnostic = _load(CONFIG_DIAGNOSTIC)
    account_summary = _load(ACCOUNT_SUMMARY)
    positions = _load(POSITIONS)
    source_package = _load(SOURCE_PACKAGE)
    status = "ready" if source_package.get("source_health", {}).get("state") == "ready" else "blocked"
    summary = {
        "schema": "account-console.p019-ib-u3028269-tws-api-pipeline-summary.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "started_at": started_at,
        "completed_at": _now(),
        "status": status,
        "blocker_id": None if status == "ready" else source_package.get("source_health", {}).get("blocker_id"),
        "socket_diagnostic_ref": _source_ref(SOCKET_DIAGNOSTIC),
        "firewall_diagnostic_ref": _source_ref(FIREWALL_DIAGNOSTIC),
        "config_diagnostic_ref": _source_ref(CONFIG_DIAGNOSTIC),
        "readiness_ref": _source_ref(READINESS),
        "account_summary_ref": _source_ref(ACCOUNT_SUMMARY),
        "positions_ref": _source_ref(POSITIONS),
        "source_package_ref": _source_ref(SOURCE_PACKAGE),
        "ibapi_available": readiness.get("ibapi_available"),
        "ibapi_runtime_ref": readiness.get("ibapi_runtime_ref"),
        "socket_primary_blocker": socket_diagnostic.get("typed_blocker", {}).get("reasons", [None])[0]
        if socket_diagnostic.get("typed_blocker")
        else None,
        "firewall_primary_blocker": firewall_diagnostic.get("diagnosis", {}).get("primary_blocker"),
        "config_primary_blocker": config_diagnostic.get("typed_blocker", {}).get("primary_blocker")
        if config_diagnostic.get("typed_blocker")
        else None,
        "ready_for_tws_api_funds_positions_query": readiness.get("ready_for_tws_api_funds_positions_query"),
        "account_summary_success": account_summary.get("success"),
        "positions_success": positions.get("success"),
        "source_package_state": source_package.get("source_health", {}).get("state"),
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
        "steps": steps,
    }
    output = args.summary
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "blocker_id": summary["blocker_id"], "summary": str(output)}, ensure_ascii=False))
    return 0 if all(step["ok"] for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
