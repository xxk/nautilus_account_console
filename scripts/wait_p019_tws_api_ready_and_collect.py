from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "wait-collect-summary.json"
PIPELINE_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
READINESS = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _run(args: list[str], *, allow_exit_2: bool = False, timeout: float | None = None) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
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


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Wait for local TWS API readiness, then run the P019 U3028269 read-only collection pipeline."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--interval-seconds", type=float, default=5.0)
    parser.add_argument("--pipeline-summary", type=Path, default=PIPELINE_SUMMARY)
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    pipeline_summary = args.pipeline_summary if args.pipeline_summary.is_absolute() else ROOT / args.pipeline_summary
    started_at = _now()
    deadline = time.monotonic() + max(args.timeout_seconds, 0.0)
    attempts: list[dict[str, Any]] = []
    ready = False

    while True:
        probe_step = _run(["scripts/probe_p019_tws_api_readiness.py"], allow_exit_2=True)
        validation_step = _run(["scripts/validate_p019_tws_api_readiness_probe.py"])
        readiness = _load(READINESS)
        attempt = {
            "attempt_index": len(attempts) + 1,
            "observed_at": _now(),
            "readiness_ref": _source_ref(READINESS),
            "ready_for_tws_api_funds_positions_query": readiness.get("ready_for_tws_api_funds_positions_query"),
            "blocker_id": None
            if readiness.get("typed_blocker") is None
            else readiness.get("typed_blocker", {}).get("blocker_id"),
            "blocker_reasons": []
            if readiness.get("typed_blocker") is None
            else readiness.get("typed_blocker", {}).get("reasons", []),
            "steps": [probe_step, validation_step],
        }
        attempts.append(attempt)
        if readiness.get("ready_for_tws_api_funds_positions_query") is True:
            ready = True
            break
        if time.monotonic() >= deadline:
            break
        time.sleep(max(args.interval_seconds, 0.1))

    pipeline_step = None
    if ready:
        pipeline_step = _run(
            ["scripts/run_p019_ib_u3028269_tws_api_pipeline.py", "--summary", str(pipeline_summary)],
            timeout=120,
        )
    summary = _load(pipeline_summary)
    status = "ready" if summary.get("status") == "ready" else "blocked"
    blocker_id = None if status == "ready" else "tws_api_readiness_missing"
    payload = {
        "schema": "account-console.p019-tws-api-wait-collect-summary.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "started_at": started_at,
        "completed_at": _now(),
        "status": status,
        "blocker_id": blocker_id,
        "attempt_count": len(attempts),
        "attempts": attempts,
        "pipeline_ran": pipeline_step is not None,
        "pipeline_step": pipeline_step,
        "pipeline_summary_ref": _source_ref(pipeline_summary),
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "tws_api_account_query_sent_before_readiness": False,
            "funds_positions_values_recorded_before_readiness": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
        "retry_condition": None
        if status == "ready"
        else "enable the logged-in TWS API socket, then rerun this wait-and-collect entrypoint.",
    }
    _write(output, payload)
    print(json.dumps({"status": status, "blocker_id": blocker_id, "summary": str(output)}, ensure_ascii=False))
    return 0 if status == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
