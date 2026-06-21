# P024 Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4_residual_blocker_audit_passed
- ADR carrier: yes
- Primary ADR: ADR-0007
- Predecessor: [P023 OpenCTP 19053 Paper Command Capability](../p023-openctp-19053-paper-command-capability/README.md)
- Account: `acct.ctp.paper.19053`

## Purpose

P024 is the successor proposal that carries ADR-0007 beyond P023's non-goal. P023 accepted real OpenCTP 19053 paper submit/cancel runtime evidence and read-only UI command status evidence; P024 defines the Web/API paper command controls that can use that governed command path.

P024 does not enable `live_armed`, production admission, capital approval, or Account Mirror write authority. It is a paper-only controls proposal for guarded submit and cancel on `acct.ctp.paper.19053`.

## Goals

1. Add a guarded backend command API that accepts `OrderIntent` and `CancelIntent` for `paper_armed` only.
2. Add Account Workbench paper command controls only when command capability evidence explicitly allows `submit` and `cancel`.
3. Preserve risk/approval/gateway/readback/reconciliation evidence in command status.
4. Reject gateway-ack-only final state, missing idempotency, missing risk/approval, stale readback identity, and duplicate submit.
5. Keep Account Mirror read-only.
6. Preserve correct Web UI order display across partial-fill then cancel lifecycle: same order identity, stable fill rows, correct remaining/cancelled quantities and explicit readback provenance.
7. Render owner-backed OpenCTP 19053 paper runtime closeout artifacts in the Web UI without claiming a browser-triggered broker order.
8. Prepare typed Web UI owner-runtime submit/cancel handoff requests while preserving `runtime_invocation_attempted=false` and `browser_triggered_broker_order=false`.
9. Freeze the external owner-runtime invocation readiness package: owner repo, guarded entrypoints, argument shape, expected write scope, required approval and post-run artifact requirements.
10. Render the owner-runtime readiness package in the Web UI as an explicit blocker with owner refs, entrypoints, approval state and non-claims.

## Non-Goals

1. No live broker mutation.
2. No `live_armed` mode.
3. No replace/modify order.
4. No direct CTP calls from the browser.
5. No Account Mirror broker writer.
6. No use of screenshots, browser text, debug/latest paths or TickTrader UI state as command truth.

## Reality Snapshot

| Dimension | Current fact | Evidence |
| --- | --- | --- |
| P023 paper runtime | Real OpenCTP 19053 paper submit/cancel/readback accepted | `python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json` |
| P023 UI status | Read-only status evidence accepted; command controls disabled | `python scripts\validate_p023_ui_status_browser_evidence.py` |
| P024 design gate | Proposal docs, ADR coverage and command boundary remain machine-checked | `python scripts\validate_p024_paper_command_controls_design.py` |
| Current controls | Guarded Web/API paper command controls are accepted as browser/API contract gates only | `python scripts\validate_p024_ui_command_controls_browser_evidence.py` |
| Phase 1 backend API | P024 backend accepts paper `OrderIntent` and `CancelIntent` contract requests, stops before risk/approval/gateway and keeps Account Mirror read-only | `python scripts\validate_p024_paper_command_api.py` |
| Phase 2 frontend controls | Web UI hides controls while disabled, mounts submit/cancel only for `paper_armed` projection, calls P024 API and keeps gateway send false | `python scripts\validate_p024_ui_command_controls_browser_evidence.py` |
| Phase 3a runtime closeout projection | Web UI renders P023 owner-backed runtime closeout refs/checksums/non-claims and keeps `browser_triggered_broker_order=false` | `python scripts\validate_p024_runtime_closeout_browser_evidence.py` |
| Phase 3b partial-fill display | Web UI order display contract passes S1 working, S2 partial, S3 cancel pending and S4 remaining cancelled with stable fill/order identities | `python scripts\validate_p024_partial_fill_cancel_browser_evidence.py` |
| Phase 3c runtime handoff request | Web UI prepares owner-runtime submit/cancel handoff requests with blocked owner invocation and no browser-triggered broker order claim | `python scripts\validate_p024_runtime_handoff_browser_evidence.py` |
| Phase 3d runtime invocation readiness | Owner-runtime readiness package records external write approval scope, owner entrypoint checksums and post-run artifact requirements while runtime remains uninvoked | `python scripts\validate_p024_owner_runtime_invocation_readiness.py` |
| Phase 3e runtime readiness UI projection | Web UI renders owner-runtime readiness blocker, owner repo refs, entrypoints, approval state and non-claims while `runtime_invocation_attempted=false` | `python scripts\validate_p024_runtime_readiness_browser_evidence.py` |
| Phase 4 residual blocker closeout | Full P024 gate matrix records accepted scope, non-accepted runtime scope and remaining owner-runtime blockers as a full residual blocker closeout audit | `python scripts\validate_p024_full_acceptance_closeout.py` |

## Document Map

| File | Purpose |
| --- | --- |
| `phase-plan.md` | phased landing plan and artifact trust boundary |
| `acceptance.md` | non-UI and browser acceptance rows |
| `ui-design.md` | guarded command control surface design |
| `ui-acceptance.md` | Web UI acceptance and negative cases |
| `partial-fill-cancel-ui-acceptance.md` | Web UI partial-fill then cancel order-display correctness scenario |
| `runtime-invocation-readiness.md` | owner-runtime invocation readiness and external approval boundary |

## Graduation / Closeout Matrix

| Graduation item | Policy | Target | Status |
| --- | --- | --- | --- |
| ADR backfill | archive_only | ADR-0007 successor proposal list | design_gate_ready |
| Backend command API contract gate | archive_only | P024 paper intent API accepts submit/cancel requests and fails closed before gateway | phase1_backend_contract_gate_passed |
| Frontend guarded controls | archive_only | Browser evidence proves disabled controls absent and `paper_armed` controls route to Phase 1 API with no gateway send | phase2_frontend_guarded_controls_passed |
| Runtime closeout projection | archive_only | Browser evidence proves owner-backed P023 runtime closeout is displayed with refs/checksums/non-claims and no browser-trigger claim | phase3a_runtime_closeout_projection_passed |
| Partial-fill cancel display | archive_only | Browser evidence proves S1-S4 order/fill display correctness and typed runtime blocker | phase3b_partial_fill_cancel_ui_display_passed |
| Runtime handoff request | archive_only | Browser evidence proves submit/cancel prepare owner-runtime run requests while owner runtime invocation, gateway send and broker order creation remain false | phase3c_runtime_handoff_request_passed |
| Runtime invocation readiness | archive_only | Machine evidence proves owner repo, guarded entrypoints, approval scope and post-run artifact requirements are frozen while external write approval remains required | phase3d_owner_runtime_invocation_readiness_blocked_by_external_approval |
| Runtime readiness UI projection | archive_only | Browser evidence proves the readiness blocker is visible in Web UI with no owner-runtime invocation, owner write, browser-triggered broker order or raw secret claim | phase3e_runtime_readiness_ui_projection_passed |
| Architecture / ownership backfill | required before implementation closeout | command gateway owner map | phase4_owner_boundary_backfill_passed |
| Phase 4 residual blocker closeout | archive_only | `full-acceptance-closeout.json` maps A1-A14, required gates, non-accepted runtime scope and residual owner-runtime blockers | phase4_residual_blocker_audit_passed |
| Proposal-local evidence | archive_only | `acceptance.md`, browser command-controls evidence, runtime closeout projection evidence, P024 partial-fill display evidence, runtime handoff request evidence, owner-runtime invocation readiness evidence, runtime readiness UI projection evidence and full acceptance closeout audit; runtime Web UI broker command execution remains blocked pending external approval | phase4_residual_blocker_audit_passed |

No stable rule graduation: proposal-local evidence only until implementation and runtime gates pass.
