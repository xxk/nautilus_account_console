from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
PIPELINE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
REAL_CLOSEOUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
DURABLE_RELOAD = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"
REAL_UI = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"


class CompletionAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CompletionAuditError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load(AUDIT)
    adr = ADR.read_text(encoding="utf-8")
    pipeline = load(PIPELINE)
    real_closeout = load(REAL_CLOSEOUT)
    executions = load(EXECUTIONS)
    durable_reload = load(DURABLE_RELOAD)
    real_ui = load(REAL_UI)

    require(payload["schema"] == "account-console.p019-completion-audit.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["adr_id"] == "ADR-0005", "ADR mismatch")
    require("decision_status: accepted" in adr, "ADR-0005 must be accepted")
    require("landing_status: foundation_accepted" in adr, "ADR-0005 landing mismatch")
    require(payload["overall_status"] == "accepted_with_residual_runtime_blockers", "overall status mismatch")
    require(payload["completion_must_not_be_claimed"] is False, "accepted foundation should allow closeout claim")
    require(payload["primary_runtime_blocker"] == "real_order_fill_callbacks_not_available", "primary blocker mismatch")
    require(payload["primary_runtime_blocker_detail"] == "same_slice_reqExecutions_returned_zero_rows", "primary blocker detail mismatch")
    require(payload["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(payload["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(payload["order_action_sent"] is False, "order action must not be sent")
    require(payload["synthetic_ready_contract_is_real_account_truth"] is False, "synthetic evidence cannot be real truth")

    adr_status = payload["adr_status"]
    require(adr_status["decision_status"] == "accepted", "audit ADR decision mismatch")
    require(adr_status["landing_status"] == "foundation_accepted", "audit ADR landing mismatch")
    require(adr_status["acceptance_required_before_direct_session"] is False, "ADR acceptance gate should be closed")
    require(adr_status["status"] == "accepted", "audit ADR status mismatch")

    runtime = payload["runtime_truth"]
    require(runtime["status"] == pipeline["status"] == "ready", "pipeline must be ready")
    require(runtime["tws_api_socket_ready"] is True, "TWS API socket must be ready")
    require(runtime["account_summary_success"] is True, "account summary must pass")
    require(runtime["positions_success"] is True, "positions must pass")
    require(runtime["source_package_state"] == "ready", "source package must be ready")

    closeout = payload["real_acceptance_closeout"]
    require(closeout["status"] == real_closeout["status"] == "ready", "real closeout must be ready")
    require(closeout["blocker_id"] is None and real_closeout["blocker_id"] is None, "ready closeout cannot carry blocker")
    require(closeout["pipeline_status"] == "ready", "closeout pipeline status mismatch")
    require(closeout["real_ui_parity_verdict"] == real_closeout["real_ui_parity_verdict"] == "pass", "UI parity must pass")
    require(closeout["synthetic_evidence_used_for_real_closeout"] is False, "synthetic closeout boundary missing")
    require(real_ui["verdict"] == "pass", "real UI evidence must pass")
    require(real_ui["parity"]["funds_parity"] == "pass", "funds parity must pass")
    require(real_ui["parity"]["positions_parity"] == "pass", "positions parity must pass")
    require(real_ui["boundaries"]["screenshot_used_for_funds_positions"] is False, "real UI screenshot boundary missing")
    require(real_ui["boundaries"]["order_action"] is False, "real UI order boundary missing")

    exec_closeout = closeout["execution_report_closeout"]
    require(executions["success"] is True, "real executions query must have succeeded")
    require(exec_closeout["executions_query_success"] is True, "closeout executions success mismatch")
    require(exec_closeout["executions_readonly_api_call"] == "reqExecutions", "executions API call mismatch")
    require(exec_closeout["executions_complete_history_claimed"] is False, "complete history must not be claimed")
    require(exec_closeout["executions_order_action_sent"] is False, "executions must not send order action")
    require(exec_closeout["execution_report_rows"] == executions["execution_report_rows"], "execution row count mismatch")
    require(exec_closeout["execution_report_rows"] == len(executions["executions"]), "execution list count mismatch")
    if executions["execution_report_rows"] == 0:
        require(executions["empty_state"] == "not_available_or_no_matching_executions", "zero executions need typed empty state")
        require(exec_closeout["orders_fills_parity"] in {"pass", "blocked"}, "open-order parity may pass while fills remain blocked")
        require(exec_closeout["execution_reports_table_parity"] in {"pass", "blocked"}, "open-order table parity may pass while fills remain blocked")
        for key in ["execution_reports_persistence_parity", "report_parity_status"]:
            require(exec_closeout[key] == "blocked", f"{key} must remain blocked for zero real execution rows")

    requirements = {item["id"]: item for item in payload["acceptance_requirements"]}
    require(set(requirements) == {f"A{idx}" for idx in range(1, 15)}, "audit must cover A1-A14")
    for accepted_id in ["A1", "A2", "A3", "A6", "A7", "A10", "A12", "A14"]:
        require(requirements[accepted_id]["current_status"] == "accepted", f"{accepted_id} should be accepted")
        require(requirements[accepted_id]["missing_for_completion"] == [], f"{accepted_id} should have no missing completion items")
    for blocked_id in ["A4", "A5", "A9", "A11", "A13"]:
        require(
            requirements[blocked_id]["current_status"] == "accepted_foundation_real_rows_blocked",
            f"{blocked_id} should preserve real-row blocker",
        )
        require(requirements[blocked_id]["missing_for_completion"], f"{blocked_id} must list residual runtime evidence")
    require(requirements["A8"]["current_status"] == "accepted_foundation_realtime_blocked", "A8 realtime status mismatch")

    closeout_requirements = {item["id"]: item for item in payload["required_before_implementation_closeout"]}
    require(set(closeout_requirements) == {f"C{idx}" for idx in range(1, 11)}, "audit must cover C1-C10")
    for proved_id in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C9", "C10"]:
        require(closeout_requirements[proved_id]["status"] == "proved", f"{proved_id} should be proved")
    require(
        closeout_requirements["C8"]["status"] == "accepted_foundation_real_rows_blocked",
        "C8 should preserve report-row residual blocker",
    )

    blockers = {item["blocker_id"]: item for item in payload["blocking_conditions"]}
    require("adr0005_not_accepted" not in blockers, "ADR blocker must be retired after acceptance")
    for blocker_id in [
        "synthetic_contract_not_real_truth",
        "real_order_fill_callbacks_not_available",
        "real_durable_store_reload_partial_empty_executions",
    ]:
        require(blocker_id in blockers, f"missing blocker {blocker_id}")
    require(
        blockers["real_order_fill_callbacks_not_available"]["evidence"]
        == "output/account_capability/ib-live-u3028269/tws-api/executions.json",
        "real order/fill blocker evidence mismatch",
    )

    durable_summary = payload["real_durable_store_reload"]
    durable_proof = durable_reload["reload_proof"]
    durable_replay = durable_reload["replay_state"]
    require(durable_summary["artifact_ref"] == "output/account_capability/ib-live-u3028269/durable-store-reload.json", "durable artifact ref mismatch")
    require(durable_summary["state"] == durable_replay["state"], "durable state mismatch")
    require(durable_summary["parity_status"] == durable_proof["parity_status"], "durable parity mismatch")
    require(durable_summary["records_loaded_from_live_memory"] == durable_proof["records_loaded_from_live_memory"] == 0, "durable reload must not use live memory")
    require(durable_reload["boundaries"]["synthetic_evidence_used"] is False, "durable reload must not use synthetic evidence")
    require(durable_reload["boundaries"]["order_action_sent"] is False, "durable reload must not send order action")
    if executions["execution_report_rows"] == 0:
        require(durable_replay["state"] == "partial", "zero real rows must keep durable reload partial")
        require(durable_proof["parity_status"] == "blocked", "zero real rows must keep durable parity blocked")

    print("P019_COMPLETION_AUDIT_OK: overall=accepted residual_blockers=real_parity")


if __name__ == "__main__":
    main()
