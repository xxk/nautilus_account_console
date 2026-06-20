# P022 UI Design / OpenCTP 19053

## Data Test ID

| Region | Data Test ID |
| --- | --- |
| Account route | `account-terminal-workbench` |
| Source health | `account-source-health-panel` |
| CNY funds | `account-summary-cash` |
| Available cash | `account-summary-available-cash` |
| Margin | `account-summary-margin` |
| Positions table | `account-positions-table` |
| Position row | `account-position-projection-row` |
| Open orders table | `tws-open-orders-table` |
| Open order row | `tws-open-order-row` |
| Open order empty state | `tws-open-order-empty-state` |
| Fills table | `tws-fills-table` |
| Fill row | `tws-fill-row` |
| Fill empty state | `tws-fill-empty-state` |

## Layout

Use the existing Account Workbench terminal layout. The route must show the same broker-neutral regions used by IB TWS:

1. top status bar and command capability;
2. funds summary;
3. positions table;
4. open orders / 挂单 tape with rows or typed empty state;
5. fills / 成交单 table with rows or typed empty state;
6. evidence/source rail.

The UI must not add CTP-specific command controls.
