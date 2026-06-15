# P004 UI Design: Account Workbench

- Proposal ID: `p004-account-workbench-summary-panel`
- Status: design_gate_ready
- Updated: 2026-06-14
- Parent design: [Account Console UI implementation design](../../design/account-console-ui-implementation-design.md)
- Parent acceptance: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)

## 1. Design Intent / 设计意图

The Account Workbench design gate covers `/accounts/{account_id}` and account drill-down routes.

It answers one operator question:

```text
What is this account's current observable state, what evidence proves it, and which blockers prevent deeper account investigation?
```

The workbench is read-only. It presents account identity, cash/margin/PnL state, latest settlement, blocker state, stream freshness, order lifecycle projections, positions, settlement/equity provenance, reconcile gaps, incidents and evidence refs from typed read models or fixtures. It must not become an order-entry page, broker action page, account lifecycle editor, funding allocator or account truth writer.

## 2. Route And Placement / 路由与位置

| Item | Design |
| --- | --- |
| Route | `/accounts/{account_id}` |
| Workbench | Account Workbench |
| Panel | Account Summary Panel plus account drill-down tabs |
| Default placement | first panel in the Account Workbench |
| Primary users | operations, PM, risk, AI repair reviewer |
| Primary drill-downs | orders, order detail, fills, positions, settlement, equity, reconcile, incidents, evidence |

The first viewport must show account context before raw artifact menus, report payloads or technical route lists.

## 3. Layout / 布局

Desktop layout:

```text
+--------------------------------------------------------------------------------+
| Top context: account id | kind | trading day | session | reducer checkpoint     |
+-------------------+------------------------------------------------------------+
| Account Selector  | Account Summary Metric Strip                               |
| paper.demo-01     | equity | cash | margin | buying power | pnl | lag | health |
| paper.demo-02     +------------------------------------------------------------+
|                   | Tabs: Summary | Positions | Orders | Fills | Settlement    |
|                   +------------------------------------------------------------+
|                   | Summary body: latest settlement, blockers, source refs      |
|                   |                                                            |
|                   |                                      Detail/Evidence Drawer |
+-------------------+------------------------------------------------------------+
```

Mobile layout:

1. Top context becomes a compact stacked header.
2. Account selector collapses into a select control.
3. Metric strip becomes a two-column grid.
4. Account drill-down tabs become a horizontal scroll tab bar.
5. Detail/evidence drawer becomes a full-screen sheet.

## 4. Required UI Components / 必需组件

| Component | Required content | Notes |
| --- | --- | --- |
| Workbench context bar | account id, account kind, portfolio uid, trading day, session id, reducer checkpoint | refs must be copyable |
| Account selector | account id and account kind | switching account changes route context only |
| Metric strip | equity, cash, frozen cash, margin, buying power, realized/unrealized PnL, lag and health | values must be read-model projections |
| Tab list | Summary, Positions, Orders, Fills, Settlement, Equity, Reconcile, Incidents, Evidence | secondary routes preserve parent context |
| Summary body | latest settlement, carryover refs, blocker summary, stream freshness | missing refs render blocked/partial/stale |
| Source ref list | account snapshot, settlement, position carryover, reducer checkpoint, blocker refs | refs/checksums use compact monospace display |
| Detail drawer | selected ref or blocker details | read-only |
| Empty state | account not found or no summary read model | must name missing contract/fixture/source |
| Blocked state | missing settlement, stale reducer, missing carryover or source mismatch | must show owner and next diagnostic ref when available |
| Stale state | stale stream or reducer checkpoint | must show last cursor/checkpoint timestamp |

## 4.1 Drill-Down Panel Design Gates / Drill-Down 面板设计门

| Route | Panel | Required source refs | Must not do |
| --- | --- | --- | --- |
| `/accounts` | Account Overview Selector | account id, account kind, health, settlement state, latest checkpoint | become a raw fixture/debug browser |
| `/accounts/{account_id}/orders` | Orders Current Panel | order refs, latest status, lifecycle event refs, account id | present final order row as lifecycle truth |
| `/accounts/{account_id}/orders/{client_order_id}` | Order Lifecycle Panel | official order events, report provenance refs, cursor/checksum, account id | parse raw report msg as account/order truth |
| `/accounts/{account_id}/positions` | Positions Panel | position refs, carryover refs, settlement refs, account id | infer available/frozen quantity in browser |
| `/accounts/{account_id}/settlement` | Settlement Panel | previous/current settlement refs, blocker refs, trading day | close the day silently without settlement or blocker |
| `/accounts/{account_id}/equity` | Equity Panel | ledger-derived equity refs, settlement refs, source checksum | derive equity from chart/report/HTML/stdout |
| `/accounts/{account_id}/reconcile` | Reconcile Panel | mismatch refs, tolerance refs, owner/next action refs | hide mismatches or treat them as normal color only |
| `/accounts/{account_id}/incidents` | Incidents Panel | incident id, owner, next action, repair refs | reduce incident to log text without owner/action |
| `/accounts/{account_id}/evidence` | Account Evidence Panel | schema refs, source refs, checksums, run/session/trading day refs | treat latest/debug paths as evidence truth |

Each drill-down panel must preserve the same Account Workbench context bar, account id, breadcrumbs and source refs. Deep links may open directly, but they must restore parent context before showing panel content.

## 4.2 Phase Design Map / Phase 设计地图

| P004 Phase | UI surface | Primary proof | Design priority |
| --- | --- | --- | --- |
| Phase 1 | Summary contract and fixtures | account summary source refs and blocker states | contract-first data shape |
| Phase 2 | Account Summary Panel | context bar, metric strip, source refs, blocker drawer | first account workbench viewport |
| Phase 3 | Orders + Order Lifecycle | current order table, lifecycle timeline, report provenance | official order-event lineage |
| Phase 4 | Positions | position table, carryover refs, settlement refs | no browser-inferred availability |
| Phase 5 | Settlement + Equity | settlement state, equity curve refs, blocked closeout | ledger-derived values only |
| Phase 6 | Reconcile + Incidents | mismatch queue, incident queue, owner next action | visible blockers and repair refs |
| Phase 7 | Evidence | schema/checksum/source package browser | evidence drill-down, not truth writer |
| Phase 8 | Workbench closeout | route screenshots, forbidden scan, test evidence | design-gate versus browser-verified separation |

## 4.3 Phase 2 Summary Panel Design / Phase 2 Summary 面板设计

The Summary Panel is the first Account Workbench viewport. It must show account context and evidence health before any technical route list.

Required sections:

| Section | Required content | Empty/blocked behavior |
| --- | --- | --- |
| Context bar | account id, account kind, portfolio uid, trading day, session id, reducer checkpoint | missing account shows empty state and expected source owner |
| Metric strip | equity, cash, frozen cash, margin, buying power, realized/unrealized PnL, lag, health | missing source refs render partial or blocked |
| Evidence summary | account snapshot ref, settlement ref, carryover ref, blocker ref | missing required refs are visible blockers |
| Blocker drawer | blocker id, owner, severity, next diagnostic ref | no silent success state |

## 4.4 Phase 3 Orders And Order Lifecycle Design / Phase 3 订单与生命周期设计

Orders must be displayed as projections from official order events, not as final snapshot truth.

Required sections:

| Section | Required content | Must not do |
| --- | --- | --- |
| Orders current table | client order id, instrument, side, quantity, status, latest event ref, account id | present final row as lifecycle truth |
| Order lifecycle timeline | official event sequence, timestamps, event ids, reconciliation flag | invent project-local order states |
| Report provenance drawer | report refs, checksums, excerpts, normalized event links | parse raw report payload as truth in browser |
| Cursor/status strip | ledger cursor, gap/duplicate state, stale state | hide missing or unreplayable event cursor |

The order detail route must preserve account id and route breadcrumbs. A direct deep link to `/accounts/{account_id}/orders/{client_order_id}` must restore Account Workbench context before showing the timeline.

## 4.5 Phase 4 Positions Design / Phase 4 持仓设计

Positions must be displayed as reduced read-model projections with carryover and settlement lineage.

Required sections:

| Section | Required content | Must not do |
| --- | --- | --- |
| Position table | instrument, side, quantity, available/frozen quantity, average price, market value, PnL | infer availability from quantity in browser |
| Carryover refs | previous settlement ref, position carryover ref, adjustment ref | silently reset missing carryover |
| Position blocker list | missing settlement, stale position, mismatch or unavailable source | hide missing carryover as empty position |

The panel must distinguish zero position from missing position evidence.

## 4.6 Phase 5 Settlement And Equity Design / Phase 5 结算与权益设计

Settlement and equity are account-ledger projections. They must not be generated from UI charts, HTML reports or screenshots.

Required sections:

| Section | Required content | Must not do |
| --- | --- | --- |
| Settlement strip | previous/current trading day, settlement state, opening/closing cash, margin, fees, taxes | mark day closed without settlement or blocker |
| Settlement evidence | previous settlement ref, current settlement ref, source checksum, blocker ref | treat latest/debug path as settlement evidence |
| Equity panel | ledger-derived equity points, daily return, cumulative return, source refs | derive equity from visual chart data |
| Blocked closeout panel | blocker id, owner, next diagnostic ref | hide settlement blocker behind warning color only |

The chart, if added, is a projection of ledger-derived equity points and cannot be the first source of equity truth.

## 4.7 Phase 6 Reconcile And Incidents Design / Phase 6 对账与事件设计

Reconcile and incidents must make broken evidence visible and actionable without becoming repair writers.

Required sections:

| Section | Required content | Must not do |
| --- | --- | --- |
| Reconcile gap table | mismatch id, dimension, expected/actual summary, tolerance ref, severity, owner | hide mismatch as normal color only |
| Incident queue | incident id, category, account id, source ref, owner, next action | reduce incident to log text |
| Repair ref drawer | repair package ref, source refs, blocker refs | mutate repair state from UI |

The UI may copy refs and navigate to evidence, but it must not mark incidents resolved unless a typed request/projection contract exists in a successor change.

## 4.8 Phase 7 Evidence Design / Phase 7 证据设计

Evidence routes are drill-down surfaces for source refs and checksums. They are not a new truth store.

Required sections:

| Section | Required content | Must not do |
| --- | --- | --- |
| Evidence package list | artifact id, schema version, checksum, run id, session id, trading day | use latest/debug path as evidence truth |
| Source lineage view | producer owner, projection owner, source ref, checksum, schema ref | obscure owner boundary |
| Raw payload viewer | lazy-loaded payload by ref/checksum only | embed unbounded raw payloads in main route |
| Missing evidence state | expected artifact, owner, next action | render missing source as empty success |

Raw payload detail must always be attached to a normalized event, read model or evidence package ref.

## 5. Visual Rules / 视觉规则

1. Use dense operational layout: context bar, account selector, metric strip, tabs, summary body and drawer.
2. Do not use a marketing hero, decorative cards or nested cards.
3. Numeric values are right-aligned and stable in width.
4. State badges use short labels: `healthy`, `blocked`, `stale`, `partial`, `empty`, `warning`.
5. Account ids, refs and checksums must not overlap at desktop, tablet or mobile widths.
6. Missing evidence is visible as `blocked`, `partial` or `stale`, not hidden.
7. Raw report payloads are never displayed by default.
8. Route tabs must not become a flat route directory.

## 6. Interactions / 交互

| Interaction | Expected behavior | Must not do |
| --- | --- | --- |
| Switch account | navigates to the selected account context and refreshes read-model projection | mutate account assignment or lifecycle |
| Select tab | keeps Account Workbench context and account id visible | open disconnected route island |
| Open source ref | opens evidence drawer or evidence route with source context | treat raw payload as truth |
| Open blocker | opens read-only blocker detail with owner and next diagnostic ref | mark blocker resolved from UI |
| Copy ref/checksum | copies exact displayed ref/checksum | alter evidence |

## 7. Data Test IDs / 测试钩子

Required stable hooks:

```text
account-workbench-summary-panel
account-workbench-context-bar
account-workbench-account-selector
account-workbench-tab-list
account-summary-metric-strip
account-summary-health-state
account-summary-source-ref
account-summary-blocker
account-summary-empty-state
account-summary-stale-state
account-summary-detail-drawer
account-summary-evidence-drawer
account-orders-panel
account-order-detail-panel
account-positions-panel
account-settlement-panel
account-equity-panel
account-reconcile-panel
account-incidents-panel
account-evidence-panel
```

## 8. State Matrix / 状态矩阵

| State | Trigger | UI requirement |
| --- | --- | --- |
| `happy_path` | account summary has current snapshot, settlement, carryover and checkpoint refs | show summary metrics, source refs and healthy state without readiness claims |
| `empty` | account id is unknown or no summary read model exists | show missing account/read-model message and expected source owner |
| `blocked` | settlement/carryover/source mismatch blocker exists | show blocker count, owner, next diagnostic ref and blocked badge |
| `stale` | reducer checkpoint or stream cursor is stale | show stale badge, last checkpoint/cursor and lag |
| `partial` | some refs exist but settlement/equity/carryover evidence is incomplete | show available values and explicit missing evidence list |

## 9. Forbidden UI Behavior / 禁止行为

The UI must not:

1. Display `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade`.
2. Submit, cancel, replace or modify orders.
3. Call broker actions or runtime mutations.
4. Create, activate, suspend or retire accounts.
5. Mutate funding, allocation, admission, PM approval or capital truth.
6. Compute account equity, settlement, position availability or tradability in the browser.
7. Treat raw report payloads, screenshots, HTML reports, stdout or latest/debug paths as account truth.
8. Render account drill-down routes as disconnected route islands.
9. Promote account drill-down routes into peer primary navigation without a successor proposal.
