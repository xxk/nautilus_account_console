# P024 Runtime Invocation Readiness / Owner Runtime Approval Gate

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase3d_owner_runtime_invocation_readiness_blocked_by_external_approval

## Scope

This gate prepares the real owner-runtime invocation path without running it from this worktree. It records the owner repo, guarded script entrypoints, argument shape, expected owner write scope and explicit non-claims required before P024 can move from browser handoff to real OpenCTP paper runtime execution.

This is not broker execution evidence. It is a readiness and approval package.

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

Without that approval, P024 remains blocked at Phase 3d and must not claim real Web UI broker execution. The external write approval is required before any owner-runtime invocation.

## Machine Gate

Run:

```powershell
python scripts\validate_p024_owner_runtime_invocation_readiness.py
```

Pass signal:

```text
P024_OWNER_RUNTIME_INVOCATION_READINESS_OK: readiness=pass runtime_invocation_attempted=false external_write_approval=required
```
