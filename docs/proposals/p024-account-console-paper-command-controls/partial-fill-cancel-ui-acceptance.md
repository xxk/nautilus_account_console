# P024 Partial Fill Then Cancel UI Acceptance

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase1_backend_contract_gate_passed
- Primary ADR: ADR-0007
- Account: `acct.ctp.paper.19053`

## Purpose

This document defines Web UI acceptance for the order display after a partial fill and cancellation of the remaining quantity. It verifies display correctness only when backed by typed evidence. It does not turn screenshots, browser text or TickTrader UI state into order truth.

P024 closeout must produce P024-scoped browser evidence under `docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-cancel-order-display.json`. Current P023 predecessor evidence can be used only as display-contract input and remains explicit that real runtime partial-fill is blocked until a real or owner-approved partial-fill state exists.

## Stage Model

| Stage | Meaning | Status | Submitted | Filled | Remaining | Cancelled | Required source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | submitted/working | `working` | 10 | 0 | 10 | missing | order readback |
| S2 | partially filled | `partial` | 10 | 4 | 6 | missing | order readback + fill readback |
| S3 | cancel pending | `cancel_pending` | 10 | 4 | 6 | missing | command audit ref; not final |
| S4 | remaining cancelled | `canceled` | 10 | 4 | 0 | 6 | cancel readback + reconciliation |

## Required Browser Checks

| Check | Required assertion |
| --- | --- |
| `same_order_identity_across_stages` | `account-order-identity` is identical in S1, S2, S3 and S4 |
| `s2_browser_fill_sum_equals_order_filled_quantity` | sum of `account-fill-quantity` rows equals `account-order-filled-quantity` |
| `s2_trade_refs_match_api_projection` | `account-fill-source-ref` values match API projection source refs |
| `s2_cancel_target_equals_s2_remaining_quantity` | `account-remaining-cancel-quantity` equals S2 `account-order-remaining-quantity` |
| `s3_quantities_unchanged_until_cancel_readback` | S3 submitted, filled, remaining and fill rows equal S2 |
| `s3_no_remaining_cancel_quantity_visible` | no second cancel target remains visible while cancel is pending |
| `s4_filled_quantity_preserved_after_cancel` | S4 filled quantity equals S2 filled quantity |
| `s4_cancelled_quantity_equals_s2_remaining_quantity` | S4 cancelled quantity equals S2 remaining quantity |
| `s4_remaining_quantity_zero` | S4 remaining quantity is zero |
| `s4_no_remaining_cancel_quantity_visible` | no cancel target remains after terminal cancel |
| `fill_trade_identities_stable_after_cancel` | S4 fill trade identities equal S2 fill trade identities |

## Data Test ID Coverage

The Web UI test must cover:

| Data Test ID | Stage coverage |
| --- | --- |
| `account-order-identity` | S1-S4 |
| `account-order-status` | S1-S4 |
| `account-order-submitted-quantity` | S1-S4 |
| `account-order-filled-quantity` | S1-S4 |
| `account-order-remaining-quantity` | S1-S4 |
| `account-order-cancelled-quantity` | S1-S4 |
| `account-order-partial-fill-row` | S2 |
| `account-remaining-cancel-quantity` | S1/S2 only when a cancel target is eligible |
| `account-cancel-pending-ref` | S3 |
| `account-fill-source-ref` | S2-S4 |
| `account-fill-quantity` | S2-S4 |
| `account-fill-price` | S2-S4 |
| `account-command-status-panel` | S3/S4 when P024 command controls are implemented |
| `account-command-readback-ref` | S4 when P024 command controls are implemented |
| `account-command-reconciliation-ref` | S4 when P024 command controls are implemented |

## Evidence Shape

P024 implementation evidence must be a machine-readable JSON file with:

1. `schema = account-console.p024.partial-fill-cancel-ui-acceptance.v1`.
2. `proposal_id = p024-account-console-paper-command-controls`.
3. `account_id = acct.ctp.paper.19053`.
4. `stages` containing S1-S4 with browser values, API/readback values, source refs and formulas.
5. `partial_cancel_display_checks` with every required browser check set to true.
6. Command artifacts for S3/S4: cancel intent, risk decision, approval decision, gateway event, readback and reconciliation refs.
7. `explicit_non_claims` including `does_not_use_screenshot_as_order_truth`, `does_not_claim_live_readiness`, and `gateway_ack_is_not_final_state`.
8. `raw_secret_values_recorded=false`.

## Negative UI Acceptance

| ID | Failure path | Required result |
| --- | --- | --- |
| PFN-01 | order identity changes between S2 and S4 | fail browser evidence |
| PFN-02 | S2 fill row sum does not equal order filled quantity | fail browser evidence |
| PFN-03 | S4 cancelled quantity does not equal S2 remaining quantity | fail browser evidence |
| PFN-04 | S4 remaining quantity is non-zero | fail browser evidence |
| PFN-05 | S3 cancel pending is shown as terminal canceled | blocker until readback/reconciliation |
| PFN-06 | fill trade identities change after cancel | fail browser evidence |
| PFN-07 | UI uses screenshot, row text or latest path as cancel authority | reject; requires readback identity and command audit |
| PFN-08 | raw password/front/auth/token appears in evidence | redaction failure |

## Current Predecessor Evidence

P023 has display-contract evidence for this shape:

1. Browser test: `frontend\tests\e2e\p023-openctp-partial-fill-order-display.spec.ts`.
2. Evidence JSON: `docs\acceptance\browser-evidence\p023-openctp-19053-command\partial-fill-order-display.json`.
3. Validator: `python scripts\validate_p023_partial_fill_browser_evidence.py`.
4. Pass signal: `P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK`.

This predecessor evidence is not P024 runtime closeout. P024 must regenerate P024-scoped evidence after guarded Web UI command controls and command artifacts are implemented.
