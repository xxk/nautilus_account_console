from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAIT_RUNNER = ROOT / "scripts" / "wait_p019_tws_api_ready_and_collect.py"
PIPELINE_RUNNER = ROOT / "scripts" / "run_p019_ib_u3028269_tws_api_pipeline.py"
COLLECTOR = ROOT / "scripts" / "collect_ib_u3028269_tws_api_snapshot.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class RecoveryPathGuardError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RecoveryPathGuardError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_order(text: str, terms: list[str], label: str) -> None:
    positions = []
    for term in terms:
        index = text.find(term)
        require(index >= 0, f"{label}: missing term {term}")
        positions.append(index)
    require(positions == sorted(positions), f"{label}: terms out of order {terms}")


def main() -> None:
    wait_runner = read(WAIT_RUNNER)
    pipeline_runner = read(PIPELINE_RUNNER)
    collector = read(COLLECTOR)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require_order(
        wait_runner,
        [
            "probe_p019_tws_api_readiness.py",
            "validate_p019_tws_api_readiness_probe.py",
            'if readiness.get("ready_for_tws_api_funds_positions_query") is True:',
            "run_p019_ib_u3028269_tws_api_pipeline.py",
        ],
        "wait runner",
    )
    require(
        "pipeline_step = _run(" in wait_runner and "if ready:" in wait_runner,
        "wait runner must only invoke the pipeline from the ready branch",
    )
    for forbidden in ["collect_ib_u3028269_tws_api_snapshot.py", "build_ib_u3028269_source_package_from_tws_api.py"]:
        before_ready = wait_runner.split('if readiness.get("ready_for_tws_api_funds_positions_query") is True:')[0]
        require(forbidden not in before_ready, f"wait runner must not call {forbidden} before readiness")

    require_order(
        pipeline_runner,
        [
            "diagnose_p019_tws_api_socket.py",
            "validate_p019_tws_api_socket_diagnostic.py",
            "diagnose_p019_windows_firewall_tws_api.py",
            "validate_p019_windows_firewall_tws_api_diagnostic.py",
            "diagnose_p019_tws_api_config.py",
            "validate_p019_tws_api_config_diagnostic.py",
            "probe_p019_tws_api_readiness.py",
            "validate_p019_tws_api_readiness_probe.py",
            "collect_ib_u3028269_tws_api_snapshot.py",
            "validate_p019_ib_u3028269_tws_api_queries.py",
            "build_ib_u3028269_source_package_from_tws_api.py",
            "validate_p019_ib_u3028269_source_package.py",
            "validate_account_mirror_api.py",
        ],
        "pipeline runner",
    )

    for required in [
        "reqManagedAccts",
        "reqAccountSummary",
        "reqPositions",
        "reqExecutions",
        "reqAutoOpenOrders",
        "reqOpenOrders",
        "reqAllOpenOrders",
        "ExecutionFilter",
        "openOrderEnd",
        "cancelAccountSummary",
        "cancelPositions",
    ]:
        require(required in collector, f"collector missing read-only IB API term {required}")
    for forbidden in ["placeOrder", "cancelOrder", "reqGlobalCancel"]:
        require(forbidden not in collector, f"collector must not contain command/order term {forbidden}")

    for term in [
        "validate_p019_tws_api_recovery_path_guard.py",
        "P019_TWS_API_RECOVERY_PATH_GUARD_OK",
    ]:
        require(term in acceptance, f"acceptance missing recovery guard term {term}")
        require(term in phase_plan, f"phase plan missing recovery guard term {term}")

    print("P019_TWS_API_RECOVERY_PATH_GUARD_OK: readiness_before_collect=true order_actions=absent")


if __name__ == "__main__":
    main()
