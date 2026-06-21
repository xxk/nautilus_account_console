# P024 Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase1_backend_contract_gate_passed
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
| Current controls | No Web/API command controls are accepted yet | `python scripts\validate_p024_paper_command_controls_design.py` |
| Phase 1 backend API | P024 backend accepts paper `OrderIntent` and `CancelIntent` contract requests, stops before risk/approval/gateway and keeps Account Mirror read-only | `python scripts\validate_p024_paper_command_api.py` |

## Document Map

| File | Purpose |
| --- | --- |
| `phase-plan.md` | phased landing plan and artifact trust boundary |
| `acceptance.md` | non-UI and browser acceptance rows |
| `ui-design.md` | guarded command control surface design |
| `ui-acceptance.md` | Web UI acceptance and negative cases |
| `partial-fill-cancel-ui-acceptance.md` | Web UI partial-fill then cancel order-display correctness scenario |

## Graduation / Closeout Matrix

| Graduation item | Policy | Target | Status |
| --- | --- | --- | --- |
| ADR backfill | archive_only | ADR-0007 successor proposal list | design_gate_ready |
| Backend command API contract gate | archive_only | P024 paper intent API accepts submit/cancel requests and fails closed before gateway | phase1_backend_contract_gate_passed |
| Architecture / ownership backfill | required before implementation closeout | command gateway owner map | not_started |
| Proposal-local evidence | archive_only | `acceptance.md` and future browser/runtime evidence | phase1_backend_contract_gate_passed |

No stable rule graduation: proposal-local evidence only until implementation and runtime gates pass.
