from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-reinstall-decision.json"
RUNBOOK = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "tws-api-runtime-recovery-runbook.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class ReinstallDecisionGateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReinstallDecisionGateError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(DECISION)
    runbook = read(RUNBOOK)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-tws-reinstall-decision.v1", "schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["decision"] == "do_not_reinstall_yet", "current decision must not recommend reinstall")
    require(payload["reinstall_recommended"] is False, "reinstall must not be recommended for current evidence")
    evidence = payload["current_evidence"]
    require(evidence["tws_process_present"] is True, "TWS process should be present")
    require(evidence["firewall_allow_rules_present"] is True, "firewall allow rules should be present")
    require(evidence["firewall_enabled_block_rules_present"] is False, "firewall block rules should be absent")
    ready_for_query = evidence.get("ready_for_tws_api_funds_positions_query") is True
    if ready_for_query:
        require(payload["primary_next_action"] == "run_real_acceptance_closeout", "ready next action mismatch")
        require(evidence["known_api_ports_connectable"] is True, "ready decision needs connectable API port")
        require(evidence["config_primary_blocker"] is None, "ready decision must not carry config blocker")
    else:
        require(
            payload["primary_next_action"] == "enable_logged_in_tws_api_socket_then_restart_or_reconnect_and_rerun_pipeline",
            "blocked next action mismatch",
        )
        require(evidence["latest_config_socket_client"] == "false", "latest socketClient should still be false")
        require(evidence["latest_config_api_socket_enabled"] is False, "latest API socket should be disabled")
        require(evidence["known_api_ports_connectable"] is False, "known API ports should not be connectable")
        require(
            evidence["config_primary_blocker"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "config primary blocker mismatch",
        )

    preconditions = payload["reinstall_preconditions"]
    require(preconditions["operator_approved_exact_path_reason_impact"] is False, "operator approval must not be inferred")
    if ready_for_query:
        require(
            "known_api_port_still_not_listening_after_enable_and_restart" not in payload["unmet_reinstall_preconditions"],
            "ready decision should not list listener as unmet",
        )
    else:
        require(preconditions["api_socket_enabled_in_logged_in_tws"] is False, "API socket is not enabled yet")
        require(
            "api_socket_enabled_in_logged_in_tws" in payload["unmet_reinstall_preconditions"],
            "missing API socket precondition blocker",
        )
    require(
        "operator_approved_exact_path_reason_impact" in payload["unmet_reinstall_preconditions"],
        "missing operator approval precondition blocker",
    )

    for step in [
        "ready_for_tws_api_funds_positions_query=true",
        "readonly_tws_api_account_summary_success=true",
        "readonly_tws_api_positions_success=true",
        "source_package_state=ready",
        "account_mirror_projection_from_real_source_package",
        "ui_parity_against_same_slice_tws_api_source",
    ]:
        require(step in payload["required_before_real_funds_positions"], f"missing real closeout step {step}")

    boundaries = payload["boundaries"]
    require(boundaries["writes_outside_worktree"] is False, "decision artifact must not write outside worktree")
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["raw_config_file_contents_recorded"] is False, "raw config contents must not be recorded")
    require(boundaries["tws_reinstall_performed"] is False, "validator must not perform reinstall")
    require(boundaries["tws_api_account_query_sent"] is False, "decision gate must not query account")
    require(boundaries["funds_positions_values_recorded"] is False, "decision gate must not record values")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not be funds truth")
    require(boundaries["order_action_sent"] is False, "decision gate must not send order action")

    for term in [
        "Reinstall Decision Gate",
        "Do not reinstall TWS as the first remediation",
        "explicit operator approval",
        "exact path, reason and expected impact",
    ]:
        require(term in runbook, f"runbook missing {term}")
    for term in [
        "decide_p019_tws_reinstall_gate.py",
        "validate_p019_tws_reinstall_decision_gate.py",
        "P019_TWS_REINSTALL_DECISION_GATE_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    next_label = "real_closeout" if ready_for_query else "enable_api_socket"
    print(f"P019_TWS_REINSTALL_DECISION_GATE_OK: decision=do_not_reinstall_yet next={next_label}")


if __name__ == "__main__":
    main()
