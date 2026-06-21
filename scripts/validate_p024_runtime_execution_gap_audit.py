from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GAP_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "runtime-execution-gap-audit.json"
)
FULL_CLOSEOUT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "full-acceptance-closeout.json"
)


class P024RuntimeExecutionGapAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeExecutionGapAuditError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text() -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    payload = GAP_AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment.lower() in payload]


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.runtime-execution-gap-audit.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4e_final_runtime_execution_gap_audited", "status mismatch")
    require(payload["verdict"] == "blocked_pending_owner_runtime_execution", "verdict mismatch")
    require(
        payload["goal_state"] == "all_acceptance_requires_owner_runtime_execution_artifacts",
        "goal state mismatch",
    )
    require(set(payload["accepted_scenarios"]) == {f"A{index}" for index in range(1, 16)} - {"A4"}, "accepted scenario set mismatch")
    not_accepted = {item["id"]: item for item in payload["not_accepted_scenarios"]}
    require(set(not_accepted) == {"A4"}, "not accepted scenario set mismatch")
    require(
        not_accepted["A4"]["current_status"] == "blocked_pending_owner_runtime_execution",
        "A4 status mismatch",
    )
    require(
        set(not_accepted["A4"]["blocker_refs"])
        == {"p024_external_owner_runtime_write_approval_required", "p024_owner_runtime_artifacts_missing"},
        "A4 blocker refs mismatch",
    )

    approval = payload["external_write_approval"]
    require(approval["required"] is True, "approval required mismatch")
    require(approval["obtained"] is False, "approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(
        "I approve writes to D:/Nautilus/nautilus_ctp_adapter" in approval["exact_approval_text"],
        "exact approval text missing",
    )

    owner = payload["owner_runtime_refs"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(owner["config_raw_content_read"] is False, "raw config flag mismatch")
    require(owner["submit_entrypoint_ref"] == "scripts/ctp_guarded_paper_order_loop.py", "submit entrypoint mismatch")
    require(owner["cancel_entrypoint_ref"] == "scripts/ctp_guarded_paper_cancel_loop.py", "cancel entrypoint mismatch")

    required_artifacts = set(payload["required_owner_artifacts"])
    for artifact in [
        "submit_intent.json",
        "submit_risk_decision.json",
        "submit_approval_decision.json",
        "submit_gateway_event.json",
        "post_submit_readback.json",
        "cancel_intent.json",
        "cancel_risk_decision.json",
        "cancel_approval_decision.json",
        "cancel_gateway_event.json",
        "post_cancel_readback.json",
        "reconciliation_result.json",
        "redaction_report.json",
        "command_audit.json",
        "closeout_manifest.json",
    ]:
        require(artifact in required_artifacts, f"missing required owner artifact: {artifact}")

    blockers = {blocker["blocker_id"]: blocker for blocker in payload["residual_blockers"]}
    require(
        set(blockers)
        == {
            "p024_external_owner_runtime_write_approval_required",
            "p024_owner_runtime_artifacts_missing",
            "p024_real_partial_fill_runtime_missing",
        },
        "residual blockers mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "final_acceptance_claimed",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")

    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_claim_all_acceptance_complete",
        "does_not_invoke_owner_runtime",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_create_broker_order",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_use_screenshot_as_order_or_runtime_truth",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_against_full_closeout(payload: dict[str, Any]) -> None:
    closeout = load(FULL_CLOSEOUT)
    scenarios = {item["id"]: item for item in closeout["scenario_matrix"]}
    require(scenarios["A4"]["status"] == "blocked_pending_owner_runtime_execution", "closeout A4 drifted")
    closeout_blockers = {item["blocker_id"] for item in closeout["residual_blockers"]}
    gap_blockers = {item["blocker_id"] for item in payload["residual_blockers"]}
    require(gap_blockers == closeout_blockers, "gap blockers must match full closeout blockers")
    negative = closeout["negative_assertions"]
    require(negative["runtime_invocation_attempted"] is False, "closeout runtime invocation drifted")
    require(negative["owner_repo_write_attempted"] is False, "closeout owner write drifted")
    require(negative["full_runtime_acceptance_claimed"] is False, "closeout full acceptance claim drifted")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    payload = load(GAP_AUDIT)
    validate_payload(payload)
    validate_against_full_closeout(payload)
    print(
        "P024_RUNTIME_EXECUTION_GAP_AUDIT_OK: "
        "verdict=blocked_pending_owner_runtime_execution final_acceptance_claimed=false"
    )


if __name__ == "__main__":
    main()
