from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_p019_runtime_evidence_freshness.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class RuntimeEvidenceFreshnessReadyContractError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeEvidenceFreshnessReadyContractError(message)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundaries(*, include_config: bool = False, include_external: bool = False, include_closeout: bool = False) -> dict[str, bool]:
    payload = {
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "funds_positions_values_recorded": False,
        "screenshot_used_for_funds_positions": False,
        "order_action_sent": False,
    }
    if include_config:
        payload["raw_config_file_contents_recorded"] = False
    if include_external:
        payload["writes_outside_worktree"] = False
        payload["raw_config_file_contents_recorded"] = False
        payload["tws_reinstall_performed"] = False
        payload["tws_api_account_query_sent"] = False
    if include_closeout:
        payload.pop("funds_positions_values_recorded")
        payload["synthetic_evidence_used_for_real_closeout"] = False
    return payload


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="p019-ready-freshness-") as tmp:
        root = Path(tmp)
        socket_path = root / "socket.json"
        firewall_path = root / "firewall.json"
        config_path = root / "config.json"
        reinstall_path = root / "reinstall.json"
        enable_path = root / "enable.json"
        wait_path = root / "wait.json"
        pipeline_path = root / "pipeline.json"
        closeout_path = root / "closeout.json"

        write_json(
            socket_path,
            {
                "schema": "account-console.p019-tws-api-socket-diagnostic.v1",
                "observed_at": "2026-06-20T10:00:00Z",
                "tws_process": {"present": True},
                "listener_port_refs": {"tws_paper_default": {"listening": True}},
                "connect_port_refs": {"tws_paper_default": {"connectable": True}},
                "handshake_port_refs": {
                    "tws_paper_default": {
                        "status": "handshake_ok",
                        "tcp_connected": True,
                        "bytes_received": 32,
                        "server_version": 199,
                        "connect_time": "20260620 18:00:00 Asia/Shanghai",
                    }
                },
                "handshake_version_range": "v100..155",
                "ready_for_tws_api_funds_positions_query": True,
                "typed_blocker": None,
                "boundaries": boundaries(),
            },
        )
        write_json(
            firewall_path,
            {
                "schema": "account-console.p019-windows-firewall-tws-api-diagnostic.v1",
                "observed_at": "2026-06-20T10:00:01Z",
                "tws_process": {"present": True},
                "diagnosis": {
                    "matching_allow_rules_present": True,
                    "matching_block_rules_present": False,
                    "firewall_is_primary_blocker": False,
                    "primary_blocker": "local_tws_api_socket_not_open",
                },
                "boundaries": boundaries(),
            },
        )
        write_json(
            config_path,
            {
                "schema": "account-console.p019-tws-api-config-diagnostic.v1",
                "observed_at": "2026-06-20T10:00:02Z",
                "latest_config_candidate": {
                    "api_settings": {
                        "socketClient": "true",
                        "allowOnlyLocalhost": "true",
                        "port": "7497",
                    },
                    "api_socket_enabled": True,
                },
                "ready_for_tws_api_funds_positions_query": True,
                "typed_blocker": None,
                "boundaries": boundaries(include_config=True),
            },
        )
        write_json(
            reinstall_path,
            {
                "schema": "account-console.p019-tws-reinstall-decision.v1",
                "observed_at": "2026-06-20T10:00:03Z",
                "decision": "do_not_reinstall_yet",
                "reinstall_recommended": False,
                "primary_next_action": "run_real_acceptance_closeout",
                "current_evidence": {"known_api_ports_connectable": True},
                "boundaries": boundaries(include_external=True),
            },
        )
        write_json(
            enable_path,
            {
                "schema": "account-console.p019-tws-api-enable-change-request.v1",
                "prepared_at": "2026-06-20T10:00:04Z",
                "status": "already_ready_no_change_required",
                "current_settings": {"socketClient": "true"},
                "requested_settings": {"socketClient": "true", "allowOnlyLocalhost": "true"},
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
            },
        )
        write_json(
            wait_path,
            {
                "schema": "account-console.p019-tws-api-wait-collect-summary.v1",
                "started_at": "2026-06-20T10:00:05Z",
                "completed_at": "2026-06-20T10:00:06Z",
                "status": "ready",
                "blocker_id": None,
                "attempt_count": 1,
                "pipeline_ran": True,
                "boundaries": {
                    "raw_secret_values_recorded": False,
                    "raw_broker_endpoint_recorded": False,
                    "tws_api_account_query_sent_before_readiness": False,
                    "funds_positions_values_recorded_before_readiness": False,
                    "screenshot_used_for_funds_positions": False,
                    "order_action_sent": False,
                },
            },
        )
        write_json(
            pipeline_path,
            {
                "schema": "account-console.p019-ib-u3028269-tws-api-pipeline-summary.v1",
                "status": "ready",
                "blocker_id": None,
                "ready_for_tws_api_funds_positions_query": True,
                "account_summary_success": True,
                "positions_success": True,
                "source_package_state": "ready",
                "boundaries": {
                    "raw_secret_values_recorded": False,
                    "raw_broker_endpoint_recorded": False,
                    "screenshot_used_for_funds_positions": False,
                    "order_action_sent": False,
                },
            },
        )
        write_json(
            closeout_path,
            {
                "schema": "account-console.p019-u3028269-real-acceptance-closeout.v1",
                "started_at": "2026-06-20T10:00:07Z",
                "completed_at": "2026-06-20T10:00:08Z",
                "status": "ready",
                "blocker_id": None,
                "real_ui_parity_verdict": "pass",
                "account_summary_success": True,
                "positions_success": True,
                "source_package_state": "ready",
                "boundaries": boundaries(include_closeout=True),
            },
        )

        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--socket-diagnostic",
                str(socket_path),
                "--firewall-diagnostic",
                str(firewall_path),
                "--config-diagnostic",
                str(config_path),
                "--reinstall-decision",
                str(reinstall_path),
                "--enable-change-request",
                str(enable_path),
                "--wait-collect-summary",
                str(wait_path),
                "--pipeline-summary",
                str(pipeline_path),
                "--real-acceptance-closeout",
                str(closeout_path),
            ],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        require(result.returncode == 0, result.stderr or result.stdout)
        require(
            "P019_RUNTIME_EVIDENCE_FRESHNESS_OK: status=ready evidence=fresh" in result.stdout,
            "ready freshness pass signal missing",
        )

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")
    for term in [
        "validate_p019_runtime_evidence_freshness_ready_contract.py",
        "P019_RUNTIME_EVIDENCE_FRESHNESS_READY_CONTRACT_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print("P019_RUNTIME_EVIDENCE_FRESHNESS_READY_CONTRACT_OK: synthetic_ready=fresh")


if __name__ == "__main__":
    main()
