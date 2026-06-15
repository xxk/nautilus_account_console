# P005 UI Acceptance: Intraday Monitor

- Proposal ID: `p005-intraday-monitor-exception-queue-panel`
- Status: design_gate_ready
- Updated: 2026-06-15
- UI design: [P005 UI Design](./ui-design.md)
- Parent acceptance: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- Anti-drift acceptance: [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)

## 1. Required UI Evidence

| Evidence | Required artifact |
| --- | --- |
| Monitor read model contract | `contracts/ui/panels/intraday_monitor_panel.contract.json` |
| Current fixture | `/monitor` with active exceptions, lag and incidents |
| Empty fixture | `/monitor` with no active exceptions and source refs still visible |
| Blocked fixture | missing monitor source or source owner blocker |
| Stale fixture | stale stream/checkpoint state |
| Partial fixture | incomplete lag or incident refs |
| Desktop screenshot | `/monitor` with current fixture |
| Tablet screenshot | `/monitor` with current or blocked fixture |
| Mobile screenshot | `/monitor` with compact exception rows |
| DOM/test evidence | stable `data-testid` hooks for panel, context bar, lag strip, queue, refs and blockers |
| Anti-drift evidence | completed anti-drift checklist in [P005 acceptance](./acceptance.md) |

## 2. Positive UI Acceptance

| ID | Must pass | Evidence |
| --- | --- | --- |
| P005-UI-POS-01 | `/monitor` first viewport shows Intraday Monitor context before raw logs or route lists | desktop screenshot |
| P005-UI-POS-02 | lag strip shows max lag, stale stream count, open incidents and blocked sources from fixture fields | fixture-backed test |
| P005-UI-POS-03 | exception queue shows severity, kind, owner, next action, source ref and checksum | DOM test or screenshot |
| P005-UI-POS-04 | blocked, stale, partial, empty and current states render distinct read-only states | state screenshots or typed browser blocker |
| P005-UI-POS-05 | source refs and checksums are visible and copyable without overlap on desktop, tablet and mobile | browser evidence |

## 3. Negative UI Acceptance

| ID | Must fail if |
| --- | --- |
| P005-UI-NEG-01 | `/monitor` appears without the declared read model contract and fixture state |
| P005-UI-NEG-02 | UI consumes fields not present in contract or fixtures |
| P005-UI-NEG-03 | monitor values appear without source refs, checksums or typed blockers |
| P005-UI-NEG-04 | browser computes runtime, stream, scheduler, account, order, ledger or HFT readiness truth |
| P005-UI-NEG-05 | UI exposes runtime start/stop/restart, stream mutation, broker action, order action or incident resolve/accept action |
| P005-UI-NEG-06 | visible text claims Paper ready, Live ready, broker tradable, admitted, capital allocated, production ready, China S2 pass, HFT S3 pass, Account Console runtime truth, Account Console UI complete or loop complete |
| P005-UI-NEG-07 | stale or blocked streams collapse into a generic healthy state |
| P005-UI-NEG-08 | latest/debug paths are treated as monitor evidence truth |

## 4. Browser Acceptance

Required viewport checks:

| Viewport | Width x height | Required proof |
| --- | --- | --- |
| Desktop | 1440 x 900 | context, lag strip, queue, blocker/source refs |
| Tablet | 1024 x 768 | queue remains scannable and refs do not overlap |
| Mobile | 390 x 844 | stacked context, compact lag strip and readable exception rows |

Screenshots prove rendering only. They never prove runtime truth, stream truth, account truth, order truth, ledger truth, HFT readiness, Paper readiness, Live readiness, broker tradability, admission, capital or Account Console UI completion.

## 5. Blocker Recording

If UI acceptance cannot be completed, record a typed Blocker with:

```text
Blocker:
  proposal_or_change_id: p005-intraday-monitor-exception-queue-panel
  route: /monitor
  missing_contract:
  missing_fixture:
  missing_browser_tooling:
  missing_selector:
  missing_source_ref:
  violated_boundary:
  owner:
  next_action:
```

