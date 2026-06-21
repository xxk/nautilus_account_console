from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-feasibility-audit.json"
)


class P024PartialFillRuntimeFeasibilityAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRuntimeFeasibilityAuditError(message)


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
    payload = AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in payload]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-runtime-feasibility-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4h_real_partial_fill_runtime_feasibility_blocked", "status mismatch")
    require(
        payload["verdict"] == "blocked_until_owner_runtime_partial_fill_state_available",
        "verdict mismatch",
    )

    approval = payload["operator_approval_scope"]
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(approval["approved_for_one_submit_cancel_attempt"] is True, "approval scope mismatch")
    require(approval["additional_partial_fill_order_authorized"] is False, "partial fill approval mismatch")

    owner = payload["owner_runtime_refs"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["config_raw_content_recorded"] is False, "config raw content flag mismatch")
    require(owner["submit_entrypoint_ref"] == "scripts/ctp_guarded_paper_order_loop.py", "submit entrypoint mismatch")
    require(owner["cancel_entrypoint_ref"] == "scripts/ctp_guarded_paper_cancel_loop.py", "cancel entrypoint mismatch")

    evidence = payload["current_real_runtime_evidence"]
    require(evidence["owner_patch_commit"] == "6a50b02", "owner patch commit mismatch")
    require(len(evidence["submit_artifact_sha256"]) == 64, "submit artifact checksum mismatch")
    require(len(evidence["cancel_artifact_sha256"]) == 64, "cancel artifact checksum mismatch")
    require(evidence["observed_submit_leaves_qty"] == 1, "submit leaves mismatch")
    require(evidence["observed_cancel_status"] == 5, "cancel status mismatch")
    require(evidence["observed_trade_fill"] is False, "trade fill must remain false")
    require(evidence["observed_partial_fill"] is False, "partial fill must remain false")

    scan = payload["owner_capability_scan"]
    for key in [
        "classifies_order_lifecycle_fill_volume",
        "classifies_order_lifecycle_leaves_qty",
        "classifies_cancel_filled_before_cancel",
        "can_record_trade_callbacks_if_emitted",
    ]:
        require(scan[key] is True, f"owner capability missing: {key}")
    require(scan["deterministic_partial_fill_generator_present"] is False, "partial-fill generator claim mismatch")
    require(scan["stable_owner_partial_fill_artifact_present"] is False, "stable partial artifact claim mismatch")
    artifact_scan = payload["owner_artifact_scan"]
    require(
        artifact_scan["scan_ref"]
        == "docs/acceptance/p024-account-console-paper-command-controls/partial-fill-owner-artifact-scan.json",
        "artifact scan ref mismatch",
    )
    require(
        artifact_scan["validator"] == "python scripts/validate_p024_partial_fill_owner_artifact_scan.py",
        "artifact scan validator mismatch",
    )
    require(artifact_scan["order_like_record_count"] >= 50, "artifact scan coverage mismatch")
    require(
        artifact_scan["qualifying_partial_fill_then_cancel_count"] == 0,
        "artifact scan candidate count mismatch",
    )
    require(
        artifact_scan["scan_verdict"] == "no_qualifying_partial_fill_then_cancel_owner_artifact_found",
        "artifact scan verdict mismatch",
    )

    constraints = payload["risk_and_market_constraints"]
    require(constraints["allowed_risk_shape"] == "exposure_reduction_only", "risk shape mismatch")
    require(constraints["max_safe_order_quantity_from_current_evidence"] == 3, "max safe qty mismatch")
    require(constraints["cannot_force_partial_fill_from_account_console"] is True, "force partial claim mismatch")
    require(constraints["cannot_use_browser_fixture_as_runtime_truth"] is True, "fixture truth mismatch")

    require(len(payload["required_owner_partial_fill_artifacts"]) >= 6, "required artifact set incomplete")
    require(payload["non_ui_acceptance_shape"]["status"] == "blocked", "non-UI status mismatch")
    require(payload["web_ui_acceptance_shape"]["status"] == "blocked", "Web UI status mismatch")
    require(
        payload["residual_blocker"]["blocker_id"] == "p024_real_partial_fill_runtime_missing",
        "residual blocker mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "new_partial_fill_order_submitted_by_this_audit",
        "final_acceptance_claimed",
        "real_partial_fill_runtime_claimed",
        "browser_fixture_promoted_to_runtime_truth",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(AUDIT))
    print(
        "P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT_OK: "
        "verdict=blocked_until_owner_runtime_partial_fill_state_available"
    )


if __name__ == "__main__":
    main()
