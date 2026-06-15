# GitHub Project Architecture / GitHub 项目架构

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: MVP GitHub-ready skeleton

## 1. Repository Role

This repository owns the independent account observation console defined by ADR-0045 in `nautilus_strategies`.

It is intentionally separate from strategy/runtime repositories:

1. Strategy/runtime owners produce normalized events, typed artifacts and report message refs.
2. `nautilus_account_console` consumes those read-only sources.
3. The console provides account overview, account detail, order event tape, report message inspection and later performance/benchmark evidence views.

## 2. GitHub Layout

| Path | GitHub owner boundary | CI job |
| --- | --- | --- |
| `contracts/` | shared wire contracts and JSON schemas | boundary + future contract tests |
| `hotpath-rs/` | Rust event ingest, ledger and batching primitives | `rust` |
| `backend/` | Python FastAPI control/query API and reducer integration | `python` |
| `frontend/` | TypeScript/Vite account console UI | `frontend` |
| `docs/adr/` | local architecture decisions and governance rules | docs review |
| `docs/proposals/` | proposal templates and future proposal work items | docs review |
| `docs/topics/` | long-running topic roadmap kernel and topic status registry | docs review |
| `docs/templates/` | reference templates copied/learned from DSLresearch | docs review |
| `docs/design/` | UI and interaction design | docs review |
| `docs/acceptance/` | self-acceptance and successor gates | docs review |
| `docs/ownership/` | owner authority map and anti-second-implementation rules | docs review |
| `.github/` | CI, issue templates, PR template and repo automation | GitHub native |

## 3. CI Contract

The initial GitHub Actions workflow has four jobs:

| Job | Purpose |
| --- | --- |
| `python` | install backend, compile Python, run backend tests |
| `rust` | run Rust hotpath workspace tests |
| `frontend` | install frontend dependencies and build Vite app |
| `boundary` | scan implementation paths for forbidden readiness/runtime wording |

The boundary scan checks implementation paths only:

```text
frontend/src
backend/src
hotpath-rs/crates
```

Docs may contain forbidden phrases only as explicit negative rules.

## 4. Branch And PR Policy

Recommended branch model:

1. `main` is protected.
2. Pull requests are required for all changes.
3. Required checks:
   - `Python backend`
   - `Rust hotpath`
   - `Frontend`
   - `Read-only boundary scan`
4. PRs must fill the boundary checklist in `.github/pull_request_template.md`.

## 5. Issue Model

Use the GitHub issue templates:

1. `Feature` for implementation slices.
2. `Bug` for defects.

Every feature must declare:

1. The affected layer.
2. Acceptance evidence.
3. Read-only boundary checks.

## 6. Ownership

`.github/CODEOWNERS` currently contains placeholders because the GitHub organization and team names are not yet known.

After the repository is created, replace `@OWNER/...` with real users or teams.

The authority owner map is canonical even before GitHub team names are known:

```text
docs/ownership/account-console-owner-map.md
```

Recommended team split:

| Layer | Suggested team |
| --- | --- |
| `contracts/` | account-console-contracts |
| `hotpath-rs/` | account-console-hotpath |
| `backend/` | account-console-backend |
| `frontend/` | account-console-frontend |
| `docs/` | account-console-docs |
| `docs/ownership/` | account-console-architecture |

## 7. Publish Steps

When the GitHub owner/name is known:

```powershell
git init -b main
git add .
git commit -m "Bootstrap Nautilus Account Console MVP skeleton"
git remote add origin https://github.com/<owner>/nautilus_account_console.git
git push -u origin main
```

If using GitHub CLI:

```powershell
gh repo create <owner>/nautilus_account_console --private --source . --remote origin --push
```
