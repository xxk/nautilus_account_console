from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
REINSTALL_DECISION = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-reinstall-decision.json"
OUTPUT = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-enable-change-request.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def main() -> None:
    config = load(CONFIG_DIAGNOSTIC)
    reinstall = load(REINSTALL_DECISION)
    latest = config["latest_config_candidate"]
    current_settings = latest["api_settings"]
    api_ready = config.get("ready_for_tws_api_funds_positions_query") is True
    api_socket_enabled = latest.get("api_socket_enabled") is True
    needs_operator_action = not api_ready

    payload = {
        "schema": "account-console.p019-tws-api-enable-change-request.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "prepared_at": now(),
        "status": "prepared_requires_operator_action" if needs_operator_action else "already_ready_no_change_required",
        "purpose": "enable_logged_in_tws_api_socket_for_readonly_funds_positions_collection",
        "change_owner": "local_tws_operator",
        "current_evidence_refs": {
            "config_diagnostic": source_ref(CONFIG_DIAGNOSTIC),
            "reinstall_decision": source_ref(REINSTALL_DECISION),
        },
        "target_config_ref": latest["config_ref"],
        "current_settings": {
            "socketClient": current_settings.get("socketClient"),
            "allowOnlyLocalhost": current_settings.get("allowOnlyLocalhost"),
            "port": current_settings.get("port"),
            "api_socket_enabled": latest.get("api_socket_enabled"),
        },
        "requested_settings": {
            "socketClient": "true" if needs_operator_action else current_settings.get("socketClient"),
            "allowOnlyLocalhost": "true",
            "port": current_settings.get("port") or "7497",
        },
        "operator_steps": (
            [
                "Open the already logged-in TWS Global Configuration API settings.",
                "Enable socket clients / TWS API socket for the U3028269 session.",
                "Keep localhost-only access enabled unless an owner-approved remote access policy exists.",
                "Confirm or set the API port to the recorded requested port.",
                "Restart or reconnect TWS if the API setting does not take effect in the running process.",
                "Rerun the P019 real acceptance closeout runner.",
            ]
            if needs_operator_action
            else [
                "No TWS API socket enable change is required for the current evidence.",
                "Run the P019 real acceptance closeout runner to collect read-only funds and positions.",
            ]
        ),
        "expected_effect": {
            "latest_config_socket_client_false_cleared": True,
            "known_api_port_listening": True,
            "ready_for_tws_api_funds_positions_query": True,
            "account_summary_positions_collection_allowed_after_readiness": True,
        },
        "post_change_verification_commands": [
            "python scripts/diagnose_p019_tws_api_config.py",
            "python scripts/validate_p019_tws_api_config_diagnostic.py",
            "python scripts/probe_p019_tws_api_readiness.py",
            "python scripts/validate_p019_tws_api_readiness_probe.py",
            "python scripts/run_p019_u3028269_real_acceptance_closeout.py --wait-timeout-seconds 120 --wait-interval-seconds 5",
            "python scripts/validate_p019_u3028269_real_acceptance_closeout.py",
        ],
        "reinstall_decision": {
            "current_decision": reinstall["decision"],
            "reinstall_recommended": reinstall["reinstall_recommended"],
            "primary_next_action": reinstall["primary_next_action"],
        },
        "approval_required_for_writes_outside_worktree": True,
        "writes_outside_worktree_performed": False,
        "boundaries": {
            "raw_config_file_contents_recorded": False,
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "tws_config_modified_by_this_script": False,
            "tws_reinstall_performed": False,
            "tws_api_account_query_sent": False,
            "funds_positions_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
    }
    if api_socket_enabled:
        payload["purpose"] = "confirm_logged_in_tws_api_socket_ready_for_readonly_funds_positions_collection"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
