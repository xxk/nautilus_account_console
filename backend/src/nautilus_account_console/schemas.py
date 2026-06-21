from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccountKind(StrEnum):
    SANDBOX_PAPER = "sandbox_paper"
    REAL_FEED_SANDBOX_PAPER = "real_feed_sandbox_paper"
    BROKER_PAPER_PROBE = "broker_paper_probe"
    LIVE_BROKER = "live_broker"
    BACKTEST_REPLAY = "backtest_replay"


class AccountSnapshot(BaseModel):
    account_id: str
    account_kind: AccountKind
    portfolio_uid: str
    session_id: str
    equity: float
    available_cash: float
    margin_used: float
    position_count: int = 0
    open_order_count: int = 0
    fill_count_today: int = 0
    event_lag_ms: float = 0.0
    health: str = "event_stream_live"
    blocker_id: str | None = None
    last_seq: int = 0
    source_ref: str
    checksum: str


class OrderEvent(BaseModel):
    event_id: str
    seq: int = Field(ge=0)
    ts_event: datetime
    ts_recv: datetime
    account_id: str
    account_kind: AccountKind
    portfolio_uid: str
    strategy_id: str
    instrument_id: str
    client_order_id: str
    venue_order_id: str | None = None
    event_type: str
    order_status: str
    side: str
    price: float | None = None
    quantity: float | None = None
    filled_qty: float = 0.0
    last_px: float | None = None
    last_qty: float | None = None
    leaves_qty: float | None = None
    reason: str | None = None
    latency_ms: float | None = None
    report_msg_type: str | None = None
    report_msg_ref: str | None = None
    report_msg_checksum: str | None = None
    report_msg_excerpt: str | None = None
    source_ref: str
    checksum: str


class AccountDetail(BaseModel):
    snapshot: AccountSnapshot
    recent_order_events: list[OrderEvent]


class OrderExecutionReports(BaseModel):
    account_id: str
    client_order_id: str
    reports: list[OrderEvent]


class MirrorCapabilityState(BaseModel):
    enabled: bool
    mirror_state: str | None = None
    mode: str | None = None


class MirrorCapabilities(BaseModel):
    observation: MirrorCapabilityState
    command: MirrorCapabilityState


class MirrorAccountProjection(BaseModel):
    schema_version: str
    account_id: str
    display_alias: str
    source_kind: str
    source_mode: str
    account_domain: str
    capabilities: MirrorCapabilities
    balances: list[dict]
    positions: list[dict]
    orders: list[dict]
    fills: list[dict]
    source_health: dict
    command_status: dict | None = None
    blockers: list[dict]
    projection_checkpoint_id: str
    projection_checksum: str
    source_ref: str
    source_checksum: str
    route_context: dict
    boundaries: dict


class MirrorAccountSummary(BaseModel):
    account_id: str
    display_alias: str
    source_kind: str
    source_mode: str
    account_domain: str
    mirror_state: str
    command_enabled: bool
    command_mode: str
    balance_count: int
    position_count: int
    order_count: int
    fill_count: int
    blocker_count: int
    projection_checkpoint_id: str
    projection_checksum: str
    source_ref: str
    source_checksum: str
    route_id: str
    evidence_partition: str


class MirrorListResponse(BaseModel):
    schema_version: str
    accounts: list[MirrorAccountSummary]


class MirrorEvidenceItem(BaseModel):
    kind: str
    owner: str
    source_ref: str
    checksum: str
    authority: str


class MirrorEvidenceResponse(BaseModel):
    schema_version: str
    account_id: str
    projection_checkpoint_id: str
    projection_checksum: str
    source_ref: str
    source_checksum: str
    evidence: list[MirrorEvidenceItem]
    blockers: list[dict]
    boundaries: dict


class MirrorSourceHealthResponse(BaseModel):
    schema_version: str
    account_id: str
    state: str
    source_ref: str
    source_checksum: str
    observed_at: str
    projection_checkpoint_id: str
    projection_checksum: str
    blockers: list[dict]
    boundaries: dict


class OrderIntentRequest(BaseModel):
    schema_version: Literal["account_command.order_intent.v1"]
    intent_id: str = Field(pattern=r"^intent\.[a-z0-9_.-]+$")
    account_id: Literal["acct.ctp.paper.19053"]
    mode: Literal["paper_armed", "live_dry_run", "live_armed"]
    action: Literal["submit"]
    instrument: str = Field(min_length=1)
    exchange: str = Field(min_length=1)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(ge=1)
    order_type: Literal["LIMIT"]
    limit_price: float = Field(gt=0)
    time_in_force: Literal["GFD", "IOC", "FAK", "FOK"]
    offset: Literal["OPEN", "CLOSE", "CLOSETODAY", "CLOSEYESTERDAY"]
    idempotency_key: str = Field(min_length=12)
    operator_ref: str = Field(min_length=1)
    preflight_ref: str = Field(min_length=1)
    raw_secret_values_recorded: Literal[False]
    raw_broker_endpoint_recorded: Literal[False]


class CancelIntentRequest(BaseModel):
    schema_version: Literal["account_command.cancel_intent.v1"]
    intent_id: str = Field(pattern=r"^intent\.[a-z0-9_.-]+$")
    account_id: Literal["acct.ctp.paper.19053"]
    mode: Literal["paper_armed", "live_dry_run", "live_armed"]
    action: Literal["cancel"]
    instrument: str = Field(min_length=1)
    exchange: str = Field(min_length=1)
    client_order_id: str = Field(min_length=1)
    venue_order_id: str = Field(min_length=1)
    order_ref: str = Field(min_length=1)
    front_id: int
    session_id: int
    idempotency_key: str = Field(min_length=12)
    operator_ref: str = Field(min_length=1)
    readback_ref: str = Field(min_length=1)
    raw_secret_values_recorded: Literal[False]
    raw_broker_endpoint_recorded: Literal[False]


class CommandBlocker(BaseModel):
    blocker_id: str
    type: str
    stage: str
    reason: str
    source_ref: str
    next_action: str


class CommandApiResult(BaseModel):
    schema_version: Literal["account_command.command_api_result.v1"]
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: str
    action: Literal["submit", "cancel"]
    mode: str
    status: Literal["accepted_for_risk", "blocked"]
    command_id: str
    intent_id: str
    intent_ref: str
    idempotency_key: str
    idempotency_enforced: bool
    next_required_stage: str
    blockers: list[CommandBlocker]
    risk_decision_ref: str | None = None
    approval_decision_ref: str | None = None
    gateway_event_refs: list[str] = Field(default_factory=list)
    readback_refs: list[str] = Field(default_factory=list)
    reconciliation_ref: str | None = None
    gateway_ack_is_final_state: Literal[False]
    gateway_send_attempted: Literal[False]
    broker_order_created: Literal[False]
    runtime_duplicate_send_attempted: Literal[False]
    raw_secret_values_recorded: Literal[False]
    raw_broker_endpoint_recorded: Literal[False]


class CommandRuntimeCloseout(BaseModel):
    schema_version: Literal["account_command.runtime_closeout.v1"]
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    run_id: str
    mode: Literal["paper_armed"]
    status: Literal["reconciled"]
    closeout_manifest_ref: str
    closeout_manifest_checksum: str
    command_audit_ref: str
    command_audit_checksum: str
    intent_refs: list[str]
    risk_decision_refs: list[str]
    approval_decision_refs: list[str]
    gateway_event_refs: list[str]
    readback_refs: list[str]
    reconciliation_ref: str
    artifact_checksums: dict[str, str]
    runtime_gateway_send_observed: Literal[True]
    broker_order_created: Literal[True]
    browser_triggered_broker_order: Literal[False]
    gateway_ack_is_final_state: Literal[False]
    raw_secret_values_recorded: Literal[False]
    raw_broker_endpoint_recorded: Literal[False]
    runtime_duplicate_send_attempted: Literal[False]
    source_owner_ref: str
    explicit_non_claims: list[str]


class CommandRuntimeRunRequest(BaseModel):
    schema_version: Literal["account_command.owner_runtime_run_request.v1"]
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    action: Literal["submit", "cancel"]
    mode: Literal["paper_armed"]
    status: Literal["blocked_until_owner_runtime_invocation"]
    command_id: str
    intent_id: str
    intent_ref: str
    idempotency_key: str
    owner_runtime_owner_ref: Literal["owner://nautilus_ctp_adapter"]
    owner_runtime_repo_ref: Literal["owner-repo://nautilus_ctp_adapter"]
    owner_runtime_entrypoint_ref: str
    owner_runtime_config_ref: str
    source_preflight_ref: str
    readback_ref: str | None = None
    expected_output_root_ref: str
    runtime_invocation_attempted: Literal[False]
    browser_triggered_broker_order: Literal[False]
    gateway_send_attempted: Literal[False]
    broker_order_created: Literal[False]
    raw_secret_values_recorded: Literal[False]
    raw_broker_endpoint_recorded: Literal[False]
    external_write_approval_required: Literal[True]
    blockers: list[CommandBlocker]
    explicit_non_claims: list[str]
    run_request_checksum: str


class CommandRuntimeInvocationReadiness(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.owner-runtime-invocation-readiness.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    status: Literal["blocked_waiting_for_external_owner_runtime_write_approval"]
    verdict: Literal["readiness_package_passed_runtime_not_invoked"]
    reviewed_at: str
    owner_runtime: dict
    entrypoints: list[dict]
    predecessor_evidence: dict
    external_write_approval_request: dict
    planned_runtime_commands: list[dict]
    acceptance_after_owner_run: dict
    negative_assertions: dict
    blockers: list[CommandBlocker]
    explicit_non_claims: list[str]


class CommandRuntimeExecutionApprovalPacket(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.owner-runtime-execution-approval-packet.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4a_owner_runtime_execution_approval_packet_ready"]
    verdict: Literal["approval_packet_ready_runtime_not_invoked"]
    owner_runtime: dict
    required_operator_approval: dict
    planned_execution: dict
    entrypoints: list[dict]
    command_templates: list[dict]
    required_post_run_artifacts: list[str]
    post_run_acceptance_gates: list[str]
    blockers: list[CommandBlocker]
    negative_assertions: dict
    explicit_non_claims: list[str]


class CommandRuntimeExecutionHandoffBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.owner-runtime-execution-handoff-bundle.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4c_owner_runtime_execution_handoff_bundle_ready"]
    verdict: Literal["handoff_bundle_ready_runtime_not_invoked"]
    depends_on: dict
    execution_guard: dict
    runtime_input_requirements: list[dict]
    operator_sequence: list[dict]
    required_owner_artifacts: list[str]
    post_handoff_gates: list[str]
    blockers: list[CommandBlocker]
    negative_assertions: dict
    explicit_non_claims: list[str]


class CommandPartialFillRuntimeExecutionApprovalPacket(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.partial-fill-runtime-execution-approval-packet.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4j_partial_fill_runtime_execution_approval_packet_ready"]
    verdict: Literal["approval_packet_ready_runtime_not_invoked"]
    owner_runtime: dict
    required_operator_approval: dict
    planned_execution: dict
    entrypoints: list[dict]
    attempt_constraints: dict
    command_templates: list[dict]
    required_post_run_artifacts: list[str]
    post_run_acceptance_gates: list[str]
    blockers: list[dict]
    negative_assertions: dict
    explicit_non_claims: list[str]


class CommandPartialFillRuntimeExecutionHandoffBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4k_partial_fill_runtime_execution_handoff_bundle_ready"]
    verdict: Literal["handoff_bundle_ready_runtime_not_invoked"]
    depends_on: dict
    execution_guard: dict
    runtime_input_requirements: list[dict]
    operator_sequence: list[dict]
    success_criteria: dict
    fallback_classifications: list[str]
    negative_assertions: dict


class CommandRuntimeExecutionGapAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.runtime-execution-gap-audit.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4e_final_runtime_execution_gap_audited"]
    verdict: Literal["blocked_pending_owner_runtime_execution"]
    goal_state: Literal["all_acceptance_requires_owner_runtime_execution_artifacts"]
    accepted_scenarios: list[str]
    not_accepted_scenarios: list[dict]
    required_before_goal_complete: list[str]
    external_write_approval: dict
    owner_runtime_refs: dict
    required_owner_artifacts: list[str]
    post_execution_gates: list[str]
    residual_blockers: list[dict]
    negative_assertions: dict
    explicit_non_claims: list[str]


class CommandPartialFillOwnerRepairImplementationPlan(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.partial-fill-owner-repair-implementation-plan.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4r_owner_close_offset_repair_implementation_plan_ready"]
    verdict: Literal["owner_repair_plan_ready_no_owner_write_attempted"]
    depends_on: dict
    owner_read_context: dict
    planned_owner_changes_after_exact_approval: list[dict]
    post_repair_validator_sequence: list[dict]
    post_repair_runtime_attempt_gate: dict
    forbidden_repair_shapes: list[str]
    negative_assertions: dict


class CommandPartialFillOwnerRepairEvidenceIngestGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.partial-fill-owner-repair-evidence-ingest-gate.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4t_owner_repair_evidence_ingest_gate_ready"]
    verdict: Literal["ingest_gate_ready_owner_repair_evidence_missing"]
    depends_on: dict
    ingest_scope: dict
    required_owner_repair_evidence: list[dict]
    post_ingest_required_account_console_updates: list[str]
    reject_evidence_if: list[str]
    negative_assertions: dict


class CommandPartialFillOwnerRepairPreflightSourceAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["account-console.p024.partial-fill-owner-repair-preflight-source-audit.v1"] = Field(alias="schema")
    proposal_id: Literal["p024-account-console-paper-command-controls"]
    account_id: Literal["acct.ctp.paper.19053"]
    reviewed_at: str
    status: Literal["phase4v_owner_repair_preflight_source_audited"]
    verdict: Literal["owner_repair_still_required_before_runtime_retry"]
    owner_repo: dict
    source_checks: list[dict]
    operator_approval_delta: dict
    next_required_action: dict
    negative_assertions: dict


class Health(BaseModel):
    ok: bool
    service: str
    version: str
