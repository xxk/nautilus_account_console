# P018 Acceptance / 验收基线

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready

## Scope / 范围

This proposal accepts only the read-only IB TWS observation path from owner-produced source package to Account Console UI readback.

It does not accept order actions, broker session ownership, broker truth ownership, live readiness, production readiness, capital allocation, can-trade, or direct TWS connectivity from Account Console.

Implementation/browser evidence is required before implementation closeout. The current `design_gate_ready` status accepts only scope, boundary, UI shape and acceptance design; it does not accept runtime connectivity, source package availability, Account Mirror projection, browser readback or multi-account feature completion.

## Artifact Root Rule

Formal pass evidence must come from the artifact roots declared in [phase-plan.md](phase-plan.md). Template refs, historical IB probe code and external owner docs are not pass evidence unless a same-slice source package and Account Console readback are produced.

## Mandatory Gate Coverage

| Gate | Requirement | Must fail if | Status |
| --- | --- | --- | --- |
| IB-G01-OWNER-RUNTIME-BOUNDARY | TWS / IB Gateway read-only collection is owned outside Account Console | Account Console opens a TWS socket, imports `ibapi`, imports Nautilus IB adapter or accepts TWS credentials | planned |
| IB-G02-SOURCE-PACKAGE | Owner package contains funds, positions, orders, fills when present, owner refs, checksum and redacted metadata | Package missing required fields, stale, checksum mismatch or records raw secrets | planned |
| IB-G03-MIRROR-PROJECTION | IB package projects through Account Mirror canonical contracts | UI/API reads broker-native payload directly or creates IB-specific account truth | planned |
| IB-G03A-FUNDS-OBSERVATION | IB account funds are projected through canonical balance/equity observation fields | Funds are missing, non-numeric, currency-less, timestamp-less, checksum-less, or rendered from broker-native payload without canonical projection | planned |
| IB-G03B-MULTI-CURRENCY-FUNDS | IB multi-currency funds are preserved as per-currency rows plus declared base-currency totals | CNH/HKD/JPY/USD or any returned currency is collapsed into one value, currency labels are missing, FX conversion provenance is absent, or base-currency totals cannot be reconciled | planned |
| IB-G03C-POSITION-OBSERVATION | U3028269 positions are projected through canonical position observation fields | Position rows are missing, broker-native only, non-numeric, market/currency-less, source-less, or not bound to `acct.ib.live.u3028269` | planned |
| IB-G03D-EXECUTION-REPORTS-OBSERVATION | IB execution reports / fills are projected as immutable read-only execution events | Execution reports are missing when owner package declares them, merged into order status only, broker-native only, lack exec/order identity, or lose commission/realized-PnL linkage when provided | planned |
| IB-G04-FAIL-CLOSED | Missing/stale/mismatch package produces typed blocker | UI fabricates funds/positions/orders/execution reports or hides source failure | planned |
| IB-G05-UI-READBACK | Account Console UI matches Account Mirror API for `acct.ib.live.u3028269` | Browser values diverge from API/projection or evidence refs are absent | planned |
| IB-G05A-FUNDS-UI-READBACK | Account Console UI funds summary matches Account Mirror API and owner source package checksum | Any displayed fund value differs from API/projection, required fund field is hidden without blocker, currency/timestamp/checksum is absent, or screenshot is used without API/source comparison | planned |
| IB-G05B-MULTI-CURRENCY-UI-READBACK | Account Console UI displays per-currency funds and base-currency totals consistently with API/source package | UI omits a returned currency, mixes original currency and converted currency without labels, rounds into unreconcilable totals, or hides FX/source provenance | planned |
| IB-G05C-POSITION-UI-READBACK | Account Console UI positions table matches Account Mirror API and owner source package for U3028269 | UI omits a source position, shows extra positions, loses exchange/currency, differs in quantity/avg price/market value/PnL beyond tolerance, or lacks source checksum | planned |
| IB-G05D-TWS-PAGE-SECTION-READBACK | Account Workbench covers the TWS account page sections: account selector, balances, margin requirements, available-for-trading, real FX balances, portfolio, filters and update metadata | Any visible TWS section is not mapped to a UI/API readback row, is collapsed into an unrelated summary, or lacks source/projection evidence | planned |
| IB-G05E-MISSING-UI-REGION-BLOCKER | Missing Account Workbench regions are explicit typed blockers, not silent omissions | A required TWS section has source/API data but no UI region, no blocker marker, no out-of-scope marker, or is still counted as passed | planned |
| IB-G05F-UI-REGION-ARCHITECTURE | Account Workbench UI is split into explicit broker-neutral regions before full TWS coverage closeout | TWS fields are added ad hoc to one dense table, region selectors are missing, or component boundaries allow broker-specific UI truth | planned |
| IB-G05G-EXECUTION-REPORTS-UI-READBACK | Account Workbench displays execution reports / fills as a separate read-only event table with source refs | UI hides execution reports inside orders only, omits returned executions, shows extra executions, loses exec id/order id/perm id/time/price/quantity/currency, or lacks source checksum | planned |
| IB-G06-NO-COMMAND | Commands remain disabled | Submit/cancel/replace/modify/readiness/can-trade controls or labels appear | planned |
| IB-G07-MULTI-ACCOUNT-FABRIC | IB is a peer account under shared Account Mirror contracts | Implementation adds broker-specific UI/API family instead of canonical account capability fields | planned |
| IB-G08-OWNER-TWS-CONNECTIVITY | Owner runtime proves it can connect to local TWS / IB Gateway in read-only mode and materializes a same-slice source package | No same-slice owner connectivity evidence exists, connection evidence is stale, Account Console connects directly, or the package cannot prove account-summary readback | planned |

## Positive-to-Negative Coverage Map

| Positive row | Required negative / anti-drift rows | Coverage rule |
| --- | --- | --- |
| A1 | N1, N2 | IB source package cannot pass if source owner boundary or secret handling fails. |
| A2 | N3, N4 | Account Mirror projection cannot pass if broker-native payload bypasses canonical contracts or fail-closed behavior. |
| A3 | N5, N6 | UI readback cannot pass if it shows command controls, readiness labels or values not derived from API/projection. |

## Scenario Matrix

| ID | Type | Scenario | Verification | Pass signal | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | success | Owner-produced IB source package validates with funds, positions, orders, execution reports/fills and evidence refs | source package validator | `IB_TWS_SOURCE_PACKAGE_OK` | planned |
| A2 | success | Account Mirror projects `acct.ib.live.u3028269` from source package | projection validator/API test | `ACCOUNT_MIRROR_IB_OK` | planned |
| A3 | success | Account Console UI displays funds, positions, orders, execution reports/fills, source health and evidence | browser/API readback | screenshots + readback JSON match | planned |
| A4 | success | Multi-account list includes IB as peer account with command disabled | API/UI test | account appears with observation enabled, command disabled | planned |
| A5 | success | Owner runtime can connect to local TWS / IB Gateway and read account summary without broker mutation | owner command evidence + source package metadata | `IB_TWS_OWNER_CONNECTIVITY_OK` and `raw_secret_values_recorded=false` | planned |
| A6 | success | IB funds validate end to end from owner source package to Account Mirror API to UI | funds source package + projection validator + API/browser readback | `IB_TWS_FUNDS_READBACK_OK` | planned |
| A7 | success | IB multi-currency funds validate per currency and reconcile to declared base-currency totals | multi-currency source package + FX/provenance metadata + API/browser readback | `IB_TWS_MULTI_CURRENCY_FUNDS_OK` | planned |
| A8 | success | U3028269 positions validate end to end from owner source package to Account Mirror API to UI | positions source package + projection validator + API/browser readback | `IB_TWS_POSITIONS_READBACK_OK` | planned |
| A9 | success | Account Workbench readback covers all TWS page sections visible in the design input | section coverage matrix + API/browser selector readback | `IB_TWS_ACCOUNT_WORKBENCH_SECTION_COVERAGE_OK` | planned |
| A10 | success | IB execution reports validate end to end from owner source package to Account Mirror API to a dedicated Account Workbench executions table | executions source package + projection validator + API/browser readback | `IB_TWS_EXECUTION_REPORTS_READBACK_OK` | planned |
| N1 | failure | Account Console attempts direct TWS connection or imports IB broker APIs | source scan / focused test | `direct_tws_connection_rejected` | planned |
| N2 | failure | Source package contains raw endpoint, credential, auth code, client id secret or broker secret | validator | `raw_secret_values_rejected` | planned |
| N3 | failure | Stale/missing/checksum-mismatched package is counted as valid | validator/API test | typed blocker | planned |
| N4 | failure | Broker-native payload is rendered without canonical projection | source/API guard | `broker_native_payload_rejected` | planned |
| N5 | failure | UI shows submit/cancel/replace/modify/order action controls | browser negative test | forbidden controls absent | planned |
| N6 | failure | UI claims can-trade, broker tradable, live ready or production ready | wording scan/browser test | forbidden claims absent | planned |
| N7 | failure | A TCP probe, historical connection, or owner log without same-slice account-summary source package is counted as TWS connectivity acceptance | artifact timestamp/package audit | `same_slice_owner_source_package_required` | planned |
| N8 | failure | UI funds differ from Account Mirror API, package checksum, currency, or collection timestamp | API/browser/source comparison | `funds_readback_mismatch` | planned |
| N9 | failure | Missing funds are rendered as zero or blank without blocker | negative package + browser test | `funds_missing_requires_blocker` | planned |
| N10 | failure | Available funds, net liquidation, cash balance, margin, or excess liquidity are inferred from unrelated fields | projection validator | `funds_field_inference_rejected` | planned |
| N11 | failure | A returned currency row is dropped, merged into another currency, or displayed only in base currency | multi-currency fixture + API/browser comparison | `currency_row_missing_or_collapsed` | planned |
| N12 | failure | Base-currency totals are shown without FX rate, FX timestamp, IB-provided translated field, or source provenance | source/API validator | `fx_provenance_missing` | planned |
| N13 | failure | UI rounds per-currency values or totals beyond declared tolerance | API/browser comparison | `multi_currency_rounding_mismatch` | planned |
| N14 | failure | A source position for U3028269 is missing from UI/API or UI shows a position not in source package | positions source/API/browser comparison | `position_row_mismatch` | planned |
| N15 | failure | Position quantity, average price, market price, market value, unrealized PnL or realized PnL differs beyond declared tolerance | positions readback comparison | `position_numeric_mismatch` | planned |
| N16 | failure | Position row lacks symbol, exchange, asset class, currency, source timestamp or source checksum | source/API validator | `position_provenance_missing` | planned |
| N17 | failure | UI collapses positions across exchanges, currencies, contracts or asset classes under the same display symbol | positions fixture + browser test | `position_identity_collision` | planned |
| N18 | failure | Account Workbench omits balances, margin requirements, available-for-trading, real FX balances, portfolio filters, update time or account type while claiming TWS page coverage | section coverage validator + browser selectors | `tws_section_coverage_missing` | planned |
| N19 | failure | `n/a`, zero and negative values are normalized into the same displayed value | numeric/null semantics validator | `tws_value_semantics_collapsed` | planned |
| N20 | failure | TWS account segment columns such as Total, US Securities, US Commodities and UK Regulated are dropped or merged without labels | API/browser comparison | `tws_segment_columns_missing` | planned |
| N21 | failure | A required UI region is not implemented and Account Workbench neither shows a blocker nor marks the section explicitly out of scope | UI region coverage validator + browser selectors | `ui_region_missing_requires_blocker` | planned |
| N22 | failure | A missing UI region is marked out of scope while source/API fields are in-scope for P018 closeout | acceptance scope audit | `ui_region_out_of_scope_conflict` | planned |
| N23 | failure | UI refactor adds IB-only truth fields outside Account Mirror region contracts | source review + browser/API comparison | `broker_specific_ui_truth_rejected` | planned |
| N24 | failure | Execution reports are rendered only as order status rows, or fills are inferred from order quantity/status without owner execution events | execution package/API/browser comparison | `execution_reports_order_status_collapse_rejected` | planned |
| N25 | failure | Execution report rows lack `exec_id`, order identity, time, side, quantity, price, currency, exchange, source timestamp or source checksum | execution source/API validator | `execution_report_provenance_missing` | planned |
| N26 | failure | UI omits a returned execution, shows an execution not in source package, or loses commission/realized-PnL fields that owner package provided | execution source/API/browser comparison | `execution_report_row_mismatch` | planned |

## UI Anti-Drift Acceptance

| ID | Must fail if | Verification | Expected rejection | Status |
| --- | --- | --- | --- | --- |
| UI-AD-1 | `acct.ib.live.u3028269` UI renders from fixture-only data while claiming live readback | API/browser readback comparison | `fixture_only_cannot_close_live_ib` | planned |
| UI-AD-2 | Old TWS probe success is reused as current source package pass | artifact timestamp/checksum check | `stale_probe_rejected` | planned |
| UI-AD-3 | UI has funds but missing source checksum/evidence refs | browser selector check | `evidence_ref_missing` | planned |
| UI-AD-4 | IB account route hides blocker when package is missing or stale | browser blocker test | `blocker_required` | planned |
| UI-AD-5 | UI shows TWS connected from probe-only evidence instead of owner source package metadata | API/browser readback comparison | `probe_only_connectivity_rejected` | planned |
| UI-AD-6 | UI shows fund values from stale package, fixture-only package, or package without checksum | API/browser/source comparison | `funds_stale_or_unpinned_rejected` | planned |
| UI-AD-7 | UI only shows a single USD total while source package contains multiple currencies | API/browser/source comparison | `multi_currency_detail_required` | planned |
| UI-AD-8 | UI shows U3028269 positions from stale screenshot, fixture-only rows, or source package without checksum | API/browser/source comparison | `positions_stale_or_unpinned_rejected` | planned |
| UI-AD-9 | UI claims full TWS account page coverage from only balances and positions | section coverage matrix | `tws_page_partial_coverage_rejected` | planned |
| UI-AD-10 | UI omits an in-scope section and passes because tests did not look for that region | UI region coverage validator | `missing_ui_region_not_tested_rejected` | planned |
| UI-AD-11 | UI claims order/fill coverage while execution reports are absent, collapsed into order status, or not source-checksum pinned | execution report validator + browser selectors | `execution_reports_required_for_fills_closeout` | planned |

## TWS Account Page Coverage / TWS 账户页覆盖

The screenshot `tws.exe_20260617_164955.png` is a design input for section coverage only. It is not acceptance evidence. Account Workbench acceptance must prove these sections from same-slice source package, Account Mirror API and browser readback.

| TWS section | Account Workbench readback requirement | Required evidence |
| --- | --- | --- |
| account selector | selected canonical account `acct.ib.live.u3028269`, display alias and owner account ref shape | API/browser selector readback |
| base-currency holding value toggle | whether values are original-currency or base-currency translated; UI labels translation mode | source package metadata + UI label |
| simplified/full view mode | UI coverage declares which fields are in compact summary and which are in details | UI design + browser selectors |
| balances | net liquidation, securities gross position value, total cash / cash, monthly interest and segment columns | source/API/browser comparison |
| margin requirements | current initial margin and current maintenance margin with segment columns | source/API/browser comparison |
| available for trading | available funds, excess liquidity and regulatory/exchange margin related fields when provided | source/API/browser comparison |
| real FX balances / market value | per-currency rows, asset-class columns, base-currency total, unrealized/realized PnL and FX provenance | multi-currency source/API/browser comparison |
| portfolio filters | filter text, security type, currency, exchange and show-zero-position state are displayed or explicitly out of scope | browser selector readback |
| portfolio rows | every source position row with symbol, name, exchange, quantity, currency, value, price, average price, unrealized/realized PnL and liquidation flag when provided | positions source/API/browser comparison |
| execution reports / fills | every owner-provided execution event with immutable execution identity, order identity, fill time, side, quantity, price, exchange, currency, commission and realized PnL when provided | execution source/API/browser comparison |
| update metadata | source collection time, UI updated time and account type | source metadata + browser selector readback |

### Segment column requirements

The source package and UI must preserve broker segment columns when provided, including at least:

1. `total`;
2. `us_securities`;
3. `us_commodities`;
4. `uk_regulated`;
5. any additional segment returned by IB.

Segment columns may be collapsed only in a compact summary if the detail view preserves the original segment columns and the UI clearly labels the summary as collapsed.

### Value semantics requirements

Account Workbench must distinguish:

1. `0` as a numeric zero;
2. negative values as real signed values;
3. `n/a` as not available;
4. missing fields as typed blocker or explicit `missing`;
5. rounded display values as display-only values backed by exact API/projection values.

### Additional TWS page fail-closed requirements

TWS page coverage must fail closed if:

1. a visible source section is omitted without an explicit out-of-scope row;
2. segment columns are merged without detail view preservation;
3. `n/a` is displayed as `0` or blank;
4. update time is missing or stale;
5. account type is missing;
6. filter state changes source truth instead of local table display;
7. any readback row lacks source checksum or projection checksum.

## Missing UI Region Policy / Web UI 缺失区域策略

If Account Workbench does not yet have a visible region for an in-scope TWS section, the proposal must not treat that section as passed. The implementation has only three valid choices:

1. implement the UI region and pass API/browser readback;
2. show a typed blocker region with section name, missing UI capability, source/API availability, next action and `status=blocked_missing_ui_region`;
3. mark the section explicitly out of scope for the current phase and remove it from closeout claims.

Silent omission is always a failure.

### Required missing-region blocker fields

| Field | Meaning |
| --- | --- |
| `section_id` | stable section id, such as `margin_requirements` or `real_fx_balances` |
| `section_label` | human-readable Account Workbench label |
| `source_available` | whether owner source package contains the section |
| `api_available` | whether Account Mirror API exposes the section |
| `ui_region_available` | must be `false` for this blocker |
| `blocker_id` | stable blocker id, such as `ib_margin_panel_missing` |
| `next_action` | implementation task required to clear blocker |
| `raw_secret_values_recorded` | must be `false` |

### Required missing-region UI markers

| Section family | Missing UI marker Data Test ID |
| --- | --- |
| balances | `ib-live-balances-region-missing` |
| segment matrix | `ib-live-segment-matrix-region-missing` |
| margin requirements | `ib-live-margin-region-missing` |
| available for trading | `ib-live-available-trading-region-missing` |
| real FX balances | `ib-live-real-fx-region-missing` |
| portfolio filters | `ib-live-portfolio-filter-region-missing` |
| positions | `ib-live-positions-region-missing` |
| execution reports | `ib-live-executions-region-missing` |
| update metadata | `ib-live-update-metadata-region-missing` |

### Missing-region closeout rule

P018 closeout cannot claim full TWS Account Workbench coverage while any required missing-region marker is visible. A phase may close only as partial/blocker-carried if those markers remain.

## Funds Acceptance Design / 资金验收设计

Funds acceptance is an end-to-end readback gate. It cannot pass from a screenshot, a TCP probe, an old owner log, or a mocked Account Console fixture alone.

### Required fund fields

| Field | Meaning | Required source | UI requirement |
| --- | --- | --- | --- |
| `net_liquidation` | account net liquidation / equity value | owner source package | visible or typed blocker |
| `cash_balance` | cash balance by currency | owner source package | visible or typed blocker |
| `available_funds` | available funds / buying power equivalent | owner source package | visible or typed blocker |
| `initial_margin` | initial margin when provided by IB | owner source package | visible or explicitly `not_available` |
| `maintenance_margin` | maintenance margin when provided by IB | owner source package | visible or explicitly `not_available` |
| `excess_liquidity` | excess liquidity when provided by IB | owner source package | visible or explicitly `not_available` |
| `currency` | currency for each money value | owner source package | visible with money values |
| `source_collected_at` | source package collection time | owner source package metadata | visible in source health/evidence |
| `source_checksum` | source package checksum | owner source package metadata | visible in evidence drawer |

### Required multi-currency fields

| Field | Meaning | Required source | UI requirement |
| --- | --- | --- | --- |
| `currency_balances[]` | one row per original currency returned by IB | owner source package | every row visible or explicitly blocked |
| `currency_balances[].currency` | ISO or IB currency code such as `CNH`, `HKD`, `JPY`, `USD` | owner source package | visible on each row |
| `currency_balances[].cash_balance` | original-currency cash balance | owner source package | visible in original currency |
| `currency_balances[].net_liquidation` | original-currency net liquidation when provided | owner source package | visible or `not_available` |
| `currency_balances[].unrealized_pnl` | original-currency unrealized PnL when provided | owner source package | visible or `not_available` |
| `currency_balances[].realized_pnl` | original-currency realized PnL when provided | owner source package | visible or `not_available` |
| `base_currency` | base currency for totals, expected from owner package metadata | owner source package | visible near totals |
| `base_currency_totals` | IB-provided or Account Mirror-projected base-currency totals | owner source package / projection | visible separately from original-currency rows |
| `fx_translation_source` | IB-provided translated values or FX source ref | owner source package metadata | visible in evidence drawer |
| `fx_translation_time` | timestamp for translated totals | owner source package metadata | visible in evidence drawer |
| `fx_tolerance` | accepted numeric comparison tolerance | Account Console validator config | recorded in validator/readback evidence |

### Funds gate chain

1. Owner runtime connects to local TWS / IB Gateway in read-only mode.
2. Owner runtime reads account summary for `acct.ib.live.u3028269`.
3. Owner runtime materializes same-slice source package with fund fields, currency rows, base-currency totals, FX/provenance metadata, source timestamp, checksum and redacted owner refs.
4. Account Console validates the source package and rejects stale/missing/mismatched/secret-leaking packages.
5. Account Mirror projects per-currency fund observations and base-currency totals without broker-specific UI fields.
6. Account Console API returns the same per-currency values, base-currency totals and evidence refs.
7. Browser readback proves visible funds match API/projection, including all currency rows and FX/provenance refs.

### Funds fail-closed requirements

Funds acceptance must fail closed if:

1. the owner package is missing;
2. any required fund field is absent without explicit typed blocker;
3. currency is missing;
4. source timestamp or checksum is missing;
5. source package is stale;
6. UI value differs from API/projection;
7. API/projection value differs from source package;
8. Account Console infers available funds from unrelated fields;
9. Account Console displays zero or blank funds for missing data;
10. source evidence contains raw endpoint, credential, auth code, client secret or broker secret;
11. a currency row is omitted or collapsed into base currency without row-level disclosure;
12. base-currency total is shown without FX/provenance fields;
13. per-currency values and base totals cannot reconcile within declared tolerance.

## forbidden_actions

1. submit order
2. cancel order
3. replace order
4. modify order
5. allocation mutation
6. funding transfer
7. broker session control from Account Console

## forbidden_claims

1. can trade
2. broker tradable
3. live ready
4. production ready
5. capital allocated
6. broker truth accepted by UI

## Evidence

| Evidence | Path or command | Conclusion |
| --- | --- | --- |
| Proposal docs gate | `python scripts/check_proposal_docs.py --root . --proposal-id p018-ib-tws-readonly-account-console` | pending |
| Source package validator | implementation phase command | pending |
| Mirror/API validator | implementation phase command | pending |
| Browser readback | implementation phase command | pending |
| Funds readback validator | `python scripts/validate_ib_tws_funds_readback.py` | pending |
| Multi-currency funds readback validator | `python scripts/validate_ib_tws_multi_currency_funds_readback.py` | pending |
| Positions readback validator | `python scripts/validate_ib_tws_positions_readback.py` | pending |
| TWS page section coverage validator | `python scripts/validate_ib_tws_account_workbench_section_coverage.py` | pending |
| Missing UI region validator | `python scripts/validate_ib_tws_missing_ui_regions.py` | pending |
| UI region architecture validator | `python scripts/validate_ib_tws_ui_region_architecture.py` | pending |
| Execution reports readback validator | `python scripts/validate_ib_tws_execution_reports_readback.py` | pending |

## Position Acceptance Design / 持仓验收设计

U3028269 position acceptance is an end-to-end readback gate. It cannot pass from a TWS screenshot, stale fixture, TCP probe, historical owner log, or UI-only table.

### Required position fields

| Field | Meaning | Required source | UI requirement |
| --- | --- | --- | --- |
| `account_id` | canonical Account Console account id | owner source package / projection | must equal `acct.ib.live.u3028269` |
| `position_uid` | stable row identity derived from account, broker symbol, exchange, contract id or equivalent source identity | Account Mirror projection | not visible unless useful, but required for matching |
| `symbol` | display symbol / contract local symbol | owner source package | visible |
| `description` | instrument name when provided | owner source package | visible or `not_available` |
| `exchange` | exchange / venue, such as SEHK, NASDAQ, NYSE, ARCA or VALUE | owner source package | visible |
| `asset_class` | stock, ETF, option, future or other IB-reported asset class | owner source package | visible or typed blocker |
| `currency` | position currency, such as HKD or USD | owner source package | visible |
| `quantity` | signed or long/short quantity | owner source package | visible |
| `average_price` | average cost / average price | owner source package | visible or `not_available` |
| `market_price` | latest market price when provided | owner source package | visible or `not_available` |
| `market_value` | market value in position currency | owner source package | visible |
| `unrealized_pnl` | unrealized PnL in position currency when provided | owner source package | visible or `not_available` |
| `realized_pnl` | realized PnL in position currency when provided | owner source package | visible or `not_available` |
| `source_collected_at` | source package collection time | owner source package metadata | visible in source health/evidence |
| `source_checksum` | source package checksum | owner source package metadata | visible in evidence drawer |

### Position gate chain

1. Owner runtime connects to local TWS / IB Gateway in read-only mode.
2. Owner runtime reads positions / portfolio rows for U3028269 without broker mutation.
3. Owner runtime materializes same-slice source package with positions, instrument identity, quantities, prices, values, PnL, currency, exchange, timestamp, checksum and redacted owner refs.
4. Account Console validates the package and rejects stale/missing/mismatched/secret-leaking packages.
5. Account Mirror projects positions into canonical rows keyed by stable `position_uid`.
6. Account Console API returns the same position rows and evidence refs.
7. Browser readback proves visible position rows match API/projection/source package.

### Position fail-closed requirements

Position acceptance must fail closed if:

1. source package is missing;
2. position rows are missing while owner package claims positions are present;
3. a position row lacks symbol, exchange, currency, quantity, market value, source timestamp or checksum;
4. UI/API row count differs from source package after documented filtering;
5. quantity, average price, market price, market value or PnL differs beyond declared tolerance;
6. positions from different exchanges, currencies, contracts or asset classes are merged under one display row;
7. UI hides negative/short quantity, option/future identity or non-stock asset class;
8. Account Console infers prices or PnL from unrelated fields;
9. a stale screenshot or fixture-only table is counted as live U3028269 position acceptance;
10. source evidence contains raw endpoint, credential, auth code, client secret or broker secret.

## Execution Reports Acceptance Design / 成交回报验收设计

Execution reports are immutable fill events. They are not the same object as orders, open order status or position rows. P018 must treat them as a separate read-only event stream from owner source package to Account Mirror API to Account Workbench UI.

This gate accepts only readback. It does not authorize order submit, cancel, replace, allocation mutation or broker session control.

### Required execution report fields

| Field | Meaning | Required source | UI requirement |
| --- | --- | --- | --- |
| `account_id` | canonical Account Console account id | owner source package / projection | must equal `acct.ib.live.u3028269` |
| `execution_uid` | stable Account Mirror execution row identity | Account Mirror projection | required for matching |
| `exec_id` | IB execution id or equivalent owner-provided execution identity | owner source package | visible or visible in row details |
| `order_id` | broker order id when provided | owner source package | visible or `not_available` |
| `perm_id` | IB permanent order id when provided | owner source package | visible or `not_available` |
| `symbol` | execution instrument symbol / local symbol | owner source package | visible |
| `side` | buy/sell or equivalent side | owner source package | visible |
| `quantity` | filled quantity for this execution event | owner source package | visible |
| `price` | execution price | owner source package | visible |
| `exchange` | execution venue / exchange when provided | owner source package | visible or `not_available` |
| `currency` | execution currency | owner source package | visible |
| `execution_time` | broker execution timestamp | owner source package | visible |
| `commission` | commission report amount when provided | owner source package / commission report join | visible or `not_available` |
| `realized_pnl` | realized PnL from commission report when provided | owner source package / commission report join | visible or `not_available` |
| `source_collected_at` | source package collection time | owner source package metadata | visible in source health/evidence |
| `source_checksum` | source package checksum | owner source package metadata | visible in evidence drawer |

### Execution reports gate chain

1. Owner runtime connects to local TWS / IB Gateway in read-only mode.
2. Owner runtime requests execution reports and commission reports for the accepted account/time window without broker mutation.
3. Owner runtime materializes same-slice source package with execution rows, optional commission joins, timestamp, checksum and redacted owner refs.
4. Account Console validates the package and rejects stale/missing/mismatched/secret-leaking packages.
5. Account Mirror projects executions into immutable canonical execution events keyed by stable `execution_uid`.
6. Account Console API returns the same execution rows and evidence refs.
7. Browser readback proves the Account Workbench executions table matches API/projection/source package.

### Execution reports fail-closed requirements

Execution reports acceptance must fail closed if:

1. owner source package declares execution reports are available but the execution array is missing;
2. execution rows are inferred from order status, positions or aggregate filled quantity;
3. an execution row lacks `exec_id`, instrument identity, side, quantity, price, currency, execution time, source timestamp or checksum;
4. UI/API row count differs from source package after documented time-window filtering;
5. quantity, price, commission or realized PnL differs beyond declared tolerance;
6. executions from different order ids, perm ids, symbols, exchanges or currencies are merged under one display row;
7. UI hides commission or realized PnL when owner package provided them;
8. a stale screenshot, fixture-only table or historical TWS log is counted as current execution report acceptance;
9. source evidence contains raw endpoint, credential, auth code, client secret or broker secret;
10. UI shows any action control next to execution rows.
