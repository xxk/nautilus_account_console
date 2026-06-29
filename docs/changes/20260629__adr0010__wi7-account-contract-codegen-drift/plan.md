---
id: 20260629__adr0010__wi7-account-contract-codegen-drift
status: completed
execution-mode: micro_change
type: child-change
date: 2026-06-29
scope: ADR-0010 WI-7 account contract codegen drift guard
change-domain: adr0010
control-plane-kind: change
control-plane-title: ADR-0010 WI-7 account contract codegen drift guard
control-plane-ref: docs/changes/20260629__adr0010__wi7-account-contract-codegen-drift/
acceptance: ./acceptance.md
progress: "100%"
---

# ADR-0010 WI-7 Account Contract Codegen Drift Guard

## Capability Mapping

```text
- capability_id: architecture.adr0010.wi7.account_contract_codegen_drift
- capability_name: Pydantic account contract source generates JSON schema and TypeScript types
- long_term_target: backend/src/nautilus_account_console/schemas.py
- affects_long_term_rules: yes
- change_type: child_change
```

## Scope

- Make Pydantic models in `backend/src/nautilus_account_console/schemas.py` the source of truth for account contract primitives.
- Generate `contracts/account_snapshot.schema.json`, `contracts/account_event.schema.json`, `contracts/order_event.schema.json`, and the top contract section of `frontend/src/types.ts`.
- Add a check-mode guard so schema/TypeScript drift fails in CI or local verification.

## Historical Scheme & Bug Inventory

| Historical item | Risk | Treatment | Guard |
| --- | --- | --- | --- |
| `AccountKind` values were hand-copied into Pydantic, JSON schema, and TypeScript | future account kind additions drift across layers | test guard | `python scripts/generate_account_contracts.py --check` |
| `OrderEvent` JSON schema required fewer fields than the Pydantic model | UI/API contract accepted stale payload shape | supersede | generated `order_event.schema.json` from Pydantic |
| `account_event.schema.json` had no Pydantic owner | orphan schema could diverge silently | rename/supersede | new `AccountEvent` model plus generated schema |
| TypeScript core account types were manually maintained | frontend could compile against stale shape | test guard | generated top section in `frontend/src/types.ts` |

## Contract-Lock Evidence Plan

- Red command: `python -m pytest backend\tests\test_adr0010_wi7_codegen_drift.py -q` failed before the generator existed.
- Green command: `python scripts\generate_account_contracts.py --check` and `python -m pytest backend\tests -q`.
- Fresh-clone command: `cd frontend && npm ci && npm run build`.

## Out Of Scope

- No UI layout or behavior change.
- No browser evidence retirement.
- No broader panel contract codegen for every `contracts/ui/panels/*.json`.

## Rollback Boundary

Reverting this change removes the codegen drift guard and restores manual synchronization risk across Pydantic, JSON schema, and TypeScript.

