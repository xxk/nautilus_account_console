from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "tws-api-runtime-recovery-runbook.md"
README = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "README.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class RuntimeRecoveryRunbookError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeRecoveryRunbookError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(text: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in text]
    require(not missing, f"{label}: missing terms {missing}")


def main() -> None:
    runbook = read(RUNBOOK)
    readme = read(README)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require_terms(
        runbook,
        [
            "tws_api_readiness_missing",
            "local_tws_api_socket_not_open",
            "tws_api_socket_disabled_in_latest_config_candidate",
            "firewall_allow_rules=present",
            "firewall_enabled_block_rules=absent",
            "latest_config_candidate.api_socket_enabled=false",
            "latest_config_candidate.socketClient=false",
            "known_api_ports_connectable=false",
            "serverVersion",
            "v100..155",
            "D:\\Nautilus\\nautilus_strategies\\scripts\\probe_tws_version.py",
            "handshake_ok",
            "local_tws_api_handshake_not_ok",
            "Trusted IPs",
            "prepare_p019_tws_api_enable_change_request.py",
            "validate_p019_tws_api_enable_change_request.py",
            "requested `socketClient=true`",
            "does not modify `C:\\Jts`",
            "wait_p019_tws_api_ready_and_collect.py --timeout-seconds 120 --interval-seconds 5",
            "validate_p019_tws_api_wait_collect.py",
            "validate_p019_ib_u3028269_tws_api_pipeline.py",
            "validate_p019_ib_u3028269_tws_api_queries.py",
            "validate_p019_ib_u3028269_source_package.py",
            "validate_account_mirror_api.py",
            "validate_p019_broker_observation_foundation.py",
            "validate_p019_runtime_evidence_freshness.py",
            "newer than the latest socket/firewall/config diagnostics",
            "newer than the config diagnostic",
            "stale pipeline summaries",
            "ready_for_tws_api_funds_positions_query=true",
            "success=true",
            "tws_api_login_confirmed=true",
            "source_health.state=ready",
            "source_health.api_transport=ib_tws_api",
            "screenshot_used_for_funds_positions=false",
            "order_action_sent=false",
            "tws_api_account_query_sent_before_readiness=false",
            "funds_positions_values_recorded_before_readiness=false",
            "Reinstall Decision Gate",
            "Do not reinstall TWS as the first remediation",
            "explicit operator approval",
            "exact path, reason and expected impact",
            "TWS has been restarted or relaunched after the API setting change",
            "same readiness, query, source-package, Account Mirror and UI parity validators still apply",
        ],
        "runtime recovery runbook",
    )
    for forbidden in [
        "paste passwords",
        "paste auth codes",
        "copy raw `tws.xml` contents",
        "screenshots as funds truth",
        "placeOrder",
        "cancelOrder",
        "reqOpenOrders",
        "reqAllOpenOrders",
        "direct browser/backend TWS routes",
    ]:
        require(forbidden in runbook, f"runtime recovery runbook missing forbidden boundary {forbidden}")

    for forbidden_claim in [
        "screenshot proves funds",
        "screenshot proves positions",
        "can_trade=true",
        "live_ready=true",
        "broker_tradable=true",
        "order_action_sent=true",
        "raw_secret_values_recorded=true",
        "Reinstall is required",
        "reinstall closes P019",
        "reinstall proves funds",
        "reinstall proves positions",
    ]:
        require(forbidden_claim not in runbook, f"runtime recovery runbook must not claim {forbidden_claim}")

    require("`tws-api-runtime-recovery-runbook.md`" in readme, "README missing runtime recovery runbook")
    require("validate_p019_tws_api_runtime_recovery_runbook.py" in acceptance, "acceptance missing runtime runbook validator")
    require("P019_TWS_API_RUNTIME_RECOVERY_RUNBOOK_OK" in acceptance, "acceptance missing runtime runbook pass signal")
    require("validate_p019_runtime_evidence_freshness.py" in acceptance, "acceptance missing runtime freshness validator")
    require("P019_RUNTIME_EVIDENCE_FRESHNESS_OK" in acceptance, "acceptance missing runtime freshness pass signal")
    require("validate_p019_tws_api_runtime_recovery_runbook.py" in phase_plan, "phase plan missing runtime runbook validator")
    require("P019_TWS_API_RUNTIME_RECOVERY_RUNBOOK_OK" in phase_plan, "phase plan missing runtime runbook pass signal")
    require("validate_p019_runtime_evidence_freshness.py" in phase_plan, "phase plan missing runtime freshness validator")
    require("P019_RUNTIME_EVIDENCE_FRESHNESS_OK" in phase_plan, "phase plan missing runtime freshness pass signal")

    print("P019_TWS_API_RUNTIME_RECOVERY_RUNBOOK_OK: no_secrets=true wait_collect_required=true screenshots_not_truth=true")


if __name__ == "__main__":
    main()
