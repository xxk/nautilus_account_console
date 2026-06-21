# P024 Acceptance / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4zb_owner_repair_approval_packet_ui_projection_passed
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
| P024 full acceptance closeout audit | `python scripts\validate_p024_full_acceptance_closeout.py` | `P024_FULL_ACCEPTANCE_CLOSEOUT_OK` | A1-A16, accepted scope, non-accepted runtime scope and residual owner-runtime blockers are machine-checked |
| P024 owner-runtime execution approval packet | `python scripts\validate_p024_owner_runtime_execution_approval_packet.py` | `P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK` | Exact owner path, reason, expected impact, approval text, guarded command templates and post-run artifact set are machine-checked while `approval_obtained=false` and `runtime_invocation_attempted=false` |
| P024 runtime approval packet UI projection | `npx playwright test tests/e2e/p024-runtime-execution-approval-packet.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_approval_packet_browser_evidence.py` | `P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK` | Web UI renders the exact approval packet and preserves `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false` |
| P024 owner-runtime execution handoff bundle | `python scripts\validate_p024_owner_runtime_execution_handoff_bundle.py` | `P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK` | Post-approval operator sequence, runtime input requirements, required owner artifacts and post-handoff gates are machine-checked while `execution_allowed=false` |
| P024 runtime handoff bundle UI projection | `npx playwright test tests/e2e/p024-runtime-execution-handoff-bundle.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_handoff_bundle_browser_evidence.py` | `P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK` | Web UI renders the handoff bundle execution guard, runtime inputs, operator sequence, artifact counts and blockers while `execution_allowed=false` |
| P024 runtime execution gap audit | `python scripts\validate_p024_runtime_execution_gap_audit.py`; `npx playwright test tests/e2e/p024-runtime-execution-gap-audit.spec.ts --project=desktop` then `python scripts\validate_p024_runtime_execution_gap_browser_evidence.py` | `P024_RUNTIME_EXECUTION_GAP_AUDIT_OK`; `P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK` | Artifact/API/Web UI identify A4 as not accepted until owner-runtime artifacts exist and keep final acceptance claim false |
| P024 owner-runtime submit/cancel callback closeout | `python scripts\validate_p024_owner_runtime_execution_attempt_audit.py` | `P024_OWNER_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK` | Approved owner-runtime submit/cancel attempt observed accepted/reported submit callbacks and terminal cancel status `5` for the same native identity |
| P024 real partial-fill runtime feasibility | `python scripts\validate_p024_partial_fill_runtime_feasibility_audit.py` | `P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT_OK` | Documents the remaining real partial-fill blocker without submitting a new order or promoting UI fixture evidence to runtime truth |
| P024 owner artifact partial-fill scan | `python scripts\validate_p024_partial_fill_owner_artifact_scan.py` | `P024_PARTIAL_FILL_OWNER_ARTIFACT_SCAN_OK` | Scans current account-console and owner runtime JSON artifacts and rejects near candidates that are cancelled-without-fill or fully filled |
| P024 partial-fill runtime execution approval packet | `python scripts\validate_p024_partial_fill_runtime_execution_approval_packet.py` | `P024_PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET_OK` | Freezes exact approval text and one-attempt exposure-reduction constraints while `approval_obtained=false` |
| P024 partial-fill runtime approval packet UI projection | `npx playwright test tests/e2e/p024-partial-fill-runtime-execution-approval-packet.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_runtime_approval_packet_browser_evidence.py` | `P024_PARTIAL_FILL_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK` | Web UI renders exact partial-fill approval text, formulas, entrypoints and blockers while `new_order_submitted=false` and `cancel_sent=false` |
| P024 partial-fill runtime execution handoff bundle | `python scripts\validate_p024_partial_fill_runtime_execution_handoff_bundle.py` | `P024_PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK` | Freezes post-approval runtime inputs, success formulas and fallback classifications while `execution_allowed=false` |
| P024 partial-fill runtime handoff bundle UI projection | `npx playwright test tests/e2e/p024-partial-fill-runtime-execution-handoff-bundle.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_runtime_handoff_bundle_browser_evidence.py` | `P024_PARTIAL_FILL_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK` | Web UI renders partial-fill runtime inputs, owner sequence, success formulas and fallback classifications while `execution_allowed=false` |
| P024 partial-fill runtime execution attempt audit | `python scripts\validate_p024_partial_fill_runtime_execution_attempt_audit.py` | `P024_PARTIAL_FILL_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK` | Owner-owned guarded paper attempt is recorded as rejected-before-partial-fill with checksum-backed refs; no cancel identity was available and full acceptance remains false |
| P024 partial-fill close-offset owner rule gap audit | `python scripts\validate_p024_partial_fill_close_offset_owner_rule_gap_audit.py` | `P024_PARTIAL_FILL_CLOSE_OFFSET_OWNER_RULE_GAP_AUDIT_OK` | CLOSEYESTERDAY submit-boundary offset 4 versus rejected callback offset 1 is source-closed as an owner repair prerequisite before any retry |
| P024 partial-fill owner repair approval packet | `python scripts\validate_p024_partial_fill_owner_repair_approval_packet.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET_OK` | Current runtime-script approval is not enough for the repair-first next action; owner repair approval and post-repair retry gates are required before another paper attempt |
| P024 partial-fill owner repair approval packet UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-approval-packet.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_approval_packet_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET_BROWSER_EVIDENCE_OK` | Web UI renders the exact owner repair approval text, current-approval mismatch, owner changes, validators and blockers while owner write, runtime retry and full acceptance remain false |
| P024 partial-fill remaining acceptance current state | `python scripts\validate_p024_partial_fill_remaining_acceptance_current_state.py` | `P024_PARTIAL_FILL_REMAINING_ACCEPTANCE_CURRENT_STATE_OK` | Full acceptance remains false and the five remaining evidence requirements are machine-checked |
| P024 partial-fill owner repair implementation plan | `python scripts\validate_p024_partial_fill_owner_repair_implementation_plan.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN_OK` | Owner guarded-loop repair target, CLOSEYESTERDAY focused test requirements and no-retry gates are machine-checked before any owner write |
| P024 partial-fill owner repair plan UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-plan.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_plan_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_PLAN_BROWSER_EVIDENCE_OK` | Web UI renders the owner repair plan and keeps owner write, runtime retry, partial-fill claim and full acceptance claim false |
| P024 partial-fill owner repair evidence ingest gate | `python scripts\validate_p024_partial_fill_owner_repair_evidence_ingest_gate.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_GATE_OK` | `partial-fill-owner-repair-evidence-ingest-gate.json` freezes post-repair owner commit/checksum/validator evidence requirements while repair evidence is still missing and runtime retry remains false |
| P024 partial-fill owner repair ingest gate UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-ingest-gate.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_ingest_gate_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_INGEST_GATE_BROWSER_EVIDENCE_OK` | `partial-fill-owner-repair-ingest-gate-ui.json` proves Web UI renders owner repair evidence intake requirements and keeps owner repair evidence, runtime retry and full acceptance false |
| P024 partial-fill owner repair preflight source audit | `python scripts\validate_p024_partial_fill_owner_repair_preflight_source_audit.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_SOURCE_AUDIT_OK` | `partial-fill-owner-repair-preflight-source-audit.json` proves current owner source checksums still require CLOSEYESTERDAY offset 4 repair evidence and rejects blind script retry |
| P024 partial-fill owner repair preflight UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-preflight.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_preflight_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_BROWSER_EVIDENCE_OK` | `partial-fill-owner-repair-preflight-ui.json` proves Web UI renders the source audit and keeps owner write, runtime invocation, repair approval and full acceptance false |
| P024 partial-fill owner repair patch preview | `python scripts\validate_p024_partial_fill_owner_repair_patch_preview.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW_OK` | `partial-fill-owner-repair-patch-preview.json` freezes the owner source/test patch shape while owner write, runtime retry and full acceptance remain false |
| P024 partial-fill owner repair patch preview UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-patch-preview.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_patch_preview_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW_BROWSER_EVIDENCE_OK` | `partial-fill-owner-repair-patch-preview-ui.json` proves Web UI renders the patch preview and keeps owner write, patch applied, runtime retry and full acceptance false |
| P024 partial-fill owner repair execution handoff bundle | `python scripts\validate_p024_partial_fill_owner_repair_execution_handoff_bundle.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BUNDLE_OK` | `partial-fill-owner-repair-execution-handoff-bundle.json` freezes the post-approval operator sequence, validators, ingest artifacts and retry packet requirement while execution remains false |
| P024 partial-fill owner repair execution handoff UI projection | `npx playwright test tests/e2e/p024-partial-fill-owner-repair-execution-handoff.spec.ts --project=desktop` then `python scripts\validate_p024_partial_fill_owner_repair_execution_handoff_browser_evidence.py` | `P024_PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BROWSER_EVIDENCE_OK` | `partial-fill-owner-repair-execution-handoff-ui.json` proves Web UI renders the handoff sequence and keeps execution, owner write, runtime retry and full acceptance false |
| P023 runtime predecessor | `python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json` | `P023_OPENCTP19053_COMMAND_RUN_OK` | Predecessor paper command evidence |
| Proposal docs | `python scripts\check_proposal_docs.py --root . --proposal-id p024-account-console-paper-command-controls` | `PROPOSAL_DOCS_OK` | Proposal structure |

Browser evidence files for the new partial-fill runtime UI projections are
`docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-runtime-approval-packet-ui.json`
and
`docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-runtime-handoff-bundle-ui.json`.

Browser evidence for the owner repair approval packet UI projection is
`docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-approval-packet-ui.json`.

The latest owner-runtime attempt audit is
`docs/acceptance/p024-account-console-paper-command-controls/partial-fill-runtime-execution-attempt-audit.json`.

The close-offset semantic gap audit is
`docs/acceptance/p024-account-console-paper-command-controls/partial-fill-close-offset-owner-rule-gap-audit.json`.

## Scenario Matrix

| ID | Type | Scenario | Verification shape | Must fail if | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | positive | Backend command API accepts paper submit intent | API contract + command artifact validator | endpoint bypasses risk/approval | phase1_backend_contract_gate_passed |
| A2 | positive | Account Mirror remains read-only | route audit | `/api/mirror` exposes POST/PUT/DELETE | design_gate_ready |
| A3 | positive | Command controls render only in `paper_armed` mode | Playwright + API projection | controls appear while disabled | phase2_frontend_guarded_controls_passed |
| A4 | positive | Submit writes intent/risk/approval/gateway/readback/reconcile refs | integration + artifact validator | gateway ack alone is final | blocked_pending_owner_runtime_execution |
| A5 | positive | Submit idempotency prevents duplicate order | retry/duplicate-click test | duplicate broker order identity appears | phase2_frontend_guarded_controls_passed |
| A6 | positive | Risk/approval fail closed | negative API tests | missing risk/approval reaches gateway | passed_pre_gateway_contract_gate |
| A7 | positive | Cancel uses latest readback identity | API/browser + readback artifact | cancel uses UI row text or screenshot | phase1_backend_contract_gate_passed |
| A8 | positive | UI status waits for readback/reconcile | browser evidence | final state shown without readback/reconcile | passed_display_contract_real_runtime_blocked |
| A9 | positive | Secret redaction | artifact redaction gate | raw password/front/auth/token recorded | passed |
| A10 | positive | Partial fill then cancel Web UI order display correctness | Playwright + `partial-fill-cancel-ui-acceptance.md` + browser evidence JSON | identity changes, fill rows drift, or quantity formulas fail | phase3b_partial_fill_cancel_ui_display_passed |
| A11 | positive | Runtime closeout evidence appears in Web UI without browser-trigger claim | Playwright + API route audit + browser evidence JSON | UI hides refs/checksums, shows gateway ack final, or claims browser submitted broker order | phase3a_runtime_closeout_projection_passed |
| A12 | positive | Web UI prepares owner-runtime submit/cancel handoff without invoking broker runtime | Playwright + API route audit + browser evidence JSON | runtime invocation, gateway send or broker order creation is claimed from the browser | phase3c_runtime_handoff_request_passed |
| A13 | positive | Owner-runtime invocation readiness and external approval scope are frozen | readiness artifact + owner script checksum validator | owner repo path, script checksum, approval scope or non-claims drift | phase3d_owner_runtime_invocation_readiness_blocked_by_external_approval |
| A14 | positive | Runtime readiness blocker appears in Web UI without broker execution claims | Playwright + API route audit + browser evidence JSON | UI hides blocker, copies raw endpoint/secret data, or claims owner runtime was invoked | phase3e_runtime_readiness_ui_projection_passed |
| A15 | positive | Runtime handoff bundle appears in Web UI without execution permission | Playwright + API route audit + browser evidence JSON | UI claims execution allowed, owner write or broker order creation | phase4d_runtime_handoff_bundle_ui_projection_passed |
| A16 | blocker | Runtime execution gap is visible until owner-runtime artifacts exist | artifact validator + Playwright + API route audit + browser evidence JSON | UI or artifact claims full acceptance complete before A4 owner-runtime artifacts exist | phase4e_runtime_execution_gap_audit_passed |
| A17 | positive | Partial-fill runtime approval packet appears in Web UI before any owner submit/cancel | Playwright + API route audit + browser evidence JSON | UI hides exact approval text/formulas or claims new order/cancel was sent | phase4l_partial_fill_runtime_approval_packet_ui_projection_passed |
| A18 | positive | Partial-fill runtime handoff bundle appears in Web UI with success formulas and fallback classifications | Playwright + API route audit + browser evidence JSON | UI claims execution allowed, hides formulas, or promotes fixture evidence to runtime truth | phase4m_partial_fill_runtime_handoff_bundle_ui_projection_passed |
| A19 | blocker | Real owner-runtime partial-fill attempt is classified if it fails before partial fill | owner artifact refs/checksums + validator | rejected/no-fill attempt is counted as partial-fill acceptance or retry is authorized without new approval | phase4n_partial_fill_runtime_attempt_rejected_blocker_recorded |
| A20 | blocker | Owner close-offset repair approval is required before retry | repair approval packet validator + gap audit dependency | runtime-script approval is treated as owner code repair approval or a post-gap retry is authorized before repair evidence | phase4p_owner_close_offset_repair_approval_packet_ready |
| A21 | blocker | Remaining full-acceptance evidence is explicit and not claimed complete | current-state audit validator | any of owner repair, real partial-fill runtime, or Web UI real-ref projection is marked accepted without authoritative evidence | phase4q_remaining_acceptance_current_state_audited |
| A22 | blocker | Owner close-offset repair plan targets the exact CLOSEYESTERDAY gap without executing owner writes | implementation plan validator + owner read context | plan authorizes runtime retry, claims owner repair complete, or omits CLOSEYESTERDAY offset 4 focused tests | phase4r_owner_close_offset_repair_implementation_plan_ready |
| A23 | blocker | Owner repair implementation plan is visible from Web UI without execution claims | Playwright + API route audit + browser evidence JSON | UI hides the CLOSEYESTERDAY repair plan or claims owner write/runtime retry/partial-fill/full acceptance | phase4s_owner_repair_plan_ui_projection_passed |
| A24 | blocker | Owner repair evidence ingest gate rejects incomplete repair evidence | ingest gate validator | owner commit/checksum/validator evidence is missing, chat-only, secret-bearing, or used to authorize runtime retry | phase4t_owner_repair_evidence_ingest_gate_ready |
| A25 | blocker | Owner repair ingest gate is visible from Web UI without evidence/retry claims | Playwright + API route audit + browser evidence JSON | UI hides required commit/checksum/validator evidence shape or claims owner repair evidence/runtime retry/full acceptance | phase4u_owner_repair_ingest_gate_ui_projection_passed |
| A26 | blocker | Current owner source preflight rejects blind script retry before repair approval | source checksum audit + owner text checks | owner source already has unrecorded repair, checksum drifts, or scripts-only approval is treated as sufficient for code repair/runtime retry | phase4v_owner_repair_preflight_source_audited |
| A27 | blocker | Owner repair preflight source audit is visible from Web UI without execution claims | Playwright + API route audit + browser evidence JSON | UI hides owner source checksums or claims owner write/runtime invocation/repair approval/full acceptance | phase4w_owner_repair_preflight_ui_projection_passed |
| A28 | blocker | Owner repair patch preview freezes exact CLOSEYESTERDAY repair shape before owner write | patch preview validator + current owner baseline checksum | patch preview applies owner code, omits CLOSEYESTERDAY offset 4 focused assertions, authorizes retry, or claims validators/full acceptance | phase4x_owner_repair_patch_preview_ready |
| A29 | blocker | Owner repair patch preview is visible from Web UI without write/retry claims | Playwright + API route audit + browser evidence JSON | UI hides baseline files, patch steps or validators, or claims owner write/patch applied/runtime retry/full acceptance | phase4y_owner_repair_patch_preview_ui_projection_passed |
| A30 | blocker | Owner repair execution handoff bundle freezes post-approval sequence without execution claims | handoff bundle validator | sequence omits patch application, owner validators, evidence ingest or fresh retry approval packet, or claims execution/owner write/runtime retry/full acceptance | phase4z_owner_repair_execution_handoff_bundle_ready |
| A31 | blocker | Owner repair execution handoff is visible from Web UI without execution claims | Playwright + API route audit + browser evidence JSON | UI hides operator sequence or artifacts, or claims execution/owner write/runtime retry/full acceptance | phase4za_owner_repair_execution_handoff_ui_projection_passed |
| A32 | blocker | Owner repair approval packet is visible from Web UI before owner repair approval | Playwright + API route audit + browser evidence JSON | UI hides exact repair approval text, treats current scripts-only approval as sufficient, or claims owner write/runtime retry/partial-fill/full acceptance | phase4zb_owner_repair_approval_packet_ui_projection_passed |

## Phase 4e Runtime Execution Gap Audit

P024 Phase 4e is final blocker evidence for the original "all acceptance" goal. It must not claim that all acceptance is complete.

Required artifact and UI projection:

1. `docs/acceptance/p024-account-console-paper-command-controls/runtime-execution-gap-audit.json`.
2. Backend exposes `GET /api/commands/accounts/{account_id}/runtime-execution-gap-audit` as a read-only projection.
3. The response uses schema `account-console.p024.runtime-execution-gap-audit.v1`.
4. The Web UI displays `account-runtime-execution-gap-panel`, `account-runtime-execution-gap-status`, `account-runtime-execution-gap-final-claimed`, A4 not-accepted evidence, approval state, runtime/owner-write/broker-order false flags and residual blockers.
5. `account-runtime-execution-gap-final-claimed`, `account-runtime-execution-gap-approval-obtained`, `account-runtime-execution-gap-invoked`, `account-runtime-execution-gap-owner-write` and `account-runtime-execution-gap-broker-order` must all show `false`.
6. The artifact and UI preserve `verdict=blocked_pending_owner_runtime_execution` until external approval and checksum-backed owner-runtime artifacts exist.

Accepted evidence: `python scripts\validate_p024_runtime_execution_gap_audit.py` returns `P024_RUNTIME_EXECUTION_GAP_AUDIT_OK`, and `python scripts\validate_p024_runtime_execution_gap_browser_evidence.py` returns `P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK`.

## Phase 4 Full Acceptance Closeout Audit

P024 Phase 4 is a residual blocker audit, not a claim that real Web UI owner-runtime execution has happened.

Required artifact:

1. `docs/acceptance/p024-account-console-paper-command-controls/full-acceptance-closeout.json`.
2. `status=phase4_residual_blocker_audit_passed`.
3. `verdict=accepted_with_residual_owner_runtime_blockers`.
4. A1-A16 are enumerated with evidence refs or typed blockers.
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

## Phase 4g Owner Runtime Submit/Cancel Callback Closeout

This gate records the real owner-runtime attempt after explicit approval:

1. `docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-execution-attempt-audit.json` uses schema `account-console.p024.owner-runtime-execution-attempt-audit.v1`.
2. The artifact records `approval_obtained=true` for the approved owner repo path and keeps raw CTP secrets, auth values and broker endpoints out of this worktree.
3. Owner-owned `scripts/ctp_guarded_paper_order_loop.py` submitted a guarded `rb2610 SELL 1 CLOSEYESTERDAY` exposure-reduction paper order and observed an accepted `OnRtnOrder` with native order identity and `leaves_qty=1`.
4. Owner-owned `scripts/ctp_guarded_paper_cancel_loop.py` was repaired in owner commit `6a50b02` to wait for native cancel callbacks and match by native order identity.
5. The approved rerun sent cancel with the native order identity and observed terminal status `5` for native order id `2081`, order ref `2`, callback source `OnRtnOrder`.
6. Post-cancel snapshot preserved rb2610 position quantity at 3 and no trade fill was observed, so simple submit/cancel order-display correctness is accepted against owner-runtime callback truth.
7. Full acceptance remains blocked by real partial-fill runtime state; P024 still must not claim a real partial-fill sequence unless owner runtime provides stable partial-fill order and trade readbacks.

Accepted evidence: `python scripts\validate_p024_owner_runtime_execution_attempt_audit.py` returns `P024_OWNER_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK`. This is real owner-runtime submit/cancel callback evidence, not real partial-fill runtime evidence.

The previous `external owner-runtime approval` blocker is now satisfied for this single guarded 19053 paper attempt only; it does not grant live readiness, unrestricted order mutation or future owner-repo writes without matching approval.

## Phase 4h Real Partial-Fill Runtime Feasibility Audit

This gate records why the remaining partial-fill acceptance cannot be declared from the current artifacts:

1. `docs/acceptance/p024-account-console-paper-command-controls/partial-fill-runtime-feasibility-audit.json` uses schema `account-console.p024.partial-fill-runtime-feasibility-audit.v1`.
2. The prior approval covered one submit/cancel attempt and is recorded as consumed by `account-console-p024-runtime-20260621T090820Z`; this audit submits no new order.
3. Owner runtime code can classify `trade_volume`, `leaves_qty` and `filled_before_cancel` if callbacks are emitted.
4. The latest real attempt observed submit leaves quantity and terminal cancel status `5`, but observed no trade fill and no partial fill.
5. `partial-fill-owner-artifact-scan.json` scans current account-console and owner runtime JSON artifacts: 58 order-like records, zero qualifying partial-fill then cancel candidates.
6. Near candidates are rejected explicitly: P023 order `166` was cancelled without fill; P077 orders `183` and `232` were fully filled, not partial-fill then cancel.
7. Required non-UI acceptance remains owner artifacts plus checksums with `0 < filled_quantity < submitted_quantity` and terminal cancellation of the remainder.
8. Required Web UI acceptance remains Playwright evidence cross-checking owner refs/checksums, stable order identity, stable fill rows and final readback/reconciliation refs.
9. Full acceptance remains blocked by `p024_real_partial_fill_runtime_missing`.

Accepted evidence: `python scripts\validate_p024_partial_fill_runtime_feasibility_audit.py` returns `P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT_OK` with `blocked_until_owner_runtime_partial_fill_state_available`. This is a typed blocker audit, not a real partial-fill pass.
The companion scan evidence is accepted when `python scripts\validate_p024_partial_fill_owner_artifact_scan.py` returns `P024_PARTIAL_FILL_OWNER_ARTIFACT_SCAN_OK`.

## Phase 4j/4k Partial-Fill Runtime Execution Approval And Handoff

The next real step is prepared but not executed:

1. `partial-fill-runtime-execution-approval-packet.json` requires exact approval text before any owner repo write or paper order mutation.
2. The approval scope is limited to one small exposure-reduction paper order in account `acct.ctp.paper.19053`.
3. The exact approval text is: `I approve writes to D:/Nautilus/nautilus_ctp_adapter to run owner-owned guarded OpenCTP paper submit/cancel scripts for P024 partial-fill acceptance; expected impact: create owner-owned runtime/debug/readback/reconciliation artifacts outside this worktree and may submit/cancel up to one small exposure-reduction paper order in the 19053 simulation account.`
4. `partial-fill-runtime-execution-handoff-bundle.json` requires fresh owner pre-snapshot, reducible rb2610 exposure, quantity `2` or `3`, owner-reviewed limit price, and owner readback identity for cancel.
5. Success requires same native order identity, `0 < filled_quantity < submitted_quantity`, `filled_quantity + cancelled_quantity == submitted_quantity`, `remaining_quantity == 0` after terminal cancel readback, and redaction evidence.
6. Fully filled, cancelled-without-fill, rejected/timeout or incomplete artifacts remain typed blockers and must not be promoted to full acceptance.

Accepted evidence: `python scripts\validate_p024_partial_fill_runtime_execution_approval_packet.py` returns `P024_PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET_OK`, and `python scripts\validate_p024_partial_fill_runtime_execution_handoff_bundle.py` returns `P024_PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK`.

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

Implementation/browser evidence is required before implementation closeout. Phase 1, Phase 2, Phase 3a, Phase 3b, Phase 3c, Phase 3d readiness, Phase 3e readiness UI projection, Phase 4 residual blocker audit, Phase 4a owner-runtime execution approval packet, Phase 4b runtime approval packet UI projection, Phase 4c owner-runtime execution handoff bundle, Phase 4d runtime handoff bundle UI projection, Phase 4e runtime execution gap audit and Phase 4g owner-runtime submit/cancel callback closeout gates are accepted; full real partial-fill acceptance remains blocked pending real or owner-approved partial-fill runtime state.






