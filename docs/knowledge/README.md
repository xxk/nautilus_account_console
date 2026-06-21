# Account Console Knowledge Base

This directory is the project-local knowledge base for `nautilus_account_console`.

It records durable project facts, repeat-bug lessons and AI routing hints. It is not a runtime, broker, account, admission, approval, capital, trading-readiness, proposal, change or acceptance truth source.

## Precedence

1. Current task truth: active proposal, change, acceptance, AGENTS and owner docs.
2. Local router: [blocker-routing.json](blocker-routing.json).
3. Matched local cards only.
4. Optional shared pattern files under `D:\Nautilus\global_docs\knowledge-common`.

AI must not read the whole shared knowledge base or this whole directory by default. Use the router first, then read only matched files.

## Shared Knowledge Boundary

Shared knowledge belongs in:

```text
D:\Nautilus\global_docs\knowledge-common
```

Shared knowledge owns reusable patterns and templates. This directory owns Account Console facts, local boundaries and local bug memory. Do not copy Account Console owner facts, local evidence or proposal state into shared knowledge as global truth.

## Forbidden Content

Knowledge cards must not contain:

1. Raw passwords, auth codes, raw front addresses, API keys, account secrets or broker secrets.
2. Raw endpoint values, raw config bodies or secret-bearing runtime material.
3. Current proposal/change acceptance pass or fail state.
4. Account, broker, runtime, admission, approval, capital or trading-readiness truth.
5. Order action instructions or command authorization.

## Required Local Files

| File | Purpose |
| --- | --- |
| [00-dashboard.md](00-dashboard.md) | Navigation-only dashboard |
| [project-playbook.md](project-playbook.md) | AI/human project-local playbook |
| [blocker-routing.json](blocker-routing.json) | Minimal-read knowledge router |
| [owner-boundaries.md](owner-boundaries.md) | Local owner boundary memory |
| [account-console-read-model-boundary.md](account-console-read-model-boundary.md) | Read-model and raw payload boundary |
| [ui-projection-boundary.md](ui-projection-boundary.md) | UI projection wording boundary |
| [runtime-secret-boundary.md](runtime-secret-boundary.md) | Sensitive runtime material boundary |
| [bug-ledger/](bug-ledger/README.md) | Repeat-bug cards |
| [templates/bug-card.md](templates/bug-card.md) | Bug-card template |
| [adoption-note.md](adoption-note.md) | Cross-project adoption note |

