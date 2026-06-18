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

## Codex Project Worktree Layout

This repository participates in `D:/Nautilus/global_docs/adr/0006-project-scoped-codex-worktree-layout.md`.

Codex development branches should be opened from `D:/Nautilus/_worktrees/<project-topic>/nautilus_account_console/`. The primary repo at `D:/Nautilus/nautilus_account_console` is reserved for `main` / `master` sync, merges, worktree creation and recovery.

When a project also changes sibling owners, each sibling repo must have its own worktree under the same project topic:

```text
D:/Nautilus/_worktrees/<project-topic>/
  nautilus_strategies/
  nautilus_account_console/
  nautilus_ctp_adapter/
```

The `_worktrees` layout is operational only. It must not become runtime truth, account truth, broker truth, admission truth, proposal acceptance, or evidence truth. This repository still owns only read-only account console contracts, reducers, APIs, and UI projections.

Current repo/worktree gate:

```powershell
python D:/Nautilus/global_docs/scripts/check_codex_worktree_layout.py --repo .
```

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
python D:/Nautilus/global_docs/scripts/check_codex_worktree_layout.py --repo .
```

When Node/npm is available:

```powershell
cd frontend
npm install
npm run build
```


## Test Contract Change Authority / 测试契约修改权威

This repository participates in `D:/Nautilus/global_docs/adr/0008-test-contract-change-authority-and-human-approval-boundary.md` and `D:/Nautilus/global_docs/harness/Test Contract Change Authority Contract.md`.

Protected tests must not be weakened, replaced, skipped, deleted, renamed away, or retired by AI self-approval. Same-worktree password locks are not a security boundary. Any protected-test contract change requires a project-local change record plus worktree-external human approval, with the workspace policy anchored at `D:/Nautilus/_human_control/test_contract_authority/workspace_policy.yaml`.

Global adoption gate:

```powershell
python D:/Nautilus/global_docs/scripts/check_test_contract_authority_adoption.py
```

AI must not self-approve protected test contract changes.
