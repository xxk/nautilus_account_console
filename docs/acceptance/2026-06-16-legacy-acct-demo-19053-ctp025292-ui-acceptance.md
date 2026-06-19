# Legacy acct.demo-19053 CTP 025292 UI Acceptance

- Date: 2026-06-16
- Status: superseded_by_legacy_simulated_001_entry
- Manual URL: `http://127.0.0.1:5173/accounts/acct.demo-19053`
- Executable route: `/accounts/acct.demo-19053`
- Canonical account: `acct.ctp.live.025292`
- Display alias: `025292`
- Evidence output: `docs/acceptance/2026-06-16-legacy-acct-demo-19053-ctp025292-ui-acceptance-evidence.json`
- Browser evidence dir: `docs/acceptance/browser-evidence/legacy-025292-ui-funds-positions-orders/`

## Acceptance Boundary

This acceptance was superseded on 2026-06-16 by [Legacy acct.demo-19053 Simulated 001 ag2612 UI Acceptance](./2026-06-16-legacy-acct-demo-19053-simulated-001-ag2612-ui-acceptance.md). The legacy Account Workbench URL `acct.demo-19053` now opens canonical `simulated-001`.

The direct CTP `025292` UI acceptance remains `/accounts/acct.ctp.live.025292`.

Historical boundary: this acceptance verified that a legacy Account Workbench URL could be treated as a compatibility entry into the CTP `025292` read-only mirror projection.

The route must display `025292` funds, positions and orders from the canonical Account Mirror projection for `acct.ctp.live.025292`. It must not use `acct.demo-19053` as the canonical account id, and it must not treat market-data lineage, fixture data, browser state or screenshots as account truth.

## Required Source

The only passing source package is:

```text
output/account_capability/ctp-live-025292/source-package.json
```

The source package must be a pinned `ctp_trader_api` / `live_observation` account readback package with:

1. funds/balances from read-only account query;
2. positions from read-only position query;
3. orders from read-only order query;
4. source refs and checksums;
5. command capability disabled.

Market-data-only route lineage for `ctp025292_marketdata_sandbox_paper_simulated_001` cannot satisfy this UI acceptance.

## Positive Acceptance

The UI acceptance passes only when:

1. opening `http://127.0.0.1:5173/accounts/acct.demo-19053` renders Account Workbench in `mirror API` mode;
2. the top status bar shows canonical account `acct.ctp.live.025292` and alias `025292`;
3. funds display `equity`, `available_cash`, `buying_power`, `margin_used` and related CNY values from the 025292 projection;
4. positions table displays every 025292 position row with instrument, quantity, available quantity and source ref;
5. orders tape displays every 025292 order row with client order id, instrument and status;
6. source health and evidence rail show the pinned source package and projection checksum;
7. command capability remains `observation only` / `none mounted`;
8. forbidden readiness/action wording is absent.

## Negative UI Acceptance

This acceptance must fail or remain blocked if:

1. the route silently falls back to another account;
2. `acct.demo-19053` appears as canonical account truth;
3. the UI displays empty funds, empty positions or empty orders while declaring a pass;
4. the 025292 source package is missing, invalid, market-data-only, unpinned or lacks balances/positions/orders;
5. order controls or wording such as `submit order`, `cancel order`, `can trade`, `Paper ready`, `Live ready`, `capital allocated` appears;
6. screenshots are used without API/source/projection comparison.

## Blocker

Current blocker:

```text
blocker_id: ctp025292_real_login_source_unavailable
owner: nautilus_ctp_adapter
next_action: Run read-only real-login CTP 025292 account, position and order queries, then build output/account_capability/ctp-live-025292/source-package.json.
```

If a file exists at the source-package path but is market-data-only lineage or lacks account readback fields, Account Console must render the same fail-closed blocker rather than crash or display false funds.

## Browser Acceptance

Run:

```powershell
cd frontend
npx playwright test tests/e2e/legacy-025292-ui-funds-positions-orders.spec.ts --project=desktop
```

Expected current result:

```text
verdict: blocked
status: blocked_waiting_for_025292_account_source_package
canonical_account_id: acct.ctp.live.025292
required_ready_domains: funds, positions, orders
```

The blocked verdict is accepted only as fail-closed UI evidence. It is not a pass for 025292 real-account consistency.
