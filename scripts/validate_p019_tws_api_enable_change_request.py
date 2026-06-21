from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-enable-change-request.json"
RUNBOOK = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "tws-api-runtime-recovery-runbook.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class EnableChangeRequestError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EnableChangeRequestError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk_values(item))
    return values


def main() -> None:
    payload = load(REQUEST)
    runbook = read(RUNBOOK)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-tws-api-enable-change-request.v1", "schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["status"] in {"prepared_requires_operator_action", "already_ready_no_change_required"}, "status mismatch")
    require(payload["change_owner"] == "local_tws_operator", "change owner mismatch")
    require(payload["target_config_ref"].startswith("local-file-ref://C:/Jts/"), "target config ref mismatch")

    current = payload["current_settings"]
    requested = payload["requested_settings"]
    already_ready = payload["status"] == "already_ready_no_change_required"
    if already_ready:
        require(requested["socketClient"] == current["socketClient"], "ready request should not change socketClient")
    else:
        require(current["socketClient"] == "false", "current socketClient should reflect blocker")
        require(current["api_socket_enabled"] is False, "current API socket should be disabled")
        require(requested["socketClient"] == "true", "requested socketClient must enable API")
    require(requested["allowOnlyLocalhost"] == "true", "requested access should remain localhost-only")
    require(requested["port"] in {"7496", "7497"}, "requested port should be a TWS default")

    require(payload["approval_required_for_writes_outside_worktree"] is True, "external write approval gate missing")
    require(payload["writes_outside_worktree_performed"] is False, "script must not write outside worktree")
    require(payload["reinstall_decision"]["current_decision"] == "do_not_reinstall_yet", "reinstall decision drifted")
    require(payload["reinstall_decision"]["reinstall_recommended"] is False, "reinstall must not be recommended")

    for command in [
        "python scripts/diagnose_p019_tws_api_config.py",
        "python scripts/probe_p019_tws_api_readiness.py",
        "python scripts/run_p019_u3028269_real_acceptance_closeout.py --wait-timeout-seconds 120 --wait-interval-seconds 5",
        "python scripts/validate_p019_u3028269_real_acceptance_closeout.py",
    ]:
        require(command in payload["post_change_verification_commands"], f"missing post-change command {command}")

    boundaries = payload["boundaries"]
    require(boundaries["raw_config_file_contents_recorded"] is False, "raw config contents must not be recorded")
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["tws_config_modified_by_this_script"] is False, "script must not modify TWS config")
    require(boundaries["tws_reinstall_performed"] is False, "script must not reinstall TWS")
    require(boundaries["tws_api_account_query_sent"] is False, "change request must not query account")
    require(boundaries["funds_positions_values_recorded"] is False, "change request must not record values")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not be funds truth")
    require(boundaries["order_action_sent"] is False, "change request must not send order action")

    forbidden_fragments = ["password=", "auth_code=", "api_key=", "secret=", "<TWS", "<tws", "127.0.0.1:"]
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in forbidden_fragments if fragment.lower() in lowered]
            require(not hits, f"change request contains forbidden raw value fragment {hits}")

    for term in [
        "prepare_p019_tws_api_enable_change_request.py",
        "validate_p019_tws_api_enable_change_request.py",
        "P019_TWS_API_ENABLE_CHANGE_REQUEST_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")
    require("Reinstall Decision Gate" in runbook, "runbook must keep reinstall gate")

    status_label = "already_ready" if already_ready else "prepared"
    print(f"P019_TWS_API_ENABLE_CHANGE_REQUEST_OK: status={status_label} target=socketClient_true")


if __name__ == "__main__":
    main()
