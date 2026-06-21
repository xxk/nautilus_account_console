from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-approval-packet.json"
)
GAP_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-close-offset-owner-rule-gap-audit.json"
)


class P024PartialFillOwnerRepairApprovalPacketError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairApprovalPacketError(message)


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
    text = PACKET.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any], gap_audit: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-approval-packet.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4p_owner_close_offset_repair_approval_packet_ready",
        "status mismatch",
    )
    require(
        payload["verdict"] == "owner_repair_approval_required_before_retry",
        "verdict mismatch",
    )

    depends = payload["depends_on"]
    require(
        depends["gap_audit_ref"]
        == "docs/acceptance/p024-account-console-paper-command-controls/partial-fill-close-offset-owner-rule-gap-audit.json",
        "gap audit dependency mismatch",
    )
    require(depends["gap_audit_status"] == gap_audit["status"], "gap audit status dependency mismatch")
    require(len(depends["latest_owner_attempt_result_sha256"]) == 64, "latest attempt checksum mismatch")

    assessment = payload["current_thread_approval_assessment"]
    require(assessment["approval_text_observed"] is True, "observed approval flag mismatch")
    require(assessment["approval_scope"] == "owner_runtime_script_execution_only", "approval scope mismatch")
    require(assessment["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(assessment["matches_current_next_action"] is False, "approval match flag mismatch")
    require(assessment["runtime_retry_authorized_by_this_packet"] is False, "runtime retry flag mismatch")
    require(assessment["owner_code_repair_authorized_by_this_packet"] is False, "owner repair flag mismatch")

    approval = payload["required_owner_repair_approval"]
    require(approval["required"] is True, "repair approval required mismatch")
    require(approval["obtained"] is False, "repair approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "repair approval path mismatch")
    required_text = approval["exact_approval_text_required"]
    require("repair owner close-offset semantics for P024" in required_text, "repair approval text missing scope")
    require("only after validators pass" in required_text, "repair approval text missing validator gate")
    require("at most one additional guarded OpenCTP paper partial-fill attempt" in required_text, "repair approval text missing retry limit")

    scope = payload["required_owner_repair_scope"]
    require(scope["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(scope["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner repo path mismatch")
    require(len(scope["expected_owner_changes"]) == 3, "owner change count mismatch")
    require(
        "python -m pytest tests/test_guarded_paper_order_loop.py -q"
        in scope["required_owner_validators_before_retry"],
        "guarded owner validator missing",
    )
    require(
        "python -m pytest tests/test_nautilus_integration.py -q"
        in scope["required_owner_validators_before_retry"],
        "integration owner validator missing",
    )
    require(len(scope["required_account_console_followup_before_retry"]) == 3, "console followup count mismatch")

    retry = payload["retry_gate"]
    require(retry["additional_partial_fill_order_authorized"] is False, "additional order flag mismatch")
    require(retry["runtime_invocation_allowed"] is False, "runtime invocation flag mismatch")
    require(retry["owner_repair_required_first"] is True, "owner repair required flag mismatch")
    require(retry["owner_repair_evidence_required"] is True, "owner repair evidence flag mismatch")
    require(retry["fresh_post_repair_runtime_attempt_approval_required"] is True, "fresh approval flag mismatch")

    blockers = {blocker["blocker_id"]: blocker for blocker in payload["residual_blockers"]}
    require(
        set(blockers)
        == {
            "p024_owner_repair_approval_not_obtained",
            "p024_close_yesterday_owner_rule_gap",
            "p024_real_partial_fill_runtime_missing",
        },
        "blocker set mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "owner_repo_write_attempted_by_this_packet",
        "owner_runtime_invocation_attempted",
        "owner_code_repair_authorized_by_current_thread_text",
        "additional_order_authorized",
        "partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(PACKET), load(GAP_AUDIT))
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET_OK: "
        "repair_approval_required=true runtime_retry_authorized=false"
    )


if __name__ == "__main__":
    main()
