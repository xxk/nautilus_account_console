from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-real-ui-parity.spec.ts"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
UI_ACCEPTANCE = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "tws-account-workbench-ui-acceptance.md"
)


class RealUiParityError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RealUiParityError(message)


def main() -> None:
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")
    ui_acceptance = UI_ACCEPTANCE.read_text(encoding="utf-8")

    require(payload["schema"] == "account-console.p019-u3028269-real-ui-parity-evidence.v1", "schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["route"] == "/accounts/acct.ib.live.u3028269", "route mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(payload["source_checksum"].startswith("sha256:"), "source checksum missing")
    require(payload["projection_checksum"].startswith("sha256:"), "projection checksum missing")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshot must not be funds/positions truth")
    require(boundaries["broker_truth"] is False, "UI parity must not claim broker truth")
    require(boundaries["order_action"] is False, "UI parity must not enable order action")

    for item in payload["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty screenshot {item['screenshot']}")

    parity = payload["parity"]
    if payload["verdict"] == "blocked":
        require(payload["status"] == "blocked_waiting_for_real_tws_api_source_package", "blocked status mismatch")
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked evidence must name TWS API readiness blocker")
        require(parity["funds_parity"] == "blocked", "blocked evidence cannot pass funds parity")
        require(parity["positions_parity"] == "blocked", "blocked evidence cannot pass positions parity")
        for non_claim in [
            "does_not_prove_real_u3028269_funds",
            "does_not_prove_real_u3028269_positions",
            "does_not_close_real_ui_parity",
            "does_not_use_screenshot_for_funds_positions",
            "does_not_enable_command_capability",
        ]:
            require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")
    else:
        require(payload["verdict"] == "pass", "verdict must be blocked or pass")
        require(
            payload["status"] == "ready_real_tws_api_source_package_ui_parity_checked",
            "pass status mismatch",
        )
        require(parity["funds_parity"] == "pass", "ready evidence must pass funds parity")
        require(parity["positions_parity"] == "pass", "ready evidence must pass positions parity")
        require(payload["compared_against"]["api_route"] == "/api/mirror/accounts/acct.ib.live.u3028269", "API route mismatch")
        require(payload["compared_against"]["balance_count"] > 0, "ready parity must include balance rows")
        rendered_currencies = payload["compared_against"].get("rendered_balance_currencies", [])
        require(isinstance(rendered_currencies, list), "rendered balance currencies missing")
        require(payload["compared_against"].get("rendered_balance_count") == len(rendered_currencies), "rendered balance count mismatch")
        require("USD" in rendered_currencies, "rendered balances must include USD")
        require(any(currency != "USD" for currency in rendered_currencies), "rendered balances must include non-USD currency")
        require(payload["compared_against"]["position_count"] >= 0, "position count missing")
        compared = payload["compared_against"]
        require(compared["order_count"] >= 0, "order count missing")
        require(
            compared.get("rendered_open_order_count") == compared["order_count"],
            "rendered open order count mismatch",
        )
        require(
            isinstance(compared.get("rendered_open_order_client_order_ids"), list),
            "rendered open order ids missing",
        )
        require(compared["executions_query_success"] is True, "ready parity must include executions query state")
        require(compared["execution_report_rows"] == compared["fill_count"], "execution report/fill count mismatch")
        require(compared.get("rendered_fill_count") == compared["fill_count"], "rendered fill count mismatch")
        require(isinstance(compared.get("rendered_fill_report_ids"), list), "rendered fill report ids missing")
        if compared["execution_report_rows"] == 0:
            require(
                compared["execution_report_state"] == "not_available_or_empty",
                "empty execution reports must carry typed empty state",
            )
        require(
            compared["executions_complete_history_claimed"] is False,
            "UI evidence must not claim complete executions history",
        )
        require(compared["executions_order_action_sent"] is False, "UI evidence must not send order action")
        require(parity["open_orders_parity"] == "pass", "ready evidence must pass open orders parity")
        require(parity["fills_parity"] == "pass", "ready evidence must pass fills parity or typed zero-row empty state")

    for term in [
        "/api/mirror/accounts/",
        "tws-multi-currency-funds-table",
        "account-position-projection-row",
        "tws-open-orders-table",
        "tws-open-order-row",
        "tws-fills-table",
        "tws-fill-row",
        "tws-fill-empty-state",
        "formatMoney",
        "screenshot_used_for_funds_positions: false",
        "executions_complete_history_claimed",
        "rendered_balance_currencies",
        "rendered_open_order_count",
        "rendered_fill_count",
    ]:
        require(term in spec, f"spec missing {term}")

    for term in [
        "2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
        "validate_p019_u3028269_real_ui_parity.py",
        "P019_U3028269_REAL_UI_PARITY_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    for term in [
        "UI-TWS-13",
        "UI-TWS-14",
        "UI-TWS-15",
        "UI-TWS-17",
        "UI-TWS-18",
        "UI-TWS-20",
        "UI-TWS-21",
        "UI-TWS-22",
        "executions_query_success=true",
        "execution_report_rows=0",
        "complete_history_claimed=false",
        "order_action_sent=false",
        "open_orders_parity=pass",
        "fills_parity=pass",
        "execution_reports_persistence_parity=blocked",
        "durable_reload_state=partial",
        "durable_reload_parity=blocked",
        "closes UI-TWS-20 through UI-TWS-22 for open orders",
        "machine-readable parity evidence compares Web UI rendered values against TWS API/source package values",
    ]:
        require(term in ui_acceptance, f"UI acceptance missing {term}")

    print(f"P019_U3028269_REAL_UI_PARITY_OK: verdict={payload['verdict']}")


if __name__ == "__main__":
    main()
