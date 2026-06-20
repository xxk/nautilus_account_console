from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "workspace-home-runbook-intake.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
RUNBOOK = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "tws-api-runtime-recovery-runbook.md"


class WorkspaceHomeRunbookIntakeError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WorkspaceHomeRunbookIntakeError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(text: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in text]
    require(not missing, f"{label}: missing terms {missing}")


def main() -> None:
    intake = read(INTAKE)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)
    runbook = read(RUNBOOK)

    require_terms(
        intake,
        [
            "D:\\Nautilus\\nautilus_strategies\\scripts\\probe_tws_version.py",
            "D:\\Nautilus\\nautilus_strategies\\tests\\scripts\\test_probe_tws_version.py",
            "D:\\Nautilus\\nautilus_strategies\\tests\\scripts\\test_run_issue19_unblock_sequence.py",
            "D:\\Nautilus\\global_docs\\network\\20_3proxy上游拓扑与接入方案_3proxy Upstream Topology and Access Plan.md",
            "D:\\Nautilus\\global_docs\\network\\93_本机Windows防火墙分析与最小启用方案_Local Windows Firewall Analysis and Enable Plan.md",
            "serverVersion",
            "v100..155",
            "handshake_ok",
            "connect_timeout",
            "connect_refused",
            "handshake_timeout",
            "handshake_invalid",
            "local_tws_api_socket_not_open",
            "tws_api_socket_disabled_in_latest_config_candidate",
            "home_zoom_runbooks_adopted=false",
            "raw_secret_values_recorded=false",
            "raw_broker_endpoint_recorded=false",
            "raw_config_file_contents_recorded=false",
            "tws_reinstall_performed=false",
            "tws_api_account_query_sent_by_intake=false",
            "funds_positions_values_recorded_by_intake=false",
            "order_action_sent=false",
        ],
        "workspace/home runbook intake",
    )
    for forbidden in [
        "home_zoom_runbooks_adopted=true",
        "raw_secret_values_recorded=true",
        "raw_broker_endpoint_recorded=true",
        "raw_config_file_contents_recorded=true",
        "tws_reinstall_performed=true",
        "funds_positions_values_recorded_by_intake=true",
        "order_action_sent=true",
        "screenshot proves funds",
        "TCP connectable alone is enough",
    ]:
        require(forbidden not in intake, f"intake must not claim {forbidden}")

    require("workspace-home-runbook-intake.md" in acceptance, "acceptance missing runbook intake")
    require("validate_p019_workspace_home_runbook_intake.py" in acceptance, "acceptance missing intake validator")
    require("P019_WORKSPACE_HOME_RUNBOOK_INTAKE_OK" in acceptance, "acceptance missing intake pass signal")
    require("workspace-home-runbook-intake.md" in phase_plan, "phase plan missing runbook intake")
    require("validate_p019_workspace_home_runbook_intake.py" in phase_plan, "phase plan missing intake validator")
    require("P019_WORKSPACE_HOME_RUNBOOK_INTAKE_OK" in phase_plan, "phase plan missing intake pass signal")
    require("serverVersion" in runbook, "runtime runbook missing serverVersion")
    require("handshake_ok" in runbook, "runtime runbook missing handshake_ok")

    print("P019_WORKSPACE_HOME_RUNBOOK_INTAKE_OK: adopted=5 excluded=3")


if __name__ == "__main__":
    main()
