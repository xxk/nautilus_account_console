from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLAN = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-implementation-plan.json"
)


class P024PartialFillOwnerRepairImplementationPlanError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairImplementationPlanError(message)


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
    text = PLAN.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-implementation-plan.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4r_owner_close_offset_repair_implementation_plan_ready",
        "status mismatch",
    )
    require(
        payload["verdict"] == "owner_repair_plan_ready_no_owner_write_attempted",
        "verdict mismatch",
    )

    depends = payload["depends_on"]
    require(
        depends["repair_approval_packet_status"] == "phase4p_owner_close_offset_repair_approval_packet_ready",
        "repair approval dependency mismatch",
    )
    require(
        depends["remaining_acceptance_current_state_status"] == "phase4q_remaining_acceptance_current_state_audited",
        "remaining acceptance dependency mismatch",
    )

    context = payload["owner_read_context"]
    require(context["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(context["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner repo path mismatch")
    require(context["owner_repo_write_attempted"] is False, "owner write flag mismatch")
    source_refs = {item["source_id"]: item for item in context["source_refs"]}
    require(
        set(source_refs)
        == {
            "guarded_order_loop_owner_rule",
            "guarded_order_loop_tests",
            "execution_client_mapping",
        },
        "source ref set mismatch",
    )
    require(
        "CLOSEYESTERDAY -> 4" in source_refs["execution_client_mapping"]["observed_current_behavior"],
        "execution mapping observation mismatch",
    )
    require(
        "not CLOSEYESTERDAY offset 4" in source_refs["guarded_order_loop_tests"]["observed_current_behavior"],
        "test gap observation mismatch",
    )

    changes = {item["change_id"]: item for item in payload["planned_owner_changes_after_exact_approval"]}
    require(
        set(changes)
        == {
            "owner_rule_generalize_close_offset_submit_observed",
            "owner_rule_wording_include_close_yesterday",
            "focused_close_yesterday_test",
        },
        "planned change set mismatch",
    )
    require(
        "CLOSEYESTERDAY expected/submit offset 4"
        in changes["owner_rule_generalize_close_offset_submit_observed"]["implementation_shape"],
        "generalization shape mismatch",
    )
    require(
        "callback_offset_rewrites_submit_truth remains false"
        in changes["owner_rule_generalize_close_offset_submit_observed"]["must_preserve"],
        "submit truth preservation missing",
    )
    focused_asserts = set(changes["focused_close_yesterday_test"]["must_assert"])
    for required in [
        "disposition == owner_rule_blocks_callback_offset_as_submit_truth",
        "expected_submit_offset_from_position_effect == 4 for CLOSEYESTERDAY",
        "observed_submit_boundary_offset == 4 for CLOSEYESTERDAY",
        "callback_offset_flags == [1]",
        "callback_sources == [OnRspOrderInsert]",
        "requires_owner_resolution_before_retry is true",
        "writes_truth is false",
    ]:
        require(required in focused_asserts, f"focused test assert missing: {required}")

    validators = {item["stage"]: item for item in payload["post_repair_validator_sequence"]}
    require(
        set(validators)
        == {
            "owner_unit_focus",
            "owner_integration_regression",
            "account_console_repair_plan_gate",
            "account_console_design_gate",
        },
        "validator stage set mismatch",
    )
    for item in validators.values():
        require(item["required_before_retry"] is True, f"validator must be required: {item['stage']}")
    require(
        validators["owner_unit_focus"]["command"] == "python -m pytest tests/test_guarded_paper_order_loop.py -q",
        "owner focus command mismatch",
    )

    runtime = payload["post_repair_runtime_attempt_gate"]
    require(runtime["runtime_attempt_allowed_by_this_plan"] is False, "runtime allowed mismatch")
    require(runtime["fresh_approval_required"] is True, "fresh approval mismatch")
    require(runtime["maximum_additional_attempts_after_repair"] == 1, "retry count mismatch")
    require(runtime["risk_shape"] == "exposure_reduction_only", "risk shape mismatch")
    require(runtime["success_formula"] == "0 < filled_quantity < submitted_quantity", "success formula mismatch")

    forbidden = payload["forbidden_repair_shapes"]
    require(any("do not treat rejected OnRspOrderInsert offset 1 as submit truth" == item for item in forbidden), "callback truth forbidden shape missing")
    require(any("do not downgrade CLOSEYESTERDAY to generic CLOSE" in item for item in forbidden), "downgrade forbidden shape missing")
    require(any("do not run another paper order before owner repair approval" in item for item in forbidden), "retry forbidden shape missing")

    negative = payload["negative_assertions"]
    for key in [
        "owner_repo_write_attempted_by_this_plan",
        "owner_runtime_invocation_attempted",
        "owner_repair_claimed_complete",
        "runtime_retry_authorized",
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
    validate_payload(load(PLAN))
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN_OK: "
        "owner_write=false runtime_retry=false close_yesterday_plan=ready"
    )


if __name__ == "__main__":
    main()
