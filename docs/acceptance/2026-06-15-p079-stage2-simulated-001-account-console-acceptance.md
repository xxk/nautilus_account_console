# P079 Stage 2 simulated-001 Account Console Acceptance

- Date: 2026-06-15
- Status: fixture_only_read_model_passed
- Scope: Account Console read-only projection/UI acceptance for `simulated-001`
- Upstream contract: `D:/Nautilus/_worktrees/r1-heartbeat-driver-contract/nautilus_strategies/docs/changes/20260615__paper__p079-stage2-025292-market-data-only-simulated-001-planning/evidence/stage2_environment_account_contract.json`

## Boundary

`simulated-001` is a Nautilus Sandbox Paper simulated ledger account for R1/P079 Stage 2. CTP `025292` is only an official market data source.

Account Console displays the read model and operator context only. It does not write ledger, order, fill, position, PnL or reconcile truth.

## Accepted UI/Read-Model Entry

```text
/accounts/simulated-001
```

Required visible facts:

1. `account_id`: `simulated-001`
2. `account_uid`: `sandbox-paper.simulated-001`
3. `account_type`: `sandbox_paper`
4. `ledger_type`: `simulated_sandbox_ledger`
5. Market: `CTP 025292 official market data only`
6. Execution: `Nautilus Sandbox Paper`
7. Orders: `simulated ledger only`
8. Broker submission: `disabled`
9. Stage: `R1/P079 Stage 2`

## Account Opening Acceptance Scenarios / 开户验收场景

### S1 开户：simulated-001 registry/read-model exists

Given the upstream Stage 2 environment account contract exists, when Account Console loads account projections, then the account list contains:

```text
account_id: simulated-001
account_uid: sandbox-paper.simulated-001
account_type: sandbox_paper
ledger_type: simulated_sandbox_ledger
stage: R1/P079 Stage 2
```

Pass evidence:

```powershell
python scripts\validate_p079_stage2_simulated_001.py
```

### S2 开户：025292 is market data only

Given `simulated-001` references CTP `025292`, when the read model is inspected, then CTP `025292` is visible only as:

```text
market_source: CTP 025292 official market data only
market_data_role: market_data_only
broker_order_submission: false
trading_adapter: disabled
```

It must not appear as a trading account, execution target, ledger owner or broker submission route.

### S3 开户：execution target is Nautilus Sandbox Paper

Given the account is opened for Stage 2 sandbox paper simulation, when UI opens `/accounts/simulated-001`, then the UI displays:

```text
Execution: Nautilus Sandbox Paper
Orders: simulated ledger only
Broker submission: disabled
```

The page must still show command plane as observation-only with no mounted submit/cancel/replace controls.

### S4 开户：Account Console is projection/operator surface only

Given `simulated-001` has summary/orders/fills/positions/PnL/reconcile concepts, Account Console may display those projections and evidence refs/checksums only. It must not write:

```text
ledger truth
order truth
fill truth
position truth
account balance truth
reconcile truth
paper readiness
live readiness
broker tradability
```

### S5 开户：fixture-only blocker is explicit

Given no pinned sandbox paper runtime projection exists yet, then this acceptance records:

```text
blocker_id: simulated001_stage2_fixture_only
type: fixture_only_read_model
owner: nautilus_strategies.sandbox_paper_runtime
```

This is enough for Stage 2 planning/UI acceptance, but not enough for runtime truth or Stage 3.

## Negative Acceptance

This acceptance must fail if:

1. CTP `025292` is treated as a trading account.
2. Any CTP trading front/order submission path is exposed.
3. `simulated-001` is treated as a real broker account.
4. Account Console writes ledger/order/fill/position/PnL/reconcile truth.
5. UI declares Paper ready, Live ready, production ready, capital allocated, broker tradable or can trade.
6. Stage 3, CTP `025202`, Live/admission/risk/capital work is introduced.

## Evidence

| Evidence | Command | Result |
| --- | --- | --- |
| Stage 2 contract/read-model gate | `python scripts\validate_p079_stage2_simulated_001.py` | `P079_STAGE2_SIMULATED_001_OK: account=simulated-001 market_source=025292 role=market_data_only` |
| Source bridge gate | `python scripts\validate_account_source_bridges.py` | `ACCOUNT_SOURCE_BRIDGES_OK: bundles=3 projections=3` |
| Mirror API gate | `python scripts\validate_account_mirror_api.py` | `ACCOUNT_MIRROR_API_OK: accounts=4` |
| Browser/UI gate | `cd frontend && npx playwright test tests/e2e/account-terminal-workbench.spec.ts` | `9 passed` |

Browser evidence for `/accounts/simulated-001`:

```text
docs/acceptance/browser-evidence/p011-account-workbench-api-readback/desktop-simulated-001-stage2.png
docs/acceptance/browser-evidence/p011-account-workbench-api-readback/tablet-simulated-001-stage2.png
docs/acceptance/browser-evidence/p011-account-workbench-api-readback/mobile-simulated-001-stage2.png
```

## Blocker

`simulated-001` currently uses a fixture-only read model:

```text
blocker_id: simulated001_stage2_fixture_only
type: fixture_only_read_model
owner: nautilus_strategies.sandbox_paper_runtime
next_action: replace with pinned sandbox paper runtime projection when the upstream owner publishes one
```

This blocker is accepted for Stage 2 planning/UI acceptance. It is not runtime truth and does not authorize order submission.

## 2026-06-16 ag2612 Buy-One Projection Update

`simulated-001` now includes a read-only sandbox paper projection for one filled buy-open order:

```text
instrument: ag2612
side: buy
quantity: 1
filled_quantity: 1
status: filled
client_order_id: simulated-001-ag2612-buy-1-001
```

The accepted UI entry for this projection is:

```text
http://127.0.0.1:5173/accounts/acct.demo-19053
```

This legacy route opens canonical `simulated-001` and is covered by:

```text
docs/acceptance/2026-06-16-legacy-acct-demo-19053-simulated-001-ag2612-ui-acceptance.md
frontend/tests/e2e/legacy-simulated-001-ag2612-ui-acceptance.spec.ts
```

The update remains projection-only. It does not mean Account Console submitted the order or wrote sandbox ledger truth.
