from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path

from fastapi import HTTPException

from .schemas import (
    CancelIntentRequest,
    CommandApiResult,
    CommandPartialFillRuntimeExecutionApprovalPacket,
    CommandPartialFillRuntimeExecutionHandoffBundle,
    CommandPartialFillOwnerRepairImplementationPlan,
    CommandRuntimeExecutionApprovalPacket,
    CommandRuntimeExecutionGapAudit,
    CommandRuntimeExecutionHandoffBundle,
    CommandRuntimeInvocationReadiness,
    CommandBlocker,
    CommandRuntimeCloseout,
    CommandRuntimeRunRequest,
    OrderIntentRequest,
)


PAPER_ACCOUNT_ID = "acct.ctp.paper.19053"
PROPOSAL_ID = "p024-account-console-paper-command-controls"
ROOT = Path(__file__).resolve().parents[3]
COMMAND_RUN_ROOT = ROOT / "output" / "account_command" / "ctp-paper-19053"
RUNTIME_INVOCATION_READINESS = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-invocation-readiness.json"
)
RUNTIME_EXECUTION_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-approval-packet.json"
)
RUNTIME_EXECUTION_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-handoff-bundle.json"
)
RUNTIME_EXECUTION_GAP_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "runtime-execution-gap-audit.json"
)
PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-approval-packet.json"
)
PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-handoff-bundle.json"
)
PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-implementation-plan.json"
)
DEFAULT_RUNTIME_RUN_ID = "p023-armed-20260621t0748z"
REQUIRED_RUNTIME_FILES = [
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
    "command_audit.json",
    "redaction_report.json",
    "closeout_manifest.json",
]
SENSITIVE_RUNTIME_FRAGMENTS = ["tcp://", "trading.openctp", "Password", "AuthCode", "BrokerID", "UserID"]


def _require_paper_scope(account_id: str, intent_account_id: str, mode: str) -> None:
    if account_id != intent_account_id:
        raise HTTPException(status_code=409, detail="path account_id does not match intent account_id")
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 command API is scoped to acct.ctp.paper.19053 only")
    if mode != "paper_armed":
        raise HTTPException(status_code=403, detail="P024 accepts paper_armed intents only")


def _command_id(account_id: str, action: str, idempotency_key: str) -> str:
    digest = sha256(f"{PROPOSAL_ID}|{account_id}|{action}|{idempotency_key}".encode("utf-8")).hexdigest()[:24]
    return f"command.p024.{action}.{digest}"


def _intent_ref(account_id: str, action: str, command_id: str) -> str:
    safe_account = account_id.replace(".", "-")
    return f"api://p024/{safe_account}/{action}/{command_id}/intent"


def _canonical_checksum(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(data).hexdigest()


def _pre_gateway_blockers(action: str, source_ref: str) -> list[CommandBlocker]:
    return [
        CommandBlocker(
            blocker_id=f"p024_{action}_risk_decision_required",
            type="risk_decision_required",
            stage="risk",
            reason="intent accepted by API contract gate; risk decision is required before gateway send",
            source_ref=source_ref,
            next_action="produce RiskDecision evidence before gateway send",
        ),
        CommandBlocker(
            blocker_id=f"p024_{action}_approval_decision_required",
            type="approval_decision_required",
            stage="approval",
            reason="intent accepted by API contract gate; approval decision is required before gateway send",
            source_ref=source_ref,
            next_action="produce ApprovalDecision evidence before gateway send",
        ),
    ]


def _owner_runtime_blockers(action: str, source_ref: str, entrypoint_ref: str) -> list[CommandBlocker]:
    return [
        CommandBlocker(
            blocker_id=f"p024_{action}_owner_runtime_invocation_required",
            type="owner_runtime_invocation_required",
            stage="owner_runtime",
            reason="Web UI prepared a typed owner-runtime run request; Account Console does not invoke the broker runner.",
            source_ref=source_ref,
            next_action=f"invoke owner://nautilus_ctp_adapter {entrypoint_ref} with explicit operator approval",
        ),
        CommandBlocker(
            blocker_id=f"p024_{action}_external_write_approval_required",
            type="external_write_approval_required",
            stage="owner_runtime",
            reason="The guarded OpenCTP runner may write owner-runtime artifacts outside this worktree.",
            source_ref=source_ref,
            next_action="approve owner-repo runtime writes before running the guarded paper command loop",
        ),
        CommandBlocker(
            blocker_id=f"p024_{action}_post_run_ingest_required",
            type="post_run_ingest_required",
            stage="readback",
            reason="A real owner-runtime run must be ingested and reconciled before UI can claim broker execution.",
            source_ref=source_ref,
            next_action="ingest owner runtime artifacts with refs, checksums, redaction report and reconciliation result",
        ),
    ]


def _runtime_handoff_entrypoint(action: str) -> str:
    if action == "cancel":
        return "scripts/ctp_guarded_paper_cancel_loop.py"
    return "scripts/ctp_guarded_paper_order_loop.py"


def _runtime_run_request(
    *,
    account_id: str,
    action: str,
    command_id: str,
    intent_id: str,
    intent_ref: str,
    idempotency_key: str,
    source_preflight_ref: str,
    readback_ref: str | None,
) -> CommandRuntimeRunRequest:
    entrypoint_ref = _runtime_handoff_entrypoint(action)
    payload = {
        "schema_version": "account_command.owner_runtime_run_request.v1",
        "proposal_id": PROPOSAL_ID,
        "account_id": account_id,
        "action": action,
        "mode": "paper_armed",
        "status": "blocked_until_owner_runtime_invocation",
        "command_id": command_id,
        "intent_id": intent_id,
        "intent_ref": intent_ref,
        "idempotency_key": idempotency_key,
        "owner_runtime_owner_ref": "owner://nautilus_ctp_adapter",
        "owner_runtime_repo_ref": "owner-repo://nautilus_ctp_adapter",
        "owner_runtime_entrypoint_ref": entrypoint_ref,
        "owner_runtime_config_ref": "cfgs/local/ctp.openctp.tts.7x24.local.json",
        "source_preflight_ref": source_preflight_ref,
        "readback_ref": readback_ref,
        "expected_output_root_ref": f"output/account_command/ctp-paper-19053/p024-ui-{action}-{command_id}",
        "runtime_invocation_attempted": False,
        "browser_triggered_broker_order": False,
        "gateway_send_attempted": False,
        "broker_order_created": False,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "external_write_approval_required": True,
        "blockers": [blocker.model_dump() for blocker in _owner_runtime_blockers(action, intent_ref, entrypoint_ref)],
        "explicit_non_claims": [
            "does_not_invoke_owner_runtime",
            "does_not_send_broker_order_from_browser",
            "does_not_store_raw_ctp_secret_or_endpoint",
            "does_not_claim_live_readiness",
            "does_not_make_gateway_ack_final_state",
        ],
    }
    payload["run_request_checksum"] = _canonical_checksum(payload)
    return CommandRuntimeRunRequest(**payload)


def _file_checksum(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _runtime_ref(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _scan_runtime_fragments(run_dir: Path) -> list[str]:
    matches: list[str] = []
    for path in sorted(run_dir.rglob("*.json")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
            matches.append(_runtime_ref(path))
    return matches


def _runtime_run_dir(run_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise HTTPException(status_code=400, detail="invalid runtime run_id")
    run_dir = (COMMAND_RUN_ROOT / run_id).resolve()
    root = COMMAND_RUN_ROOT.resolve()
    if not str(run_dir).startswith(str(root)):
        raise HTTPException(status_code=400, detail="runtime run_id escaped command evidence root")
    return run_dir


def load_runtime_closeout(account_id: str, run_id: str = DEFAULT_RUNTIME_RUN_ID) -> CommandRuntimeCloseout:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime closeout is scoped to acct.ctp.paper.19053 only")
    run_dir = _runtime_run_dir(run_id)
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="runtime closeout run not found")
    missing = [filename for filename in REQUIRED_RUNTIME_FILES if not (run_dir / filename).exists()]
    if missing:
        raise HTTPException(status_code=409, detail=f"runtime closeout missing artifacts: {missing}")
    leaks = _scan_runtime_fragments(run_dir)
    if leaks:
        raise HTTPException(status_code=409, detail=f"runtime closeout contains forbidden sensitive fragments: {leaks}")

    manifest_path = run_dir / "closeout_manifest.json"
    manifest = _read_json(manifest_path)
    audit_path = run_dir / "command_audit.json"
    audit = _read_json(audit_path)
    redaction = _read_json(run_dir / "redaction_report.json")
    reconciliation = _read_json(run_dir / "reconciliation_result.json")
    submit_gateway = _read_json(run_dir / "submit_gateway_event.json")
    cancel_gateway = _read_json(run_dir / "cancel_gateway_event.json")

    if manifest.get("account_id") != PAPER_ACCOUNT_ID or audit.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime closeout account_id mismatch")
    if manifest.get("status") != "reconciled" or audit.get("status") != "reconciled":
        raise HTTPException(status_code=409, detail="runtime closeout is not reconciled")
    if manifest.get("mode") != "paper_armed" or audit.get("mode") != "paper_armed":
        raise HTTPException(status_code=409, detail="runtime closeout is not paper_armed")
    if redaction.get("status") != "passed":
        raise HTTPException(status_code=409, detail="runtime closeout redaction did not pass")
    if reconciliation.get("status") != "reconciled":
        raise HTTPException(status_code=409, detail="runtime closeout reconciliation did not pass")
    if manifest.get("gateway_ack_is_final_state") is not False or audit.get("gateway_ack_is_final_state") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout marked gateway ack as final state")
    if manifest.get("raw_secret_values_recorded") is not False or audit.get("raw_secret_values_recorded") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout recorded raw secret values")
    if manifest.get("raw_broker_endpoint_recorded") is not False or audit.get("raw_broker_endpoint_recorded") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout recorded raw broker endpoint")
    if submit_gateway.get("paper_send_armed") is not True or cancel_gateway.get("cancel_send_armed") is not True:
        raise HTTPException(status_code=409, detail="runtime closeout gateway send evidence is not armed paper runtime")

    artifact_refs = manifest.get("artifact_refs")
    if not isinstance(artifact_refs, dict) or not artifact_refs:
        raise HTTPException(status_code=409, detail="runtime closeout manifest artifact_refs missing")
    artifact_checksums: dict[str, str] = {}
    for filename, item in artifact_refs.items():
        artifact_path = run_dir / filename
        if not artifact_path.exists():
            raise HTTPException(status_code=409, detail=f"manifest references missing artifact: {filename}")
        checksum = _file_checksum(artifact_path)
        if item.get("checksum") != checksum:
            raise HTTPException(status_code=409, detail=f"manifest checksum mismatch: {filename}")
        artifact_checksums[_runtime_ref(artifact_path)] = checksum

    return CommandRuntimeCloseout(
        schema_version="account_command.runtime_closeout.v1",
        proposal_id=PROPOSAL_ID,
        account_id=PAPER_ACCOUNT_ID,
        run_id=run_id,
        mode="paper_armed",
        status="reconciled",
        closeout_manifest_ref=_runtime_ref(manifest_path),
        closeout_manifest_checksum=_file_checksum(manifest_path),
        command_audit_ref=_runtime_ref(audit_path),
        command_audit_checksum=_file_checksum(audit_path),
        intent_refs=list(audit.get("intent_refs") or []),
        risk_decision_refs=list(audit.get("risk_decision_refs") or []),
        approval_decision_refs=list(audit.get("approval_decision_refs") or []),
        gateway_event_refs=list(audit.get("gateway_event_refs") or []),
        readback_refs=list(audit.get("readback_refs") or []),
        reconciliation_ref=str(audit.get("reconciliation_ref") or ""),
        artifact_checksums=artifact_checksums,
        runtime_gateway_send_observed=True,
        broker_order_created=True,
        browser_triggered_broker_order=False,
        gateway_ack_is_final_state=False,
        raw_secret_values_recorded=False,
        raw_broker_endpoint_recorded=False,
        runtime_duplicate_send_attempted=False,
        source_owner_ref="output/account_command/ctp-paper-19053",
        explicit_non_claims=[
            "does_not_send_broker_order_from_browser_read",
            "does_not_store_raw_ctp_secret_or_endpoint",
            "does_not_claim_live_readiness",
            "does_not_make_gateway_ack_final_state",
            "web_ui_trigger_of_new_runtime_order_still_pending",
        ],
    )


def load_runtime_invocation_readiness(account_id: str) -> CommandRuntimeInvocationReadiness:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime readiness is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_INVOCATION_READINESS.exists():
        raise HTTPException(status_code=404, detail="runtime invocation readiness evidence not found")
    text = RUNTIME_INVOCATION_READINESS.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime invocation readiness contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime invocation readiness account_id mismatch")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime invocation readiness negative assertion failed: {key}")
    owner = payload.get("owner_runtime") or {}
    if owner.get("config_raw_content_read") is not False:
        raise HTTPException(status_code=409, detail="runtime invocation readiness read raw config content")
    approval = payload.get("external_write_approval_request") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime invocation readiness approval boundary drifted")
    return CommandRuntimeInvocationReadiness(**payload)


def load_runtime_execution_approval_packet(account_id: str) -> CommandRuntimeExecutionApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime approval packet is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="runtime execution approval packet evidence not found")
    text = RUNTIME_EXECUTION_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution approval packet account_id mismatch")
    approval = payload.get("required_operator_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution approval packet approval boundary drifted")
    if approval.get("approval_path") != "D:/Nautilus/nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="runtime execution approval packet owner path drifted")
    planned = payload.get("planned_execution") or {}
    if planned.get("runtime_invocation_attempted") is not False or planned.get("owner_repo_write_attempted") is not False:
        raise HTTPException(status_code=409, detail="runtime execution approval packet planned execution flags drifted")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution approval packet negative assertion failed: {key}")
    return CommandRuntimeExecutionApprovalPacket(**payload)


def load_runtime_execution_handoff_bundle(account_id: str) -> CommandRuntimeExecutionHandoffBundle:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime handoff bundle is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_HANDOFF_BUNDLE.exists():
        raise HTTPException(status_code=404, detail="runtime execution handoff bundle evidence not found")
    text = RUNTIME_EXECUTION_HANDOFF_BUNDLE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle account_id mismatch")
    guard = payload.get("execution_guard") or {}
    if guard.get("execution_allowed") is not False:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle allowed execution before approval")
    if guard.get("approval_required") is not True or guard.get("approval_obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle approval boundary drifted")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution handoff bundle negative assertion failed: {key}")
    return CommandRuntimeExecutionHandoffBundle(**payload)


def load_partial_fill_runtime_execution_approval_packet(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 partial-fill approval packet is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="partial-fill runtime execution approval packet evidence not found")
    text = PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval packet account_id mismatch")
    approval = payload.get("required_operator_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval boundary drifted")
    planned = payload.get("planned_execution") or {}
    for key in ["runtime_invocation_attempted", "owner_repo_write_attempted", "new_order_submitted", "cancel_sent"]:
        if planned.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill planned execution flag drifted: {key}")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill approval packet negative assertion failed: {key}")
    return CommandPartialFillRuntimeExecutionApprovalPacket(**payload)


def load_partial_fill_runtime_execution_handoff_bundle(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionHandoffBundle:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 partial-fill handoff bundle is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE.exists():
        raise HTTPException(status_code=404, detail="partial-fill runtime execution handoff bundle evidence not found")
    text = PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff bundle contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff bundle account_id mismatch")
    guard = payload.get("execution_guard") or {}
    if guard.get("execution_allowed") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff allowed execution before approval")
    if guard.get("approval_required") is not True or guard.get("approval_obtained") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff approval boundary drifted")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill handoff bundle negative assertion failed: {key}")
    return CommandPartialFillRuntimeExecutionHandoffBundle(**payload)


def load_runtime_execution_gap_audit(account_id: str) -> CommandRuntimeExecutionGapAudit:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime execution gap audit is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_GAP_AUDIT.exists():
        raise HTTPException(status_code=404, detail="runtime execution gap audit evidence not found")
    text = RUNTIME_EXECUTION_GAP_AUDIT.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution gap audit contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution gap audit account_id mismatch")
    approval = payload.get("external_write_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution gap audit approval boundary drifted")
    not_accepted = {item.get("id"): item for item in payload.get("not_accepted_scenarios") or []}
    if not_accepted.get("A4", {}).get("current_status") != "blocked_pending_owner_runtime_execution":
        raise HTTPException(status_code=409, detail="runtime execution gap audit A4 status drifted")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution gap audit negative assertion failed: {key}")
    return CommandRuntimeExecutionGapAudit(**payload)


def load_partial_fill_owner_repair_implementation_plan(
    account_id: str,
) -> CommandPartialFillOwnerRepairImplementationPlan:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair plan is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair implementation plan evidence not found")
    text = PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan account_id mismatch")
    context = payload.get("owner_read_context") or {}
    if context.get("owner_repo_path") != "D:/Nautilus/nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan owner path drifted")
    if context.get("owner_repo_write_attempted") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan attempted owner write")
    runtime = payload.get("post_repair_runtime_attempt_gate") or {}
    if runtime.get("runtime_attempt_allowed_by_this_plan") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan allowed runtime retry")
    if runtime.get("fresh_approval_required") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan lost fresh approval gate")
    negative = payload.get("negative_assertions") or {}
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
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair implementation plan negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairImplementationPlan(**payload)


def accept_submit_intent(account_id: str, intent: OrderIntentRequest) -> CommandApiResult:
    _require_paper_scope(account_id, intent.account_id, intent.mode)
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return CommandApiResult(
        schema_version="account_command.command_api_result.v1",
        proposal_id=PROPOSAL_ID,
        account_id=account_id,
        action="submit",
        mode=intent.mode,
        status="accepted_for_risk",
        command_id=command_id,
        intent_id=intent.intent_id,
        intent_ref=intent_ref,
        idempotency_key=intent.idempotency_key,
        idempotency_enforced=True,
        next_required_stage="risk_decision",
        blockers=_pre_gateway_blockers("submit", intent_ref),
        gateway_ack_is_final_state=False,
        gateway_send_attempted=False,
        broker_order_created=False,
        runtime_duplicate_send_attempted=False,
        raw_secret_values_recorded=False,
        raw_broker_endpoint_recorded=False,
    )


def accept_cancel_intent(account_id: str, intent: CancelIntentRequest) -> CommandApiResult:
    _require_paper_scope(account_id, intent.account_id, intent.mode)
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return CommandApiResult(
        schema_version="account_command.command_api_result.v1",
        proposal_id=PROPOSAL_ID,
        account_id=account_id,
        action="cancel",
        mode=intent.mode,
        status="accepted_for_risk",
        command_id=command_id,
        intent_id=intent.intent_id,
        intent_ref=intent_ref,
        idempotency_key=intent.idempotency_key,
        idempotency_enforced=True,
        next_required_stage="risk_decision",
        blockers=_pre_gateway_blockers("cancel", intent_ref),
        readback_refs=[intent.readback_ref],
        gateway_ack_is_final_state=False,
        gateway_send_attempted=False,
        broker_order_created=False,
        runtime_duplicate_send_attempted=False,
        raw_secret_values_recorded=False,
        raw_broker_endpoint_recorded=False,
    )


def prepare_submit_runtime_run_request(account_id: str, intent: OrderIntentRequest) -> CommandRuntimeRunRequest:
    _require_paper_scope(account_id, intent.account_id, intent.mode)
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return _runtime_run_request(
        account_id=account_id,
        action="submit",
        command_id=command_id,
        intent_id=intent.intent_id,
        intent_ref=intent_ref,
        idempotency_key=intent.idempotency_key,
        source_preflight_ref=intent.preflight_ref,
        readback_ref=None,
    )


def prepare_cancel_runtime_run_request(account_id: str, intent: CancelIntentRequest) -> CommandRuntimeRunRequest:
    _require_paper_scope(account_id, intent.account_id, intent.mode)
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return _runtime_run_request(
        account_id=account_id,
        action="cancel",
        command_id=command_id,
        intent_id=intent.intent_id,
        intent_ref=intent_ref,
        idempotency_key=intent.idempotency_key,
        source_preflight_ref=intent.readback_ref,
        readback_ref=intent.readback_ref,
    )
