# AGENTS.md - Nautilus Account Console

## Project Role

This repository owns the independent `nautilus_account_console` project described by ADR-0045 in `nautilus_strategies`.

It is a read-only account observation console for sandbox, real-feed sandbox Paper, broker paper probe, live broker and backtest replay read models.

## Hard Boundaries

1. Do not write runtime truth, admission truth, approval truth, capital truth or broker truth from this project.
2. Raw report messages are provenance/debug payloads only. Account, order, fill and position state must come from normalized events or reduced read models.
3. The UI may show stream health and lag, but must not display `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade`.
4. HFT acceptance requires typed benchmark evidence for durable ledger zero-loss, bounded lag, cursor replay, backpressure and virtualized browser rendering.
5. Rust owns the default high-frequency hot path. Python owns control/query/integration. TypeScript owns the browser projection.

## Layout

| Path | Responsibility |
| --- | --- |
| `contracts/` | Shared JSON schemas and wire contracts |
| `hotpath-rs/` | Rust event ingest, cursor/dedupe, batching and durable ledger primitives |
| `backend/` | Python FastAPI control/query API and reducer/read model integration |
| `frontend/` | TypeScript/Vite account console UI |

## Validation

Use the fastest applicable checks:

```powershell
python -m compileall backend/src
cargo test --manifest-path hotpath-rs/Cargo.toml
```

When Node/npm is available:

```powershell
cd frontend
npm install
npm run build
```

