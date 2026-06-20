from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "topics" / "ib-tws" / "u3028269-tws-login-and-api-knowledge.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class IbTwsLoginApiKnowledgeError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IbTwsLoginApiKnowledgeError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(text: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in text]
    require(not missing, f"{label}: missing terms {missing}")


def main() -> None:
    card = read(CARD)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require_terms(
        card,
        [
            "ib-tws-u3028269-login-api",
            "acct.ib.live.u3028269",
            "U3028269",
            "login-success recorded",
            "runtime `handshake_ok=true`; latest static XML candidate may still report `socketClient=false`",
            "allowOnlyLocalhost=true",
            "port=7497",
            "handshake_ok",
            "reqAccountSummary",
            "reqPositions",
            "refresh_p019_u3028269_current_state_closeout.py --wait-timeout-seconds 120 --wait-interval-seconds 5",
            "validate_p019_u3028269_current_state_closeout_refresh.py",
            "validate_p019_runtime_evidence_freshness.py",
            "local_tws_api_socket_not_open",
            "local_tws_api_handshake_not_ok",
            "tws_api_socket_disabled_in_latest_config_candidate",
            "tws_api_readiness_missing",
            "placeOrder=false",
            "cancelOrder=false",
            "screenshot_used_for_funds_positions=false",
            "raw_secret_values_recorded=false",
            "raw_broker_endpoint_recorded=false",
            "raw_config_file_contents_recorded=false",
            "Do not record passwords, auth codes, raw endpoints, raw XML or funds/positions values",
            "Success Backfill Template",
            "closeout_status: ready",
            "closeout_ref: output/account_capability/ib-live-u3028269/real-acceptance-closeout.json",
            "current_state_refresh_ref: output/account_capability/ib-live-u3028269/current-state-closeout-refresh.json",
            "socket_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json",
            "config_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-config-diagnostic.json",
            "account_summary_ref: output/account_capability/ib-live-u3028269/tws-api/account_summary.json",
            "positions_ref: output/account_capability/ib-live-u3028269/tws-api/positions.json",
            "source_package_ref: output/account_capability/ib-live-u3028269/source-package.json",
            "real_ui_parity_ref: docs/acceptance/2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
            "2026-06-20 Successful TWS API Login/API Enablement",
            "sanitized_config_shape: runtime_handshake_ok=true, latest_static_socketClient=false, allowOnlyLocalhost=true, port_ref=7497",
            "readiness_shape: handshake_ok=true, account_summary_success=true, positions_success=true, source_package_state=ready, real_ui_parity_verdict=pass",
            "funds_positions_values_recorded_in_knowledge=false",
        ],
        "IB TWS U3028269 knowledge card",
    )
    for forbidden in [
        "raw_tws_password=true",
        "raw_2fa_or_auth_code=true",
        "raw_broker_secret=true",
        "raw_broker_endpoint=true",
        "raw_tws_xml_contents=true",
        "placeOrder=true",
        "cancelOrder=true",
        "screenshot_used_for_funds_positions=true",
        "can_trade=true",
        "broker_tradable=true",
    ]:
        require(forbidden not in card, f"knowledge card must not claim {forbidden}")

    require("u3028269-tws-login-and-api-knowledge.md" in acceptance, "acceptance missing knowledge card")
    require("validate_ib_tws_u3028269_login_api_knowledge.py" in acceptance, "acceptance missing knowledge validator")
    require("IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_OK" in acceptance, "acceptance missing knowledge pass signal")
    require("u3028269-tws-login-and-api-knowledge.md" in phase_plan, "phase plan missing knowledge card")
    require("validate_ib_tws_u3028269_login_api_knowledge.py" in phase_plan, "phase plan missing knowledge validator")
    require("IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_OK" in phase_plan, "phase plan missing knowledge pass signal")

    print("IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_OK: status=login_success_recorded")


if __name__ == "__main__":
    main()
