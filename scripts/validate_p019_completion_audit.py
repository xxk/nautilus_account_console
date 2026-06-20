from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
PIPELINE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
WAIT_COLLECT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "wait-collect-summary.json"
REAL_CLOSEOUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
SYNTHETIC_READY_UI = (
    ROOT
    / "docs"
    / "acceptance"
    / "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json"
)


class CompletionAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CompletionAuditError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(AUDIT)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)
    adr = read(ADR)
    pipeline = load(PIPELINE)
    wait_collect = load(WAIT_COLLECT)
    real_closeout = load(REAL_CLOSEOUT)
    synthetic_ready_ui = load(SYNTHETIC_READY_UI)

    require(payload["schema"] == "account-console.p019-completion-audit.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["adr_id"] == "ADR-0005", "ADR mismatch")
    require(payload["overall_status"] == "not_complete", "P019 completion audit must remain not_complete")
    require(payload["completion_must_not_be_claimed"] is True, "completion must not be claimed")
    require(payload["primary_runtime_blocker"] in {"adr0005_not_accepted", "tws_api_readiness_missing"}, "primary runtime blocker mismatch")
    if payload["primary_runtime_blocker"] == "tws_api_readiness_missing":
        require(
            payload["primary_runtime_blocker_detail"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "primary runtime detail mismatch",
        )
    require(payload["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(payload["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(payload["order_action_sent"] is False, "order action must not be sent")
    require(payload["synthetic_ready_contract_is_real_account_truth"] is False, "synthetic ready contract cannot be real truth")

    require("decision_status: proposed" in adr, "ADR-0005 must remain proposed")
    require(payload["adr_status"]["decision_status"] == "proposed", "completion audit ADR status mismatch")
    require(payload["adr_status"]["landing_status"] == "not_started", "completion audit ADR landing mismatch")
    require(payload["adr_status"]["acceptance_required_before_direct_session"] is True, "ADR acceptance gate missing")

    runtime = payload["runtime_truth"]
    require(runtime["tws_process_present"] is True, "runtime audit should retain TWS process evidence")
    require(runtime["tws_account_window_ref"] == "U3028269_account_window", "runtime account window ref mismatch")
    require(runtime["tws_api_socket_ready"] == (pipeline["status"] == "ready"), "runtime socket status must mirror pipeline")
    require(runtime["account_summary_success"] == pipeline["account_summary_success"], "runtime account summary status mismatch")
    require(runtime["positions_success"] == pipeline["positions_success"], "runtime positions status mismatch")
    require(runtime["source_package_state"] == pipeline["source_package_state"], "runtime source package state mismatch")
    require(runtime["status"] == pipeline["status"], "runtime status must mirror pipeline")

    closeout_audit = payload["real_acceptance_closeout"]
    require(
        closeout_audit["closeout_summary_ref"] == "output/account_capability/ib-live-u3028269/real-acceptance-closeout.json",
        "completion audit closeout summary ref mismatch",
    )
    require(closeout_audit["runner_ref"] == "scripts/run_p019_u3028269_real_acceptance_closeout.py", "runner ref mismatch")
    require(
        closeout_audit["validator_ref"] == "scripts/validate_p019_u3028269_real_acceptance_closeout.py",
        "validator ref mismatch",
    )
    require(closeout_audit["synthetic_evidence_used_for_real_closeout"] is False, "synthetic closeout boundary missing")
    require(closeout_audit["status"] == real_closeout["status"], "completion audit closeout status mismatch")
    require(closeout_audit["blocker_id"] == real_closeout["blocker_id"], "completion audit closeout blocker mismatch")
    require(closeout_audit["pipeline_status"] == real_closeout["pipeline_status"], "completion audit pipeline status mismatch")
    require(
        closeout_audit["real_ui_parity_verdict"] == real_closeout["real_ui_parity_verdict"],
        "completion audit UI parity verdict mismatch",
    )
    require(
        closeout_audit["required_ready_chain"] == real_closeout["required_ready_chain"],
        "completion audit ready chain mismatch",
    )

    require(pipeline["status"] in {"blocked", "ready"}, "pipeline status mismatch")
    if pipeline["status"] == "ready":
        require(pipeline["blocker_id"] is None, "ready pipeline must not carry blocker")
        require(pipeline["ready_for_tws_api_funds_positions_query"] is True, "ready pipeline readiness must be true")
        require(pipeline["account_summary_success"] is True, "ready pipeline account summary success must be true")
        require(pipeline["positions_success"] is True, "ready pipeline positions success must be true")
        require(pipeline["source_package_state"] == "ready", "ready pipeline source package state mismatch")
    else:
        require(pipeline["blocker_id"] == "tws_api_readiness_missing", "pipeline blocker mismatch")
        require(pipeline["ready_for_tws_api_funds_positions_query"] is False, "pipeline readiness must be false")
        require(pipeline["account_summary_success"] is False, "pipeline account summary success must be false")
        require(pipeline["positions_success"] is False, "pipeline positions success must be false")
        require(pipeline["source_package_state"] == "blocked", "pipeline source package state must be blocked")
    require(wait_collect["status"] in {"blocked", "ready"}, "wait collect status mismatch")
    if wait_collect["status"] == "blocked":
        require(wait_collect["pipeline_ran"] is False, "wait collect must not have run pipeline before readiness")
    else:
        require(wait_collect["pipeline_ran"] is True, "ready wait collect must run pipeline")
    require(real_closeout["status"] in {"blocked", "ready"}, "real closeout status mismatch")
    if real_closeout["status"] == "ready":
        require(real_closeout["blocker_id"] is None, "ready real closeout must not carry blocker")
        require(real_closeout["real_ui_parity_verdict"] == "pass", "ready real closeout UI parity must pass")
    else:
        require(real_closeout["blocker_id"] == "tws_api_readiness_missing", "real closeout blocker mismatch")
        require(real_closeout["real_ui_parity_verdict"] == "blocked", "real closeout UI parity must be blocked")
    require(
        real_closeout["boundaries"]["synthetic_evidence_used_for_real_closeout"] is False,
        "real closeout must reject synthetic evidence",
    )

    requirements = {item["id"]: item for item in payload["acceptance_requirements"]}
    require(set(requirements) == {f"A{idx}" for idx in range(1, 15)}, "audit must cover A1-A14")
    for req_id, item in requirements.items():
        require(item["current_status"] == "pre_acceptance_partial", f"{req_id} must remain pre_acceptance_partial")
        require(item["missing_for_completion"], f"{req_id} must list missing completion evidence")

    closeout = {item["id"]: item for item in payload["required_before_implementation_closeout"]}
    require(set(closeout) == {f"C{idx}" for idx in range(1, 11)}, "audit must cover C1-C10")
    require(closeout["C8"]["status"] == "pre_acceptance_partial", "C8 must remain pre_acceptance_partial")
    require(
        closeout["C8"].get("missing_for_completion")
        == [
            "accepted real owner/runtime report-row parity",
            "accepted real owner/runtime persistence reload parity",
        ],
        "C8 missing real report/store evidence conditions drifted",
    )
    require(
        synthetic_ready_ui["verdict"] == "synthetic_contract_only",
        "synthetic report/store evidence must remain synthetic-only",
    )
    observed_contract = synthetic_ready_ui["observed_contract_values"]
    require(observed_contract["execution_report_types"] == ["OrderStatusReport", "FillReport"], "C8 synthetic reports missing")
    require(observed_contract["reload_parity_status"] == "passed", "C8 synthetic reload parity missing")
    require(observed_contract["records_loaded_from_live_memory"] == 0, "C8 synthetic reload must not use live memory")
    require(
        "does_not_prove_real_u3028269_order_or_fill_callbacks" in synthetic_ready_ui["explicit_non_claims"],
        "synthetic report evidence must not prove real callbacks",
    )
    require(
        synthetic_ready_ui["boundaries"]["execution_reports_synthetic_contract_only"] is True,
        "synthetic report boundary missing",
    )
    require(
        synthetic_ready_ui["boundaries"]["durable_store_synthetic_contract_only"] is True,
        "synthetic store boundary missing",
    )
    if real_closeout["status"] == "ready":
        require(closeout["C9"]["status"] == "proved", "C9 should be proved when real closeout is ready")
        require(closeout["C10"]["status"] == "proved", "C10 should be proved when pipeline is ready")
    else:
        for blocked_id in ["C9", "C10"]:
            require(closeout[blocked_id]["status"] == "blocked", f"{blocked_id} must remain blocked")
            require(closeout[blocked_id].get("missing_for_completion"), f"{blocked_id} must list missing evidence")
    if real_closeout["status"] != "ready":
        require(closeout["C9"]["missing_for_completion"] == [
            "ready_for_tws_api_funds_positions_query=true",
            "account_summary_success=true",
            "positions_success=true",
            "source_package_state=ready",
            "query_source_parity=pass",
            "real_ui_parity_verdict=pass",
            "P019_U3028269_REAL_ACCEPTANCE_CLOSEOUT_OK: status=ready",
        ], "C9 missing real parity conditions drifted")

    blockers = {item["blocker_id"]: item for item in payload["blocking_conditions"]}
    for blocker_id in ["adr0005_not_accepted", "synthetic_contract_not_real_truth"]:
        require(blocker_id in blockers, f"missing blocker {blocker_id}")
    if pipeline["status"] == "ready":
        require("tws_api_readiness_missing" not in blockers, "ready audit must not keep TWS readiness blocker")
    else:
        require("tws_api_readiness_missing" in blockers, "blocked audit missing TWS readiness blocker")

    for term in [
        "p019-completion-audit.json",
        "validate_p019_completion_audit.py",
        "P019_COMPLETION_AUDIT_OK",
    ]:
        require(term in acceptance, f"acceptance missing completion audit term {term}")
        require(term in phase_plan, f"phase plan missing completion audit term {term}")

    blocker_label = "adr0005,real_parity" if pipeline["status"] == "ready" else "adr0005,tws_api_readiness,real_parity"
    print(f"P019_COMPLETION_AUDIT_OK: overall=not_complete blockers={blocker_label}")


if __name__ == "__main__":
    main()
