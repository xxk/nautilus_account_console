from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from .schemas import AccountKind, AccountSnapshot, OrderEvent


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _checksum(*parts: object) -> str:
    data = "|".join(str(part) for part in parts)
    return "sha256:" + sha256(data.encode("utf-8")).hexdigest()


def seed_order_events() -> list[OrderEvent]:
    account_id = "paper.demo-01"
    account_kind = AccountKind.REAL_FEED_SANDBOX_PAPER
    portfolio_uid = "portfolio.demo"
    source_ref = "fixture://mvp/order-events.jsonl"
    rows = [
        {
            "seq": 1,
            "ts": "2026-06-13T01:00:00Z",
            "client_order_id": "C-0001",
            "venue_order_id": "V-0001",
            "event_type": "submitted",
            "order_status": "SUBMITTED",
            "filled_qty": 0.0,
            "leaves_qty": 2.0,
            "excerpt": "sandbox report: order accepted",
        },
        {
            "seq": 2,
            "ts": "2026-06-13T01:00:00.080Z",
            "client_order_id": "C-0001",
            "venue_order_id": "V-0001",
            "event_type": "accepted",
            "order_status": "ACCEPTED",
            "filled_qty": 0.0,
            "leaves_qty": 2.0,
            "excerpt": "sandbox report: venue ack",
        },
        {
            "seq": 3,
            "ts": "2026-06-13T01:00:00.180Z",
            "client_order_id": "C-0001",
            "venue_order_id": "V-0001",
            "event_type": "partially_filled",
            "order_status": "PARTIALLY_FILLED",
            "filled_qty": 1.0,
            "last_px": 3512.5,
            "last_qty": 1.0,
            "leaves_qty": 1.0,
            "excerpt": "sandbox report: partial fill",
        },
        {
            "seq": 4,
            "ts": "2026-06-13T01:00:01.040Z",
            "client_order_id": "C-0002",
            "venue_order_id": "V-0002",
            "event_type": "rejected",
            "order_status": "REJECTED",
            "filled_qty": 0.0,
            "leaves_qty": 0.0,
            "reason": "risk_limit",
            "excerpt": "sandbox report: rejected by risk limit",
        },
    ]
    events: list[OrderEvent] = []
    for row in rows:
        seq = int(row["seq"])
        event_id = f"evt-{account_id}-{seq}"
        checksum = _checksum(event_id, row["event_type"], row["order_status"], row["filled_qty"])
        events.append(
            OrderEvent(
                event_id=event_id,
                seq=seq,
                ts_event=_utc(str(row["ts"])),
                ts_recv=_utc(str(row["ts"])),
                account_id=account_id,
                account_kind=account_kind,
                portfolio_uid=portfolio_uid,
                strategy_id="strategy.demo",
                instrument_id="IF.TEST",
                client_order_id=str(row["client_order_id"]),
                venue_order_id=str(row["venue_order_id"]),
                event_type=str(row["event_type"]),
                order_status=str(row["order_status"]),
                side="BUY",
                price=3512.5,
                quantity=2.0,
                filled_qty=float(row["filled_qty"]),
                last_px=row.get("last_px"),
                last_qty=row.get("last_qty"),
                leaves_qty=float(row["leaves_qty"]),
                reason=row.get("reason"),
                latency_ms=80.0,
                report_msg_type="sandbox_execution_report",
                report_msg_ref=f"fixture://mvp/report-msg/{seq}.json",
                report_msg_checksum=_checksum("report", seq),
                report_msg_excerpt=str(row["excerpt"]),
                source_ref=source_ref,
                checksum=checksum,
            )
        )
    return events


EVENTS = seed_order_events()


def list_account_snapshots() -> list[AccountSnapshot]:
    last = EVENTS[-1]
    return [
        AccountSnapshot(
            account_id=last.account_id,
            account_kind=last.account_kind,
            portfolio_uid=last.portfolio_uid,
            session_id="session.demo-20260613",
            equity=1_000_320.50,
            available_cash=812_000.00,
            margin_used=188_320.50,
            position_count=1,
            open_order_count=1,
            fill_count_today=1,
            event_lag_ms=0.0,
            health="event_stream_live",
            last_seq=last.seq,
            source_ref="fixture://mvp/account-snapshot.json",
            checksum=_checksum("snapshot", last.seq),
        )
    ]


def get_account_snapshot(account_id: str) -> AccountSnapshot | None:
    for snapshot in list_account_snapshots():
        if snapshot.account_id == account_id:
            return snapshot
    return None


def list_order_events(account_id: str, cursor: int = 0, limit: int = 500) -> list[OrderEvent]:
    return [
        event
        for event in EVENTS
        if event.account_id == account_id and event.seq > cursor
    ][:limit]


def list_order_execution_reports(account_id: str, client_order_id: str) -> list[OrderEvent]:
    return [
        event
        for event in EVENTS
        if event.account_id == account_id and event.client_order_id == client_order_id
    ]
