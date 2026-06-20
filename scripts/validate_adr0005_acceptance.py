from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-20-adr0005-broker-observation-session-acceptance.json"
P019_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
PIPELINE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
REAL_UI = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
DURABLE_RELOAD = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"


class Adr0005AcceptanceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Adr0005AcceptanceError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    adr = ADR.read_text(encoding="utf-8")
    acceptance = load(ACCEPTANCE)
    audit = load(P019_AUDIT)
    source_package = load(SOURCE_PACKAGE)
    pipeline = load(PIPELINE)
    executions = load(EXECUTIONS)
    real_ui = load(REAL_UI)
    durable_reload = load(DURABLE_RELOAD)

    require("decision_status: accepted" in adr, "ADR-0005 must be accepted")
    require("landing_status: foundation_accepted" in adr, "ADR-0005 landing status mismatch")
    require("Executable landing consistency gate: `python scripts\\validate_adr0005_acceptance.py`" in adr, "ADR gate link missing")

    require(
        acceptance["schema"] == "account-console.adr0005-broker-observation-session-acceptance.v1",
        "acceptance schema drifted",
    )
    require(acceptance["adr_id"] == "ADR-0005", "ADR id mismatch")
    require(acceptance["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(acceptance["decision_status"] == "accepted", "decision status mismatch")
    require(acceptance["landing_status"] == "foundation_accepted", "landing status mismatch")
    require(acceptance["verdict"] == "accepted", "verdict mismatch")
    require(acceptance["status"] == "accepted_with_residual_runtime_blockers", "status mismatch")

    items = {item["id"]: item for item in acceptance["decision_items"]}
    require(set(items) == {f"D{idx}" for idx in range(1, 13)}, "D1-D12 coverage missing")
    for item_id, item in items.items():
        require(item["status"].startswith("accepted"), f"{item_id} not accepted")
        require(item["evidence"], f"{item_id} missing evidence")
    for item_id in ["D4", "D5", "D11"]:
        require(
            items[item_id]["status"] == "accepted_foundation_real_rows_blocked",
            f"{item_id} must preserve real-row residual blocker",
        )
        require(items[item_id].get("residual_blocker_id"), f"{item_id} missing residual blocker")
    require(items["D8"]["status"] == "accepted_foundation_realtime_blocked", "D8 realtime boundary mismatch")

    boundaries = acceptance["boundaries"]
    for key in [
        "command_enabled",
        "order_action_sent",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "screenshot_used_for_funds_positions",
        "synthetic_evidence_used_for_real_closeout",
        "broker_truth",
        "account_truth",
        "trading_readiness_truth",
    ]:
        require(boundaries[key] is False, f"boundary {key} must be false")

    closeout = acceptance["real_u3028269_closeout"]
    require(closeout["status"] == "ready", "real U3028269 closeout must be ready")
    require(closeout["funds_parity"] == "pass", "funds parity must pass")
    require(closeout["positions_parity"] == "pass", "positions parity must pass")
    require(closeout["executions_query_success"] is True, "executions query must have succeeded")
    require(closeout["execution_report_rows"] == executions["execution_report_rows"], "execution row count drifted")
    require(closeout["orders_fills_parity"] == "blocked", "zero-row orders/fills parity must remain blocked")
    require(closeout["execution_reports_persistence_parity"] == "blocked", "zero-row persistence parity must remain blocked")

    require(pipeline["status"] == "ready", "pipeline must be ready")
    require(source_package["source_health"]["state"] == "ready", "source package must be ready")
    require(source_package["source_health"]["api_transport"] == "ib_tws_api", "source package transport mismatch")
    require(source_package["boundaries"]["raw_secret_values_recorded"] is False, "source package secret boundary drifted")
    require(source_package["boundaries"]["screenshot_used_for_funds_positions"] is False, "source package screenshot boundary drifted")
    require(source_package["boundaries"]["order_action_sent"] is False, "source package order boundary drifted")
    require(source_package["balances"], "ready source package must include balances")
    require(source_package["positions"], "ready source package must include positions")

    require(real_ui["verdict"] == "pass", "real UI parity must pass")
    require(real_ui["parity"]["funds_parity"] == "pass", "real UI funds parity must pass")
    require(real_ui["parity"]["positions_parity"] == "pass", "real UI positions parity must pass")
    require(real_ui["boundaries"]["screenshot_used_for_funds_positions"] is False, "real UI screenshot boundary drifted")
    require(real_ui["boundaries"]["order_action"] is False, "real UI order boundary drifted")
    require(real_ui["compared_against"]["executions_query_success"] is True, "real UI executions query flag drifted")
    require(real_ui["compared_against"]["execution_report_rows"] == executions["execution_report_rows"], "real UI row count drifted")
    require(real_ui["compared_against"]["executions_complete_history_claimed"] is False, "complete history must not be claimed")
    require(real_ui["compared_against"]["executions_order_action_sent"] is False, "order action must not be sent")

    require(executions["success"] is True, "executions query must succeed")
    readonly_query = executions["readonly_query"]
    require(readonly_query["api_call"] == "reqExecutions", "executions must use read-only reqExecutions")
    require(executions["order_action_sent"] is False, "executions query must not send order action")
    require(readonly_query["order_action_sent"] is False, "readonly executions query must not send order action")
    require(readonly_query["complete_history_claimed"] is False, "complete history must not be claimed")
    require(executions["execution_report_rows"] == len(executions["executions"]), "execution row count mismatch")
    if executions["execution_report_rows"] == 0:
        require(
            executions["empty_state"] == "not_available_or_no_matching_executions",
            "zero executions must carry typed empty state",
        )

    reload_proof = durable_reload["reload_proof"]
    replay_state = durable_reload["replay_state"]
    require(reload_proof["records_loaded_from_live_memory"] == 0, "durable reload must not use live memory")
    require(durable_reload["boundaries"]["synthetic_evidence_used"] is False, "durable reload synthetic boundary drifted")
    require(durable_reload["boundaries"]["order_action_sent"] is False, "durable reload order boundary drifted")
    if executions["execution_report_rows"] == 0:
        require(replay_state["state"] == "partial", "zero real execution rows must keep reload partial")
        require(reload_proof["parity_status"] == "blocked", "zero real execution rows must keep reload blocked")

    residuals = {item["blocker_id"]: item for item in acceptance["residual_runtime_blockers"]}
    for blocker_id in [
        "real_order_fill_callbacks_not_available",
        "real_durable_store_reload_partial_empty_executions",
    ]:
        require(blocker_id in residuals, f"missing residual blocker {blocker_id}")
        require(residuals[blocker_id]["retry_condition"], f"{blocker_id} missing retry condition")

    require(audit["schema"] == "account-console.p019-completion-audit.v1", "P019 audit schema drifted")
    require(audit["adr_status"]["decision_status"] == "accepted", "P019 audit ADR status must be accepted")
    require(audit["overall_status"] == "accepted_with_residual_runtime_blockers", "P019 audit status mismatch")
    require(audit["completion_must_not_be_claimed"] is False, "P019 accepted foundation should allow closeout claim")
    require(audit["real_acceptance_closeout"]["status"] == "ready", "P019 real closeout must be ready")
    require(audit["real_acceptance_closeout"]["real_ui_parity_verdict"] == "pass", "P019 UI parity must pass")

    print("ADR0005_ACCEPTANCE_OK: status=accepted residual_blockers=real_order_fill_callbacks_not_available,real_durable_store_reload_partial_empty_executions")


if __name__ == "__main__":
    main()
