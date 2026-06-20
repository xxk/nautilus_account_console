from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "knowledge-backfill-draft.json"
REAL_CLOSEOUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "real-acceptance-closeout.json"
CURRENT_REFRESH = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "current-state-closeout-refresh.json"
SOCKET_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-socket-diagnostic.json"
CONFIG_DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
ACCOUNT_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "account_summary.json"
POSITIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "positions.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
COMPLETION_AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"
DURABLE_RELOAD = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"
REAL_UI_PARITY = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def ref(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    closeout = load(REAL_CLOSEOUT)
    socket = load(SOCKET_DIAGNOSTIC)
    config = load(CONFIG_DIAGNOSTIC)
    executions = load(EXECUTIONS)
    audit = load(COMPLETION_AUDIT)
    durable_reload = load(DURABLE_RELOAD)
    status = "ready" if closeout.get("status") == "ready" else "blocked_not_ready"
    latest_config = config.get("latest_config_candidate", {})
    api_settings = latest_config.get("api_settings", {})
    handshake_ok = any(
        item.get("status") == "handshake_ok" for item in socket.get("handshake_port_refs", {}).values()
    )

    entry_lines = [
        f"### {datetime.now(UTC).date().isoformat()} Successful TWS API Login/API Enablement",
        "",
        "- closeout_status: ready",
        f"- closeout_ref: {ref(REAL_CLOSEOUT)}",
        f"- current_state_refresh_ref: {ref(CURRENT_REFRESH)}",
        f"- socket_diagnostic_ref: {ref(SOCKET_DIAGNOSTIC)}",
        f"- config_diagnostic_ref: {ref(CONFIG_DIAGNOSTIC)}",
        f"- account_summary_ref: {ref(ACCOUNT_SUMMARY)}",
        f"- positions_ref: {ref(POSITIONS)}",
        f"- executions_ref: {ref(EXECUTIONS)}",
        f"- source_package_ref: {ref(SOURCE_PACKAGE)}",
        f"- durable_store_reload_ref: {ref(DURABLE_RELOAD)}",
        f"- completion_audit_ref: {ref(COMPLETION_AUDIT)}",
        f"- real_ui_parity_ref: {ref(REAL_UI_PARITY)}",
        "- sanitized_config_shape: "
        f"socketClient={api_settings.get('socketClient')}, "
        f"allowOnlyLocalhost={api_settings.get('allowOnlyLocalhost')}, "
        f"port_ref={api_settings.get('port')}",
        "- readiness_shape: "
        f"handshake_ok={str(handshake_ok).lower()}, "
        f"account_summary_success={str(closeout.get('account_summary_success') is True).lower()}, "
        f"positions_success={str(closeout.get('positions_success') is True).lower()}, "
        f"source_package_state={closeout.get('source_package_state')}, "
        f"real_ui_parity_verdict={closeout.get('real_ui_parity_verdict')}",
        "- report_store_non_claims: "
        f"executions_query_success={str(executions.get('success') is True).lower()}, "
        f"execution_report_rows={executions.get('execution_report_rows')}, "
        f"complete_history_claimed={str(executions.get('readonly_query', {}).get('complete_history_claimed') is True).lower()}, "
        f"durable_reload_state={durable_reload.get('replay_state', {}).get('state')}, "
        f"durable_reload_parity={durable_reload.get('reload_proof', {}).get('parity_status')}, "
        f"completion_overall_status={audit.get('overall_status')}",
        "- non_secret_operator_steps_required: <fill non-secret step, or none>",
        "- verification_commands:",
        "  - python scripts/validate_p019_u3028269_current_state_closeout_refresh.py",
        "  - python scripts/validate_p019_u3028269_real_acceptance_closeout.py",
        "  - python scripts/validate_p019_runtime_evidence_freshness.py",
        "  - python scripts/validate_p019_broker_observation_foundation.py",
        "- raw_secret_values_recorded=false",
        "- raw_broker_endpoint_recorded=false",
        "- raw_config_file_contents_recorded=false",
        "- funds_positions_values_recorded_in_knowledge=false",
        "- screenshot_used_for_funds_positions=false",
        "- order_action_sent=false",
    ]
    entry_markdown = "\n".join(entry_lines) if status == "ready" else ""

    payload = {
        "schema": "account-console.ib-tws-u3028269-login-api-knowledge-backfill-draft.v1",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "prepared_at": now(),
        "status": status,
        "ready_to_append_to_knowledge_card": status == "ready",
        "blocker_id": None if status == "ready" else closeout.get("blocker_id", "tws_api_readiness_missing"),
        "source_refs": {
            "real_closeout": ref(REAL_CLOSEOUT),
            "current_state_refresh": ref(CURRENT_REFRESH),
            "socket_diagnostic": ref(SOCKET_DIAGNOSTIC),
            "config_diagnostic": ref(CONFIG_DIAGNOSTIC),
            "account_summary": ref(ACCOUNT_SUMMARY),
            "positions": ref(POSITIONS),
            "executions": ref(EXECUTIONS),
            "source_package": ref(SOURCE_PACKAGE),
            "durable_store_reload": ref(DURABLE_RELOAD),
            "completion_audit": ref(COMPLETION_AUDIT),
            "real_ui_parity": ref(REAL_UI_PARITY),
        },
        "required_before_append": [
            "real_acceptance_closeout.status=ready",
            "handshake_ok=true",
            "account_summary_success=true",
            "positions_success=true",
            "source_package_state=ready",
            "real_ui_parity_verdict=pass",
            "executions_query_success=true",
            "execution_report_rows=0 keeps real report parity blocked until rows exist",
            "durable_reload_parity=blocked while real execution rows are absent",
        ],
        "sanitized_config_shape": {
            "socketClient": api_settings.get("socketClient"),
            "allowOnlyLocalhost": api_settings.get("allowOnlyLocalhost"),
            "port_ref": api_settings.get("port"),
        },
        "readiness_shape": {
            "handshake_ok": handshake_ok,
            "account_summary_success": closeout.get("account_summary_success") is True,
            "positions_success": closeout.get("positions_success") is True,
            "source_package_state": closeout.get("source_package_state"),
            "real_ui_parity_verdict": closeout.get("real_ui_parity_verdict"),
        },
        "report_store_non_claims": {
            "executions_query_success": executions.get("success") is True,
            "execution_report_rows": executions.get("execution_report_rows"),
            "complete_history_claimed": executions.get("readonly_query", {}).get("complete_history_claimed") is True,
            "order_action_sent": executions.get("readonly_query", {}).get("order_action_sent") is True,
            "durable_reload_state": durable_reload.get("replay_state", {}).get("state"),
            "durable_reload_parity": durable_reload.get("reload_proof", {}).get("parity_status"),
            "completion_overall_status": audit.get("overall_status"),
            "completion_must_not_be_claimed": audit.get("completion_must_not_be_claimed"),
        },
        "knowledge_card_entry_markdown": entry_markdown,
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "raw_config_file_contents_recorded": False,
            "funds_positions_values_recorded_in_knowledge": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
            "writes_outside_worktree": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "output": ref(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
