# P023 Web UI Acceptance / Web UI 验收场景

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Primary ADR: ADR-0007
- Route: `/accounts/acct.ctp.paper.19053`

## Purpose

This document maps the 10 live-trading scenario groups to Web UI acceptance. The UI may capture intent and display status, but final command state must come from command audit plus Account Mirror readback/reconciliation.

## Required Web UI Evidence

Every browser acceptance run must write:

```text
docs/acceptance/browser-evidence/p023-openctp-19053-command/<project>/
  disabled-state.png
  paper-armed-submit.png
  submit-readback.png
  cancel-readback.png
  blocker-state.png
  closeout.json
```

## Web UI Scenario Matrix

| Group | Scenario | Web UI verification | Pass signal | Must fail if |
| --- | --- | --- | --- | --- |
| G1 Pre-trade readiness | Show command preflight state | Account page displays latest preflight ref and freshness | preflight source refs visible; stale state blocks controls | controls enabled with stale/missing preflight |
| G2 Submit | Capture guarded paper order intent | Submit form shows account, instrument, qty, price, TIF and idempotency preview | clicking submit creates pending command status, not final state | button calls broker directly or lacks idempotency |
| G3 Cancel | Cancel eligible open order | Cancel button appears only on row with readback identity | cancel intent preview includes venue/order ref | cancel button appears on row without identity |
| G4 Fill lifecycle | Show working/partial/filled/cancelled lifecycle | Order/fill tables and command status reflect readback/reconcile | quantities and statuses cite source refs | UI infers fills without source evidence |
| G5 Reject/block | Show risk/approval/broker rejects | Blocker panel displays reason and stage | blocked command cannot be resubmitted without changed evidence | reject is hidden as success |
| G6 Connectivity | Show timeout/disconnect/reconnect state | Status panel shows uncertain/stale/recovered states | readback timeout blocks final status | gateway ack displayed as final during disconnect |
| G7 Session conflict | Show session owner blocker | Capability/source health panel displays session conflict | command controls hidden | UI silently continues after conflict |
| G8 Emergency controls | Show kill switch/account disabled | Paper command strip disabled with reason | submit/cancel hidden or disabled | controls active while kill switch active |
| G9 Audit/reconciliation | Show audit and reconciliation refs | Command status panel links audit, gateway, readback, reconcile refs | all refs visible and copyable | command status lacks provenance |
| G10 UI safety | Default disabled and paper/live separation | Disabled default, paper banner when armed, no live-ready wording | live controls absent until `live_armed` | paper 7x24 claim appears as live readiness |

## Required Data Test IDs

| Test ID | Purpose |
| --- | --- |
| `account-command-mode` | command mode display |
| `account-paper-command-banner` | paper-only 7x24 warning |
| `account-command-preflight-ref` | preflight evidence ref |
| `account-submit-order-form` | guarded submit form |
| `account-submit-order-button` | submit action |
| `account-submit-idempotency-key` | idempotency preview |
| `account-cancel-order-button` | cancel action |
| `account-cancel-order-identity` | readback identity used for cancel |
| `account-command-status-panel` | command lifecycle status |
| `account-command-risk-ref` | risk decision ref |
| `account-command-approval-ref` | approval decision ref |
| `account-command-gateway-ref` | gateway event ref |
| `account-command-readback-ref` | readback ref |
| `account-command-reconciliation-ref` | reconciliation ref |
| `account-command-blocker` | fail-closed blocker |

## Web UI Positive Acceptance

| ID | Group | Positive path | Browser assertion |
| --- | --- | --- | --- |
| UI-01 | G1 | disabled default shows observation-only and preflight freshness | no submit/cancel controls |
| UI-02 | G2 | paper armed submit form renders | form fields and idempotency key visible |
| UI-03 | G2 | submit click shows pending command status | status is pending until readback |
| UI-04 | G3 | eligible row shows cancel control | row has cancel identity ref |
| UI-05 | G3 | cancel click shows pending cancel status | status cites cancel intent ref |
| UI-06 | G4 | lifecycle table updates from readback | order/fill rows cite source refs |
| UI-07 | G5 | risk/approval reject visible | blocker row includes reason and stage |
| UI-08 | G6 | readback timeout visible | status is blocked/uncertain |
| UI-09 | G7 | session conflict visible | controls hidden and blocker visible |
| UI-10 | G8 | kill switch disables controls | controls hidden/disabled |
| UI-11 | G9 | audit/reconciliation refs visible | refs are copyable |
| UI-12 | G10 | paper banner visible when armed | no live-ready text |

## Web UI Negative Acceptance

| ID | Group | Negative path | Required rejection |
| --- | --- | --- | --- |
| UIN-01 | G1 | stale preflight | submit/cancel controls absent |
| UIN-02 | G2 | missing idempotency key | submit disabled |
| UIN-03 | G3 | missing cancel identity | cancel absent |
| UIN-04 | G4 | missing fill/readback source | UI displays blocker, not inferred state |
| UIN-05 | G5 | risk/approval block | no gateway-success styling |
| UIN-06 | G6 | disconnect after ack | no final filled/cancelled state |
| UIN-07 | G7 | session conflict | no command controls |
| UIN-08 | G8 | kill switch active | no command controls |
| UIN-09 | G9 | missing audit/reconcile refs | command status rejected |
| UIN-10 | G10 | paper state uses live-ready wording | reject |

## Closeout Rule

Web UI acceptance must compare browser state with API projection and command artifacts. Screenshots alone are never sufficient.
