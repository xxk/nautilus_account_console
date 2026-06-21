# P023 Non-UI Acceptance / 非 UI 验收场景

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Primary ADR: ADR-0007
- Account: `acct.ctp.paper.19053`

## Purpose

This document maps the 10 live-trading scenario groups to non-UI acceptance. Non-UI means contracts, API responses, runtime artifacts, command audit records, OpenCTP query evidence, validators and typed blockers. Browser rendering is covered separately in `web-ui-acceptance.md`.

## Required Non-UI Artifact Family

Every runtime acceptance run must write:

```text
output/account_command/ctp-paper-19053/<run-id>/
  preflight_readback.json
  submit_intent.json
  submit_risk_decision.json
  submit_approval_decision.json
  submit_gateway_event.json
  post_submit_readback.json
  cancel_intent.json
  cancel_risk_decision.json
  cancel_approval_decision.json
  cancel_gateway_event.json
  post_cancel_readback.json
  reconciliation_result.json
  partial_fill_readback.json
  partial_fill_reconciliation_result.json
  command_audit.json
  redaction_report.json
  closeout_manifest.json
```

## Non-UI Scenario Matrix

| Group | Scenario | Non-UI verification | Pass signal | Must fail if |
| --- | --- | --- | --- | --- |
| G1 Pre-trade readiness | Query account/funds/positions/orders/fills before command | Run OpenCTP preflight query and validate `preflight_readback.json` | account id, balances, positions, open orders/fills source refs and `ready=true` | command starts with stale/missing preflight |
| G2 Submit | Submit guarded paper limit order | Validate `submit_intent`, risk/approval, gateway event and post-submit `ReqQryOrder` | one broker order identity appears in readback and idempotency key maps to one order | duplicate submit creates duplicate broker orders |
| G3 Cancel | Cancel open order by readback identity | Validate `cancel_intent` uses `venue_order_id/order_ref` from post-submit readback | post-cancel readback reaches cancelled/withdrawn or typed blocker | cancel uses UI text, screenshot, latest path or missing identity |
| G4 Fill lifecycle | Observe no-fill/partial/full/fill-after-cancel states | Validate `ReqQryOrder` and `ReqQryTrade` reports or typed runtime blocker | fill/order quantities reconcile | remaining/fill quantity inferred without source evidence |
| G5 Reject/block | Risk, approval, validation and broker rejects | Negative contract/API tests plus gateway reject event | blocked intents never reach broker gateway; broker reject is visible | reject hidden as success/pending |
| G6 Connectivity | Timeout, disconnect, reconnect and stale readback | Runtime timeout/reconnect harness and blocker artifacts | stale/unknown states become typed blockers; recovered readback reconciles | in-memory state used as pass after disconnect |
| G7 Session conflict | Duplicate login/session owner ambiguity | Session conflict validator and owner refs | conflict blocks command before gateway | Account Console silently steals session |
| G8 Emergency controls | Kill switch/account disable/cancel-all boundary | Capability/risk policy validator | disabled account blocks submit/cancel; cancel-all remains out of scope | kill switch ignored or cancel-all exposed |
| G9 Audit/reconciliation | Reconstruct command lifecycle | Validate `command_audit.json`, checksums and `reconciliation_result.json` | intent, decisions, gateway, readback and UI status refs chain by checksum | command cannot be reconstructed |
| G10 UI safety backend state | API projection exposes correct command mode for UI | API tests for `command.mode` and allowed actions | disabled before implementation; paper_armed only with evidence refs | API exposes controls without evidence |

## Non-UI Positive Acceptance

| ID | Group | Positive path | Required verifier |
| --- | --- | --- | --- |
| NU-01 | G1 | 19053 preflight ready from OpenCTP readback | `validate_preflight_readback` |
| NU-02 | G2 | submit intent schema valid | `validate_order_intent_schema` |
| NU-03 | G2 | submit idempotency creates one broker order | `validate_submit_idempotency_replay` |
| NU-04 | G2 | post-submit readback sees venue identity | `validate_post_submit_readback` |
| NU-05 | G3 | cancel intent schema valid and identity-bound | `validate_cancel_intent_schema` |
| NU-06 | G3 | post-cancel readback terminal or typed blocker | `validate_post_cancel_readback` |
| NU-07 | G4 | order/fill quantities reconcile or typed blocker | `validate_fill_lifecycle_reconciliation` |
| NU-08 | G5 | risk/approval block stops before gateway | `validate_fail_closed_policy` |
| NU-09 | G6 | readback timeout writes typed blocker | `validate_readback_timeout_blocker` |
| NU-10 | G7 | session conflict blocks before gateway | `validate_session_conflict_blocker` |
| NU-11 | G8 | kill switch disables command mode | `validate_kill_switch_blocker` |
| NU-12 | G9 | command audit chain reconstructs lifecycle | `validate_command_audit_chain` |
| NU-13 | G9 | redaction report proves no raw secrets/endpoints | `validate_command_redaction` |
| NU-14 | G10 | command API projection remains disabled by default | `validate_command_projection_default` |
| NU-15 | G4 | partial fill then cancel reconciles filled and remaining quantities | `validate_partial_fill_then_cancel_reconciliation` |

## Submit Idempotency Non-UI Acceptance

NU-03 is accepted at the contract-lock level by `submit_idempotency_replay_valid.json` and `validate_submit_idempotency_replay`. The verifier must prove the original submit intent, retry intent, command audit, gateway event and post-submit readback refs have valid SHA256 checksums; the original and retry share one idempotency key; the retry maps to the same command result and `same_broker_order_identity=true`; `duplicate_broker_order_created=false`; `gateway_send_replayed=false`; and `runtime_duplicate_send_attempted=false`. A second broker order identity, missing source ref, bad checksum, gateway replay or raw secret artifact must be rejected.

## Partial Fill Non-UI Acceptance

NU-15 is a conditional runtime acceptance: it may pass only when the OpenCTP 19053 paper lane naturally produces or an owner-approved fixture produces a real partial-fill state. If the run cannot produce that state, the result must be a typed runtime blocker, not a pass.

Required NU-15 verification:

1. `partial_fill_readback.json` records `ReqQryTrade` rows with broker trade identity, order identity, fill quantity, fill price, source refs and checksums.
2. `post_submit_readback.json` records `ReqQryOrder` for the same order identity with `filled_quantity > 0` and `remaining_quantity > 0`.
3. `partial_fill_reconciliation_result.json` records `partial_fill=true`.
4. The validator proves `filled_quantity + remaining_quantity == submitted_quantity` before cancel.
5. `cancel_intent.json` is built from the readback order identity and targets only the remaining quantity.
6. `post_cancel_readback.json` preserves the filled quantity and shows the remaining quantity cancelled/withdrawn, or writes a typed blocker.
7. Reconciliation deduplicates duplicate trade rows by broker trade identity before summing fill quantity.

## Non-UI Negative Acceptance

| ID | Group | Negative path | Required rejection |
| --- | --- | --- | --- |
| NUN-01 | G1 | stale preflight checkpoint | typed blocker, no gateway call |
| NUN-02 | G2 | missing idempotency key | reject before risk/gateway |
| NUN-03 | G2 | duplicate submit retry | same command result, no second broker order |
| NUN-04 | G3 | cancel without `venue_order_id/order_ref` | reject before gateway |
| NUN-05 | G4 | fill quantity mismatch | reconciliation mismatch blocker |
| NUN-06 | G5 | missing risk decision | reject before gateway |
| NUN-07 | G5 | missing approval decision | reject before gateway |
| NUN-08 | G6 | disconnect after gateway ack before readback | uncertain/blocked, not success |
| NUN-09 | G7 | ambiguous session owner | command blocked |
| NUN-10 | G8 | kill switch active | command blocked |
| NUN-11 | G9 | artifact contains raw secret/front/auth/token | redaction failure |
| NUN-12 | G10 | API exposes `paper_armed` without evidence refs | projection rejected |
| NUN-13 | G4 | partial fill uses UI/screenshot/gateway ack instead of `ReqQryTrade` | reconciliation blocker |
| NUN-14 | G4 | partial fill duplicate trade rows double-counted | reconciliation mismatch blocker |
| NUN-15 | G4 | cancel quantity exceeds readback remaining quantity after partial fill | cancel rejected before gateway |

## Closeout Rule

Non-UI acceptance can pass only if every positive verifier passes and every negative verifier rejects as expected. Missing real runtime state may be a typed blocker, not a pass.
