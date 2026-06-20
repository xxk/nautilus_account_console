from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TWS_API_READINESS_DIR = ROOT / "output" / "debug" / "p019-tws-api-readiness"
ACCOUNT_CAPABILITY_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269"

SOCKET_DIAGNOSTIC = TWS_API_READINESS_DIR / "tws-api-socket-diagnostic.json"
FIREWALL_DIAGNOSTIC = TWS_API_READINESS_DIR / "windows-firewall-tws-api-diagnostic.json"
CONFIG_DIAGNOSTIC = TWS_API_READINESS_DIR / "tws-api-config-diagnostic.json"
REINSTALL_DECISION = TWS_API_READINESS_DIR / "tws-reinstall-decision.json"
ENABLE_CHANGE_REQUEST = TWS_API_READINESS_DIR / "tws-api-enable-change-request.json"
WAIT_COLLECT_SUMMARY = ACCOUNT_CAPABILITY_DIR / "wait-collect-summary.json"
PIPELINE_SUMMARY = ACCOUNT_CAPABILITY_DIR / "pipeline-summary.json"
REAL_ACCEPTANCE_CLOSEOUT = ACCOUNT_CAPABILITY_DIR / "real-acceptance-closeout.json"


class RuntimeEvidenceFreshnessError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeEvidenceFreshnessError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str, label: str) -> datetime:
    require(value.endswith("Z"), f"{label} must be UTC Z timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def require_false_boundaries(data: dict[str, Any], keys: list[str], label: str) -> None:
    boundaries = data.get("boundaries", {})
    for key in keys:
        require(boundaries.get(key) is False, f"{label} boundary drifted: {key}")


def require_observed_after(
    actual: datetime,
    expected_minimum: datetime,
    actual_label: str,
    expected_label: str,
) -> None:
    require(actual >= expected_minimum, f"{actual_label} is older than {expected_label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate freshness and status alignment for P019 runtime evidence.")
    parser.add_argument("--socket-diagnostic", type=Path, default=SOCKET_DIAGNOSTIC)
    parser.add_argument("--firewall-diagnostic", type=Path, default=FIREWALL_DIAGNOSTIC)
    parser.add_argument("--config-diagnostic", type=Path, default=CONFIG_DIAGNOSTIC)
    parser.add_argument("--reinstall-decision", type=Path, default=REINSTALL_DECISION)
    parser.add_argument("--enable-change-request", type=Path, default=ENABLE_CHANGE_REQUEST)
    parser.add_argument("--wait-collect-summary", type=Path, default=WAIT_COLLECT_SUMMARY)
    parser.add_argument("--pipeline-summary", type=Path, default=PIPELINE_SUMMARY)
    parser.add_argument("--real-acceptance-closeout", type=Path, default=REAL_ACCEPTANCE_CLOSEOUT)
    args = parser.parse_args()

    socket = load(args.socket_diagnostic)
    firewall = load(args.firewall_diagnostic)
    config = load(args.config_diagnostic)
    reinstall = load(args.reinstall_decision)
    enable_change = load(args.enable_change_request)
    wait_collect = load(args.wait_collect_summary)
    pipeline = load(args.pipeline_summary)
    closeout = load(args.real_acceptance_closeout)

    require(socket["schema"] == "account-console.p019-tws-api-socket-diagnostic.v1", "socket diagnostic schema drifted")
    require(
        firewall["schema"] == "account-console.p019-windows-firewall-tws-api-diagnostic.v1",
        "firewall diagnostic schema drifted",
    )
    require(config["schema"] == "account-console.p019-tws-api-config-diagnostic.v1", "config diagnostic schema drifted")
    require(reinstall["schema"] == "account-console.p019-tws-reinstall-decision.v1", "reinstall decision schema drifted")
    require(
        enable_change["schema"] == "account-console.p019-tws-api-enable-change-request.v1",
        "enable change request schema drifted",
    )
    require(
        wait_collect["schema"] == "account-console.p019-tws-api-wait-collect-summary.v1",
        "wait collect summary schema drifted",
    )
    require(
        pipeline["schema"] == "account-console.p019-ib-u3028269-tws-api-pipeline-summary.v1",
        "pipeline summary schema drifted",
    )
    require(
        closeout["schema"] == "account-console.p019-u3028269-real-acceptance-closeout.v1",
        "real acceptance closeout schema drifted",
    )

    socket_at = parse_time(socket["observed_at"], "socket observed_at")
    firewall_at = parse_time(firewall["observed_at"], "firewall observed_at")
    config_at = parse_time(config["observed_at"], "config observed_at")
    latest_diagnostic_at = max(socket_at, firewall_at, config_at)
    reinstall_at = parse_time(reinstall["observed_at"], "reinstall observed_at")
    enable_change_at = parse_time(enable_change["prepared_at"], "enable change prepared_at")
    wait_started = parse_time(wait_collect["started_at"], "wait collect started_at")
    wait_completed = parse_time(wait_collect["completed_at"], "wait collect completed_at")
    closeout_started = parse_time(closeout["started_at"], "closeout started_at")
    closeout_completed = parse_time(closeout["completed_at"], "closeout completed_at")
    closeout_status = closeout["status"]
    require(closeout_status in {"blocked", "ready"}, "real closeout status drifted")

    require_observed_after(closeout_completed, latest_diagnostic_at, "real acceptance closeout", "latest diagnostic")
    require(wait_completed >= wait_started, "wait collect completed before start")
    require(closeout_completed >= closeout_started, "real acceptance closeout completed before start")

    require(socket["tws_process"]["present"] is True, "socket diagnostic must see local TWS process")

    require(firewall["tws_process"]["present"] is True, "firewall diagnostic must see local TWS process")
    require(firewall["diagnosis"]["matching_allow_rules_present"] is True, "firewall allow rules missing")
    require(firewall["diagnosis"]["matching_block_rules_present"] is False, "firewall block rule drifted")
    if firewall["diagnosis"]["known_tws_api_ports_listening"] is True:
        require(firewall["diagnosis"]["firewall_is_primary_blocker"] is None, "ready firewall diagnostic drifted")
        require(firewall["diagnosis"]["primary_blocker"] == "unknown", "ready firewall blocker drifted")
    else:
        require(firewall["diagnosis"]["firewall_is_primary_blocker"] is False, "firewall became primary blocker")
        require(firewall["diagnosis"]["primary_blocker"] == "local_tws_api_socket_not_open", "firewall blocker drifted")

    latest_config = config["latest_config_candidate"]
    require(latest_config["api_settings"]["allowOnlyLocalhost"] == "true", "localhost-only evidence drifted")
    require(latest_config["api_settings"]["port"] in {"7496", "7497"}, "latest port evidence drifted")

    require(reinstall["decision"] == "do_not_reinstall_yet", "reinstall decision drifted")
    require(reinstall["reinstall_recommended"] is False, "reinstall recommendation drifted")

    require(
        enable_change["status"] in {"prepared_requires_operator_action", "already_ready_no_change_required"},
        "enable change request status drifted",
    )
    require(enable_change["requested_settings"]["allowOnlyLocalhost"] == "true", "enable change localhost boundary drifted")
    require(enable_change["writes_outside_worktree_performed"] is False, "enable change wrote outside worktree")

    require(wait_collect["attempt_count"] >= 1, "wait collect missing attempts")

    if closeout_status == "blocked":
        require_observed_after(reinstall_at, latest_diagnostic_at, "reinstall decision", "latest diagnostic")
        require_observed_after(enable_change_at, config_at, "enable change request", "config diagnostic")
        require_observed_after(wait_started, enable_change_at, "wait collect", "enable change request")
        require_observed_after(closeout_started, wait_started, "real acceptance closeout", "wait collect")
        require(socket["ready_for_tws_api_funds_positions_query"] is False, "blocked socket readiness drifted")
        require(socket["typed_blocker"]["blocker_id"] == "tws_api_readiness_missing", "blocked socket blocker drifted")
        require(
            any(
                reason in socket["typed_blocker"]["reasons"]
                for reason in ["local_tws_api_socket_not_open", "local_tws_api_handshake_not_ok"]
            ),
            "blocked socket reason drifted",
        )
        require(
            not any(ref["status"] == "handshake_ok" for ref in socket["handshake_port_refs"].values()),
            "blocked socket diagnostic unexpectedly has handshake_ok",
        )
        require(config["ready_for_tws_api_funds_positions_query"] is False, "blocked config readiness drifted")
        require(latest_config["api_settings"]["socketClient"] == "false", "blocked latest socketClient evidence drifted")
        require(latest_config["api_socket_enabled"] is False, "blocked latest API socket evidence drifted")
        require(
            config["typed_blocker"]["primary_blocker"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "blocked config primary blocker drifted",
        )
        require(
            "latest_tws_config_candidate_socket_client_false" in config["typed_blocker"]["reasons"],
            "blocked config blocker reason drifted",
        )
        require(
            reinstall["primary_next_action"] == "enable_logged_in_tws_api_socket_then_restart_or_reconnect_and_rerun_pipeline",
            "blocked reinstall next action drifted",
        )
        require(reinstall["current_evidence"]["latest_config_socket_client"] == "false", "blocked reinstall config drifted")
        require(reinstall["current_evidence"]["known_api_ports_connectable"] is False, "blocked reinstall socket drifted")
        require(enable_change["status"] == "prepared_requires_operator_action", "blocked enable change status drifted")
        require(enable_change["current_settings"]["socketClient"] == "false", "blocked enable current socketClient drifted")
        require(enable_change["requested_settings"]["socketClient"] == "true", "blocked enable requested socketClient drifted")
        require(wait_collect["status"] == "blocked", "blocked wait collect status drifted")
        require(wait_collect["blocker_id"] == "tws_api_readiness_missing", "blocked wait collect blocker drifted")
        require(wait_collect["pipeline_ran"] is False, "blocked wait collect must not run pipeline before readiness")
        require(pipeline["status"] == "blocked", "blocked pipeline status drifted")
        require(pipeline["blocker_id"] == "tws_api_readiness_missing", "blocked pipeline blocker drifted")
        require(pipeline["ready_for_tws_api_funds_positions_query"] is False, "blocked pipeline readiness drifted")
        require(pipeline["account_summary_success"] is False, "blocked pipeline account summary drifted")
        require(pipeline["positions_success"] is False, "blocked pipeline positions drifted")
        require(pipeline["source_package_state"] == "blocked", "blocked pipeline source package drifted")
        require(closeout["blocker_id"] == "tws_api_readiness_missing", "blocked real closeout blocker drifted")
        require(closeout["real_ui_parity_verdict"] == "blocked", "blocked real closeout UI parity drifted")
        require(closeout["account_summary_success"] is False, "blocked real closeout account summary drifted")
        require(closeout["positions_success"] is False, "blocked real closeout positions drifted")
        require(closeout["source_package_state"] == "blocked", "blocked real closeout source package drifted")
    else:
        require(socket["ready_for_tws_api_funds_positions_query"] is True, "ready socket readiness drifted")
        require(socket["typed_blocker"] is None, "ready socket diagnostic must not carry blocker")
        require(
            any(ref["status"] == "handshake_ok" for ref in socket["handshake_port_refs"].values()),
            "ready socket diagnostic needs IB API handshake_ok",
        )
        require(config["ready_for_tws_api_funds_positions_query"] is True, "ready config readiness drifted")
        require(config["typed_blocker"] is None, "ready config diagnostic must not carry blocker")
        require(reinstall["primary_next_action"] == "run_real_acceptance_closeout", "ready reinstall next action drifted")
        require(reinstall["current_evidence"]["known_api_ports_connectable"] is True, "ready reinstall socket drifted")
        require(enable_change["status"] == "already_ready_no_change_required", "ready enable status drifted")
        require(wait_collect["status"] == "ready", "ready wait collect status drifted")
        require(wait_collect["blocker_id"] is None, "ready wait collect must not carry blocker")
        require(wait_collect["pipeline_ran"] is True, "ready wait collect must run pipeline")
        require(pipeline["status"] == "ready", "ready pipeline status drifted")
        require(pipeline["blocker_id"] is None, "ready pipeline must not carry blocker")
        require(pipeline["ready_for_tws_api_funds_positions_query"] is True, "ready pipeline readiness drifted")
        require(pipeline["account_summary_success"] is True, "ready pipeline account summary drifted")
        require(pipeline["positions_success"] is True, "ready pipeline positions drifted")
        require(pipeline["source_package_state"] == "ready", "ready pipeline source package drifted")
        require(closeout["blocker_id"] is None, "ready real closeout must not carry blocker")
        require(closeout["real_ui_parity_verdict"] == "pass", "ready real closeout UI parity drifted")
        require(closeout["account_summary_success"] is True, "ready real closeout account summary drifted")
        require(closeout["positions_success"] is True, "ready real closeout positions drifted")
        require(closeout["source_package_state"] == "ready", "ready real closeout source package drifted")

    common_boundary_keys = [
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "funds_positions_values_recorded",
        "screenshot_used_for_funds_positions",
        "order_action_sent",
    ]
    require_false_boundaries(socket, common_boundary_keys, "socket diagnostic")
    require_false_boundaries(firewall, common_boundary_keys, "firewall diagnostic")
    require_false_boundaries(config, ["raw_config_file_contents_recorded", *common_boundary_keys], "config diagnostic")
    require_false_boundaries(
        reinstall,
        [
            "writes_outside_worktree",
            "raw_secret_values_recorded",
            "raw_broker_endpoint_recorded",
            "raw_config_file_contents_recorded",
            "tws_reinstall_performed",
            "tws_api_account_query_sent",
            "funds_positions_values_recorded",
            "screenshot_used_for_funds_positions",
            "order_action_sent",
        ],
        "reinstall decision",
    )
    require_false_boundaries(
        enable_change,
        [
            "raw_config_file_contents_recorded",
            "raw_secret_values_recorded",
            "raw_broker_endpoint_recorded",
            "tws_config_modified_by_this_script",
            "tws_reinstall_performed",
            "tws_api_account_query_sent",
            "funds_positions_values_recorded",
            "screenshot_used_for_funds_positions",
            "order_action_sent",
        ],
        "enable change request",
    )
    require_false_boundaries(
        wait_collect,
        [
            "raw_secret_values_recorded",
            "raw_broker_endpoint_recorded",
            "tws_api_account_query_sent_before_readiness",
            "funds_positions_values_recorded_before_readiness",
            "screenshot_used_for_funds_positions",
            "order_action_sent",
        ],
        "wait collect",
    )
    require_false_boundaries(
        pipeline,
        [
            "raw_secret_values_recorded",
            "raw_broker_endpoint_recorded",
            "screenshot_used_for_funds_positions",
            "order_action_sent",
        ],
        "pipeline summary",
    )
    require_false_boundaries(
        closeout,
        [
            "raw_secret_values_recorded",
            "raw_broker_endpoint_recorded",
            "screenshot_used_for_funds_positions",
            "order_action_sent",
            "synthetic_evidence_used_for_real_closeout",
        ],
        "real closeout",
    )

    print(f"P019_RUNTIME_EVIDENCE_FRESHNESS_OK: status={closeout_status} evidence=fresh")


if __name__ == "__main__":
    main()
