# Nautilus Account Console

Independent event-driven universal account console for Nautilus account read models.

This is the MVP technical skeleton for ADR-0045:

```text
Rust hot path -> durable event ledger -> Python query/control API -> TypeScript realtime UI
```

The project is read-only. It observes normalized account/order/fill/report events and reduced snapshots. It does not write trading runtime state, admission state, approval state, capital state or broker state.

## MVP Shape

```text
contracts/      shared JSON schema contracts
hotpath-rs/     Rust ingest, ledger and stream primitives
backend/        Python FastAPI API and reducer fixture
frontend/       Vite/React account console scaffold
docs/design/    UI design and acceptance gates
.github/        GitHub CI, PR/Issue templates and repo automation
```

UI design:

```text
docs/design/account-console-ui-mvp.md
docs/architecture/github-project-architecture.md
```

## GitHub

The repository is GitHub-ready:

```text
.github/workflows/ci.yml
.github/pull_request_template.md
.github/ISSUE_TEMPLATE/
.github/CODEOWNERS
.github/dependabot.yml
```

Project architecture and publish steps:

```text
docs/architecture/github-project-architecture.md
```

## Local Checks

Python:

```powershell
python -m compileall backend/src
```

Rust:

```powershell
cargo test --manifest-path hotpath-rs/Cargo.toml
```

Frontend, when Node/npm is available:

```powershell
cd frontend
npm install
npm run build
```

## Backend Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -e .
.\.venv\Scripts\nac --host 127.0.0.1 --port 8765
```

Then open:

```text
http://127.0.0.1:8765/api/accounts
http://127.0.0.1:8765/api/accounts/paper.demo-01/events/stream
```

## First Real Implementation Targets

1. Replace fixture events with file-backed append-only ledger reads.
2. Connect Rust hot path output to Python reducer/query cache.
3. Add typed benchmark output for `steady_1k_eps_5min` and `burst_10k_eps_30sec`.
4. Add frontend virtualized order event tape and report message drawer.
5. Add cross-language contract tests for Rust, Python and TypeScript.
