# P021 Account Console Owner/Fork Governance Acceptance / 验收

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20
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
5. Issue-ledger closeout discipline.

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

## Mandatory Gate Coverage

| Gate | Requirement | Applies when | Must fail if | Status |
| --- | --- | --- | --- | --- |
| G1 Owner issue ledger | Every discovered issue is recorded with owner, evidence, phase and acceptance row | all P021 work | issue remains only in chat or commit text | passed |
| G2 Route-context single owner | Backend route_context generation has one canonical resolver or explicit delegation | backend route context work | same account class has independent fallback business rules in two modules | passed |
| G3 Source package owner boundary | Source packages are read as owner evidence, not Account Console-owned truth | real account source package path work | local output path is treated as canonical source owner | passed_with_guardrails |
| G4 Synthetic test display-only boundary | Synthetic-ready e2e remains display guard only | Playwright mock projection work | mocked projection claims account/capital/broker/runtime truth | passed |
| G5 Frontend canonical registry | Route/fixture registry remains single-owner and production-owned | frontend route/panel work | feature-specific second route registry appears | passed_with_guardrails |
| G6 Protected test authority | Existing tests are not weakened, skipped, renamed away or retired by AI self-approval | any test change | protected test contract is weakened without human approval | passed |

## Scenario Matrix / 验收场景矩阵

| ID | Type | Scenario | Verification | Pass signal | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | success | P021 opens with all four discovered risks in issue-list | docs review | P021-I1 through P021-I4 present with owner/phase/acceptance mapping | passed |
| N1 | drift | A discovered risk is only in chat and not mapped to issue-list | docs review | `owner_issue_unmapped` | passed |
| A2 | success | Route-context resolver has one canonical owner path | backend tests + source review | no duplicate fallback route_context logic for same account family | passed |
| N2 | drift | `source_bridge.py` and `account_mirror.py` independently mint route_context for the same account family | source review / focused test | `route_context_second_resolver` | passed |
| A3 | success | Source package loading is owner-explicit and fail-closed | backend tests | missing/invalid package becomes typed blocker | passed_with_guardrails |
| N3 | drift | `output/account_capability/**/source-package.json` is accepted as local truth without owner/source_ref/checksum | backend tests / source review | `source_package_owner_boundary_violation` | passed_with_guardrails |
| A4 | success | Synthetic-ready e2e mock is display-only and cannot be real source evidence | frontend test + source review | mock authority says synthetic contract guard only; no account/capital truth claims | passed |
| N4 | drift | Synthetic mock payload carries `account_truth: true`, `capital_truth: true`, command authority or readiness claim | source review / e2e negative assertion | `synthetic_projection_authority_leak` | passed |
| A5 | success | Frontend route/fixture registry has one canonical production owner | owner boundary gate + source review | no test-owned or feature-specific second route registry | passed_with_guardrails |
| N5 | drift | A test or feature file creates a second production-like route registry or special runtime path | owner boundary gate / source review | `frontend_second_route_registry` | passed_with_guardrails |
| A6 | success | Existing owner-boundary gate still passes after governance work | `python scripts\validate_owner_boundaries.py` | `owner boundary validation passed` | passed |
| N6 | drift | Governance work weakens owner-boundary gate coverage or removes negative checks | git/source review | `owner_gate_weakened` | passed |
| A7 | success | Proposal docs gate passes for P021 | `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` | `PROPOSAL_DOCS_OK` | passed |
| N7 | drift | P021 closes while docs gate fails or issue-list remains open without typed blocker | docs gate + issue review | `proposal_closeout_unverified` | passed |

## Positive-to-Negative Coverage Map

| Positive scenario | Required anti-drift rows | Coverage rule |
| --- | --- | --- |
| A1 Issue ledger | N1 | Issue inventory cannot pass unless every discovered risk is mapped. |
| A2 Route-context convergence | N2 | Route-context work cannot pass with duplicate fallback business logic. |
| A3 Source package boundary | N3 | Provider boundary cannot pass if local output path becomes truth owner. |
| A4 Synthetic test boundary | N4 | Synthetic e2e cannot pass if mock payload claims real authority. |
| A5 Frontend registry governance | N5 | Registry governance cannot pass with feature-specific second registry. |
| A6 Owner-boundary gate | N6 | Governance cannot pass if gates are weakened. |
| A7 Proposal docs | N7 | Closeout cannot pass with failing docs gate or open unmapped issues. |

## Issue-to-Acceptance Map

| Issue | Acceptance rows | Required closeout evidence |
| --- | --- | --- |
| P021-I1 route_context duplicated fallback | A2, N2 | backend tests, source review, issue-list closeout |
| P021-I2 source package owner boundary | A3, N3 | backend tests, typed blocker behavior, owner map or README update |
| P021-I3 synthetic ready mock risk | A4, N4 | e2e/source review, no authority leakage, issue-list closeout |
| P021-I4 frontend registry fragility | A5, N5 | owner boundary gate, frontend build/e2e or source review |

## Evidence

| Evidence | Command / path | Result |
| --- | --- | --- |
| Owner boundary gate before P021 | `python scripts\validate_owner_boundaries.py` | `owner boundary validation passed` |
| P021 proposal docs | `docs/proposals/p021-account-console-owner-fork-governance/` | created |
| P021 governance validator | `python scripts\validate_p021_owner_fork_governance.py` | `P021_OWNER_FORK_GOVERNANCE_OK: issues=4 route_context=canonical synthetic=guarded registry=single_owner` |
| Focused backend tests | `python -m pytest backend\tests\test_mirror_api.py backend\tests\test_source_bridge.py backend\tests\test_account_mirror.py -q` | `13 passed in 0.51s` |
| Proposal docs gate | `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` | `PROPOSAL_DOCS_OK: proposals=1` |
| Synthetic projection e2e | `cmd /c npx playwright test tests/e2e/p019-ib-tws-synthetic-ready-projection.spec.ts --project=desktop --reporter=line` | `1 passed` |

## Required Before Closeout

1. `python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance` passes.
2. `python scripts\validate_owner_boundaries.py` passes.
3. Each P021 issue is `closed`, `accepted_with_guardrails` or `blocked_external_owner` with exact next action.
4. No issue remains `open`.
5. Any stable governance rule is backfilled to the owner map or frontend tests README.
