from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "README.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
COMPLETION_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
ADR_ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-20-adr0005-broker-observation-session-acceptance.json"
REAL_UI_PARITY_EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
DURABLE_RELOAD = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"


class FoundationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FoundationError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    proposal = read(PROPOSAL)
    phase_plan = read(PHASE_PLAN)
    acceptance = read(ACCEPTANCE)
    adr = read(ADR)
    owner_map = read(OWNER_MAP)
    completion = load(COMPLETION_AUDIT)
    adr_acceptance = load(ADR_ACCEPTANCE)
    real_ui = load(REAL_UI_PARITY_EVIDENCE)
    source_package = load(SOURCE_PACKAGE)
    executions = load(EXECUTIONS)
    durable_reload = load(DURABLE_RELOAD)

    require("- Status: accepted_with_residual_runtime_blockers" in proposal, "P019 README must be accepted")
    require("- Status: accepted_with_residual_runtime_blockers" in phase_plan, "P019 phase plan must be accepted")
    require("- Status: accepted_with_residual_runtime_blockers" in acceptance, "P019 acceptance must be accepted")
    require("decision_status: accepted" in adr, "ADR-0005 must be accepted")
    require("landing_status: foundation_accepted" in adr, "ADR-0005 landing mismatch")
    require("P019 Broker Observation Session Foundation Accepted Assignment" in owner_map, "owner map accepted assignment missing")

    require(completion["overall_status"] == "accepted_with_residual_runtime_blockers", "completion audit status mismatch")
    require(completion["adr_status"]["decision_status"] == "accepted", "completion ADR status mismatch")
    require(completion["real_acceptance_closeout"]["status"] == "ready", "real closeout must be ready")
    require(completion["real_acceptance_closeout"]["real_ui_parity_verdict"] == "pass", "real UI parity must pass")
    require(adr_acceptance["verdict"] == "accepted", "ADR acceptance verdict mismatch")
    require(adr_acceptance["status"] == "accepted_with_residual_runtime_blockers", "ADR acceptance status mismatch")

    require(real_ui["verdict"] == "pass", "real UI parity evidence must pass")
    require(real_ui["parity"]["funds_parity"] == "pass", "funds parity must pass")
    require(real_ui["parity"]["positions_parity"] == "pass", "positions parity must pass")
    require(source_package["source_health"]["state"] == "ready", "source package must be ready")
    require(source_package["boundaries"]["raw_secret_values_recorded"] is False, "source package secret boundary drifted")
    require(source_package["boundaries"]["screenshot_used_for_funds_positions"] is False, "source package screenshot boundary drifted")
    require(source_package["boundaries"]["order_action_sent"] is False, "source package order boundary drifted")

    require(executions["success"] is True, "executions query must have succeeded")
    readonly_query = executions["readonly_query"]
    require(readonly_query["api_call"] == "reqExecutions", "executions query must remain read-only")
    require(readonly_query["complete_history_claimed"] is False, "complete execution history must not be claimed")
    require(executions["order_action_sent"] is False, "executions query must not send order action")
    require(readonly_query["order_action_sent"] is False, "readonly executions query must not send order action")
    if executions["execution_report_rows"] == 0:
        require(executions["empty_state"] == "not_available_or_no_matching_executions", "zero execution rows need typed empty state")
        require(durable_reload["replay_state"]["state"] == "partial", "zero rows should keep durable reload partial")
        require(durable_reload["reload_proof"]["parity_status"] == "blocked", "zero rows should keep durable parity blocked")

    require(durable_reload["reload_proof"]["records_loaded_from_live_memory"] == 0, "durable reload must not use live memory")
    require(durable_reload["boundaries"]["synthetic_evidence_used"] is False, "durable reload synthetic boundary drifted")
    require(durable_reload["boundaries"]["order_action_sent"] is False, "durable reload order boundary drifted")

    require_terms(
        ACCEPTANCE,
        [
            "ADR0005_ACCEPTANCE_OK: status=accepted",
            "P019_COMPLETION_AUDIT_OK: overall=accepted residual_blockers=real_parity",
            "P019_BROKER_OBSERVATION_FOUNDATION_OK: status=accepted residual_blockers=real_parity",
            "P019_U3028269_REAL_UI_PARITY_OK: verdict=pass",
            "P019_U3028269_REAL_DURABLE_STORE_RELOAD_OK",
            "P019_OPEN_ORDERS_ACCEPTANCE_DESIGN_OK",
        ],
    )
    require_terms(
        PHASE_PLAN,
        [
            "accepted_with_residual_runtime_blockers",
            "real_order_fill_callbacks_not_available",
            "real_durable_store_reload_partial_empty_executions",
            "validate_adr0005_acceptance.py",
        ],
    )

    for forbidden in [
        "raw_secret_values_recorded=true",
        "broker_truth=true",
        "order_action=true",
        "can_trade=true",
        "live_ready=true",
        "complete_history_claimed=true",
    ]:
        require(forbidden not in proposal, f"P019 README must not claim {forbidden}")
        require(forbidden not in acceptance, f"P019 acceptance must not claim {forbidden}")
        require(forbidden not in owner_map, f"owner map must not claim {forbidden}")

    print("P019_BROKER_OBSERVATION_FOUNDATION_OK: status=accepted residual_blockers=real_parity")


if __name__ == "__main__":
    main()
