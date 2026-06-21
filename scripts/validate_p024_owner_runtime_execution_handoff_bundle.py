from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "p024-account-console-paper-command-controls"
BUNDLE = EVIDENCE_DIR / "owner-runtime-execution-handoff-bundle.json"
APPROVAL_PACKET = EVIDENCE_DIR / "owner-runtime-execution-approval-packet.json"
UI_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-approval-packet-ui.json"
)
PROPOSAL = ROOT / "docs" / "proposals" / "p024-account-console-paper-command-controls"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"


class P024OwnerRuntimeExecutionHandoffBundleError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRuntimeExecutionHandoffBundleError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def scan_forbidden_text(paths: list[Path]) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    matches: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(path))
    return matches


def validate_payload(payload: dict[str, Any], approval_packet: dict[str, Any], ui_evidence: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready", "status mismatch")
    require(payload["verdict"] == "handoff_bundle_ready_runtime_not_invoked", "verdict mismatch")

    depends = payload["depends_on"]
    require(depends["approval_packet_schema"] == approval_packet["schema"], "approval packet schema dependency mismatch")
    require(depends["approval_packet_status"] == approval_packet["status"], "approval packet status dependency mismatch")
    require(depends["approval_packet_ui_status"] == "phase4b_runtime_approval_packet_ui_projection_passed", "UI status dependency mismatch")
    require(ui_evidence["schema"] == "account-console.p024.runtime-approval-packet-ui.v1", "UI evidence schema mismatch")
    require(ui_evidence["verdict"] == "pass", "UI evidence verdict mismatch")

    guard = payload["execution_guard"]
    approval = approval_packet["required_operator_approval"]
    require(guard["execution_allowed"] is False, "execution must not be allowed before approval")
    require(guard["approval_required"] is True, "approval required mismatch")
    require(guard["approval_obtained"] is False, "approval obtained mismatch")
    require(guard["exact_approval_text_required"] == approval["exact_approval_text"], "exact approval text mismatch")
    require(guard["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner repo path mismatch")
    for key in ["raw_secret_values_recorded", "raw_broker_endpoint_recorded", "config_raw_content_read"]:
        require(guard[key] is False, f"guard flag mismatch: {key}")

    required_inputs = {item["field"]: item for item in payload["runtime_input_requirements"]}
    for field in [
        "owner_pre_snapshot_ref",
        "owner_post_snapshot_ref",
        "instrument",
        "side",
        "qty",
        "price",
        "readback_order_identity",
    ]:
        require(field in required_inputs, f"runtime input missing: {field}")
        require(required_inputs[field]["required"] is True, f"runtime input not required: {field}")

    steps = [item["step"] for item in payload["operator_sequence"]]
    require(
        steps
        == [
            "pre_approval_gate",
            "owner_repo_context",
            "submit_runtime",
            "submit_readback",
            "cancel_runtime",
            "post_run_ingest",
            "browser_closeout",
        ],
        "operator sequence mismatch",
    )
    for item in payload["operator_sequence"]:
        require(item["must_pass_before_next"] is True, f"operator sequence step is not gated: {item['step']}")
    submit = next(item for item in payload["operator_sequence"] if item["step"] == "submit_runtime")
    cancel = next(item for item in payload["operator_sequence"] if item["step"] == "cancel_runtime")
    require(submit["armed_flag"] == "--arm-paper-send", "submit arm flag mismatch")
    require(cancel["armed_flag"] == "--arm-cancel-send", "cancel arm flag mismatch")

    required_artifacts = set(payload["required_owner_artifacts"])
    approval_artifacts = set(approval_packet["required_post_run_artifacts"])
    require(required_artifacts == approval_artifacts, "required owner artifacts differ from approval packet")
    for gate in [
        "python scripts\\validate_p024_owner_runtime_execution_approval_packet.py",
        "python scripts\\validate_p024_owner_runtime_execution_handoff_bundle.py",
        "python scripts\\validate_p024_runtime_closeout_browser_evidence.py",
        "python scripts\\validate_p024_partial_fill_cancel_browser_evidence.py",
        "python scripts\\validate_p024_full_acceptance_closeout.py",
        "python scripts\\validate_p024_paper_command_controls_design.py",
    ]:
        require(gate in payload["post_handoff_gates"], f"missing post-handoff gate: {gate}")

    blockers = {item["type"] for item in payload["blockers"]}
    require(
        blockers == {"external_write_approval_required", "runtime_inputs_required", "owner_runtime_artifacts_missing"},
        "blocker type set mismatch",
    )
    negative = payload["negative_assertions"]
    for key in [
        "execution_allowed",
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
        "full_runtime_acceptance_claimed",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")
    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_create_broker_order",
        "does_not_guess_runtime_inputs",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_real_runtime_execution",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_docs() -> None:
    combined = "\n".join(
        read(path)
        for path in [
            PROPOSAL / "README.md",
            PROPOSAL / "acceptance.md",
            PROPOSAL / "phase-plan.md",
            PROPOSAL / "runtime-invocation-readiness.md",
            PROPOSAL_INDEX,
            ADR,
        ]
    )
    for phrase in [
        "phase4c_owner_runtime_execution_handoff_bundle_ready",
        "owner-runtime execution handoff bundle",
        "P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK",
        "handoff_bundle_ready_runtime_not_invoked",
        "owner-runtime-execution-handoff-bundle.json",
    ]:
        require(phrase in combined, f"docs missing phrase: {phrase}")


def main() -> None:
    leaks = scan_forbidden_text([BUNDLE, PROPOSAL / "runtime-invocation-readiness.md"])
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(BUNDLE), load(APPROVAL_PACKET), load(UI_EVIDENCE))
    validate_docs()
    print(
        "P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK: "
        "status=phase4c_owner_runtime_execution_handoff_bundle_ready "
        "execution_allowed=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
