# P022 Acceptance / OpenCTP 19053

- Proposal ID: `p022-openctp-19053-account-console-readback`
- Status: implementation_gate_passed
- Updated: 2026-06-20

## Required Gates

| Gate | Command | Pass signal | Scope |
| --- | --- | --- | --- |
| P022 docs/source/UI validator | `python scripts/validate_p022_openctp_19053_readback.py` | `P022_OPENCTP_19053_READBACK_OK` | Proposal terms, source package, Account Mirror and UI evidence shape |
| CTP 19053 consistency | `python scripts/validate_ctp19053_consistency.py` | `CTP19053_CONSISTENCY_OK` | Source package projects through Account Mirror with command disabled |
| Account Mirror API | `python scripts/validate_account_mirror_api.py` | `ACCOUNT_MIRROR_API_OK` | `/api/mirror/accounts/acct.ctp.paper.19053` is read-only |
| Browser evidence | `npx playwright test tests/e2e/ctp19053-ui-funds-positions.spec.ts --project=desktop --workers=1` | Playwright pass | Funds, positions, open-order / 挂单 and fills / 成交单 empty/table UI |

## UI Anti-Drift Acceptance

forbidden_actions:

1. `OrderInsert`
2. `OrderAction`
3. `submit order`
4. `cancel order`
5. `replace order`
6. `can trade`

forbidden_claims:

1. browser screenshot proves OpenCTP account truth
2. Account Console owns CTP broker truth
3. Account Console owns OpenCTP command capability
4. empty order table proves no orders without owner evidence
5. empty fills table proves no trades without owner evidence

Implementation/browser evidence is required before implementation closeout.

## Required Positive Evidence

1. `source_health.api_transport=ctp_trader_api`
2. `source_health.order_action_sent=false`
3. `source_health.open_orders_state=empty` or `available`
4. `source_health.fills_state=empty` or `available`
5. `source_health.td_order_truth_login_success=true`
6. `source_health.td_order_truth_observed_order_event_count == orders.length`
7. `source_health.td_order_truth_observed_trade_event_count == fills.length`
8. `balances[0].currency=CNY`
9. `positions.length > 0`
10. UI evidence records `rendered_open_order_count`.
11. UI evidence records `rendered_fill_count`.
