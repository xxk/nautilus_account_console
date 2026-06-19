from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


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
    blockers: list[dict]
    projection_checkpoint_id: str
    projection_checksum: str
    source_ref: str
    source_checksum: str
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


class Health(BaseModel):
    ok: bool
    service: str
    version: str
