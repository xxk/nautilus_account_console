from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ACCEPTANCE = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "tws-account-workbench-ui-acceptance.md"
)
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"


class OpenOrdersAcceptanceDesignError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise OpenOrdersAcceptanceDesignError(message)


def main() -> None:
    ui_acceptance = UI_ACCEPTANCE.read_text(encoding="utf-8")
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")

    for term in [
        "Open orders / 挂单",
        "UI-TWS-20",
        "UI-TWS-21",
        "UI-TWS-22",
        "UI-TWS-23",
        "UI-TWS-24",
        "tws-open-orders-table",
        "tws-open-order-row",
        "tws-open-order-source-ref",
        "tws-fills-table",
        "tws-fill-row",
        "tws-fill-empty-state",
        "account-console.ib-tws-open-orders-query.v1",
        "openOrder",
        "orderStatus",
        "openOrderEnd",
        "reqExecutions",
        "ExecutionFilter",
        "FillReport",
        "order_action_sent=false",
        "cancel_order_sent=false",
        "replace_order_sent=false",
        "complete_history_claimed=false",
        "screenshot_used_for_values=false",
        "open_orders_source_missing",
        "open_orders_parity: pass | blocked | fail",
        "fills_parity: pass | blocked | fail",
    ]:
        require(term in ui_acceptance, f"UI acceptance missing open-orders term: {term}")

    for forbidden_claim in [
        "screenshot proves open-order parity",
        "screenshot closes open-order parity",
        "cancel controls are allowed",
        "replace controls are allowed",
    ]:
        require(forbidden_claim not in ui_acceptance, f"forbidden open-orders claim present: {forbidden_claim}")

    for term in [
        "validate_p019_open_orders_acceptance_design.py",
        "P019_OPEN_ORDERS_ACCEPTANCE_DESIGN_OK",
        "screenshots cannot prove挂单 parity",
        "must not expose cancel/replace/modify/submit controls",
    ]:
        require(term in acceptance, f"acceptance missing open-orders design term: {term}")

    print("P019_OPEN_ORDERS_ACCEPTANCE_DESIGN_OK: readonly=true ui_tws=20-24")


if __name__ == "__main__":
    main()
