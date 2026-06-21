from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "wait-collect-summary.json"
RUNNER = ROOT / "scripts" / "wait_p019_tws_api_ready_and_collect.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class WaitCollectError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WaitCollectError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(SUMMARY)
    runner = read(RUNNER)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-tws-api-wait-collect-summary.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["status"] in {"ready", "blocked"}, "status mismatch")
    require(payload["attempt_count"] >= 1, "wait collect must record at least one readiness attempt")
    require(payload["attempt_count"] == len(payload["attempts"]), "attempt count mismatch")
    require(payload["pipeline_summary_ref"].endswith("pipeline-summary.json"), "pipeline summary ref mismatch")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["tws_api_account_query_sent_before_readiness"] is False, "must not query account before readiness")
    require(
        boundaries["funds_positions_values_recorded_before_readiness"] is False,
        "must not record funds/positions before readiness",
    )
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(boundaries["order_action_sent"] is False, "order action must not be sent")

    for attempt in payload["attempts"]:
        require(attempt["readiness_ref"] == "output/debug/p019-tws-api-readiness/tws-api-readiness-probe.json", "readiness ref mismatch")
        commands = {step["command"] for step in attempt["steps"]}
        require("python scripts/probe_p019_tws_api_readiness.py" in commands, "attempt missing readiness probe")
        require("python scripts/validate_p019_tws_api_readiness_probe.py" in commands, "attempt missing readiness validator")
        for step in attempt["steps"]:
            require(step["ok"] is True, f"attempt step failed: {step['command']}")

    if payload["status"] == "blocked":
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked wait collect blocker mismatch")
        require(payload["pipeline_ran"] is False, "blocked wait collect must not run account query pipeline before readiness")
        require(payload["pipeline_step"] is None, "blocked wait collect must not have pipeline step")
        require(payload["retry_condition"], "blocked wait collect must carry retry condition")
        require(
            all(attempt["ready_for_tws_api_funds_positions_query"] is False for attempt in payload["attempts"]),
            "blocked wait collect cannot include ready attempt",
        )
    else:
        require(payload["blocker_id"] is None, "ready wait collect must not carry blocker")
        require(payload["pipeline_ran"] is True, "ready wait collect must run account query pipeline")
        require(payload["pipeline_step"]["ok"] is True, "ready wait collect pipeline step must pass")

    for term in [
        "probe_p019_tws_api_readiness.py",
        "run_p019_ib_u3028269_tws_api_pipeline.py",
    ]:
        require(term in runner, f"runner missing term {term}")
    for term in [
        "wait_p019_tws_api_ready_and_collect.py",
        "validate_p019_tws_api_wait_collect.py",
        "P019_TWS_API_WAIT_COLLECT_OK",
    ]:
        require(term in acceptance, f"acceptance missing wait collect term {term}")
        require(term in phase_plan, f"phase plan missing wait collect term {term}")

    print(
        "P019_TWS_API_WAIT_COLLECT_OK: "
        f"status={payload['status']} attempts={payload['attempt_count']} pipeline_ran={str(payload['pipeline_ran']).lower()}"
    )


if __name__ == "__main__":
    main()
