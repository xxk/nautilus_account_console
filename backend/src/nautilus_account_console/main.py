from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from . import __version__
from .command_api import (
    accept_cancel_intent,
    accept_submit_intent,
    load_partial_fill_owner_repair_approval_packet,
    load_partial_fill_remaining_acceptance_current_state,
    load_partial_fill_owner_repair_implementation_plan,
    load_partial_fill_owner_repair_evidence_ingest_gate,
    load_partial_fill_owner_repair_preflight_source_audit,
    load_partial_fill_owner_repair_patch_preview,
    load_partial_fill_owner_repair_execution_handoff_bundle,
    load_partial_fill_runtime_execution_approval_packet,
    load_partial_fill_runtime_execution_handoff_bundle,
    load_runtime_execution_approval_packet,
    load_runtime_execution_gap_audit,
    load_runtime_execution_handoff_bundle,
    load_runtime_invocation_readiness,
    load_runtime_closeout,
    prepare_cancel_runtime_run_request,
    prepare_submit_runtime_run_request,
)
from .ledger import (
    get_account_snapshot,
    list_account_snapshots,
    list_order_events,
    list_order_execution_reports,
)
from .account_mirror import AccountMirrorStore
from .schemas import (
    AccountDetail,
    AccountSnapshot,
    CancelIntentRequest,
    CommandApiResult,
    CommandPartialFillOwnerRepairApprovalPacket,
    CommandPartialFillRemainingAcceptanceCurrentState,
    CommandPartialFillOwnerRepairEvidenceIngestGate,
    CommandPartialFillOwnerRepairImplementationPlan,
    CommandPartialFillOwnerRepairPreflightSourceAudit,
    CommandPartialFillOwnerRepairPatchPreview,
    CommandPartialFillOwnerRepairExecutionHandoffBundle,
    CommandPartialFillRuntimeExecutionApprovalPacket,
    CommandPartialFillRuntimeExecutionHandoffBundle,
    CommandRuntimeCloseout,
    CommandRuntimeExecutionApprovalPacket,
    CommandRuntimeExecutionGapAudit,
    CommandRuntimeExecutionHandoffBundle,
    CommandRuntimeInvocationReadiness,
    CommandRuntimeRunRequest,
    Health,
    MirrorAccountProjection,
    MirrorEvidenceResponse,
    MirrorEvidenceItem,
    MirrorListResponse,
    MirrorAccountSummary,
    MirrorSourceHealthResponse,
    OrderIntentRequest,
    OrderEvent,
    OrderExecutionReports,
)
from .source_bridge import load_capability_bundles


app = FastAPI(title="Nautilus Account Console API", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/healthz", response_model=Health)
def healthz() -> Health:
    return Health(ok=True, service="nautilus-account-console", version=__version__)


@app.get("/api/accounts", response_model=list[AccountSnapshot])
def accounts() -> list[AccountSnapshot]:
    return list_account_snapshots()


def _mirror_projections() -> list[MirrorAccountProjection]:
    bundles = load_capability_bundles()
    projections = AccountMirrorStore().list_projections_from_bundles(bundles)
    return [MirrorAccountProjection(**projection.to_dict()) for projection in projections]


def _mirror_projection(account_id: str) -> MirrorAccountProjection:
    for projection in _mirror_projections():
        if projection.account_id == account_id:
            return projection
    raise HTTPException(status_code=404, detail="mirror account projection not found")


def _mirror_summary(projection: MirrorAccountProjection) -> MirrorAccountSummary:
    return MirrorAccountSummary(
        account_id=projection.account_id,
        display_alias=projection.display_alias,
        source_kind=projection.source_kind,
        source_mode=projection.source_mode,
        account_domain=projection.account_domain,
        mirror_state=projection.capabilities.observation.mirror_state or "unknown",
        command_enabled=projection.capabilities.command.enabled,
        command_mode=projection.capabilities.command.mode or "disabled",
        balance_count=len(projection.balances),
        position_count=len(projection.positions),
        order_count=len(projection.orders),
        fill_count=len(projection.fills),
        blocker_count=len(projection.blockers),
        projection_checkpoint_id=projection.projection_checkpoint_id,
        projection_checksum=projection.projection_checksum,
        source_ref=projection.source_ref,
        source_checksum=projection.source_checksum,
        route_id=str(projection.route_context["route_id"]),
        evidence_partition=str(projection.route_context["evidence_partition"]),
    )


@app.get("/api/mirror/accounts", response_model=MirrorListResponse, response_model_exclude_none=True)
def mirror_accounts() -> MirrorListResponse:
    projections = _mirror_projections()
    return MirrorListResponse(
        schema_version="account_mirror_list.v1",
        accounts=[_mirror_summary(projection) for projection in projections],
    )


@app.get(
    "/api/mirror/accounts/{account_id}",
    response_model=MirrorAccountProjection,
    response_model_exclude_none=True,
)
def mirror_account_detail(account_id: str) -> MirrorAccountProjection:
    return _mirror_projection(account_id)


@app.get("/api/mirror/accounts/{account_id}/positions", response_model=list[dict])
def mirror_account_positions(account_id: str) -> list[dict]:
    return _mirror_projection(account_id).positions


@app.get("/api/mirror/accounts/{account_id}/orders", response_model=list[dict])
def mirror_account_orders(account_id: str) -> list[dict]:
    return _mirror_projection(account_id).orders


@app.get("/api/mirror/accounts/{account_id}/capabilities", response_model=dict, response_model_exclude_none=True)
def mirror_account_capabilities(account_id: str) -> dict:
    projection = _mirror_projection(account_id)
    return projection.capabilities.model_dump()


@app.get("/api/mirror/accounts/{account_id}/source-health", response_model=MirrorSourceHealthResponse)
def mirror_account_source_health(account_id: str) -> MirrorSourceHealthResponse:
    projection = _mirror_projection(account_id)
    health = projection.source_health
    return MirrorSourceHealthResponse(
        schema_version="account_mirror_source_health.v1",
        account_id=projection.account_id,
        state=str(health.get("state", "unknown")),
        source_ref=str(health["source_ref"]),
        source_checksum=str(health["checksum"]),
        observed_at=str(health["observed_at"]),
        projection_checkpoint_id=projection.projection_checkpoint_id,
        projection_checksum=projection.projection_checksum,
        blockers=projection.blockers,
        boundaries=projection.boundaries,
    )


@app.get("/api/mirror/accounts/{account_id}/evidence", response_model=MirrorEvidenceResponse)
def mirror_account_evidence(account_id: str) -> MirrorEvidenceResponse:
    projection = _mirror_projection(account_id)
    evidence = [
        MirrorEvidenceItem(
            kind="source_package",
            owner=projection.source_kind,
            source_ref=projection.source_ref,
            checksum=projection.source_checksum,
            authority="source artifact provenance; not broker or account truth",
        ),
        MirrorEvidenceItem(
            kind="mirror_projection",
            owner="account-console-backend",
            source_ref=projection.projection_checkpoint_id,
            checksum=projection.projection_checksum,
            authority="Account Mirror read-only projection checkpoint",
        ),
    ]
    for blocker in projection.blockers:
        evidence.append(
            MirrorEvidenceItem(
                kind="typed_blocker",
                owner=str(blocker["owner"]),
                source_ref=str(blocker["source_ref"]),
                checksum=str(blocker["checksum"]),
                authority="typed blocker; fail closed until owner resolves source evidence",
            )
        )
    return MirrorEvidenceResponse(
        schema_version="account_mirror_evidence.v1",
        account_id=projection.account_id,
        projection_checkpoint_id=projection.projection_checkpoint_id,
        projection_checksum=projection.projection_checksum,
        source_ref=projection.source_ref,
        source_checksum=projection.source_checksum,
        evidence=evidence,
        blockers=projection.blockers,
        boundaries=projection.boundaries,
    )


@app.post(
    "/api/commands/accounts/{account_id}/submit-intents",
    response_model=CommandApiResult,
    response_model_exclude_none=True,
    status_code=202,
)
def command_submit_intent(account_id: str, intent: OrderIntentRequest) -> CommandApiResult:
    return accept_submit_intent(account_id, intent)


@app.post(
    "/api/commands/accounts/{account_id}/cancel-intents",
    response_model=CommandApiResult,
    response_model_exclude_none=True,
    status_code=202,
)
def command_cancel_intent(account_id: str, intent: CancelIntentRequest) -> CommandApiResult:
    return accept_cancel_intent(account_id, intent)


@app.post(
    "/api/commands/accounts/{account_id}/runtime-run-requests/submit",
    response_model=CommandRuntimeRunRequest,
    response_model_exclude_none=True,
    status_code=202,
)
def command_submit_runtime_run_request(account_id: str, intent: OrderIntentRequest) -> CommandRuntimeRunRequest:
    return prepare_submit_runtime_run_request(account_id, intent)


@app.post(
    "/api/commands/accounts/{account_id}/runtime-run-requests/cancel",
    response_model=CommandRuntimeRunRequest,
    response_model_exclude_none=True,
    status_code=202,
)
def command_cancel_runtime_run_request(account_id: str, intent: CancelIntentRequest) -> CommandRuntimeRunRequest:
    return prepare_cancel_runtime_run_request(account_id, intent)


@app.get(
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}",
    response_model=CommandRuntimeCloseout,
    response_model_exclude_none=True,
)
def command_runtime_closeout(account_id: str, run_id: str) -> CommandRuntimeCloseout:
    return load_runtime_closeout(account_id, run_id)


@app.get(
    "/api/commands/accounts/{account_id}/runtime-invocation-readiness",
    response_model=CommandRuntimeInvocationReadiness,
    response_model_exclude_none=True,
)
def command_runtime_invocation_readiness(account_id: str) -> CommandRuntimeInvocationReadiness:
    return load_runtime_invocation_readiness(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/runtime-execution-approval-packet",
    response_model=CommandRuntimeExecutionApprovalPacket,
    response_model_exclude_none=True,
)
def command_runtime_execution_approval_packet(account_id: str) -> CommandRuntimeExecutionApprovalPacket:
    return load_runtime_execution_approval_packet(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle",
    response_model=CommandRuntimeExecutionHandoffBundle,
    response_model_exclude_none=True,
)
def command_runtime_execution_handoff_bundle(account_id: str) -> CommandRuntimeExecutionHandoffBundle:
    return load_runtime_execution_handoff_bundle(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet",
    response_model=CommandPartialFillRuntimeExecutionApprovalPacket,
    response_model_exclude_none=True,
)
def command_partial_fill_runtime_execution_approval_packet(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionApprovalPacket:
    return load_partial_fill_runtime_execution_approval_packet(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle",
    response_model=CommandPartialFillRuntimeExecutionHandoffBundle,
    response_model_exclude_none=True,
)
def command_partial_fill_runtime_execution_handoff_bundle(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionHandoffBundle:
    return load_partial_fill_runtime_execution_handoff_bundle(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/runtime-execution-gap-audit",
    response_model=CommandRuntimeExecutionGapAudit,
    response_model_exclude_none=True,
)
def command_runtime_execution_gap_audit(account_id: str) -> CommandRuntimeExecutionGapAudit:
    return load_runtime_execution_gap_audit(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-approval-packet",
    response_model=CommandPartialFillOwnerRepairApprovalPacket,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_approval_packet(
    account_id: str,
) -> CommandPartialFillOwnerRepairApprovalPacket:
    return load_partial_fill_owner_repair_approval_packet(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-remaining-acceptance-current-state",
    response_model=CommandPartialFillRemainingAcceptanceCurrentState,
    response_model_exclude_none=True,
)
def command_partial_fill_remaining_acceptance_current_state(
    account_id: str,
) -> CommandPartialFillRemainingAcceptanceCurrentState:
    return load_partial_fill_remaining_acceptance_current_state(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan",
    response_model=CommandPartialFillOwnerRepairImplementationPlan,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_implementation_plan(
    account_id: str,
) -> CommandPartialFillOwnerRepairImplementationPlan:
    return load_partial_fill_owner_repair_implementation_plan(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate",
    response_model=CommandPartialFillOwnerRepairEvidenceIngestGate,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_evidence_ingest_gate(
    account_id: str,
) -> CommandPartialFillOwnerRepairEvidenceIngestGate:
    return load_partial_fill_owner_repair_evidence_ingest_gate(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit",
    response_model=CommandPartialFillOwnerRepairPreflightSourceAudit,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_preflight_source_audit(
    account_id: str,
) -> CommandPartialFillOwnerRepairPreflightSourceAudit:
    return load_partial_fill_owner_repair_preflight_source_audit(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview",
    response_model=CommandPartialFillOwnerRepairPatchPreview,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_patch_preview(
    account_id: str,
) -> CommandPartialFillOwnerRepairPatchPreview:
    return load_partial_fill_owner_repair_patch_preview(account_id)


@app.get(
    "/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle",
    response_model=CommandPartialFillOwnerRepairExecutionHandoffBundle,
    response_model_exclude_none=True,
)
def command_partial_fill_owner_repair_execution_handoff_bundle(
    account_id: str,
) -> CommandPartialFillOwnerRepairExecutionHandoffBundle:
    return load_partial_fill_owner_repair_execution_handoff_bundle(account_id)


@app.get("/api/accounts/{account_id}", response_model=AccountDetail)
def account_detail(account_id: str) -> AccountDetail:
    snapshot = get_account_snapshot(account_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="account not found")
    return AccountDetail(snapshot=snapshot, recent_order_events=list_order_events(account_id))


@app.get("/api/accounts/{account_id}/events", response_model=list[OrderEvent])
def account_events(
    account_id: str,
    cursor: int = Query(default=0, ge=0),
    limit: int = Query(default=500, ge=1, le=5000),
) -> list[OrderEvent]:
    if get_account_snapshot(account_id) is None:
        raise HTTPException(status_code=404, detail="account not found")
    return list_order_events(account_id, cursor=cursor, limit=limit)


@app.get(
    "/api/accounts/{account_id}/orders/{client_order_id}/execution-reports",
    response_model=OrderExecutionReports,
)
def order_execution_reports(account_id: str, client_order_id: str) -> OrderExecutionReports:
    if get_account_snapshot(account_id) is None:
        raise HTTPException(status_code=404, detail="account not found")
    reports = list_order_execution_reports(account_id, client_order_id)
    if not reports:
        raise HTTPException(status_code=404, detail="order reports not found")
    return OrderExecutionReports(
        account_id=account_id,
        client_order_id=client_order_id,
        reports=reports,
    )


async def _event_stream(account_id: str, cursor: int) -> AsyncIterator[str]:
    events = list_order_events(account_id, cursor=cursor)
    for event in events:
        yield (
            f"id: {event.seq}\n"
            "event: order_event\n"
            f"data: {event.model_dump_json()}\n\n"
        )
        await asyncio.sleep(0.05)


@app.get("/api/accounts/{account_id}/events/stream")
def account_event_stream(
    account_id: str,
    cursor: int = Query(default=0, ge=0),
) -> StreamingResponse:
    if get_account_snapshot(account_id) is None:
        raise HTTPException(status_code=404, detail="account not found")
    return StreamingResponse(
        _event_stream(account_id, cursor),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
