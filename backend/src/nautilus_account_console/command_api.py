from __future__ import annotations

from hashlib import sha256

from fastapi import HTTPException

from .schemas import CancelIntentRequest, CommandApiResult, CommandBlocker, OrderIntentRequest


PAPER_ACCOUNT_ID = "acct.ctp.paper.19053"
PROPOSAL_ID = "p024-account-console-paper-command-controls"


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
