# P022 UI Acceptance / OpenCTP 19053

## Browser Acceptance

1. `/accounts/acct.ctp.paper.19053` renders `mirror API`.
2. Funds show CNY equity, available cash, buying power and margin from the source package.
3. Positions table contains one row per source package position.
4. Open orders / 挂单 tape contains one row per source package open order, or `tws-open-order-empty-state` when owner evidence reports zero order events.
5. Fills / 成交单 table contains one row per source package fill, or `tws-fill-empty-state` when owner evidence reports zero trade events.
6. Source refs and checksums remain visible.
7. Command capability remains observation-only.

## Negative UI Acceptance

1. Blocker: missing source package renders typed source blocker.
2. Blocker: owner evidence with zero orders must not be upgraded to fabricated order rows.
3. Blocker: owner evidence with zero trades must not be upgraded to fabricated fill rows.
4. UI must not contain submit, cancel, replace, modify or can-trade controls.
5. UI must not expose raw CTP secrets or raw broker endpoint values.
