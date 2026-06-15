# Account Console UI Route Coverage Matrix / 账户控制台 UI 路由验收覆盖矩阵

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: active coverage matrix
- Scope: route-by-route UI acceptance coverage for the 26-route capability map
- Anchors:
  - [Capability UI design](../design/account-console-capability-ui-design.md)
  - [Capability UI acceptance](./2026-06-13-account-console-capability-ui-acceptance.md)
  - [UI implementation acceptance](./2026-06-13-account-console-ui-implementation-acceptance.md)
  - [UI anti-drift acceptance](./2026-06-13-account-console-ui-anti-drift-acceptance.md)

## 1. Coverage Summary / 覆盖摘要

| Count | Meaning |
| --- | --- |
| 26 | total routable capabilities in the route map |
| 7 | primary workbench pages requiring browser acceptance when implemented |
| 19 | secondary routes requiring proposal-level acceptance when implemented or promoted |
| 9 | current proposal-level UI browser evidence completed: P001 `/closeout` Account Health Panel, P009 P077 Paper Slice Evidence Panel, P004 Phase 2 Account Summary Panel, P004 Phase 3 Orders/Order Detail Panel, P004 Phase 4 Positions Panel, P004 Phase 5 Settlement/Equity Panel, P004 Phase 6 Reconcile/Incidents Panel, P004 Phase 7 Evidence Panel and P005 `/monitor` Intraday Monitor |
| 0 | current proposal-level contract/fixture gates waiting for browser implementation |

Coverage does not mean all 26 routes are ready to implement. Coverage means every route has a declared tier, parent context, acceptance anchor and anti-drift rule so later AI work cannot land outside the product model.

Compatibility note: P001 and the P009 P077 slice now have completed proposal-level browser coverage; P004 Phase 2 adds Account Summary browser evidence, P004 Phase 3 adds orders/order-detail browser evidence, P004 Phase 4 adds positions browser evidence, P004 Phase 5 adds settlement/equity browser evidence, P004 Phase 6 adds reconcile/incidents browser evidence, P004 Phase 7 adds evidence browser evidence and P004 Phase 8 closes the P004 scoped Account Workbench phases. P005 Phase 2 adds `/monitor` Intraday Monitor browser evidence from accepted fixtures. This still does not claim full Account Console UI completion.

## 2. Coverage Status Legend / 覆盖状态说明

| Status | Meaning |
| --- | --- |
| `covered-global` | route has capability, implementation and anti-drift acceptance anchors |
| `covered-proposal` | route also has proposal-level UI design and UI acceptance |
| `proposal-required` | route must add proposal-level `ui-design.md` and `ui-acceptance.md` before implementation |
| `deferred` | route is intentionally later-stage; must not be implemented without mature read models and proposal acceptance |

All routes inherit:

1. `UI-IMPL-*` implementation gates.
2. `UI-DRIFT-*` anti-drift gates.
3. Global guards from capability UI acceptance.

## 3. Route Coverage Matrix / 路由覆盖矩阵

| Route | Tier | Parent workbench | Capability acceptance | Browser acceptance | Proposal-level status | Must not miss |
| --- | --- | --- | --- | --- | --- | --- |
| `/closeout` | primary_workbench | Daily Closeout | UI-WB-01, UI-VIS-01, UI-ROUTE-01 | required primary | covered-proposal: P001 | blockers, settlement, equity continuity, refs |
| `/monitor` | primary_workbench | Intraday Monitor | UI-WB-02, UI-ROUTE-01, UI-HFT-01 | required primary | covered-proposal: P005 Phase 2 UI/browser evidence exists | active issues, stale streams, lag, incidents |
| `/accounts` | account_drilldown | Account Workbench | UI-OBS-01, UI-ROUTE-02 | proposal-level when implemented | covered-design-gate: P004; browser evidence still required before implementation closeout | account list must open account context |
| `/accounts/{account_id}` | primary_workbench | Account Workbench | UI-WB-03, UI-OBS-02, UI-ROUTE-01 | required primary | covered-proposal: P004 Phase 8 scoped Account Workbench closeout exists | account context, tabs, latest settlement/blockers |
| `/accounts/{account_id}/orders` | account_drilldown | Account Workbench | UI-OBS-04, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 3 orders UI/browser evidence exists | final order row is not lifecycle truth |
| `/accounts/{account_id}/orders/{client_order_id}` | account_drilldown | Account Workbench | UI-OBS-05, UI-OBS-06, UI-ROUTE-02 | core secondary screenshot before acceptance | covered-proposal: P004 Phase 3 order-detail UI/browser evidence exists; P009 E93 implementation/browser evidence exists for the P077 read-only panel only | official order events and report provenance; P077 slice remains read-only evidence only |
| `/accounts/{account_id}/positions` | account_drilldown | Account Workbench | UI-OBS-03, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 4 positions UI/browser evidence exists | carryover and settlement refs |
| `/accounts/{account_id}/settlement` | account_drilldown | Account Workbench | UI-OBS-08, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 5 settlement UI/browser evidence exists | no silent day close without settlement/blocker |
| `/accounts/{account_id}/equity` | account_drilldown | Account Workbench | UI-OBS-09, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 5 equity UI/browser evidence exists | ledger-derived curve only |
| `/accounts/{account_id}/reconcile` | account_drilldown | Account Workbench | UI-OBS-10, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 6 reconcile UI/browser evidence exists | mismatches cannot be hidden |
| `/accounts/{account_id}/incidents` | account_drilldown | Account Workbench | UI-OBS-11, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 6 incidents UI/browser evidence exists | incident owner, next action, repair refs |
| `/accounts/{account_id}/evidence` | account_drilldown | Account Workbench | UI-OBS-12, UI-ROUTE-02 | proposal-level when implemented | covered-proposal: P004 Phase 7 evidence UI/browser evidence exists; P009 E93 implementation/browser evidence exists for the P077 read-only panel only | refs/checksums/schema/run/session/trading day; P077 fixture cannot become runtime truth |
| `/management/accounts` | primary_workbench | Allocation Admin | UI-WB-04, UI-MGMT-01, UI-MGMT-02, UI-MGMT-03, UI-ROUTE-01 | required primary | proposal-required | request/projection boundary |
| `/management/accounts/requests` | management_drilldown | Allocation Admin | UI-MGMT-07, UI-ROUTE-03 | proposal-level when implemented | proposal-required | requests are not accepted ledger truth |
| `/management/assignments` | management_drilldown | Allocation Admin | UI-MGMT-04, UI-ROUTE-03 | proposal-level when implemented | proposal-required | no implicit default account |
| `/management/funding` | management_drilldown | Allocation Admin | UI-MGMT-05, UI-MGMT-06, UI-ROUTE-03 | core secondary screenshot before acceptance | proposal-required | virtual funding is not real capital approval |
| `/portfolio` | portfolio_review | Portfolio / PM Review | UI-PM-01, UI-ROUTE-04 | core secondary screenshot before acceptance | deferred | no Paper/Live readiness claim |
| `/portfolio/attribution` | portfolio_review | Portfolio / PM Review | UI-PM-02, UI-ROUTE-04 | proposal-level when implemented | deferred | attribution cannot infer only from final equity |
| `/portfolio/reconcile` | portfolio_review | Portfolio / PM Review | UI-PM-03, UI-ROUTE-04 | proposal-level when implemented | deferred | pending orders/conflicts are visible |
| `/portfolio/risk` | portfolio_review | Portfolio / PM Review | UI-PM-04, UI-ROUTE-04 | proposal-level when implemented | deferred | UI judgment cannot replace risk artifacts |
| `/portfolio/closeout` | portfolio_review | Portfolio / PM Review | UI-PM-05, UI-ROUTE-04 | proposal-level when implemented | deferred | PM closeout cannot write admission/capital truth |
| `/risk-reconcile` | primary_workbench | Risk And Reconcile | UI-WB-05, UI-OBS-10, UI-ROUTE-01 | required primary | proposal-required | blocker severity, tolerances and source refs |
| `/evidence` | primary_workbench | Evidence Explorer | UI-WB-06, UI-OBS-12, UI-ROUTE-01 | required primary | proposal-required | evidence packages, checksums and repair refs |
| `/ops/stream` | primary_workbench | Stream Ops | UI-WB-07, UI-HFT-01, UI-HFT-02, UI-ROUTE-01 | required primary | proposal-required | no HFT readiness claim |
| `/ops/replay` | ops_drilldown | Stream Ops | UI-HFT-03, UI-ROUTE-05 | proposal-level when implemented | proposal-required | replay is diagnostic, not trading readiness |
| `/ops/benchmarks` | ops_drilldown | Stream Ops | UI-HFT-04, UI-ROUTE-05 | proposal-level when implemented | proposal-required | benchmark evidence must be typed |

## 4. Coverage Acceptance / 覆盖验收

| ID | Must pass | Must fail if |
| --- | --- | --- |
| UI-COV-01 | all 26 route-map entries appear in this coverage matrix | a route exists in design route map but not in coverage matrix |
| UI-COV-02 | each route has exactly one route tier | route tier is missing or ambiguous |
| UI-COV-03 | each route maps to a parent workbench | route has no business parent context |
| UI-COV-04 | each route maps to at least one capability acceptance ID | route has no acceptance anchor |
| UI-COV-05 | each primary workbench route declares browser acceptance requirement | primary route has no screenshot/browser acceptance path |
| UI-COV-06 | each secondary route declares proposal-level acceptance requirement | secondary route can be implemented without proposal `ui-design.md` and `ui-acceptance.md` |
| UI-COV-07 | each deferred portfolio route remains read-only and deferred until read models are mature | portfolio route is implemented early as readiness/capital/approval surface |
| UI-COV-08 | P001, P009, P004 Phase 2 through Phase 8 and P005 Phase 2 now have completed proposal-level browser/closeout coverage for their scoped routes | docs imply unimplemented routes already have implementation or browser acceptance |

## 5. Successor Proposal Rule / 后续 Proposal 规则

When a proposal implements any route in this matrix, it must update:

1. This matrix row's `Proposal-level status`.
2. Its own `ui-design.md`.
3. Its own `ui-acceptance.md`.
4. Its own completed `UI Anti-Drift Acceptance` block.
5. Screenshot/browser evidence requirements for the route tier.

If a proposal adds a new route, it must update:

1. Capability UI design route map.
2. UI implementation design route hierarchy.
3. UI anti-drift route tier rules.
4. This coverage matrix.
5. Capability and implementation acceptance IDs.
