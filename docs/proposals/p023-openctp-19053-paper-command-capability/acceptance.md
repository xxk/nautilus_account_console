# P023 Acceptance / OpenCTP 19053 Paper Command

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Primary ADR: ADR-0007

## Required Gates

| Gate | Command | Pass signal | Scope |
| --- | --- | --- | --- |
| ADR-0007 command validator | `python scripts\validate_adr0007_account_command_capability.py` | `ADR0007_ACCOUNT_COMMAND_CAPABILITY_OK` | ADR proposed state and existing command-disabled boundary |
| P023 command contracts | `python scripts\validate_p023_account_command_contracts.py` | `P023_ACCOUNT_COMMAND_CONTRACTS_OK` | Order/cancel/audit contracts, fixtures and negative sensitive-boundary gates |
| P023 design validator | `python scripts\validate_p023_openctp_19053_command_acceptance_design.py` | `P023_OPENCTP_19053_COMMAND_ACCEPTANCE_DESIGN_OK` | P023 acceptance design completeness |
| P023 paper command run | `python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json` | `P023_OPENCTP19053_COMMAND_RUN_OK` | Real OpenCTP 19053 paper submit/cancel/readback/reconciliation and read-model projection guard |
| P023 partial-fill browser evidence | `python scripts\validate_p023_partial_fill_browser_evidence.py` | `P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK` | Web UI order display correctness for partial fill then cancel; runtime partial-fill remains typed blocker |
| Proposal docs | `python scripts\check_proposal_docs.py --root . --proposal-id p023-openctp-19053-paper-command-capability` | `PROPOSAL_DOCS_OK` | Proposal structure |

## Scenario Matrix

The scenario matrix below is backed by [live-trading-scenarios.md](live-trading-scenarios.md). That catalog lists live trading scenarios `LT-01` through `LT-30`; P023's first runtime must cover the declared 19053 paper subset and preserve typed blockers for unavailable live-only states.

The 10 scenario groups have two acceptance surfaces:

1. [non-ui-acceptance.md](non-ui-acceptance.md): contracts, API, runtime artifacts, OpenCTP readback, reconciliation, redaction and typed blockers.
2. [web-ui-acceptance.md](web-ui-acceptance.md): Account Workbench browser behavior, controls, disabled states, paper banners, command status and evidence refs.

| ID | Type | Scenario | Verification shape | Must fail if | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | positive | Contract family exists for command path | schema validator | missing `OrderIntent`, `CancelIntent`, `RiskDecision`, `ApprovalDecision`, `ExecutionCommand`, `ExecutionEvent`, `MirrorReadback`, `ReconciliationResult` | contract_gate_ready |
| A2 | positive | 19053 7x24 paper preflight ready | real OpenCTP query artifact | login/query/readback unavailable without typed blocker | runtime_accepted |
| A3 | positive | Paper submit accepted by gateway | integration test + command audit | Account Mirror or UI sends broker mutation | runtime_accepted |
| A4 | positive | Submit idempotency | duplicate submit test | duplicate click creates duplicate broker order | planned |
| A5 | positive | Post-submit readback reconciles | `ReqQryOrder` evidence + reconciliation artifact | gateway ack alone marks final state | runtime_accepted |
| A6 | positive | Paper cancel uses readback identity | cancel integration test | cancel uses screenshot/UI text/latest path | runtime_accepted |
| A7 | positive | Post-cancel readback reconciles | `ReqQryOrder` terminal state evidence | missing terminal state is hidden as success | runtime_accepted |
| A8 | positive | Secret redaction | artifact redaction validator | raw password/front/auth/token recorded | runtime_accepted |
| A9 | positive | UI status evidence | Playwright + API projection | UI shows command complete without readback/reconcile | planned |
| A10 | positive | Partial fill then cancel | `ReqQryTrade` + `ReqQryOrder` + reconciliation validator plus browser order-display gate | partial fill inferred from UI/gateway ack/screenshot | browser_order_display_contract_ready_runtime_blocked |

A10 supersedes the earlier `designed_runtime_blocker_until_partial_state` design-only state for the Web UI order-display surface: the browser order display contract is ready, while real OpenCTP partial-fill runtime and command action controls remain typed blockers.

## Negative Acceptance

| ID | Failure path | Required rejection |
| --- | --- | --- |
| N1 | `POST /api/mirror/.../orders` appears | reject; Account Mirror is not writer |
| N2 | UI command controls appear while `command.mode=disabled` | reject |
| N3 | Missing idempotency key | reject before gateway |
| N4 | Cancel intent lacks readback `venue_order_id` / `order_ref` | reject before gateway |
| N5 | Gateway ack treated as final order state | reject |
| N6 | Missing risk or approval decision | reject before gateway |
| N7 | Artifact records raw secret or broker endpoint | reject |
| N8 | Paper 7x24 evidence claims live readiness | reject |
| N9 | Screenshot or TickTrader UI table used as command truth | reject |
| N10 | Partial fill quantity or remaining quantity cannot be traced to broker readback | typed reconciliation blocker |

## OpenCTP 19053 Runtime Evidence Shape

Each accepted runtime run must write a single run directory:

```text
output/account_command/ctp-paper-19053/<run-id>/
  command_audit.json
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
  partial_fill_readback.json
  partial_fill_reconciliation_result.json
  reconciliation_result.json
```

Every JSON artifact must include:

1. `account_id=acct.ctp.paper.19053`
2. `mode=paper_armed`
3. `raw_secret_values_recorded=false`
4. `raw_broker_endpoint_recorded=false`
5. `gateway_ack_is_final_state=false`
6. source refs and checksums
7. typed blocker fields when not passed

For partial-fill acceptance, `partial_fill_reconciliation_result.json` must include `partial_fill=true`, `remaining_quantity_cancelled`, deduplicated broker trade identities, and proof that `filled_quantity + remaining_quantity == submitted_quantity`. If OpenCTP 19053 does not produce a partial-fill state during the run, A10 remains a typed runtime blocker and cannot be marked pass.

## UI Acceptance

Before Phase 6, no command controls may render. After Phase 6, controls may render only when API projection shows:

1. `capabilities.command.enabled=true`
2. `capabilities.command.mode=paper_armed`
3. allowed actions contain `submit` and `cancel`
4. risk/approval/gateway/readback evidence refs are present
5. command status panel cites command audit and Account Mirror readback refs

## Closeout Rule

P023 cannot close with text-only evidence. It requires schema tests, API tests, real OpenCTP paper runtime artifacts, redaction gates and browser evidence.
