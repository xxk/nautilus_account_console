# Account Console UI Implementation Design / 账户控制台 UI 实现级设计

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: active implementation design baseline
- Scope: global UI implementation rules for Account Console routes, workbenches and panel slices
- Anchors:
  - [ADR-0002 business workbench navigation](../adr/0002-adopt-business-workbench-first-account-console-navigation.md)
  - [ADR-0003 contract-first UI slice development](../adr/0003-adopt-contract-first-ui-slice-development.md)
  - [Contract-first UI slice development topic](../topics/contract-first-ui-slice-development.md)
  - [Capability UI design](./account-console-capability-ui-design.md)
  - [UI landing blueprint](./account-console-ui-landing-blueprint.md)
  - [UI implementation acceptance](../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)

## 1. Product Shape / 产品形态

Account Console is an operational workbench, not a landing page and not a trading terminal.

The UI must start from account work and evidence:

```text
App Shell
  -> Business Workbench
    -> Panel Slice
      -> Read Model Projection
      -> Source Ref / Evidence Drill-down
```

It observes account, order, fill, settlement, equity, risk, reconcile, allocation and stream state. It never owns runtime truth, broker truth, account truth, admission truth, approval truth or capital truth.

## 2. App Shell / 应用壳

| Area | Required design |
| --- | --- |
| Left navigation | Daily Closeout, Intraday Monitor, Account Workbench, Allocation Admin, Risk And Reconcile, Evidence Explorer, Stream Ops |
| Top context bar | trading day, session id, environment label, reducer checkpoint, stream status |
| Main workbench area | dense operational panels, tables, metric strips and drawers |
| Right drawer | detail, evidence, blocker, report provenance and repair package views |
| Footer/status area | optional build/version/schema refs; must not claim readiness or tradability |

Navigation order must match operator priority:

1. Daily Closeout
2. Intraday Monitor
3. Account Workbench
4. Allocation Admin
5. Risk And Reconcile
6. Evidence Explorer
7. Stream Ops

Only these seven entries are primary navigation. The broader route map contains deep links and secondary capabilities; it must not be rendered as a flat 26-item primary menu.

## 3. Workbench Composition / 工作台组合

| Workbench | First accepted panel | Secondary panels | Primary route |
| --- | --- | --- | --- |
| Daily Closeout | Account Health Panel | settlement state, equity continuity, blocker queue, PM package refs | `/closeout` |
| Intraday Monitor | Exception Queue Panel | account stream grid, active orders/fills, stream health | `/monitor` |
| Account Workbench | Account Summary Panel | positions, orders, fills, settlement, equity, order event tape, report detail | `/accounts/{account_id}` |
| Allocation Admin | Account Registry Panel | lifecycle timeline, assignments, funding allocation, replay/diff, request queue | `/management/accounts` |
| Risk And Reconcile | Reconcile Gap Panel | risk triggers, tolerance detail, incident package, source refs | `/risk-reconcile` |
| Evidence Explorer | Evidence Package Panel | schema refs, checksums, run/session/trading-day refs, repair packages | `/evidence` |
| Stream Ops | Stream Health Panel | cursor replay, virtualized event tape, benchmark evidence | `/ops/stream` |

Each panel must be independently contract-backed and fixture-backed.

## 3.1 Route Hierarchy / 路由层级

| Tier | UI role | Routes |
| --- | --- | --- |
| Primary workbench page | top-level navigation and browser acceptance focus | `/closeout`, `/monitor`, `/accounts/{account_id}`, `/management/accounts`, `/risk-reconcile`, `/evidence`, `/ops/stream` |
| Account drill-down | Account Workbench tabs, drawers and deep links | `/accounts`, `/accounts/{account_id}/orders`, `/accounts/{account_id}/orders/{client_order_id}`, `/accounts/{account_id}/positions`, `/accounts/{account_id}/settlement`, `/accounts/{account_id}/equity`, `/accounts/{account_id}/reconcile`, `/accounts/{account_id}/incidents`, `/accounts/{account_id}/evidence` |
| Management drill-down | Allocation Admin tabs, request queues and replay panels | `/management/accounts/requests`, `/management/assignments`, `/management/funding` |
| PM review surface | deferred portfolio review once read models exist | `/portfolio`, `/portfolio/attribution`, `/portfolio/reconcile`, `/portfolio/risk`, `/portfolio/closeout` |
| Ops drill-down | Stream Ops diagnostic panels | `/ops/replay`, `/ops/benchmarks` |

Deep links may be routable, but they must preserve parent workbench context, breadcrumbs and source refs. They should not become independent product entry points unless a future proposal promotes them.

## 4. Panel Anatomy / 面板结构

Every panel should follow this implementation shape:

```text
Panel Header
  - title
  - route/workbench context
  - source checkpoint/ref

Controls
  - filters
  - sort
  - view mode
  - copy refs

State Summary
  - compact metrics
  - health/blocker/stale indicators

Primary Body
  - table, tape, chart or timeline

Detail/Evidence Drawer
  - selected row details
  - refs/checksums/schema/run/session/trading-day
  - blocked/missing evidence explanation
```

Panel implementations must include stable dimensions for metric strips, tables, tapes, drawers, badges and empty states.

## 5. Component Standards / 组件标准

| Component | Required behavior |
| --- | --- |
| Metric strip | compact, right-aligned numeric values, stable width |
| Data table | sortable/filterable where useful, sticky header, bounded height or pagination |
| Event tape | virtualized or bounded visible rows; pause/resume affects display only |
| State badge | short labels only: `healthy`, `blocked`, `stale`, `partial`, `empty`, `warning` |
| Detail drawer | read-only; opens from selected rows or refs |
| Evidence drawer | lazy-loads raw payload by ref only; source refs always visible |
| Request panel | creates request/projection objects only after a typed request contract exists |
| Empty state | names the missing read model, fixture or filter condition |
| Blocked state | shows owner, next diagnostic ref and source evidence when available |
| Stale state | shows last cursor/checkpoint timestamp and source ref |

## 6. Interaction Standards / 交互标准

Allowed interactions:

1. Filter, sort, search and select.
2. Open detail, evidence, incident and repair drawers.
3. Copy refs, checksums, cursor ids and artifact ids.
4. Navigate from workbench context to account/order/evidence drill-down.
5. Pause/resume visual stream rendering without changing source truth.
6. Create request/projection objects only when a typed request contract exists.

Forbidden interactions:

1. Broker action.
2. Runtime mutation.
3. Order submit, cancel, replace or modify.
4. Direct accepted lifecycle or funding ledger mutation.
5. PM approval, admission approval or capital approval.
6. UI-only correction of account, order, fill, position, settlement or equity truth.

## 7. Responsive Design / 响应式设计

Required viewport behavior:

| Viewport | Design requirement |
| --- | --- |
| Desktop 1440 x 900 | sidebar, top context, main panels and right drawer can coexist |
| Tablet 1024 x 768 | sidebar may collapse; drawer overlays without hiding primary state |
| Mobile 390 x 844 | rows become stacked records; drawer becomes full-screen sheet |

Text must not overlap or overflow at any required viewport. Long refs and checksums should truncate with copy support and full value in a tooltip or drawer.

## 8. Data Test ID Convention / 测试钩子约定

Use stable `data-testid` hooks:

```text
{workbench}-{panel}
{workbench}-{panel}-row
{workbench}-{panel}-filter
{workbench}-{panel}-state
{workbench}-{panel}-drawer
{workbench}-{panel}-evidence-ref
```

Examples:

```text
daily-closeout-account-health-panel
daily-closeout-account-health-row
account-workbench-order-event-tape
stream-ops-stream-health-panel
```

## 9. Visual Style / 视觉风格

1. Operational, dense and calm.
2. No hero page, marketing copy or decorative full-page composition.
3. No nested cards.
4. Summary cards are allowed only for compact metrics.
5. Use tabs for panel groups, drawers for details, tables for comparisons and segmented controls for modes.
6. Numeric columns are right-aligned.
7. Color is secondary to labels; state must remain legible without color.
8. Missing evidence must appear as `blocked`, `partial` or `stale`, never as healthy.

## 10. Proposal Design Requirement / Proposal 设计要求

Each UI implementation proposal must include:

```text
ui-design.md:
  route:
  workbench:
  panel:
  users:
  layout:
  required_components:
  interactions:
  state_matrix:
  data_testids:
  visual_rules:
  landing_guardrails:
  forbidden_ui:
  closeout_ui_open_plan:
```

P001 is the reference example:

1. [P001 UI Design](../proposals/p001-daily-closeout-account-health-panel/ui-design.md)
2. [P001 UI Acceptance](../proposals/p001-daily-closeout-account-health-panel/ui-acceptance.md)

## 11. UI Closeout Rule / UI 收口规则

Any UI design or implementation slice must be opened from the actual UI at closeout.

Required closeout behavior:

1. Start the app or deterministic renderer after the final UI code change.
2. Open every implemented or promoted route touched by the slice.
3. Verify the route with the proposal's `ui-acceptance.md` states and required viewports.
4. Record the closeout evidence path, viewport, timestamp and pass/blocker result.
5. Keep UI evidence as display acceptance only; it must not become runtime, account, order, settlement, admission or capital truth.

Closeout must fail if the route was not opened, if evidence comes only from static tests or old screenshots, or if missing browser tooling is not recorded as a typed blocker.
