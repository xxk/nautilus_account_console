# P005: Intraday Monitor Exception Queue Panel

- Proposal ID: `p005-intraday-monitor-exception-queue-panel`
- Status: phase1_contract_fixture_gate_passed
- Updated: 2026-06-15
- Owner: account-console-ui
- ADR anchor: [ADR-0003](../../adr/0003-adopt-contract-first-ui-slice-development.md)
- Design anchor: [Account Console capability UI design](../../design/account-console-capability-ui-design.md)
- Implementation design anchor: [Account Console UI implementation design](../../design/account-console-ui-implementation-design.md)
- Acceptance anchor: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- Route coverage anchor: [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
- Workflow gate: [Account Console Proposal Workflow Stage Contract](../../workflows/proposal-gates/README.md)
- UI design: [P005 UI Design](./ui-design.md)
- UI acceptance: [P005 UI Acceptance](./ui-acceptance.md)

## 1. Purpose

P005 defines the contract-first boundary for the Intraday Monitor at `/monitor`.

The slice answers one operator question:

```text
Which intraday exceptions, stale streams, lag states and incidents require attention, and which typed source refs prove that projection?
```

The panel is read-only. It may display monitor queues, lag summaries, freshness states, incident refs and blocker refs from accepted contracts or fixtures. It must not become a runtime controller, stream scheduler, broker action surface, HFT readiness surface, issue resolver or second truth writer.

## 2. Scope

In scope:

1. Define `/monitor` proposal-level UI design and UI acceptance.
2. Define the Intraday Monitor read-model contract before implementation.
3. Define deterministic current, empty, blocked, stale and partial fixture states.
4. Define stable selectors for monitor shell, exception queue, lag strip, stream state, incident refs and blocker refs.
5. Keep all monitor evidence read-only and source-ref backed.

Out of scope:

1. Implementing the `/monitor` UI route.
2. Opening browser evidence for `/monitor`.
3. Starting, stopping or repairing runtimes, schedulers, streams, gateways or broker connections.
4. Marking incidents resolved or accepted.
5. Claiming HFT readiness, China S2 pass, Paper readiness, Live readiness, broker tradability, admission or capital truth.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p005-intraday-monitor-exception-queue-panel
  producer_owner: external runtime/stream/order/incident owners for normalized monitor events; fixture producer is account-console-contracts
  verifier_owner: account-console-contracts for fixture shape; account-console-ui for panel acceptance
  projection_owner: account-console-backend when live read model is added; account-console-contracts for deterministic fixtures before live endpoint
  ui_or_report_owner: account-console-frontend
  approval_owner: none
  canonical_contracts:
    - contracts/ui/panels/intraday_monitor_panel.contract.json
  canonical_source_refs:
    - monitor_snapshot_ref
    - stream_cursor_ref
    - lag_probe_ref
    - incident_ref
    - blocker_ref
  write_authority:
    allowed:
      - UI panel code after contract/fixture gate
      - deterministic UI fixtures
      - browser acceptance evidence after implementation
    forbidden:
      - runtime truth
      - stream truth
      - scheduler truth
      - account truth
      - order truth
      - ledger truth
      - broker truth
      - admission truth
      - capital truth
      - HFT readiness truth
  second_implementation_rejected:
    - browser-side stream freshness reducer that replaces source owner artifacts
    - UI incident resolver that writes accepted repair state
    - frontend runtime control surface hidden behind monitor actions
    - second artifact root or latest/debug path treated as monitor truth
  blocker_owner_if_missing_source: external source owner or account-console-contracts, recorded as typed blocked/partial/stale fixture
```

## 4. UI Slice Contract

```text
UI Slice Contract:
  proposal_or_change_id: p005-intraday-monitor-exception-queue-panel
  workbench: Intraday Monitor
  panel: Intraday Monitor Exception Queue Panel
  route_or_parent_surface: /monitor
  read_model_contract: contracts/ui/panels/intraday_monitor_panel.contract.json
  fixture_refs:
    - contracts/ui/fixtures/intraday_monitor/intraday_monitor_current.json
    - contracts/ui/fixtures/intraday_monitor/intraday_monitor_empty.json
    - contracts/ui/fixtures/intraday_monitor/intraday_monitor_blocked.json
    - contracts/ui/fixtures/intraday_monitor/intraday_monitor_stale.json
    - contracts/ui/fixtures/intraday_monitor/intraday_monitor_partial.json
  states:
    - current
    - empty
    - blocked
    - stale
    - partial
  data_testids:
    - intraday-monitor-panel
    - intraday-monitor-context-bar
    - intraday-monitor-lag-strip
    - intraday-monitor-exception-queue
    - intraday-monitor-stream-state
    - intraday-monitor-incident-row
    - intraday-monitor-source-ref
    - intraday-monitor-blocker
  forbidden_actions:
    - runtime start/stop/restart
    - stream scheduler mutation
    - broker action
    - order submit/cancel/replace/modify
    - incident resolve/accept/mutate
    - admission or capital approval action
  positive_acceptance:
    - UI-WB-02
    - UI-ROUTE-01
    - UI-HFT-01
  negative_acceptance:
    - UI-IMPL-03
    - UI-IMPL-08
    - UI-DRIFT-CLAIM-01
    - UI-DRIFT-CLAIM-02
    - UI-DRIFT-CLAIM-05
    - UI-DRIFT-CLAIM-06
    - UI-DRIFT-ACT-01
    - UI-DRIFT-ACT-02
```

## 5. Current Evidence

- Phase 1 contract/fixture gate evidence: [2026-06-15 P005 Phase 1 contract/fixtures](../../acceptance/2026-06-15-p005-phase1-intraday-monitor-contract-fixtures.json)
- Prior blocker superseded: [2026-06-15 P010 Intraday Monitor read-model blocker](../../acceptance/2026-06-15-p010-intraday-monitor-read-model-blocker.json)

