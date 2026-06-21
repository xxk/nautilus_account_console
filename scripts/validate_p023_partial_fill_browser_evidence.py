from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p023-openctp-19053-command"
ORDER_DISPLAY = EVIDENCE_DIR / "partial-fill-order-display.json"
CLOSEOUT = EVIDENCE_DIR / "closeout.json"
REQUIRED_SCREENSHOTS = [
    "disabled-state.png",
    "submit-readback.png",
    "partial-fill-readback.png",
    "blocker-state.png",
    "cancel-readback.png",
]


class P023PartialFillBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P023PartialFillBrowserEvidenceError(message)


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
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "OrderInsert", "OrderAction"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_order_display(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p023.partial-fill-order-display.v1", "schema mismatch")
    require(payload["proposal_id"] == "p023-openctp-19053-paper-command-capability", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["ui13_order_display_verdict"] == "pass", "order display verdict mismatch")
    require(payload["partial_cancel_display_verdict"] == "pass", "partial-cancel display verdict mismatch")
    require(
        payload["ui13_action_control_verdict"] == "typed_blocker_command_controls_disabled",
        "action control blocker mismatch",
    )
    require(
        payload["runtime_partial_fill_verdict"]
        == "typed_blocker_until_real_or_owner_approved_partial_fill_state",
        "runtime partial-fill blocker mismatch",
    )
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_submit_orders",
        "does_not_cancel_orders",
        "does_not_prove_real_openctp_partial_fill_runtime",
        "does_not_use_screenshot_as_order_truth",
        "does_not_enable_command_capability",
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
        require(api["identity"] == "ctp19053-partial-order-001", f"{stage_id}: identity mismatch")
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
        require(str(stage["artifact_ref"]).startswith("readback://"), f"{stage_id}: order artifact ref mismatch")

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
        if stage_id == "S3":
            require(str(browser.get("cancel_pending_ref")).startswith("command-audit://"), "S3: cancel ref missing")

    require(seen == set(expected), f"stage set mismatch: {seen}")


def validate_closeout(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p023.browser-closeout.v1", "closeout schema mismatch")
    require(payload["proposal_id"] == "p023-openctp-19053-paper-command-capability", "closeout proposal mismatch")
    require(
        payload["verdict"] == "browser_order_display_contract_pass_runtime_partial_fill_blocked",
        "closeout verdict mismatch",
    )
    require(payload["command_enabled"] is False, "command must remain disabled")
    require(payload["command_mode"] == "disabled", "command mode mismatch")
    require(
        payload["runtime_partial_fill"] == "blocked_until_real_or_owner_approved_partial_fill_state",
        "runtime partial-fill closeout mismatch",
    )


def main() -> None:
    for screenshot in REQUIRED_SCREENSHOTS:
        require((EVIDENCE_DIR / screenshot).exists(), f"missing browser screenshot: {screenshot}")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive/action fragments found: {leaks}")
    validate_order_display(load(ORDER_DISPLAY))
    validate_closeout(load(CLOSEOUT))
    print(
        "P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK: "
        "ui_order_display=pass partial_cancel_display=pass runtime_partial_fill=typed_blocker"
    )


if __name__ == "__main__":
    main()
