# P024 Phase Plan / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4h_real_partial_fill_runtime_feasibility_blocked
- Primary ADR: ADR-0007

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - output/account_command/ctp-paper-19053/
    - docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/
  allowed_evidence_roots:
    - docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/
    - docs/acceptance/p024-account-console-paper-command-controls/
  source_issue_lists: []
  source_input_templates:
    - docs/proposals/p023-openctp-19053-paper-command-capability/
  source_contract_templates:
    - contracts/account_command/
```

## ADR Decision Coverage Mapping

Primary ADR: ADR-0007

| ADR decision item | ADR section / successor scenario | Phase | Acceptance row |
| --- | --- | --- | --- |
| D1 governed command path | OrderIntent -> risk -> approval -> gateway -> readback -> reconciliation | Phase 1-4 | A1, A4, A6 |
| D2 Account Mirror never sends commands | Mirror remains read-only | Phase 1-4 | A2, N1 |
| D3 paper/live separation | `paper_armed` only in P024 | Phase 1-4 | A3, N8 |
| D4 idempotency | duplicate submit/click/retry | Phase 1-4 | A5, N3 |
| D5 cancel identity | cancel uses readback identity | Phase 1-4 | A7, A10, N4 |
| D6 gateway ack not final | UI/API status waits for readback/reconcile | Phase 1-4 | A8, A10, N5, N10 |
| D7 secret boundary | no raw broker secrets in worktree | Phase 1-4 | A9, N7 |

## AI Tracking Status

<!-- AI-PHASE-STATUS-BEGIN
reviewed_at: 2026-06-21
reviewer: codex
overall_status: phase4h_real_partial_fill_runtime_feasibility_blocked
phases:
  - id: phase_0_design_gate
    status: completed
    ai_progress: 100
    evidence: "python scripts\\validate_p024_paper_command_controls_design.py"
  - id: phase_1_backend_command_api
    status: completed_contract_gate
    ai_progress: 100
    evidence: "python scripts\\validate_p024_paper_command_api.py"
  - id: phase_2_frontend_guarded_controls
    status: completed_browser_contract_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-paper-command-controls.spec.ts --project=desktop; python scripts\\validate_p024_ui_command_controls_browser_evidence.py"
  - id: phase_3_browser_paper_submit_cancel
    status: planned
    ai_progress: 0
    evidence: "future Playwright and command runtime artifacts"
  - id: phase_3a_runtime_closeout_projection
    status: completed_browser_runtime_projection_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-runtime-closeout-evidence.spec.ts --project=desktop; python scripts\\validate_p024_runtime_closeout_browser_evidence.py"
  - id: phase_3b_partial_fill_cancel_ui_display
    status: completed_browser_display_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-partial-fill-cancel-order-display.spec.ts --project=desktop; python scripts\\validate_p024_partial_fill_cancel_browser_evidence.py"
  - id: phase_3c_owner_runtime_handoff_request
    status: completed_browser_handoff_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-runtime-handoff-request.spec.ts --project=desktop; python scripts\\validate_p024_runtime_handoff_browser_evidence.py"
  - id: phase_3d_owner_runtime_invocation_readiness
    status: completed_readiness_gate_blocked_by_external_approval
    ai_progress: 100
    evidence: "python scripts\\validate_p024_owner_runtime_invocation_readiness.py"
  - id: phase_3e_runtime_readiness_ui_projection
    status: completed_browser_readiness_projection_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-runtime-invocation-readiness.spec.ts --project=desktop; python scripts\\validate_p024_runtime_readiness_browser_evidence.py"
  - id: phase_4_closeout
    status: completed_residual_blocker_audit
    ai_progress: 100
    evidence: "python scripts\\validate_p024_full_acceptance_closeout.py"
  - id: phase_4a_owner_runtime_execution_approval_packet
    status: completed_approval_packet_gate_runtime_not_invoked
    ai_progress: 100
    evidence: "python scripts\\validate_p024_owner_runtime_execution_approval_packet.py"
  - id: phase_4b_runtime_approval_packet_ui_projection
    status: completed_browser_approval_packet_projection_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-runtime-execution-approval-packet.spec.ts --project=desktop; python scripts\\validate_p024_runtime_approval_packet_browser_evidence.py"
  - id: phase_4c_owner_runtime_execution_handoff_bundle
    status: completed_handoff_bundle_gate_runtime_not_invoked
    ai_progress: 100
    evidence: "python scripts\\validate_p024_owner_runtime_execution_handoff_bundle.py"
  - id: phase_4d_runtime_handoff_bundle_ui_projection
    status: completed_browser_handoff_bundle_projection_gate
    ai_progress: 100
    evidence: "npx playwright test tests/e2e/p024-runtime-execution-handoff-bundle.spec.ts --project=desktop; python scripts\\validate_p024_runtime_handoff_bundle_browser_evidence.py"
  - id: phase_4e_runtime_execution_gap_audit
    status: completed_final_gap_audit_gate_blocked_by_owner_runtime_execution
    ai_progress: 100
    evidence: "python scripts\\validate_p024_runtime_execution_gap_audit.py; npx playwright test tests/e2e/p024-runtime-execution-gap-audit.spec.ts --project=desktop; python scripts\\validate_p024_runtime_execution_gap_browser_evidence.py"
  - id: phase_4g_owner_runtime_submit_cancel_callback_closeout
    status: completed_owner_runtime_submit_cancel_callback_closed
    ai_progress: 100
    evidence: "python scripts\\validate_p024_owner_runtime_execution_attempt_audit.py"
  - id: phase_4h_real_partial_fill_runtime_feasibility
    status: blocked_until_owner_runtime_partial_fill_state_available
    ai_progress: 100
    evidence: "python scripts\\validate_p024_partial_fill_runtime_feasibility_audit.py"
AI-PHASE-STATUS-END -->

## Phase Status Board

| Phase | Goal | Current Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| Phase 0 Design gate | Freeze P024 scope, controls boundary and acceptance rows | completed | `python scripts\validate_p024_paper_command_controls_design.py` | Maintain design gate while implementation phases land |
| Phase 1 Backend command API | Add guarded paper-only command endpoints outside `/api/mirror` | completed_contract_gate | `python scripts\validate_p024_paper_command_api.py`; backend tests | Add frontend guarded controls after API contract |
| Phase 2 Frontend guarded controls | Show submit/cancel controls only when `command.mode=paper_armed` and refs exist | completed_browser_contract_gate | `npx playwright test tests/e2e/p024-paper-command-controls.spec.ts --project=desktop`; `python scripts\validate_p024_ui_command_controls_browser_evidence.py` | Add real browser submit/cancel runtime evidence |
| Phase 3 Browser paper submit/cancel | Prove Web UI submit/cancel round-trip through command audit and mirror readback | planned | future evidence | Run 19053 paper acceptance from UI |
| Phase 3a Runtime closeout projection | Render owner-backed P023 OpenCTP 19053 paper runtime closeout in Web UI with refs/checksums/non-claims | completed_browser_runtime_projection_gate | `npx playwright test tests/e2e/p024-runtime-closeout-evidence.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_closeout_browser_evidence.py` | Keep `browser_triggered_broker_order=false` until browser-triggered runtime exists |
| Phase 3b Partial-fill cancel display | Prove Web UI display correctness for S1 working, S2 partial, S3 cancel pending and S4 remaining cancelled | completed_browser_display_gate | `npx playwright test tests/e2e/p024-partial-fill-cancel-order-display.spec.ts --project=desktop`; `python scripts\validate_p024_partial_fill_cancel_browser_evidence.py` | Keep runtime partial-fill blocker until real or owner-approved partial-fill state exists |
| Phase 3c Owner-runtime handoff request | Prove Web UI prepares typed submit/cancel handoff requests for the owner runtime without invoking broker mutation | completed_browser_handoff_gate | `npx playwright test tests/e2e/p024-runtime-handoff-request.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_handoff_browser_evidence.py` | External owner runtime invocation remains blocked until approved outside this worktree |
| Phase 3d Owner-runtime invocation readiness | Freeze exact owner repo, guarded script entrypoints, argument shape, external write approval scope and post-run artifact requirements | completed_readiness_gate_blocked_by_external_approval | `python scripts\validate_p024_owner_runtime_invocation_readiness.py` | Ask for explicit approval before running owner scripts that may write outside this worktree and submit/cancel one paper order |
| Phase 3e Runtime readiness UI projection | Render owner-runtime readiness blocker in Web UI with owner refs, entrypoints, approval state and non-claims | completed_browser_readiness_projection_gate | `npx playwright test tests/e2e/p024-runtime-invocation-readiness.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_readiness_browser_evidence.py` | Keep owner-runtime execution blocked until explicit external approval and owner artifacts exist |
| Phase 4 Closeout | Full P024 gate set and residual blocker mapping | completed_residual_blocker_audit | `python scripts\validate_p024_full_acceptance_closeout.py` | Real owner-runtime execution still requires explicit external approval and checksum-backed owner artifacts |
| Phase 4a Owner-runtime execution approval packet | Freeze exact approval text, owner path, expected impact, guarded command templates and post-run artifact set | completed_approval_packet_gate_runtime_not_invoked | `python scripts\validate_p024_owner_runtime_execution_approval_packet.py` | Wait for operator to provide the exact approval text before any owner repo write or broker paper order attempt |
| Phase 4b Runtime approval packet UI projection | Render exact approval packet in Web UI with no owner runtime invocation or broker order claim | completed_browser_approval_packet_projection_gate | `npx playwright test tests/e2e/p024-runtime-execution-approval-packet.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_approval_packet_browser_evidence.py` | Wait for operator to provide the exact approval text before invoking owner runtime |
| Phase 4c Owner-runtime execution handoff bundle | Freeze post-approval operator sequence, runtime input requirements, owner artifact list and post-handoff gates | completed_handoff_bundle_gate_runtime_not_invoked | `python scripts\validate_p024_owner_runtime_execution_handoff_bundle.py` | Wait for explicit approval and runtime inputs before invoking owner runtime |
| Phase 4d Runtime handoff bundle UI projection | Render execution handoff bundle in Web UI with no execution allowed or broker order claim | completed_browser_handoff_bundle_projection_gate | `npx playwright test tests/e2e/p024-runtime-execution-handoff-bundle.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_handoff_bundle_browser_evidence.py` | Wait for explicit approval and runtime inputs before invoking owner runtime |
| Phase 4e Runtime execution gap audit | Render final A4 gap in Web UI without claiming all acceptance complete | completed_final_gap_audit_gate_blocked_by_owner_runtime_execution | `python scripts\validate_p024_runtime_execution_gap_audit.py`; `npx playwright test tests/e2e/p024-runtime-execution-gap-audit.spec.ts --project=desktop`; `python scripts\validate_p024_runtime_execution_gap_browser_evidence.py` | Obtain explicit approval and owner-runtime artifacts before declaring all acceptance complete |
| Phase 4g Owner-runtime submit/cancel callback closeout | Record approved owner-runtime paper submit/cancel attempt, owner cancel-loop repair and terminal cancel callback for the same native identity | completed_owner_runtime_submit_cancel_callback_closed | `python scripts\validate_p024_owner_runtime_execution_attempt_audit.py` | Keep real partial-fill runtime blocked until owner provides stable partial-fill order/trade readbacks |
| Phase 4h Real partial-fill runtime feasibility | Record why current owner evidence cannot satisfy partial-fill runtime truth and preserve the exact non-UI/Web UI acceptance shapes | blocked_until_owner_runtime_partial_fill_state_available | `python scripts\validate_p024_partial_fill_runtime_feasibility_audit.py` | Obtain fresh approval plus owner-generated partial-fill artifacts before declaring full acceptance |

## Runtime / Command Freeze

Phase 0 does not run broker mutation. Phase 1 may add API contracts but must not send broker commands until a paper command runner is explicitly invoked with paper-arm evidence. Any browser-triggered command must write intent, decision, gateway, readback and reconciliation artifacts under `output/account_command/ctp-paper-19053/<run-id>/`.

## Current Blockers

1. Browser controls are implemented only for `paper_armed` projection and currently stop at Phase 1 API `accepted_for_risk`.
2. Phase 3a displays existing owner-backed runtime closeout artifacts only; it does not create a new browser-triggered broker order.
3. Broker mutation from Web UI is not accepted yet because risk/approval/gateway/readback/reconciliation runtime chain is still future.
4. Live trading readiness remains out of scope.
5. Real partial-fill runtime remains blocked until a real or owner-approved partial-fill state is available.
6. Web UI owner-runtime handoff requests are accepted only as typed requests; `runtime_invocation_attempted=false` and `browser_triggered_broker_order=false` remain required until owner runtime execution is approved and ingested.
7. Phase 3d readiness is complete but real owner-runtime execution remains blocked because external write approval for `D:/Nautilus/nautilus_ctp_adapter` has not been granted in this thread.
8. Phase 3e readiness UI projection is complete; it displays the blocker and owner refs in Web UI but does not invoke owner runtime, write the owner repo or create broker orders.
9. Phase 4 residual blocker audit is complete; A1-A16 and all required gates are mapped, while new browser-triggered owner-runtime execution remains explicitly not accepted.
10. Phase 4a owner-runtime execution approval packet is complete; `owner-runtime-execution-approval-packet.json` and `P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK` freeze the exact approval text, while approval is still not obtained and `runtime_invocation_attempted=false`.
11. Phase 4b runtime approval packet UI projection is complete; `P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK` proves the exact approval packet is visible in Web UI while `approval_obtained=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.
12. Phase 4c owner-runtime execution handoff bundle is complete; `P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK` proves the post-approval sequence and runtime input requirements are frozen while `execution_allowed=false` and `runtime_invocation_attempted=false`.
13. Phase 4d runtime handoff bundle UI projection is complete; `P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK` proves the handoff bundle is visible in Web UI while `execution_allowed=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.
14. Phase 4e runtime execution gap audit is complete; `P024_RUNTIME_EXECUTION_GAP_AUDIT_OK` and `P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK` prove A4 remains visibly blocked until owner-runtime artifacts exist and `final_acceptance_claimed=false`.
15. Phase 4g owner-runtime submit/cancel callback closeout is complete; `P024_OWNER_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK` proves explicit approval was obtained, owner-owned submit/cancel scripts ran, owner patch `6a50b02` waited for cancel callbacks, and terminal cancel status `5` was observed for native order id `2081`. Real partial-fill runtime remains blocked.
16. Phase 4h real partial-fill runtime feasibility audit is complete as a typed blocker; `P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT_OK` proves no new partial-fill order was submitted, current artifacts have no trade fill, and both non-UI and Web UI real partial-fill acceptance remain blocked until owner partial-fill artifacts exist.
