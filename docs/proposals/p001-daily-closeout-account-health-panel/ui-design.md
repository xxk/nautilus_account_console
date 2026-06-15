# P001 UI Design: Daily Closeout Account Health Panel

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Status: proposed
- Updated: 2026-06-13
- Parent design: [Account Console capability UI design](../../design/account-console-capability-ui-design.md)
- Parent acceptance: [Account Console capability UI acceptance](../../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)

## 1. Design Intent / 设计意图

The Daily Closeout Account Health Panel is the first accepted UI slice for the Account Console.

It answers one operator question:

```text
Which Paper accounts can be closed, which accounts are blocked or stale, and which evidence refs prove the state?
```

The panel is read-only. It presents closeout state, settlement state, equity continuity, blockers and source refs from typed read models and fixtures. It must not become a runtime, broker, admission, capital or order-entry surface.

## 2. Route And Placement / 路由与位置

| Item | Design |
| --- | --- |
| Route | `/closeout` |
| Workbench | Daily Closeout |
| Panel | Account Health Panel |
| Default placement | first panel in the Daily Closeout workbench |
| Primary users | PM, risk, operations, AI repair reviewer |
| Primary drill-downs | account detail, settlement detail, equity detail, evidence refs, blocker/incident refs |

The first viewport should show this panel before raw artifact menus or technical evidence explorers.

## 3. Layout / 布局

Desktop layout:

```text
+-----------------------------------------------------------------------+
| Top bar: trading day | session | filters | source checkpoint          |
+-----------------------------------------------------------------------+
| Metric strip: accounts | closeout blocked | settlement blocked | stale |
+-----------------------------------------------------------------------+
| Account Health Table                         | Detail / Evidence Drawer|
| - account id                                 | selected account         |
| - type / owner                               | blockers                 |
| - closeout state                             | refs/checksums           |
| - settlement state                           | next diagnostic links    |
| - equity continuity                          |                          |
| - blockers                                   |                          |
+-----------------------------------------------------------------------+
```

Mobile layout:

1. Top filters collapse into a compact toolbar.
2. Metric strip becomes a two-column grid.
3. Account rows become stacked operational rows.
4. Detail/evidence drawer becomes a full-screen sheet.

## 4. Required UI Components / 必需组件

| Component | Required content | Notes |
| --- | --- | --- |
| Workbench header | trading day, session id, closeout run id, reducer checkpoint id | refs must be copyable |
| Filter toolbar | account type, closeout state, settlement state, blocker severity | filters must not change source truth |
| Metric strip | total accounts, closeout completed, closeout blocked, settlement blocked, stale/partial | right-aligned numeric values |
| Account health table | account id, account type, owner, closeout state, settlement state, equity continuity, blocker count, source ref | virtualized or bounded rows when data grows |
| State badge | healthy, blocked, stale, partial, empty | no readiness/tradability wording |
| Detail drawer | selected account summary, blockers, source refs, drill-down links | read-only |
| Evidence drawer | artifact id, schema version, checksum, run/session/trading day refs | raw payload lazy-loaded only by ref |
| Empty state | no closeout data or no accounts in filter | must show which fixture/read model is empty |
| Blocked state | settlement/carryover/evidence blocker | must show owner and next diagnostic ref when available |
| Stale state | stale stream or stale reducer checkpoint | must show last cursor/checkpoint timestamp |

## 5. Visual Rules / 视觉规则

1. Use dense operational layout: toolbar, metric strip, table and drawer.
2. Do not use a marketing hero, decorative cards or nested cards.
3. Numeric values are right-aligned.
4. State badges use stable dimensions and short labels: `healthy`, `blocked`, `stale`, `partial`, `empty`.
5. Text must not overlap in desktop, tablet or mobile widths.
6. Missing evidence is visible as `blocked` or `partial`, not hidden.
7. Evidence refs and checksums use monospace display and copy controls.
8. Raw report payloads are never displayed by default.

## 6. Interactions / 交互

| Interaction | Expected behavior | Must not do |
| --- | --- | --- |
| Filter by account type | table and metrics update from fixture/read model projection | mutate account assignment or type |
| Filter by closeout state | table narrows to selected state | call the state ready/tradable |
| Select account row | opens read-only detail drawer | write account state |
| Open evidence ref | opens evidence drawer or navigates to evidence route | treat raw payload as truth |
| Copy ref/checksum | copies exact displayed ref/checksum | alter evidence |
| Open account detail | navigates to account workbench with account context | create broker/runtime action |

## 7. Data Test IDs / 测试钩子

Required stable hooks:

```text
daily-closeout-account-health-panel
daily-closeout-filter-toolbar
daily-closeout-metric-strip
daily-closeout-account-health-row
daily-closeout-closeout-state
daily-closeout-settlement-state
daily-closeout-equity-continuity
daily-closeout-blocker
daily-closeout-evidence-ref
daily-closeout-detail-drawer
daily-closeout-evidence-drawer
daily-closeout-empty-state
daily-closeout-stale-state
```

## 8. State Matrix / 状态矩阵

| State | Trigger | UI requirement |
| --- | --- | --- |
| happy path | all source refs present and closeout state complete | show healthy/complete counts and source refs |
| empty | no accounts or no closeout data for selected filter | show empty message with fixture/read model identity |
| blocked | settlement, carryover, equity or evidence blocker exists | show blocked row, owner/next diagnostic ref and evidence ref |
| stale | stream/checkpoint is older than fixture threshold | show stale banner and last cursor/checkpoint |
| partial | some refs exist but required closeout package is incomplete | show partial badge and missing refs |

## 9. Forbidden UI / 禁止 UI

The panel must not show:

1. `Paper ready`
2. `Live ready`
3. `admitted`
4. `production ready`
5. `capital allocated`
6. `can trade`
7. order submit/cancel/replace controls
8. broker action controls
9. direct lifecycle/funding mutation controls
