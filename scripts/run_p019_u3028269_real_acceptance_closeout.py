from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
PIPELINE_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
REAL_UI_PARITY = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
COMPLETION_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _run(args: list[str], *, cwd: Path = ROOT, allow_exit_2: bool = False, timeout: float | None = None) -> dict[str, Any]:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    ok = result.returncode == 0 or (allow_exit_2 and result.returncode == 2)
    return {
        "command": " ".join(args),
        "cwd": _source_ref(cwd),
        "returncode": result.returncode,
        "ok": ok,
        "stdout_tail": (result.stdout or "").strip().splitlines()[-4:],
        "stderr_tail": (result.stderr or "").strip().splitlines()[-4:],
    }


def _python(script: str, *args: str, allow_exit_2: bool = False, timeout: float | None = None) -> dict[str, Any]:
    return _run([sys.executable, script, *args], allow_exit_2=allow_exit_2, timeout=timeout)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _refresh_completion_audit(closeout_payload: dict[str, Any], pipeline_summary: dict[str, Any]) -> None:
    audit = _load(COMPLETION_AUDIT)
    if not audit:
        return

    pipeline_ready = pipeline_summary.get("status") == "ready"
    audit["audited_at"] = _now()
    audit["primary_runtime_blocker"] = "adr0005_not_accepted" if pipeline_ready else "tws_api_readiness_missing"
    audit["primary_runtime_blocker_detail"] = (
        "adr0005_proposed_landing_not_started"
        if pipeline_ready
        else "tws_api_socket_disabled_in_latest_config_candidate"
    )
    audit["runtime_truth"] = {
        **audit["runtime_truth"],
        "tws_api_socket_ready": pipeline_ready,
        "account_summary_success": pipeline_summary.get("account_summary_success") is True,
        "positions_success": pipeline_summary.get("positions_success") is True,
        "source_package_state": pipeline_summary.get("source_package_state", "blocked"),
        "pipeline_summary_ref": "output/account_capability/ib-live-u3028269/pipeline-summary.json",
        "status": pipeline_summary.get("status", "blocked"),
    }
    audit["real_acceptance_closeout"] = {
        **audit["real_acceptance_closeout"],
        "status": closeout_payload["status"],
        "blocker_id": closeout_payload["blocker_id"],
        "pipeline_status": closeout_payload["pipeline_status"],
        "real_ui_parity_verdict": closeout_payload["real_ui_parity_verdict"],
        "synthetic_evidence_used_for_real_closeout": False,
        "required_ready_chain": closeout_payload["required_ready_chain"],
    }

    closeout_items = {item["id"]: item for item in audit["required_before_implementation_closeout"]}
    if pipeline_ready:
        closeout_items["C10"]["status"] = "proved"
        closeout_items["C10"].pop("missing_for_completion", None)
    if closeout_payload["status"] == "ready":
        closeout_items["C9"]["status"] = "proved"
        closeout_items["C9"].pop("missing_for_completion", None)
    blockers = [item for item in audit["blocking_conditions"] if item["blocker_id"] != "tws_api_readiness_missing"]
    if not pipeline_ready:
        blockers.append(
            {
                "blocker_id": "tws_api_readiness_missing",
                "owner": "local runtime / TWS operator",
                "blocks": [
                    "real U3028269 funds collection",
                    "real U3028269 positions collection",
                    "positive UI parity",
                ],
            }
        )
    audit["blocking_conditions"] = blockers
    _write(COMPLETION_AUDIT, audit)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run P019 U3028269 real acceptance closeout after TWS API readiness or record typed blocker."
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--wait-timeout-seconds", type=str, default="30")
    parser.add_argument("--wait-interval-seconds", type=str, default="5")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    started_at = _now()
    steps: list[dict[str, Any]] = []

    steps.append(
        _python(
            "scripts/wait_p019_tws_api_ready_and_collect.py",
            "--timeout-seconds",
            args.wait_timeout_seconds,
            "--interval-seconds",
            args.wait_interval_seconds,
            allow_exit_2=True,
            timeout=max(float(args.wait_timeout_seconds) + 30.0, 60.0),
        )
    )
    steps.extend(
        [
            _python("scripts/validate_p019_tws_api_wait_collect.py"),
            _python("scripts/validate_p019_ib_u3028269_tws_api_pipeline.py"),
            _python("scripts/validate_p019_ib_u3028269_tws_api_queries.py"),
            _python("scripts/validate_p019_ib_u3028269_source_package.py"),
            _python("scripts/validate_p019_ib_u3028269_query_source_parity.py"),
            _python("scripts/validate_account_mirror_api.py"),
        ]
    )

    pipeline_summary = _load(PIPELINE_SUMMARY)
    pipeline_status = pipeline_summary.get("status", "blocked")

    playwright_step = _run(
        [
            "cmd",
            "/c",
            "npx",
            "playwright",
            "test",
            "tests/e2e/p019-ib-tws-real-ui-parity.spec.ts",
            "--project=desktop",
        ],
        cwd=FRONTEND,
        timeout=120,
    )
    steps.append(playwright_step)
    steps.append(_python("scripts/validate_p019_u3028269_real_ui_parity.py"))

    real_ui_parity = _load(REAL_UI_PARITY)
    status = "ready" if pipeline_status == "ready" and real_ui_parity.get("verdict") == "pass" else "blocked"
    blocker_id = None if status == "ready" else "tws_api_readiness_missing"

    payload = {
        "schema": "account-console.p019-u3028269-real-acceptance-closeout.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "started_at": started_at,
        "completed_at": _now(),
        "status": status,
        "blocker_id": blocker_id,
        "pipeline_summary_ref": _source_ref(PIPELINE_SUMMARY),
        "real_ui_parity_ref": _source_ref(REAL_UI_PARITY),
        "pipeline_status": pipeline_status,
        "real_ui_parity_verdict": real_ui_parity.get("verdict"),
        "account_summary_success": pipeline_summary.get("account_summary_success"),
        "positions_success": pipeline_summary.get("positions_success"),
        "source_package_state": pipeline_summary.get("source_package_state"),
        "required_ready_chain": [
            "ready_for_tws_api_funds_positions_query=true",
            "account_summary_success=true",
            "positions_success=true",
            "source_package_state=ready",
            "query_source_parity=pass",
            "real_ui_parity_verdict=pass",
            "command_enabled=false",
            "order_action=false",
        ],
        "steps": steps,
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
            "synthetic_evidence_used_for_real_closeout": False,
        },
    }
    _write(output, payload)

    foundation_step = _python("scripts/validate_p019_broker_observation_foundation.py")
    _refresh_completion_audit(payload, pipeline_summary)
    completion_step = _python("scripts/validate_p019_completion_audit.py")
    steps.extend([foundation_step, completion_step])
    payload["steps"] = steps
    payload["completed_at"] = _now()
    _write(output, payload)
    print(json.dumps({"status": status, "blocker_id": blocker_id, "summary": str(output)}, ensure_ascii=False))
    return 0 if all(step["ok"] for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
