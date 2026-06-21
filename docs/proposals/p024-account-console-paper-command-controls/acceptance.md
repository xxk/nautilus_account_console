# P024 Acceptance / Account Console Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: design_gate_ready
- Primary ADR: ADR-0007

## Scope

P024 accepts only guarded Web/API paper command controls for `acct.ctp.paper.19053`. Implementation/browser evidence is required before implementation closeout; design-gate readiness is not browser or runtime closeout.

Out of scope: live trading, replace order, Account Mirror write authority, direct browser-to-CTP calls, raw secret ownership, screenshots as command truth.

## Required Gates

| Gate | Command | Pass signal | Scope |
| --- | --- | --- | --- |
| P024 design gate | `python scripts\validate_p024_paper_command_controls_design.py` | `P024_PAPER_COMMAND_CONTROLS_DESIGN_OK` | Proposal docs, ADR coverage, current no-controls boundary |
| P023 runtime predecessor | `python scripts\validate_p023_openctp19053_command_run.py --run-dir output\account_command\ctp-paper-19053\p023-armed-20260621t0748z --source-package output\account_capability\ctp-paper-19053\source-package.json` | `P023_OPENCTP19053_COMMAND_RUN_OK` | Predecessor paper command evidence |
| Proposal docs | `python scripts\check_proposal_docs.py --root . --proposal-id p024-account-console-paper-command-controls` | `PROPOSAL_DOCS_OK` | Proposal structure |

## Scenario Matrix

| ID | Type | Scenario | Verification shape | Must fail if | Status |
| --- | --- | --- | --- | --- | --- |
| A1 | positive | Backend command API accepts paper submit intent | API contract + command artifact validator | endpoint bypasses risk/approval | planned |
| A2 | positive | Account Mirror remains read-only | route audit | `/api/mirror` exposes POST/PUT/DELETE | design_gate_ready |
| A3 | positive | Command controls render only in `paper_armed` mode | Playwright + API projection | controls appear while disabled | planned |
| A4 | positive | Submit writes intent/risk/approval/gateway/readback/reconcile refs | integration + artifact validator | gateway ack alone is final | planned |
| A5 | positive | Submit idempotency prevents duplicate order | retry/duplicate-click test | duplicate broker order identity appears | planned |
| A6 | positive | Risk/approval fail closed | negative API tests | missing risk/approval reaches gateway | planned |
| A7 | positive | Cancel uses latest readback identity | API/browser + readback artifact | cancel uses UI row text or screenshot | planned |
| A8 | positive | UI status waits for readback/reconcile | browser evidence | final state shown without readback/reconcile | planned |
| A9 | positive | Secret redaction | artifact redaction gate | raw password/front/auth/token recorded | planned |
| A10 | positive | Partial fill then cancel Web UI order display correctness | Playwright + `partial-fill-cancel-ui-acceptance.md` + browser evidence JSON | identity changes, fill rows drift, or quantity formulas fail | design_gate_ready |

## Partial Fill Then Cancel Acceptance

The Web UI must verify the same order across four stages: `S1 submitted/working`, `S2 partially filled`, `S3 cancel pending`, and `S4 remaining cancelled`.

Required display formulas:

1. `S2`: `filled_quantity + remaining_quantity == submitted_quantity`.
2. `S3`: filled, remaining and fill rows remain unchanged until cancel readback.
3. `S4`: `filled_quantity + cancelled_quantity == submitted_quantity`.
4. `S4`: `remaining_quantity == 0`.

Required identity and provenance checks:

1. `account-order-identity` is stable across all stages.
2. `account-fill-source-ref` rows remain stable after cancel.
3. `account-remaining-cancel-quantity` equals the S2 remaining quantity and disappears after cancel is pending or terminal.
4. `account-cancel-pending-ref` cites command audit evidence and never proves final state by itself.
5. The final canceled display requires readback and reconciliation evidence, not gateway acknowledgement alone.

Current predecessor evidence is P023 display-contract evidence only: `python scripts\validate_p023_partial_fill_browser_evidence.py` returns `P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK` and explicitly states runtime partial-fill remains a typed blocker until real or owner-approved partial-fill state exists. P024 implementation must regenerate P024-scoped browser evidence before closeout.

## Negative Acceptance

| ID | Failure path | Required rejection |
| --- | --- | --- |
| N1 | Account Mirror writer path appears | reject; mirror remains read-only |
| N2 | UI controls appear with `command.mode=disabled` | hidden controls and blocker |
| N3 | duplicate submit/click/retry | same command result, one broker order identity |
| N4 | cancel without readback identity | reject before gateway |
| N5 | gateway ack final-state claim | blocked until readback/reconcile |
| N6 | missing risk or approval | reject before gateway |
| N7 | raw secret/front/auth/token in artifact | redaction failure |
| N8 | live mode exposed | reject; P024 is paper-only |
| N9 | partial-fill cancel display uses changed identity, stale fill rows or broken quantity formula | reject browser evidence |
| N10 | cancel-pending gateway event is shown as final canceled state | blocked until readback/reconciliation |

## UI Anti-Drift Acceptance

| ID | Drift | forbidden_actions | forbidden_claims | Required rejection |
| --- | --- | --- | --- | --- |
| UAD-01 | Disabled account shows controls | submit, cancel, replace | Paper ready, can trade | controls absent |
| UAD-02 | Browser calls broker directly | CTP/TWS browser mutation | broker truth from UI | browser test fails |
| UAD-03 | Gateway ack shown as final | final success without readback | command complete | blocker |
| UAD-04 | Live control appears | live submit/cancel | live ready | reject |

## Evidence Boundary

Implementation/browser evidence is required before implementation closeout. Until Phase 1-4 are implemented, P024 remains `design_gate_ready`, not runtime accepted.
