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
    / "partial-fill-remaining-acceptance-current-state.json"
)


class P024PartialFillRemainingAcceptanceCurrentStateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRemainingAcceptanceCurrentStateError(message)


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
    text = AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-remaining-acceptance-current-state.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4q_remaining_acceptance_current_state_audited",
        "status mismatch",
    )
    require(
        payload["verdict"] == "not_fully_accepted_pending_owner_repair_and_real_partial_fill",
        "verdict mismatch",
    )

    current = payload["current_authoritative_state"]
    require(current["account_console_worktree_clean_at_review"] is True, "worktree state mismatch")
    require(current["owner_repo_code_change_recorded_for_close_offset_repair"] is False, "owner repair claim mismatch")
    require(current["owner_repo_runtime_artifacts_present"] is True, "owner runtime artifact presence mismatch")
    require(
        current["latest_real_partial_fill_attempt_classification"] == "rejected_before_partial_fill_not_partial_fill",
        "latest partial-fill classification mismatch",
    )
    require(
        current["latest_owner_repair_gate"] == "phase4p_owner_close_offset_repair_approval_packet_ready",
        "latest owner repair gate mismatch",
    )
    require(current["full_acceptance_claimed"] is False, "full acceptance claim mismatch")

    groups = {group["group_id"]: group for group in payload["accepted_evidence_groups"]}
    require(
        set(groups)
        == {
            "api_and_ui_contracts",
            "browser_display_contracts",
            "real_owner_submit_cancel_non_partial_runtime",
            "real_partial_fill_failed_attempt_classification",
        },
        "accepted evidence group set mismatch",
    )
    require(groups["api_and_ui_contracts"]["status"] == "accepted", "api/ui group status mismatch")
    require(
        groups["browser_display_contracts"]["status"] == "accepted_as_browser_contract_not_runtime_truth",
        "browser contract group status mismatch",
    )
    require(
        groups["real_owner_submit_cancel_non_partial_runtime"]["status"]
        == "accepted_for_submit_cancel_callback_closeout_only",
        "submit/cancel runtime group status mismatch",
    )
    require(
        groups["real_partial_fill_failed_attempt_classification"]["status"] == "accepted_as_blocker_evidence",
        "failed partial-fill group status mismatch",
    )

    requirements = {item["requirement_id"]: item for item in payload["remaining_acceptance_requirements"]}
    require(
        set(requirements)
        == {
            "R1_owner_repair_approval",
            "R2_owner_close_offset_repair",
            "R3_owner_validators",
            "R4_post_repair_partial_fill_runtime",
            "R5_web_ui_real_partial_fill_projection",
        },
        "remaining requirement set mismatch",
    )
    for requirement in requirements.values():
        require(requirement["current_status"] == "missing", f"requirement must remain missing: {requirement['requirement_id']}")
    require(
        requirements["R1_owner_repair_approval"]["current_blocker_id"]
        == "p024_owner_repair_approval_not_obtained",
        "repair approval blocker mismatch",
    )
    require(
        requirements["R2_owner_close_offset_repair"]["current_blocker_id"]
        == "p024_close_yesterday_owner_rule_gap",
        "close offset blocker mismatch",
    )
    require(
        "0 < filled_quantity < submitted_quantity"
        in requirements["R4_post_repair_partial_fill_runtime"]["required_evidence_shape"],
        "partial-fill formula missing",
    )
    require(
        "Playwright/browser evidence"
        in requirements["R5_web_ui_real_partial_fill_projection"]["required_evidence_shape"],
        "web ui evidence shape missing",
    )

    action = payload["next_authorized_action"]
    require(action["owner_code_repair_allowed"] is False, "owner repair allowed mismatch")
    require(action["owner_runtime_retry_allowed"] is False, "owner retry allowed mismatch")
    require(action["account_console_only_work_allowed"] is True, "console-only work flag mismatch")
    require(
        "repair owner close-offset semantics for P024"
        in action["required_exact_approval_before_owner_repair_or_retry"],
        "required approval text mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "full_acceptance_claimed",
        "owner_repair_claimed",
        "post_repair_runtime_retry_claimed",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
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
        "P024_PARTIAL_FILL_REMAINING_ACCEPTANCE_CURRENT_STATE_OK: "
        "full_acceptance=false remaining=5 owner_retry_allowed=false"
    )


if __name__ == "__main__":
    main()
