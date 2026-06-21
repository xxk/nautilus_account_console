# P023 Phase Plan / OpenCTP 19053 Paper Command

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Primary ADR: ADR-0007

## Phase Table

| Phase | Scope | Entry condition | Exit evidence | Status |
| --- | --- | --- | --- | --- |
| Phase 0 | ADR/proposal acceptance design | ADR-0007 exists | P023 docs and validator pass | completed_design |
| Phase 1 | Command contracts | P023 design accepted | `OrderIntent`, `CancelIntent`, risk/approval/gateway/readback/reconcile schemas and fixtures pass | completed_contract_gate |
| Phase 2 | Disabled default gates | Phase 1 | Existing accounts remain `command.enabled=false`; command API absent until explicitly enabled | completed_disabled_gate |
| Phase 3 | Paper gateway dry-run | Phase 2 | Gateway validates intent without broker mutation and writes audit evidence | completed_dry_run |
| Phase 4 | OpenCTP 19053 paper submit | Phase 3 | Real paper submit event plus `ReqQryOrder` post-submit readback match | completed_paper_submit |
| Phase 5 | OpenCTP 19053 paper cancel | Phase 4 | Cancel event plus `ReqQryOrder` terminal readback match | completed_paper_cancel |
| Phase 5b | OpenCTP 19053 partial-fill lifecycle | Phase 5 | `ReqQryTrade` partial fill, `ReqQryOrder` remaining quantity, cancel remaining quantity and reconciliation match, or typed runtime blocker | designed_runtime_blocker_until_partial_state |
| Phase 6 | UI command status | Phase 5 | UI shows command status from audit + mirror readback; no gateway-ack-as-final-state | read_model_refreshed_command_controls_disabled |
| Phase 7 | Closeout | Phase 6 | P023 acceptance evidence and browser/API/validator gates pass | runtime_closeout_accepted_browser_pending |

## ADR Decision Coverage Mapping

Primary ADR: ADR-0007

| ADR decision item | ADR section / successor scenario | Phase | Acceptance row |
| --- | --- | --- | --- |
| D1 | Command path requires intent, risk, approval, gateway, event, readback, reconciliation | Phase 1-7 | A1, A3, A5 |
| D2 | Account Mirror never sends commands | Phase 2-7 | N1, N2 |
| D3 | OpenCTP 19053 7x24 is paper acceptance lane only | Phase 4-7 | A2, N8 |
| D4 | Submit must be idempotent | Phase 3-4 | A4, N3 |
| D5 | Cancel must use readback identity | Phase 5 | A6, N4 |
| D6 | Gateway ack is not final account state | Phase 4-7 | A5, N5 |
| D7 | Secrets remain outside worktree | Phase 1-7 | A8, N7 |

## Runtime Acceptance Sequence

1. Query current OpenCTP 19053 account/funds/positions/orders/fills.
2. Build `OrderIntent` with paper-only policy, approved instrument and idempotency key.
3. Run risk and approval/admission policy.
4. Send through command gateway.
5. Collect gateway event.
6. Query `ReqQryOrder` until submitted order identity appears or typed timeout blocker is written.
7. Build `CancelIntent` from readback identity.
8. Send cancel through command gateway.
9. Query `ReqQryOrder` until cancelled/withdrawn state appears or typed timeout blocker is written.
10. Build reconciliation result.
11. Project UI status only from command audit and Account Mirror readback.

## Partial-Fill Runtime Sequence

Phase 5b is entered only for a real or owner-approved partial-fill state. It cannot be satisfied by screenshots, UI table text or gateway ack.

1. Submit a guarded order with a quantity that can leave a remaining quantity.
2. Query `ReqQryOrder` until the order identity is visible.
3. Query `ReqQryTrade` until at least one fill row exists for the same order identity.
4. Require `filled_quantity > 0`, `remaining_quantity > 0`, and `filled_quantity + remaining_quantity == submitted_quantity`.
5. Build `CancelIntent` from the readback identity and remaining quantity.
6. Query `ReqQryOrder` after cancel until the remaining quantity is cancelled/withdrawn or a typed blocker is written.
7. Build `partial_fill_reconciliation_result.json` with `partial_fill=true`, `remaining_quantity_cancelled`, deduped trade ids, source refs and checksums.

## Current Blockers

Browser command-control implementation remains blocked. True OpenCTP paper submit/cancel evidence exists at `output/account_command/ctp-paper-19053/p023-armed-20260621t0748z/`; partial-fill runtime evidence is designed but remains blocked until a real or owner-approved partial-fill state is produced. Live trading readiness and web/API command controls remain disabled.
