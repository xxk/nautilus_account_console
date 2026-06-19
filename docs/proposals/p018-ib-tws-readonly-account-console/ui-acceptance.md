# P018 UI Acceptance / UI 验收

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready

## Browser Acceptance

| ID | Scenario | Required evidence | Status |
| --- | --- | --- | --- |
| B1 | `/accounts` lists `acct.ib.live.u3028269` as IB live observation account | desktop/tablet/mobile screenshot + API readback | planned |
| B2 | IB account summary displays funds and capability badges | browser screenshot + selector readback | planned |
| B3 | IB positions route displays canonical positions table | browser screenshot + API comparison | planned |
| B4 | IB orders route displays read-only open orders and order status when present | browser screenshot + API comparison | planned |
| B5 | source health and evidence drawer show owner refs and checksums | browser screenshot + selector readback | planned |
| B6 | missing/stale/mismatch source package displays blocker state | browser screenshot + negative fixture | planned |
| B7 | UI shows TWS connectivity as connected only when source package metadata carries same-slice owner connectivity evidence | browser screenshot + API/source package comparison | planned |
| B8 | UI funds summary displays net liquidation, cash, available funds, margin fields, excess liquidity, currency, source timestamp and checksum | browser selector readback + API/source package comparison | planned |
| B9 | UI multi-currency funds table displays every returned currency row, original-currency values, base-currency totals and FX/provenance refs | browser selector readback + API/source package comparison | planned |
| B10 | UI positions table displays every U3028269 source position with symbol, description, exchange, asset class, currency, quantity, prices, value, PnL and source refs | browser selector readback + API/source package comparison | planned |
| B11 | UI Account Workbench covers TWS page sections: selected account, balances, margin, available-for-trading, real FX balances, portfolio filters, update metadata and account type | section coverage screenshot + API/source package comparison | planned |
| B12 | UI preserves segment columns such as Total, US Securities, US Commodities and UK Regulated in detail view | browser selector readback + API/source package comparison | planned |
| B13 | UI distinguishes zero, negative, `n/a`, missing and rounded display values | negative fixture + browser selector readback | planned |
| B14 | Missing in-scope UI regions display typed blocker markers instead of silent omissions | browser selector readback + blocker payload comparison | planned |
| B15 | UI execution reports route displays immutable read-only execution/fill events with exec id, order identity, time, side, quantity, price, exchange, currency, commission and realized PnL when present | browser selector readback + API/source package comparison | planned |

## Negative UI Acceptance

| ID | Must fail if | Required rejection | Status |
| --- | --- | --- | --- |
| NUI1 | submit/cancel/replace/modify controls appear | forbidden controls absent | planned |
| NUI2 | UI displays can-trade, broker tradable, live ready or production ready | forbidden claims absent | planned |
| NUI3 | UI displays funds/positions without package checksum and projection checksum | `evidence_ref_missing` blocker | planned |
| NUI4 | UI hides missing or stale source package state | `ib-live-blocker` visible | planned |
| NUI5 | UI renders broker-native fields not mapped into canonical Account Mirror response | `broker_native_payload_rejected` | planned |
| NUI6 | UI shows connected from TCP probe-only or historical evidence without same-slice source package | `probe_only_connectivity_rejected` | planned |
| NUI7 | UI renders missing funds as zero or blank without blocker | `funds_missing_requires_blocker` | planned |
| NUI8 | UI fund value differs from API/projection/source package | `funds_readback_mismatch` | planned |
| NUI9 | UI collapses CNH/HKD/JPY/USD or any returned currency rows into one base-currency total | `multi_currency_detail_required` | planned |
| NUI10 | UI shows base-currency total without FX translation source, timestamp and tolerance | `fx_provenance_missing` | planned |
| NUI11 | UI omits a U3028269 source position or shows a position not present in source package | `position_row_mismatch` | planned |
| NUI12 | UI position quantity, price, market value or PnL differs from API/projection/source package | `position_numeric_mismatch` | planned |
| NUI13 | UI collapses positions across exchange, currency, contract or asset class under one display symbol | `position_identity_collision` | planned |
| NUI14 | UI shows empty positions table while source package is missing or stale | `positions_missing_requires_blocker` | planned |
| NUI15 | UI omits a TWS source section while claiming full Account Workbench coverage | `tws_section_coverage_missing` | planned |
| NUI16 | UI drops or merges segment columns without detail view preservation | `tws_segment_columns_missing` | planned |
| NUI17 | UI displays `n/a` as zero, hides negative values, or rounds values beyond declared tolerance | `tws_value_semantics_collapsed` | planned |
| NUI18 | UI filter controls mutate source truth or hide rows without disclosing filter state | `portfolio_filter_state_untracked` | planned |
| NUI19 | Required source/API section has no visible UI region and no typed missing-region blocker | `ui_region_missing_requires_blocker` | planned |
| NUI20 | UI shows missing-region blocker but still marks section or proposal as passed | `missing_ui_region_blocks_closeout` | planned |
| NUI21 | UI collapses execution reports into order status or infers fills from order quantity/status | `execution_reports_order_status_collapse_rejected` | planned |
| NUI22 | UI omits a returned execution, shows extra executions, or hides execution identity/source checksum | `execution_report_row_mismatch` | planned |
| NUI23 | UI displays execution rows with submit/cancel/replace/modify controls nearby | `execution_report_actions_forbidden` | planned |

## Blocker

Required blocker states:

1. `ib_source_package_missing`
2. `ib_source_package_stale`
3. `ib_source_package_checksum_mismatch`
4. `ib_source_package_schema_mismatch`
5. `ib_owner_runtime_unavailable`
6. `ib_secret_ref_missing`
7. `ib_command_capability_disabled`
8. `ib_funds_missing`
9. `ib_funds_stale`
10. `ib_funds_readback_mismatch`
11. `ib_currency_row_missing`
12. `ib_fx_provenance_missing`
13. `ib_multi_currency_rounding_mismatch`
14. `ib_positions_missing`
15. `ib_position_row_mismatch`
16. `ib_position_numeric_mismatch`
17. `ib_position_identity_collision`
18. `ib_tws_section_coverage_missing`
19. `ib_tws_segment_columns_missing`
20. `ib_tws_value_semantics_collapsed`
21. `ib_portfolio_filter_state_untracked`
22. `ib_ui_region_missing`
23. `ib_missing_ui_region_blocks_closeout`
24. `ib_execution_reports_missing`
25. `ib_execution_report_row_mismatch`
26. `ib_execution_order_status_collapse`

## Screenshot Requirements

1. desktop viewport for summary and blocker state;
2. tablet viewport for positions;
3. mobile viewport for summary/source health;
4. desktop or wide viewport for multi-currency funds table when more than three currencies are present;
5. desktop or wide viewport for U3028269 positions when multiple exchanges/currencies are present;
6. desktop or wide viewport for segment matrix and real FX balances;
7. desktop or wide viewport for execution reports when executions are present;
8. screenshots must show no clipped text, overlapping controls, hidden currency labels, hidden exchange labels, hidden segment labels, hidden quantity/PnL values, hidden execution ids or hidden blocker rows;
9. screenshots alone are not acceptance unless API/projection readback also matches.
