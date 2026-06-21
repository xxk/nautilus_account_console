# P023 OpenCTP 19053 Paper Command Capability / OpenCTP 19053 Paper 下单撤单能力

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Updated: 2026-06-21
- ADR carrier: yes
- Primary ADR: ADR-0007
- Predecessors: ADR-0004, ADR-0005, P022
- Account: `acct.ctp.paper.19053`
- Broker profile: OpenCTP TTS 7x24 simulation

## Purpose

P023 lands the acceptance design, command contracts and first paper runtime acceptance for Account Console account command capability using OpenCTP 19053 as the first 7x24 paper command lane. It covers guarded paper submit and cancel, real readback reconciliation, UI status evidence and negative gates.

This proposal does not enable Account Console web/API command controls. It lands a worktree-owned runtime acceptance harness and keeps Account Mirror as a read-only projection.

The live-trading scenario catalog is [live-trading-scenarios.md](live-trading-scenarios.md). P023 uses those real trading scenarios to define paper acceptance and live-blocked gates.

## Scope

1. Paper-only command mode for `acct.ctp.paper.19053`.
2. Submit one guarded OpenCTP paper order through a command gateway.
3. Read back the submitted order through `ReqQryOrder`.
4. Cancel the same order using readback identity.
5. Read back cancelled/withdrawn terminal state.
6. Project command status to Account Console only after command audit and Account Mirror readback.
7. Preserve typed blockers for any missing owner, risk, approval, gateway, readback or reconciliation evidence.

## Non-Goals

1. Live trading readiness.
2. Capital approval or production admission.
3. Account Mirror as broker writer.
4. UI direct CTP calls.
5. Replace/modify order.
6. Using screenshots, browser text, debug/latest paths or TickTrader UI state as command truth.

## Boundary Summary

| Concern | Decision |
| --- | --- |
| 7x24 meaning | Paper acceptance lane availability only |
| Command owner | Command Gateway / execution owner, not Account Mirror |
| Readback owner | Account Mirror from OpenCTP query evidence |
| Credential owner | Owner repo/runtime refs only |
| UI role | Intent capture and evidence/status display |
| Final state | Mirror readback + reconciliation, not gateway ack |

## Required Artifacts

1. `contracts/account_command/*.schema.json`
2. `contracts/account_command/fixtures/openctp19053/*.json`
3. `output/account_command/ctp-paper-19053/<run-id>/command_audit.json`
4. `output/account_command/ctp-paper-19053/<run-id>/submit_intent.json`
5. `output/account_command/ctp-paper-19053/<run-id>/submit_gateway_event.json`
6. `output/account_command/ctp-paper-19053/<run-id>/post_submit_readback.json`
7. `output/account_command/ctp-paper-19053/<run-id>/cancel_intent.json`
8. `output/account_command/ctp-paper-19053/<run-id>/cancel_gateway_event.json`
9. `output/account_command/ctp-paper-19053/<run-id>/post_cancel_readback.json`
10. `output/account_command/ctp-paper-19053/<run-id>/reconciliation_result.json`
11. Browser evidence for `/accounts/acct.ctp.paper.19053`

## Gates

Run before claiming P023 design acceptance:

```powershell
python scripts\validate_adr0007_account_command_capability.py
python scripts\validate_p023_account_command_contracts.py
python scripts\validate_p023_openctp_19053_command_acceptance_design.py
python scripts\check_proposal_docs.py --root . --proposal-id p023-openctp-19053-paper-command-capability
```

Run after paper runtime acceptance:

```powershell
python scripts\run_p023_openctp19053_command_acceptance.py --preflight-readback output\account_command\ctp-paper-19053\preflight-20260621Tnow\owner_preflight_readback.json --limit-price 3300 --client-order-id p023-rb2610-close-20260621t0748z --output-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --arm-paper-send --arm-cancel-send
python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json
```

## Live Scenario Coverage

P023 must keep the live scenario catalog current before implementation starts. The first 19053 paper runtime covers the paper subset from `LT-01` through closeout scenarios; live mutation remains blocked until the `live_armed` evidence bundle exists.

## Status

P023 paper runtime is accepted for the guarded OpenCTP 19053 paper lane. Current Account Console web/API command capability remains disabled.

Phase 1 command contracts are landed behind `validate_p023_account_command_contracts.py`, including submit idempotency replay contract-lock evidence. Phase 3 dry-run and Phase 4/5 real paper submit/cancel are landed behind `validate_p023_openctp19053_command_run.py`. Phase 6 UI command status evidence is landed behind `validate_p023_ui_status_browser_evidence.py` with command controls still disabled. Live trading readiness remains blocked.
