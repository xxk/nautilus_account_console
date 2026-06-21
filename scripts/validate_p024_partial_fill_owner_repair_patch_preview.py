from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = Path("D:/Nautilus/nautilus_ctp_adapter")
PREVIEW = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-patch-preview.json"
)


class P024OwnerRepairPatchPreviewError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRepairPatchPreviewError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    payload = load_json(PREVIEW)
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-patch-preview.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4x_owner_repair_patch_preview_ready", "status mismatch")
    require(payload["verdict"] == "patch_preview_ready_owner_write_not_authorized", "verdict mismatch")

    baseline = payload["owner_baseline"]
    require(baseline["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(baseline["owner_repo_write_attempted_by_preview"] is False, "preview must not write owner repo")
    files = {item["path"]: item for item in baseline["baseline_files"]}
    require(
        set(files) == {"scripts/ctp_guarded_paper_order_loop.py", "tests/test_guarded_paper_order_loop.py"},
        "baseline file set mismatch",
    )
    for rel_path, item in files.items():
        path = OWNER_ROOT / rel_path
        require(path.exists(), f"owner baseline file missing: {rel_path}")
        text = path.read_text(encoding="utf-8")
        require(item["sha256"] == sha256(path), f"baseline checksum mismatch: {rel_path}")
        for phrase in item["required_current_text"]:
            require(phrase in text, f"baseline phrase missing in {rel_path}: {phrase}")

    patches = {item["patch_id"]: item for item in payload["previewed_owner_patch"]}
    require(
        set(patches)
        == {
            "generalize_close_offset_submit_observed",
            "expand_owner_rule_wording",
            "add_close_yesterday_focused_test",
        },
        "preview patch set mismatch",
    )
    generalize = patches["generalize_close_offset_submit_observed"]
    require(generalize["target_symbol"] == "build_close_offset_owner_rule_semantics", "generalize target mismatch")
    for phrase in [
        "close_offset_submit_observed",
        "CLOSEYESTERDAY",
        "expected_offset == \"4\"",
        "submit_offset == \"4\"",
    ]:
        require(any(phrase in item for item in generalize["required_new_text"]), f"generalize required text missing: {phrase}")
    test_patch = patches["add_close_yesterday_focused_test"]
    require(
        test_patch["target_symbol"] == "test_close_yesterday_owner_rule_blocks_callback_offset_as_submit_truth",
        "focused test target mismatch",
    )
    for phrase in [
        "position_effect=\"CLOSEYESTERDAY\"",
        "expected_submit_offset_from_position_effect\"] == \"4\"",
        "callback_offset_flags\"] == [\"1\"]",
    ]:
        require(phrase in test_patch["required_new_text"], f"focused test required text missing: {phrase}")

    validators = {item["evidence_id"]: item for item in payload["post_patch_required_validators"]}
    require(
        set(validators)
        == {
            "owner_focus_validator_result",
            "owner_integration_validator_result",
            "account_console_ingest_gate_still_rejects_until_evidence_recorded",
        },
        "validator set mismatch",
    )
    for item in validators.values():
        require(item["required_exit_code"] == 0, f"validator exit requirement mismatch: {item['evidence_id']}")
    gate = payload["post_patch_runtime_gate"]
    require(gate["runtime_retry_authorized_by_preview"] is False, "preview authorized runtime retry")
    require(gate["fresh_runtime_retry_approval_required_after_patch"] is True, "fresh approval requirement missing")
    require(gate["maximum_runtime_attempts_after_repair"] == 1, "runtime attempt limit mismatch")

    forbidden = set(payload["forbidden_preview_shapes"])
    require("do not write owner repo from this preview" in forbidden, "owner write forbidden shape missing")
    require("do not run OpenCTP runtime scripts from this preview" in forbidden, "runtime forbidden shape missing")
    negative = payload["negative_assertions"]
    for key in [
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
        "P024_PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW_OK: "
        "preview_ready=true owner_write=false runtime_retry=false"
    )


if __name__ == "__main__":
    main()
