# P021 Account Console Owner/Fork Governance / Owner 分叉治理

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: draft
- Created: 2026-06-20
- Updated: 2026-06-20
- Owner: account-console-governance / account-console-architecture
- Source audit: local architecture review on `nautilus_account_console`
- Owner map anchor: [Account Console owner map](../../ownership/account-console-owner-map.md)

## 1. Purpose / 目的

P021 is the governance proposal for owner ambiguity, fork risk and second-implementation risk found during the local architecture review of Account Console.

The proposal does not declare the current implementation broken. It records four concrete risk lanes and turns them into phase-bound governance work with contract-lock expectations:

1. Route-context generation is split between backend modules.
2. Real source-package paths are hard-coded under repo-local `output/`.
3. A synthetic-ready Playwright test constructs a full Account Mirror projection and can look like a second projector.
4. Frontend route and fixture registries are centralized in a large `App.tsx`; this is still a single point today, but it needs guardrails before feature growth creates a fork.

## 2. Scope / 范围

In scope:

1. Record every discovered owner/fork/second-implementation issue in `issue-list.md`.
2. Define phase-by-phase remediation for route-context ownership, source-package provider ownership, synthetic-test boundary and frontend registry governance.
3. Add acceptance rows that prevent these risks from closing through prose-only evidence.
4. Keep the Account Console read-only observation boundary intact.

Out of scope:

1. Accepting broker, runtime, account, order, ledger, admission, approval, capital or trading-readiness truth.
2. Opening direct TWS/CTP sessions from Account Console.
3. Rewriting source packages or owner artifacts that belong to sibling owner repositories.
4. Refactoring the full frontend in this proposal document itself.
5. Weakening protected tests or replacing existing owner-boundary tests.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p021-account-console-owner-fork-governance
  producer_owner: external source owners for broker/runtime/account evidence; account-console-contracts for local contracts
  verifier_owner: account-console-governance
  projection_owner: account-console-backend
  ui_or_report_owner: account-console-frontend and account-console-browser-acceptance-tests
  approval_owner: none
  canonical_contracts:
    - docs/ownership/account-console-owner-map.md
    - frontend/tests/README.md
    - backend/src/nautilus_account_console/source_bridge.py
    - backend/src/nautilus_account_console/account_mirror.py
    - frontend/src/App.tsx
  canonical_source_refs:
    - contracts/source_artifacts/account_sources/
    - contracts/ui/fixtures/account_capability/
    - output/account_capability/*/source-package.json as referenced evidence only, not Account Console-owned truth
  write_authority:
    allowed:
      - proposal governance docs
      - owner-boundary guard tests
      - backend route-context resolver consolidation
      - source-package provider indirection that preserves external owner refs
      - synthetic-test boundary hardening
      - frontend registry documentation and single-owner extraction
    forbidden:
      - Account Console writing runtime/account/broker/admission/capital truth
      - Account Console regenerating external source evidence as substitute owner truth
      - Playwright mocks becoming formal source-package evidence
      - a second route registry, second projector or second source-package schema family
      - test weakening, skip-only replacement or AI self-approval of protected test contracts
  second_implementation_rejected:
    - duplicate backend route_context fallback logic
    - repo-local output path as canonical source owner
    - full mock Account Mirror projector in browser tests
    - feature-specific route branches outside the canonical workbench route registry
```

## 4. Review Verdict / 评审结论

**Current verdict**: `draft`

| Item | Verdict |
| --- | --- |
| Formal proposal needed | yes |
| Requires child changes | yes |
| Allows runtime/account truth changes | no |
| Allows source-owner artifact substitution | no |
| Allows test-only evidence as proposal closeout | no |

## 5. Risk Inventory / 风险清单

| Issue | Summary | Current status | Target phase |
| --- | --- | --- | --- |
| P021-I1 | Backend route-context fallback is duplicated in `source_bridge.py` and `account_mirror.py` | open | Phase 1 |
| P021-I2 | Source-package paths under `output/account_capability/**` are hard-coded into backend modules | open | Phase 2 |
| P021-I3 | Synthetic-ready Playwright test mocks a full ready projection and can become a second projector | open | Phase 3 |
| P021-I4 | Frontend `App.tsx` owns route/fixture/panel registry in one large module; currently single but fragile | open | Phase 4 |

See [issue-list.md](issue-list.md) for per-issue evidence, rejection rules and carry-forward status.

## 6. Document Map / 文档地图

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | proposal scope, owner boundary and risk inventory | present |
| `phase-plan.md` | phased governance and remediation plan | present |
| `acceptance.md` | acceptance and anti-drift matrix | present |
| `issue-list.md` | issue ledger for all discovered owner/fork/second implementation risks | present |

## 7. Graduation / Closeout Matrix

| Graduation item | Policy | Target | Status |
| --- | --- | --- | --- |
| Owner map backfill | required | `docs/ownership/account-console-owner-map.md` | planned |
| Backend route-context resolver convergence | required | `backend/src/nautilus_account_console/` | planned |
| Source package provider boundary | required | backend source package loading path | planned |
| Browser synthetic-test boundary | required | `frontend/tests/e2e/` | planned |
| Frontend registry governance | required | `frontend/src/` and `frontend/tests/README.md` | planned |
| Proposal-local evidence | archive_only | `acceptance.md`, `issue-list.md` | present |
