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
    require(payload["wait_collect_summary_ref"].endswith("wait-collect-summary.json"), "wait collect summary ref mismatch")
    require(payload["wait_collect_status"] in {"ready", "blocked"}, "wait collect status mismatch")
    require(payload.get("expected_ok") is True, "closeout did not classify expected blocked/ready outcomes")
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

    execution_closeout = payload["execution_report_closeout"]
    require(execution_closeout["executions_query_ref"].endswith("tws-api/executions.json"), "executions query ref mismatch")
    require(execution_closeout["executions_query_success"] is True, "executions query must be successful")
    require(execution_closeout["executions_readonly_api_call"] == "reqExecutions", "executions query must use reqExecutions")
    require(execution_closeout["executions_filter_type"] == "ExecutionFilter", "executions query must use ExecutionFilter")
    require(execution_closeout["executions_complete_history_claimed"] is False, "executions query cannot claim complete history")
    require(execution_closeout["executions_order_action_sent"] is False, "executions query must not send order actions")
    require(execution_closeout["synthetic_evidence_used"] is False, "synthetic evidence cannot close execution report parity")
    require(execution_closeout["execution_report_rows"] >= 0, "execution report rows invalid")
    require(execution_closeout["fill_count"] >= 0, "fill count invalid")
    require(
        execution_closeout["ui_execution_report_rows"] == execution_closeout["execution_report_rows"],
        "UI execution row count must match source closeout",
    )
    require(
        execution_closeout["ui_fill_count"] == execution_closeout["fill_count"],
        "UI fill count must match source closeout",
    )
    if execution_closeout["execution_report_rows"] == 0:
        require(execution_closeout["fill_count"] == 0, "empty executions cannot map fills")
        require(execution_closeout["execution_report_state"] == "not_available_or_empty", "empty execution state mismatch")
        require(execution_closeout["ui_execution_report_state"] == "not_available_or_empty", "empty UI execution state mismatch")
        require(
            execution_closeout["orders_fills_parity"] in {"pass", "blocked"},
            "open-order parity may pass while fill rows remain absent",
        )
        require(
            execution_closeout["execution_reports_table_parity"] in {"pass", "blocked"},
            "open-order table parity may pass while fill rows remain absent",
        )
        require(
            execution_closeout["execution_reports_persistence_parity"] == "blocked",
            "execution report persistence parity must remain blocked with no rows",
        )
        require(execution_closeout["report_parity_status"] == "blocked", "empty executions cannot prove report parity")
        require(execution_closeout["blocker_id"] == "real_report_rows_absent", "empty executions blocker mismatch")
    else:
        require(execution_closeout["fill_count"] == execution_closeout["execution_report_rows"], "fill/report row mismatch")
        require(execution_closeout["report_parity_status"] == "proved", "non-empty executions must prove report parity")
        require(execution_closeout["blocker_id"] is None, "proved report parity must not carry blocker")

    commands = {step["command"] for step in payload["steps"]}
    for expected in [
        "scripts/wait_p019_tws_api_ready_and_collect.py",
        "scripts/validate_p019_tws_api_wait_collect.py",
        "scripts/validate_p019_ib_u3028269_tws_api_pipeline.py",
        "scripts/validate_p019_ib_u3028269_tws_api_queries.py",
        "scripts/validate_p019_ib_u3028269_source_package.py",
        "scripts/validate_p019_ib_u3028269_query_source_parity.py",
        "scripts/build_p019_u3028269_real_durable_store_reload.py",
        "scripts/validate_p019_u3028269_real_durable_store_reload.py",
        "scripts/validate_account_mirror_api.py",
        "playwright test tests/e2e/p019-ib-tws-real-ui-parity.spec.ts",
        "scripts/validate_p019_u3028269_real_ui_parity.py",
        "scripts/validate_p019_broker_observation_foundation.py",
        "scripts/validate_p019_completion_audit.py",
    ]:
        require(any(expected in command for command in commands), f"closeout missing command {expected}")
    for step in payload["steps"]:
        if payload["status"] == "blocked" and (
            "scripts/validate_p019_completion_audit.py" in step["command"]
            or "scripts/validate_p019_broker_observation_foundation.py" in step["command"]
        ):
            require(step["ok"] is False, "blocked closeout should not pass completion audit")
            continue
        require(step["ok"] is True, f"closeout step failed: {step['command']}")

    for item in [
        "ready_for_tws_api_funds_positions_query=true",
        "account_summary_success=true",
        "positions_success=true",
        "source_package_state=ready",
        "query_source_parity=pass",
        "real_ui_parity_verdict=pass",
        "executions_query_success=true",
        "execution_report_parity=blocked_when_no_real_rows",
        "command_enabled=false",
        "order_action=false",
    ]:
        require(item in payload["required_ready_chain"], f"missing ready chain item {item}")

    if payload["status"] == "blocked":
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked closeout blocker mismatch")
        require(payload["wait_collect_status"] == "blocked", "blocked closeout must be driven by blocked wait collect")
        require(payload["pipeline_status"] in {"ready", "blocked"}, "blocked closeout pipeline status mismatch")
        require(payload["real_ui_parity_verdict"] in {"pass", "blocked"}, "blocked closeout UI parity mismatch")
    else:
        require(payload["blocker_id"] is None, "ready closeout must not carry blocker")
        require(payload["wait_collect_status"] == "ready", "ready closeout needs ready wait collect")
        require(payload["pipeline_status"] == "ready", "ready closeout needs ready pipeline")
        require(payload["real_ui_parity_verdict"] == "pass", "ready closeout needs passing real UI parity")
        require(payload["account_summary_success"] is True, "ready closeout needs account summary success")
        require(payload["positions_success"] is True, "ready closeout needs positions success")
        require(payload["source_package_state"] == "ready", "ready closeout needs ready source package")
        require(
            payload["execution_report_closeout"]["report_parity_status"] in {"blocked", "proved"},
            "ready closeout must carry report parity status",
        )

    for term in [
        "wait_p019_tws_api_ready_and_collect.py",
        "validate_p019_ib_u3028269_query_source_parity.py",
        "build_p019_u3028269_real_durable_store_reload.py",
        "validate_p019_u3028269_real_durable_store_reload.py",
        "p019-ib-tws-real-ui-parity.spec.ts",
        "validate_p019_completion_audit.py",
        "execution_report_closeout",
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
