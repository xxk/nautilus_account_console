# P024 Phase Plan / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase3c_runtime_handoff_request_passed
- Primary ADR: ADR-0007

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - output/account_command/ctp-paper-19053/
    - docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/
  allowed_evidence_roots:
    - docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/
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
overall_status: phase3c_runtime_handoff_request_passed
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
  - id: phase_4_closeout
    status: planned
    ai_progress: 0
    evidence: "future full gate set"
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
| Phase 4 Closeout | Full P024 gate set and residual blocker mapping | planned | future evidence | Close only after implementation/browser evidence |

## Runtime / Command Freeze

Phase 0 does not run broker mutation. Phase 1 may add API contracts but must not send broker commands until a paper command runner is explicitly invoked with paper-arm evidence. Any browser-triggered command must write intent, decision, gateway, readback and reconciliation artifacts under `output/account_command/ctp-paper-19053/<run-id>/`.

## Current Blockers

1. Browser controls are implemented only for `paper_armed` projection and currently stop at Phase 1 API `accepted_for_risk`.
2. Phase 3a displays existing owner-backed runtime closeout artifacts only; it does not create a new browser-triggered broker order.
3. Broker mutation from Web UI is not accepted yet because risk/approval/gateway/readback/reconciliation runtime chain is still future.
4. Live trading readiness remains out of scope.
5. Real partial-fill runtime remains blocked until a real or owner-approved partial-fill state is available.
6. Web UI owner-runtime handoff requests are accepted only as typed requests; `runtime_invocation_attempted=false` and `browser_triggered_broker_order=false` remain required until owner runtime execution is approved and ingested.
