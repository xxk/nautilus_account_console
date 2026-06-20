from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
RUNNER = ROOT / "scripts" / "run_p019_u3028269_real_acceptance_closeout.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class RealAcceptanceCloseoutError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RealAcceptanceCloseoutError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(SUMMARY)
    runner = read(RUNNER)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-u3028269-real-acceptance-closeout.v1", "schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["status"] in {"ready", "blocked"}, "status mismatch")
    require(payload["pipeline_summary_ref"].endswith("pipeline-summary.json"), "pipeline summary ref mismatch")
    require(
        payload["real_ui_parity_ref"].endswith("2026-06-20-p019-u3028269-real-ui-parity-evidence.json"),
        "real UI parity ref mismatch",
    )

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(boundaries["order_action_sent"] is False, "order action must not be sent")
    require(boundaries["synthetic_evidence_used_for_real_closeout"] is False, "synthetic evidence cannot close real acceptance")

    commands = {step["command"] for step in payload["steps"]}
    for expected in [
        "scripts/wait_p019_tws_api_ready_and_collect.py",
        "scripts/validate_p019_tws_api_wait_collect.py",
        "scripts/validate_p019_ib_u3028269_tws_api_pipeline.py",
        "scripts/validate_p019_ib_u3028269_tws_api_queries.py",
        "scripts/validate_p019_ib_u3028269_source_package.py",
        "scripts/validate_p019_ib_u3028269_query_source_parity.py",
        "scripts/validate_account_mirror_api.py",
        "playwright test tests/e2e/p019-ib-tws-real-ui-parity.spec.ts",
        "scripts/validate_p019_u3028269_real_ui_parity.py",
        "scripts/validate_p019_broker_observation_foundation.py",
        "scripts/validate_p019_completion_audit.py",
    ]:
        require(any(expected in command for command in commands), f"closeout missing command {expected}")
    for step in payload["steps"]:
        require(step["ok"] is True, f"closeout step failed: {step['command']}")

    for item in [
        "ready_for_tws_api_funds_positions_query=true",
        "account_summary_success=true",
        "positions_success=true",
        "source_package_state=ready",
        "query_source_parity=pass",
        "real_ui_parity_verdict=pass",
        "command_enabled=false",
        "order_action=false",
    ]:
        require(item in payload["required_ready_chain"], f"missing ready chain item {item}")

    if payload["status"] == "blocked":
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked closeout blocker mismatch")
        require(payload["pipeline_status"] == "blocked", "blocked closeout must preserve blocked pipeline")
        require(payload["real_ui_parity_verdict"] == "blocked", "blocked closeout must preserve blocked UI parity")
        require(payload["account_summary_success"] is False, "blocked closeout cannot claim account summary success")
        require(payload["positions_success"] is False, "blocked closeout cannot claim positions success")
    else:
        require(payload["blocker_id"] is None, "ready closeout must not carry blocker")
        require(payload["pipeline_status"] == "ready", "ready closeout needs ready pipeline")
        require(payload["real_ui_parity_verdict"] == "pass", "ready closeout needs passing real UI parity")
        require(payload["account_summary_success"] is True, "ready closeout needs account summary success")
        require(payload["positions_success"] is True, "ready closeout needs positions success")
        require(payload["source_package_state"] == "ready", "ready closeout needs ready source package")

    for term in [
        "wait_p019_tws_api_ready_and_collect.py",
        "validate_p019_ib_u3028269_query_source_parity.py",
        "p019-ib-tws-real-ui-parity.spec.ts",
        "validate_p019_completion_audit.py",
        "synthetic_evidence_used_for_real_closeout",
    ]:
        require(term in runner, f"runner missing {term}")
    for term in [
        "run_p019_u3028269_real_acceptance_closeout.py",
        "validate_p019_u3028269_real_acceptance_closeout.py",
        "P019_U3028269_REAL_ACCEPTANCE_CLOSEOUT_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print(f"P019_U3028269_REAL_ACCEPTANCE_CLOSEOUT_OK: status={payload['status']}")


if __name__ == "__main__":
    main()
