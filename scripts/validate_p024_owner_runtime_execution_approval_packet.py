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
    / "owner-runtime-execution-approval-packet.json"
)
READINESS = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-invocation-readiness.json"
)
FULL_CLOSEOUT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "full-acceptance-closeout.json"
)
PROPOSAL = ROOT / "docs" / "proposals" / "p024-account-console-paper-command-controls"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"
OWNER_REPO = Path("D:/Nautilus/nautilus_ctp_adapter")
OWNER_CONFIG = OWNER_REPO / "cfgs" / "local" / "ctp.openctp.tts.7x24.local.json"
OWNER_ORDER_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_order_loop.py"
OWNER_CANCEL_SCRIPT = OWNER_REPO / "scripts" / "ctp_guarded_paper_cancel_loop.py"


class P024OwnerRuntimeExecutionApprovalPacketError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRuntimeExecutionApprovalPacketError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def scan_forbidden_text(paths: list[Path]) -> list[str]:
    fragments = [
        "password=",
        "auth_code=",
        "api_key=",
        "secret=",
        "tcp://",
        "trading.openctp",
        "live_armed=true",
    ]
    matches: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(path))
    return matches


def validate_payload(payload: dict[str, Any], readiness: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4a_owner_runtime_execution_approval_packet_ready",
        "status mismatch",
    )
    require(payload["verdict"] == "approval_packet_ready_runtime_not_invoked", "verdict mismatch")

    owner = payload["owner_runtime"]
    ready_owner = readiness["owner_runtime"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(owner["config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", "config ref mismatch")
    require(owner["config_ref"] == ready_owner["config_ref"], "config ref differs from readiness package")
    require(owner["config_file_exists_on_owner_node"] is True, "config existence flag mismatch")
    require(OWNER_CONFIG.exists(), "owner config missing; validator checks existence only")
    for key in ["config_raw_content_read", "raw_secret_values_recorded", "raw_broker_endpoint_recorded"]:
        require(owner[key] is False, f"owner flag mismatch: {key}")

    approval = payload["required_operator_approval"]
    require(approval["required"] is True, "approval required flag mismatch")
    require(approval["obtained"] is False, "approval obtained flag mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require("I approve writes to D:/Nautilus/nautilus_ctp_adapter" in approval["exact_approval_text"], "approval text path missing")
    require("may submit/cancel one paper order" in approval["exact_approval_text"], "approval text impact missing")
    require(any("outside this worktree" in item for item in approval["expected_impact"]), "approval impact missing write scope")
    require(any("19053 simulation account" in item for item in approval["expected_impact"]), "approval impact missing account")
    require(approval["approval_prompt_required_before_execution"] is True, "approval prompt flag mismatch")

    execution = payload["planned_execution"]
    require(execution["execution_root_ref"].startswith("owner-repo://nautilus_ctp_adapter/output/account_command/ctp-paper-19053/"), "execution root mismatch")
    require(execution["debug_root_ref"] == "owner-repo://nautilus_ctp_adapter/output/debug/", "debug root mismatch")
    require(execution["predecessor_readiness_ref"].endswith("owner-runtime-invocation-readiness.json"), "readiness ref mismatch")
    require(execution["predecessor_closeout_ref"].endswith("full-acceptance-closeout.json"), "closeout ref mismatch")
    require(execution["runtime_invocation_attempted"] is False, "runtime invocation flag mismatch")
    require(execution["owner_repo_write_attempted"] is False, "owner write flag mismatch")

    require(OWNER_ORDER_SCRIPT.exists(), "owner submit script missing")
    require(OWNER_CANCEL_SCRIPT.exists(), "owner cancel script missing")
    entrypoints = {entry["action"]: entry for entry in payload["entrypoints"]}
    ready_entrypoints = {entry["action"]: entry for entry in readiness["entrypoints"]}
    require(set(entrypoints) == {"submit", "cancel"}, "entrypoint action set mismatch")
    require(entrypoints["submit"]["checksum"] == sha256(OWNER_ORDER_SCRIPT), "submit checksum mismatch")
    require(entrypoints["cancel"]["checksum"] == sha256(OWNER_CANCEL_SCRIPT), "cancel checksum mismatch")
    for action in ["submit", "cancel"]:
        require(entrypoints[action]["checksum"] == ready_entrypoints[action]["checksum"], f"{action} checksum readiness mismatch")
        require(entrypoints[action]["armed_flag"] == ready_entrypoints[action]["armed_flag"], f"{action} arm flag readiness mismatch")
    require(entrypoints["submit"]["armed_flag"] == "--arm-paper-send", "submit arm flag mismatch")
    require(entrypoints["cancel"]["armed_flag"] == "--arm-cancel-send", "cancel arm flag mismatch")

    commands = {command["action"]: command for command in payload["command_templates"]}
    require(set(commands) == {"submit", "cancel"}, "command template action set mismatch")
    for action, arm_flag in {"submit": "--arm-paper-send", "cancel": "--arm-cancel-send"}.items():
        template = commands[action]["template"]
        require("cfgs/local/ctp.openctp.tts.7x24.local.json" in template, f"{action} config ref missing")
        require(arm_flag in template, f"{action} arm flag missing")
        require("<" in template and ">" in template, f"{action} template lacks placeholders")
        require(commands[action]["uses_placeholders_only_for_runtime_values"] is True, f"{action} placeholder flag mismatch")
        require(commands[action]["runtime_invocation_attempted"] is False, f"{action} invocation flag mismatch")

    required_artifacts = set(payload["required_post_run_artifacts"])
    expected_artifacts = {
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
    }
    require(required_artifacts == expected_artifacts, "post-run artifact set mismatch")
    gates = set(payload["post_run_acceptance_gates"])
    for gate in [
        "python scripts\\validate_p024_owner_runtime_invocation_readiness.py",
        "python scripts\\validate_p024_runtime_closeout_browser_evidence.py",
        "python scripts\\validate_p024_full_acceptance_closeout.py",
        "python scripts\\validate_p024_paper_command_controls_design.py",
    ]:
        require(gate in gates, f"missing post-run gate: {gate}")

    blockers = {blocker["type"] for blocker in payload["blockers"]}
    require(blockers == {"external_write_approval_required", "owner_runtime_artifacts_missing"}, "blocker set mismatch")
    negative = payload["negative_assertions"]
    for key in [
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
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_real_runtime_execution",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_docs() -> None:
    files = [
        PROPOSAL / "README.md",
        PROPOSAL / "acceptance.md",
        PROPOSAL / "phase-plan.md",
        PROPOSAL / "runtime-invocation-readiness.md",
        PROPOSAL_INDEX,
        ADR,
    ]
    combined = "\n".join(read(path) for path in files)
    for phrase in [
        "phase4a_owner_runtime_execution_approval_packet_ready",
        "owner-runtime execution approval packet",
        "P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK",
        "approval_packet_ready_runtime_not_invoked",
        "owner-runtime-execution-approval-packet.json",
        "I approve writes to D:/Nautilus/nautilus_ctp_adapter",
    ]:
        require(phrase in combined, f"docs missing phrase: {phrase}")


def main() -> None:
    leaks = scan_forbidden_text([PACKET, PROPOSAL / "runtime-invocation-readiness.md"])
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(PACKET), load(READINESS))
    require(FULL_CLOSEOUT.exists(), "full closeout missing")
    validate_docs()
    print(
        "P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK: "
        "status=phase4a_owner_runtime_execution_approval_packet_ready "
        "approval_required=true approval_obtained=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
