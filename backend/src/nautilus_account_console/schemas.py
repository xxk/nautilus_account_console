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


class Health(BaseModel):
    ok: bool
    service: str
    version: str
