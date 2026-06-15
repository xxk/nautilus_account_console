# Account Command Capability Design Gate / 账户命令能力设计闸门

- Created: 2026-06-15
- Status: design_gate_only
- Primary ADR: ADR-0004
- Topic: T001 Account Mirror Observation Plane
- Proposal phase: P011 Phase 7

## Purpose

This document freezes the command capability architecture before any order action UI, API or broker gateway implementation is accepted.

P011 Phase 7 does not implement submit, cancel or replace. It only defines the gate that a future command proposal must satisfy before Account Console can display or invoke command controls.

## Architecture Rule

Observation and command are separate planes.

Account Mirror may read broker/runtime/account observations and project them to UI. Account Mirror must not become the command authority, broker writer, approval owner, risk owner, capital owner or trading-readiness owner.

## Required Future Command Flow

```text
Order Intent
  -> Risk Check
  -> Approval / Admission
  -> Execution Gateway
  -> Execution Event
  -> Account Mirror Readback
  -> Reconciliation Projection
  -> UI Status / Evidence
```

The gateway response is not final account state. UI-visible order state must be confirmed by Account Mirror readback and reconciliation evidence.

## Capability Modes

| Mode | Meaning | UI command controls |
| --- | --- | --- |
| `disabled` | No accepted command authority exists for the account | hidden |
| `paper_design_only` | Future paper/sandbox command design is allowed to be specified, not executed | hidden |
| `live_design_only` | Future live command design is allowed to be specified, not executed | hidden |

The current P011 account capability bundle remains stricter and uses `command.enabled=false` with `mode=disabled`. The design-only modes above are reserved vocabulary for a future command proposal, not current runtime capability.

## Required Future Contracts

Any proposal that enables commands must add, at minimum:

1. `OrderIntent`: account id, instrument, side, quantity, order type, time-in-force, strategy/source owner, idempotency key and source evidence.
2. `RiskDecision`: deterministic risk result, rule ids, limits checked, owner, timestamp and checksum.
3. `ApprovalDecision`: approval/admission result, approver or automated authority, policy version, timestamp and checksum.
4. `ExecutionCommand`: gateway kind, session id, command id, action, payload checksum and authority ref.
5. `ExecutionEvent`: accepted/rejected/submitted/canceled/replaced/fill events from gateway or runtime.
6. `MirrorReadback`: Account Mirror observation proving what the account/broker reported after the command.
7. `ReconciliationResult`: comparison between intent, gateway event and readback observation.

## Positive Acceptance

P011 Phase 7 passes only if:

1. The design gate declares command implementation as not accepted.
2. The required flow includes intent, risk, approval, gateway, execution event, mirror readback and reconciliation.
3. Existing account capability fixtures keep `command.enabled=false`.
4. Existing Account Console mirror API routes remain read-only.
5. The P011 acceptance document records Phase 7 as design-gate-only, not implementation.

## Negative Acceptance

Future command work must fail if:

1. UI exposes submit, cancel or replace controls from P011 Phase 7 evidence.
2. Account Console backend exposes command routes before a command proposal is accepted.
3. A live account claims command capability without risk, approval, session, authority ref and readback reconciliation.
4. A gateway acknowledgement is treated as final account state without Account Mirror readback.
5. Command capability is inferred from `paper`, `sandbox`, `live`, `ctp`, `ib_tws` or stock source kind.
6. Account Mirror writes broker/runtime/account/order state.

## Future Proposal Handoff

A future command proposal may use this design gate as its starting point, but it must still provide its own contracts, fixtures, browser/API acceptance, risk/approval authority evidence and fail-closed negative tests.

The first implementation proposal should start with paper/sandbox command authority only. Live CTP, IB TWS and stock command capability require separate live-command acceptance gates.
