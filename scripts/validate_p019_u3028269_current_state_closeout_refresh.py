from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "current-state-closeout-refresh.json"
REAL_CLOSEOUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
COMPLETION_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class CurrentStateCloseoutRefreshError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CurrentStateCloseoutRefreshError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str, label: str) -> datetime:
    require(value.endswith("Z"), f"{label} must be UTC Z timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def require_terms(path: Path, terms: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def step_by_command(summary: dict[str, Any], command_term: str) -> dict[str, Any]:
    matches = [step for step in summary["steps"] if command_term in step["command"]]
    require(len(matches) == 1, f"expected exactly one step for {command_term}, got {len(matches)}")
    return matches[0]


def main() -> None:
    summary = load(SUMMARY)
    real_closeout = load(REAL_CLOSEOUT)
    completion_audit = load(COMPLETION_AUDIT)
    executions = load(EXECUTIONS)
    require(
        summary["schema"] == "account-console.p019-u3028269-current-state-closeout-refresh.v1",
        "refresh summary schema drifted",
    )
    require(summary["proposal_id"] == "p019-broker-observation-session-foundation", "proposal id drifted")
    require(summary["account_id"] == "acct.ib.live.u3028269", "account id drifted")
    require(summary["status"] in {"blocked", "ready"}, "refresh status drifted")
    if summary["status"] == "blocked":
        require(summary["blocker_id"] == "tws_api_readiness_missing", "blocked refresh blocker drifted")
    else:
        require(summary["blocker_id"] is None, "ready refresh must not carry blocker")
    require(summary["real_acceptance_closeout_ref"].endswith("real-acceptance-closeout.json"), "closeout ref drifted")
    require(summary.get("expected_ok") is True, "refresh did not classify expected blocked/ready outcomes")

    started_at = parse_time(summary["started_at"], "refresh started_at")
    completed_at = parse_time(summary["completed_at"], "refresh completed_at")
    require(completed_at >= started_at, "refresh completed before start")

    expected_order = [
        "diagnose_p019_tws_api_socket.py",
        "validate_p019_tws_api_socket_diagnostic.py",
        "diagnose_p019_windows_firewall_tws_api.py",
        "validate_p019_windows_firewall_tws_api_diagnostic.py",
        "diagnose_p019_tws_api_config.py",
        "validate_p019_tws_api_config_diagnostic.py",
        "decide_p019_tws_reinstall_gate.py",
        "validate_p019_tws_reinstall_decision_gate.py",
        "prepare_p019_tws_api_enable_change_request.py",
        "validate_p019_tws_api_enable_change_request.py",
        "run_p019_u3028269_real_acceptance_closeout.py",
        "validate_p019_u3028269_real_acceptance_closeout.py",
        "validate_p019_runtime_evidence_freshness.py",
        "validate_p019_completion_audit.py",
        "validate_p019_broker_observation_foundation.py",
    ]
    commands = [step["command"] for step in summary["steps"]]
    require(len(commands) == len(expected_order), "refresh step count drifted")
    for index, expected in enumerate(expected_order):
        require(expected in commands[index], f"refresh step {index + 1} should run {expected}")
        if summary["steps"][index]["ok"] is False:
            require(
                summary["status"] == "blocked"
                and expected
                in {
                    "run_p019_u3028269_real_acceptance_closeout.py",
                    "validate_p019_completion_audit.py",
                    "validate_p019_broker_observation_foundation.py",
                },
                f"refresh step failed unexpectedly: {expected}",
            )

    socket_step = step_by_command(summary, "diagnose_p019_tws_api_socket.py")
    config_step = step_by_command(summary, "diagnose_p019_tws_api_config.py")
    closeout_step = step_by_command(summary, "run_p019_u3028269_real_acceptance_closeout.py")
    freshness_step = step_by_command(summary, "validate_p019_runtime_evidence_freshness.py")
    require(socket_step["returncode"] in {0, 2}, "socket diagnostic return code drifted")
    require(config_step["returncode"] in {0, 2}, "config diagnostic return code drifted")
    if summary["status"] == "blocked":
        require(closeout_step["returncode"] in {0, 1, 2}, "blocked real closeout runner return code drifted")
        require(real_closeout["status"] == "blocked", "blocked refresh must point at blocked real closeout")
        require(real_closeout["blocker_id"] == "tws_api_readiness_missing", "blocked real closeout blocker mismatch")
    else:
        require(closeout_step["returncode"] == 0, "real closeout runner failed")
        require(real_closeout["status"] == "ready", "ready refresh must point at ready real closeout")
    closeout_commands = [step["command"] for step in real_closeout["steps"]]
    for term in [
        "scripts/build_p019_u3028269_real_durable_store_reload.py",
        "scripts/validate_p019_u3028269_real_durable_store_reload.py",
    ]:
        require(any(term in command for command in closeout_commands), f"real closeout did not refresh durable reload: {term}")
    durable_summary = completion_audit["real_durable_store_reload"]
    require(
        durable_summary["artifact_ref"] == "output/account_capability/ib-live-u3028269/durable-store-reload.json",
        "completion audit durable artifact ref mismatch",
    )
    require(
        durable_summary["source_report_batch_checksum"] == executions["query_checksum"],
        "current-state refresh left durable summary on a stale executions checksum",
    )
    require(durable_summary["records_loaded_from_live_memory"] == 0, "durable reload used live memory")
    require(durable_summary["synthetic_evidence_used"] is False, "durable reload used synthetic evidence")
    require(durable_summary["order_action_sent"] is False, "durable reload sent order action")
    if executions["execution_report_rows"] == 0:
        require(durable_summary["state"] == "partial", "zero executions must keep durable reload partial")
        require(durable_summary["parity_status"] == "blocked", "zero executions must keep durable parity blocked")
        require(
            durable_summary["blocker_id"] == "real_order_fill_callbacks_not_available",
            "zero executions durable blocker mismatch",
        )
    require(
        "P019_RUNTIME_EVIDENCE_FRESHNESS_OK: status=blocked evidence=fresh" in freshness_step["stdout_tail"]
        or "P019_RUNTIME_EVIDENCE_FRESHNESS_OK: status=ready evidence=fresh" in freshness_step["stdout_tail"],
        "freshness validator pass signal missing",
    )

    boundaries = summary["boundaries"]
    for key in [
        "writes_outside_worktree",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "raw_config_file_contents_recorded",
        "tws_reinstall_performed",
        "screenshot_used_for_funds_positions",
        "order_action_sent",
    ]:
        require(boundaries[key] is False, f"boundary drifted: {key}")

    require_terms(
        ACCEPTANCE,
        [
            "refresh_p019_u3028269_current_state_closeout.py",
            "validate_p019_u3028269_current_state_closeout_refresh.py",
            "durable reload rebuild/validation",
            "P019_U3028269_CURRENT_STATE_CLOSEOUT_REFRESH_OK",
        ],
    )
    require_terms(
        PHASE_PLAN,
        [
            "refresh_p019_u3028269_current_state_closeout.py",
            "validate_p019_u3028269_current_state_closeout_refresh.py",
            "durable reload rebuild/validation",
            "P019_U3028269_CURRENT_STATE_CLOSEOUT_REFRESH_OK",
        ],
    )

    print(f"P019_U3028269_CURRENT_STATE_CLOSEOUT_REFRESH_OK: status={summary['status']}")


if __name__ == "__main__":
    main()
