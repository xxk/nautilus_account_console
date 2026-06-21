from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "knowledge-backfill-draft.json"
SCRIPT = ROOT / "scripts" / "prepare_ib_tws_u3028269_login_api_knowledge_backfill.py"
CARD = ROOT / "docs" / "topics" / "ib-tws" / "u3028269-tws-login-and-api-knowledge.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class KnowledgeBackfillError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise KnowledgeBackfillError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    draft = load(DRAFT)
    script = read(SCRIPT)
    card = read(CARD)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(
        draft["schema"] == "account-console.ib-tws-u3028269-login-api-knowledge-backfill-draft.v1",
        "backfill schema drifted",
    )
    require(draft["account_id"] == "acct.ib.live.u3028269", "account id drifted")
    require(draft["display_alias"] == "U3028269", "alias drifted")
    require(draft["status"] in {"ready", "blocked_not_ready"}, "draft status drifted")
    require(draft["ready_to_append_to_knowledge_card"] is (draft["status"] == "ready"), "append gate drifted")
    if draft["status"] == "blocked_not_ready":
        require(draft["blocker_id"] == "tws_api_readiness_missing", "blocked draft blocker drifted")
        require(draft["readiness_shape"]["handshake_ok"] is False, "blocked draft cannot claim handshake_ok")
    else:
        require(draft["blocker_id"] is None, "ready draft must not carry blocker")
        require(draft["readiness_shape"]["handshake_ok"] is True, "ready draft needs handshake_ok")
        require(draft["readiness_shape"]["account_summary_success"] is True, "ready draft needs account summary")
        require(draft["readiness_shape"]["positions_success"] is True, "ready draft needs positions")
        require(draft["readiness_shape"]["source_package_state"] == "ready", "ready draft needs source package")
        require(draft["readiness_shape"]["real_ui_parity_verdict"] == "pass", "ready draft needs UI parity")

    for key in [
        "real_closeout",
        "current_state_refresh",
        "socket_diagnostic",
        "config_diagnostic",
        "account_summary",
        "positions",
        "executions",
        "source_package",
        "durable_store_reload",
        "completion_audit",
        "real_ui_parity",
    ]:
        require(key in draft["source_refs"], f"missing source ref {key}")

    non_claims = draft["report_store_non_claims"]
    require(non_claims["executions_query_success"] is True, "draft must record executions query success")
    require(non_claims["execution_report_rows"] == 0, "draft must record zero real execution rows")
    require(non_claims["complete_history_claimed"] is False, "draft must not claim complete execution history")
    require(non_claims["order_action_sent"] is False, "draft must not send order action")
    require(non_claims["durable_reload_state"] == "partial", "draft must record partial durable reload")
    require(non_claims["durable_reload_parity"] == "blocked", "draft must record blocked durable parity")
    require(non_claims["completion_overall_status"] == "not_complete", "draft must preserve not_complete audit")
    require(non_claims["completion_must_not_be_claimed"] is True, "draft must preserve completion non-claim")

    entry = draft["knowledge_card_entry_markdown"]
    if draft["status"] == "blocked_not_ready":
        require(entry == "", "blocked draft must not generate appendable success markdown")
    else:
        for term in [
            "closeout_status: ready",
            "closeout_ref: output/account_capability/ib-live-u3028269/real-acceptance-closeout.json",
            "current_state_refresh_ref: output/account_capability/ib-live-u3028269/current-state-closeout-refresh.json",
            "socket_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json",
            "account_summary_ref: output/account_capability/ib-live-u3028269/tws-api/account_summary.json",
            "positions_ref: output/account_capability/ib-live-u3028269/tws-api/positions.json",
            "executions_ref: output/account_capability/ib-live-u3028269/tws-api/executions.json",
            "durable_store_reload_ref: output/account_capability/ib-live-u3028269/durable-store-reload.json",
            "completion_audit_ref: docs/proposals/p019-broker-observation-session-foundation/p019-completion-audit.json",
            "report_store_non_claims: executions_query_success=true, execution_report_rows=0",
            "complete_history_claimed=false",
            "durable_reload_state=partial",
            "durable_reload_parity=blocked",
            "completion_overall_status=not_complete",
            "funds_positions_values_recorded_in_knowledge=false",
            "raw_secret_values_recorded=false",
            "order_action_sent=false",
        ]:
            require(term in entry, f"entry missing {term}")

    boundaries = draft["boundaries"]
    for key in [
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "raw_config_file_contents_recorded",
        "funds_positions_values_recorded_in_knowledge",
        "screenshot_used_for_funds_positions",
        "order_action_sent",
        "writes_outside_worktree",
    ]:
        require(boundaries[key] is False, f"boundary drifted: {key}")

    for forbidden in [
        "password",
        "auth_code",
        "raw_tws_xml_contents=true",
        "funds_positions_values_recorded_in_knowledge=true",
        "order_action_sent=true",
        "complete_history_claimed=true",
        "completion_overall_status=complete",
    ]:
        require(forbidden not in json.dumps(draft, ensure_ascii=False).lower(), f"draft contains forbidden {forbidden}")

    for term in [
        "knowledge-backfill-draft.json",
        "executions_ref: output/account_capability/ib-live-u3028269/tws-api/executions.json",
        "durable_store_reload_ref: output/account_capability/ib-live-u3028269/durable-store-reload.json",
        "report_store_non_claims: executions_query_success=true, execution_report_rows=0",
        "funds_positions_values_recorded_in_knowledge=false",
        "If closeout remains blocked, do not create a success entry",
    ]:
        require(term in card, f"knowledge card missing {term}")
    for term in [
        "prepare_ib_tws_u3028269_login_api_knowledge_backfill.py",
        "validate_ib_tws_u3028269_login_api_knowledge_backfill.py",
        "IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_BACKFILL_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")
    for term in [
        "REAL_CLOSEOUT",
        "EXECUTIONS",
        "DURABLE_RELOAD",
        "COMPLETION_AUDIT",
        "knowledge_card_entry_markdown",
        "report_store_non_claims",
        "funds_positions_values_recorded_in_knowledge",
    ]:
        require(term in script, f"backfill script missing {term}")

    print(f"IB_TWS_U3028269_LOGIN_API_KNOWLEDGE_BACKFILL_OK: status={draft['status']}")


if __name__ == "__main__":
    main()
