# P018 UI Design / UI 设计

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready

## Surface / 界面

P018 extends existing Account Workbench surfaces instead of creating a broker-specific page family.

Routes:

1. `/accounts`
2. `/accounts/acct.ib.live.u3028269`
3. `/accounts/acct.ib.live.u3028269/positions`
4. `/accounts/acct.ib.live.u3028269/orders`
5. `/accounts/acct.ib.live.u3028269/executions`

## Account Summary Layout

The IB account detail route shows:

1. account identity: canonical id, display alias, source type and observation status;
2. capability badges: observation enabled, command disabled, reconciliation pending/blocked as applicable;
3. funds summary: net liquidation / equity, cash, margin, available funds, currency;
4. position summary: instrument, asset class, quantity, average price, market price, market value, unrealized PnL;
5. order readback: open orders and order status when present;
6. execution report readback: immutable execution/fill events and commission report joins when present;
7. source health strip: collected time, staleness, owner package checksum, blocker state;
8. evidence drawer: owner repo ref, owner entrypoint ref, owner config ref, package checksum, projection checksum.

## Data Test ID

| Element | Data Test ID |
| --- | --- |
| account route shell | `account-workbench-ib-live-route` |
| account summary card | `ib-live-account-summary` |
| funds summary | `ib-live-funds-summary` |
| positions table | `ib-live-positions-table` |
| orders table | `ib-live-orders-table` |
| execution reports table | `ib-live-executions-table` |
| capability badge group | `ib-live-capability-badges` |
| source health strip | `ib-live-source-health` |
| evidence drawer trigger | `ib-live-evidence-drawer-trigger` |
| blocker row | `ib-live-blocker` |

## TWS Page Section Mapping / TWS 页面分区映射

Account Workbench should expose the TWS account page as read-only account sections. The UI may be more compact than TWS, but it must preserve section identity, labels, source refs and detail access.

| TWS section | Account Workbench section | Data Test ID |
| --- | --- | --- |
| selected account | account identity header | `ib-live-selected-account` |
| account type / update time | source metadata strip | `ib-live-update-metadata` |
| base-currency display toggle | translation mode badge | `ib-live-translation-mode` |
| simplified/full view mode | compact/detail mode control | `ib-live-view-mode` |
| balances | balances panel | `ib-live-balances-panel` |
| balance segment columns | balance segment matrix | `ib-live-balance-segment-matrix` |
| margin requirements | margin requirements panel | `ib-live-margin-panel` |
| available for trading | available-for-trading panel | `ib-live-available-trading-panel` |
| real FX balances / market value | multi-currency market value panel | `ib-live-real-fx-market-value-panel` |
| portfolio filters | portfolio filter bar | `ib-live-portfolio-filter-bar` |
| portfolio table | positions table | `ib-live-positions-table` |
| executions / fills | execution reports table | `ib-live-executions-table` |

## Segment Matrix Fields / 分段矩阵字段

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| Total segment | `ib-live-segment-total` | `segments.total` |
| US Securities segment | `ib-live-segment-us-securities` | `segments.us_securities` |
| US Commodities segment | `ib-live-segment-us-commodities` | `segments.us_commodities` |
| UK Regulated segment | `ib-live-segment-uk-regulated` | `segments.uk_regulated` |
| additional segment | `ib-live-segment-extra` | `segments.*` |

## Available-For-Trading Fields / 可交易资金字段

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| available funds | `ib-live-available-funds` | `available_for_trading.available_funds` |
| excess liquidity | `ib-live-excess-liquidity` | `available_for_trading.excess_liquidity` |
| SMA / special memorandum account | `ib-live-sma` | `available_for_trading.sma` |
| regulatory / exchange margin cushion | `ib-live-margin-cushion` | `available_for_trading.margin_cushion` |

## Margin Requirement Fields / 保证金字段

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| current initial margin | `ib-live-current-initial-margin` | `margin_requirements.current_initial_margin` |
| current maintenance margin | `ib-live-current-maintenance-margin` | `margin_requirements.current_maintenance_margin` |

## Funds Summary Fields / 资金摘要字段

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| Net liquidation | `ib-live-funds-net-liquidation` | `funds.net_liquidation` |
| Cash balance | `ib-live-funds-cash-balance` | `funds.cash_balance` |
| Available funds | `ib-live-funds-available` | `funds.available_funds` |
| Initial margin | `ib-live-funds-initial-margin` | `funds.initial_margin` |
| Maintenance margin | `ib-live-funds-maintenance-margin` | `funds.maintenance_margin` |
| Excess liquidity | `ib-live-funds-excess-liquidity` | `funds.excess_liquidity` |
| Currency | `ib-live-funds-currency` | `funds.currency` |
| Funds source timestamp | `ib-live-funds-source-time` | `source_collected_at` |
| Funds source checksum | `ib-live-funds-source-checksum` | `source_checksum` |

## Multi-Currency Funds Fields / 多币种资金字段

The TWS account window may expose original-currency rows such as `CNH`, `HKD`, `JPY` and `USD`, plus a base-currency total row. Account Console must preserve this shape instead of rendering only a single converted total.

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| currency funds table | `ib-live-currency-funds-table` | `currency_balances[]` |
| currency code | `ib-live-currency-code` | `currency_balances[].currency` |
| original-currency cash | `ib-live-currency-cash-balance` | `currency_balances[].cash_balance` |
| original-currency net liquidation | `ib-live-currency-net-liquidation` | `currency_balances[].net_liquidation` |
| original-currency unrealized PnL | `ib-live-currency-unrealized-pnl` | `currency_balances[].unrealized_pnl` |
| original-currency realized PnL | `ib-live-currency-realized-pnl` | `currency_balances[].realized_pnl` |
| base currency | `ib-live-base-currency` | `base_currency` |
| base-currency total net liquidation | `ib-live-base-total-net-liquidation` | `base_currency_totals.net_liquidation` |
| base-currency total cash | `ib-live-base-total-cash-balance` | `base_currency_totals.cash_balance` |
| FX translation source | `ib-live-fx-source` | `fx_translation_source` |
| FX translation time | `ib-live-fx-time` | `fx_translation_time` |
| FX comparison tolerance | `ib-live-fx-tolerance` | `fx_tolerance` |

## Position Table Fields / 持仓表字段

The U3028269 TWS position table may contain HK and US equities, ETFs, options or other IB contract types. Account Console must preserve contract identity, exchange and currency; display symbol alone is not a stable identity.

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| positions table | `ib-live-positions-table` | `positions[]` |
| position row | `ib-live-position-row` | `positions[]` |
| position identity | `ib-live-position-uid` | `positions[].position_uid` |
| symbol | `ib-live-position-symbol` | `positions[].symbol` |
| description | `ib-live-position-description` | `positions[].description` |
| exchange | `ib-live-position-exchange` | `positions[].exchange` |
| asset class | `ib-live-position-asset-class` | `positions[].asset_class` |
| currency | `ib-live-position-currency` | `positions[].currency` |
| quantity | `ib-live-position-quantity` | `positions[].quantity` |
| average price | `ib-live-position-average-price` | `positions[].average_price` |
| market price | `ib-live-position-market-price` | `positions[].market_price` |
| market value | `ib-live-position-market-value` | `positions[].market_value` |
| unrealized PnL | `ib-live-position-unrealized-pnl` | `positions[].unrealized_pnl` |
| realized PnL | `ib-live-position-realized-pnl` | `positions[].realized_pnl` |
| position source timestamp | `ib-live-position-source-time` | `source_collected_at` |
| position source checksum | `ib-live-position-source-checksum` | `source_checksum` |

## Execution Reports Fields / 成交回报字段

Execution reports are immutable fill events. They must be shown as a separate Account Workbench region and cannot be inferred from order status, aggregate filled quantity or position deltas.

| UI label | Data Test ID | Source field |
| --- | --- | --- |
| executions table | `ib-live-executions-table` | `executions[]` |
| execution row | `ib-live-execution-row` | `executions[]` |
| execution identity | `ib-live-execution-uid` | `executions[].execution_uid` |
| exec id | `ib-live-execution-exec-id` | `executions[].exec_id` |
| order id | `ib-live-execution-order-id` | `executions[].order_id` |
| perm id | `ib-live-execution-perm-id` | `executions[].perm_id` |
| symbol | `ib-live-execution-symbol` | `executions[].symbol` |
| side | `ib-live-execution-side` | `executions[].side` |
| filled quantity | `ib-live-execution-quantity` | `executions[].quantity` |
| execution price | `ib-live-execution-price` | `executions[].price` |
| exchange | `ib-live-execution-exchange` | `executions[].exchange` |
| currency | `ib-live-execution-currency` | `executions[].currency` |
| execution time | `ib-live-execution-time` | `executions[].execution_time` |
| commission | `ib-live-execution-commission` | `executions[].commission` |
| realized PnL | `ib-live-execution-realized-pnl` | `executions[].realized_pnl` |
| execution source timestamp | `ib-live-execution-source-time` | `source_collected_at` |
| execution source checksum | `ib-live-execution-source-checksum` | `source_checksum` |

## States / 状态

1. `source_ready`: owner package valid, projection ready, UI values match API.
2. `source_missing`: no package, UI shows blocker and no fabricated values.
3. `source_stale`: package exists but outside accepted freshness window.
4. `source_checksum_mismatch`: package checksum does not match metadata.
5. `schema_mismatch`: package cannot validate.
6. `command_disabled`: observation is visible but order controls are absent.
7. `funds_missing`: funds package is missing or incomplete; UI shows blocker and does not render zero/blank inferred values.
8. `funds_mismatch`: API/projection/source values differ; UI shows blocker until resolved.
9. `currency_row_missing`: source package has a currency row that UI/API does not expose.
10. `fx_provenance_missing`: base-currency totals exist but FX/provenance metadata is absent.
11. `positions_missing`: source package is missing position rows or Account Mirror cannot project them; UI shows blocker instead of an empty table unless owner package explicitly says no positions.
12. `position_mismatch`: API/projection/source position rows differ; UI shows blocker until resolved.
13. `position_identity_collision`: two broker positions would collapse into one display row; UI blocks until stable identity is available.
14. `section_coverage_missing`: a TWS page section is present in source package but not shown or explicitly blocked in Account Workbench.
15. `value_semantics_mismatch`: `0`, negative, `n/a`, missing and rounded display values are not distinguishable.
16. `execution_reports_missing`: owner package declares execution reports are available but UI/API has no execution report rows or typed blocker.
17. `execution_order_status_collapse`: execution reports are displayed only as order status or inferred fills.
18. `execution_report_mismatch`: UI/API execution rows differ from source package.

## Interaction Rules / 交互规则

1. Evidence drawer may open source refs and checksums.
2. Table filtering/sorting is allowed for local projection rows.
3. Navigation between summary, positions, orders and executions is allowed.
4. No UI element may initiate broker login, TWS reconnect, order submit, order cancel, order replace, order modify, funding transfer or allocation mutation.

## Execution Reports Region / 成交回报区域

The compact account route may show a recent executions slice. The detail route must preserve immutable event identity, order identity, source timestamp and checksum. If the owner source package has no execution report support yet, the UI must show `ib-live-executions-region-missing` or a typed blocker with `blocker_id=ib_execution_reports_missing`; empty whitespace is not acceptable.
