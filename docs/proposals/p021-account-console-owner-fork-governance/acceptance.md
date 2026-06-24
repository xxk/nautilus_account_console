# P021 Account Console Owner/Fork Governance Acceptance / 验收

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-23
- Linked proposal: [README.md](README.md)
- Linked phase plan: [phase-plan.md](phase-plan.md)
- Linked issue list: [issue-list.md](issue-list.md)

## Acceptance Scope / 验收范围

This proposal accepts only governance and implementation-hardening work for owner/fork/second-implementation risks.

In scope:

1. Route-context owner convergence.
2. Source-package provider ownership boundary.
3. Synthetic-ready browser test boundary.
4. Frontend route/fixture registry governance.
5. Frontend command-status owner convergence.
6. Backend command-plane owner convergence.
7. Issue-ledger closeout discipline.

Out of scope:

1. Broker, runtime, account, order, fill, position, ledger, admission, approval, capital or trading-readiness truth.
2. Any direct TWS/CTP session opening from Account Console.
3. Replacing external owner evidence with local generated evidence.
4. Protected-test weakening or AI self-approval of test contract changes.

## Acceptance Evidence Boundary

1. Test-only evidence is guard evidence, not formal source-owner truth.
2. Browser mocks prove UI display behavior only.
3. Source-package closeout requires source_ref, checksum and owner boundary.
4. Missing external owner evidence must become a typed blocker, not a local substitute.
5. A proposal scenario cannot pass unless its paired anti-drift row is mapped.

Historical artifact rule:

1. Archive-only browser evidence or time-point acceptance artifacts may still reference historical implementation paths such as `frontend/src/App.tsx`.
2. Those historical paths prove what rendered at that time; they do not redefine the current canonical frontend owner boundary.
3. Current owner authority comes from the owner map, active proposal docs and validator-backed canonical owner modules.

## Mandatory Gate Coverage

| Gate | Requirement | Applies when | Must fail if | Status |
| --- | --- | --- | --- | --- |
| G1 Owner issue ledger | Every discovered issue is recorded with owner, evidence, phase and acceptance row | all P021 work | issue remains only in chat or commit text | passed |
| G2 Route-context single owner | Backend route_context generation has one canonical resolver or explicit delegation | backend route context work | same account class has independent fallback business rules in two modules | passed |
| G3 Source package owner boundary | Source packages are read as owner evidence, not Account Console-owned truth | real account source package path work | local output path is treated as canonical source owner | passed_with_guardrails |
| G4 Synthetic test display-only boundary | Synthetic-ready e2e remains display guard only | Playwright mock projection work | mocked projection claims account/capital/broker/runtime truth | passed |
| G5 Frontend canonical registry | Route/fixture registry remains single-owner and production-owned | frontend route/panel work | feature-specific second route registry appears | passed_with_guardrails |
| G6 Frontend command-state single owner | Canonical `command_status` comes only from mirror-owned projection | frontend command-state work | UI synthesizes canonical command status from transient command surfaces | passed |
| G7 Backend command-plane owner split | Action intake and canonical command read projection stay explicitly separated | backend command-plane work | mixed module or legacy read surface becomes canonical command truth | passed_with_guardrails |
| G9 Frontend legacy governance suite owner | Legacy governance panels are consumed as one governed suite contract | frontend command-plane retirement work | `App.tsx` owns scattered per-panel governance state or settled-result retirement semantics | passed_with_guardrails |
| G8 Protected test authority | Existing tests are not weakened, skipped, renamed away or retired by AI self-approval | any test change | protected test contract is weakened without human approval | passed |

## Scenario Matrix / 验收场景矩阵

| ID | Type | Scenario | Verification | Pass signal | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | success | P021 opens with all six discovered risks in issue-list | docs review | P021-I1 through P021-I6 present with owner/phase/acceptance mapping | passed |
| N1 | drift | A discovered risk is only in chat and not mapped to issue-list | docs review | `owner_issue_unmapped` | passed |
| A2 | success | Route-context resolver has one canonical owner path | backend tests + source review | no duplicate fallback route_context logic for same account family | passed |
| N2 | drift | `source_bridge.py` and `account_mirror.py` independently mint route_context for the same account family | source review / focused test | `route_context_second_resolver` | passed |
| A3 | success | Source package loading is owner-explicit and fail-closed | backend tests | missing/invalid package becomes typed blocker | passed_with_guardrails |
| N3 | drift | `output/account_capability/**/source-package.json` is accepted as local truth without owner/source_ref/checksum | backend tests / source review | `source_package_owner_boundary_violation` | passed_with_guardrails |
| A4 | success | Synthetic-ready e2e mock is display-only and cannot be real source evidence | frontend test + source review | mock authority says synthetic contract guard only; no account/capital truth claims | passed |
| N4 | drift | Synthetic mock payload carries `account_truth: true`, `capital_truth: true`, command authority or readiness claim | source review / e2e negative assertion | `synthetic_projection_authority_leak` | passed |
| A5 | success | Frontend route/fixture registry has one canonical production owner and extracted owner modules | owner boundary gate + source review | no test-owned or feature-specific second route registry; `App.tsx` consumes canonical registry/routing/fixture-selection/adapters/terminal owners | passed_with_guardrails |
| N5 | drift | A test or feature file creates a second production-like route registry or special runtime path | owner boundary gate / source review | `frontend_second_route_registry` | passed_with_guardrails |
| A6 | success | Frontend command status renders only mirror-owned canonical projection | source review + e2e evidence | no production command-status synthesis helpers remain; receipt UI is separate | passed |
| N6 | drift | Frontend reconstructs canonical command status from `CommandApiResult` or runtime closeout payloads | source review / anti-fork gate | `frontend_command_status_second_owner` | passed |
| A7 | success | Backend exposes a canonical command-plane projection with mirror as durable owner | backend tests + source review | `/api/commands/accounts/{account_id}/projection` points to mirror as canonical command truth | passed_with_guardrails |
| N7 | drift | Backend legacy command reads or mixed modules become canonical command-state truth | backend tests / anti-fork gate | `backend_command_plane_owner_drift` | passed_with_guardrails |
| A10 | success | Frontend legacy governance panels are held as one governed suite contract | source review + anti-fork gate | `legacyCommandPanels` is the only App-level legacy governance state owner | passed_with_guardrails |
| N10 | drift | Frontend reintroduces per-panel legacy governance state or local retirement semantics | source review / anti-fork gate | `frontend_legacy_governance_suite_fork` | passed_with_guardrails |
| A8 | success | Existing owner-boundary gate still passes after governance work | `python scripts\validate_owner_boundaries.py` | `owner boundary validation passed` | passed |
| N8 | drift | Governance work weakens owner-boundary gate coverage or removes negative checks | git/source review | `owner_gate_weakened` | passed |
| A9 | success | Proposal docs gate passes for P021 | `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` | `PROPOSAL_DOCS_OK` | passed |
| N9 | drift | P021 closes while docs gate fails or issue-list remains open without typed blocker | docs gate + issue review | `proposal_closeout_unverified` | passed |

## Positive-to-Negative Coverage Map

| Positive scenario | Required anti-drift rows | Coverage rule |
| --- | --- | --- |
| A1 Issue ledger | N1 | Issue inventory cannot pass unless every discovered risk is mapped. |
| A2 Route-context convergence | N2 | Route-context work cannot pass with duplicate fallback business logic. |
| A3 Source package boundary | N3 | Provider boundary cannot pass if local output path becomes truth owner. |
| A4 Synthetic test boundary | N4 | Synthetic e2e cannot pass if mock payload claims real authority. |
| A5 Frontend registry governance | N5 | Registry governance cannot pass with feature-specific second registry. |
| A6 Frontend command-state owner convergence | N6 | Frontend command-state work cannot pass if transient command surfaces become canonical truth. |
| A7 Backend command-plane owner convergence | N7 | Backend command-plane work cannot pass if legacy command reads become canonical truth. |
| A10 Frontend legacy governance suite owner | N10 | Frontend retirement work cannot pass if per-panel governance state or local retirement semantics return. |
| A8 Owner-boundary gate | N8 | Governance cannot pass if gates are weakened. |
| A9 Proposal docs | N9 | Closeout cannot pass with failing docs gate or open unmapped issues. |

## Issue-to-Acceptance Map

| Issue | Acceptance rows | Required closeout evidence |
| --- | --- | --- |
| P021-I1 route_context duplicated fallback | A2, N2 | backend tests, source review, issue-list closeout |
| P021-I2 source package owner boundary | A3, N3 | backend tests, typed blocker behavior, owner map or README update |
| P021-I3 synthetic ready mock risk | A4, N4 | e2e/source review, no authority leakage, issue-list closeout |
| P021-I4 frontend registry fragility | A5, N5 | owner boundary gate, frontend build/e2e or source review proving `App.tsx` is composition-only and owner modules are canonical |
| P021-I5 frontend command-status synthesis | A6, N6 | source review, E2E evidence, validator rejection of local command-status synthesis |
| P021-I6 backend action/read owner split | A7, N7 | backend tests, canonical command-plane projection route, centralized frontend legacy-read suite, validator rejection of owner drift |
| P021-I6 backend action/read owner split | A10, N10 | governed frontend legacy panel suite contract, App shell no longer owns scattered panel retirement state |

## Evidence

| Evidence | Command / path | Result |
| --- | --- | --- |
| Owner boundary gate before P021 | `python scripts\validate_owner_boundaries.py` | `owner boundary validation passed` |
| P021 proposal docs | `docs/proposals/p021-account-console-owner-fork-governance/` | created |
| P021 governance validator | `python scripts\validate_p021_owner_fork_governance.py` | `P021_OWNER_FORK_GOVERNANCE_OK: issues=6 route_context=canonical synthetic=guarded registry=single_owner` |
| Focused backend tests | `python -m pytest backend\tests\test_mirror_api.py backend\tests\test_source_bridge.py backend\tests\test_account_mirror.py -q` | `13 passed in 0.51s` |
| Proposal docs gate | `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` | `PROPOSAL_DOCS_OK: proposals=1` |
| Synthetic projection e2e | `cmd /c npx playwright test tests/e2e/p019-ib-tws-synthetic-ready-projection.spec.ts --project=desktop --reporter=line` | `1 passed` |
| Frontend command-state retirement | `frontend/src/App.tsx` composition root plus canonical frontend owner modules; `frontend/tests/e2e/p024-partial-fill-cancel-order-display.spec.ts`; `frontend/tests/e2e/p024-runtime-closeout-evidence.spec.ts` | mirror-owned status only; transient receipt separated |
| Frontend owner convergence extraction | `frontend/src/app-registry.ts`; `frontend/src/account-workbench-routing.ts`; `frontend/src/fixture-selection.ts`; `frontend/src/account-workbench-adapters.ts`; `frontend/src/account-workbench-terminal.tsx`; `python scripts\validate_p021_owner_fork_governance.py` | registry/routing/fixture-selection/read-model/terminal owners extracted; App shell guarded against re-growth |
| Backend command-plane projection | `python -m pytest backend\tests\test_command_api.py -q` | canonical `/api/commands/accounts/{account_id}/projection` declares mirror owner |

## Required Before Closeout

1. `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` passes.
2. `python scripts\validate_owner_boundaries.py` passes.
3. Each P021 issue is `closed`, `accepted_with_guardrails` or `blocked_external_owner` with exact next action.
4. No issue remains `open`.
5. Any stable governance rule is backfilled to the owner map or frontend tests README.
