# MVP Skeleton Self Acceptance / MVP 技术骨架自验收

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Scope: initial technical skeleton for ADR-0045
- Verdict: accepted as MVP skeleton, not accepted as production/HFT implementation

## 1. Acceptance Summary

| Area | Status | Evidence |
| --- | --- | --- |
| Project layout | pass | `contracts/`, `backend/`, `hotpath-rs/`, `frontend/` exist |
| Shared contracts | pass | JSON schemas for account event, order event, fill event, account snapshot and report msg exist |
| Python API skeleton | pass | FastAPI app exposes health, account list, account detail, event query, order execution reports query and SSE event stream |
| Python tests | pass | `python -m pytest backend\tests` -> 3 passed |
| Python compile | pass | `python -m compileall backend\src` -> passed |
| Rust hot path skeleton | pass | `nac_ingest`, `nac_ledger`, `nac_stream` crates exist |
| Rust tests | pass | `cargo test --manifest-path hotpath-rs\Cargo.toml` -> 3 passed |
| TypeScript UI scaffold | partial | Vite/React source exists, but Node/npm is unavailable in current environment |
| UI design doc | pass | `docs/design/account-console-ui-mvp.md` defines layout, route model, high-frequency interaction rules and UI acceptance |
| UI first screen shape | pass | Current React scaffold renders account overview, account summary, order event tape, selected-order execution reports panel and stream status |
| UI report msg drawer | partial | Current scaffold shows report refs/checksums/excerpts in the adjacent execution reports panel; raw payload drawer is successor work |
| Read-only boundary | pass | No runtime/admission/capital/broker writer implemented |
| Forbidden readiness wording | pass | UI does not display `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade` |
| HFT production evidence | not yet | benchmark harness and typed performance artifacts are successor work |

## 2. What This MVP Proves

1. The independent project can be developed outside `nautilus_strategies`.
2. The ADR-0045 three-layer shape is represented in code:
   - Rust hot path primitives
   - Python control/query API
   - TypeScript account console UI
3. The backend has a minimal end-to-end read model fixture:
   - account snapshot
   - order event list
   - cursor-filtered event query
   - SSE event stream
4. The Rust layer has minimal primitives for:
   - raw report normalization
   - append-only JSONL writing
   - bounded event batching
5. The UI first screen is an account console, not a landing page:
   - account overview
   - account detail summary
   - order event tape
   - adjacent selected-order execution reports panel
   - stream status
6. The UI design acceptance is documented in `docs/design/account-console-ui-mvp.md`.

## 3. Explicit Non-Acceptance

This MVP does not yet prove:

1. HFT capacity.
2. Durable ledger zero-loss under load.
3. 1k/10k events/sec benchmark budgets.
4. Real Nautilus runtime integration.
5. Real account reconciliation.
6. Real report msg payload storage and on-demand load.
7. Cross-language schema generation.
8. Browser build or runtime behavior, because Node/npm is unavailable in the current environment.
9. Paper readiness, Live readiness, capital allocation or broker tradability.
10. Raw report msg drawer behavior; the MVP scaffold currently shows refs/checksums/excerpts in the selected-order execution reports panel.

## 4. Successor Gates

Before this project can claim ADR-0045 HFT readiness, add:

1. `steady_1k_eps_5min` benchmark.
2. `burst_10k_eps_30sec` benchmark.
3. Cursor replay gap/duplicate tests.
4. Durable ledger checksum and rebuild tests.
5. Python reducer rebuild from Rust hotpath output.
6. Browser virtualized event tape test once Node/npm is available.
7. Large report msg on-demand payload test.
8. Cross-language contract tests for Rust, Python and TypeScript.
9. Raw report msg drawer with lazy payload fetch from a selected execution report.
10. UI route tests for `/accounts`, `/accounts/{account_id}` and `/accounts/{account_id}/events`.
11. Playwright screenshot/non-overlap checks once Node/npm is available.

## 5. Validation Commands

```powershell
python -m compileall backend\src
python -m pytest backend\tests
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit|cancel|place order|latest/debug|raw report.*truth|runtime truth|capital truth" .
```

Observed results on 2026-06-13:

```text
compileall: pass
pytest: 3 passed
cargo test: 3 passed
forbidden wording scan: no UI violation found
frontend build: blocked by missing/unavailable Node/npm
```
