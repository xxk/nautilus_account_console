# P021 Account Console Owner/Fork Governance Phase Plan / 分阶段推进计划

- Proposal ID: `p021-account-console-owner-fork-governance`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-23
- Linked proposal: [README.md](README.md)
- Linked acceptance: [acceptance.md](acceptance.md)
- Issue ledger: [issue-list.md](issue-list.md)

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - docs/ownership/
    - docs/proposals/p021-account-console-owner-fork-governance/
    - backend/src/nautilus_account_console/
    - backend/tests/
    - frontend/src/
    - frontend/tests/
    - scripts/
  allowed_evidence_roots:
    - docs/proposals/p021-account-console-owner-fork-governance/
    - docs/acceptance/
  source_issue_lists:
    - docs/proposals/p021-account-console-owner-fork-governance/issue-list.md
  source_input_templates: []
  source_contract_templates:
    - docs/ownership/account-console-owner-map.md
    - frontend/tests/README.md
```

Boundary rules:

1. `output/account_capability/**/source-package.json` may be referenced as source evidence, but this proposal must not turn `output/` into Account Console-owned truth.
2. Playwright mocked projections are guard evidence only and cannot become formal source-package evidence.
3. Screenshots and browser traces prove display behavior only.
4. Owner-map and route-context changes must preserve read-only projection boundaries.

## AI Tracking Status

<!-- AI-PHASE-STATUS-BEGIN
reviewed_at: 2026-06-20
reviewer: codex
overall_status: implementation_gate_passed
phases:
  - id: phase_0_proposal_convergence
    status: completed
    ai_progress: 100
    evidence: "P021 README, phase-plan, acceptance and issue-list created; proposal docs gate mapped"
  - id: phase_1_route_context_owner_convergence
    status: completed
    ai_progress: 100
    evidence: "backend/src/nautilus_account_console/route_context.py canonical owner plus backend tests"
  - id: phase_2_source_package_provider_boundary
    status: accepted_with_guardrails
    ai_progress: 100
    evidence: "source refs/checksums preserved; output source packages documented as not Account Console-owned truth"
  - id: phase_3_synthetic_test_boundary
    status: completed
    ai_progress: 100
    evidence: "synthetic projection truth flags false and validator guard added"
  - id: phase_4_frontend_registry_governance
    status: accepted_with_guardrails
    ai_progress: 100
    evidence: "frontend tests README rule and P021 validator reject second test route registries; extracted owner modules now hold registry, routing, fixture selection, adapters and terminal rendering"
  - id: phase_5_closeout
    status: completed
    ai_progress: 100
    evidence: "frontend command-status synthesis retired; receipt UI separated from canonical mirror-owned command status"
  - id: phase_6_backend_command_plane_owner_convergence
    status: accepted_with_guardrails
    ai_progress: 100
    evidence: "command_actions.py owns action intake; canonical command-plane projection route declares mirror owner; retirement slicing, archive-only inventory and validators/docs are aligned"
AI-PHASE-STATUS-END -->

## Phase Status Board / Phase 状态表

| Phase | Goal | Current status | AI Progress | Evidence / Current facts | Next action |
| --- | --- | --- | ---: | --- | --- |
| Phase 0 Proposal convergence | Open governance proposal and issue ledger | `completed` | 100% | P021 docs created and gate mapped | Maintain proposal docs gate |
| Phase 1 Route-context owner convergence | Replace duplicated fallback route-context logic with one canonical resolver or one canonical owner path | `completed` | 100% | canonical `route_context.py`; source_bridge/account_mirror delegate | Preserve compatibility wrapper only |
| Phase 2 Source-package provider boundary | Make real source package loading owner-explicit and not hard-coded as Account Console truth | `accepted_with_guardrails` | 100% | source refs/checksums preserved; issue ledger rejects Account Console truth ownership | Keep external owner evidence boundary |
| Phase 3 Synthetic-test boundary | Prevent synthetic-ready e2e mocks from becoming a second projector or formal evidence | `completed` | 100% | synthetic test asserts no account/capital/broker/runtime truth | Keep display-contract-only evidence |
| Phase 4 Frontend registry governance | Keep one canonical route/fixture registry while reducing `App.tsx` growth risk | `accepted_with_guardrails` | 100% | README rule plus validator guard for test route registries; `app-registry.ts`, `account-workbench-routing.ts`, `fixture-selection.ts`, `account-workbench-adapters.ts` and `account-workbench-terminal.tsx` now hold extracted owners | Preserve owner map and anti-fork validator as the retirement guard |
| Phase 5 Frontend command-status owner convergence | Retire frontend-local command-status synthesis and keep transient receipts non-canonical | `completed` | 100% | `command_status` reads only mirror projection; receipt panel shows transient intent API result separately | Preserve receipt vs canonical status split |
| Phase 6 Backend command-plane owner convergence | Make backend action intake and canonical command projection explicit while marking legacy reads non-canonical | `accepted_with_guardrails` | 100% | `command_actions.py` owns actions; `/api/commands/accounts/{account_id}/projection` declares mirror as canonical owner; legacy read retirement slicing and archive-only inventory are governed | Preserve validator-backed guardrails against owner drift |

## Phase 0: Proposal Convergence

### Goal

Record all discovered owner/fork/second-implementation risks in a proposal-bound issue ledger and acceptance matrix.

### Dependencies

1. Local architecture review findings from 2026-06-20.
2. Existing owner map and owner-boundary validation gate.

### Deliverables

1. `docs/proposals/p021-account-console-owner-fork-governance/README.md`
2. `docs/proposals/p021-account-console-owner-fork-governance/phase-plan.md`
3. `docs/proposals/p021-account-console-owner-fork-governance/acceptance.md`
4. `docs/proposals/p021-account-console-owner-fork-governance/issue-list.md`

### Exit Conditions

1. All six discovered issues are listed in `issue-list.md`.
2. Each issue maps to a phase and at least one acceptance row.
3. Proposal docs gate passes for P021.

### Fail-fast / Negative Cases

1. A discovered risk remains only in chat and is not in `issue-list.md`.
2. Proposal claims governance closeout before implementation phases run.

### Verification

```powershell
python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance
```

## Phase 1: Route-Context Owner Convergence

### Goal

Converge route-context fallback and validation into one canonical owner path so backend code cannot grow two route/account-context rule sets.

### Dependencies

1. `backend/src/nautilus_account_console/source_bridge.py`
2. `backend/src/nautilus_account_console/account_mirror.py`
3. `backend/tests/`

### Deliverables

1. A single canonical route-context resolver or explicitly documented canonical ownership.
2. Focused tests proving valid route contexts still project.
3. Negative tests proving missing/underconstrained route context fails.

### Exit Conditions

1. P021-I1 is marked `closed` in `issue-list.md`.
2. No duplicate fallback route-context business rules remain without an explicit delegation comment.
3. Backend tests pass.

### Fail-fast / Negative Cases

1. `source_bridge.py` and `account_mirror.py` both keep independent fallback rules for the same account classes.
2. Route-context fallback can silently mint readiness, broker truth, account truth or command authority.

### Verification

```powershell
python -m pytest backend\tests
python scripts\validate_owner_boundaries.py
```

## Phase 2: Source-Package Provider Boundary

### Goal

Make real source package loading owner-explicit and keep Account Console from appearing to own `output/account_capability/**` truth.

### Dependencies

1. `backend/src/nautilus_account_console/source_bridge.py`
2. `backend/src/nautilus_account_console/ctp19053_consistency.py`
3. `backend/src/nautilus_account_console/ctp025292_consistency.py`
4. Owner refs from external source repositories when available.

### Deliverables

1. A source-package provider/ref boundary or config object.
2. Tests that missing owner evidence produces typed blockers instead of local substitute truth.
3. Documentation update in owner map or proposal evidence.

### Exit Conditions

1. P021-I2 is marked `closed` or `blocked_external_owner` with exact retry condition.
2. Hard-coded output paths no longer imply Account Console source ownership.
3. No raw secret or runtime material is copied into this worktree.

### Fail-fast / Negative Cases

1. Account Console regenerates source-owner package contents as a substitute for owner evidence.
2. A local `output/` package is accepted without owner, source_ref and checksum.
3. Raw CTP/IB password, auth code, raw front address or broker secret is stored in docs/tests/evidence/chat.

### Verification

```powershell
python -m pytest backend\tests
python scripts\validate_owner_boundaries.py
```

## Phase 3: Synthetic-Test Boundary

### Goal

Harden synthetic-ready browser tests so they remain display contract guards and cannot become a second Account Mirror implementation.

### Dependencies

1. `frontend/tests/e2e/p019-ib-tws-synthetic-ready-projection.spec.ts`
2. `frontend/tests/README.md`
3. `frontend/playwright.config.ts`

### Deliverables

1. Test naming and payload authority clearly says synthetic/display-only.
2. Mock payload boundaries do not claim account/capital truth.
3. Negative assertions reject command controls, readiness wording and formal source evidence claims.

### Exit Conditions

1. P021-I3 is marked `closed`.
2. Synthetic test cannot be cited as real U3028269 funds/positions truth.
3. Playwright e2e still verifies canonical UI projection behavior.

### Fail-fast / Negative Cases

1. Test mock contains `capital_truth: true`, `account_truth: true` or equivalent authority claim.
2. Test route interception becomes the only pass evidence for real-account acceptance.
3. Test creates a feature-specific UI route rather than using the canonical account route.

### Verification

```powershell
cd frontend
npm run test:e2e -- p019-ib-tws-synthetic-ready-projection.spec.ts
```

## Phase 4: Frontend Registry Governance

### Goal

Keep a single canonical frontend route/fixture registry while reducing the risk that `App.tsx` turns into multiple implicit registries.

### Dependencies

1. `frontend/src/App.tsx`
2. `frontend/src/app-registry.ts`
3. `frontend/src/account-workbench-routing.ts`
4. `frontend/src/fixture-selection.ts`
5. `frontend/src/account-workbench-adapters.ts`
6. `frontend/src/account-workbench-terminal.tsx`
7. `frontend/src/types.ts`
8. `frontend/tests/README.md`
9. Account Workbench e2e tests.

### Deliverables

1. A documented or extracted canonical registry owner.
2. Tests or source review guard rejecting feature-specific second route registries.
3. No production code imports from `frontend/tests`.
4. `App.tsx` consumes registry state from a canonical frontend registry module instead of owning large ad hoc registry constants.
5. `App.tsx` consumes account workbench route classification, fixture selection, read-model adaptation and terminal rendering from dedicated owner modules instead of owning those implementations directly.

### Exit Conditions

1. P021-I4 is marked `closed` or `accepted_with_guardrails`.
2. New panels have one route/fixture registration path.
3. Existing e2e tests continue to exercise canonical routes.
4. `App.tsx` acts as a composition root and no longer remains a second owner for account workbench route parsing, fixture selection or mirror read-model adaptation.

### Fail-fast / Negative Cases

1. A top-level feature route duplicates an Account Workbench panel route.
2. A test file creates production-like route registration or feature UI implementation.
3. Production code imports from `frontend/tests`.

### Verification

```powershell
python scripts\validate_owner_boundaries.py
cd frontend
npm run build
```

## Phase 5: Frontend Command-Status Owner Convergence

### Goal

Retire frontend-local command-status synthesis so `command_status` is rendered only from the mirror-owned projection, while transient command receipts remain explicitly non-canonical.

### Dependencies

1. `frontend/src/App.tsx` composition root
2. `frontend/src/types.ts`
3. P024 command-control browser evidence and E2E coverage

### Deliverables

1. No production helper synthesizes `command_status` from `CommandApiResult` or runtime closeout payloads.
2. UI displays transient submit/cancel acceptance as a separate receipt surface.
3. Anti-fork validation rejects reintroduction of frontend-local command-status synthesis.

### Exit Conditions

1. P021-I5 is marked `closed`.
2. `Command Status` reads only `mirrorReadback.selected.command_status`.
3. Runtime closeout and partial-fill E2E evidence keep receipt state separate from canonical command status.

### Verification

```powershell
python scripts\validate_p021_owner_fork_governance.py
cd frontend
npx playwright test p024-partial-fill-cancel-order-display.spec.ts --project=desktop
npx playwright test p024-runtime-closeout-evidence.spec.ts --project=desktop
```

## Phase 6: Backend Command-Plane Owner Convergence

### Goal

Make backend command action intake and command-plane read projection explicit owners, and publish one canonical command-plane projection contract that points at mirror-owned durable command truth.

### Dependencies

1. `backend/src/nautilus_account_console/command_actions.py`
2. `backend/src/nautilus_account_console/command_api.py`
3. `backend/src/nautilus_account_console/main.py`
4. `backend/src/nautilus_account_console/account_mirror.py`

### Deliverables

1. Action-intake helpers stay isolated in `command_actions.py`.
2. Read projection owner exposes `/api/commands/accounts/{account_id}/projection`.
3. Canonical command-plane projection declares mirror as durable `command_status` owner and marks legacy read surfaces as non-canonical.
4. Frontend consumes legacy command read surfaces only through one centralized suite loader.
5. Canonical projection classifies each legacy read surface as retain-blocker or retire-with-panel.
6. Each retire-with-panel surface is mapped to the exact frontend panel that must be removed or converged before route retirement.
7. The first safe retirement batch is explicitly named with routes, panels and preconditions before any route deletion begins.
8. Validators and proposal docs reject drift back to mixed ownership.

### Exit Conditions

1. P021-I6 is `closed` or `accepted_with_guardrails` with explicit retirement next step for legacy reads.
2. `main.py` wires action and read owners separately.
3. Backend tests and P021/P024 validators pass.

### Verification

```powershell
python -m pytest backend\tests\test_command_api.py backend\tests\test_source_bridge.py backend\tests\test_mirror_api.py
python scripts\validate_p021_owner_fork_governance.py
python scripts\validate_p024_paper_command_api.py
```

## Phase 7: Closeout

### Goal

Close P021 only after every issue is either fixed with evidence or carried forward as a typed blocker with owner and retry condition.

### Exit Conditions

1. `issue-list.md` has no `open` issue without next action.
2. `acceptance.md` status rows reflect real verification.
3. Owner map is updated if stable governance rules changed.
4. Proposal docs gate and owner boundary gate pass.

### Verification

```powershell
python scripts\check_proposal_docs.py --root . --proposal-id p021-account-console-owner-fork-governance
python scripts\validate_owner_boundaries.py
```
