# P009 Phase Plan / 阶段计划

- Proposal ID: `p009-p077-paper-slice-evidence-panel`
- Status: account_evidence_owner_unified
- Updated: 2026-06-14

## Phase 0: Design Gate / 设计门

- Status: completed
- Goal: confirm proposal-level UI design, UI acceptance, route hierarchy and owner boundary before any P077 evidence package implementation.
- Exit evidence:
  - `README.md` contains Owner Boundary and UI Slice Contract.
  - `ui-design.md` defines layout, states, interactions and Data Test ID hooks.
  - `ui-acceptance.md` defines positive, Negative UI Acceptance, Browser Acceptance and Blocker handling.
  - `acceptance.md` contains UI Anti-Drift Acceptance, `forbidden_actions` and `forbidden_claims`.
  - route coverage matrix maps P009 under Account Workbench order/evidence routes without adding a top-level `/orders/p077-paper-slice` route.

## Phase 1: Route Mapping Repair / 路由映射修复

- Status: completed
- Goal: align the E90 fixture contract route identifier with Account Workbench implementation routing and reject a P077-specific frontend route branch.
- Exit evidence:
  - implementation uses the generic `/accounts/{account_id}/evidence` Account Evidence route.
  - contract route identifier remains an internal fixture identity.
  - no flat top-level route or P077-specific route branch is added.

## Phase 2: UI Implementation / UI 实现

- Status: completed
- Goal: implement a read-only P077 evidence package projection after route mapping is accepted.
- Exit evidence:
  - Account Evidence Panel renders a P077 package whose normalized ref is `p077_paper_slice_panel.v1`.
  - source refs, checksums, owners, boundaries and guarded rejection summaries are visible.
  - no order action controls or readiness claims exist.
  - stable Account Evidence `data-testid` hooks exist.
  - machine-readable evidence: `../../acceptance/2026-06-14-p077-p009-ui-implementation-browser-evidence.json`, checksum `sha256:4fc4cedaa0c6f7bb67ab1e6dca1302ffa51ae9838faff61e7a3eca892ee270ed`.

## Phase 3: Browser Acceptance / 浏览器验收

- Status: completed
- Goal: prove the implemented panel renders correctly in desktop, tablet and mobile viewports.
- Exit evidence:
  - browser screenshots exist under `../../acceptance/browser-evidence/p009-p077-paper-slice-evidence-panel/`.
  - forbidden visible wording/action scan passed.
  - owner boundary validation passed with the E93 validator hook.
  - route matrix still distinguishes Account Workbench route context from the internal fixture route identifier.

## Phase 4: E100/E102 Read-Only Fixture Refresh / 只读 Fixture 刷新

- Status: completed
- Goal: refresh the P077 evidence package fixture from E100/E101/E102 source refs/checksums after the current bounded owner slice closeout.
- Exit evidence:
  - fixture `../../contracts/ui/fixtures/p077_paper_slice/e100_close_yesterday_filled_e102_closeout.json`, checksum `sha256:4c751c917bf63811055cda2de52343731a4f6e22360c923945539d79bcc27cb0`, projects E100 filled/reconciled owner evidence, E101 evidence hygiene audit and E102 no-active-authorization closeout.
  - frontend binding uses the E100/E102 fixture as an Account Evidence package under existing Account Workbench route context; no top-level route, P077-specific route branch or action control is added.
  - machine-readable acceptance evidence `../../acceptance/2026-06-14-p077-e100-e102-readonly-fixture-refresh.json`, checksum `sha256:4387706e6a740f3267091c009ae556a78bab6ca26e721279bc3290fd8479974c`.
  - gates passed: fixture JSON, owner boundary, frontend fixture validation, frontend build, frontend e2e, proposal docs, backend compileall and hotpath Rust tests.
  - no runtime, ledger, broker, admission, capital, readiness, retry authorization, Account Console runtime truth or loop-completion truth is created.

## Phase 5: E105 Status Normalization Read-Only Alignment / 只读状态对齐

- Status: completed
- Goal: bind P077 E105 non-ready/no-active-authorization status to the existing Account Console read-only projection posture without changing frontend behavior.
- Exit evidence:
  - machine-readable acceptance evidence `../../acceptance/2026-06-14-p077-e105-status-normalization-readonly-alignment.json`, checksum `sha256:b6f913a24613e83386f18d7ef2c41d8183adc43fed30a732a9099b415a603450`.
  - E105 is governance/status provenance only; it is not rendered or accepted as runtime truth, UI truth, readiness, retry authorization, action permission or loop completion.
  - no frontend, runtime, ledger, Paper, broker, admission or capital mutation was made.
