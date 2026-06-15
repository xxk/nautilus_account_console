# P004 Exception-First Order Observation MVP Acceptance / 异常优先订单观察 MVP 验收

- Proposal ID: `p004-account-workbench-summary-panel`
- Phase: Phase 3 Orders and Order Lifecycle
- Status: mvp_acceptance_defined
- Updated: 2026-06-14
- Parent UI design: [P004 UI Design](./ui-design.md)
- Parent UI acceptance: [P004 UI Acceptance](./ui-acceptance.md)
- Static preview: [Account Console order observation preview](../../design/account-console-order-observation-preview.html)
- Preview screenshots, design review only:
  - [desktop](../../design/account-console-order-observation-preview-desktop.png)
  - [tablet](../../design/account-console-order-observation-preview-tablet.png)
  - [mobile](../../design/account-console-order-observation-preview-mobile.png)

## 1. V1 Scope / V1 范围

V1 is a lightweight read-only exception-first Orders surface under Account Workbench.

It accepts only the UI shape shown in the static preview:

1. Global Nautilus Account Console primary navigation with Account Workbench selected.
2. Account Workbench context and Orders tab.
3. Lightweight account observation list for switching account context.
4. Exception-first operational summary for partial, stale and report-gap orders.
5. Current order projection table.
6. Selected order lifecycle list.
7. Minimal evidence refs for report provenance, checksum and schema.

V1 does not accept market quote workflows, order entry, broker action, runtime mutation, account lifecycle management, funding allocation, full contract completeness or all future order-management flows.

## 1.1 Visual Direction / 视觉方向

V1 should visually follow a Nautilus-flavored simplified CTP / cross-period terminal style:

1. compact Account Workbench context bar,
2. exception-first summary strip for active accounts, unfinished orders, stale/lag and report gaps,
3. lightweight account observation list in the left pane,
4. split panes for filter context, current orders, lifecycle and evidence refs,
5. small table typography, tight borders and terminal-style status bar,
6. restrained Nautilus colors for selection, evidence and read-model context.

The left-side area is a read-only account observation and filter/context mirror. It must not become an executable order ticket or account-management panel.

Non-essential terminal elements should be removed in V1. Do not implement market quote tables, full menu systems, top account/equity ledger strips, full quote depth, full shortcut matrices, advanced order forms, strong legacy red selection frames or complete broker-terminal behavior until a later proposal explicitly asks for them.

## 2. Minimum UI Acceptance / 最小 UI 验收

| ID | Must pass |
| --- | --- |
| P004-ORD-V1-UI-01 | The page keeps Account Workbench context visible: account id, trading day, session id and order read-model ref. |
| P004-ORD-V1-UI-02 | The primary navigation still shows only the seven business workbenches; Orders stays under Account Workbench. |
| P004-ORD-V1-UI-03 | The main table shows at least client order id, instrument, side, qty, filled, pending, status and latest event ref. |
| P004-ORD-V1-UI-04 | Selecting an order shows a lifecycle list and report provenance without making raw reports the source of truth. |
| P004-ORD-V1-UI-05 | The drawer shows copyable evidence refs: order event, fill event, checksum/schema and source refs. |
| P004-ORD-V1-UI-06 | The rendered layout follows the MVP preview closely enough that account, summary, order, lifecycle and evidence panes are visible in one dense workbench. |
| P004-ORD-V1-UI-07 | A lightweight account list or account-group context supports multi-account observation without exposing lifecycle, assignment or funding actions. |
| P004-ORD-V1-UI-08 | Partial, stale or report-gap orders appear before matched/completed rows and expose a short handling clue such as `report gap` or `cursor lag`. |
| P004-ORD-V1-UI-09 | The Nautilus primary navigation remains visible in the app shell and highlights Account Workbench. |

## 3. Must Fail / 必须失败

| ID | Must fail if |
| --- | --- |
| P004-ORD-V1-NEG-01 | The UI exposes submit, place, cancel, replace, modify, broker action or runtime mutation controls. |
| P004-ORD-V1-NEG-02 | A current/final order row is presented as lifecycle truth instead of a projection from official events. |
| P004-ORD-V1-NEG-03 | Raw report payload becomes first-screen workflow or browser-parsed order/account truth. |
| P004-ORD-V1-NEG-04 | Missing event/report/evidence refs are hidden behind healthy styling. |
| P004-ORD-V1-NEG-05 | The UI claims readiness, admission, approval, capital allocation or account tradability. |
| P004-ORD-V1-NEG-06 | The multi-account list exposes account create, activate, suspend, assign, fund or allocation actions. |
| P004-ORD-V1-NEG-07 | MVP implementation adds market quote workflows, full terminal menus or advanced order form behavior. |
| P004-ORD-V1-NEG-08 | The order MVP replaces or hides the global Nautilus primary navigation. |

## 4. Minimal Selectors / 最小测试钩子

```text
[data-testid="account-orders-panel"]
[data-testid="account-console-primary-nav"]
[data-testid="account-observation-list"]
[data-testid="account-orders-row"]
[data-testid="account-orders-latest-event-ref"]
[data-testid="account-order-lifecycle-event"]
[data-testid="account-order-report-provenance"]
[data-testid="account-order-evidence-ref"]
```

## 5. Navigation Retention Acceptance / 主导航保留验收

The Order Observation MVP must render inside the normal Nautilus Account Console app shell.

| ID | Must pass |
| --- | --- |
| P004-ORD-V1-NAV-01 | The left primary navigation is visible in the desktop MVP route. |
| P004-ORD-V1-NAV-02 | The primary navigation includes exactly the seven workbenches: Daily Closeout, Intraday Monitor, Account Workbench, Allocation Admin, Risk And Reconcile, Evidence Explorer and Stream Ops. |
| P004-ORD-V1-NAV-03 | Account Workbench is visually active while the Orders MVP is open. |
| P004-ORD-V1-NAV-04 | Orders appears as Account Workbench content, not as a new primary navigation entry. |

Must fail if the MVP replaces the app shell with a standalone terminal, hides the global navigation, or promotes Orders to a peer primary workbench.

## 6. Browser Evidence / 浏览器证据

For V1 closeout, desktop evidence is the only blocking browser requirement.

| Viewport | Size | Required proof |
| --- | --- | --- |
| Desktop | 1440 x 900 | primary navigation, account list, exception summary, order table, lifecycle and evidence refs visible |

Tablet and mobile screenshots may be kept as design previews, but they are not V1 acceptance gates.

V1 explicitly defers:

1. mobile stacked layout acceptance,
2. mobile drawer/sheet behavior,
3. tablet-specific layout tuning,
4. touch ergonomics.

Static preview screenshots are design-review evidence only. Product implementation closeout must reopen the implemented UI after the final code change.

## 7. Lightweight Validation / 轻量验证

```powershell
python scripts\check_proposal_docs.py --root . --proposal-id p004-account-workbench-summary-panel
python scripts\validate_owner_boundaries.py
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|tradable|approved for trading|broker ready|submit order|place order|cancel order|replace order|modify order|broker action" frontend\src contracts\ui
```

## 8. Current State / 当前状态

| Item | Status |
| --- | --- |
| Static visual preview | present; design review only |
| V1 UI acceptance | defined in this document |
| Product implementation | not started |
| Implementation browser evidence | desktop required later; tablet/mobile deferred; preview screenshots do not count |
