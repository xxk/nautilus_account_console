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
docs/adr/       local architecture decisions and governance rules
docs/proposals/ proposal templates copied/learned from DSLresearch
docs/topics/    topic roadmap kernel copied/learned from DSLresearch
docs/templates/ reference templates copied/learned from DSLresearch
docs/workflows/ proposal workflow gates copied/adapted from DSLresearch
.github/        GitHub CI, PR/Issue templates and repo automation
```

Architecture and UI design:

```text
docs/adr/README.md
docs/adr/0002-adopt-business-workbench-first-account-console-navigation.md
docs/adr/0003-adopt-contract-first-ui-slice-development.md
docs/proposals/README.md
docs/proposals/p001-daily-closeout-account-health-panel/README.md
docs/workflows/README.md
docs/workflows/proposal-gates/README.md
docs/topics/README.md
docs/topics/contract-first-ui-slice-development.md
docs/templates/README.md
docs/design/README.md
docs/design/account-console-ui-mvp.md
docs/design/account-console-capability-ui-design.md
docs/design/account-console-ui-implementation-design.md
docs/design/account-console-ui-landing-blueprint.md
docs/ownership/README.md
docs/ownership/account-console-owner-map.md
docs/acceptance/README.md
docs/acceptance/2026-06-13-account-console-capability-ui-acceptance.md
docs/acceptance/2026-06-13-account-console-ui-implementation-acceptance.md
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
python scripts/validate_owner_boundaries.py
python scripts/check_proposal_docs.py --root .
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
http://127.0.0.1:8765/api/accounts/paper.demo-01/orders/C-0001/execution-reports
```

## First Real Implementation Targets

1. Replace fixture events with file-backed append-only ledger reads.
2. Connect Rust hot path output to Python reducer/query cache.
3. Add typed benchmark output for `steady_1k_eps_5min` and `burst_10k_eps_30sec`.
4. Add frontend virtualized order event tape and report message drawer.
5. Add cross-language contract tests for Rust, Python and TypeScript.
