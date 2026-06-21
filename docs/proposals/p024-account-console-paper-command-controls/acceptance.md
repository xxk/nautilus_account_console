# P024 Acceptance / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4d_runtime_handoff_bundle_ui_projection_passed
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
| P024 owner-runtime invocation readiness | `python scripts\validate_p024_owner_runtime_invocation_readiness.py` | `P024_OWNER_RUNTIME_INVOCATION_READINESS_OK` | Owner repo, guarded script checksums, external write approval scope and post-run artifact requirements are frozen; runtime remains uninvoked |
| P024 runtime readiness UI projection | `npx playwright test tests/e2e/p024-runtime-invocation-readiness.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_readiness_browser_evidence.py` | `P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK` | Web UI renders readiness blocker, owner refs, entrypoints, approval state and non-claims without owner runtime invocation |
| P024 full acceptance closeout audit | `python scripts\validate_p024_full_acceptance_closeout.py` | `P024_FULL_ACCEPTANCE_CLOSEOUT_OK` | A1-A15, accepted scope, non-accepted runtime scope and residual owner-runtime blockers are machine-checked |
| P024 owner-runtime execution approval packet | `python scripts\validate_p024_owner_runtime_execution_approval_packet.py` | `P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK` | Exact owner path, reason, expected impact, approval text, guarded command templates and post-run artifact set are machine-checked while `approval_obtained=false` and `runtime_invocation_attempted=false` |
| P024 runtime approval packet UI projection | `npx playwright test tests/e2e/p024-runtime-execution-approval-packet.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_approval_packet_browser_evidence.py` | `P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK` | Web UI renders the exact approval packet and preserves `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false` |
| P024 owner-runtime execution handoff bundle | `python scripts\validate_p024_owner_runtime_execution_handoff_bundle.py` | `P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK` | Post-approval operator sequence, runtime input requirements, required owner artifacts and post-handoff gates are machine-checked while `execution_allowed=false` |
| P024 runtime handoff bundle UI projection | `npx playwright test tests/e2e/p024-runtime-execution-handoff-bundle.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_handoff_bundle_browser_evidence.py` | `P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK` | Web UI renders the handoff bundle execution guard, runtime inputs, operator sequence, artifact counts and blockers while `execution_allowed=false` |
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
| A13 | positive | Owner-runtime invocation readiness and external approval scope are frozen | readiness artifact + owner script checksum validator | owner repo path, script checksum, approval scope or non-claims drift | phase3d_owner_runtime_invocation_readiness_blocked_by_external_approval |
| A14 | positive | Runtime readiness blocker appears in Web UI without broker execution claims | Playwright + API route audit + browser evidence JSON | UI hides blocker, copies raw endpoint/secret data, or claims owner runtime was invoked | phase3e_runtime_readiness_ui_projection_passed |

## Phase 4 Full Acceptance Closeout Audit

P024 Phase 4 is a residual blocker audit, not a claim that real Web UI owner-runtime execution has happened.

Required artifact:

1. `docs/acceptance/p024-account-console-paper-command-controls/full-acceptance-closeout.json`.
2. `status=phase4_residual_blocker_audit_passed`.
3. `verdict=accepted_with_residual_owner_runtime_blockers`.
4. A1-A15 are enumerated with evidence refs or typed blockers.
5. Non-accepted runtime scope includes new browser-triggered owner-runtime submit/cancel execution, gateway send from Web UI, broker order creation from Web UI, real partial-fill runtime, live mode, Account Mirror write authority and replace/modify orders.
6. Residual blockers include external owner-runtime write approval, missing owner-runtime artifacts and missing real partial-fill runtime state.
7. Negative assertions require `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false`, `browser_triggered_broker_order=false`, `gateway_send_attempted_from_browser=false`, `broker_order_created_from_browser=false`, `live_armed=false`, `account_mirror_write_authority=false` and `full_runtime_acceptance_claimed=false`.

Accepted evidence: `python scripts\validate_p024_full_acceptance_closeout.py` returns `P024_FULL_ACCEPTANCE_CLOSEOUT_OK`.

## Phase 4a Owner Runtime Execution Approval Packet

P024 Phase 4a is the executable approval packet for the next owner-runtime step. It still does not run owner scripts or create a broker order.

Required artifact:

1. `docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-execution-approval-packet.json`.
2. `status=phase4a_owner_runtime_execution_approval_packet_ready`.
3. `verdict=approval_packet_ready_runtime_not_invoked`.
4. The packet records exact path `D:/Nautilus/nautilus_ctp_adapter`, reason, expected impact and command templates for submit/cancel.
5. The exact required approval text is: `I approve writes to D:/Nautilus/nautilus_ctp_adapter to run owner-owned guarded OpenCTP paper submit/cancel scripts for P024; expected impact: create owner-owned runtime/debug/readback/reconciliation artifacts outside this worktree and may submit/cancel one paper order in the 19053 simulation account.`
6. Negative assertions require `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false`, `browser_triggered_broker_order=false`, `gateway_send_attempted=false`, `broker_order_created=false`, `raw_secret_values_recorded=false` and `raw_broker_endpoint_recorded=false`.

Accepted evidence: `python scripts\validate_p024_owner_runtime_execution_approval_packet.py` returns `P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK`.

## Phase 4b Runtime Approval Packet UI Projection

The Web UI must render the Phase 4a approval packet as an explicit pre-execution blocker:

1. Backend exposes `GET /api/commands/accounts/{account_id}/runtime-execution-approval-packet` as a read-only projection.
2. The response uses schema `account-console.p024.owner-runtime-execution-approval-packet.v1`.
3. The Web UI displays `account-runtime-approval-packet-panel`, `account-runtime-approval-packet-status`, `account-runtime-approval-packet-owner-path`, approval required/obtained flags, `account-runtime-approval-packet-exact-text`, entrypoints and blockers.
4. `account-runtime-approval-packet-obtained`, `account-runtime-approval-packet-invoked`, `account-runtime-approval-packet-owner-write` and `account-runtime-approval-packet-broker-order` must all show `false`.
5. UI text must not include raw broker endpoints, raw front-address wording, live-ready wording or browser-submitted broker-order claims.

Accepted evidence: `python scripts\validate_p024_runtime_approval_packet_browser_evidence.py` returns `P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK`.

## Phase 4c Owner Runtime Execution Handoff Bundle

P024 Phase 4c freezes the post-approval execution sequence without invoking owner runtime.

Required artifact:

1. `docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-execution-handoff-bundle.json`.
2. `status=phase4c_owner_runtime_execution_handoff_bundle_ready`.
3. `verdict=handoff_bundle_ready_runtime_not_invoked`.
4. `execution_allowed=false`, `approval_obtained=false`, `runtime_invocation_attempted=false` and `owner_repo_write_attempted=false`.
5. Runtime input requirements include fresh owner pre/post snapshot refs, instrument, side, quantity, price and readback order identity.
6. Operator sequence is gated: approval, owner repo context, submit runtime, submit readback, cancel runtime, post-run ingest and browser closeout.
7. Required owner artifacts and post-handoff gates match the approval packet and closeout gates.

Accepted evidence: `python scripts\validate_p024_owner_runtime_execution_handoff_bundle.py` returns `P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK`.

## Phase 4d Runtime Handoff Bundle UI Projection

The Web UI must render the Phase 4c handoff bundle as an explicit pre-execution blocker:

1. Backend exposes `GET /api/commands/accounts/{account_id}/runtime-execution-handoff-bundle` as a read-only projection.
2. The response uses schema `account-console.p024.owner-runtime-execution-handoff-bundle.v1`.
3. The Web UI displays `account-runtime-handoff-bundle-panel`, `account-runtime-handoff-bundle-status`, execution allowed/approval/runtime/owner-write/broker-order false flags, runtime inputs, operator sequence, artifact count, gate count and blockers.
4. `account-runtime-handoff-bundle-execution-allowed`, `account-runtime-handoff-bundle-approval-obtained`, `account-runtime-handoff-bundle-invoked`, `account-runtime-handoff-bundle-owner-write` and `account-runtime-handoff-bundle-broker-order` must all show `false`.
5. UI text must not include raw broker endpoints, raw front-address wording, live-ready wording or browser-submitted broker-order claims.

Accepted evidence: `python scripts\validate_p024_runtime_handoff_bundle_browser_evidence.py` returns `P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK`.

## Phase 3e Runtime Readiness UI Projection Acceptance

The Web UI must render the Phase 3d readiness package as an explicit blocker:

1. Backend exposes `GET /api/commands/accounts/{account_id}/runtime-invocation-readiness` as a read-only projection.
2. The response uses schema `account-console.p024.owner-runtime-invocation-readiness.v1`.
3. The Web UI displays `account-runtime-readiness-panel`, `account-runtime-readiness-status`, owner repo ref/path, config ref, entrypoint refs, approval required/obtained flags, blockers and explicit non-claims.
4. `account-runtime-readiness-invoked`, `account-runtime-readiness-owner-write`, `account-runtime-readiness-browser-trigger`, `account-runtime-readiness-config-raw` and `account-runtime-readiness-raw-secret` must all show `false`.
5. UI text must not include raw broker endpoints, raw front-address wording, live-ready wording or browser-submitted broker-order claims.

Accepted evidence: `python scripts\validate_p024_runtime_readiness_browser_evidence.py` returns `P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK`. This is a browser projection of a blocker, not owner-runtime execution.

## Phase 3d Owner Runtime Invocation Readiness Acceptance

This gate prepares real owner-runtime execution but does not run it:

1. `docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-invocation-readiness.json` uses schema `account-console.p024.owner-runtime-invocation-readiness.v1`.
2. The readiness artifact cites owner `owner://nautilus_ctp_adapter`, owner repo path, submit/cancel guarded entrypoints and script checksums.
3. The config is recorded only as `cfgs/local/ctp.openctp.tts.7x24.local.json`; raw config contents, broker endpoints and secrets are not read or copied.
4. External write approval is required for `D:/Nautilus/nautilus_ctp_adapter` before any owner runtime invocation.
5. `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false`, `browser_triggered_broker_order=false`, `gateway_send_attempted=false`, `broker_order_created=false`, `raw_secret_values_recorded=false` and `raw_broker_endpoint_recorded=false` are required.
6. Post-run required artifacts are enumerated before execution: intents, risk decisions, approvals, gateway events, readbacks, reconciliation, redaction report, command audit and closeout manifest.

Accepted evidence: `python scripts\validate_p024_owner_runtime_invocation_readiness.py` returns `P024_OWNER_RUNTIME_INVOCATION_READINESS_OK`. This is still not real broker execution evidence; it is the exact approval and readiness boundary for the next step.

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
| N13 | owner runtime is executed or owner repo is written before explicit approval | reject; preserve external write approval blocker |

## UI Anti-Drift Acceptance

| ID | Drift | forbidden_actions | forbidden_claims | Required rejection |
| --- | --- | --- | --- | --- |
| UAD-01 | Disabled account shows controls | submit, cancel, replace | Paper ready, can trade | controls absent |
| UAD-02 | Browser calls broker directly | CTP/TWS browser mutation | broker truth from UI | browser test fails |
| UAD-03 | Gateway ack shown as final | final success without readback | command complete | blocker |
| UAD-04 | Live control appears | live submit/cancel | live ready | reject |
| UAD-05 | Runtime handoff panel claims owner runtime was invoked from browser | owner runtime send | broker order created by browser | reject |
| UAD-06 | Readiness artifact copies raw owner config, endpoint or secret values | owner config read/copy | broker endpoint truth in this repo | reject |

## Evidence Boundary

Implementation/browser evidence is required before implementation closeout. Phase 1, Phase 2, Phase 3a, Phase 3b, Phase 3c, Phase 3d readiness, Phase 3e readiness UI projection, Phase 4 residual blocker audit, Phase 4a owner-runtime execution approval packet, Phase 4b runtime approval packet UI projection, Phase 4c owner-runtime execution handoff bundle and Phase 4d runtime handoff bundle UI projection gates are accepted; real Web UI submit/cancel runtime execution remains blocked pending external owner-runtime approval and artifacts.
