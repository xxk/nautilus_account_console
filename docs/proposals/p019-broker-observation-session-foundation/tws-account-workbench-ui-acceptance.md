# P019 TWS Account Workbench UI Acceptance / TWS Account Workbench UI 验收

- Proposal ID: `p019-broker-observation-session-foundation`
- Slice: `tws_account_workbench_u3028269_ui`
- Status: planned
- Date: 2026-06-20
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)
- Parent slice: [TWS today slice acceptance](./tws-today-slice-acceptance.md)

## 1. UI Target / UI 目标

Account Workbench must display the TWS account `U3028269` through Account Console Web UI as a read-only observed account.

Canonical Account Console identity:

```text
account_id: acct.ib.live.u3028269
display_alias: U3028269
source_kind: ib_tws_observation
route: /accounts/acct.ib.live.u3028269
positions_route: /accounts/acct.ib.live.u3028269/positions
```

The UI acceptance must open the Web UI and verify the Account Workbench route. API-only or fixture-only evidence cannot close this UI slice.

## 2. Required Visible Information / 必须显示的信息

| Area | Required UI content | Acceptance notes |
| --- | --- | --- |
| Account identity | Account Workbench title/context shows `acct.ib.live.u3028269` and display alias `U3028269` | Must not expose raw broker secrets or hidden account credentials |
| Source state | TWS observation state, source health, freshness and blocker if not connected | Missing source must show typed blocker, not blank success |
| Funds table | Funds must render as a table, not only metric cards: currency, cash, available, buying power, margin, equity/net liquidation, unrealized PnL where provided | Table rows must carry source/projection refs |
| Multi-currency funds | One table row per returned TWS currency, plus a clearly separated base-currency rollup row/section when available | USD/CNY/HKD/etc. must not be silently collapsed into one number |
| FX/provenance | FX translation source/timestamp/tolerance when base-currency totals are shown | If FX provenance is missing, base-currency rollup must be blocked or marked partial |
| Positions | Every TWS position row with instrument, asset class/exchange where available, currency, qty, avg price, market price, market value and PnL | Empty table cannot mean no broker positions unless source explicitly proves empty |
| Orders and fills | Observed orders/fills available through order/report sections when source provides them | Must use Nautilus-compatible reports, not raw broker payload as truth |
| Execution Reports table | Execution reports must render as a table, not cards/free text: report type, report id, client order id, venue order id, instrument, side, status/trade id, order status, quantity, filled quantity, remaining quantity, limit/stop price, avg/last fill price, timestamp, sequence/cursor and source/provenance | Required for post-session review and parity against normalized reports |
| Execution Reports table controls | Table must provide stable sort/filter/readback behavior for report type, order id, instrument, status/trade id and timestamp without changing the underlying normalized report rows | Required for high-frequency test review; filtering cannot hide loss of source rows in parity evidence |
| Evidence | Source ref, projection checksum, observed/received/projected timestamps | Screenshot alone cannot prove account truth |
| Command state | Read-only / command disabled state | No submit/cancel/replace/modify controls |

## 3. Browser Acceptance Matrix / 浏览器验收矩阵

| ID | Requirement | Browser action | Must fail if | Evidence |
| --- | --- | --- | --- | --- |
| UI-TWS-01 | Account Workbench route opens for U3028269 | Open `/accounts/acct.ib.live.u3028269` in Web UI | route redirects to demo account or disconnected page | Playwright screenshot + route assertion |
| UI-TWS-02 | Account identity is visible | Assert page contains `Account Workbench`, `acct.ib.live.u3028269`, `U3028269` | raw broker secret/account credential is rendered | Playwright text/testid assertion |
| UI-TWS-03 | Funds table visible | Assert funds table renders columns for currency, cash, available, buying power, margin and equity/net liquidation where provided | funds are only shown as metric cards like Cash/Available/Buying power | Playwright locator assertion |
| UI-TWS-04 | Multi-currency funds visible | Assert original-currency table has one row per source currency | currencies are collapsed into base currency without original rows | Playwright table-row assertion |
| UI-TWS-05 | Base currency rollup is provenanced | Assert base-currency total has FX/provenance marker or blocker | base total appears with no FX source/timestamp/tolerance | Playwright assertion |
| UI-TWS-06 | Positions visible | Open `/accounts/acct.ib.live.u3028269/positions`; assert positions table rows match source count or typed empty proof | empty positions table appears without source proof | Playwright row-count/source assertion |
| UI-TWS-07 | Position fields complete | Assert each visible position row has instrument, currency, qty, price/value/PnL fields where provided | row drops currency or value semantics | Playwright table-cell assertion |
| UI-TWS-08 | Source health and freshness visible | Assert source health, observed/received/projected timestamps and staleness state are visible | page claims realtime without freshness fields | Playwright text/testid assertion |
| UI-TWS-09 | Evidence visible | Assert source ref/checksum/projection ref are visible in evidence/source area | screenshot-only page has no provenance | Playwright assertion |
| UI-TWS-10 | No command controls | Assert no submit/cancel/replace/modify controls are present | any order action control appears | Playwright negative assertion |
| UI-TWS-11 | Missing source blocks correctly | Force/mock missing TWS source and open route | page shows healthy zero balances/positions | Playwright blocked-state assertion |
| UI-TWS-12 | Responsive coverage | Open desktop, tablet and mobile widths | text overlaps, tables become unreadable, source/evidence disappears | screenshots for each viewport |
| UI-TWS-13 | Web UI vs TWS API funds parity | Compare every rendered funds table value against the same-slice TWS API/source package normalized payload | UI value differs from TWS API payload, drops a currency row, silently rounds away material precision, or lacks provenance | Playwright UI readback + API/source parity artifact |
| UI-TWS-14 | Web UI vs TWS API positions parity | Compare every rendered position row against the same-slice TWS API/source package normalized payload | UI drops a position, changes sign/quantity/currency/value/PnL semantics, or invents an empty row | Playwright UI readback + API/source parity artifact |
| UI-TWS-15 | Web UI vs TWS API orders/fills parity | Compare visible order/fill report rows against Nautilus-compatible reports derived from TWS API/callback payloads | UI parses raw payload directly, loses client/venue order id, or shows lifecycle state not present in normalized report | Playwright UI readback + API/source parity artifact |
| UI-TWS-16 | Execution Reports table visible | Assert execution reports render as a table with stable columns for report type, ids, instrument, status/trade, quantity, price, timestamp and provenance | reports render only as cards/free text or raw payload dump | Playwright table/column assertion |
| UI-TWS-17 | Execution Reports table parity | Compare every execution report table row to the Nautilus-compatible `OrderStatusReport` / `FillReport` source rows | table drops report rows, merges order/fill semantics incorrectly, or loses report id/provenance | Playwright UI readback + report parity artifact |
| UI-TWS-18 | Execution Reports table persistence parity | Restart/reload Account Console and assert the table can be rebuilt from the durable observation store for the same account/order scope | table only contains startup callback data or loses rows after process restart | persistence reload + Playwright row parity artifact |
| UI-TWS-19 | Execution Reports empty/partial states | Open an account/order scope with no reports, stale reports or replay gaps | empty table is shown as healthy complete history without source proof or typed blocker | Playwright blocked/empty-state assertion |

## 4. Required Web UI Verification / 必须打开 Web UI 验收

At implementation closeout, verification must open the Account Workbench Web UI:

```text
http://127.0.0.1:5175/accounts/acct.ib.live.u3028269
http://127.0.0.1:5175/accounts/acct.ib.live.u3028269/positions
```

If the dev server uses another port, the evidence must record the actual URL. The evidence must include:

1. Browser route URL.
2. Screenshot path for desktop/tablet/mobile.
3. API payload checksum or projection checksum used by the UI.
4. Source package / observation package ref.
5. Negative assertion that command controls are absent.
6. Negative assertion that raw secrets are absent.
7. TWS API/source package payload ref used for parity.
8. Machine-readable parity result comparing Web UI rendered values to TWS API/source package values.

## 5. Suggested Playwright Assertions / 建议 Playwright 断言

```text
page.goto("/accounts/acct.ib.live.u3028269")
expect(page.getByRole("heading", { name: /Account Workbench/i })).toBeVisible()
expect(page.getByText("acct.ib.live.u3028269")).toBeVisible()
expect(page.getByText("U3028269")).toBeVisible()
expect(page.getByTestId("tws-multi-currency-funds-table")).toBeVisible()
expect(page.getByTestId("tws-execution-reports-table")).toBeVisible()
expect(page.getByTestId("account-readback-mode")).toContainText(/mirror API|Account Mirror/i)
expect(page.getByTestId("account-summary-source-ref").first()).toBeVisible()
expect(page.getByText(/submit|cancel|replace|modify/i)).not.toBeVisible()
```

For multi-currency funds, the final implementation must add stable test ids such as:

```text
tws-multi-currency-funds-table
tws-currency-balance-row
tws-base-currency-rollup
tws-fx-provenance
```

The existing metric-strip-only pattern:

```text
Cash
Available
Buying power
Margin
Unrealized PnL
```

is not sufficient for U3028269 acceptance because it cannot represent multiple original-currency rows. It may remain as a compact summary above the table, but the table is the acceptance surface.

For execution reports, the final implementation must add stable test ids such as:

```text
tws-execution-reports-table
tws-execution-report-row
tws-execution-report-type
tws-execution-report-provenance
tws-execution-report-client-order-id
tws-execution-report-venue-order-id
tws-execution-report-sequence
tws-execution-report-source-ref
tws-execution-report-empty-state
tws-execution-report-blocker
```

The execution report table is the acceptance surface for order/fill report review. Raw payload drawers may exist as drill-down evidence, but they cannot replace the normalized table.

Required columns:

```text
report_type
report_id
client_order_id
venue_order_id
instrument_id
side
order_status_or_trade_id
quantity
filled_quantity
remaining_quantity
limit_or_stop_price
avg_or_last_fill_price
event_timestamp
observed_timestamp
sequence_or_cursor
source_ref
```

Required behavior:

1. Default sort is deterministic by source sequence/cursor when available, otherwise by event timestamp and report id.
2. User sorting/filtering must not mutate the underlying parity row set.
3. `OrderStatusReport` and `FillReport` rows may share one table only if `report_type` remains explicit and row semantics are not merged.
4. Empty history requires source proof; partial or replay-gapped history requires a typed blocker.
5. Reloaded rows must come from the durable observation store or Account Mirror projection backed by that store, not only from live callback memory.

## 6. UI/API Parity Rule / UI 与 TWS API 对比规则

The final UI acceptance must compare rendered Web UI values against the same-slice TWS API return or owner-produced normalized source package. Account Mirror projection can be an intermediate layer, but UI-only rendering or API-only shape is not sufficient.

Required parity checks:

1. Funds table row count equals TWS returned currency row count.
2. Each currency row matches TWS normalized fields: currency, cash, available, buying power, margin, equity/net liquidation and unrealized PnL where provided.
3. Base-currency rollup matches the source package rollup and carries FX/provenance metadata.
4. Positions table row count equals TWS normalized positions count.
5. Each position matches instrument, asset class/exchange where available, currency, quantity, average price, market price, market value and PnL.
6. Orders/fills visible in UI match Nautilus-compatible reports derived from TWS callbacks/source package.
7. Execution Reports table row count equals normalized `OrderStatusReport` + `FillReport` row count for the selected account/order scope.
8. Each Execution Reports table row preserves report id, report type, client order id, venue order id, instrument, side, status or trade id, quantity/fill quantity, price/avg/last price, timestamp and provenance.
9. Execution Reports table order is deterministic and backed by sequence/cursor or timestamp/report id fallback.
10. Execution Reports table reload after process restart matches durable observation store rows for the selected account/order scope.
11. Any missing source section must show a typed blocker instead of passing parity with blanks or zeros.

Parity evidence must be machine-readable and include:

```text
ui_route
tws_source_payload_ref
tws_source_checksum
account_mirror_projection_checksum
ui_render_checksum_or_screenshot_ref
funds_parity: pass | blocked | fail
positions_parity: pass | blocked | fail
orders_fills_parity: pass | blocked | fail
execution_reports_table_parity: pass | blocked | fail
execution_reports_persistence_parity: pass | blocked | fail
raw_secret_values_recorded=false
```

## 7. Closeout Rule / 收口规则

This UI slice cannot close from API tests alone. It closes only when UI-TWS-01 through UI-TWS-19 pass or produce typed blockers, browser evidence opens Account Workbench for `acct.ib.live.u3028269`, and machine-readable parity evidence compares Web UI rendered values against TWS API/source package values.

## 8. Current Baseline / 当前基线

Baseline probe on 2026-06-20 opened:

```text
http://127.0.0.1:5175/accounts/acct.ib.live.u3028269
```

Observed baseline state:

1. Web UI route responds and renders Account Workbench.
2. Page content falls back to `acct.demo-19053` deterministic fixture.
3. `acct.ib.live.u3028269` and display alias `U3028269` are not visible.
4. No command words were detected in the rendered body.
5. Screenshot evidence path:

```text
output/debug/p019-tws-ui-baseline/acct-ib-live-u3028269-desktop.png
```

This baseline does not pass UI-TWS-01, UI-TWS-02, UI-TWS-13, UI-TWS-14, UI-TWS-15, UI-TWS-16, UI-TWS-17, UI-TWS-18 or UI-TWS-19. It is a blocker/starting point for the implementation slice, not acceptance evidence.
