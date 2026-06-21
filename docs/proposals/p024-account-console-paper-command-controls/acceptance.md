# P024 Acceptance / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase3c_runtime_handoff_request_passed
- Primary ADR: ADR-0007

## Scope

P024 accepts only guarded Web/API paper command controls for `acct.ctp.paper.19053`. Implementation/browser evidence is required before implementation closeout; design-gate readiness is not browser or runtime closeout.

Out of scope: live trading, replace order, Account Mirror write authority, direct browser-to-CTP calls, raw secret ownership, screenshots as command truth.

## Required Gates

| Gate | Command | Pass signal | Scope |
| --- | --- | --- | --- |
| P024 design gate | `python scripts\validate_p024_paper_command_controls_design.py` | `P024_PAPER_COMMAND_CONTROLS_DESIGN_OK` | Proposal docs, ADR coverage, current no-controls boundary |
| P024 backend command API | `python scripts\validate_p024_paper_command_api.py` | `P024_PAPER_COMMAND_API_OK` | Paper-only submit/cancel intent API, fail-closed before gateway, mirror remains read-only |
| P024 frontend command controls | `npx playwright test tests/e2e/p024-paper-command-controls.spec.ts --project=desktop` then `python scripts\validate_p024_ui_command_controls_browser_evidence.py` | `P024_UI_COMMAND_CONTROLS_BROWSER_EVIDENCE_OK` | Disabled controls absent; `paper_armed` controls visible; submit/cancel call Phase 1 API; gateway send remains false |
| P024 runtime closeout projection | `npx playwright test tests/e2e/p024-runtime-closeout-evidence.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_closeout_browser_evidence.py` | `P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK` | Existing owner-backed P023 OpenCTP paper runtime closeout refs/checksums/non-claims render in Web UI; browser-triggered broker order remains false |
| P024 partial-fill cancel display | `npx playwright test tests/e2e/p024-partial-fill-cancel-order-display.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_cancel_browser_evidence.py` | `P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK` | S1-S4 Web UI order/fill display correctness; cancel pending is not final; runtime partial-fill remains typed blocker |
| P024 runtime handoff request | `npx playwright test tests/e2e/p024-runtime-handoff-request.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_handoff_browser_evidence.py` | `P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK` | Submit/cancel controls prepare owner-runtime run requests with blocked owner invocation; no browser-triggered broker order claim |
| P023 runtime predecessor | `python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json` | `P023_OPENCTP19053_COMMAND_RUN_OK` | Predecessor paper command evidence |
| Proposal docs | `python scripts\check_proposal_docs.py --root . --proposal-id p024-account-console-paper-command-controls` | `PROPOSAL_DOCS_OK` | Proposal structure |

## Scenario Matrix

| ID | Type | Scenario | Verification shape | Must fail if | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | positive | Backend command API accepts paper submit intent | API contract + command artifact validator | endpoint bypasses risk/approval | phase1_backend_contract_gate_passed |
| A2 | positive | Account Mirror remains read-only | route audit | `/api/mirror` exposes POST/PUT/DELETE | design_gate_ready |
| A3 | positive | Command controls render only in `paper_armed` mode | Playwright + API projection | controls appear while disabled | phase2_frontend_guarded_controls_passed |
| A4 | positive | Submit writes intent/risk/approval/gateway/readback/reconcile refs | integration + artifact validator | gateway ack alone is final | planned |
| A5 | positive | Submit idempotency prevents duplicate order | retry/duplicate-click test | duplicate broker order identity appears | phase2_frontend_guarded_controls_passed |
| A6 | positive | Risk/approval fail closed | negative API tests | missing risk/approval reaches gateway | planned |
| A7 | positive | Cancel uses latest readback identity | API/browser + readback artifact | cancel uses UI row text or screenshot | phase1_backend_contract_gate_passed |
| A8 | positive | UI status waits for readback/reconcile | browser evidence | final state shown without readback/reconcile | planned |
| A9 | positive | Secret redaction | artifact redaction gate | raw password/front/auth/token recorded | planned |
| A10 | positive | Partial fill then cancel Web UI order display correctness | Playwright + `partial-fill-cancel-ui-acceptance.md` + browser evidence JSON | identity changes, fill rows drift, or quantity formulas fail | phase3b_partial_fill_cancel_ui_display_passed |
| A11 | positive | Runtime closeout evidence appears in Web UI without browser-trigger claim | Playwright + API route audit + browser evidence JSON | UI hides refs/checksums, shows gateway ack final, or claims browser submitted broker order | phase3a_runtime_closeout_projection_passed |
| A12 | positive | Web UI prepares owner-runtime submit/cancel handoff without invoking broker runtime | Playwright + API route audit + browser evidence JSON | runtime invocation, gateway send or broker order creation is claimed from the browser | phase3c_runtime_handoff_request_passed |

## Phase 3c Owner Runtime Handoff Request Acceptance

The Web UI must prepare typed owner-runtime handoff requests for submit and cancel while keeping broker mutation outside this worktree:

1. Backend exposes `POST /api/commands/accounts/{account_id}/runtime-run-requests/submit` and `POST /api/commands/accounts/{account_id}/runtime-run-requests/cancel`.
2. Each response uses `account_command.owner_runtime_run_request.v1` and returns `status=blocked_until_owner_runtime_invocation`.
3. Submit handoff cites `scripts/ctp_guarded_paper_order_loop.py`; cancel handoff cites `scripts/ctp_guarded_paper_cancel_loop.py`.
4. The Web UI displays owner runtime entrypoint, config ref, checksum, blockers and explicit non-claims in `account-runtime-handoff-panel`.
5. `runtime_invocation_attempted=false`, `browser_triggered_broker_order=false`, `gateway_send_attempted=false`, `broker_order_created=false`, `raw_secret_values_recorded=false` and `raw_broker_endpoint_recorded=false` are required.
6. The accepted blocker is an owner-runtime handoff blocker, not a pass for real broker execution.

Accepted evidence: `python scripts\validate_p024_runtime_handoff_browser_evidence.py` returns `P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK`.

## Phase 3a Runtime Closeout Projection Acceptance

The Web UI must render the existing owner-backed P023 OpenCTP 19053 paper runtime closeout for `p023-armed-20260621t0748z` as read-only evidence:

1. Backend exposes `GET /api/commands/accounts/{account_id}/runtime-closeouts/{run_id}` and no write method for closeout projection.
2. The response includes `closeout_manifest_ref`, `command_audit_ref`, artifact checksums, intent/risk/approval/gateway/readback/reconciliation refs and explicit non-claims.
3. `runtime_gateway_send_observed=true` and `broker_order_created=true` are accepted only as owner-backed predecessor runtime evidence.
4. `browser_triggered_broker_order=false`, `gateway_ack_is_final_state=false`, `raw_secret_values_recorded=false` and `raw_broker_endpoint_recorded=false` must be displayed and validated.
5. The command status panel may project those refs, but it must not claim live readiness or a new browser-triggered broker order.

Accepted evidence: `python scripts\validate_p024_runtime_closeout_browser_evidence.py` returns `P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK`.

## Partial Fill Then Cancel Acceptance

The Web UI must verify the same order across four stages: `S1 submitted/working`, `S2 partially filled`, `S3 cancel pending`, and `S4 remaining cancelled`.

Required display formulas:

1. `S2`: `filled_quantity + remaining_quantity == submitted_quantity`.
2. `S3`: filled, remaining and fill rows remain unchanged until cancel readback.
3. `S4`: `filled_quantity + cancelled_quantity == submitted_quantity`.
4. `S4`: `remaining_quantity == 0`.

Required identity and provenance checks:

1. `account-order-identity` is stable across all stages.
2. `account-fill-source-ref` rows remain stable after cancel.
3. `account-remaining-cancel-quantity` equals the S2 remaining quantity and disappears after cancel is pending or terminal.
4. `account-cancel-pending-ref` cites command audit evidence and never proves final state by itself.
5. The final canceled display requires readback and reconciliation evidence, not gateway acknowledgement alone.

P024 browser evidence is now proposal-scoped: `python scripts\validate_p024_partial_fill_cancel_browser_evidence.py` returns `P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK`. This is display-contract evidence only and explicitly preserves `typed_blocker_until_real_or_owner_approved_partial_fill_state`; it does not claim real partial-fill runtime or broker truth.

## Phase 1 Backend Command API Acceptance

P024 Phase 1 exposes only these backend routes:

1. `POST /api/commands/accounts/{account_id}/submit-intents`
2. `POST /api/commands/accounts/{account_id}/cancel-intents`
3. `POST /api/commands/accounts/{account_id}/runtime-run-requests/submit`
4. `POST /api/commands/accounts/{account_id}/runtime-run-requests/cancel`
5. `GET /api/commands/accounts/{account_id}/runtime-closeouts/{run_id}`

The API accepts only `account_id=acct.ctp.paper.19053` and `mode=paper_armed`. A valid request returns `status=accepted_for_risk`, deterministic `command_id`, `idempotency_enforced=true`, `gateway_send_attempted=false`, `broker_order_created=false`, `runtime_duplicate_send_attempted=false`, `gateway_ack_is_final_state=false`, `raw_secret_values_recorded=false`, and blockers for `risk_decision_required` plus `approval_decision_required`.

The submit/cancel routes are contract gates only. They do not send broker commands. The runtime handoff routes prepare typed owner-runtime run requests only; they do not invoke owner scripts, send gateway commands or create broker orders. The runtime closeout route is read-only projection of existing owner-backed artifacts and does not send broker commands.

## Phase 2 Frontend Guarded Controls Acceptance

Browser evidence proves:

1. Disabled projection has no `account-submit-order-form`, `account-submit-order-button` or `account-cancel-order-button`.
2. `paper_armed` projection shows `account-paper-command-banner`, `account-command-preflight-ref`, `account-submit-order-form`, `account-submit-idempotency-key`, `account-submit-order-button`, `account-cancel-order-identity` and `account-cancel-order-button`.
3. Submit and cancel call only the P024 Phase 1 API and both return `accepted_for_risk`.
4. Browser evidence records `paper_armed_controls_visible=true`, `gateway_send_attempted=false`, `broker_order_created=false` and `gateway_ack_is_final_state=false`.
5. The cancel request uses readback identity and readback ref from the order row, not screenshot or row text alone.

This remains browser/control contract evidence. It does not claim real Web UI OpenCTP runtime command execution.

## Negative Acceptance

| ID | Failure path | Required rejection |
| --- | --- | --- |
| N1 | Account Mirror writer path appears | reject; mirror remains read-only |
| N2 | UI controls appear with `command.mode=disabled` | hidden controls and blocker |
| N3 | duplicate submit/click/retry | same command result, one broker order identity |
| N4 | cancel without readback identity | reject before gateway |
| N5 | gateway ack final-state claim | blocked until readback/reconcile |
| N6 | missing risk or approval | reject before gateway |
| N7 | raw secret/front/auth/token in artifact | redaction failure |
| N8 | live mode exposed | reject; P024 is paper-only |
| N9 | partial-fill cancel display uses changed identity, stale fill rows or broken quantity formula | reject browser evidence |
| N10 | cancel-pending gateway event is shown as final canceled state | blocked until readback/reconciliation |
| N11 | Phase 1 API reaches gateway without risk/approval | reject; `gateway_send_attempted=false` required |
| N12 | runtime handoff request is treated as broker execution | blocked until owner runtime artifacts are ingested and reconciled |

## UI Anti-Drift Acceptance

| ID | Drift | forbidden_actions | forbidden_claims | Required rejection |
| --- | --- | --- | --- | --- |
| UAD-01 | Disabled account shows controls | submit, cancel, replace | Paper ready, can trade | controls absent |
| UAD-02 | Browser calls broker directly | CTP/TWS browser mutation | broker truth from UI | browser test fails |
| UAD-03 | Gateway ack shown as final | final success without readback | command complete | blocker |
| UAD-04 | Live control appears | live submit/cancel | live ready | reject |
| UAD-05 | Runtime handoff panel claims owner runtime was invoked from browser | owner runtime send | broker order created by browser | reject |

## Evidence Boundary

Implementation/browser evidence is required before implementation closeout. Phase 1, Phase 2, Phase 3a, Phase 3b and Phase 3c browser/contract gates are accepted; Phase 3 real Web UI submit/cancel runtime execution and Phase 4 closeout remain pending.
