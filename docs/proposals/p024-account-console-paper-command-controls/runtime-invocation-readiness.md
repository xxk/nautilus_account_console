# P024 Runtime Invocation Readiness / Owner Runtime Approval Gate

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4c_owner_runtime_execution_handoff_bundle_ready
- Previous readiness UI status: phase3e_runtime_readiness_ui_projection_passed
- Previous approval packet status: phase4a_owner_runtime_execution_approval_packet_ready

## Scope

This gate prepares the real owner-runtime invocation path without running it from this worktree. It records the owner repo, guarded script entrypoints, argument shape, expected owner write scope and explicit non-claims required before P024 can move from browser handoff to real OpenCTP paper runtime execution.

This is not broker execution evidence. It is a readiness and approval package.

Phase 4a adds an owner-runtime execution approval packet on top of this readiness package. That packet is also not broker execution evidence; it freezes the exact operator approval text and command templates needed before owner scripts may be invoked.

Phase 4b renders that approval packet in the Web UI as a browser blocker projection. This is still not owner-runtime invocation and still requires `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.

Phase 4c freezes the owner-runtime execution handoff bundle. The bundle records the post-approval sequence, runtime input requirements, required owner artifacts and post-handoff gates while `execution_allowed=false`.

## Required Artifact

`docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-invocation-readiness.json`

Required facts:

1. Owner runtime is `owner://nautilus_ctp_adapter`.
2. Submit entrypoint is `scripts/ctp_guarded_paper_order_loop.py`.
3. Cancel entrypoint is `scripts/ctp_guarded_paper_cancel_loop.py`.
4. Config is recorded only as `cfgs/local/ctp.openctp.tts.7x24.local.json`; raw config contents are not read or copied.
5. External write approval is required before running owner scripts.
6. `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false`, `browser_triggered_broker_order=false`, `gateway_send_attempted=false` and `broker_order_created=false`.
7. The readiness package must cite P023 predecessor closeout refs/checksums but must not treat them as new browser-triggered runtime evidence.

## Approval Boundary

Before any owner runtime execution, the operator must explicitly approve:

1. Exact path: `D:/Nautilus/nautilus_ctp_adapter`.
2. Reason: run owner-owned guarded OpenCTP paper submit/cancel scripts for P024.
3. Expected impact: create owner-owned runtime/debug/readback/reconciliation artifacts outside this worktree and potentially submit/cancel one paper order in the 19053 simulation account.

Without that approval, P024 remains blocked for real owner-runtime execution and must not claim real Web UI broker execution. The external write approval is required before any owner-runtime invocation.

The exact approval text required by the Phase 4a owner-runtime execution approval packet is:

```text
I approve writes to D:/Nautilus/nautilus_ctp_adapter to run owner-owned guarded OpenCTP paper submit/cancel scripts for P024; expected impact: create owner-owned runtime/debug/readback/reconciliation artifacts outside this worktree and may submit/cancel one paper order in the 19053 simulation account.
```

Machine artifact:

```text
docs/acceptance/p024-account-console-paper-command-controls/owner-runtime-execution-approval-packet.json
```

## Web UI Projection Gate

Phase 3e projects this readiness package into Account Workbench:

1. Backend route: `GET /api/commands/accounts/{account_id}/runtime-invocation-readiness`.
2. Web UI panel: `account-runtime-readiness-panel`.
3. Required false flags: `account-runtime-readiness-invoked`, `account-runtime-readiness-owner-write`, `account-runtime-readiness-browser-trigger`, `account-runtime-readiness-config-raw` and `account-runtime-readiness-raw-secret`.
4. Required visible blocker: external write approval is required and not obtained.
5. Required non-claim: `does_not_close_phase_3_runtime_execution`.

Run:

```powershell
npx playwright test tests/e2e/p024-runtime-invocation-readiness.spec.ts --project=desktop
python scripts\validate_p024_runtime_readiness_browser_evidence.py
```

Pass signal:

```text
P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK: runtime_readiness_ui=pass runtime_invocation_attempted=false external_write_approval=blocked
```

## Machine Gate

Run:

```powershell
python scripts\validate_p024_owner_runtime_invocation_readiness.py
```

Pass signal:

```text
P024_OWNER_RUNTIME_INVOCATION_READINESS_OK: readiness=pass runtime_invocation_attempted=false external_write_approval=required
```

## Execution Approval Packet Gate

Run:

```powershell
python scripts\validate_p024_owner_runtime_execution_approval_packet.py
```

Pass signal:

```text
P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK: status=phase4a_owner_runtime_execution_approval_packet_ready approval_required=true approval_obtained=false runtime_invocation_attempted=false
```

## Runtime Approval Packet UI Gate

Run:

```powershell
npx playwright test tests/e2e/p024-runtime-execution-approval-packet.spec.ts --project=desktop
python scripts\validate_p024_runtime_approval_packet_browser_evidence.py
```

Pass signal:

```text
P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK: runtime_approval_packet_ui=pass approval_obtained=false runtime_invocation_attempted=false
```

## Execution Handoff Bundle Gate

Run:

```powershell
python scripts\validate_p024_owner_runtime_execution_handoff_bundle.py
```

Pass signal:

```text
P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK: status=phase4c_owner_runtime_execution_handoff_bundle_ready execution_allowed=false runtime_invocation_attempted=false
```
