from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "current-state-closeout-refresh.json"


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
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    ok = result.returncode == 0 or (allow_exit_2 and result.returncode == 2)
    return {
        "command": "python " + " ".join(args),
        "returncode": result.returncode,
        "ok": ok,
        "stdout_tail": (result.stdout or "").strip().splitlines()[-4:],
        "stderr_tail": (result.stderr or "").strip().splitlines()[-4:],
    }


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _status_from_step(step: dict[str, Any]) -> str | None:
    for line in reversed(step.get("stdout_tail", [])):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        value = payload.get("status")
        if isinstance(value, str):
            return value
    return None


def _step_is_expected(step: dict[str, Any], closeout_status: str) -> bool:
    if step["ok"]:
        return True
    if closeout_status == "blocked" and (
        "scripts/run_p019_u3028269_real_acceptance_closeout.py" in step["command"]
        or "scripts/validate_p019_completion_audit.py" in step["command"]
        or "scripts/validate_p019_broker_observation_foundation.py" in step["command"]
    ):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh the P019 U3028269 current-state diagnostic, remediation and real closeout evidence chain."
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--wait-timeout-seconds", type=str, default="1")
    parser.add_argument("--wait-interval-seconds", type=str, default="1")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    started_at = _now()
    steps: list[dict[str, Any]] = []

    steps.extend(
        [
            _run(["scripts/diagnose_p019_tws_api_socket.py"], allow_exit_2=True, timeout=30),
            _run(["scripts/validate_p019_tws_api_socket_diagnostic.py"], timeout=30),
            _run(["scripts/diagnose_p019_windows_firewall_tws_api.py"], timeout=30),
            _run(["scripts/validate_p019_windows_firewall_tws_api_diagnostic.py"], timeout=30),
            _run(["scripts/diagnose_p019_tws_api_config.py"], allow_exit_2=True, timeout=30),
            _run(["scripts/validate_p019_tws_api_config_diagnostic.py"], timeout=30),
            _run(["scripts/decide_p019_tws_reinstall_gate.py"], timeout=30),
            _run(["scripts/validate_p019_tws_reinstall_decision_gate.py"], timeout=30),
            _run(["scripts/prepare_p019_tws_api_enable_change_request.py"], timeout=30),
            _run(["scripts/validate_p019_tws_api_enable_change_request.py"], timeout=30),
            _run(
                [
                    "scripts/run_p019_u3028269_real_acceptance_closeout.py",
                    "--wait-timeout-seconds",
                    args.wait_timeout_seconds,
                    "--wait-interval-seconds",
                    args.wait_interval_seconds,
                ],
                timeout=max(float(args.wait_timeout_seconds) + 150.0, 180.0),
            ),
            _run(["scripts/validate_p019_u3028269_real_acceptance_closeout.py"], timeout=30),
            _run(["scripts/validate_p019_runtime_evidence_freshness.py"], timeout=30),
            _run(["scripts/validate_p019_completion_audit.py"], timeout=30),
            _run(["scripts/validate_p019_broker_observation_foundation.py"], timeout=30),
        ]
    )

    closeout_status = _status_from_step(steps[10]) or "unknown"
    expected_ok = all(_step_is_expected(step, closeout_status) for step in steps)
    payload = {
        "schema": "account-console.p019-u3028269-current-state-closeout-refresh.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "started_at": started_at,
        "completed_at": _now(),
        "status": closeout_status,
        "blocker_id": None if closeout_status == "ready" else "tws_api_readiness_missing",
        "real_acceptance_closeout_ref": "output/account_capability/ib-live-u3028269/real-acceptance-closeout.json",
        "runtime_evidence_freshness_ref": "scripts/validate_p019_runtime_evidence_freshness.py",
        "steps": steps,
        "expected_ok": expected_ok,
        "boundaries": {
            "writes_outside_worktree": False,
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "raw_config_file_contents_recorded": False,
            "tws_reinstall_performed": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
    }
    _write(output, payload)
    print(json.dumps({"status": closeout_status, "summary": _source_ref(output)}, ensure_ascii=False))
    return 0 if expected_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
