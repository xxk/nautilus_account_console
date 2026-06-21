from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCAN = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-artifact-scan.json"
)


class P024PartialFillOwnerArtifactScanError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerArtifactScanError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text() -> list[str]:
    fragments = [
        "password",
        "authcode",
        "auth_code",
        "tcp://",
        "trading.openctp",
        "frontaddress",
        "broker_secret",
        "account_secret",
    ]
    payload = SCAN.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in payload]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-artifact-scan.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4i_owner_artifact_partial_fill_scan_complete_no_candidate",
        "status mismatch",
    )
    require(
        payload["verdict"] == "no_qualifying_partial_fill_then_cancel_owner_artifact_found",
        "verdict mismatch",
    )

    scope = payload["scan_scope"]
    require(scope["raw_secret_values_recorded"] is False, "raw secret flag mismatch")
    require(scope["raw_broker_endpoint_recorded"] is False, "raw endpoint flag mismatch")
    require("nautilus_account_console/output" in scope["account_console_root"], "account console root mismatch")
    require("nautilus_ctp_adapter/output" in scope["owner_runtime_root"], "owner runtime root mismatch")

    result = payload["scan_result"]
    require(result["order_like_record_count"] >= 50, "scan coverage too small")
    require(result["partial_fill_candidate_count"] == 0, "partial-fill candidate count mismatch")
    require(result["cancelled_with_fill_candidate_count"] == 0, "cancelled-with-fill candidate count mismatch")
    require(result["qualifying_partial_fill_then_cancel_count"] == 0, "qualifying candidate count mismatch")

    rule = payload["qualification_rule"]
    for key in [
        "same_order_identity_required",
        "same_native_order_identity_required",
        "requires_trade_volume_between_zero_and_submitted_quantity",
        "requires_cancelled_remaining_quantity_after_fill",
        "requires_stable_trade_readback_or_trade_callback",
        "requires_readback_or_reconciliation_ref",
    ]:
        require(rule[key] is True, f"qualification rule mismatch: {key}")

    rejected = {candidate["candidate_id"]: candidate for candidate in payload["rejected_near_candidates"]}
    require(
        set(rejected)
        == {
            "p023-rb2610-order-166",
            "p077-rb2610-order-183",
            "p077-rb2610-order-232",
            "p024-rb2610-partial-attempt-20260621T174616",
        },
        "near candidate set mismatch",
    )
    require(rejected["p023-rb2610-order-166"]["observed_trade_volume"] == 0, "P023 trade volume mismatch")
    require(
        rejected["p023-rb2610-order-166"]["rejection_reason"] == "cancelled_without_fill_not_partial_fill",
        "P023 rejection reason mismatch",
    )
    for candidate_id in ["p077-rb2610-order-183", "p077-rb2610-order-232"]:
        require(rejected[candidate_id]["observed_trade_volume"] == 1, f"{candidate_id} trade volume mismatch")
        require(rejected[candidate_id]["observed_leaves_qty"] == 0, f"{candidate_id} leaves mismatch")
        require(
            rejected[candidate_id]["rejection_reason"] == "fully_filled_not_partial_fill_then_cancel",
            f"{candidate_id} rejection reason mismatch",
        )
    require(
        rejected["p024-rb2610-partial-attempt-20260621T174616"]["observed_trade_volume"] == 0,
        "P024 latest attempt trade volume mismatch",
    )
    require(
        rejected["p024-rb2610-partial-attempt-20260621T174616"]["rejection_reason"]
        == "rejected_before_partial_fill_not_partial_fill",
        "P024 latest attempt rejection reason mismatch",
    )

    impact = payload["acceptance_impact"]
    require(impact["non_ui_partial_fill_runtime_acceptance"] == "blocked", "non-UI impact mismatch")
    require(impact["web_ui_real_partial_fill_runtime_acceptance"] == "blocked", "Web UI impact mismatch")
    require(impact["full_acceptance_claimed"] is False, "full acceptance claim mismatch")
    require(
        payload["residual_blocker"]["blocker_id"] == "p024_real_partial_fill_runtime_missing",
        "residual blocker mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "new_order_submitted_by_scan",
        "cancel_sent_by_scan",
        "browser_fixture_promoted_to_runtime_truth",
        "final_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(SCAN))
    print(
        "P024_PARTIAL_FILL_OWNER_ARTIFACT_SCAN_OK: "
        "verdict=no_qualifying_partial_fill_then_cancel_owner_artifact_found"
    )


if __name__ == "__main__":
    main()
