# Account Console Capability UI Design / 账户控制台能力级 UI 设计

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: design acceptance baseline
- Scope: ADR-0045 Account Console UI surfaces for ADR-0044 Paper account artifacts and read models

## 1. Design Principle

Nautilus Account Console is a read-only account observability workspace. It can show account state, evidence, provenance, blockers and account-management requests, but it must not write runtime truth, account truth, broker truth, admission truth or capital truth.

The UI is split into four surfaces:

| Surface | Purpose | Truth boundary |
| --- | --- | --- |
| Account Observability | show account, order, fill, position, settlement, equity, reconcile and incident state | reads normalized events, snapshots and typed artifacts |
| Account Management Requests | create/suspend/retire/assign/fund Paper accounts as request/projection UI | request-only; accepted events must come from typed lifecycle/allocation ledgers |
| Portfolio / PM Review | show sleeve attribution, target reconciliation, risk/capacity and daily closeout package | read-only derived portfolio views |
| HFT / Stream Operations | show lag, cursor replay, durable ledger health and virtualized event streams | observes hot path evidence, does not certify trading readiness |

## 2. Business Workbenches

The primary navigation is business-workflow first. Artifact routes are drill-downs from these workbenches, not the main mental model.

| Workbench | Primary users | Core question | Default UI composition |
| --- | --- | --- | --- |
| Daily Closeout | PM, risk, operations | Can today's Paper accounts close cleanly? | account health summary, settlement state, equity/PnL, blockers, PM daily package links |
| Intraday Monitor | trader, operations | Which account, order or stream needs attention now? | live account grid, exception queue, stream health, active orders/fills summary |
| Account Workbench | strategy owner, researcher, developer | How did this account/order/fill/position state happen? | account detail, positions, orders, fills, settlement, equity, order event tape and report detail |
| Allocation Admin | PM, account admin | Which Paper accounts, assignments and virtual funding events are effective or requested? | account registry, lifecycle timeline, assignment, funding allocation, request queue, replay/diff |
| Risk And Reconcile | risk, operations | Which risk or reconcile gaps block trust? | risk triggers, reconcile gaps, blocked accounts, tolerances and source refs |
| Evidence Explorer | developer, auditor, AI repair | Which refs/checksums/artifacts prove or block the state? | artifact evidence, schema versions, run/session/trading-day refs, incident/repair packages |
| Stream Ops | platform, HFT owner | Are ingest, ledger, replay, backpressure and browser rendering healthy? | lag, cursor replay, backpressure, durable ledger checksum and benchmark evidence |

The first screen should be a control tower view for Daily Closeout / Intraday Monitor, not a flat menu of artifact pages.

## 3. Route Map

The route map is a capability map, not a requirement to build 26 equal top-level pages. Product navigation has seven primary workbench entries; other routes are tabs, drawers, drill-downs or deep links that preserve workbench context.

Primary workbench pages:

| Primary page | Workbench | Business priority |
| --- | --- | --- |
| `/closeout` | Daily Closeout | daily operating control tower |
| `/monitor` | Intraday Monitor | live exception and stream watch |
| `/accounts/{account_id}` | Account Workbench | account/order/fill/position investigation |
| `/management/accounts` | Allocation Admin | account lifecycle, assignment and funding request projection |
| `/risk-reconcile` | Risk And Reconcile | blocker and mismatch triage |
| `/evidence` | Evidence Explorer | source refs, checksums and repair packages |
| `/ops/stream` | Stream Ops | hot path, stream and replay diagnostics |

Secondary routes:

1. May be implemented as tabs, drawers, drill-down routes or deep links.
2. Must remain reachable from a primary workbench context.
3. Must not appear as a flat top-level route menu unless a future proposal explicitly promotes one.
4. Must carry source refs and account/session context when opened directly.

| Route | UI | Required read source |
| --- | --- | --- |
| `/closeout` | Daily Closeout | closeout package, settlement state, blockers and account summaries |
| `/monitor` | Intraday Monitor | account snapshot stream, active orders/fills, incident and stream-health read models |
| `/accounts` | Account Overview | account snapshot index / account registry read model |
| `/accounts/{account_id}` | Account Detail | account snapshot, positions, orders, fills, settlement and incidents |
| `/accounts/{account_id}/orders` | Orders View | current/final order derived view plus order event refs |
| `/accounts/{account_id}/orders/{client_order_id}` | Order Event Tape and Report Detail | `paper_order_events`, report provenance and fill refs |
| `/accounts/{account_id}/positions` | Positions View | positions and carryover read model |
| `/accounts/{account_id}/settlement` | Settlement View | daily settlement and carryover refs |
| `/accounts/{account_id}/equity` | Equity Curve View | ledger-derived equity curve |
| `/accounts/{account_id}/reconcile` | Reconcile View | reconcile summary and blockers |
| `/accounts/{account_id}/incidents` | Incidents View | incident ledger and repair handoff refs |
| `/accounts/{account_id}/evidence` | Artifact Evidence View | refs, checksums, schema versions and source refs |
| `/management/accounts` | Account Registry | account lifecycle and type registry projections |
| `/management/accounts/requests` | Account Management Requests | pending lifecycle/assignment/funding requests |
| `/management/assignments` | Account Assignment | account assignment ledger projection |
| `/management/funding` | Funding Allocation | virtual allocation ledger projection |
| `/portfolio` | Portfolio Dashboard | portfolio read model |
| `/portfolio/attribution` | Sleeve Attribution | strategy/sleeve attribution artifacts |
| `/portfolio/reconcile` | Target Reconciliation | target vs actual reconciliation artifacts |
| `/portfolio/risk` | Portfolio Risk | exposure/capacity/risk summary |
| `/portfolio/closeout` | PM Daily Closeout | PM closeout package refs |
| `/risk-reconcile` | Risk And Reconcile | risk and reconcile summary |
| `/evidence` | Evidence Explorer | artifact evidence index |
| `/ops/stream` | Stream Health | ingest/reducer/SSE lag and backpressure metrics |
| `/ops/replay` | Cursor Replay | cursor replay and gap/duplicate evidence |
| `/ops/benchmarks` | Performance Benchmarks | typed benchmark artifacts |

## 3.1 Route Tier Acceptance / 路由层级验收

| Tier | Routes | Acceptance rule | Must fail if |
| --- | --- | --- | --- |
| Primary workbench | `/closeout`, `/monitor`, `/accounts/{account_id}`, `/management/accounts`, `/risk-reconcile`, `/evidence`, `/ops/stream` | first-class navigation entries with screenshot/browser acceptance when implemented | route is only reachable through raw artifact/debug navigation |
| Secondary account drill-down | `/accounts`, `/accounts/{account_id}/orders`, `/accounts/{account_id}/orders/{client_order_id}`, `/accounts/{account_id}/positions`, `/accounts/{account_id}/settlement`, `/accounts/{account_id}/equity`, `/accounts/{account_id}/reconcile`, `/accounts/{account_id}/incidents`, `/accounts/{account_id}/evidence` | tabs/drawers/deep links under Account Workbench with preserved account context | route loses account context or becomes disconnected menu island |
| Secondary management drill-down | `/management/accounts/requests`, `/management/assignments`, `/management/funding` | tabs/drawers/deep links under Allocation Admin with request/projection boundary | route mutates accepted lifecycle/allocation truth directly |
| Deferred portfolio surface | `/portfolio`, `/portfolio/attribution`, `/portfolio/reconcile`, `/portfolio/risk`, `/portfolio/closeout` | PM review views after account, settlement, equity and attribution read models exist | route claims readiness, admission, approval or capital truth |
| Secondary ops drill-down | `/ops/replay`, `/ops/benchmarks` | diagnostic panels under Stream Ops | route implies trading readiness or bypasses durable ledger evidence |

## 4. Workbench UI Acceptance Shape

| Workbench | Required first-panel content | Required drill-downs | Must not do |
| --- | --- | --- | --- |
| Daily Closeout | accounts needing closeout, unclosed settlement, equity/PnL, blockers, next action | settlement, equity, reconcile, PM closeout, incidents | bury blockers behind account detail only |
| Intraday Monitor | active accounts, active orders/fills, stale streams, lag, incident queue | order tape, report detail, stream ops, account detail | require manual account-by-account inspection to find issues |
| Account Workbench | single account summary, position/order/fill/settlement tabs and selected order event tape | report detail, evidence, reconcile, incidents | make final orders or raw reports the truth |
| Allocation Admin | account registry, lifecycle state, assignment, virtual funding and request queue | lifecycle timeline, funding replay, account type registry | mutate accepted lifecycle/allocation truth directly |
| Risk And Reconcile | risk triggers, mismatches, tolerance, blocker severity and source refs | account detail, artifact evidence, incident package | mark mismatches healthy without typed blocker |
| Evidence Explorer | run/session/trading-day refs, checksums, schema versions and artifact packages | every source artifact and repair package | use latest/debug/stdout/report HTML as evidence truth |
| Stream Ops | ingest/reducer/SSE lag, backpressure, cursor replay and benchmark refs | virtualized tape, benchmark detail, durable ledger checksum | mix HFT pass claims into PM closeout |

## 5. Account Observability UI

| UI | Required content | Required interactions | Must not do |
| --- | --- | --- | --- |
| Account Overview | account id, kind, status, equity, cash, margin, PnL, stream health, settlement state | filter, sort, select account, open detail | show Paper/Live readiness or account tradability |
| Account Detail | cash, frozen cash, margin, buying power, realized/unrealized PnL, fees/taxes, latest settlement, latest blocker | switch tabs, copy refs/checksums | compute account truth in browser |
| Positions View | current qty, available/frozen qty, average price, market value, PnL, previous settlement ref, carryover state | filter by instrument/strategy/sleeve, open source refs | hide missing carryover or settlement blocker |
| Orders View | current/final order derived state, official event status, pending qty, filled qty, report refs | open order event tape, filter by status/instrument/strategy | treat final order row as lifecycle truth |
| Order Event Tape | official `OrderEvent` sequence, event id, timestamps, client/venue order ids, account id, strategy id, reconciliation flag | virtualized scroll, select event, pause visual stream, copy cursor | invent project-local order states |
| Report Detail | `OrderStatusReport` / `FillReport` refs, checksums, normalized links and raw payload on demand | lazy-load by report ref, compare normalized event | parse raw report as account truth |
| Fills View | trade id, last qty/price, commission, liquidity side, linked order event, linked position/account delta | filter by instrument/order/strategy | show fill without order/account lineage |
| Settlement View | previous/current settlement refs, settlement state, carryover, market value, fees/taxes, blocked reason | compare days, open blockers | let a day close silently without settlement or blocker |
| Equity Curve View | ledger-derived daily points, drawdown, daily return, source refs | range select, inspect point refs | derive curve from chart/report/HTML |
| Reconcile View | order/fill/position/account/settlement mismatches, tolerances, blockers | drill into source artifacts | mark mismatch normal without typed blocker |
| Incidents View | outage, stale order, reconcile gap, writer failure, owner, next action, repair refs | filter by severity/status, open repair package | hide incident behind health color only |
| Artifact Evidence View | run id, session id, trading day, schema version, source refs, checksums, runtime owner | copy evidence package | use latest/debug/stdout as evidence truth |

## 6. Account Management UI

Account management UI is request/projection-only. It must show the state reconstructed from typed lifecycle, assignment and funding ledgers. It may create request objects only when a later approved change defines that request contract.

| UI | Required content | Request actions allowed | Must not do |
| --- | --- | --- | --- |
| Account Registry | `paper_account_id`, lifecycle state, owner, account type, permissions, effective period | request create/activate/suspend/retire/correct | directly append accepted lifecycle ledger events |
| Account Lifecycle Timeline | create, activate, suspend, retire, type/permission updates, overrides and corrections | open request or evidence detail | overwrite historical events |
| Account Type Registry | allowed markets, order permissions, leverage/margin assumptions, netting policy, risk limits, broker-probe shadowing flag | request account type update | treat type as display label only |
| Account Assignment | portfolio/strategy/sleeve scope, effective period, source decision ref, supersedes ref | request assign/reassign/suspend/correct | allow implicit default account |
| Funding Allocation | initial allocation, transfers, injection, withdrawal, risk reserve/release, override/correction | request funding event | imply real PM capital approval |
| Allocation Replay | reconstructed account state, assignments and available virtual capital after replay | choose replay point | depend on manual config or UI state |

## 7. Portfolio / PM UI

| UI | Required content | Must not do |
| --- | --- | --- |
| Portfolio Dashboard | account equity, strategy contribution, open blockers, risk status, unfilled targets | declare Paper ready or Live ready |
| Sleeve Attribution | PnL, fees, slippage, cash drag, hedge effect and drawdown contribution by strategy/sleeve | infer attribution only from final equity |
| Target Reconciliation | strategy target, portfolio target, actual position, pending orders, drift, shortfall, overfill, conflict policy | ignore pending orders or hidden netting |
| Portfolio Risk | exposure, concentration, leverage, margin, drawdown, participation, capacity/liquidity | replace risk artifacts with UI judgment |
| PM Daily Closeout | equity, strategy contribution, blockers, next action, tomorrow carry positions, refs/checksums | write admission/capital truth |

## 8. HFT / Stream UI

| UI | Required content | Must not do |
| --- | --- | --- |
| Live Stream Health | ingest lag, reducer lag, SSE state, backpressure, last cursor, dropped/duplicate/gap counts | imply zero-loss without durable ledger evidence |
| Virtualized Event Tape | bounded visible window, cursor pagination, pause/resume visual updates | render unbounded DOM rows |
| Cursor Replay Panel | replay from cursor, gap/duplicate detection, checksum comparison | use replay result as trading readiness |
| Performance Benchmarks | `steady_1k_eps_5min`, `burst_10k_eps_30sec`, durable ledger checksum, browser render evidence | let Python/browser become default per-event hot path without evidence |

## 9. Visual And Interaction Rules

1. First screen must be the account workspace, not a landing page.
2. The sidebar must show the seven primary workbench entries, not all 26 capability routes as peer pages.
3. Use dense, operational layout: sidebar, toolbar, data tables, detail panels, drawers and tabs.
4. Use compact cards only for summary metrics; do not nest UI cards.
5. Use stable dimensions for tapes, tables, metric strips and drawers.
6. Numeric columns must be right-aligned.
7. Missing evidence must be visible as `blocked` or `partial`, not hidden.
8. Report payloads must lazy-load by ref/checksum.
9. Every major row and panel needs stable `data-testid` hooks.
10. Health colors: live green, stale amber, blocked red, partial blue-gray.
11. The UI must not show `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade`.

## 10. Landing Order

| Order | UI slice | Required before acceptance |
| --- | --- | --- |
| 1 | Account Control Tower: Daily Closeout + Intraday Monitor shell | account snapshot, settlement state, blocker and stream-health fixtures |
| 2 | Account Workbench: Account Detail + Orders/Event Tape/Report Detail | official order event/report provenance fixture |
| 3 | Positions, Fills, Settlement and Equity | position/fill lineage plus daily settlement and ledger-derived equity fixtures |
| 4 | Risk And Reconcile + Incident Queue + Evidence Explorer | reconcile, incident and artifact evidence fixtures |
| 5 | Allocation Admin: Registry + Lifecycle Requests | lifecycle ledger/request contract |
| 6 | Funding Allocation + Replay/Diff | assignment/funding ledger/request contract |
| 7 | Portfolio / PM Review | portfolio attribution/reconcile/risk package |
| 8 | Stream Ops and HFT Benchmarks | Rust hot path benchmark and virtualized browser evidence |
