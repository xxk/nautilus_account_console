from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "p024-account-console-paper-command-controls"
BUNDLE = EVIDENCE_DIR / "partial-fill-runtime-execution-handoff-bundle.json"
APPROVAL_PACKET = EVIDENCE_DIR / "partial-fill-runtime-execution-approval-packet.json"
ARTIFACT_SCAN = EVIDENCE_DIR / "partial-fill-owner-artifact-scan.json"


class P024PartialFillRuntimeExecutionHandoffBundleError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRuntimeExecutionHandoffBundleError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text() -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    text = BUNDLE.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any], approval: dict[str, Any], scan: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4k_partial_fill_runtime_execution_handoff_bundle_ready", "status mismatch")
    require(payload["verdict"] == "handoff_bundle_ready_runtime_not_invoked", "verdict mismatch")

    depends = payload["depends_on"]
    require(depends["approval_packet_schema"] == approval["schema"], "approval schema dependency mismatch")
    require(depends["approval_packet_status"] == approval["status"], "approval status dependency mismatch")
    require(depends["owner_artifact_scan_verdict"] == scan["verdict"], "artifact scan dependency mismatch")

    guard = payload["execution_guard"]
    require(guard["execution_allowed"] is False, "execution allowed mismatch")
    require(guard["approval_required"] is True, "approval required mismatch")
    require(guard["approval_obtained"] is False, "approval obtained mismatch")
    require(guard["exact_approval_text_required"] == approval["required_operator_approval"]["exact_approval_text"], "approval text mismatch")
    for key in ["raw_secret_values_recorded", "raw_broker_endpoint_recorded", "config_raw_content_read"]:
        require(guard[key] is False, f"guard flag mismatch: {key}")

    inputs = {item["field"]: item for item in payload["runtime_input_requirements"]}
    for field in [
        "fresh_owner_pre_snapshot_ref",
        "quantity",
        "risk_reviewed_limit_price",
        "owner_post_submit_order_identity",
    ]:
        require(field in inputs, f"runtime input missing: {field}")
        require(inputs[field]["required"] is True, f"runtime input not required: {field}")
    require(inputs["quantity"]["allowed_values"] == [2, 3], "quantity allowed values mismatch")

    steps = [item["step"] for item in payload["operator_sequence"]]
    require(
        steps
        == [
            "pre_approval_gate",
            "owner_pre_snapshot",
            "submit_partial_fill_attempt",
            "classify_submit_lifecycle",
            "cancel_remaining_if_identity_available",
            "post_cancel_readback",
            "ingest_or_preserve_blocker",
        ],
        "operator sequence mismatch",
    )
    for item in payload["operator_sequence"]:
        require(item["must_pass_before_next"] is True, f"step not gated: {item['step']}")

    criteria = payload["success_criteria"]
    for phrase in [
        "0 < filled_quantity < submitted_quantity",
        "filled_quantity + cancelled_quantity == submitted_quantity",
        "remaining_quantity == 0 after terminal cancel readback",
    ]:
        require(phrase in criteria["non_ui_runtime"], f"missing non-UI criterion: {phrase}")
    require("cancel pending is not rendered as final" in criteria["web_ui_runtime"], "missing Web UI criterion")

    require(
        set(payload["fallback_classifications"])
        == {
            "fully_filled_not_partial_fill_then_cancel",
            "cancelled_without_fill_not_partial_fill",
            "rejected_or_timeout_not_partial_fill",
            "owner_runtime_artifact_incomplete",
        },
        "fallback classifications mismatch",
    )
    negative = payload["negative_assertions"]
    for key in [
        "execution_allowed",
        "approval_obtained",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "new_order_submitted",
        "cancel_sent",
        "full_acceptance_claimed",
        "browser_fixture_promoted_to_runtime_truth",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(BUNDLE), load(APPROVAL_PACKET), load(ARTIFACT_SCAN))
    print(
        "P024_PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK: "
        "execution_allowed=false approval_obtained=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
