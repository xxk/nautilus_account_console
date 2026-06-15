# Account Console UI Implementation Acceptance / 账户控制台 UI 实现级验收

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: active implementation acceptance baseline
- Scope: global acceptance gates for Account Console UI implementation
- Design anchor: [Account Console UI implementation design](../design/account-console-ui-implementation-design.md)
- Capability acceptance anchor: [Account Console capability UI acceptance](./2026-06-13-account-console-capability-ui-acceptance.md)
- Anti-drift acceptance anchor: [Account Console UI anti-drift acceptance](./2026-06-13-account-console-ui-anti-drift-acceptance.md)
- Route coverage anchor: [Account Console UI route coverage matrix](./2026-06-13-account-console-ui-route-coverage-matrix.md)
- Owner map anchor: [Account Console owner map](../ownership/account-console-owner-map.md)

## 1. Acceptance Boundary / 验收边界

This document accepts UI implementation quality only. It does not accept Paper runtime correctness, real broker connectivity, PM approval, admission approval, real capital allocation, matching engine correctness or trading readiness.

UI implementation is accepted only when it is backed by:

1. A declared workbench and panel.
2. A completed `UI Anti-Drift Acceptance` block.
3. A completed `Owner Boundary` block with producer, verifier, projection, UI/report and approval owners.
4. A route coverage matrix row for every route touched.
5. A read model contract or typed blocker.
6. Happy, empty, blocked and stale/partial fixtures or typed blockers.
7. Stable selectors.
8. Browser or deterministic rendering evidence.
9. Forbidden action and forbidden wording checks.
10. A closeout UI-open acceptance pass for every implemented or promoted UI route.

## 2. Global UI Acceptance Gates / 全局 UI 验收门

| ID | Gate | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-IMPL-01 | Workbench-first entry | first screen is an account workbench/control tower | app opens with marketing page or raw artifact menu |
| UI-IMPL-02 | Contract-backed panel | every new panel declares read model contract and fixtures | panel renders invented fields |
| UI-IMPL-03 | Read-only truth boundary | UI reads projections, refs and typed artifacts only | UI mutates runtime/account/broker/admission/capital truth |
| UI-IMPL-04 | Evidence visibility | displayed state has source refs or typed blockers | values appear with no traceable source |
| UI-IMPL-05 | Missing evidence state | missing, stale and partial evidence are visible | UI hides gaps behind healthy/empty state |
| UI-IMPL-06 | Stable selectors | major panel, row, filter, state and drawer hooks exist | UI cannot be deterministically tested |
| UI-IMPL-07 | Responsive layout | desktop, tablet and mobile have no overlap or hidden critical state | labels, refs or badges overlap/clipped |
| UI-IMPL-08 | Forbidden actions | no broker, runtime, order-entry or direct ledger mutation controls appear | UI behaves like a trading terminal |
| UI-IMPL-09 | Route hierarchy | seven primary workbench entries are primary; secondary routes are tabs/drawers/deep links | implementation renders all 26 capability routes as equal top-level pages |
| UI-IMPL-10 | Owner boundary | producer, verifier, projection, UI/report and approval owners are declared before implementation | implementation creates a second truth writer or ambiguous owner lane |
| UI-IMPL-11 | Closeout UI-open acceptance | closeout opens the implemented UI route in a browser or equivalent renderer and records viewport evidence or a typed browser-tooling blocker | closeout accepts a UI change from contract tests, static scans or screenshots from an old run only |

## 3. Required Proposal UI Acceptance / Proposal 必需 UI 验收

Every UI implementation proposal must include:

```text
ui-acceptance.md:
  route:
  route_tier:
  route_coverage_matrix_updated:
  workbench:
  panel:
  anti_drift_acceptance:
  required_screenshots:
  required_selectors:
  positive_acceptance:
  negative_acceptance:
  browser_acceptance:
  closeout_ui_open_acceptance:
    route_opened:
    closeout_time:
    viewport_evidence:
    manual_or_playwright_result:
    blocker_if_not_opened:
  fixture_replay_acceptance:
  performance_acceptance:
  forbidden_scan:
  blocker_conditions:
```

P001 is the reference example:

1. [P001 UI Design](../proposals/p001-daily-closeout-account-health-panel/ui-design.md)
2. [P001 UI Acceptance](../proposals/p001-daily-closeout-account-health-panel/ui-acceptance.md)

## 4. Screenshot Matrix / 截图矩阵

When browser tooling is available, each accepted UI slice must provide screenshots for:

| Viewport | Size | Required state |
| --- | --- | --- |
| Desktop | 1440 x 900 | happy path and blocked state |
| Tablet | 1024 x 768 | happy path |
| Mobile | 390 x 844 | happy path and drawer/sheet state |

For state-heavy panels, add screenshots for:

1. Empty state.
2. Stale state.
3. Partial evidence state.
4. Blocked state.

Primary workbench pages require browser acceptance when implemented:

1. `/closeout`
2. `/monitor`
3. `/accounts/{account_id}`
4. `/management/accounts`
5. `/risk-reconcile`
6. `/evidence`
7. `/ops/stream`

Secondary routes require proposal-level browser acceptance only when the proposal implements or promotes that route.

Closeout rule:

Every UI implementation closeout must open the touched route after the final code change and before marking the proposal/change accepted. The closeout evidence may be Playwright screenshots, deterministic browser-render artifacts, or a typed blocker explaining why browser tooling is unavailable. Static tests, contract tests, old screenshots, terminal output and build success alone cannot satisfy UI closeout.

## 5. Selector Acceptance / 选择器验收

Each panel must expose selectors for:

```text
panel root
filter toolbar
metric strip or summary
primary rows/items
state badge
source/evidence ref
detail drawer
empty state
blocked state
stale/partial state
```

Selectors must be stable across data changes and must not depend on visible text.

## 6. Negative Acceptance / 反向验收

UI implementation must fail acceptance if:

1. It starts from a whole route without a panel-level contract.
2. It consumes fields not declared in contract or fixture.
3. It makes raw reports, debug paths, stdout or report HTML the first-class truth.
4. It hides missing source evidence.
5. It labels runtime, admission, PM approval, capital or tradability as accepted UI truth.
6. It exposes order entry, broker action or direct accepted ledger mutation.
7. It uses decorative hero layout, nested cards or marketing copy as the primary workspace.
8. It lacks browser evidence or records no typed blocker for missing browser tooling.
9. It promotes secondary routes into peer primary navigation without a proposal and acceptance update.
10. It omits the anti-drift checklist or leaves route tier unspecified.
11. It touches a route without updating or confirming the route coverage matrix row.
12. It closes out a UI route without opening that route for final UI acceptance in the same change.

## 7. Required Local Checks / 必跑本地检查

Minimum checks:

```powershell
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates
```

When frontend dependencies are available:

```powershell
cd frontend
npm run build
npm run test
npm run test:e2e
```

## 8. Blocker Format / 阻塞格式

If an implementation cannot satisfy UI acceptance, it must record:

```text
UI Implementation Acceptance Blocker:
  proposal_or_change_id:
  route:
  workbench:
  panel:
  missing_contract:
  missing_fixture:
  missing_browser_tooling:
  missing_selector:
  missing_source_ref:
  violated_boundary:
  owner:
  next_action:
```
