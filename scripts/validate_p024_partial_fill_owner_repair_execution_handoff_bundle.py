from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-execution-handoff-bundle.json"
)
PATCH_PREVIEW = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-patch-preview.json"
)
INGEST_GATE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-evidence-ingest-gate.json"
)


class P024OwnerRepairExecutionHandoffBundleError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRepairExecutionHandoffBundleError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load_json(HANDOFF)
    preview = load_json(PATCH_PREVIEW)
    ingest = load_json(INGEST_GATE)
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-execution-handoff-bundle.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4z_owner_repair_execution_handoff_bundle_ready", "status mismatch")
    require(payload["verdict"] == "handoff_bundle_ready_owner_write_not_invoked", "verdict mismatch")
    require(payload["depends_on"]["patch_preview_status"] == preview["status"], "patch preview status mismatch")
    require(payload["depends_on"]["ingest_gate_status"] == ingest["status"], "ingest gate status mismatch")

    guard = payload["execution_guard"]
    require(guard["execution_allowed"] is False, "handoff unexpectedly allows execution")
    require(guard["owner_repo_write_allowed_by_this_bundle"] is False, "handoff allowed owner write")
    require(guard["owner_runtime_invocation_allowed_by_this_bundle"] is False, "handoff allowed owner runtime")
    require(guard["runtime_retry_authorized_by_this_bundle"] is False, "handoff authorized runtime retry")
    require(guard["requires_exact_owner_repair_approval"] is True, "exact approval requirement missing")
    require("repair owner close-offset semantics" in guard["required_exact_approval_text"], "approval text missing repair scope")

    owner = payload["owner_repo_context"]
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(owner["baseline_head_ref"] == preview["owner_baseline"]["head_ref"], "baseline head mismatch")
    steps = {item["step"]: item for item in payload["operator_sequence_after_exact_approval"]}
    require(
        set(steps)
        == {
            "confirm_owner_repo_clean_or_preserve_untracked_runtime_artifacts",
            "apply_patch_preview",
            "run_owner_focus_validator",
            "run_owner_integration_validator",
            "record_owner_repair_commit_and_checksums",
            "ingest_owner_repair_evidence_to_account_console",
            "prepare_post_repair_runtime_retry_packet",
        },
        "operator sequence mismatch",
    )
    for step in steps.values():
        require(step["execution_allowed_before_approval"] is False, f"step allowed before approval: {step['step']}")
    require(
        steps["run_owner_focus_validator"]["command"] == "python -m pytest tests/test_guarded_paper_order_loop.py -q",
        "focus validator command mismatch",
    )
    require(
        steps["run_owner_integration_validator"]["command"] == "python -m pytest tests/test_nautilus_integration.py -q",
        "integration validator command mismatch",
    )
    artifacts = set(payload["required_post_handoff_artifacts"])
    require(
        artifacts
        == {
            "owner_repair_commit_ref",
            "guarded_order_loop_source_checksum",
            "focused_owner_tests_checksum",
            "owner_focus_validator_result",
            "owner_integration_validator_result",
            "account_console_ingest_audit",
            "post_repair_runtime_retry_approval_packet",
        },
        "post handoff artifact set mismatch",
    )
    criteria = payload["success_criteria_before_runtime_retry"]
    for phrase in [
        "CLOSEYESTERDAY expected submit offset 4",
        "owner focus validator exits 0",
        "fresh runtime retry approval packet passes",
    ]:
        require(any(phrase in item for item in criteria), f"success criterion missing: {phrase}")
    negative = payload["negative_assertions"]
    for key in [
        "execution_allowed",
        "owner_repo_write_attempted",
        "owner_patch_applied",
        "owner_validator_run_claimed",
        "owner_runtime_invocation_attempted",
        "runtime_retry_authorized",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BUNDLE_OK: "
        "handoff_ready=true owner_write=false runtime_retry=false"
    )


if __name__ == "__main__":
    main()
