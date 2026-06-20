from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "README.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-implementation-audit.md"
PREACCEPTANCE_COVERAGE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-acceptance-coverage.md"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
UI_EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json"
REAL_UI_PARITY_EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
TWS_WINDOW_BLOCKER = (
    ROOT
    / "output"
    / "debug"
    / "p019-tws-local-window-confirmation"
    / "tws-local-window-confirmation-blocker.json"
)
TWS_API_READINESS_PROBE = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"
TWS_API_SOCKET_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-socket-diagnostic.json"
WINDOWS_FIREWALL_TWS_API_DIAGNOSTIC = (
    ROOT / "output" / "debug" / "p019-tws-api-readiness" / "windows-firewall-tws-api-diagnostic.json"
)
TWS_API_CONFIG_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
TWS_REINSTALL_DECISION = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-reinstall-decision.json"
TWS_API_ENABLE_CHANGE_REQUEST = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-enable-change-request.json"
IB_U3028269_SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
TWS_API_WAIT_COLLECT_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "wait-collect-summary.json"
REAL_ACCEPTANCE_CLOSEOUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
COMPLETION_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
LANE_MANIFEST = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "evidence-lane-manifest.json"
PROFILE = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_profile_blocked_adr0005_not_accepted.json"
STORE_COMPLETE = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_store_complete_reload.json"
STORE_GAP = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_store_gap_blocker.json"
SESSION_CONFLICT = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_session_conflict_policy_blocked.json"
FRESHNESS_SEQUENCE = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_freshness_sequence_blocked_gap.json"
CROSS_BROKER_MATRIX = ROOT / "contracts" / "broker_observation" / "fixtures" / "cross_broker_extension_matrix_blocked.json"
REPORT_MAPPING = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_report_mapping_matrix.json"


class FoundationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FoundationError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    proposal = read(PROPOSAL)
    phase_plan = read(PHASE_PLAN)
    acceptance = read(ACCEPTANCE)
    preacceptance_coverage = read(PREACCEPTANCE_COVERAGE)
    adr = read(ADR)
    proposal_index = read(PROPOSAL_INDEX)
    owner_map = read(OWNER_MAP)

    require("- Status: proposed" in proposal, "P019 README must remain proposed")
    require("- Status: proposed" in phase_plan, "P019 phase plan must remain proposed")
    require("decision_status: proposed" in adr, "ADR-0005 must remain proposed until explicitly accepted")
    require("landing_status: not_started" in adr, "ADR-0005 landing must not be overclaimed")
    require("| [P019 Broker Observation Session Foundation]" in proposal_index, "proposal index missing P019")
    require("| [P019 Broker Observation Session Foundation](./p019-broker-observation-session-foundation/README.md) | proposed |" in proposal_index, "proposal index must keep P019 proposed")
    require("[IB TWS](../../topics/ib-tws/README.md)" in proposal, "P019 README missing IB TWS topic link")
    require("workspace-home-runbook-intake.md" in proposal, "P019 README missing runbook intake")
    require("u3028269-tws-login-and-api-knowledge.md" in proposal, "P019 README missing U3028269 knowledge card")

    for forbidden in [
        "**Current verdict**: `accepted`",
        "**Current verdict**: `implemented`",
        "| Allows broker order action | yes |",
        "| Allows raw broker secrets | yes |",
        "| Allows direct broker observation session | yes |",
        "live_ready=true",
        "can_trade=true",
        "broker_tradable=true",
    ]:
        require(forbidden not in proposal, f"P019 README must not claim {forbidden}")

    require_terms(
        ACCEPTANCE,
        [
            "ADR0005_BROKER_OBSERVATION_CONTRACTS_OK: positive=8 negative=13 docs_gates=ok",
            "ACCOUNT_MIRROR_API_OK: accounts=5 ib_tws_u3028269=",
            "P019_U3028269_BLOCKED_UI_EVIDENCE_OK: verdict=blocked surfaces=7",
            "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json",
            "process_and_window_title_confirmed_screenshot_blocked_minimized",
            "pre-acceptance partial",
            "positive per-currency TWS parity remains required",
            "P019_OWNER_MAP_ALIGNMENT_OK: pending_owner=guarded adr0005=proposed",
            "P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true",
            "P019_API_BOUNDARY_OK: mirror_only=true command_routes=absent direct_broker_routes=absent",
            "P019_PROFILE_SECURITY_PROVENANCE_OK: observation_only=true raw_secret_refs_only=true raw_payload_provenance_only=true",
            "P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=partial",
            "P019_TWS_API_READINESS_PROBE_OK",
            "P019_TWS_API_SOCKET_DIAGNOSTIC_OK",
            "P019_WINDOWS_FIREWALL_TWS_API_DIAGNOSTIC_OK",
            "P019_TWS_API_CONFIG_DIAGNOSTIC_OK",
            "P019_IB_U3028269_TWS_API_QUERIES_OK",
            "P019_IB_U3028269_SOURCE_PACKAGE_OK",
            "P019_IB_U3028269_QUERY_SOURCE_PARITY_OK",
            "P019_IB_TWS_READY_SOURCE_CONTRACT_OK",
            "P019_U3028269_SYNTHETIC_READY_UI_CONTRACT_OK",
            "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json",
            "P019_U3028269_REAL_UI_PARITY_OK",
            "2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
            "P019_IB_U3028269_TWS_API_PIPELINE_OK",
            "P019_TWS_API_WAIT_COLLECT_OK",
            "P019_TWS_API_RECOVERY_PATH_GUARD_OK",
            "P019_TWS_API_RUNTIME_RECOVERY_RUNBOOK_OK",
            "P019_WORKSPACE_HOME_RUNBOOK_INTAKE_OK",
            "IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_OK",
            "IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_BACKFILL_OK",
            "IB_TWS_TOPIC_INDEX_OK",
            "IB_TWS_KNOWLEDGE_REDACTION_OK",
            "P019_TWS_REINSTALL_DECISION_GATE_OK",
            "P019_TWS_API_ENABLE_CHANGE_REQUEST_OK",
            "P019_U3028269_REAL_ACCEPTANCE_CLOSEOUT_OK",
            "P019_RUNTIME_EVIDENCE_FRESHNESS_OK",
            "P019_RUNTIME_EVIDENCE_FRESHNESS_READY_CONTRACT_OK",
            "P019_RUNTIME_ARTIFACT_REDACTION_OK",
            "P019_U3028269_CURRENT_STATE_CLOSEOUT_REFRESH_OK",
            "P019_COMPLETION_AUDIT_OK",
            "diagnose_p019_windows_firewall_tws_api.py",
            "validate_p019_windows_firewall_tws_api_diagnostic.py",
            "diagnose_p019_tws_api_config.py",
            "validate_p019_tws_api_config_diagnostic.py",
            "validate_p019_ib_u3028269_query_source_parity.py",
            "validate_p019_ib_tws_ready_source_contract.py",
            "validate_p019_u3028269_synthetic_ready_ui_contract.py",
            "validate_p019_u3028269_real_ui_parity.py",
            "wait_p019_tws_api_ready_and_collect.py",
            "validate_p019_tws_api_wait_collect.py",
            "validate_p019_tws_api_recovery_path_guard.py",
            "validate_p019_tws_api_runtime_recovery_runbook.py",
            "validate_p019_workspace_home_runbook_intake.py",
            "validate_ib_tws_u3028269_login_api_knowledge.py",
            "prepare_ib_tws_u3028269_login_api_knowledge_backfill.py",
            "validate_ib_tws_u3028269_login_api_knowledge_backfill.py",
            "validate_ib_tws_topic_index.py",
            "validate_ib_tws_knowledge_redaction.py",
            "decide_p019_tws_reinstall_gate.py",
            "validate_p019_tws_reinstall_decision_gate.py",
            "prepare_p019_tws_api_enable_change_request.py",
            "validate_p019_tws_api_enable_change_request.py",
            "run_p019_u3028269_real_acceptance_closeout.py",
            "validate_p019_u3028269_real_acceptance_closeout.py",
            "validate_p019_runtime_evidence_freshness.py",
            "validate_p019_runtime_evidence_freshness_ready_contract.py",
            "validate_p019_runtime_artifact_redaction.py",
            "refresh_p019_u3028269_current_state_closeout.py",
            "validate_p019_u3028269_current_state_closeout_refresh.py",
            "validate_p019_completion_audit.py",
            "tws_api_readiness_missing",
        ],
    )
    require_terms(
        PHASE_PLAN,
        [
            "pre_acceptance_partial",
            "pending owner-map guard",
            "evidence-lane-manifest.json",
            "validate_p019_u3028269_blocked_ui_evidence.py",
            "validate_p019_owner_map_alignment.py",
            "validate_p019_evidence_lane_manifest.py",
            "validate_p019_api_boundary.py",
            "validate_p019_profile_security_provenance.py",
            "session_conflict_policy.schema.json",
            "ib_tws_session_conflict_policy_blocked.json",
            "freshness_sequence_checkpoint.schema.json",
            "ib_tws_freshness_sequence_blocked_gap.json",
            "cross_broker_extension_matrix.schema.json",
            "report_mapping_matrix.schema.json",
            "ib_tws_report_mapping_matrix.json",
            "IB TWS, CTP, stock broker, CQG and TT",
            "funds, positions, orders/fills, execution report table and persistence parity as typed `blocked`",
            "direct broker/TWS routes",
            "real owner-source report callback and durable-store reload evidence",
            "synthetic positive report-row/reload UI parity is present as contract evidence",
            "validate_p019_preacceptance_coverage.py",
            "validate_p019_tws_api_readiness_probe.py",
            "validate_p019_tws_api_socket_diagnostic.py",
            "validate_p019_windows_firewall_tws_api_diagnostic.py",
            "validate_p019_tws_api_config_diagnostic.py",
            "validate_p019_ib_u3028269_tws_api_queries.py",
            "validate_p019_ib_u3028269_source_package.py",
            "validate_p019_ib_u3028269_query_source_parity.py",
            "validate_p019_ib_tws_ready_source_contract.py",
            "validate_p019_u3028269_synthetic_ready_ui_contract.py",
            "validate_p019_u3028269_real_ui_parity.py",
            "validate_p019_ib_u3028269_tws_api_pipeline.py",
            "validate_p019_tws_api_wait_collect.py",
            "validate_p019_tws_api_recovery_path_guard.py",
            "validate_p019_tws_api_runtime_recovery_runbook.py",
            "validate_p019_workspace_home_runbook_intake.py",
            "validate_ib_tws_u3028269_login_api_knowledge.py",
            "prepare_ib_tws_u3028269_login_api_knowledge_backfill.py",
            "validate_ib_tws_u3028269_login_api_knowledge_backfill.py",
            "validate_ib_tws_topic_index.py",
            "validate_ib_tws_knowledge_redaction.py",
            "validate_p019_tws_reinstall_decision_gate.py",
            "validate_p019_tws_api_enable_change_request.py",
            "validate_p019_u3028269_real_acceptance_closeout.py",
            "validate_p019_runtime_evidence_freshness.py",
            "validate_p019_runtime_evidence_freshness_ready_contract.py",
            "validate_p019_runtime_artifact_redaction.py",
            "refresh_p019_u3028269_current_state_closeout.py",
            "validate_p019_u3028269_current_state_closeout_refresh.py",
            "validate_p019_completion_audit.py",
        ],
    )
    require_terms(
        OWNER_MAP,
        [
            "P019 Broker Observation Session Foundation Pending Assignment",
            "`account-console-broker-observation-session` is a pending capability owner",
            "P019 pre-acceptance work does not authorize Account Console to open a direct TWS/CTP/stock/CQG/TT session",
            "`adr0005_not_accepted`",
            "`direct_session_allowed=false`",
            "`raw_secret_values_recorded=false`",
            "no rows, no command and no broker truth",
        ],
    )
    for forbidden in [
        "direct_session_allowed=true",
        "raw_secret_values_recorded=true",
        "broker_truth=true",
        "order_action=true",
        "live_ready=true",
        "can_trade=true",
    ]:
        require(forbidden not in owner_map, f"owner map must not claim {forbidden}")
    require_terms(
        AUDIT,
        [
            "PRE-G01",
            "PRE-G09",
            "PRE-G03 P018/P019 lane separation",
            "Pre-acceptance contract mode",
            "adr0005_not_accepted",
            "P018 compatibility mode",
        ],
    )
    require_terms(
        PREACCEPTANCE_COVERAGE,
        [
            "- Status: pre-acceptance partial",
            "Funds and positions acceptance must come from an authorized TWS API login / owner runtime source / Account Mirror projection chain.",
            "Screenshots may confirm local operator/window state only",
            "screenshot evidence is forbidden for funds and positions truth",
            "P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=partial",
        ],
    )
    for row_id in [f"A{idx}" for idx in range(1, 15)]:
        require(f"| {row_id} | pre-acceptance partial |" in preacceptance_coverage, f"{row_id} missing partial coverage row")
    for row_id in [f"PRE-G{idx:02d}" for idx in range(1, 10)]:
        require(f"| {row_id} |" in preacceptance_coverage, f"{row_id} missing pre-code gate coverage row")

    ui_evidence = load(UI_EVIDENCE)
    require(ui_evidence["verdict"] == "blocked", "UI parity evidence must remain blocked")
    require(ui_evidence["blocker_id"] == "tws_api_readiness_missing", "UI evidence blocker mismatch")
    require(ui_evidence["blocker_kind"] == "source_unavailable", "UI evidence blocker kind mismatch")
    require(ui_evidence["boundaries"]["raw_secret_values_recorded"] is False, "raw secrets must stay false")
    require(ui_evidence["boundaries"]["direct_session_allowed"] is False, "direct session must stay false")
    require(ui_evidence["boundaries"]["broker_truth"] is False, "broker truth must stay false")
    require(ui_evidence["boundaries"]["order_action"] is False, "order action must stay false")
    for parity_name, parity_status in ui_evidence["parity"].items():
        require(parity_status == "blocked", f"{parity_name} must remain blocked")
    for item in ui_evidence["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing P019 browser screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty P019 browser screenshot {item['screenshot']}")

    real_ui_parity = load(REAL_UI_PARITY_EVIDENCE)
    require(
        real_ui_parity["schema"] == "account-console.p019-u3028269-real-ui-parity-evidence.v1",
        "real UI parity evidence schema drifted",
    )
    require(real_ui_parity["account_id"] == "acct.ib.live.u3028269", "real UI parity account drifted")
    require(real_ui_parity["source_kind"] == "ib_tws_observation", "real UI parity source kind drifted")
    require(
        real_ui_parity["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "real UI parity must not use screenshots for funds/positions",
    )
    require(real_ui_parity["boundaries"]["order_action"] is False, "real UI parity must not enable order action")
    if real_ui_parity["verdict"] == "blocked":
        require(
            real_ui_parity["blocker_id"] == "tws_api_readiness_missing",
            "blocked real UI parity must name TWS API readiness blocker",
        )
        require(real_ui_parity["parity"]["funds_parity"] == "blocked", "blocked real UI funds parity drifted")
        require(
            real_ui_parity["parity"]["positions_parity"] == "blocked",
            "blocked real UI positions parity drifted",
        )
    else:
        require(real_ui_parity["verdict"] == "pass", "real UI parity verdict must be blocked or pass")
        require(real_ui_parity["parity"]["funds_parity"] == "pass", "passing real UI funds parity required")
        require(real_ui_parity["parity"]["positions_parity"] == "pass", "passing real UI positions parity required")
        require(
            real_ui_parity["compared_against"]["api_route"] == "/api/mirror/accounts/acct.ib.live.u3028269",
            "real UI parity API route drifted",
        )

    window_blocker = load(TWS_WINDOW_BLOCKER)
    require(
        window_blocker["status"] == "process_and_window_title_confirmed_screenshot_blocked_minimized",
        "TWS local window blocker status drifted",
    )
    require(window_blocker["boundaries"]["visual_evidence_accepted"] is False, "minimized screenshot must not be accepted")
    require(window_blocker["boundaries"]["raw_secret_values_recorded"] is False, "TWS window blocker must not record secrets")

    api_probe = load(TWS_API_READINESS_PROBE)
    require(api_probe["schema"] == "account-console.p019-tws-api-readiness-probe.v1", "TWS API readiness probe schema drifted")
    require(api_probe["account_id"] == "acct.ib.live.u3028269", "TWS API readiness probe account drifted")
    require(api_probe["display_alias"] == "U3028269", "TWS API readiness probe alias drifted")
    require(api_probe["boundaries"]["raw_secret_values_recorded"] is False, "TWS API probe must not record secrets")
    require(api_probe["boundaries"]["raw_broker_endpoint_recorded"] is False, "TWS API probe must not record raw endpoint")
    require(api_probe["boundaries"]["tws_api_account_query_sent"] is False, "TWS API readiness probe must not send account query")
    require(api_probe["boundaries"]["funds_positions_values_recorded"] is False, "TWS API readiness probe must not record funds/positions values")
    require(api_probe["boundaries"]["screenshot_used_for_funds_positions"] is False, "TWS API probe must not use screenshot for funds/positions")
    require(api_probe["boundaries"]["order_action_sent"] is False, "TWS API readiness probe must not send order action")
    if not api_probe["ready_for_tws_api_funds_positions_query"]:
        require(api_probe["typed_blocker"]["blocker_id"] == "tws_api_readiness_missing", "TWS API readiness blocker drifted")

    socket_diagnostic = load(TWS_API_SOCKET_DIAGNOSTIC)
    require(socket_diagnostic["schema"] == "account-console.p019-tws-api-socket-diagnostic.v1", "TWS socket diagnostic schema drifted")
    require(socket_diagnostic["tws_process"]["present"] is True, "TWS socket diagnostic must see TWS process")
    require(socket_diagnostic["tws_process"]["window_title_ref"] == "U3028269_account_window", "TWS socket diagnostic account title drifted")
    require(socket_diagnostic["ibapi_available"] is True, "TWS socket diagnostic must keep ibapi available")
    require(socket_diagnostic["ibapi_runtime_ref"] == "output/runtime/python", "TWS socket diagnostic runtime ref drifted")
    require(socket_diagnostic["boundaries"]["tws_api_account_query_sent"] is False, "TWS socket diagnostic must not query account")
    require(socket_diagnostic["boundaries"]["funds_positions_values_recorded"] is False, "TWS socket diagnostic must not record values")
    if not socket_diagnostic["ready_for_tws_api_funds_positions_query"]:
        require(socket_diagnostic["typed_blocker"]["reasons"] == ["local_tws_api_socket_not_open"], "TWS socket diagnostic blocker reason drifted")

    firewall_diagnostic = load(WINDOWS_FIREWALL_TWS_API_DIAGNOSTIC)
    require(
        firewall_diagnostic["schema"] == "account-console.p019-windows-firewall-tws-api-diagnostic.v1",
        "Windows firewall TWS API diagnostic schema drifted",
    )
    require(firewall_diagnostic["account_id"] == "acct.ib.live.u3028269", "Windows firewall diagnostic account drifted")
    require(firewall_diagnostic["display_alias"] == "U3028269", "Windows firewall diagnostic alias drifted")
    require(firewall_diagnostic["diagnostic_kind"] == "windows_firewall_tws_api", "Windows firewall diagnostic kind drifted")
    require(firewall_diagnostic["tws_process"]["present"] is True, "Windows firewall diagnostic must see TWS process")
    require(
        firewall_diagnostic["tws_process"]["window_title_ref"] == "U3028269_account_window",
        "Windows firewall diagnostic title drifted",
    )
    diagnosis = firewall_diagnostic["diagnosis"]
    require(diagnosis["matching_allow_rules_present"] is True, "Windows firewall diagnostic must find allow rules")
    require(diagnosis["matching_block_rules_present"] is False, "Windows firewall diagnostic must not find block rules")
    if diagnosis["known_tws_api_ports_listening"] is True:
        require(diagnosis["firewall_is_primary_blocker"] is None, "Windows firewall ready listener state drifted")
        require(diagnosis["primary_blocker"] == "unknown", "Windows firewall ready primary blocker drifted")
        require(firewall_diagnostic["known_api_listeners"], "Windows firewall ready diagnostic listeners missing")
    else:
        require(diagnosis["firewall_is_primary_blocker"] is False, "Windows firewall must not be primary blocker")
        require(diagnosis["primary_blocker"] == "local_tws_api_socket_not_open", "Windows firewall primary blocker drifted")
        require(firewall_diagnostic["known_api_listeners"] == [], "Windows firewall diagnostic listeners must be empty")
    allow_ports = {str(row.get("LocalPort")) for row in firewall_diagnostic["matching_allow_rules"]}
    require({"7496", "7497", "4002"}.issubset(allow_ports), "Windows firewall TWS/Gateway allow ports missing")
    require(firewall_diagnostic["matching_block_rules"] == [], "Windows firewall block rules must be empty")
    require(
        firewall_diagnostic["boundaries"]["raw_secret_values_recorded"] is False,
        "Windows firewall diagnostic must not record secrets",
    )
    require(
        firewall_diagnostic["boundaries"]["raw_broker_endpoint_recorded"] is False,
        "Windows firewall diagnostic must not record raw endpoint",
    )
    require(
        firewall_diagnostic["boundaries"]["tws_api_account_query_sent"] is False,
        "Windows firewall diagnostic must not query account",
    )
    require(
        firewall_diagnostic["boundaries"]["funds_positions_values_recorded"] is False,
        "Windows firewall diagnostic must not record funds/positions values",
    )
    require(
        firewall_diagnostic["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "Windows firewall diagnostic must not use screenshots",
    )
    require(
        firewall_diagnostic["boundaries"]["order_action_sent"] is False,
        "Windows firewall diagnostic must not send order action",
    )

    config_diagnostic = load(TWS_API_CONFIG_DIAGNOSTIC)
    require(
        config_diagnostic["schema"] == "account-console.p019-tws-api-config-diagnostic.v1",
        "TWS API config diagnostic schema drifted",
    )
    require(config_diagnostic["account_id"] == "acct.ib.live.u3028269", "TWS API config diagnostic account drifted")
    require(config_diagnostic["display_alias"] == "U3028269", "TWS API config diagnostic alias drifted")
    require(config_diagnostic["diagnostic_kind"] == "tws_api_config", "TWS API config diagnostic kind drifted")
    require(config_diagnostic["tws_process"]["present"] is True, "TWS API config diagnostic must see TWS process")
    require(
        config_diagnostic["tws_process"]["window_title_ref"] == "U3028269_account_window",
        "TWS API config diagnostic title drifted",
    )
    require(config_diagnostic["candidate_config_count"] >= 1, "TWS API config diagnostic must find candidates")
    latest_config = config_diagnostic["latest_config_candidate"]
    require(latest_config["config_ref"].startswith("local-file-ref://"), "TWS API config must use local refs")
    require(latest_config["api_settings"]["socketClient"] == "false", "latest TWS config candidate must show socketClient=false")
    require(latest_config["api_settings"]["allowOnlyLocalhost"] == "true", "latest TWS config localhost setting drifted")
    require(latest_config["api_settings"]["port"] == "7497", "latest TWS config port drifted")
    require(
        any(item["api_settings"]["socketClient"] == "true" for item in config_diagnostic["config_candidates"]),
        "TWS API config diagnostic must keep historical enabled candidate evidence",
    )
    config_blocker = config_diagnostic.get("typed_blocker")
    if config_diagnostic.get("ready_for_tws_api_funds_positions_query") is True:
        require(config_blocker is None, "ready TWS API config diagnostic must not carry blocker")
        require(
            any(item["connectable"] for item in config_diagnostic["connect_port_refs"].values()),
            "ready TWS API config diagnostic needs connectable port ref",
        )
    else:
        require(config_blocker["blocker_id"] == "tws_api_readiness_missing", "TWS API config blocker id drifted")
        require(
            config_blocker["primary_blocker"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "TWS API config primary blocker drifted",
        )
        require(
            config_blocker["reasons"] == [
                "local_tws_api_socket_not_open",
                "latest_tws_config_candidate_socket_client_false",
            ],
            "TWS API config blocker reasons drifted",
        )
        require(
            not any(item["connectable"] for item in config_diagnostic["connect_port_refs"].values()),
            "TWS API config diagnostic must not have connectable port refs while blocked",
        )
    require(
        config_diagnostic["boundaries"]["raw_config_file_contents_recorded"] is False,
        "TWS API config diagnostic must not record raw config contents",
    )
    require(
        config_diagnostic["boundaries"]["raw_secret_values_recorded"] is False,
        "TWS API config diagnostic must not record secrets",
    )
    require(
        config_diagnostic["boundaries"]["raw_broker_endpoint_recorded"] is False,
        "TWS API config diagnostic must not record raw endpoint",
    )
    require(
        config_diagnostic["boundaries"]["tws_api_account_query_sent"] is False,
        "TWS API config diagnostic must not query account",
    )
    require(
        config_diagnostic["boundaries"]["funds_positions_values_recorded"] is False,
        "TWS API config diagnostic must not record funds/positions values",
    )
    require(
        config_diagnostic["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "TWS API config diagnostic must not use screenshots",
    )
    require(
        config_diagnostic["boundaries"]["order_action_sent"] is False,
        "TWS API config diagnostic must not send order action",
    )

    reinstall_decision = load(TWS_REINSTALL_DECISION)
    require(
        reinstall_decision["schema"] == "account-console.p019-tws-reinstall-decision.v1",
        "TWS reinstall decision schema drifted",
    )
    require(reinstall_decision["decision"] == "do_not_reinstall_yet", "TWS reinstall decision drifted")
    require(reinstall_decision["reinstall_recommended"] is False, "TWS reinstall must not be recommended yet")
    decision_ready = reinstall_decision["current_evidence"].get("ready_for_tws_api_funds_positions_query") is True
    if decision_ready:
        require(reinstall_decision["primary_next_action"] == "run_real_acceptance_closeout", "TWS reinstall ready next action drifted")
    else:
        require(
            reinstall_decision["primary_next_action"]
            == "enable_logged_in_tws_api_socket_then_restart_or_reconnect_and_rerun_pipeline",
            "TWS reinstall decision next action drifted",
        )
    decision_evidence = reinstall_decision["current_evidence"]
    require(decision_evidence["tws_process_present"] is True, "TWS reinstall decision must see TWS process")
    require(decision_evidence["firewall_allow_rules_present"] is True, "TWS reinstall decision must see allow rules")
    require(
        decision_evidence["firewall_enabled_block_rules_present"] is False,
        "TWS reinstall decision must not see firewall block rules",
    )
    require(
        decision_evidence["latest_config_socket_client"] == "false",
        "TWS reinstall decision must preserve socketClient=false evidence",
    )
    require(
        decision_evidence["known_api_ports_connectable"] is decision_ready,
        "TWS reinstall decision connectable evidence drifted",
    )
    require(
        reinstall_decision["boundaries"]["tws_reinstall_performed"] is False,
        "TWS reinstall decision must not perform reinstall",
    )
    require(
        reinstall_decision["boundaries"]["writes_outside_worktree"] is False,
        "TWS reinstall decision must not write outside worktree",
    )

    enable_change = load(TWS_API_ENABLE_CHANGE_REQUEST)
    require(
        enable_change["schema"] == "account-console.p019-tws-api-enable-change-request.v1",
        "TWS API enable change request schema drifted",
    )
    require(enable_change["account_id"] == "acct.ib.live.u3028269", "TWS API enable change request account drifted")
    require(
        enable_change["status"] in {"prepared_requires_operator_action", "already_ready_no_change_required"},
        "TWS API enable change request status drifted",
    )
    require(
        enable_change["target_config_ref"] == latest_config["config_ref"],
        "TWS API enable change request target config ref drifted",
    )
    require(
        enable_change["current_settings"]["socketClient"] == "false",
        "TWS API enable change request must preserve current socketClient=false",
    )
    if enable_change["status"] == "prepared_requires_operator_action":
        require(
            enable_change["requested_settings"]["socketClient"] == "true",
            "TWS API enable change request must request socketClient=true",
        )
    else:
        require(
            enable_change["requested_settings"]["socketClient"] == enable_change["current_settings"]["socketClient"],
            "ready TWS API enable change request must not request a change",
        )
    require(
        enable_change["requested_settings"]["allowOnlyLocalhost"] == "true",
        "TWS API enable change request must preserve localhost-only access",
    )
    require(
        enable_change["approval_required_for_writes_outside_worktree"] is True,
        "TWS API enable change request must require approval for external writes",
    )
    require(
        enable_change["writes_outside_worktree_performed"] is False,
        "TWS API enable change request must not write outside worktree",
    )
    require(
        enable_change["boundaries"]["tws_config_modified_by_this_script"] is False,
        "TWS API enable change request must not modify TWS config",
    )
    require(
        enable_change["boundaries"]["tws_api_account_query_sent"] is False,
        "TWS API enable change request must not query account",
    )

    ib_source_package = load(IB_U3028269_SOURCE_PACKAGE)
    require(ib_source_package["account_id"] == "acct.ib.live.u3028269", "IB source package account drifted")
    require(ib_source_package["source_kind"] == "ib_tws_observation", "IB source package source kind drifted")
    require(ib_source_package["source_health"]["api_transport"] == "ib_tws_api", "IB source package must use TWS API transport")
    if ib_source_package["source_health"]["state"] == "ready":
        require(ib_source_package["source_health"].get("blocker_id") is None, "ready IB source package must not carry blocker")
        require(ib_source_package["balances"], "ready IB source package must include API balances")
        require(ib_source_package["positions"], "ready IB source package must include API positions")
    else:
        require(ib_source_package["source_health"]["blocker_id"] == "tws_api_readiness_missing", "IB source package readiness blocker drifted")
        require(ib_source_package["balances"] == [], "blocked IB source package must not invent balances")
        require(ib_source_package["positions"] == [], "blocked IB source package must not invent positions")
    require(ib_source_package["boundaries"]["screenshot_used_for_funds_positions"] is False, "IB source package must not use screenshots for funds/positions")
    require(ib_source_package["boundaries"]["raw_secret_values_recorded"] is False, "IB source package must not record raw secrets")
    require(ib_source_package["boundaries"]["order_action_sent"] is False, "IB source package must not send order actions")

    wait_collect = load(TWS_API_WAIT_COLLECT_SUMMARY)
    require(
        wait_collect["schema"] == "account-console.p019-tws-api-wait-collect-summary.v1",
        "TWS API wait collect schema drifted",
    )
    require(wait_collect["account_id"] == "acct.ib.live.u3028269", "TWS API wait collect account drifted")
    require(wait_collect["display_alias"] == "U3028269", "TWS API wait collect alias drifted")
    require(wait_collect["status"] in {"blocked", "ready"}, "TWS API wait collect status drifted")
    require(wait_collect["attempt_count"] >= 1, "TWS API wait collect attempts missing")
    if wait_collect["status"] == "blocked":
        require(wait_collect["blocker_id"] == "tws_api_readiness_missing", "TWS API wait collect blocker drifted")
        require(wait_collect["pipeline_ran"] is False, "TWS API wait collect must not run pipeline before readiness")
        require(wait_collect["pipeline_step"] is None, "TWS API wait collect must not carry pipeline step while blocked")
        require(
            all(attempt["ready_for_tws_api_funds_positions_query"] is False for attempt in wait_collect["attempts"]),
            "TWS API wait collect blocked evidence cannot include ready attempt",
        )
    else:
        require(wait_collect["blocker_id"] is None, "ready TWS API wait collect must not carry blocker")
        require(wait_collect["pipeline_ran"] is True, "ready TWS API wait collect must run pipeline")
        require(wait_collect["pipeline_step"]["ok"] is True, "ready TWS API wait collect pipeline step must pass")
    require(
        wait_collect["boundaries"]["raw_secret_values_recorded"] is False,
        "TWS API wait collect must not record secrets",
    )
    require(
        wait_collect["boundaries"]["raw_broker_endpoint_recorded"] is False,
        "TWS API wait collect must not record raw endpoints",
    )
    require(
        wait_collect["boundaries"]["tws_api_account_query_sent_before_readiness"] is False,
        "TWS API wait collect must not query account before readiness",
    )
    require(
        wait_collect["boundaries"]["funds_positions_values_recorded_before_readiness"] is False,
        "TWS API wait collect must not record values before readiness",
    )
    require(
        wait_collect["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "TWS API wait collect must not use screenshots",
    )
    require(wait_collect["boundaries"]["order_action_sent"] is False, "TWS API wait collect must not send order action")

    real_closeout = load(REAL_ACCEPTANCE_CLOSEOUT)
    require(
        real_closeout["schema"] == "account-console.p019-u3028269-real-acceptance-closeout.v1",
        "real acceptance closeout schema drifted",
    )
    require(real_closeout["account_id"] == "acct.ib.live.u3028269", "real acceptance closeout account drifted")
    require(real_closeout["status"] in {"ready", "blocked"}, "real acceptance closeout status drifted")
    require(real_closeout["pipeline_summary_ref"].endswith("pipeline-summary.json"), "real acceptance closeout pipeline ref drifted")
    require(
        real_closeout["real_ui_parity_ref"].endswith("2026-06-20-p019-u3028269-real-ui-parity-evidence.json"),
        "real acceptance closeout UI parity ref drifted",
    )
    require(
        real_closeout["boundaries"]["synthetic_evidence_used_for_real_closeout"] is False,
        "real acceptance closeout must not use synthetic evidence",
    )
    require(
        real_closeout["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "real acceptance closeout must not use screenshots for funds/positions",
    )
    require(real_closeout["boundaries"]["order_action_sent"] is False, "real acceptance closeout must not send order action")
    if real_closeout["status"] == "blocked":
        require(real_closeout["blocker_id"] == "tws_api_readiness_missing", "blocked real acceptance closeout blocker drifted")
        require(real_closeout["real_ui_parity_verdict"] == "blocked", "blocked real acceptance closeout UI parity drifted")
    else:
        require(real_closeout["blocker_id"] is None, "ready real acceptance closeout must not carry blocker")
        require(real_closeout["pipeline_status"] == "ready", "ready real acceptance closeout needs ready pipeline")
        require(real_closeout["real_ui_parity_verdict"] == "pass", "ready real acceptance closeout needs UI pass")

    completion_audit = load(COMPLETION_AUDIT)
    require(completion_audit["schema"] == "account-console.p019-completion-audit.v1", "completion audit schema drifted")
    require(completion_audit["overall_status"] == "not_complete", "completion audit must remain not_complete")
    require(completion_audit["completion_must_not_be_claimed"] is True, "completion audit must block completion claim")
    require(completion_audit["primary_runtime_blocker"] in {"adr0005_not_accepted", "tws_api_readiness_missing"}, "completion audit blocker drifted")
    if completion_audit["primary_runtime_blocker"] == "tws_api_readiness_missing":
        require(
            completion_audit["primary_runtime_blocker_detail"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "completion audit blocker detail drifted",
        )
    require(completion_audit["raw_secret_values_recorded"] is False, "completion audit must not record secrets")
    require(
        completion_audit["screenshot_used_for_funds_positions"] is False,
        "completion audit must not allow screenshot-backed funds/positions",
    )
    require(completion_audit["order_action_sent"] is False, "completion audit must not allow order action")
    require(
        completion_audit["synthetic_ready_contract_is_real_account_truth"] is False,
        "completion audit must keep synthetic evidence out of real truth",
    )
    require(
        {item["id"] for item in completion_audit["acceptance_requirements"]} == {f"A{idx}" for idx in range(1, 15)},
        "completion audit must cover A1-A14",
    )
    require(
        {item["id"] for item in completion_audit["required_before_implementation_closeout"]}
        == {f"C{idx}" for idx in range(1, 11)},
        "completion audit must cover C1-C10",
    )

    profile = load(PROFILE)
    require(profile["mode"] == "read_only_observation", "profile must remain read-only observation")
    require(profile["adr_gate"]["decision_status"] == "proposed", "profile must remain pre-acceptance")
    require(profile["adr_gate"]["direct_session_allowed"] is False, "profile must not allow direct session")
    require(profile["adr_gate"]["blocker_id"] == "adr0005_not_accepted", "profile ADR blocker drifted")
    require(profile["config_ref"].startswith("owner-config-ref://"), "profile config must be owner ref")
    require(profile["secret_ref"].startswith("owner-secret-ref://"), "profile secret must be owner ref")
    require(profile["raw_secret_values_recorded"] is False, "profile must not record raw secrets")
    require(profile["command"]["enabled"] is False, "profile command must remain disabled")
    require(profile["command"]["allowed_actions"] == [], "profile allowed actions must remain empty")
    require(profile["projection_boundary"] == "account_mirror", "profile must project through Account Mirror")

    store_complete = load(STORE_COMPLETE)
    store_gap = load(STORE_GAP)
    require(store_complete["replay_state"]["state"] == "complete", "complete reload fixture state drifted")
    require(store_complete["reload_proof"]["parity_status"] == "passed", "complete reload parity drifted")
    require(store_complete["reload_proof"]["records_loaded_from_live_memory"] == 0, "complete reload must not use live memory")
    require(store_gap["replay_state"]["state"] == "blocked", "gap fixture state drifted")
    require(store_gap["reload_proof"]["parity_status"] == "blocked", "gap fixture parity must remain blocked")

    session_conflict = load(SESSION_CONFLICT)
    require(session_conflict["fail_closed"] is True, "session conflict policy must fail closed")
    require(session_conflict["unknown_owner_policy"] == "blocked", "unknown owner policy must stay blocked")
    require(session_conflict["direct_session_allowed"] is False, "session conflict fixture must not allow direct session")
    cases = {case["case_id"]: case for case in session_conflict["evaluations"]}
    for case_id in [
        "unknown_owner",
        "same_client_id_conflict",
        "active_nautilus_trading_session",
        "broker_connection_slot_conflict",
    ]:
        require(case_id in cases, f"session conflict missing case {case_id}")
        require(cases[case_id]["decision"] == "blocked", f"{case_id} must stay blocked")
        require(cases[case_id]["session_allowed"] is False, f"{case_id} must not allow session")

    freshness_sequence = load(FRESHNESS_SEQUENCE)
    require(
        freshness_sequence["cursor"]["continuity"] == "gap",
        "freshness sequence fixture must keep gapped cursor state",
    )
    require(
        freshness_sequence["claim_guard"]["may_claim_realtime"] is False,
        "freshness sequence fixture must not claim realtime",
    )
    require(
        freshness_sequence["claim_guard"]["may_claim_complete_history"] is False,
        "freshness sequence fixture must not claim complete history",
    )
    require(
        freshness_sequence["claim_guard"]["may_claim_trading_readiness"] is False,
        "freshness sequence fixture must not claim trading readiness",
    )
    require(freshness_sequence["claim_guard"]["blockers"], "freshness sequence fixture must carry blockers")

    cross_broker = load(CROSS_BROKER_MATRIX)
    expected_brokers = {"ib_tws", "ctp", "stock_broker", "cqg", "tt"}
    rows = {row["broker_family"]: row for row in cross_broker["broker_rows"]}
    require(set(rows) == expected_brokers, "cross-broker matrix must cover all ADR-0005 broker families")
    for broker_family, row in rows.items():
        require(row["profile_contract"] == "broker_observation_profile.v1", f"{broker_family} profile contract forked")
        require(row["report_contract"] == "broker_observation_report_batch.v1", f"{broker_family} report contract forked")
        require(row["store_contract"] == "broker_observation_store_snapshot.v1", f"{broker_family} store contract forked")
        require(
            row["freshness_contract"] == "broker_observation_freshness_sequence_checkpoint.v1",
            f"{broker_family} freshness contract forked",
        )
        require(row["projection_boundary"] == "account_mirror", f"{broker_family} must stay behind Account Mirror")
        require(row["command_allowed"] is False, f"{broker_family} must not allow command from observation")
        require(row["raw_secret_values_recorded"] is False, f"{broker_family} must not record raw secrets")

    report_mapping = load(REPORT_MAPPING)
    mapping_types = {mapping["target_report_type"] for mapping in report_mapping["mappings"]}
    require(mapping_types == {"OrderStatusReport", "FillReport"}, "report mapping must cover order status and fill reports")
    require(
        report_mapping["raw_payload_policy"]["browser_may_parse_raw_payload"] is False,
        "browser must not parse raw payload from report mapping",
    )
    for mapping in report_mapping["mappings"]:
        require(mapping["raw_payload_is_canonical"] is False, "raw payload must not be canonical in report mapping")
        target_fields = {item["target_field"] for item in mapping["field_map"]}
        if mapping["target_report_type"] == "OrderStatusReport":
            require("order_status" in target_fields, "OrderStatusReport mapping missing order_status")
            require("venue_order_id" in target_fields, "OrderStatusReport mapping missing venue_order_id")
        if mapping["target_report_type"] == "FillReport":
            for field in ["trade_id", "last_px", "last_qty"]:
                require(field in target_fields, f"FillReport mapping missing {field}")

    lane_manifest = load(LANE_MANIFEST)
    require(lane_manifest["status"] == "pre_acceptance_blocked", "lane manifest must remain blocked")
    require(lane_manifest["blocker_id"] == "adr0005_not_accepted", "lane manifest blocker drifted")
    require(lane_manifest["raw_secret_values_recorded"] is False, "lane manifest must not record raw secrets")
    lanes = {lane["lane_id"]: lane for lane in lane_manifest["lanes"]}
    require(
        lanes["p018-owner-source-package"]["may_satisfy_p019_direct_observation_acceptance"] is False,
        "P018 source package lane must not close P019 direct observation acceptance",
    )
    require(
        lanes["p019-adr0005-governed-observation-session"]["may_satisfy_p018_owner_source_package_acceptance"] is False,
        "P019 blocked observation lane must not close P018 source package acceptance",
    )
    require(
        lane_manifest["cross_lane_rules"]["same_artifact_must_not_close_both_lanes_without_mapping"] is True,
        "lane manifest must require explicit mapping before cross-lane reuse",
    )

    print("P019_BROKER_OBSERVATION_FOUNDATION_OK: status=proposed pre_acceptance=partial blockers=typed")


if __name__ == "__main__":
    main()
