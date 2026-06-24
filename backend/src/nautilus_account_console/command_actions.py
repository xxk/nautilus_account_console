from __future__ import annotations

import json
from hashlib import sha256

from fastapi import HTTPException

from .schemas import (
    CancelIntentRequest,
    CommandApiResult,
    CommandBlocker,
    CommandRuntimeRunRequest,
    OrderIntentRequest,
)
from .source_bridge import SourceBridgeError, load_capability_bundles


PAPER_ACCOUNT_ID = "acct.ctp.paper.19053"
PROPOSAL_ID = "p024-account-console-paper-command-controls"


def _require_paper_scope(account_id: str, intent_account_id: str, mode: str) -> None:
    if account_id != intent_account_id:
        raise HTTPException(status_code=409, detail="path account_id does not match intent account_id")
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 command API is scoped to acct.ctp.paper.19053 only")
    if mode != "paper_armed":
        raise HTTPException(status_code=403, detail="P024 accepts paper_armed intents only")


def _require_command_capability(account_id: str, action: str) -> None:
    try:
        bundles = load_capability_bundles()
    except SourceBridgeError as exc:
        raise HTTPException(status_code=409, detail=f"command capability source invalid: {exc}") from exc

    for bundle in bundles:
        account = bundle.get("account") or {}
        if account.get("account_id") != account_id:
            continue
        command = bundle.get("capabilities", {}).get("command") or {}
        if command.get("enabled") is not True:
            raise HTTPException(status_code=403, detail="command_capability_not_mounted")
        if command.get("mode") != "paper_armed":
            raise HTTPException(status_code=403, detail="command_capability_not_paper_armed")
        if action not in set(command.get("allowed_actions") or []):
            raise HTTPException(status_code=403, detail=f"command_action_not_allowed:{action}")
        authority_ref = command.get("authority_ref")
        if authority_ref != "owner-repo://nautilus_ctp_adapter":
            raise HTTPException(status_code=403, detail="command_capability_owner_authority_missing")
        checksum = str(command.get("capability_checksum") or "")
        if not checksum.startswith("sha256:"):
            raise HTTPException(status_code=403, detail="command_capability_checksum_missing")
        return

    raise HTTPException(status_code=404, detail="command capability account not found")


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


def accept_submit_intent(account_id: str, intent: OrderIntentRequest) -> CommandApiResult:
    _require_paper_scope(account_id, intent.account_id, intent.mode)
    _require_command_capability(account_id, "submit")
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return CommandApiResult(
        schema_version="account_command.command_api_result.v1",
        proposal_id=PROPOSAL_ID,
        account_id=account_id,
        action="submit",
        mode=intent.mode,
        status="risk_gate_pending",
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
    _require_command_capability(account_id, "cancel")
    command_id = _command_id(account_id, intent.action, intent.idempotency_key)
    intent_ref = _intent_ref(account_id, intent.action, command_id)
    return CommandApiResult(
        schema_version="account_command.command_api_result.v1",
        proposal_id=PROPOSAL_ID,
        account_id=account_id,
        action="cancel",
        mode=intent.mode,
        status="risk_gate_pending",
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
    _require_command_capability(account_id, "submit")
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
    _require_command_capability(account_id, "cancel")
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
