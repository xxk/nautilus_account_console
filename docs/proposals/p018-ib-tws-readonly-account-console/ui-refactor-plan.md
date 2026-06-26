# P018 UI Refactor Plan / UI 重构方案

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready

## 1. Refactor Goal / 重构目标

Refactor Account Workbench from a generic dense terminal page into a broker-neutral account operations surface that can display IB TWS page coverage without creating broker-specific truth or action controls.

The refactor must keep existing P004/P011 readback behavior green while adding explicit regions for IB live account sections.

## 2. Target Layout / 目标布局

```text
Account Workbench
  Top status bar
    account identity / alias / account type / source timestamp / freshness / command disabled

  Left rail
    account selector
    source package status
    capability gates

  Main workspace
    Overview band
      balances / margin / available-for-trading / command-disabled state
    Multi-currency funds
      original-currency rows / base-currency totals / FX provenance
    Positions
      portfolio filters / stable position table / row-level evidence
    Orders
      open orders / read-only order provenance
    Execution reports
      immutable fills / commission joins / read-only execution provenance
    Missing regions
      typed blockers for any in-scope section not implemented

  Right rail
    evidence refs
    source health
    blockers
    boundary assertions
```

## 3. Region Contract / 区域合同

| Region | Purpose | Required data-testid | Closeout rule |
| --- | --- | --- | --- |
| account identity | selected account, alias, account type and update time | `ib-live-selected-account`, `ib-live-update-metadata` | must render or block |
| balances | net liquidation, cash, available funds, monthly interest and segment columns | `ib-live-balances-panel` | must render or block |
| segment matrix | Total / US Securities / US Commodities / UK Regulated / extra segments | `ib-live-balance-segment-matrix` | detail view must preserve columns |
| margin requirements | current initial and maintenance margin | `ib-live-margin-panel` | must render or block |
| available trading | available funds, excess liquidity, SMA/margin cushion when provided | `ib-live-available-trading-panel` | must render or block |
| real FX / market value | original-currency rows, base totals, FX provenance | `ib-live-real-fx-market-value-panel` | must render or block |
| portfolio filters | text, security type, currency, exchange and zero-position toggle | `ib-live-portfolio-filter-bar` | must disclose filter state |
| positions | stable position rows with exchange/currency/contract identity | `ib-live-positions-table` | must match source/API |
| orders | read-only open orders and order status | `ib-live-orders-table` | no action controls |
| execution reports | immutable fills, commission joins and realized PnL when provided | `ib-live-executions-table` | no action controls and no order-status inference |
| missing region blockers | explicit partial state for unimplemented in-scope regions | `ib-live-*-region-missing` | blocks full closeout |

## 4. Component Split / 组件拆分

The implementation should split the current monolithic Account Workbench UI into small read-only components:

1. `AccountWorkbenchShell`
2. `AccountSelectorRail`
3. `AccountStatusBar`
4. `SourceHealthPanel`
5. `CapabilityGatePanel`
6. `FundsOverviewPanel`
7. `SegmentMatrixPanel`
8. `MultiCurrencyFundsPanel`
9. `MarginRequirementsPanel`
10. `AvailableTradingPanel`
11. `PortfolioFilters`
12. `PositionsTable`
13. `OrdersPanel`
14. `ExecutionReportsTable`
15. `EvidenceRail`
16. `MissingRegionBlocker`

These components should land through canonical owner modules such as `frontend/src/account-workbench-terminal.tsx`, `frontend/src/account-workbench-adapters.ts`, `frontend/src/account-workbench-routing.ts` and `frontend/src/fixture-selection.ts`. `frontend/src/App.tsx` is the composition root and must not be the lasting owner for these regions.

## 5. Implementation Phases / 实现阶段

### Phase UI-1: Region Skeleton

Add static region containers and missing-region blockers without changing source truth.

Exit:

1. existing Account Workbench tests still pass;
2. missing IB regions show typed blockers;
3. no full TWS coverage claim is possible.

### Phase UI-2: Source Package Binding

Bind IB source package/API fields to each region.

Exit:

1. balances, margin, available trading, multi-currency funds and positions read from Account Mirror API;
2. stale/missing/mismatch source states fail closed.

### Phase UI-3: Browser Readback

Add browser tests for desktop/tablet/mobile and section coverage.

Exit:

1. selectors match `ui-acceptance.md`;
2. screenshots plus API readback prove the regions;
3. missing-region blockers prevent full closeout.

### Phase UI-4: Component Extraction

Extract stable components after behavior is tested.

Exit:

1. no data contract changes;
2. no visual/readback regression;
3. no duplicate broker-specific UI truth.

## 6. Design Rules / 设计规则

1. Dense operational UI, not a marketing page.
2. Every section shows source/projection evidence or a blocker.
3. No cards inside cards.
4. Tables use stable columns and horizontal scroll where necessary.
5. Numeric values align right; currency and `n/a` semantics remain visible.
6. Compact summary may collapse data only if detail view preserves original rows/columns.
7. Missing UI regions are visible blockers, not hidden gaps.
8. No submit, cancel, replace, reconnect, login or broker mutation controls.

## 7. Acceptance Hooks / 验收钩子

The UI refactor is not accepted unless these selectors exist or their missing-region blockers exist:

1. `ib-live-balances-panel`
2. `ib-live-balance-segment-matrix`
3. `ib-live-margin-panel`
4. `ib-live-available-trading-panel`
5. `ib-live-real-fx-market-value-panel`
6. `ib-live-portfolio-filter-bar`
7. `ib-live-positions-table`
8. `ib-live-orders-table`
9. `ib-live-executions-table`
10. `ib-live-evidence-drawer-trigger`
