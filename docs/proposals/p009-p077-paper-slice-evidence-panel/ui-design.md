# P009 UI Design: P077 Paper Slice Evidence Panel

- Proposal ID: `p009-p077-paper-slice-evidence-panel`
- Status: readonly_fixture_refresh
- Updated: 2026-06-14
- Parent design: [P004 Account Workbench UI Design](../p004-account-workbench-summary-panel/ui-design.md)
- Parent acceptance: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)

## 1. Design Intent / 设计意图

The P077 Paper Slice Evidence Panel is a read-only Account Workbench drill-down panel for a single bounded Paper slice.

It shows what the CTP owner artifact says, what the P077 governance handoff says, and which boundary flags prevent any readiness, broker, admission, capital or runtime truth claim.

## 2. Route And Placement / 路由与位置

| Item | Design |
| --- | --- |
| Parent workbench | Account Workbench |
| Primary parent route | `/accounts/{account_id}/orders/{client_order_id}` |
| Secondary parent route | `/accounts/{account_id}/evidence` |
| Contract route identifier | `/orders/p077-paper-slice` |
| Panel | P077 Paper Slice Evidence Panel |
| Default placement | order lifecycle/evidence drawer or tab under Account Workbench |

The contract route identifier is not a product route by itself. Implementation must preserve account context and breadcrumbs before rendering the panel.

## 3. Layout / 布局

Desktop layout:

```text
+--------------------------------------------------------------------------------+
| Account Workbench context: account id | trading day | source checksum status    |
+--------------------------------------------------------------------------------+
| Slice summary: instrument | side | offset | qty | lifecycle | reconcile         |
+--------------------------------------------------------------------------------+
| Evidence refs                              | Boundary and rejection rules       |
| - lifecycle source ref/checksum            | - no active authorization          |
| - governance handoff ref/checksum          | - no Paper/Live readiness          |
| - contract/fixture ref/checksum            | - no broker/admission/capital      |
+--------------------------------------------------------------------------------+
| Detail drawer: selected source ref, owner, schema, authority                    |
+--------------------------------------------------------------------------------+
```

Mobile layout:

1. Context and summary stack vertically.
2. Evidence refs and boundaries become two tabs.
3. Long refs wrap in monospace blocks with copy controls.
4. Detail drawer becomes a full-screen sheet.

## 4. Required UI Components / 必需组件

| Component | Required content | Must not do |
| --- | --- | --- |
| Context bar | account id and Account Evidence checkpoint | hide account context |
| Evidence package row | P077 package id, owner, schema ref, normalized ref, source ref and checksum | infer readiness from filled state |
| Source refs list | source ref, checksum, owner, authority | treat raw reports as truth |
| Boundary list | runtime, account, order, ledger, UI, broker and action flags | convert false flags into pass badges |
| Rejection rule list | rejection rules from Account Evidence fixture | hide missing source refs |
| Detail drawer | source refs, blockers and rejection rules | mutate source payload |
| Blocked state | missing ref, checksum mismatch, route mapping blocker | collapse into healthy or complete |

## 5. Data Test ID / 测试钩子

Required stable hooks:

```text
account-evidence-panel
account-evidence-context-bar
account-evidence-table
account-evidence-package-row
account-evidence-boundary-list
account-evidence-source-ref
account-evidence-rejection-rule
account-evidence-blocker
account-evidence-detail-drawer
```

## 6. State Matrix / 状态矩阵

| State | Trigger | UI requirement |
| --- | --- | --- |
| filled_bounded_slice | Current P077 fixture has bounded filled source ref/checksum and no active authorization | show filled slice as bounded evidence only |
| blocked_missing_ref | any required source ref, checksum or owner is missing | show blocker with owner and next action |
| stale_or_mismatched_checksum | source checksum does not match accepted fixture/proposal ref | show stale/mismatch state |
| no_active_authorization | fixture says active authorization is false | show no active authorization without implying readiness |

## 7. Forbidden UI / 禁止 UI

The panel must not show:

1. `Paper ready`
2. `Live ready`
3. `admitted`
4. `production ready`
5. `capital allocated`
6. `can trade`
7. `broker tradable`
8. order submit/cancel/replace controls
9. Paper retry authorization controls
