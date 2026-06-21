# P024 UI Acceptance / Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4za_owner_repair_execution_handoff_ui_projection_passed

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
| UI-12 | runtime readiness blocker projection | readiness package owner refs, entrypoints, approval state, blockers and non-claims render in UI while runtime invocation remains false | phase3e_runtime_readiness_ui_projection_passed |
| UI-13 | runtime approval packet projection | exact approval text, owner path, entrypoints, blockers and false execution flags render in UI while approval remains unobtained | phase4b_runtime_approval_packet_ui_projection_passed |
| UI-14 | runtime handoff bundle projection | execution guard, runtime inputs, operator sequence, artifact counts and blockers render in UI while execution remains disallowed | phase4d_runtime_handoff_bundle_ui_projection_passed |
| UI-15 | runtime execution gap audit projection | A4 not-accepted status, approval blocker, owner artifact count and false final-acceptance/execution flags render in UI | phase4e_runtime_execution_gap_audit_passed |
| UI-16 | partial-fill runtime approval packet projection | exact partial-fill approval text, owner path, formulas, entrypoints, blockers and false new-order/cancel flags render in UI | phase4l_partial_fill_runtime_approval_packet_ui_projection_passed |
| UI-17 | partial-fill runtime handoff bundle projection | runtime inputs, owner sequence, success formulas, fallback classifications and false execution flags render in UI | phase4m_partial_fill_runtime_handoff_bundle_ui_projection_passed |

## UI-17 Partial-Fill Runtime Handoff Bundle Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only partial-fill runtime handoff bundle endpoint, and verify:

1. `account-partial-fill-runtime-handoff-bundle-panel` is visible.
2. `account-partial-fill-runtime-handoff-bundle-status` is `phase4k_partial_fill_runtime_execution_handoff_bundle_ready`.
3. `account-partial-fill-runtime-handoff-bundle-execution-allowed` and `account-partial-fill-runtime-handoff-bundle-approval-obtained` are `false`.
4. `account-partial-fill-runtime-handoff-bundle-invoked`, `account-partial-fill-runtime-handoff-bundle-owner-write`, `account-partial-fill-runtime-handoff-bundle-new-order` and `account-partial-fill-runtime-handoff-bundle-cancel-sent` are all `false`.
5. `account-partial-fill-runtime-handoff-bundle-input` shows fresh owner pre-snapshot, quantity, owner-reviewed limit price and owner readback identity requirements.
6. `account-partial-fill-runtime-handoff-bundle-step` shows the gated submit, classify, cancel, readback and ingest sequence.
7. `account-partial-fill-runtime-handoff-bundle-success` includes `0 < filled_quantity < submitted_quantity`, terminal cancel and remaining quantity formulas.
8. `account-partial-fill-runtime-handoff-bundle-fallback` includes fully filled, cancelled-without-fill, rejected/timeout and incomplete-artifact classifications.

Accepted evidence: `python scripts\validate_p024_partial_fill_runtime_handoff_bundle_browser_evidence.py` returns `P024_PARTIAL_FILL_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK`.

## UI-16 Partial-Fill Runtime Approval Packet Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only partial-fill runtime approval packet endpoint, and verify:

1. `account-partial-fill-runtime-approval-packet-panel` is visible.
2. `account-partial-fill-runtime-approval-packet-status` is `phase4j_partial_fill_runtime_execution_approval_packet_ready`.
3. `account-partial-fill-runtime-approval-packet-owner-path` is `D:/Nautilus/nautilus_ctp_adapter`.
4. `account-partial-fill-runtime-approval-packet-required` is `true` and `account-partial-fill-runtime-approval-packet-obtained` is `false`.
5. `account-partial-fill-runtime-approval-packet-invoked`, `account-partial-fill-runtime-approval-packet-owner-write`, `account-partial-fill-runtime-approval-packet-new-order` and `account-partial-fill-runtime-approval-packet-cancel-sent` are all `false`.
6. `account-partial-fill-runtime-approval-packet-exact-text` displays the exact P024 partial-fill approval text.
7. `account-partial-fill-runtime-approval-packet-formula` displays the partial-fill, terminal cancel and remaining quantity formulas.
8. `account-partial-fill-runtime-approval-packet-blocker` includes external approval and missing real partial-fill runtime artifact blockers.

Accepted evidence: `python scripts\validate_p024_partial_fill_runtime_approval_packet_browser_evidence.py` returns `P024_PARTIAL_FILL_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK`.

## UI-15 Runtime Execution Gap Audit Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only runtime execution gap endpoint, and verify:

1. `account-runtime-execution-gap-panel` is visible.
2. `account-runtime-execution-gap-status` is `phase4e_final_runtime_execution_gap_audited`.
3. `account-runtime-execution-gap-verdict` is `blocked_pending_owner_runtime_execution`.
4. `account-runtime-execution-gap-final-claimed` is `false`.
5. `account-runtime-execution-gap-not-accepted` includes A4 and owner-runtime execution artifact requirements.
6. `account-runtime-execution-gap-approval-obtained`, `account-runtime-execution-gap-invoked`, `account-runtime-execution-gap-owner-write` and `account-runtime-execution-gap-broker-order` are all `false`.
7. `account-runtime-execution-gap-blocker` includes external write approval, owner runtime artifact and real partial-fill runtime blockers.

Accepted evidence: `python scripts\validate_p024_runtime_execution_gap_browser_evidence.py` returns `P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK`.

## UI-14 Runtime Handoff Bundle Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only handoff bundle endpoint, and verify:

1. `account-runtime-handoff-bundle-panel` is visible.
2. `account-runtime-handoff-bundle-status` is `phase4c_owner_runtime_execution_handoff_bundle_ready`.
3. `account-runtime-handoff-bundle-execution-allowed` is `false`.
4. `account-runtime-handoff-bundle-approval-obtained` is `false`.
5. `account-runtime-handoff-bundle-invoked`, `account-runtime-handoff-bundle-owner-write` and `account-runtime-handoff-bundle-broker-order` are all `false`.
6. `account-runtime-handoff-bundle-input` shows runtime input requirements including owner pre-snapshot and readback order identity.
7. `account-runtime-handoff-bundle-step` shows the gated operator sequence including submit and cancel runtime steps.
8. `account-runtime-handoff-bundle-blocker` includes external write approval, runtime input and owner artifact blockers.

Accepted evidence: `python scripts\validate_p024_runtime_handoff_bundle_browser_evidence.py` returns `P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK`.

## UI-13 Runtime Approval Packet Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only approval packet endpoint, and verify:

1. `account-runtime-approval-packet-panel` is visible.
2. `account-runtime-approval-packet-status` is `phase4a_owner_runtime_execution_approval_packet_ready`.
3. `account-runtime-approval-packet-owner-path` is `D:/Nautilus/nautilus_ctp_adapter`.
4. `account-runtime-approval-packet-required` is `true` and `account-runtime-approval-packet-obtained` is `false`.
5. `account-runtime-approval-packet-invoked`, `account-runtime-approval-packet-owner-write` and `account-runtime-approval-packet-broker-order` are all `false`.
6. `account-runtime-approval-packet-exact-text` displays the exact operator approval text beginning with `I approve writes to D:/Nautilus/nautilus_ctp_adapter`.
7. `account-runtime-approval-packet-entrypoint` shows both guarded submit/cancel entrypoints and arm flags.
8. `account-runtime-approval-packet-blocker` includes external write approval and owner artifact blockers.

Accepted evidence: `python scripts\validate_p024_runtime_approval_packet_browser_evidence.py` returns `P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK`.

## UI-12 Runtime Readiness Blocker Projection

The browser test must load `/accounts/acct.ctp.paper.19053`, call the read-only readiness endpoint, and verify:

1. `account-runtime-readiness-panel` is visible.
2. `account-runtime-readiness-status` is `blocked_waiting_for_external_owner_runtime_write_approval`.
3. `account-runtime-readiness-owner`, `account-runtime-readiness-owner-path` and `account-runtime-readiness-config-ref` are visible without raw endpoint values.
4. `account-runtime-readiness-approval-required` is `true` and `account-runtime-readiness-approval-obtained` is `false`.
5. `account-runtime-readiness-invoked`, `account-runtime-readiness-owner-write`, `account-runtime-readiness-browser-trigger`, `account-runtime-readiness-config-raw` and `account-runtime-readiness-raw-secret` are all `false`.
6. `account-runtime-readiness-entrypoint` shows both guarded submit/cancel entrypoints and arm flags.
7. `account-runtime-readiness-blocker` includes external write approval and owner artifact blockers.
8. No UI text claims live readiness, raw OpenCTP endpoint truth, or browser-submitted broker order.

Accepted evidence: `python scripts\validate_p024_runtime_readiness_browser_evidence.py` returns `P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK`.

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
| NUI-13 | runtime readiness panel hides approval blocker, shows raw endpoint/secret material, or claims owner runtime invocation | test failure |
| NUI-14 | runtime approval packet panel hides exact approval text, claims approval obtained, owner runtime invoked, owner repo written, broker order created or raw endpoint/secret material | test failure |
| NUI-15 | runtime handoff bundle panel claims execution allowed, approval obtained, owner runtime invoked, owner repo written, broker order created or raw endpoint/secret material | test failure |
| NUI-16 | partial-fill approval packet panel claims approval obtained, owner runtime invoked, owner repo written, new order submitted, cancel sent or hides formulas | test failure |
| NUI-17 | partial-fill handoff bundle panel claims execution allowed, new order submitted, cancel sent, full acceptance claimed or promotes fixture evidence to runtime truth | test failure |

## Blocker

Every blocked command-control state must include reason, stage, source ref and next action. Browser screenshots alone are not sufficient evidence.

## Evidence

P024 cannot close on UI design text alone. Browser evidence and command artifacts are required before implementation closeout.





