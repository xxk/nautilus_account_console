# P001: Daily Closeout Account Health Panel

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Status: browser_evidence_verified
- Updated: 2026-06-13
- Owner: account-console-ui
- ADR anchor: [ADR-0003](../../adr/0003-adopt-contract-first-ui-slice-development.md)
- Topic anchor: [Contract-first UI slice development](../../topics/contract-first-ui-slice-development.md)
- Design anchor: [Account Console capability UI design](../../design/account-console-capability-ui-design.md)
- Acceptance anchor: [Account Console capability UI acceptance](../../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
- Owner map: [Account Console owner map](../../ownership/account-console-owner-map.md)
- UI design: [P001 UI Design](./ui-design.md)
- UI acceptance: [P001 UI Acceptance](./ui-acceptance.md)

## 1. Purpose / 目的

This proposal defines the first contract-first UI implementation slice for Account Console: the Daily Closeout Account Health Panel.

The panel is the first visible slice of the business workbench-first Account Console. It should let operators see whether account closeout, settlement carryover, equity curve continuity and evidence availability are healthy, blocked, stale or incomplete.

## 2. Scope / 范围

In scope:

1. Define the panel read model contract.
2. Define happy, empty, blocked and stale fixtures.
3. Implement the Account Health Panel under the Daily Closeout workbench.
4. Show account/session identity, closeout state, settlement state, equity continuity, latest evidence artifact references and blockers.
5. Add deterministic UI tests, stable `data-testid` hooks and acceptance evidence.

Out of scope:

1. Direct account creation, funding allocation or broker/runtime mutation.
2. Full Daily Closeout workbench completion.
3. Full account detail workbench, order event tape or report detail panels.
4. Live/Paper readiness, admission, capital approval or tradability claims.
5. Treating raw reports as the primary operator workflow.

## 3. UI Slice Contract / UI 切片合同

```text
Owner Boundary:
  proposal_or_change_id: p001-daily-closeout-account-health-panel
  producer_owner: external strategy/runtime owner for source refs; fixture producer is account-console-contracts
  verifier_owner: account-console-contracts for fixture shape; account-console-ui for panel acceptance
  projection_owner: account-console-contracts for fixture projections; backend owner only when live read model endpoint is added
  ui_or_report_owner: account-console-frontend
  approval_owner: none
  canonical_contracts:
    - contracts/ui/panels/account_health_panel.contract.json
  canonical_source_refs:
    - source_ref
    - checksum
    - closeout_run_id
    - settlement_run_id
    - equity_curve_artifact_id
    - reducer_checkpoint_id
  write_authority:
    allowed:
      - UI panel code
      - deterministic UI fixtures
      - browser acceptance evidence
    forbidden:
      - runtime truth
      - account truth
      - broker truth
      - admission truth
      - approval truth
      - capital truth
      - accepted lifecycle or funding ledger truth
  second_implementation_rejected:
    - frontend reducer that computes account closeout truth
    - Python writer that appends accepted account/funding truth for this panel
    - browser parsing raw report/debug/latest paths as evidence truth
    - second route that implements Daily Closeout outside /closeout without owner-map update
  blocker_owner_if_missing_source: external source owner or account-console-contracts, recorded as typed blocked/partial/stale fixture
```

```text
UI Slice Contract:
  proposal_or_change_id: p001-daily-closeout-account-health-panel
  workbench: Daily Closeout
  panel: Account Health Panel
  route_or_parent_surface: /closeout
  read_model_contract: contracts/ui/panels/account_health_panel.contract.json
  fixture_refs:
    - contracts/ui/fixtures/daily_closeout/account_health_happy_path.json
    - contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json
    - contracts/ui/fixtures/daily_closeout/account_health_empty.json
    - contracts/ui/fixtures/daily_closeout/account_health_blocked_settlement.json
    - contracts/ui/fixtures/daily_closeout/account_health_stale_stream.json
    - contracts/ui/fixtures/daily_closeout/account_health_partial_evidence.json
  states:
    - happy_path
    - empty
    - blocked
    - stale
    - partial
  data_testids:
    - daily-closeout-account-health-panel
    - daily-closeout-account-health-row
    - daily-closeout-closeout-state
    - daily-closeout-settlement-state
    - daily-closeout-equity-continuity
    - daily-closeout-evidence-ref
    - daily-closeout-blocker
  user_interactions:
    - filter by account type
    - filter by closeout state
    - open evidence drill-down
    - open account detail drill-down
  source_refs_displayed:
    - account_id
    - account_type
    - session_id
    - closeout_run_id
    - settlement_run_id
    - equity_curve_artifact_id
    - reducer_checkpoint_id
  forbidden_actions:
    - account creation
    - funding allocation mutation
    - runtime state mutation
    - broker action
    - admission or capital approval action
    - order submit/cancel/replace action
  positive_acceptance:
    - UI-WB-01
    - UI-VIS-01
  negative_acceptance:
    - UI-IMPL-03
    - UI-IMPL-08
    - UI-DRIFT-CLAIM-01
    - UI-DRIFT-CLAIM-02
    - UI-DRIFT-CLAIM-05
    - UI-DRIFT-CLAIM-06
    - UI-DRIFT-ACT-01
    - UI-DRIFT-ACT-02
  visual_acceptance:
    - desktop and mobile screenshots show no overlap or hidden closeout state
  performance_acceptance:
    - panel renders deterministic fixture without unbounded list growth
  blockers:
    - missing read model fields
    - missing fixture state
    - missing source artifact references
    - unavailable frontend test runner
```

## 4. Required Artifacts / 必需产物

| Artifact | Purpose |
| --- | --- |
| `contracts/ui/panels/account_health_panel.contract.json` | typed read model for the panel |
| `contracts/ui/fixtures/daily_closeout/account_health_happy_path.json` | normal closeout fixture |
| `contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json` | ADR-0044 P078 A0-A3 closeout-backed read-model handoff fixture |
| `contracts/ui/fixtures/daily_closeout/account_health_empty.json` | no accounts or no closeout data fixture |
| `contracts/ui/fixtures/daily_closeout/account_health_blocked_settlement.json` | settlement/carryover blocked fixture |
| `contracts/ui/fixtures/daily_closeout/account_health_stale_stream.json` | stale stream/checkpoint fixture |
| `contracts/ui/fixtures/daily_closeout/account_health_partial_evidence.json` | partial evidence package fixture |
| frontend panel component and tests | visible slice and deterministic verification |
| acceptance evidence update | proof that UI and guard checks passed or typed blocker was recorded |

## 5. Design Review Gate / 设计验收门

Code implementation must not start until the proposal confirms:

1. No second runtime.
2. No second matching engine.
3. No second ledger truth.
4. Read model fields and fixture states are named.
5. Positive and negative acceptance IDs are mapped.
6. Forbidden actions and forbidden claims are named.
7. UI source artifact references are present.
8. Blocker conditions are explicit.
9. P001 UI design and UI acceptance have been reviewed before code starts.
10. [Account Console owner map](../../ownership/account-console-owner-map.md) has been confirmed and no second implementation path is introduced.

## 6. Current Acceptance Evidence / 当前验收证据

| Evidence | Result |
| --- | --- |
| Read model contract and fixtures | verified by `npm run test` |
| ADR-0044 source-backed fixture | `contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json` |
| Frontend build | pass: `npm run build` |
| Browser evidence | pass: `npm run test:e2e`; desktop/tablet/mobile screenshots under `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/` |
| Runner blocker | resolved by portable Node/npm runner: `D:\Nautilus\.tools\node-v22.22.3-win-x64` |
| Boundary | read-only fixture projection only; no runtime, account, broker, admission or capital truth |

Security follow-up:

- Closed by [P003 Frontend Dependency Security Follow-up](../p003-frontend-dependency-security-followup/README.md): `npm audit --audit-level=high`, build, fixture validation and browser evidence all pass after upgrading Vite/React plugin.
