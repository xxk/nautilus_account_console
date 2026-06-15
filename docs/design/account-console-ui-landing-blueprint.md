# Account Console UI Landing Blueprint / UI 落地防跑偏蓝图

- Date: 2026-06-14
- Project: `nautilus_account_console`
- Status: active landing design guardrail
- Scope: product-level UI landing rules for implementation proposals, AI-assisted frontend work and closeout review
- Anchors:
  - [Capability UI design](./account-console-capability-ui-design.md)
  - [UI implementation design](./account-console-ui-implementation-design.md)
  - [UI anti-drift acceptance](../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
  - [UI route coverage matrix](../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)

## 1. Product North Star / 产品北极星

Account Console is a read-only operational account observability workspace.

It must feel like an operations console for account evidence, not like:

1. a trading terminal,
2. a broker control panel,
3. a PM approval tool,
4. a landing page,
5. a raw artifact browser,
6. a generic admin dashboard.

The first product question is always:

```text
What account state is observable, what evidence proves it, and what blocker prevents trust?
```

Every screen must keep three things visible or one click away:

1. the business context,
2. the read-model or event projection,
3. the source ref, checksum, cursor, blocker or typed missing-evidence reason.

## 2. First Viewport Contract / 首屏合同

The first viewport of every primary workbench must show the working surface immediately.

| Area | Required landing behavior | Must not land as |
| --- | --- | --- |
| Top context bar | environment label, trading day, session id, reducer checkpoint, stream state | marketing hero, product slogan or empty header |
| Primary navigation | exactly the seven business workbenches | flat 26-route directory |
| Main content | first accepted panel for the workbench | placeholder card grid or raw fixture list |
| State summary | compact metrics and blocker/stale/partial counts | readiness, approval or tradability banner |
| Detail/evidence access | drawer, split panel or row action with copyable refs | raw payload as the default body |

Primary workbench first panels:

| Workbench | First viewport must prioritize |
| --- | --- |
| Daily Closeout | account closeout blockers, settlement/equity continuity and evidence refs |
| Intraday Monitor | exception queue, active accounts/orders/fills, stale streams and lag |
| Account Workbench | selected account context, summary metrics, tabs and source refs |
| Allocation Admin | account registry projection, lifecycle state and request boundary |
| Risk And Reconcile | risk/reconcile gaps, severity, owner and source refs |
| Evidence Explorer | evidence package index, checksums, schema and owner lineage |
| Stream Ops | ingest/reducer/SSE lag, cursor replay, backpressure and benchmark refs |

## 3. Navigation Guardrails / 导航护栏

Navigation must preserve the business workbench model.

| Rule | Required behavior |
| --- | --- |
| Primary entries | show only Daily Closeout, Intraday Monitor, Account Workbench, Allocation Admin, Risk And Reconcile, Evidence Explorer and Stream Ops |
| Secondary routes | render as tabs, drawers, nested panels or deep links under a parent workbench |
| Direct deep links | restore breadcrumb, parent workbench context, account/session context and source refs |
| Route promotion | requires proposal-level design, acceptance and route coverage update before implementation |
| Technical views | stay behind evidence/debug drawers unless promoted by explicit design |

Do not let a URL map turn into the product IA. The route map is a capability inventory; the sidebar is an operator workflow.

## 4. Panel Landing Shape / 面板落地形态

Every panel implementation must freeze this structure before code:

```text
Panel identity
  route, workbench, panel id, owner users

Source contract
  read model, normalized event, fixture states, source refs

Viewport composition
  header, controls, summary, primary body, drawer/sheet

State matrix
  happy_path, empty, blocked, stale, partial

Interaction list
  allowed display-only actions and forbidden mutations

Evidence behavior
  visible refs, lazy raw payload, copy/checksum behavior

Closeout plan
  browser routes, viewport sizes, screenshot paths, blocker handling
```

If any item is unknown, the proposal remains design-gate blocked instead of inventing UI behavior during implementation.

## 5. Visual Density And Layout / 视觉密度与布局

Account Console should be calm, dense and scannable.

| Element | Required design |
| --- | --- |
| Shell | restrained app shell with sidebar, top context and workbench area |
| Tables | sticky headers, sortable/filterable columns where useful, bounded height or pagination |
| Metric strips | compact, right-aligned numeric values, stable widths |
| Drawers | read-only detail, evidence, blocker or repair context |
| Tabs | switch related secondary panels without losing parent context |
| Badges | short status labels with color as secondary signal |
| Refs/checksums | monospace, truncation, copy control and full value in tooltip/drawer |
| Mobile | stacked records, compact context header and full-screen drawer sheet |

Avoid:

1. hero sections,
2. decorative dashboards,
3. nested cards,
4. oversized metric cards,
5. route-directory home pages,
6. color-only health signals,
7. unbounded raw payload or event DOM rendering.

## 6. Copy And State Vocabulary / 文案与状态词汇

Allowed display state labels:

```text
healthy
blocked
stale
partial
empty
warning
complete
missing evidence
source unavailable
```

Allowed operator verbs:

```text
filter
sort
select
open
copy
inspect
compare
replay display
pause display
resume display
```

Forbidden visible claims, fixture labels and projection labels:

```text
Paper ready
Live ready
admitted
production ready
capital allocated
can trade
tradable
approved for trading
broker ready
```

Any future wording that implies runtime, broker, admission, PM approval, capital or trading readiness must fail anti-drift review unless an owner-approved artifact explicitly defines it as read-only evidence wording.

## 7. Truth Boundary In The UI / UI 真值边界

The UI can display only these categories as first-class state:

| Display category | Valid source |
| --- | --- |
| account state | normalized events, reduced read models or typed account snapshots |
| order state | official order events and reduced order projections |
| fill state | normalized fill events and linked order/account deltas |
| position state | position read models with carryover and settlement refs |
| settlement/equity | ledger-derived projections and settlement artifacts |
| stream state | ingest/reducer/SSE health, cursor and benchmark evidence |
| blockers | typed blocker, incident or missing-evidence records |
| raw payload | drill-down provenance only, lazy-loaded by ref/checksum |

The UI must not compute or write account truth, order truth, fill truth, position truth, settlement truth, equity truth, broker truth, runtime truth, approval truth or capital truth.

## 8. Implementation Start Gate / 开工前设计门

Before frontend code starts, each UI proposal must answer:

| Question | Required answer |
| --- | --- |
| Which parent workbench owns this UI? | one of the seven primary workbenches |
| Which route tier is touched? | primary, account drill-down, management drill-down, portfolio review or ops drill-down |
| Which contract or fixture drives it? | path and state coverage |
| Which state matrix is implemented? | happy, empty, blocked, stale/partial |
| Which source refs are visible? | refs/checksums/cursors/blockers |
| Which interactions are allowed? | display-only list |
| Which interactions are forbidden? | mutation/readiness/action list |
| Which test ids are stable? | panel, row, state, drawer, evidence refs |
| Which closeout screenshots are required? | route and viewport list |

Missing answers are blockers. They should not be patched over by UI placeholders.

## 9. Closeout Review Gate / 收口复核门

Closeout review must open the implemented UI after the final code change and check:

1. first viewport shows the workbench surface, not a landing page or route directory,
2. primary navigation has only seven workbench entries,
3. touched secondary routes preserve parent context,
4. every displayed account/order/fill/position/settlement/equity/risk state has source refs or typed blockers,
5. missing evidence is visible as blocked, partial or stale,
6. forbidden claims and forbidden actions are absent,
7. desktop, tablet and mobile layouts have no overlapping text,
8. browser evidence paths, viewport sizes and blocker status are recorded.

Static tests, route definitions, old screenshots and terminal output cannot close a UI slice by themselves.
