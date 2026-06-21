from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-approval-packet.json"
)
OWNER_REPO = Path("D:/Nautilus/nautilus_ctp_adapter")
OWNER_CONFIG = OWNER_REPO / "cfgs" / "local" / "ctp.openctp.tts.7x24.local.json"
OWNER_ORDER_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_order_loop.py"
OWNER_CANCEL_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_cancel_loop.py"


class P024PartialFillRuntimeExecutionApprovalPacketError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRuntimeExecutionApprovalPacketError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def scan_forbidden_text() -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    text = PACKET.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-runtime-execution-approval-packet.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4j_partial_fill_runtime_execution_approval_packet_ready", "status mismatch")
    require(payload["verdict"] == "approval_packet_ready_runtime_not_invoked", "verdict mismatch")

    owner = payload["owner_runtime"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(owner["config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", "config ref mismatch")
    require(owner["config_file_exists_on_owner_node"] is True, "config existence flag mismatch")
    require(OWNER_CONFIG.exists(), "owner config missing; validator checks existence only")
    for key in ["config_raw_content_read", "raw_secret_values_recorded", "raw_broker_endpoint_recorded"]:
        require(owner[key] is False, f"owner flag mismatch: {key}")

    approval = payload["required_operator_approval"]
    require(approval["required"] is True, "approval required mismatch")
    require(approval["obtained"] is False, "approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require("P024 partial-fill acceptance" in approval["exact_approval_text"], "approval text scope mismatch")
    require("up to one small exposure-reduction paper order" in approval["exact_approval_text"], "approval text impact mismatch")
    require(approval["approval_prompt_required_before_execution"] is True, "approval prompt mismatch")

    planned = payload["planned_execution"]
    require(planned["runtime_invocation_attempted"] is False, "runtime invocation mismatch")
    require(planned["owner_repo_write_attempted"] is False, "owner write mismatch")
    require(planned["new_order_submitted"] is False, "new order flag mismatch")
    require(planned["cancel_sent"] is False, "cancel sent flag mismatch")
    for ref_key in ["predecessor_attempt_ref", "partial_fill_feasibility_ref", "owner_artifact_scan_ref"]:
        require(planned[ref_key].startswith("docs/acceptance/p024-account-console-paper-command-controls/"), f"{ref_key} mismatch")

    require(OWNER_ORDER_SCRIPT.exists(), "owner submit script missing")
    require(OWNER_CANCEL_SCRIPT.exists(), "owner cancel script missing")
    entrypoints = {entry["action"]: entry for entry in payload["entrypoints"]}
    require(entrypoints["submit"]["checksum"] == sha256(OWNER_ORDER_SCRIPT), "submit checksum mismatch")
    require(entrypoints["cancel"]["checksum"] == sha256(OWNER_CANCEL_SCRIPT), "cancel checksum mismatch")
    require(entrypoints["submit"]["armed_flag"] == "--arm-paper-send", "submit arm flag mismatch")
    require(entrypoints["cancel"]["armed_flag"] == "--arm-cancel-send", "cancel arm flag mismatch")

    constraints = payload["attempt_constraints"]
    require(constraints["risk_shape"] == "exposure_reduction_only", "risk shape mismatch")
    require(constraints["preferred_instrument"] == "rb2610", "instrument mismatch")
    require(constraints["maximum_submit_attempts"] == 1, "maximum submit attempts mismatch")
    require(constraints["maximum_order_quantity"] == 3, "maximum quantity mismatch")
    require(constraints["requires_fresh_pre_snapshot"] is True, "fresh snapshot mismatch")
    require(constraints["requires_reducible_position_before_submit"] is True, "reducible position mismatch")
    require(constraints["requires_owner_readback_identity_for_cancel"] is True, "cancel identity mismatch")
    require(constraints["partial_fill_success_formula"] == "0 < filled_quantity < submitted_quantity", "partial formula mismatch")
    require("do not retry without fresh approval" in constraints["fallback_if_no_partial_fill"], "fallback mismatch")

    commands = {command["action"]: command for command in payload["command_templates"]}
    for action, arm_flag in {"submit": "--arm-paper-send", "cancel": "--arm-cancel-send"}.items():
        template = commands[action]["template"]
        require(arm_flag in template, f"{action} arm flag missing")
        require("<" in template and ">" in template, f"{action} template placeholders missing")
        require(commands[action]["uses_placeholders_only_for_runtime_values"] is True, f"{action} placeholder flag mismatch")
        require(commands[action]["runtime_invocation_attempted"] is False, f"{action} invocation mismatch")

    required_artifacts = set(payload["required_post_run_artifacts"])
    for artifact in [
        "pre_snapshot_with_reducible_position.json",
        "trade_callback_or_trade_readback.json",
        "partial_fill_closeout_manifest.json",
        "redaction_report.json",
    ]:
        require(artifact in required_artifacts, f"missing artifact: {artifact}")
    gates = set(payload["post_run_acceptance_gates"])
    for gate in [
        "python scripts\\validate_p024_partial_fill_runtime_feasibility_audit.py",
        "python scripts\\validate_p024_partial_fill_owner_artifact_scan.py",
        "python scripts\\validate_p024_partial_fill_cancel_browser_evidence.py",
        "python scripts\\validate_p024_paper_command_controls_design.py",
    ]:
        require(gate in gates, f"missing post-run gate: {gate}")

    blockers = {blocker["blocker_id"] for blocker in payload["blockers"]}
    require(
        blockers
        == {"p024_partial_fill_operator_approval_not_obtained", "p024_partial_fill_runtime_artifacts_missing"},
        "blocker set mismatch",
    )
    negative = payload["negative_assertions"]
    for key in [
        "approval_obtained",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "new_order_submitted",
        "cancel_sent",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
        "full_acceptance_claimed",
        "browser_fixture_promoted_to_runtime_truth",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(PACKET))
    print(
        "P024_PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET_OK: "
        "approval_required=true approval_obtained=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
