from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
ORDER_DISPLAY = EVIDENCE_DIR / "partial-fill-cancel-order-display.json"
APP = ROOT / "frontend" / "src" / "App.tsx"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-partial-fill-cancel-order-display.spec.ts"
REQUIRED_SCREENSHOTS = [
    "p024-working-order-display.png",
    "p024-partial-fill-display.png",
    "p024-cancel-intent-accepted.png",
    "p024-cancel-pending-display.png",
    "p024-cancelled-display.png",
]


class P024PartialFillCancelEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillCancelEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_int(value: Any) -> int | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "missing":
        return None
    return int(text)


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "live_armed=true"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_order_display(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-cancel-ui-acceptance.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["verdict"] == "browser_order_display_contract_pass_runtime_partial_fill_blocked",
        "verdict mismatch",
    )
    require(payload["ui_order_display_verdict"] == "pass", "order display verdict mismatch")
    require(payload["partial_cancel_display_verdict"] == "pass", "partial-cancel display verdict mismatch")
    require(
        payload["ui_command_control_verdict"] == "paper_armed_cancel_intent_accepted_for_risk",
        "command control verdict mismatch",
    )
    require(
        payload["runtime_partial_fill_verdict"]
        == "typed_blocker_until_real_or_owner_approved_partial_fill_state",
        "runtime partial-fill blocker mismatch",
    )
    require(payload["raw_secret_values_recorded"] is False, "raw secret flag mismatch")
    require(payload["raw_broker_endpoint_recorded"] is False, "raw endpoint flag mismatch")

    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_prove_real_openctp_partial_fill_runtime",
        "does_not_use_screenshot_as_order_truth",
        "does_not_claim_live_readiness",
        "gateway_ack_is_not_final_state",
        "browser_test_does_not_send_broker_cancel",
        "typed_owner_approved_fixture_is_not_broker_truth",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")

    stages = payload.get("stages")
    require(isinstance(stages, list) and len(stages) == 4, "must contain S1-S4 stages")
    expected = {
        "S1": {"status": "working", "submitted": 10, "filled": 0, "remaining": 10, "cancelled": None},
        "S2": {"status": "partial", "submitted": 10, "filled": 4, "remaining": 6, "cancelled": None},
        "S3": {"status": "cancel_pending", "submitted": 10, "filled": 4, "remaining": 6, "cancelled": None},
        "S4": {"status": "canceled", "submitted": 10, "filled": 4, "remaining": 0, "cancelled": 6},
    }
    checks = payload.get("partial_cancel_display_checks") or {}
    for check in [
        "same_order_identity_across_stages",
        "s2_browser_fill_sum_equals_order_filled_quantity",
        "s2_trade_refs_match_api_projection",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "s3_quantities_unchanged_until_cancel_readback",
        "s3_no_remaining_cancel_quantity_visible",
        "s3_cancel_pending_is_not_terminal",
        "s4_filled_quantity_preserved_after_cancel",
        "s4_cancelled_quantity_equals_s2_remaining_quantity",
        "s4_remaining_quantity_zero",
        "s4_no_remaining_cancel_quantity_visible",
        "fill_trade_identities_stable_after_cancel",
    ]:
        require(checks.get(check) is True, f"partial-cancel display check failed or missing: {check}")

    seen: set[str] = set()
    for stage in stages:
        stage_id = str(stage["stage"])
        require(stage_id in expected, f"unexpected stage: {stage_id}")
        seen.add(stage_id)
        browser = stage["browser"]
        api = stage["api"]
        exp = expected[stage_id]
        require(api["identity"] == "ctp19053-p024-partial-order-001", f"{stage_id}: identity mismatch")
        require(str(browser["identity"]) == api["identity"], f"{stage_id}: browser identity mismatch")
        require(api["status"] == exp["status"], f"{stage_id}: API status mismatch")
        require(str(api["status"]).replace("_", " ") in str(browser["status"]), f"{stage_id}: browser status mismatch")
        submitted = parse_int(browser["submitted_quantity"])
        filled = parse_int(browser["filled_quantity"])
        remaining = parse_int(browser["remaining_quantity"])
        cancelled = parse_int(browser["cancelled_quantity"])
        require(submitted == exp["submitted"], f"{stage_id}: submitted mismatch")
        require(filled == exp["filled"], f"{stage_id}: filled mismatch")
        require(remaining == exp["remaining"], f"{stage_id}: remaining mismatch")
        require(cancelled == exp["cancelled"], f"{stage_id}: cancelled mismatch")
        if stage_id in {"S1", "S2", "S3"}:
            require(filled + remaining == submitted, f"{stage_id}: filled+remaining formula mismatch")
        if stage_id == "S4":
            require(filled + (cancelled or 0) == submitted, "S4: filled+cancelled formula mismatch")
            require(remaining == 0, "S4: open remaining must be zero")

        order_ref = str(stage["order_artifact_ref"])
        require(order_ref.startswith("readback://"), f"{stage_id}: order artifact ref mismatch")
        if stage_id == "S3":
            require(
                str(browser.get("cancel_pending_ref")).startswith("command-audit://"),
                "S3: cancel pending audit ref missing",
            )

        browser_fill_rows = stage.get("browser_fill_rows") or []
        api_fill_rows = stage.get("api_fill_rows") or []
        browser_fill_total = parse_int(stage.get("browser_fill_total")) or 0
        api_fill_total = parse_int(stage.get("api_fill_total")) or 0
        require(len(browser_fill_rows) == len(api_fill_rows), f"{stage_id}: browser/API fill row count mismatch")
        require(api_fill_total == exp["filled"], f"{stage_id}: API fill total mismatch")
        require(browser_fill_total == exp["filled"], f"{stage_id}: browser fill total mismatch")
        if stage_id in {"S2", "S3", "S4"}:
            refs = stage.get("fill_artifact_refs") or []
            require(len(refs) == 2, f"{stage_id}: fill refs missing")
            require(all(str(ref).startswith("ReqQryTrade://") for ref in refs), f"{stage_id}: fill refs not trade readback")
            require(len(browser_fill_rows) == 2, f"{stage_id}: browser fill rows missing")
            require(len({str(row.get("trade_id")) for row in browser_fill_rows}) == 2, f"{stage_id}: duplicate trade ids")
            for index, (browser_fill, api_fill) in enumerate(zip(browser_fill_rows, api_fill_rows, strict=True)):
                require(
                    str(browser_fill.get("trade_id")) == str(api_fill.get("trade_id")),
                    f"{stage_id}: fill {index} trade id mismatch",
                )
                require(
                    parse_int(browser_fill.get("filled_quantity")) == parse_int(api_fill.get("filled_quantity")),
                    f"{stage_id}: fill {index} quantity mismatch",
                )
                require(
                    parse_int(browser_fill.get("price")) == parse_int(api_fill.get("price")),
                    f"{stage_id}: fill {index} price mismatch",
                )
                require(
                    str(browser_fill.get("source_ref")) == str(api_fill.get("source_ref")),
                    f"{stage_id}: fill {index} source ref mismatch",
                )
        else:
            require(browser_fill_rows == [], f"{stage_id}: unexpected browser fill rows")

        remaining_cancel = parse_int(browser.get("remaining_cancel_quantity"))
        if stage_id == "S2":
            require(remaining_cancel == exp["remaining"], "S2: cancel target must equal remaining quantity")
        if stage_id in {"S3", "S4"}:
            require(remaining_cancel is None, f"{stage_id}: remaining cancel target must not stay visible")

        command_refs = stage.get("command_status_refs") or {}
        require(command_refs.get("gateway_ack_is_final_state") is False, f"{stage_id}: gateway final flag mismatch")
        if stage_id == "S3":
            require(str(command_refs.get("audit")).startswith("command-audit://"), "S3: command audit ref missing")
            require(not command_refs.get("readback"), "S3: readback must be absent before final readback")
            require(command_refs.get("reconciliation") is None, "S3: reconciliation must be absent before final readback")
        if stage_id == "S4":
            require(str(command_refs.get("audit")).startswith("command-audit://"), "S4: command audit ref missing")
            require(command_refs.get("readback") == [order_ref], "S4: readback ref mismatch")
            require(str(command_refs.get("reconciliation")).startswith("reconcile://"), "S4: reconcile ref missing")

    require(seen == set(expected), f"stage set mismatch: {seen}")


def validate_cancel_request(payload: dict[str, Any]) -> None:
    cancel = payload["cancel_request"]
    require(cancel["schema_version"] == "account_command.cancel_intent.v1", "cancel schema mismatch")
    require(cancel["account_id"] == "acct.ctp.paper.19053", "cancel account mismatch")
    require(cancel["mode"] == "paper_armed", "cancel mode mismatch")
    require(cancel["action"] == "cancel", "cancel action mismatch")
    require(cancel["venue_order_id"] == "ctp19053-p024-partial-order-001", "cancel venue identity mismatch")
    require(cancel["order_ref"] == "37", "cancel order_ref mismatch")
    require(cancel["front_id"] == 1, "cancel front_id mismatch")
    require(cancel["session_id"] == 1, "cancel session_id mismatch")
    require(
        cancel["readback_ref"] == "readback://p024/openctp19053/partial-fill-cancel/s2/order",
        "cancel readback ref mismatch",
    )
    require(str(cancel["idempotency_key"]).startswith("p024-ui-cancel-"), "cancel idempotency mismatch")
    require(cancel["raw_secret_values_recorded"] is False, "cancel raw secret flag mismatch")
    require(cancel["raw_broker_endpoint_recorded"] is False, "cancel endpoint flag mismatch")


def validate_command_artifacts(payload: dict[str, Any]) -> None:
    artifacts = payload["command_artifacts"]
    for key, prefix in [
        ("cancel_intent_ref", "api://p024/"),
        ("risk_decision_ref", "risk://"),
        ("approval_decision_ref", "approval://"),
        ("gateway_event_ref", "gateway://"),
        ("s3_cancel_pending_ref", "command-audit://"),
        ("s4_readback_ref", "readback://"),
        ("s4_reconciliation_ref", "reconcile://"),
    ]:
        require(str(artifacts.get(key)).startswith(prefix), f"command artifact {key} mismatch")
    require(artifacts["gateway_ack_is_final_state"] is False, "gateway final flag mismatch")
    require(artifacts["gateway_send_attempted_from_browser_test"] is False, "browser gateway send flag mismatch")
    require(artifacts["broker_order_created_from_browser_test"] is False, "browser broker order flag mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    for phrase in [
        "account-order-filled-quantity",
        "account-order-remaining-quantity",
        "account-order-cancelled-quantity",
        "account-order-partial-fill-row",
        "account-remaining-cancel-quantity",
        "account-cancel-pending-ref",
        "account-command-readback-ref",
        "account-command-reconciliation-ref",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in [
        "p024-partial-fill-display.png",
        "p024-cancel-pending-display.png",
        "p024-cancelled-display.png",
        "partial_cancel_display_checks",
        "gateway_ack_is_not_final_state",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    for screenshot in REQUIRED_SCREENSHOTS:
        require((EVIDENCE_DIR / screenshot).exists(), f"missing browser screenshot: {screenshot}")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    payload = load(ORDER_DISPLAY)
    validate_order_display(payload)
    validate_cancel_request(payload)
    validate_command_artifacts(payload)
    validate_frontend_hooks()
    print(
        "P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK: "
        "ui_order_display=pass partial_cancel_display=pass runtime_partial_fill=typed_blocker"
    )


if __name__ == "__main__":
    main()
