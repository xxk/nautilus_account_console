# P004 UI Acceptance: Account Workbench

- Proposal ID: `p004-account-workbench-summary-panel`
- Status: design_gate_ready
- Updated: 2026-06-14
- UI design: [P004 UI Design](./ui-design.md)
- Parent acceptance: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- Anti-drift acceptance: [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
- Order Observation V1 acceptance: [P004 Exception-First Order Observation MVP Acceptance](./order-observation-v1-acceptance.md)

## 1. Required UI Evidence / 必需 UI 证据

| Evidence | Required artifact |
| --- | --- |
| Summary read model contract | `contracts/ui/panels/account_summary_panel.contract.json` |
| Drill-down read model contracts | `contracts/ui/panels/account_{orders,order_detail,positions,settlement,equity,reconcile,incidents,evidence}_panel.contract.json` before each panel implementation |
| Happy fixture | `/accounts/{account_id}` with complete summary refs |
| Empty fixture | unknown account or missing summary read model |
| Blocked fixture | settlement/carryover/source mismatch blocker |
| Stale fixture | stale reducer checkpoint or stream cursor |
| Partial fixture | incomplete settlement/equity/carryover evidence |
| Desktop screenshot | `/accounts/{account_id}` with happy-path fixture |
| Tablet screenshot | `/accounts/{account_id}` with happy-path fixture |
| Mobile screenshot | `/accounts/{account_id}` with happy-path fixture and drawer/sheet |
| DOM/test evidence | stable `data-testid` hooks for panel, context bar, tabs, metrics, refs, blockers and drawer |
| Forbidden wording scan | source scan and browser text scan |
| Anti-drift evidence | completed anti-drift checklist in [P004 acceptance](./acceptance.md) |

## 1.1 Route-Level Acceptance Gates / Route 级验收门

| Route | Gate | Required before implementation closeout |
| --- | --- | --- |
| `/accounts` | Account overview selector preserves workbench context | contract, fixtures, selectors and browser evidence if implemented |
| `/accounts/{account_id}` | Account Summary Panel | contract, fixtures, selectors and desktop/tablet/mobile browser evidence |
| `/accounts/{account_id}/orders` | Orders Current Panel | official order event lineage refs; final snapshot cannot be truth |
| `/accounts/{account_id}/orders/{client_order_id}` | Order Lifecycle Panel | official order event sequence and report provenance refs |
| `/accounts/{account_id}/positions` | Positions Panel | carryover and settlement refs; no browser-inferred availability |
| `/accounts/{account_id}/settlement` | Settlement Panel | previous/current settlement refs or typed blocker |
| `/accounts/{account_id}/equity` | Equity Panel | ledger-derived equity refs; no chart/report-derived truth |
| `/accounts/{account_id}/reconcile` | Reconcile Panel | mismatch/tolerance/blocker refs and owner next action |
| `/accounts/{account_id}/incidents` | Incidents Panel | incident owner, next action and repair refs |
| `/accounts/{account_id}/evidence` | Account Evidence Panel | schema refs, checksums and run/session/trading day refs |

## 1.2 Phase-Level Acceptance Gates / Phase 级验收门

| Phase | Must pass | Must fail if | Browser evidence |
| --- | --- | --- | --- |
| Phase 1 Summary contract/fixtures | contract and happy/empty/blocked/stale/partial fixtures exist with source refs | fields are invented in frontend or missing refs render healthy | not required until Phase 2 |
| Phase 2 Summary UI | `/accounts/{account_id}` shows context, metrics, refs and blockers | first viewport is raw artifact/debug menu or disconnected page | desktop/tablet/mobile required |
| Phase 3 Orders lifecycle | orders link final/current rows to official event timeline and report provenance | final order snapshot is lifecycle truth or raw report is parsed as truth | desktop route screenshot or typed blocker for MVP; tablet/mobile deferred |
| Phase 4 Positions | positions show carryover and settlement refs | availability/carryover is inferred in browser or missing evidence is zeroed | route screenshot or typed blocker |
| Phase 5 Settlement/equity | settlement and equity are ledger-derived with refs/blockers | chart/report/HTML/stdout/browser state becomes truth | route screenshot or typed blocker for each implemented route |
| Phase 6 Reconcile/incidents | mismatches and incidents show severity, owner and next action | mismatches are hidden or incident is just log text | route screenshot or typed blocker for each implemented route |
| Phase 7 Evidence | evidence packages show schema, checksum and lineage; raw payload loads by ref | latest/debug path is evidence truth or raw payload dominates first screen | route screenshot or typed blocker |
| Phase 8 Closeout | checks, forbidden scan and browser evidence match implemented phases | design-gate routes are labeled browser verified without evidence | required for every implemented P004 route |

## 2. Positive UI Acceptance / 正向 UI 验收

| ID | Must pass | Evidence |
| --- | --- | --- |
| P004-UI-POS-01 | `/accounts/{account_id}` first viewport shows Account Workbench context before raw artifact menus | desktop screenshot |
| P004-UI-POS-02 | context bar shows account id, account kind, portfolio uid, trading day, session id and reducer checkpoint | DOM test or screenshot |
| P004-UI-POS-03 | metric strip shows equity, cash, frozen cash, margin, buying power, realized/unrealized PnL, lag and health | fixture-backed test |
| P004-UI-POS-04 | source refs show account snapshot, settlement, position carryover, reducer checkpoint and blocker refs where available | fixture-backed test |
| P004-UI-POS-05 | tabs preserve Account Workbench parent context and account id | route interaction test |
| P004-UI-POS-06 | selecting a source ref opens a read-only evidence/detail drawer | interaction test |
| P004-UI-POS-07 | happy, empty, blocked, stale and partial states render distinct visual states | state screenshots or typed blocker |
| P004-UI-POS-08 | desktop, tablet and mobile layouts have no overlapping account ids, refs, metric labels or badges | screenshot review |
| P004-UI-POS-09 | each implemented account drill-down route preserves account id, breadcrumbs and source refs | route interaction test |
| P004-UI-POS-10 | orders and order detail panels show official order-event lineage and report provenance when implemented | fixture-backed test |
| P004-UI-POS-11 | settlement and equity panels show ledger-derived refs or typed blockers when implemented | fixture-backed test |
| P004-UI-POS-12 | Order Observation V1 uses the exception-first MVP acceptance before `/accounts/{account_id}/orders` or order detail implementation closeout | [order-observation-v1-acceptance.md](./order-observation-v1-acceptance.md) |

## 2.1 Basic Business Domain Acceptance / 基础业务域验收

These rows define the minimum acceptance shape before any P004 implementation can claim a domain is ready. They are design-gate rows until contracts, fixtures and browser evidence land.

| Domain | Routes | Required contract/fixture content | Must pass | Must fail if |
| --- | --- | --- | --- | --- |
| Orders current view | `/accounts/{account_id}/orders` | current order rows, account id, client order id, instrument, side, quantity, latest official event ref, stale/gap state | rows link to official event lineage and preserve Account Workbench context | final/current order row is treated as lifecycle truth |
| Order lifecycle detail | `/accounts/{account_id}/orders/{client_order_id}` | ordered event sequence, event ids, timestamps, status transitions, cursor/checksum refs | detail route reconstructs lifecycle from official order events only | browser invents project-local order states or hides missing event gaps |
| Order report provenance | `/accounts/{account_id}/orders/{client_order_id}` and `/accounts/{account_id}/evidence` | report refs, normalized event links, checksum, source owner, raw payload ref | report payload is shown only as provenance/debug drill-down attached to normalized events | raw report text becomes order/account truth or first-screen workflow |
| Funds / cash summary | `/accounts/{account_id}` and `/accounts/{account_id}/settlement` | cash, frozen cash, margin, buying power, fees, taxes, settlement refs, blocker refs | displayed funds are read-model projections with source refs or typed blockers | UI mutates funding/allocation or labels funds as real capital approval |
| Positions | `/accounts/{account_id}/positions` | instrument, side, quantity, available/frozen quantity, average price, market value, PnL, carryover refs, settlement refs | positions distinguish zero position from missing evidence and expose carryover lineage | browser infers availability/carryover or missing evidence is rendered as zero |
| Settlement | `/accounts/{account_id}/settlement` | previous/current trading day, settlement state, opening/closing cash, margin, fees, taxes, settlement artifact refs | settlement status is source/ref-backed or blocked with owner and next action | day close appears successful without settlement artifact or typed blocker |
| Equity | `/accounts/{account_id}/equity` | ledger-derived equity points, daily return, cumulative return, source refs, checksum | chart/table renders ledger-derived values only and names source refs | equity is derived from chart pixels, report HTML, screenshots, stdout or browser state |
| Reconcile | `/accounts/{account_id}/reconcile` | mismatch id, dimension, expected/actual summary, tolerance ref, severity, owner, next action | mismatches are visible, sortable/scannable and source-ref backed | mismatch is hidden as normal styling or dismissed without typed repair projection |
| Incidents | `/accounts/{account_id}/incidents` | incident id, category, source ref, severity, owner, next action, repair refs | incident rows expose owner and next diagnostic/repair ref | incident is reduced to unowned log text or silently marked resolved |
| Evidence package | `/accounts/{account_id}/evidence` | schema version, checksum, run id, session id, trading day, producer owner, source refs | evidence drill-down links source lineage without becoming truth writer | latest/debug path is accepted as evidence truth |

## 3. Negative UI Acceptance / 反向 UI 验收

| ID | Must fail if |
| --- | --- |
| P004-UI-NEG-01 | Account Summary Panel appears without a declared read model contract and fixture state |
| P004-UI-NEG-02 | UI consumes fields not present in the contract or fixtures |
| P004-UI-NEG-03 | account values appear without source refs, checksums or typed blockers |
| P004-UI-NEG-04 | raw artifact menus or raw report payloads are the first visible workflow |
| P004-UI-NEG-05 | blocked, stale or partial states collapse into a generic healthy or empty state |
| P004-UI-NEG-06 | visible UI uses forbidden readiness, admission, capital or tradability wording |
| P004-UI-NEG-07 | UI exposes broker action, order submit/cancel/replace, direct funding mutation or direct account lifecycle mutation |
| P004-UI-NEG-08 | browser computes account equity, settlement, position availability or tradability truth |
| P004-UI-NEG-09 | `/accounts/{account_id}` opens as a disconnected route island without Account Workbench context |
| P004-UI-NEG-10 | account drill-down routes appear as peer primary navigation entries |
| P004-UI-NEG-11 | orders view treats final order snapshot as lifecycle truth |
| P004-UI-NEG-12 | settlement or equity view derives account truth from charts, reports, screenshots, stdout or browser state |
| P004-UI-NEG-13 | order report payload is parsed in the browser as order/account truth instead of provenance attached to normalized events |
| P004-UI-NEG-14 | funds/cash view exposes funding mutation, allocation mutation, real capital approval or tradability claims |
| P004-UI-NEG-15 | position view collapses missing carryover/settlement evidence into zero position or healthy state |
| P004-UI-NEG-16 | reconcile or incident view hides owner, severity, next action or source refs for blockers |

## 4. Data Test ID Acceptance / 测试钩子验收

All required hooks from [P004 UI Design](./ui-design.md) must exist.

Minimum required selectors:

```text
[data-testid="account-workbench-summary-panel"]
[data-testid="account-workbench-context-bar"]
[data-testid="account-workbench-account-selector"]
[data-testid="account-workbench-tab-list"]
[data-testid="account-summary-metric-strip"]
[data-testid="account-summary-health-state"]
[data-testid="account-summary-source-ref"]
[data-testid="account-summary-blocker"]
[data-testid="account-summary-empty-state"]
[data-testid="account-summary-stale-state"]
[data-testid="account-summary-detail-drawer"]
[data-testid="account-orders-panel"]
[data-testid="account-order-detail-panel"]
[data-testid="account-positions-panel"]
[data-testid="account-settlement-panel"]
[data-testid="account-equity-panel"]
[data-testid="account-reconcile-panel"]
[data-testid="account-incidents-panel"]
[data-testid="account-evidence-panel"]
```

## 5. Browser Acceptance / 浏览器验收

Required viewport checks:

| Viewport | Width x height | Required proof |
| --- | --- | --- |
| Desktop | 1440 x 900 | context bar, metrics, source refs and drawer |
| Tablet | 1024 x 768 | tabs usable, no overlap, refs visible |
| Mobile | 390 x 844 | stacked summary, horizontal tabs or compact tabs, full-screen drawer/sheet |

Must pass:

1. No horizontal overflow caused by account ids, route tabs, refs or checksums.
2. Metric strip values do not shift layout when fixture changes.
3. Detail drawer does not hide account context in desktop layout.
4. Mobile sheet has visible close affordance and source refs remain readable.
5. Browser evidence is captured after the final implementation change.
6. Implemented secondary account routes have proposal-level screenshots or typed browser/tooling blockers.

Phase-specific screenshot expectations:

| Phase | Required screenshots when implemented |
| --- | --- |
| Phase 2 | `/accounts/{account_id}` happy, blocked, stale or partial state across desktop/tablet/mobile |
| Phase 3 | `/accounts/{account_id}/orders` and `/accounts/{account_id}/orders/{client_order_id}` with order lineage visible on desktop; tablet/mobile deferred for MVP |
| Phase 4 | `/accounts/{account_id}/positions` with carryover/settlement refs or blocked state |
| Phase 5 | `/accounts/{account_id}/settlement` and `/accounts/{account_id}/equity` with ledger refs or blockers |
| Phase 6 | `/accounts/{account_id}/reconcile` and `/accounts/{account_id}/incidents` with owner/next action visible |
| Phase 7 | `/accounts/{account_id}/evidence` with schema/checksum/source lineage visible |

Screenshots prove rendering only. They never prove account truth, settlement truth, equity truth, broker truth, admission truth, approval truth or capital truth.

## 6. Required Validation Commands / 必跑验证

Minimum repo checks:

```powershell
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates contracts\ui
```

Frontend checks when dependencies are available:

```powershell
cd frontend
npm run build
npm run test
npm run test:e2e
```

## 7. Blocker Recording / 阻塞记录

If UI acceptance cannot be completed, the implementation change must record:

```text
UI Acceptance Blocker:
  proposal_or_change_id: p004-account-workbench-summary-panel
  route: /accounts/{account_id}
  phase:
  workbench: Account Workbench
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
