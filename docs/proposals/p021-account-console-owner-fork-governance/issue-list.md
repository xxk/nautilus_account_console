# P021 Issue List / Owner-Fork Governance Ledger

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: draft
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

### P021-I1: Backend route_context fallback has two owners

| Field | Value |
| --- | --- |
| Status | `open` |
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

Must not:

1. Keep two independent fallback tables for the same account family.
2. Allow UI or tests to define route_context authority.

### P021-I2: Source package owner boundary is blurred by hard-coded output paths

| Field | Value |
| --- | --- |
| Status | `open` |
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

Must not:

1. Copy raw runtime secrets or raw broker endpoint material into this worktree.
2. Generate owner source packages locally as formal owner truth.
3. Treat repo-local `output/` as canonical owner root.

### P021-I3: Synthetic-ready Playwright mock can become a second projector

| Field | Value |
| --- | --- |
| Status | `open` |
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

Must not:

1. Let test payloads claim broker, account, runtime, capital or trading-readiness truth.
2. Use mocked API response as formal source package evidence.
3. Create feature-specific UI route implementation in tests.

### P021-I4: Frontend App.tsx registry is single today but fragile

| Field | Value |
| --- | --- |
| Status | `open` |
| Risk type | future fork risk |
| Current owner | account-console-frontend |
| Affected files | `frontend/src/App.tsx`; `frontend/src/types.ts`; `frontend/tests/README.md` |
| Evidence | `App.tsx` holds many fixture maps, route checks and panel render paths in one large module |
| Why it matters | future feature work can accidentally add feature-specific second route or fixture registries |
| Required phase | Phase 4 |
| Acceptance rows | A5, N5 |

Required governance:

1. Preserve one canonical production route/fixture registry.
2. Extract or document registry ownership before more panels are added.
3. Guard against production imports from `frontend/tests` and test-owned routes.

Must not:

1. Add top-level routes that duplicate Account Workbench panels.
2. Create route registration inside tests.
3. Let per-feature files become hidden route registries.

## Carry-Forward Rules

1. Any issue still `open` after a remediation attempt must name the blocker owner and retry condition.
2. Any stable rule learned from an issue must be backfilled to `docs/ownership/account-console-owner-map.md` or `frontend/tests/README.md`.
3. Test-only proof may close a guard row but cannot close real source-owner evidence.
4. If a child change is opened, it must cite the relevant P021 issue ID.
