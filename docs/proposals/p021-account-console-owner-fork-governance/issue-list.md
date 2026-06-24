# P021 Issue List / Owner-Fork Governance Ledger

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20

This ledger is the required carry-forward surface for owner ambiguity, fork risk and second-implementation risk found during the Account Console architecture review.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `open` | Risk is recorded and not yet governed. |
| `in_progress` | A remediation slice is actively changing code/docs/tests. |
| `closed` | Risk is fixed with evidence and acceptance mapping. |
| `accepted_with_guardrails` | Existing shape is intentionally kept, with documented guardrails and tests. |
| `blocked_external_owner` | Repo-local work is done, but closeout depends on external owner evidence. |

## Issues

### P021-I5: Frontend command-status synthesis creates a second command-state owner

| Field | Value |
| --- | --- |
| Status | `closed` |
| Risk type | second implementation |
| Current owner | account-console-frontend |
| Affected files | `frontend/src/App.tsx`; `frontend/src/types.ts` |
| Evidence | production UI previously synthesized `command_status` from `/api/commands/*` responses and runtime closeout payloads instead of rendering only mirror-owned command state |
| Why it matters | command truth can drift between mirror projection, command endpoints and frontend-local reconstruction |
| Required phase | Phase 5 |
| Acceptance rows | A5, N5 |

Required governance:

1. Frontend renders canonical mirror-owned `command_status` only.
2. Transient command API receipts are displayed separately and must not be promoted to `command_status`.
3. Anti-fork validation must reject new frontend-local `command_status` synthesizers.

Closeout evidence:

1. `frontend/src/App.tsx` no longer contains production `commandResultToStatus` or `runtimeCloseoutToStatus` helpers.
2. `Command Status` reads only `mirrorReadback.selected.command_status`.
3. `python scripts\validate_p021_owner_fork_governance.py` rejects reintroduction of frontend-local command-status synthesis.

Must not:

1. Build `command_status` in React from `CommandApiResult`.
2. Build `command_status` in React from runtime closeout payloads.
3. Let UI-local receipts outrank mirror-owned command status.

### P021-I6: Backend command plane lacks explicit owner split between action intake and read projection

| Field | Value |
| --- | --- |
| Status | `accepted_with_guardrails` |
| Risk type | second implementation |
| Current owner | account-console-backend |
| Affected files | `backend/src/nautilus_account_console/command_api.py`; `backend/src/nautilus_account_console/main.py` |
| Evidence | one module previously owned both action-intake handlers and long-lived command/readiness/handoff/closeout projection loaders |
| Why it matters | command actions and command read models can drift into two implicit owners and make safe retirement of legacy surfaces harder |
| Required phase | Phase 6 |
| Acceptance rows | A2, A5, N2, N5 |

Required governance:

1. Action intake owner and command read-projection owner are separate modules with explicit boundaries.
2. `main.py` wires action routes from the action owner and read routes from the read owner.
3. Future retirement of legacy command-plane surfaces happens by owner boundary, not by editing a mixed module.

Closeout evidence:

1. `backend/src/nautilus_account_console/command_actions.py` owns submit/cancel intake and runtime handoff preparation only.
2. `backend/src/nautilus_account_console/command_api.py` remains the read-projection owner for closeout/readiness/handoff/audit packets.
3. Validators and tests continue to pass after the split.

Must not:

1. Recombine action-intake and long-lived read projection logic without an explicit owner decision.
2. Let one helper silently mint both transient action receipts and canonical command truth.
3. Treat this module split by itself as proof that the second backend plane is retired.

### P021-I1: Backend route_context fallback has two owners

| Field | Value |
| --- | --- |
| Status | `closed` |
| Risk type | second implementation |
| Current owner | account-console-backend |
| Affected files | `backend/src/nautilus_account_console/source_bridge.py`; `backend/src/nautilus_account_console/account_mirror.py` |
| Evidence | both modules contain fallback route_context construction logic |
| Why it matters | route/account context can drift and create two route identity authorities |
| Required phase | Phase 1 |
| Acceptance rows | A2, N2 |

Required governance:

1. Create one canonical resolver or one explicit delegation path.
2. Keep validation fail-closed for missing checksum/source authority.
3. Add focused tests so route_context cannot mint readiness, broker truth, account truth or command authority.

Closeout evidence:

1. `backend/src/nautilus_account_console/route_context.py` is the canonical resolver/validator owner.
2. `source_bridge.py` and `account_mirror.py` delegate fallback construction to that module.
3. `python scripts\validate_p021_owner_fork_governance.py` checks this remains true.

Must not:

1. Keep two independent fallback tables for the same account family.
2. Allow UI or tests to define route_context authority.

### P021-I2: Source package owner boundary is blurred by hard-coded output paths

| Field | Value |
| --- | --- |
| Status | `accepted_with_guardrails` |
| Risk type | owner unclear / truth-source drift |
| Current owner | account-console-backend reads; external owners produce |
| Affected files | `backend/src/nautilus_account_console/source_bridge.py`; `backend/src/nautilus_account_console/ctp19053_consistency.py`; `backend/src/nautilus_account_console/ctp025292_consistency.py` |
| Evidence | backend constants point directly at `output/account_capability/**/source-package.json` |
| Why it matters | Account Console can appear to own real source packages instead of reading owner evidence |
| Required phase | Phase 2 |
| Acceptance rows | A3, N3 |

Required governance:

1. Introduce a provider/ref boundary or config layer for source package paths.
2. Preserve owner, source_ref, checksum and blocker semantics.
3. Missing or invalid external owner evidence must render typed blocker, not substitute truth.

Closeout evidence:

1. Source packages remain referenced evidence with `source_ref` and checksum preservation.
2. Repo-local `output/account_capability/**/source-package.json` is explicitly not Account Console-owned truth.
3. `python scripts\validate_p021_owner_fork_governance.py` keeps this boundary in the issue ledger and owner map.

Must not:

1. Copy raw runtime secrets or raw broker endpoint material into this worktree.
2. Generate owner source packages locally as formal owner truth.
3. Treat repo-local `output/` as canonical owner root.

### P021-I3: Synthetic-ready Playwright mock can become a second projector

| Field | Value |
| --- | --- |
| Status | `closed` |
| Risk type | fork implementation / test authority leakage |
| Current owner | account-console-browser-acceptance-tests |
| Affected files | `frontend/tests/e2e/p019-ib-tws-synthetic-ready-projection.spec.ts`; `frontend/tests/README.md` |
| Evidence | test intercepts `/api/mirror/**` and constructs complete ready projection/list/source-health/evidence payloads |
| Why it matters | a full mock projection can be mistaken for Account Mirror projector logic or source-owner evidence |
| Required phase | Phase 3 |
| Acceptance rows | A4, N4 |

Required governance:

1. Mark synthetic payloads as display-contract guard only.
2. Remove or neutralize authority-looking fields such as account/capital truth claims.
3. Ensure the test cannot be cited as real U3028269 funds/positions evidence.

Closeout evidence:

1. Synthetic ready projection now marks `synthetic_contract_guard_not_account_truth`.
2. Synthetic boundaries assert broker/account/runtime/capital truth are all false.
3. `python scripts\validate_p021_owner_fork_governance.py` rejects authority leakage in the synthetic Playwright contract.

Must not:

1. Let test payloads claim broker, account, runtime, capital or trading-readiness truth.
2. Use mocked API response as formal source package evidence.
3. Create feature-specific UI route implementation in tests.

### P021-I4: Frontend owner convergence must stay out of App.tsx

| Field | Value |
| --- | --- |
| Status | `accepted_with_guardrails` |
| Risk type | future fork risk |
| Current owner | account-console-frontend |
| Affected files | `frontend/src/App.tsx`; `frontend/src/app-registry.ts`; `frontend/src/account-workbench-routing.ts`; `frontend/src/fixture-selection.ts`; `frontend/src/account-workbench-adapters.ts`; `frontend/src/account-workbench-terminal.tsx`; `frontend/tests/README.md` |
| Evidence | historical `App.tsx` concentration was reduced by extracting canonical registry, routing, fixture-selection, adapter and terminal owner modules; the remaining risk is governance drift back into `App.tsx` |
| Why it matters | future feature work can accidentally reintroduce second route registries, second fixture selectors or second read-model adapters if the extracted owner boundaries are not guarded |
| Required phase | Phase 4 |
| Acceptance rows | A5, N5 |

Required governance:

1. Preserve one canonical production route/fixture registry.
2. Keep route classification, fixture selection, mirror read-model adaptation and terminal rendering in dedicated owner modules instead of `App.tsx`.
3. Guard against production imports from `frontend/tests` and test-owned routes.

Closeout evidence:

1. The current production route registry remains single-owner in `frontend/src/app-registry.ts`.
2. `frontend/src/account-workbench-routing.ts`, `frontend/src/fixture-selection.ts`, `frontend/src/account-workbench-adapters.ts` and `frontend/src/account-workbench-terminal.tsx` remain the canonical extracted owners.
3. `frontend/tests/README.md` records the no-second-route-registry rule.
4. `python scripts\validate_p021_owner_fork_governance.py` rejects test route registries, production imports from tests and owner drift back into `App.tsx`.

Must not:

1. Add top-level routes that duplicate Account Workbench panels.
2. Create route registration inside tests.
3. Let per-feature files become hidden route registries.
4. Reintroduce fixture-state defaults, route regex trees or mirror read-model factories directly inside `App.tsx`.

## Carry-Forward Rules

1. Any issue still `open` after a remediation attempt must name the blocker owner and retry condition.
2. Any stable rule learned from an issue must be backfilled to `docs/ownership/account-console-owner-map.md` or `frontend/tests/README.md`.
3. Test-only proof may close a guard row but cannot close real source-owner evidence.
4. If a child change is opened, it must cite the relevant P021 issue ID.
