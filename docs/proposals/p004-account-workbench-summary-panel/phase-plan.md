# P004 Phase Plan / 阶段计划

- Proposal ID: `p004-account-workbench-summary-panel`
- Status: phase8_account_workbench_closeout_passed
- Updated: 2026-06-14

## Phase 0: Design Gate / 设计门

- Status: completed
- Goal: confirm proposal-level Account Workbench UI design and acceptance before implementation.
- Exit evidence:
  - `ui-design.md` exists and defines layout, states, interactions and stable selectors for summary and account drill-down routes.
  - `ui-acceptance.md` exists and defines positive, negative, browser, selector and blocker acceptance for Account Workbench routes.
  - Owner Boundary block is present in [README](./README.md).
  - UI Anti-Drift Acceptance block is present in [acceptance](./acceptance.md).
  - Route coverage matrix binds `/accounts/{account_id}` to P004 design gate.

## Phase 1: Summary Contract And Fixture Gate / Summary 契约与夹具门

- Status: completed
- Goal: add the Account Summary read model contract and deterministic fixture states.
- Exit evidence:
  - contract includes account identity, session/run/trading day identity, cash, margin, buying power, PnL, fees/taxes, latest settlement, blockers and source refs.
  - contract excludes order-entry, broker action, runtime mutation, admission, approval and capital action fields.
  - happy, empty, blocked, stale and partial fixture states exist.
  - fixture values are read-model projections with source refs or typed blockers.
  - machine-readable acceptance evidence: `../../acceptance/2026-06-14-p004-phase1-summary-contract-fixtures.json`, checksum `sha256:0e1cb660e0ccb8309006b1c58ff15d8b230fffc058d6e5fdd400a35ebe97ed73`.
  - no frontend implementation, browser evidence, Account Console runtime truth, readiness, admission, capital or action truth is created.

## Phase 2: Summary UI Slice / Summary UI Slice

- Status: completed
- Goal: implement the Account Summary Panel under `/accounts/{account_id}`.
- Exit evidence:
  - panel displays account state, blockers and source refs from the contract.
  - panel preserves Account Workbench parent context and tab navigation.
  - panel opens source/blocker detail drawers without mutating truth.
  - stable `data-testid` hooks exist.
  - desktop, tablet and mobile screenshots exist or a typed browser blocker is recorded.
  - machine-readable acceptance evidence: `../../acceptance/2026-06-14-p004-phase2-summary-ui-browser-evidence.json`, checksum `sha256:6ad5b945d88b360e419292674bb0df42000a54ecf084e6c47197b974f1fe26c4`.
  - no runtime, account, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 3: Orders And Order Lifecycle Gate / 订单与订单生命周期门

- Status: completed
- Goal: add contracts, fixtures and UI design closeout for `/accounts/{account_id}/orders` and `/accounts/{account_id}/orders/{client_order_id}`.
- Exit evidence:
  - `account_orders_panel.contract.json` and `account_order_detail_panel.contract.json` exist before implementation.
  - fixtures include current orders, official order event sequence, report provenance, blocked and stale states.
  - orders view links final/current order rows to lifecycle events.
  - order detail view shows official order events and report provenance refs.
  - raw report payloads remain drill-down/debug evidence and never become order/account truth.
  - contract/fixture gate evidence: `../../acceptance/2026-06-14-p004-phase3-orders-contract-fixtures.json`, checksum `sha256:c494a7ad499bb93898fcd59d36b6277c19e2f24f117e4d2f10150b346d3eb814`.
  - browser evidence: `../../acceptance/2026-06-14-p004-phase3-orders-ui-browser-evidence.json`, checksum `sha256:26181b95bc374b5390b79407835f6c974d7b8a4ce86767dccc1efc58a4314822`.
  - no runtime, account, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 4: Positions Gate / 持仓门

- Status: completed
- Goal: add contract, fixtures and UI design closeout for `/accounts/{account_id}/positions`.
- Exit evidence:
  - `account_positions_panel.contract.json` exists before implementation.
  - positions fixture includes current quantity, available/frozen quantity, average price, market value, PnL, carryover refs and settlement refs.
  - UI does not infer availability, carryover or T+1 state in the browser.
  - missing carryover or settlement refs render blocked/partial.
  - contract/fixture gate evidence: `../../acceptance/2026-06-14-p004-phase4-positions-contract-fixtures.json`, checksum `sha256:631949614834dbb31b918e381da06c772a5579a8572fd8670c540eb8596b6c91`.
  - browser evidence exists for implemented route or typed blocker is recorded before UI closeout.
  - browser evidence: `../../acceptance/2026-06-14-p004-phase4-positions-ui-browser-evidence.json`, checksum `sha256:10fc038c361f025400bc2b71fde886fdfa0fa6f93c6aebd35f35aae904a413ab`.
  - no runtime, account, position, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 5: Settlement And Equity Gate / 结算与权益门

- Status: completed
- Goal: add contracts, fixtures and UI design closeout for `/accounts/{account_id}/settlement` and `/accounts/{account_id}/equity`.
- Exit evidence:
  - `account_settlement_panel.contract.json` and `account_equity_panel.contract.json` exist before implementation.
  - settlement fixture includes previous/current settlement refs, settlement state, blocked reason and carryover.
  - equity fixture includes ledger-derived equity points and source refs.
  - UI never derives equity from chart/report/HTML/stdout/browser state.
  - day close cannot appear successful without settlement artifact or typed blocker.
  - contract/fixture gate evidence: `../../acceptance/2026-06-14-p004-phase5-settlement-equity-contract-fixtures.json`, checksum `sha256:f881d2b0dbb0b3496dacf50abb0ae84e2b84f3bfbf4ffcf04f1ac07c6ac41fa1`.
  - browser evidence: `../../acceptance/2026-06-14-p004-phase5-settlement-equity-ui-browser-evidence.json`, checksum `sha256:8a53d446b5f38a8c2fb59848f49016d0e73fc248cf489bb114fa6cc20c8bff37`.
  - no runtime, account, settlement, equity, position, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 6: Reconcile And Incidents Gate / 对账与事件门

- Status: completed
- Goal: add contracts, fixtures and UI design closeout for `/accounts/{account_id}/reconcile` and `/accounts/{account_id}/incidents`.
- Exit evidence:
  - `account_reconcile_panel.contract.json` and `account_incidents_panel.contract.json` exist before implementation.
  - reconcile fixture includes mismatch refs, tolerance refs, severity, owner and next action.
  - incidents fixture includes outage, stale order, reconcile gap, writer failure or source blocker states.
  - UI never hides mismatches as normal styling only.
  - incidents always expose owner, next action and repair refs when available.
  - contract/fixture gate evidence: `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-contract-fixtures.json`, checksum `sha256:7918fbe64ec607f80809dea53c107fba8f17570e18ab96ad369067a8fc1479e6`.
  - UI/browser evidence: `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-ui-browser-evidence.json`, checksum `sha256:0ef92a65a91e12b6c6f70e95a55853c6f9c194cc880bef85f7cd754bfb2a6d54`.
  - no runtime, account, reconcile, incident, settlement, equity, position, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 7: Evidence Gate / 证据门

- Status: completed
- Goal: add contract, fixtures and UI design closeout for `/accounts/{account_id}/evidence`.
- Exit evidence:
  - `account_evidence_panel.contract.json` exists before implementation.
  - evidence fixture includes schema refs, checksums, run/session/trading day refs and source refs.
  - latest/debug paths are never treated as evidence truth.
  - raw payloads load lazily by ref only.
  - contract/fixture gate evidence: `../../acceptance/2026-06-14-p004-phase7-evidence-contract-fixtures.json`, checksum `sha256:f288e3b7c6e1ae5c4412d44e4b660cf3c64053661fab0d084284df10b9c4c481`.
  - UI/browser evidence: `../../acceptance/2026-06-15-p004-phase7-evidence-ui-browser-evidence.json`, checksum `sha256:6d1f754ef2c9e676d44a109ce6cad4e9e54e68063953e5058ecf00a393bfe638`.
  - no runtime, account, evidence, order, ledger, readiness, admission, capital, action or Account Console UI completion truth is created.

## Phase 8: Account Workbench Acceptance Closeout / Account Workbench 验收收口

- Status: completed
- Goal: prove the implemented Account Workbench phases are verifiable and do not violate account-console boundaries.
- Exit evidence:
  - Python compile check passes.
  - owner boundary validation passes.
  - Rust tests pass.
  - frontend build/test/e2e pass or typed blockers are recorded.
  - forbidden wording/action scan passes.
  - desktop, tablet and mobile browser screenshots for `/accounts/{account_id}` are recorded after the final implementation change.
  - implemented secondary account routes have proposal-level screenshots or typed browser/tooling blockers.
  - route coverage matrix still distinguishes design-gate readiness from browser-verified implementation.
  - closeout evidence: `../../acceptance/2026-06-15-p004-phase8-account-workbench-closeout.json`, checksum `sha256:fd725adaf513461005d0df172120049d1cc9e68ef39e68e6eadd739bdbff01d0`.
  - closeout scope is P004 Account Workbench only; no Account Console UI completion, ADR loop completion or runtime/account/ledger truth is created.
