from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "windows-firewall-tws-api-diagnostic.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class FirewallDiagnosticError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FirewallDiagnosticError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(DIAGNOSTIC)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-windows-firewall-tws-api-diagnostic.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["diagnostic_kind"] == "windows_firewall_tws_api", "diagnostic kind mismatch")
    tws_present = payload["tws_process"]["present"] is True
    if tws_present:
        require(payload["tws_process"]["window_title_ref"] == "U3028269_account_window", "TWS window ref mismatch")

    diagnosis = payload["diagnosis"]
    require(diagnosis["matching_allow_rules_present"] is True, "expected matching allow rules")
    require(diagnosis["matching_block_rules_present"] is False, "must not have matching enabled block rules")
    if diagnosis["known_tws_api_ports_listening"] is True:
        require(tws_present, "listener-ready firewall diagnostic must see TWS process")
        require(diagnosis["firewall_is_primary_blocker"] is None, "firewall primary blocker must be unknown after socket opens")
        require(diagnosis["primary_blocker"] == "unknown", "ready-listener primary blocker mismatch")
        require(payload["known_api_listeners"], "known API listener rows are required after socket opens")
    else:
        require(diagnosis["firewall_is_primary_blocker"] is False, "firewall must not be primary blocker when no socket listens")
        require(diagnosis["primary_blocker"] == "local_tws_api_socket_not_open", "primary blocker mismatch")
        require(payload["known_api_listeners"] == [], "known API listener rows must be empty when no socket listens")

    allow_ports = {str(row.get("LocalPort")) for row in payload["matching_allow_rules"]}
    require({"7496", "7497", "4002"}.issubset(allow_ports), "expected TWS/Gateway allow ports missing")
    require(payload["matching_block_rules"] == [], "matching block rules must be empty")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["tws_api_account_query_sent"] is False, "diagnostic must not query account")
    require(boundaries["funds_positions_values_recorded"] is False, "diagnostic must not record values")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "diagnostic must not use screenshots")
    require(boundaries["order_action_sent"] is False, "diagnostic must not send order action")

    for term in [
        "diagnose_p019_windows_firewall_tws_api.py",
        "validate_p019_windows_firewall_tws_api_diagnostic.py",
        "P019_WINDOWS_FIREWALL_TWS_API_DIAGNOSTIC_OK",
    ]:
        require(term in acceptance, f"acceptance missing firewall term {term}")
        require(term in phase_plan, f"phase plan missing firewall term {term}")

    print(
        "P019_WINDOWS_FIREWALL_TWS_API_DIAGNOSTIC_OK: "
        f"allow_rules=present block_rules=absent api_listener={diagnosis['known_tws_api_ports_listening']}"
    )


if __name__ == "__main__":
    main()
