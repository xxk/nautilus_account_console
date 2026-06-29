---
change-id: 20260629__adr0010-batch0-owner-carrier
status: draft
work_item_layer: change_stub
---

# ADR-0010 Batch 0 Owner Carrier - nautilus_account_console

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
| runtime generated artifact | none classified yet | 0 | pending deeper classification |

Sample paths:

- `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/desktop-happy.png`
- `docs/acceptance/browser-evidence/legacy-simulated-001-ag2612/desktop-legacy-simulated-001-ag2612.png`

## Acceptance Evidence Slots

| Scenario | red command | green command | fresh-clone command | Status |
| --- | --- | --- | --- | --- |
| RC-1 Batch entry gate | pending | pending | pending | slot-created |
| RC-2 WI-2 inventory classification | inventory above | pending | pending | slot-created |
| RC-3 WI-2 post-retirement guard | pending | pending | pending | slot-created |
| RC-6 Evidence replay | pending | pending | pending | slot-created |

## Rollback Boundary

WI-2 evidence retirement and WI-7 codegen drift work must be separate changes.
