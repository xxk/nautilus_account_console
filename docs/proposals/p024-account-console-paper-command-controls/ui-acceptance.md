# P024 UI Acceptance / Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase3c_runtime_handoff_request_passed

## Browser Acceptance

| ID | Scenario | Browser assertion | Status |
| --- | --- | --- | --- |
| UI-01 | disabled default | no submit/cancel/replace controls; `account-command-mode=disabled` | planned |
| UI-02 | paper armed controls | submit form and paper banner visible only with `paper_armed` evidence | phase2_frontend_guarded_controls_passed |
| UI-03 | submit pending | submit creates pending command status with intent/risk/approval refs | phase2_frontend_guarded_controls_passed |
| UI-04 | submit reconciled | final status requires readback and reconciliation refs | planned |
| UI-05 | cancel eligible row | cancel button uses `account-cancel-order-identity` | phase2_frontend_guarded_controls_passed |
| UI-06 | cancel pending/reconciled | cancel status cites cancel intent, gateway, readback and reconciliation refs | planned |
| UI-07 | duplicate click | duplicate click keeps one idempotency key and one command result | planned |
| UI-08 | gateway ack only | status is blocked, not final | planned |
| UI-09 | partial fill then cancel display correctness | S1/S2/S3/S4 order row keeps identity, stable fill rows, correct formulas and P024 evidence refs | phase3b_partial_fill_cancel_ui_display_passed |
| UI-10 | runtime closeout projection | owner-backed P023 runtime closeout refs/checksums/non-claims render in UI with browser trigger false | phase3a_runtime_closeout_projection_passed |
| UI-11 | owner-runtime handoff request | submit/cancel controls prepare blocked owner-runtime handoff requests with no browser-triggered broker order | phase3c_runtime_handoff_request_passed |

## UI-11 Owner Runtime Handoff Request

The browser test must click submit and cancel from `/accounts/acct.ctp.paper.19053`, then verify:

1. `account-runtime-handoff-panel` is visible after each action.
2. Submit handoff shows `account-runtime-handoff-entrypoint` ending in `ctp_guarded_paper_order_loop.py`.
3. Cancel handoff shows `account-runtime-handoff-entrypoint` ending in `ctp_guarded_paper_cancel_loop.py` and carries the order readback ref.
4. `account-runtime-handoff-status` is `blocked_until_owner_runtime_invocation`.
5. `account-runtime-handoff-invoked`, `account-runtime-handoff-web-trigger` and `account-runtime-handoff-raw-secret` are all `false`.
6. Blockers include owner runtime invocation, external write approval and post-run ingest.

Accepted evidence: `python scripts\validate_p024_runtime_handoff_browser_evidence.py` returns `P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK`.

## UI-10 Runtime Closeout Projection

The browser test must load `/accounts/acct.ctp.paper.19053` with the P024 runtime closeout endpoint available and verify:

1. `account-runtime-closeout-panel` is visible.
2. `account-runtime-closeout-run-id` is `p023-armed-20260621t0748z`.
3. `account-runtime-closeout-status` is `reconciled`.
4. `account-runtime-closeout-gateway-send` is `true` only as predecessor runtime evidence.
5. `account-runtime-closeout-web-trigger`, `account-runtime-closeout-raw-secret` and `account-runtime-closeout-gateway-final` are all `false`.
6. Command status refs for audit, risk, approval, gateway, readback and reconciliation are visible.
7. No UI text claims live readiness, gateway ack final state or browser-submitted broker order.

Accepted evidence: `python scripts\validate_p024_runtime_closeout_browser_evidence.py` returns `P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK`.

## UI-09 Partial Fill Then Cancel Display

The browser test must drive or mock the `/accounts/acct.ctp.paper.19053` projection through these stages:

| Stage | UI status | Submitted | Filled | Remaining | Cancelled | Required UI evidence |
| --- | --- | --- | --- | --- | --- | --- |
| S1 submitted/working | `working` | 10 | 0 | 10 | missing | `account-order-identity`; no fill rows |
| S2 partially filled | `partial` | 10 | 4 | 6 | missing | `account-order-partial-fill-row`; two fill rows; remaining cancel target `6` |
| S3 cancel pending | `cancel_pending` | 10 | 4 | 6 | missing | `account-cancel-pending-ref`; no final canceled claim |
| S4 remaining cancelled | `canceled` | 10 | 4 | 0 | 6 | filled rows unchanged; `filled + cancelled == submitted` |

Pass requires:

1. Same `account-order-identity` across S1-S4.
2. Browser fill sum equals order filled quantity.
3. Browser fill source refs match API projection source refs.
4. S2 cancel target equals S2 remaining quantity.
5. S3 quantities remain unchanged until cancel readback.
6. S4 filled quantity and trade identities remain stable after cancel.
7. S4 cancelled quantity equals S2 remaining quantity and remaining quantity is zero.
8. Screenshots alone are not sufficient; evidence JSON must carry source refs and explicit non-claims.

Accepted evidence: `python scripts\validate_p024_partial_fill_cancel_browser_evidence.py` returns `P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK`.

## Negative UI Acceptance

| ID | Failure path | Blocker / rejection |
| --- | --- | --- |
| NUI-01 | missing command capability | controls absent; `account-command-blocker` visible |
| NUI-02 | missing idempotency key | submit disabled |
| NUI-03 | missing risk/approval ref | submit blocked before gateway |
| NUI-04 | missing readback identity for cancel | cancel absent |
| NUI-05 | gateway ack as final | blocked |
| NUI-06 | live-ready wording | rejected |
| NUI-07 | browser attempts direct broker mutation | test failure |
| NUI-08 | partial-fill cancel display changes order identity | test failure |
| NUI-09 | final canceled row has `remaining_quantity > 0` or `cancelled_quantity != S2 remaining_quantity` | test failure |
| NUI-10 | cancel pending hides the blocker and claims final canceled state | blocked |
| NUI-11 | runtime closeout panel claims browser-triggered broker order or gateway ack final state | test failure |
| NUI-12 | runtime handoff panel claims owner runtime invocation, gateway send or broker order creation from browser | test failure |

## Blocker

Every blocked command-control state must include reason, stage, source ref and next action. Browser screenshots alone are not sufficient evidence.

## Evidence

P024 cannot close on UI design text alone. Browser evidence and command artifacts are required before implementation closeout.
