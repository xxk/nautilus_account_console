# P004 Acceptance / 验收

- Proposal ID: `p004-account-workbench-summary-panel`
- Status: phase8_account_workbench_closeout_passed
- Updated: 2026-06-15
- Inherits:
  - [Account Console capability UI acceptance](../../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
  - [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
  - [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
  - [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
  - [Account Console owner map](../../ownership/account-console-owner-map.md)
  - [Account Console Proposal Workflow Stage Contract](../../workflows/proposal-gates/README.md)
  - [Contract-first UI slice development topic](../../topics/contract-first-ui-slice-development.md)
  - [P004 UI Acceptance](./ui-acceptance.md)
  - [P004 Exception-First Order Observation MVP Acceptance](./order-observation-v1-acceptance.md)

## 1. Positive Acceptance / 正向验收

| ID | Acceptance | Evidence |
| --- | --- | --- |
| P004-POS-01 | Account Workbench routes have proposal-level UI design and UI acceptance before implementation | [ui-design.md](./ui-design.md), [ui-acceptance.md](./ui-acceptance.md) |
| P004-POS-02 | `/accounts/{account_id}` is bound to Account Workbench and Account Summary Panel | [README](./README.md) |
| P004-POS-03 | account source refs and blocker fields are required before displayed values can pass | [ui-acceptance.md](./ui-acceptance.md) |
| P004-POS-04 | route hierarchy keeps account drill-downs under Account Workbench context | [ui-design.md](./ui-design.md), route coverage matrix |
| P004-POS-05 | forbidden actions and forbidden claims are listed before code starts | [README](./README.md), [ui-acceptance.md](./ui-acceptance.md) |
| P004-POS-06 | UI Anti-Drift Acceptance block is completed before implementation | this file |
| P004-POS-07 | account drill-down routes are covered by P004 design gate before implementation | [ui-design.md](./ui-design.md), route coverage matrix |
| P004-POS-08 | proposal is bound to Account Console Proposal Workflow Stage Contract | [README](./README.md), [workflow gate](../../workflows/proposal-gates/README.md) |
| P004-POS-09 | orders, order report provenance, funds/cash, positions, settlement/equity, reconcile/incidents and evidence each have basic domain acceptance before implementation | [ui-acceptance.md](./ui-acceptance.md) |
| P004-POS-10 | Order Observation V1 has exception-first MVP UI acceptance before implementation closeout | [order-observation-v1-acceptance.md](./order-observation-v1-acceptance.md) |
| P004-POS-11 | Account Summary contract and happy/empty/blocked/stale/partial fixtures exist before Account Summary UI implementation | `../../acceptance/2026-06-14-p004-phase1-summary-contract-fixtures.json`, checksum `sha256:0e1cb660e0ccb8309006b1c58ff15d8b230fffc058d6e5fdd400a35ebe97ed73` |
| P004-POS-12 | Account Summary UI renders the accepted fixtures under `/accounts/{account_id}` with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-14-p004-phase2-summary-ui-browser-evidence.json`, checksum `sha256:6ad5b945d88b360e419292674bb0df42000a54ecf084e6c47197b974f1fe26c4` |
| P004-POS-13 | Account Orders and Order Detail contracts plus current/empty/blocked/stale/filled lifecycle fixtures exist before orders UI implementation | `../../acceptance/2026-06-14-p004-phase3-orders-contract-fixtures.json`, checksum `sha256:c494a7ad499bb93898fcd59d36b6277c19e2f24f117e4d2f10150b346d3eb814` |
| P004-POS-14 | Account Orders and Order Detail UI render accepted fixtures with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-14-p004-phase3-orders-ui-browser-evidence.json`, checksum `sha256:26181b95bc374b5390b79407835f6c974d7b8a4ce86767dccc1efc58a4314822` |
| P004-POS-15 | Account Positions contract and current/empty/blocked/stale/partial fixtures exist before positions UI implementation | `../../acceptance/2026-06-14-p004-phase4-positions-contract-fixtures.json`, checksum `sha256:631949614834dbb31b918e381da06c772a5579a8572fd8670c540eb8596b6c91` |
| P004-POS-16 | Account Positions UI renders accepted fixtures with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-14-p004-phase4-positions-ui-browser-evidence.json`, checksum `sha256:10fc038c361f025400bc2b71fde886fdfa0fa6f93c6aebd35f35aae904a413ab` |
| P004-POS-17 | Account Settlement and Account Equity contracts plus current/empty/blocked/stale/partial fixtures exist before settlement/equity UI implementation | `../../acceptance/2026-06-14-p004-phase5-settlement-equity-contract-fixtures.json`, checksum `sha256:f881d2b0dbb0b3496dacf50abb0ae84e2b84f3bfbf4ffcf04f1ac07c6ac41fa1` |
| P004-POS-18 | Account Settlement and Account Equity UI render accepted fixtures with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-14-p004-phase5-settlement-equity-ui-browser-evidence.json`, checksum `sha256:8a53d446b5f38a8c2fb59848f49016d0e73fc248cf489bb114fa6cc20c8bff37` |
| P004-POS-19 | Account Reconcile and Account Incidents contracts plus matched/empty/mismatch/stale/partial and active/empty/blocked/stale/partial fixtures exist before reconcile/incidents UI implementation | `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-contract-fixtures.json`, checksum `sha256:7918fbe64ec607f80809dea53c107fba8f17570e18ab96ad369067a8fc1479e6` |
| P004-POS-20 | Account Reconcile and Account Incidents UI render accepted fixtures with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-ui-browser-evidence.json`, checksum `sha256:0ef92a65a91e12b6c6f70e95a55853c6f9c194cc880bef85f7cd754bfb2a6d54` |
| P004-POS-21 | Account Evidence contract plus current/empty/blocked/stale/partial fixtures exist before evidence UI implementation | `../../acceptance/2026-06-14-p004-phase7-evidence-contract-fixtures.json`, checksum `sha256:f288e3b7c6e1ae5c4412d44e4b660cf3c64053661fab0d084284df10b9c4c481` |
| P004-POS-22 | Account Evidence UI renders accepted fixtures with desktop/tablet/mobile browser evidence and no action controls | `../../acceptance/2026-06-15-p004-phase7-evidence-ui-browser-evidence.json`, checksum `sha256:6d1f754ef2c9e676d44a109ce6cad4e9e54e68063953e5058ecf00a393bfe638` |

## 2. Negative Acceptance / 反向验收

| ID | Must fail if |
| --- | --- |
| P004-NEG-01 | implementation starts without `contracts/ui/panels/account_summary_panel.contract.json` or a typed blocker |
| P004-NEG-02 | UI renders account values not declared in the contract or fixtures |
| P004-NEG-03 | UI displays forbidden readiness, admission, capital or tradability claims |
| P004-NEG-04 | UI exposes direct account lifecycle, funding, broker or order-entry actions |
| P004-NEG-05 | raw reports, latest/debug paths, screenshots, stdout or HTML reports become account truth |
| P004-NEG-06 | account drill-down routes lose Account Workbench parent context |
| P004-NEG-07 | blocked or stale states are hidden behind a generic healthy or empty state |
| P004-NEG-08 | Account Console creates a second source of account, settlement, equity or position truth |
| P004-NEG-09 | Proposal Gate writes or upgrades runtime/account/browser/source closeout truth instead of blocking advancement or recording a typed blocker |
| P004-NEG-10 | order report, funds, positions, settlement/equity, reconcile, incidents or evidence domains claim implementation readiness without contract/fixture/browser evidence or typed blockers |

## 2.1 UI Anti-Drift Acceptance / UI 防跑偏验收

```text
UI Anti-Drift Acceptance:
  proposal_or_change_id: p004-account-workbench-summary-panel
  route_tier: primary_workbench
  primary_workbench: Account Workbench
  route_or_routes_touched:
    - /accounts
    - /accounts/{account_id}
    - /accounts/{account_id}/orders
    - /accounts/{account_id}/orders/{client_order_id}
    - /accounts/{account_id}/positions
    - /accounts/{account_id}/settlement
    - /accounts/{account_id}/equity
    - /accounts/{account_id}/reconcile
    - /accounts/{account_id}/incidents
    - /accounts/{account_id}/evidence
  route_coverage_matrix_rows:
    - /accounts: covered-design-gate P004
    - /accounts/{account_id}: covered-proposal P004 design gate
    - /accounts/{account_id}/orders: covered-design-gate P004
    - /accounts/{account_id}/orders/{client_order_id}: covered-design-gate P004
    - /accounts/{account_id}/positions: covered-design-gate P004
    - /accounts/{account_id}/settlement: covered-design-gate P004
    - /accounts/{account_id}/equity: covered-design-gate P004
    - /accounts/{account_id}/reconcile: covered-design-gate P004
    - /accounts/{account_id}/incidents: covered-design-gate P004
    - /accounts/{account_id}/evidence: covered-design-gate P004
  promoted_to_primary_navigation: no
  promotion_reason: already a primary workbench route
  parent_context_required: Account Workbench context
  breadcrumbs_required:
    - Account Workbench
    - Account Summary
  source_refs_required:
    - account_id
    - account_kind
    - session_id
    - run_id
    - trading_day
    - reducer_checkpoint_id
    - account_snapshot_ref
    - settlement_ref
    - position_carryover_ref
    - blocker_ref
  read_model_contracts:
    - contracts/ui/panels/account_summary_panel.contract.json
    - contracts/ui/panels/account_orders_panel.contract.json
    - contracts/ui/panels/account_order_detail_panel.contract.json
    - contracts/ui/panels/account_positions_panel.contract.json
    - contracts/ui/panels/account_settlement_panel.contract.json
    - contracts/ui/panels/account_equity_panel.contract.json
    - contracts/ui/panels/account_reconcile_panel.contract.json
    - contracts/ui/panels/account_incidents_panel.contract.json
    - contracts/ui/panels/account_evidence_panel.contract.json
  fixture_states:
    - happy_path
    - empty
    - blocked
    - stale
    - partial
  browser_evidence_required: yes
  screenshot_viewports:
    - 1440x900
    - 1024x768
    - 390x844
  closeout_ui_open_required: yes
  closeout_ui_open_evidence: required during implementation closeout
  forbidden_primary_menu_entries:
    - all 26 route-map entries as peer primary pages
  forbidden_actions:
    - broker action
    - runtime mutation
    - order submit/cancel/replace
    - direct account lifecycle mutation
    - direct funding/allocation mutation
  forbidden_claims:
    - Paper readiness
    - Live readiness
    - admission approval
    - PM approval
    - real capital allocation
    - account tradability
  positive_acceptance_ids:
    - UI-WB-03
    - UI-OBS-02
    - UI-ROUTE-01
    - UI-DRIFT-NAV-01
    - UI-DRIFT-EVD-01
  negative_acceptance_ids:
    - UI-DRIFT-CLAIM-01
    - UI-DRIFT-CLAIM-02
    - UI-DRIFT-ACT-01
    - UI-DRIFT-ACT-02
    - ASI-02
    - ASI-05
  blocker_conditions:
    - browser evidence unavailable
    - account summary contract unavailable
    - fixture state unavailable
    - source refs unavailable
```

## 3. Replay And Conservation Acceptance / 回放与守恒验收

| ID | Acceptance |
| --- | --- |
| P004-REP-01 | the same fixture renders the same account summary state across repeated frontend test runs |
| P004-REP-02 | account, settlement and equity values are displayed as read-model projections, not recomputed browser truth |
| P004-CONS-01 | summary health, blocker count and source ref availability match fixture totals |
| P004-CONS-02 | missing settlement, carryover or snapshot references render as blocked or partial |

## 3.0 Basic Domain Acceptance Ledger / 基础业务域验收账本

| Domain | Status | Required before implementation closeout |
| --- | --- | --- |
| Orders current view | design_gate_ready | order contract, current-order fixtures, official event refs, stale/gap states and route screenshot or typed blocker |
| Order lifecycle detail | design_gate_ready | order-detail contract, official event sequence, cursor/checksum refs and route screenshot or typed blocker |
| Order report provenance | design_gate_ready | report provenance refs linked to normalized events; raw payload is debug/evidence only |
| Funds / cash summary | design_gate_ready | cash/frozen/margin/buying-power/fees/taxes fields with settlement/source refs; no funding mutation or capital approval claim |
| Positions | design_gate_ready | position contract, carryover refs, settlement refs, zero-vs-missing distinction and route screenshot or typed blocker |
| Settlement | design_gate_ready | settlement artifact refs, blocker refs, owner/next action for missing closeout and route screenshot or typed blocker |
| Equity | design_gate_ready | ledger-derived equity refs/checksums and route screenshot or typed blocker; no chart/report-derived truth |
| Reconcile | design_gate_ready | mismatch/tolerance/severity/owner/next-action refs and route screenshot or typed blocker |
| Incidents | design_gate_ready | incident category/severity/source/owner/repair refs and route screenshot or typed blocker |
| Evidence package | design_gate_ready | schema/checksum/run/session/trading-day/source lineage refs and route screenshot or typed blocker |

These rows are not implementation evidence. They prevent future implementation from skipping source refs, typed blockers, browser evidence or owner boundaries.

## 3.1 Phase Acceptance Ledger / Phase 验收账本

| Phase | Status | Required before phase closeout |
| --- | --- | --- |
| Phase 1 Summary contract/fixtures | completed | summary contract, fixture states, source refs and blocker states; evidence `../../acceptance/2026-06-14-p004-phase1-summary-contract-fixtures.json`, checksum `sha256:0e1cb660e0ccb8309006b1c58ff15d8b230fffc058d6e5fdd400a35ebe97ed73` |
| Phase 2 Summary UI | completed | UI implementation, selectors, browser screenshots and forbidden scan; evidence `../../acceptance/2026-06-14-p004-phase2-summary-ui-browser-evidence.json`, checksum `sha256:6ad5b945d88b360e419292674bb0df42000a54ecf084e6c47197b974f1fe26c4` |
| Phase 3 Orders lifecycle | completed | order contracts, official event lineage fixtures, read-only orders UI and browser evidence accepted |
| Phase 4 Positions | completed | position contract, carryover/settlement refs, typed blocker fixture states, read-only UI and browser evidence accepted |
| Phase 5 Settlement/equity | completed | settlement/equity contracts, ledger-derived fixture refs, read-only UI and browser evidence accepted |
| Phase 6 Reconcile/incidents | completed | mismatch/incident contracts, owner/next action fixture refs, read-only UI and browser evidence accepted |
| Phase 7 Evidence | completed | evidence contract, schema/checksum/source lineage fixture refs, read-only UI and browser evidence accepted |
| Phase 8 Closeout | completed | local checks, forbidden scan, browser evidence and matrix status update; evidence `../../acceptance/2026-06-15-p004-phase8-account-workbench-closeout.json`, checksum `sha256:fd725adaf513461005d0df172120049d1cc9e68ef39e68e6eadd739bdbff01d0` |

No phase may be marked completed from design text alone. Each phase needs contracts/fixtures and implementation or a typed blocker before implementation closeout. Phase 8 closeout is the required before implementation closeout evidence for the P004 scoped Account Workbench phases only.

## 4. Performance Acceptance / 性能验收

| ID | Acceptance |
| --- | --- |
| P004-PERF-01 | account context switching does not create unbounded DOM growth |
| P004-PERF-02 | metric strip and tab layout remain stable when fixture values change |

## 5. Required Validation Commands / 必跑验证

```powershell
python scripts\check_proposal_docs.py --root . --proposal-id p004-account-workbench-summary-panel
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates contracts\ui
```

Frontend validation, when Node/npm is available:

```powershell
cd frontend
npm run build
npm run test
npm run test:e2e
```

## 6. Blocker Conditions / 阻塞条件

1. No frontend package manager is available for build/test.
2. Read model fields needed by the panel cannot be sourced from current contracts or fixtures.
3. Visual screenshot tooling is unavailable.
4. A requested interaction would mutate runtime/account/broker/admission/capital truth.
5. Account summary source refs are unavailable from external strategy/runtime artifacts and no typed blocker exists.

## 7. Current Closeout Evidence / 当前收口证据

| Check | Result |
| --- | --- |
| Proposal-level UI design | pass: [ui-design.md](./ui-design.md) |
| Proposal-level UI acceptance | pass: [ui-acceptance.md](./ui-acceptance.md) |
| UI anti-drift checklist | pass: present in this file |
| Route coverage matrix update | pass: `/accounts/{account_id}` and implemented drill-down routes through `/accounts/{account_id}/evidence` record scoped P004 implementation/browser evidence and P004 Phase 8 closeout while broader Account Console routes remain proposal-required or deferred |
| Phase-level design map | pass: phase sections added to [phase-plan.md](./phase-plan.md), [ui-design.md](./ui-design.md) and [ui-acceptance.md](./ui-acceptance.md) |
| Phase 1 Summary contract/fixtures | pass: `contracts/ui/panels/account_summary_panel.contract.json` plus five `contracts/ui/fixtures/account_workbench/account_summary_*.json` fixtures; evidence checksum `sha256:0e1cb660e0ccb8309006b1c58ff15d8b230fffc058d6e5fdd400a35ebe97ed73` |
| Phase 2 Summary UI/browser evidence | pass: historical implementation evidence references `frontend/src/App.tsx`, `frontend/src/types.ts`, `frontend/src/styles.css`, `frontend/playwright.config.ts` and `frontend/tests/e2e/account-summary-panel.spec.ts` rendering `/accounts/acct.demo-19053` from accepted fixtures; current owner boundary is governed by P021 canonical frontend owners (`app-registry.ts`, `account-workbench-routing.ts`, `fixture-selection.ts`, `account-workbench-adapters.ts`, `account-workbench-terminal.tsx`) with evidence checksum `sha256:6ad5b945d88b360e419292674bb0df42000a54ecf084e6c47197b974f1fe26c4` |
| Phase 3 Orders contract/fixtures | pass: `contracts/ui/panels/account_orders_panel.contract.json`, `contracts/ui/panels/account_order_detail_panel.contract.json` and six order fixtures are accepted before UI implementation; evidence checksum `sha256:c494a7ad499bb93898fcd59d36b6277c19e2f24f117e4d2f10150b346d3eb814` |
| Phase 3 Orders UI/browser evidence | pass: `/accounts/acct.demo-19053/orders` and `/accounts/acct.demo-19053/orders/p077-e100-rb2610-closeyesterday` render read-only fixtures with browser evidence; evidence checksum `sha256:26181b95bc374b5390b79407835f6c974d7b8a4ce86767dccc1efc58a4314822` |
| Phase 4 Positions contract/fixtures | pass: `contracts/ui/panels/account_positions_panel.contract.json` and five `contracts/ui/fixtures/account_workbench/account_positions_*.json` fixtures are accepted before UI implementation; evidence checksum `sha256:631949614834dbb31b918e381da06c772a5579a8572fd8670c540eb8596b6c91` |
| Phase 4 Positions UI/browser evidence | pass: `/accounts/acct.demo-19053/positions` renders read-only current, blocked, partial and stale positions fixtures with browser evidence; evidence checksum `sha256:10fc038c361f025400bc2b71fde886fdfa0fa6f93c6aebd35f35aae904a413ab` |
| Phase 5 Settlement/equity contract/fixtures | pass: `contracts/ui/panels/account_settlement_panel.contract.json`, `contracts/ui/panels/account_equity_panel.contract.json` and ten `contracts/ui/fixtures/account_workbench/account_settlement_*.json` / `account_equity_*.json` fixtures are accepted before UI implementation; evidence checksum `sha256:f881d2b0dbb0b3496dacf50abb0ae84e2b84f3bfbf4ffcf04f1ac07c6ac41fa1` |
| Phase 5 Settlement/equity UI/browser evidence | pass: `/accounts/acct.demo-19053/settlement` and `/accounts/acct.demo-19053/equity` render read-only current, blocked, partial and stale settlement/equity fixtures with browser evidence; evidence checksum `sha256:8a53d446b5f38a8c2fb59848f49016d0e73fc248cf489bb114fa6cc20c8bff37` |
| Phase 6 Reconcile/incidents contract/fixtures | pass: `contracts/ui/panels/account_reconcile_panel.contract.json`, `contracts/ui/panels/account_incidents_panel.contract.json` and ten `contracts/ui/fixtures/account_workbench/account_reconcile_*.json` / `account_incidents_*.json` fixtures are accepted before UI implementation; evidence checksum `sha256:7918fbe64ec607f80809dea53c107fba8f17570e18ab96ad369067a8fc1479e6` |
| Phase 6 Reconcile/incidents UI/browser evidence | pass: `/accounts/acct.demo-19053/reconcile` and `/accounts/acct.demo-19053/incidents` render read-only mismatch/incident fixtures with desktop/tablet/mobile browser evidence; evidence checksum `sha256:0ef92a65a91e12b6c6f70e95a55853c6f9c194cc880bef85f7cd754bfb2a6d54` |
| Phase 7 Evidence contract/fixtures | pass: `contracts/ui/panels/account_evidence_panel.contract.json` and five `contracts/ui/fixtures/account_workbench/account_evidence_*.json` fixtures are accepted before UI implementation; evidence checksum `sha256:f288e3b7c6e1ae5c4412d44e4b660cf3c64053661fab0d084284df10b9c4c481` |
| Phase 7 Evidence UI/browser evidence | pass: `/accounts/acct.demo-19053/evidence` renders read-only evidence packages with desktop/tablet/mobile browser evidence; evidence checksum `sha256:6d1f754ef2c9e676d44a109ce6cad4e9e54e68063953e5058ecf00a393bfe638` |
| Phase 8 Account Workbench closeout | pass: P004 scoped Account Workbench phases have passing docs, owner-boundary, backend, Rust, frontend and closeout browser checks; evidence checksum `sha256:fd725adaf513461005d0df172120049d1cc9e68ef39e68e6eadd739bdbff01d0` |
| Basic business domain acceptance | pass: orders, order report provenance, funds/cash, positions, settlement/equity, reconcile/incidents and evidence rows added to [ui-acceptance.md](./ui-acceptance.md) and this file |
| Order Observation V1 acceptance | pass: [order-observation-v1-acceptance.md](./order-observation-v1-acceptance.md) defines exception-first MVP UI acceptance |
| Proposal workflow stage contract | pass: P004 references `docs/workflows/proposal-gates/` and keeps Proposal Gate separate from source/runtime/browser truth |
| Implementation/browser evidence | accepted for P004 Phase 2 through Phase 8 scoped Account Workbench closeout only; this does not complete the full Account Console UI or ADR0044/ADR0045 loop |

