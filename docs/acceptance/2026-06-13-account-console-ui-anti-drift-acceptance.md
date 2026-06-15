# Account Console UI Anti-Drift Acceptance / 账户控制台 UI 防跑偏验收

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: active anti-drift acceptance
- Scope: mandatory acceptance guardrails for UI proposals and successor implementation changes
- Design anchors:
  - [Capability UI design](../design/account-console-capability-ui-design.md)
  - [UI implementation design](../design/account-console-ui-implementation-design.md)
  - [UI landing blueprint](../design/account-console-ui-landing-blueprint.md)
- Acceptance anchors:
  - [Capability UI acceptance](./2026-06-13-account-console-capability-ui-acceptance.md)
  - [UI implementation acceptance](./2026-06-13-account-console-ui-implementation-acceptance.md)
  - [UI route coverage matrix](./2026-06-13-account-console-ui-route-coverage-matrix.md)

## 1. Purpose / 目的

This acceptance prevents future AI-assisted UI work from drifting away from the business workbench model.

The UI route map contains 26 routable capabilities, but the product model is not 26 peer pages. Account Console has seven primary workbench entries. Secondary routes are tabs, drawers, drill-downs or deep links that preserve parent context.

## 2. Mandatory Anti-Drift Checklist / 必填防跑偏清单

Every UI proposal or successor implementation change must fill this block before code:

```text
UI Anti-Drift Acceptance:
  proposal_or_change_id:
  route_tier: primary_workbench | account_drilldown | management_drilldown | portfolio_review | ops_drilldown
  primary_workbench:
  route_or_routes_touched:
  route_coverage_matrix_rows:
  promoted_to_primary_navigation: yes | no
  promotion_reason:
  parent_context_required:
  breadcrumbs_required:
  source_refs_required:
  read_model_contracts:
  fixture_states:
    - happy_path
    - empty
    - blocked
    - stale_or_partial
  browser_evidence_required:
  screenshot_viewports:
  first_viewport_contract:
  landing_blueprint_checked:
  closeout_ui_open_required: yes
  closeout_ui_open_evidence:
  forbidden_primary_menu_entries:
  forbidden_actions:
  forbidden_claims:
  positive_acceptance_ids:
  negative_acceptance_ids:
  blocker_conditions:
```

## 3. Route Tier Rules / 路由层级规则

| Tier | Routes | Allowed UI form | Acceptance rule | Must fail if |
| --- | --- | --- | --- | --- |
| `primary_workbench` | `/closeout`, `/monitor`, `/accounts/{account_id}`, `/management/accounts`, `/risk-reconcile`, `/evidence`, `/ops/stream` | first-class workbench page | may appear in primary navigation and needs browser acceptance when implemented | route is hidden behind raw artifact/debug navigation |
| `account_drilldown` | `/accounts`, `/accounts/{account_id}/orders`, `/accounts/{account_id}/orders/{client_order_id}`, `/accounts/{account_id}/positions`, `/accounts/{account_id}/settlement`, `/accounts/{account_id}/equity`, `/accounts/{account_id}/reconcile`, `/accounts/{account_id}/incidents`, `/accounts/{account_id}/evidence` | Account Workbench tab, drawer, nested panel or deep link | must preserve account id, breadcrumbs and source refs | opens as disconnected page or loses account context |
| `management_drilldown` | `/management/accounts/requests`, `/management/assignments`, `/management/funding` | Allocation Admin tab, request queue, drawer or replay panel | must preserve request/projection boundary | directly mutates accepted lifecycle/allocation truth |
| `portfolio_review` | `/portfolio`, `/portfolio/attribution`, `/portfolio/reconcile`, `/portfolio/risk`, `/portfolio/closeout` | deferred PM review surface | must remain read-only and depend on account/settlement/equity/attribution read models | claims Paper readiness, Live readiness, admission, approval or capital truth |
| `ops_drilldown` | `/ops/replay`, `/ops/benchmarks` | Stream Ops diagnostic panel or deep link | must cite cursor/checksum/durable ledger evidence | implies trading readiness or bypasses durable ledger evidence |

## 4. Primary Navigation Acceptance / 主导航验收

| ID | Must pass | Must fail if |
| --- | --- | --- |
| UI-DRIFT-NAV-01 | primary navigation contains the seven workbench entries only | sidebar/top navigation shows all 26 route-map entries as peers |
| UI-DRIFT-NAV-02 | secondary routes appear under their parent workbench context | account, management, portfolio or ops drill-downs appear as unrelated route islands |
| UI-DRIFT-NAV-03 | direct deep-link entry restores breadcrumb and parent context | deep link lands on a blank technical page with no business context |
| UI-DRIFT-NAV-04 | route promotion requires proposal-level design and acceptance update | a secondary route becomes a primary page without explicit acceptance |

## 5. Evidence Boundary Acceptance / 证据边界验收

| ID | Must pass | Must fail if |
| --- | --- | --- |
| UI-DRIFT-EVD-01 | every displayed state has source refs, checksums or typed blockers | UI value appears with no provenance |
| UI-DRIFT-EVD-02 | raw reports are drill-down/debug evidence only | raw reports become the first-screen or primary workflow |
| UI-DRIFT-EVD-03 | missing source evidence appears as `blocked`, `partial` or `stale` | UI hides missing evidence behind success styling |
| UI-DRIFT-EVD-04 | browser charts/tables display projections, not recomputed account truth | browser becomes account, settlement or equity truth |

## 6. Forbidden Claim Acceptance / 禁止声明验收

| ID | Must fail if visible UI, fixture labels or API projection labels claim |
| --- | --- |
| UI-DRIFT-CLAIM-01 | Paper readiness |
| UI-DRIFT-CLAIM-02 | Live readiness |
| UI-DRIFT-CLAIM-03 | admission approval |
| UI-DRIFT-CLAIM-04 | PM approval |
| UI-DRIFT-CLAIM-05 | real capital allocation |
| UI-DRIFT-CLAIM-06 | account tradability |
| UI-DRIFT-CLAIM-07 | trading readiness from replay, benchmark or stream health |

## 7. Forbidden Action Acceptance / 禁止动作验收

| ID | Must fail if UI exposes |
| --- | --- |
| UI-DRIFT-ACT-01 | order submit, cancel, replace or modify |
| UI-DRIFT-ACT-02 | broker action |
| UI-DRIFT-ACT-03 | runtime state mutation |
| UI-DRIFT-ACT-04 | direct accepted lifecycle ledger mutation |
| UI-DRIFT-ACT-05 | direct accepted funding/allocation ledger mutation |
| UI-DRIFT-ACT-06 | UI-only correction of account, order, fill, position, settlement or equity truth |

## 8. Required Evidence / 必需证据

Any UI proposal/change acceptance closeout must include:

1. Completed `UI Anti-Drift Acceptance` block.
2. Route tier and parent workbench declaration.
3. Confirmed coverage matrix rows for every route touched.
4. Source refs or typed blockers for every displayed account/order/fill/position/settlement/equity/risk state.
5. Browser evidence for primary workbench pages when implemented.
6. Proposal-level browser evidence for secondary routes when implemented or promoted.
7. Closeout UI-open evidence proving the touched route was opened after the final implementation change.
8. Static forbidden wording/action scan.
9. Typed blocker if browser evidence cannot be produced.

Closeout cannot pass from static checks, unit tests, old screenshots, terminal output or route definitions alone. If the UI route cannot be opened during closeout, the proposal/change must remain blocked with a typed browser-tooling or environment blocker.
