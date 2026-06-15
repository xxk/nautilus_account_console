# P001 Phase Plan / 阶段计划

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Status: browser_evidence_verified
- Updated: 2026-06-13

## Phase 0: Design Gate / 设计门

- Status: completed
- Goal: confirm the UI Slice Contract, UI design and UI acceptance before code.
- Exit evidence:
  - read model fields are listed
  - fixtures are named
  - positive and negative acceptance IDs are mapped
  - forbidden actions and forbidden claims are named
  - blockers are named
  - `ui-design.md` exists and defines layout, states, interactions and test hooks
  - `ui-acceptance.md` exists and defines screenshot, selector, negative and browser acceptance

## Phase 1: Read Model Contract / 读模型契约

- Status: completed
- Goal: add `contracts/ui/panels/account_health_panel.contract.json`.
- Exit evidence:
  - contract includes account/session identity, closeout state, settlement state, equity continuity, evidence references and blockers
  - contract does not include runtime mutation, broker action, capital approval or admission action fields

## Phase 2: Fixtures / 夹具

- Status: completed
- Goal: add deterministic Daily Closeout fixture states.
- Exit evidence:
  - happy path fixture
  - empty fixture
  - blocked settlement fixture
  - stale stream fixture
  - fixtures pass schema validation when a local schema validator exists

## Phase 3: UI Slice / UI 切片

- Status: completed
- Goal: implement the Account Health Panel under `/closeout`.
- Exit evidence:
  - panel displays state, blockers and source artifact references
  - panel supports account type and closeout state filtering
  - panel provides drill-down links without mutating runtime or account truth
  - stable `data-testid` hooks exist

## Phase 4: Acceptance Closeout / 验收收口

- Status: completed_with_security_followup
- Goal: prove the slice is verifiable and does not violate account-console boundaries.
- Exit evidence:
  - Python compile check passes
  - Rust tests pass
  - frontend build/test passes or a typed blocker is recorded
  - forbidden wording scan passes
  - visual screenshots for `/closeout` pass or a typed blocker is recorded

Evidence:

- `npm run build`: pass
- `npm run test`: pass
- `npm run test:e2e`: pass for desktop, tablet and mobile
- Browser screenshots: `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/`
- Runner blocker: resolved by `D:\Nautilus\.tools\node-v22.22.3-win-x64`

Security follow-up:

- Closed by [P003 Frontend Dependency Security Follow-up](../p003-frontend-dependency-security-followup/README.md).
