---
change-id: 20260629__adr0010-batch0-owner-carrier
status: superseded
work_item_layer: change_stub
---

# ADR-0010 Batch 0 Owner Carrier - nautilus_account_console

## Superseded / Closure

This Batch 0 bootstrap carrier is closed and superseded by the completed ADR-0010 landing matrix plus the repo-local WI-2/WI-7 change bundles. Do not treat these bootstrap slots as current pending work.

## Owner / Scope

- Owner repo: `nautilus_account_console`
- Scope:
  - WI-2: classify tracked browser evidence before any retirement.
  - WI-7: prepare codegen drift guard for Pydantic source -> JSON schema -> TypeScript types.

## WI-2 Tracked Artifact Inventory

| Class | Pattern | Count | Initial disposition |
| --- | --- | ---: | --- |
| browser evidence artifact | `docs/acceptance/browser-evidence/**` and proposal evidence image/html/jsonl/pdf | 121 | keep only if explicit evidence; otherwise move/offload before untracking |
| required fixture | none classified yet | 0 | must be explicitly named before retirement |
| runtime generated artifact | none classified in Batch 0 | 0 | superseded by WI-2 browser evidence retirement |

Sample paths:

- `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/desktop-happy.png`
- `docs/acceptance/browser-evidence/legacy-simulated-001-ag2612/desktop-legacy-simulated-001-ag2612.png`

## Acceptance Evidence Slots

| Scenario | red command | green command | fresh-clone command | Status |
| --- | --- | --- | --- | --- |
| RC-1 Batch entry gate | superseded by ADR-0010 accepted/completed ledger | WI-2/WI-7 carrier gates landed | ADR-0010 landing matrix is current source of truth | superseded |
| RC-2 WI-2 inventory classification | inventory above | `20260629__adr0010-wi2-browser-evidence-retirement` | ADR-0010 landing matrix is current source of truth | superseded |
| RC-3 WI-2 post-retirement guard | superseded by WI-2 carrier | `20260629__adr0010-wi2-browser-evidence-retirement` | ADR-0010 landing matrix is current source of truth | superseded |
| RC-5 WI-7 codegen drift guard | remove or stale `scripts/generate_account_contracts.py --check` output | `python scripts\generate_account_contracts.py --check` + `python -m pytest backend\tests -q` | `cd frontend && npm ci && npm run build` | WI-7 passed |
| RC-6 Evidence replay | superseded by WI-7 carrier | `20260629__adr0010__wi7-account-contract-codegen-drift` | ADR-0010 landing matrix is current source of truth | superseded |

## Rollback Boundary

WI-2 evidence retirement and WI-7 codegen drift work must be separate changes. WI-7 landed in `docs/changes/20260629__adr0010__wi7-account-contract-codegen-drift/`.
