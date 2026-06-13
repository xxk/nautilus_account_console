from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from . import __version__
from .ledger import (
    get_account_snapshot,
    list_account_snapshots,
    list_order_events,
    list_order_execution_reports,
)
from .schemas import AccountDetail, AccountSnapshot, Health, OrderEvent, OrderExecutionReports


app = FastAPI(title="Nautilus Account Console API", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/healthz", response_model=Health)
def healthz() -> Health:
    return Health(ok=True, service="nautilus-account-console", version=__version__)


@app.get("/api/accounts", response_model=list[AccountSnapshot])
def accounts() -> list[AccountSnapshot]:
    return list_account_snapshots()


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
