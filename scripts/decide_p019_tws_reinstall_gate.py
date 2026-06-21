from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEBUG_DIR = ROOT / "output" / "debug" / "p019-tws-api-readiness"
SOCKET_DIAGNOSTIC = DEBUG_DIR / "tws-api-socket-diagnostic.json"
FIREWALL_DIAGNOSTIC = DEBUG_DIR / "windows-firewall-tws-api-diagnostic.json"
CONFIG_DIAGNOSTIC = DEBUG_DIR / "tws-api-config-diagnostic.json"
OUTPUT = DEBUG_DIR / "tws-reinstall-decision.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    socket_payload = load(SOCKET_DIAGNOSTIC)
    firewall_payload = load(FIREWALL_DIAGNOSTIC)
    config_payload = load(CONFIG_DIAGNOSTIC)

    latest_config = config_payload["latest_config_candidate"]
    latest_api_settings = latest_config["api_settings"]
    allow_rules_present = bool(firewall_payload.get("matching_allow_rules"))
    block_rules_present = bool(firewall_payload.get("matching_block_rules"))

    api_socket_enabled = latest_config.get("api_socket_enabled") is True
    known_ports_connectable = any(
        item.get("connectable") is True for item in config_payload.get("connect_port_refs", {}).values()
    )
    tws_present = socket_payload.get("tws_process", {}).get("present") is True
    ready_for_query = (
        socket_payload.get("ready_for_tws_api_funds_positions_query") is True
        or config_payload.get("ready_for_tws_api_funds_positions_query") is True
        or known_ports_connectable
    )
    config_primary_blocker = (
        config_payload.get("typed_blocker", {}).get("primary_blocker")
        if config_payload.get("typed_blocker")
        else None
    )

    reinstall_preconditions = {
        "api_socket_enabled_in_logged_in_tws": api_socket_enabled,
        "tws_restarted_after_api_setting_change": False,
        "latest_config_socket_client_false_cleared": latest_api_settings.get("socketClient") != "false",
        "known_api_port_still_not_listening_after_enable_and_restart": not known_ports_connectable,
        "firewall_allow_rules_present": allow_rules_present,
        "firewall_enabled_block_rules_absent": not block_rules_present,
        "operator_approved_exact_path_reason_impact": False,
    }
    unmet = [
        name
        for name, value in reinstall_preconditions.items()
        if value is not True and name != "known_api_port_still_not_listening_after_enable_and_restart"
    ]
    if reinstall_preconditions["known_api_port_still_not_listening_after_enable_and_restart"] is True:
        unmet.append("known_api_port_still_not_listening_after_enable_and_restart")

    decision = {
        "schema": "account-console.p019-tws-reinstall-decision.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "observed_at": utc_now(),
        "decision": "do_not_reinstall_yet",
        "reinstall_recommended": False,
        "primary_next_action": (
            "run_real_acceptance_closeout"
            if ready_for_query
            else "enable_logged_in_tws_api_socket_then_restart_or_reconnect_and_rerun_pipeline"
        ),
        "current_evidence": {
            "tws_process_present": tws_present,
            "firewall_allow_rules_present": allow_rules_present,
            "firewall_enabled_block_rules_present": block_rules_present,
            "latest_config_ref": latest_config["config_ref"],
            "latest_config_socket_client": latest_api_settings.get("socketClient"),
            "latest_config_allow_only_localhost": latest_api_settings.get("allowOnlyLocalhost"),
            "latest_config_port": latest_api_settings.get("port"),
            "latest_config_api_socket_enabled": api_socket_enabled,
            "known_api_ports_connectable": known_ports_connectable,
            "config_primary_blocker": config_primary_blocker,
            "ready_for_tws_api_funds_positions_query": ready_for_query,
        },
        "reinstall_preconditions": reinstall_preconditions,
        "unmet_reinstall_preconditions": unmet,
        "required_before_real_funds_positions": [
            "ready_for_tws_api_funds_positions_query=true",
            "readonly_tws_api_account_summary_success=true",
            "readonly_tws_api_positions_success=true",
            "source_package_state=ready",
            "account_mirror_projection_from_real_source_package",
            "ui_parity_against_same_slice_tws_api_source",
        ],
        "boundaries": {
            "writes_outside_worktree": False,
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "raw_config_file_contents_recorded": False,
            "tws_reinstall_performed": False,
            "tws_api_account_query_sent": False,
            "funds_positions_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print(json.dumps({"status": decision["decision"], "output": str(OUTPUT)}))


if __name__ == "__main__":
    main()
