# Account Console Capability UI Acceptance / 账户控制台能力级 UI 验收

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: acceptance baseline
- Scope: UI acceptance for account observability, account-management request surfaces, portfolio review and HFT stream operations

## 1. Acceptance Boundary

This acceptance validates Account Console UI behavior only. It does not accept Paper runtime correctness, broker tradability, Paper readiness, Live readiness, PM approval or real capital allocation.

All accepted UI evidence must come from normalized read models, typed artifacts, append-only ledgers or request contracts. UI screenshots, report HTML, stdout, latest/debug paths and manual notes cannot satisfy runtime/account truth.

## 2. Global UI Guards

| Guard | Required evidence | Must fail if |
| --- | --- | --- |
| Read-only truth boundary | UI reads normalized events/read models/artifacts and does not write runtime/account/broker/admission/capital truth | UI directly mutates runtime, ledger truth or broker state |
| Request/projection boundary | account-management controls create request/projection objects only after a request contract exists | UI directly appends accepted lifecycle/allocation ledger events |
| Forbidden wording | static scan and browser text scan find no `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated`, `can trade` | forbidden wording appears in visible UI or API fixture labels |
| Evidence provenance | every detail view exposes source refs/checksums/schema/run/session/trading day where applicable | view cannot trace displayed data to artifacts/read models |
| Missing evidence visibility | stale, partial, blocked and missing evidence states are visible | UI hides missing evidence or silently marks it healthy |
| Stable test hooks | major routes, panels, rows, drawers and action requests have `data-testid` hooks | UI cannot be tested deterministically |
| No trading terminal behavior | no submit/cancel/modify/replace trading actions are exposed | UI offers order-entry or broker actions |
| Route hierarchy | sidebar/top navigation contains seven primary workbench entries and secondary routes remain tabs/drawers/deep links | all 26 capability routes appear as peer primary pages |

## 3. Business Workbench Acceptance

| ID | Workbench | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-WB-01 | Daily Closeout | shows accounts needing closeout, settlement state, equity/PnL, blockers and next action before raw artifact menus | user must open every account to know if today can close |
| UI-WB-02 | Intraday Monitor | shows active accounts, active orders/fills, stale stream state, lag and incident queue | live problems are only visible inside deep technical pages |
| UI-WB-03 | Account Workbench | gives one-account drill-down with summary, positions, orders, fills, settlement, equity, order tape and report detail | order/fill/position views lose account context |
| UI-WB-04 | Allocation Admin | shows account registry, lifecycle, assignment, funding, request queue and replay/diff as request/projection surfaces | accepted account/funding truth is mutated directly by UI |
| UI-WB-05 | Risk And Reconcile | prioritizes risk triggers, reconcile gaps, tolerances, blocker severity and source refs | mismatches are hidden or treated as normal UI color only |
| UI-WB-06 | Evidence Explorer | gives refs/checksums/schema/run/session/trading-day evidence packages and repair refs | evidence is scattered only inside visual panels |
| UI-WB-07 | Stream Ops | isolates lag, cursor replay, backpressure, durable ledger checksum and benchmark evidence | HFT metrics dominate PM daily closeout or imply readiness |
| UI-WB-08 | Artifact drill-down | artifact routes are reachable from workbench context and preserve source lineage | artifact pages become disconnected route islands |

## 3.1 Route Hierarchy Acceptance / 路由层级验收

| ID | Route group | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-ROUTE-01 | Primary workbenches | `/closeout`, `/monitor`, `/accounts/{account_id}`, `/management/accounts`, `/risk-reconcile`, `/evidence` and `/ops/stream` are the only first-class workbench entries | UI presents all 26 routes as equal top-level pages |
| UI-ROUTE-02 | Account drill-downs | account secondary routes preserve account id, workbench breadcrumbs and source refs | `/accounts/{account_id}/positions`, settlement, equity, incidents or evidence open as disconnected route islands |
| UI-ROUTE-03 | Management drill-downs | management secondary routes stay under Allocation Admin and preserve request/projection boundary | assignment or funding pages mutate accepted lifecycle/allocation truth |
| UI-ROUTE-04 | Portfolio surface | portfolio routes are deferred/read-only PM review surfaces until account, settlement, equity and attribution read models exist | portfolio route claims Paper readiness, PM approval, admission or capital truth |
| UI-ROUTE-05 | Ops drill-downs | replay and benchmark routes stay under Stream Ops diagnostics and cite durable ledger evidence | ops routes imply trading readiness or bypass checksum/cursor evidence |

## 4. Account Observability Acceptance

| ID | UI | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-OBS-01 | Account Overview | lists accounts with id, kind, status, equity, cash, margin, PnL, stream health and settlement state | account can only be found through raw fixture/debug data |
| UI-OBS-02 | Account Detail | shows cash, frozen cash, margin, buying power, PnL, fees/taxes, latest settlement and blockers | account values have no source refs |
| UI-OBS-03 | Positions View | shows current qty, available/frozen qty, average price, market value, PnL, previous settlement and carryover refs | current position cannot trace to carryover or settlement |
| UI-OBS-04 | Orders View | shows current/final order derived state and links to lifecycle events | final order row is presented as lifecycle truth |
| UI-OBS-05 | Order Event Tape | renders official order event sequence with timestamps, ids, account, strategy, reconciliation flag and cursor | project-local order state appears without official mapping |
| UI-OBS-06 | Report Detail | lazy-loads `OrderStatusReport` / `FillReport` by ref/checksum and links normalized events | browser parses raw report as account truth |
| UI-OBS-07 | Fills View | shows trade id, qty, price, commission, liquidity side and linked order/account/position refs | fill appears without order/account lineage |
| UI-OBS-08 | Settlement View | shows previous/current settlement, settlement state, blocked reason and carryover | day closes without settlement or typed blocker |
| UI-OBS-09 | Equity Curve View | shows ledger-derived equity points with source refs | curve is generated from chart/report/HTML/stdout |
| UI-OBS-10 | Reconcile View | shows order/fill/position/account/settlement mismatches and blockers | mismatch is hidden or called normal without typed blocker |
| UI-OBS-11 | Incidents View | shows outage, stale order, reconcile gap, writer failure, owner, next action and repair refs | incident only appears as log text or color |
| UI-OBS-12 | Artifact Evidence View | shows refs, checksums, schema version, runtime owner, run/session/trading day and source refs | latest/debug path is treated as evidence truth |

## 5. Account Management UI Acceptance

| ID | UI | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-MGMT-01 | Account Registry | reconstructs account state from lifecycle/type projections and shows owner, status, permissions and effective period | account is created or changed only through UI/config/chat |
| UI-MGMT-02 | Lifecycle Timeline | displays create, activate, suspend, retire, type update, permission update, override and correction events | history is overwritten instead of superseded/corrected |
| UI-MGMT-03 | Account Type Registry | shows allowed markets, permissions, leverage/margin, netting policy, risk limits and broker-probe flag | account type is display text only |
| UI-MGMT-04 | Account Assignment | shows portfolio/strategy/sleeve scope, account id, type, effective period and source decision ref | strategy silently uses default account |
| UI-MGMT-05 | Funding Allocation | shows initial allocation, transfers, injection, withdrawal, risk reserve/release, override/correction and source decision refs | Paper funding is implied as real capital approval |
| UI-MGMT-06 | Allocation Replay | replay reconstructs account state, assignment state and available virtual capital | current state depends on manual config/UI state |
| UI-MGMT-07 | Request Boundary | create/suspend/retire/assign/fund controls are disabled or request-only until a typed request contract exists | UI directly mutates accepted account or funding truth |

## 6. Portfolio / PM UI Acceptance

| ID | UI | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-PM-01 | Portfolio Dashboard | shows equity, strategy contribution, open blockers, risk state and unfilled targets with refs | dashboard declares Paper/Live readiness |
| UI-PM-02 | Sleeve Attribution | shows PnL, fees, slippage, cash drag, hedge effect and drawdown contribution refs | attribution is inferred only from final equity |
| UI-PM-03 | Target Reconciliation | shows strategy target, portfolio target, actual position, pending orders, drift, shortfall, overfill and conflict policy | pending orders or conflicts are ignored |
| UI-PM-04 | Portfolio Risk | shows exposure, concentration, leverage, margin, drawdown, participation and capacity/liquidity refs | UI judgment replaces risk artifacts |
| UI-PM-05 | PM Daily Closeout | shows daily package refs, blockers, next action and tomorrow carry positions | PM closeout writes admission or capital truth |

## 7. HFT / Stream UI Acceptance

| ID | UI | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-HFT-01 | Stream Health | shows ingest lag, reducer lag, SSE state, backpressure, last cursor and gap/duplicate counts | healthy state is shown without cursor/lag evidence |
| UI-HFT-02 | Virtualized Event Tape | uses bounded visible rows, cursor pagination and pause/resume visual updates | unbounded DOM rows are rendered |
| UI-HFT-03 | Cursor Replay | supports replay from cursor with gap/duplicate/checksum evidence | replay evidence is used as trading readiness |
| UI-HFT-04 | Performance Benchmarks | displays typed `steady_1k_eps_5min` and `burst_10k_eps_30sec` evidence when available | HFT pass is claimed without benchmark artifacts |

## 8. Visual And Browser Acceptance

| ID | Check | Must pass | Must fail if |
| --- | --- | --- | --- |
| UI-VIS-01 | First screen | account control tower appears first, prioritizing Daily Closeout / Intraday Monitor states, not a landing page | marketing/hero page or raw route menu blocks the workspace |
| UI-VIS-02 | Layout stability | account list, metric strip, tables, tape and drawers keep stable dimensions | hover/loading/dynamic labels shift layout |
| UI-VIS-03 | Text fit | labels and values do not overlap at desktop and mobile widths | text overflows or occludes adjacent controls |
| UI-VIS-04 | Data density | operational data is compact and scannable | page uses decorative card-heavy composition |
| UI-VIS-05 | Screenshot QA | Playwright screenshot and non-overlap checks exist when Node/npm is available | visual acceptance is based only on manual inspection |

## 9. Required Validation Commands

Minimum local checks:

```powershell
python -m compileall backend/src
cargo test --manifest-path hotpath-rs/Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend/src backend/src hotpath-rs/crates
```

When Node/npm is available:

```powershell
cd frontend
npm install
npm run build
npm run test
npm run test:e2e
```

Primary workbench browser acceptance must include screenshots for:

1. `/closeout`
2. `/monitor`
3. `/accounts/{account_id}`
4. `/management/accounts`
5. `/risk-reconcile`
6. `/evidence`
7. `/ops/stream`

Secondary route browser acceptance should be added by the proposal that implements the route or panel. Core secondary examples that need proposal-level screenshots before acceptance:

1. `/accounts/{account_id}/orders/{client_order_id}`
2. `/management/funding`
3. `/portfolio`

## 10. Successor Change Rule

Any UI successor change must list:

```text
UI Acceptance:
  workbenches_touched:
  routes_touched:
  read_models_used:
  artifacts_or_refs_displayed:
  request_contracts_used:
  data_testids_added:
  positive_ui_acceptance:
  negative_ui_acceptance:
  visual_checks:
  forbidden_wording_scan:
  performance_or_virtualization_checks:
  blockers:
```
