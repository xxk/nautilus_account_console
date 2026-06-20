from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "pipeline-summary.json"
RUNNER = ROOT / "scripts" / "run_p019_ib_u3028269_tws_api_pipeline.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class PipelineError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PipelineError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(SUMMARY)
    runner = read(RUNNER)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-ib-u3028269-tws-api-pipeline-summary.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["status"] in {"ready", "blocked"}, "status mismatch")
    require(payload["ibapi_available"] is True, "pipeline must use available worktree-local ibapi")
    require(payload["ibapi_runtime_ref"] == "output/runtime/python", "ibapi runtime ref mismatch")
    require(
        payload["socket_diagnostic_ref"] == "output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json",
        "socket diagnostic ref mismatch",
    )
    require(
        payload["firewall_diagnostic_ref"]
        == "output/debug/p019-tws-api-readiness/windows-firewall-tws-api-diagnostic.json",
        "firewall diagnostic ref mismatch",
    )
    require(
        payload["config_diagnostic_ref"] == "output/debug/p019-tws-api-readiness/tws-api-config-diagnostic.json",
        "config diagnostic ref mismatch",
    )
    require(payload["readiness_ref"] == "output/debug/p019-tws-api-readiness/tws-api-readiness-probe.json", "readiness ref mismatch")
    require(payload["account_summary_ref"].endswith("account_summary.json"), "account summary ref mismatch")
    require(payload["positions_ref"].endswith("positions.json"), "positions ref mismatch")
    require(payload["source_package_ref"].endswith("source-package.json"), "source package ref mismatch")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(boundaries["order_action_sent"] is False, "order action must not be sent")

    require(payload["steps"], "pipeline steps missing")
    for step in payload["steps"]:
        require(step["ok"] is True, f"pipeline step failed: {step['command']}")
    commands = {step["command"] for step in payload["steps"]}
    for expected in [
        "python scripts/diagnose_p019_tws_api_socket.py",
        "python scripts/validate_p019_tws_api_socket_diagnostic.py",
        "python scripts/diagnose_p019_windows_firewall_tws_api.py",
        "python scripts/validate_p019_windows_firewall_tws_api_diagnostic.py",
        "python scripts/diagnose_p019_tws_api_config.py",
        "python scripts/validate_p019_tws_api_config_diagnostic.py",
        "python scripts/probe_p019_tws_api_readiness.py",
        "python scripts/validate_p019_tws_api_readiness_probe.py",
        "python scripts/collect_ib_u3028269_tws_api_snapshot.py --allow-blocked",
        "python scripts/validate_p019_ib_u3028269_tws_api_queries.py",
        "python scripts/build_ib_u3028269_source_package_from_tws_api.py --allow-blocked",
        "python scripts/validate_p019_ib_u3028269_source_package.py",
        "python scripts/validate_account_mirror_api.py",
    ]:
        require(expected in commands, f"pipeline missing command {expected}")

    if payload["status"] == "blocked":
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked pipeline blocker mismatch")
        require(payload["socket_primary_blocker"] == "local_tws_api_socket_not_open", "socket primary blocker mismatch")
        require(payload["firewall_primary_blocker"] == "local_tws_api_socket_not_open", "firewall primary blocker mismatch")
        require(
            payload["config_primary_blocker"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "config primary blocker mismatch",
        )
        require(payload["ready_for_tws_api_funds_positions_query"] is False, "blocked pipeline must not be API-ready")
        require(payload["account_summary_success"] is False, "blocked pipeline must not claim account summary success")
        require(payload["positions_success"] is False, "blocked pipeline must not claim positions success")
    else:
        require(payload["blocker_id"] is None, "ready pipeline must not carry blocker")
        require(payload["ready_for_tws_api_funds_positions_query"] is True, "ready pipeline must be API-ready")
        require(payload["account_summary_success"] is True, "ready pipeline must have account summary success")
        require(payload["positions_success"] is True, "ready pipeline must have positions success")

    for term in [
        "diagnose_p019_tws_api_socket.py",
        "diagnose_p019_windows_firewall_tws_api.py",
        "diagnose_p019_tws_api_config.py",
        "probe_p019_tws_api_readiness.py",
        "collect_ib_u3028269_tws_api_snapshot.py",
        "build_ib_u3028269_source_package_from_tws_api.py",
        "validate_account_mirror_api.py",
    ]:
        require(term in runner, f"runner missing command term {term}")
    for term in [
        "run_p019_ib_u3028269_tws_api_pipeline.py",
        "validate_p019_ib_u3028269_tws_api_pipeline.py",
        "P019_IB_U3028269_TWS_API_PIPELINE_OK",
    ]:
        require(term in acceptance, f"acceptance missing pipeline term {term}")
        require(term in phase_plan, f"phase plan missing pipeline term {term}")

    print(
        "P019_IB_U3028269_TWS_API_PIPELINE_OK: "
        f"status={payload['status']} blocker_id={payload['blocker_id'] or 'none'} steps={len(payload['steps'])}"
    )


if __name__ == "__main__":
    main()
