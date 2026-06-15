# P004: Account Workbench UI Design Gate

- Proposal ID: `p004-account-workbench-summary-panel`
- Status: phase8_account_workbench_closeout_passed
- Updated: 2026-06-15
- Owner: account-console-ui
- ADR anchor: [ADR-0003](../../adr/0003-adopt-contract-first-ui-slice-development.md)
- Topic anchor: [Contract-first UI slice development](../../topics/contract-first-ui-slice-development.md)
- Design anchor: [Account Console capability UI design](../../design/account-console-capability-ui-design.md)
- Implementation design anchor: [Account Console UI implementation design](../../design/account-console-ui-implementation-design.md)
- Acceptance anchor: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- Route coverage anchor: [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
- Owner map: [Account Console owner map](../../ownership/account-console-owner-map.md)
- Workflow gate: [Account Console Proposal Workflow Stage Contract](../../workflows/proposal-gates/README.md)
- UI design: [P004 UI Design](./ui-design.md)
- UI acceptance: [P004 UI Acceptance](./ui-acceptance.md)

## 1. Purpose / 目的

This proposal defines the proposal-level design and acceptance boundary for the Account Workbench at `/accounts/{account_id}` and its account drill-down routes.

The slice answers one operator question:

```text
What is the current account state, which source refs prove it, and which blockers must be handled before deeper account investigation continues?
```

P004 prevents the Account Workbench from drifting into a trading terminal, a raw artifact browser, a browser-side account calculator, disconnected route islands or a second account truth writer.

## 2. Scope / 范围

In scope:

1. Define the Account Workbench route design for `/accounts/{account_id}`.
2. Define account drill-down route design gates for orders, order detail, positions, settlement, equity, reconcile, incidents and evidence.
3. Define the summary panel read model contract requirements before implementation.
4. Define secondary panel contract requirements before each drill-down implementation.
5. Define happy, empty, blocked, stale and partial fixture requirements.
6. Define stable selectors for account identity, account summary, blockers, source refs, tab context and drill-down panels.
7. Define browser acceptance for desktop, tablet and mobile route opening.
8. Lock the account drill-down route hierarchy so secondary tabs remain under Account Workbench context.
9. Split Account Workbench UI landing into P004 phases so future implementation can close out one panel family at a time.

Out of scope:

1. Implementing the panel UI.
2. Implementing orders, positions, settlement, equity, reconcile, incidents or evidence drill-down panels.
3. Direct order submission, cancellation, replacement or broker actions.
4. Writing runtime, account, broker, admission, approval or capital truth.
5. Treating raw reports, screenshots, HTML reports, stdout or latest/debug paths as account truth.

## 3. Owner Boundary / Owner 边界

Workflow metadata:

```text
Proposal Workflow Stage Contract:
  manifest: docs/workflows/proposal-gates/proposal_gate_manifest.yaml
  gate_family: account_console_proposal_workflow_stage_contract
  stage_contract: scaffold -> workflow_contract -> ui_design_acceptance -> source_contracts -> implementation_evidence -> issue_ledger -> closeout
  proposal_gate_boundary: Proposal Gates may block phase advancement but must not write runtime/account/broker/admission/approval/capital/trading-readiness truth.
  source_gate_boundary: contracts, fixtures, browser evidence and source/read-model evidence remain owned by their declared source owners.
```

```text
Owner Boundary:
  proposal_or_change_id: p004-account-workbench-summary-panel
  producer_owner: external strategy/runtime owner for normalized account/order/fill/settlement artifacts; fixture producer is account-console-contracts
  verifier_owner: account-console-contracts for fixture shape; account-console-ui for panel acceptance
  projection_owner: account-console-backend when live read model is added; account-console-contracts for deterministic fixtures before live endpoint
  ui_or_report_owner: account-console-frontend
  approval_owner: none
  canonical_contracts:
    - contracts/ui/panels/account_summary_panel.contract.json
    - contracts/ui/panels/account_orders_panel.contract.json
    - contracts/ui/panels/account_order_detail_panel.contract.json
    - contracts/ui/panels/account_positions_panel.contract.json
    - contracts/ui/panels/account_settlement_panel.contract.json
    - contracts/ui/panels/account_equity_panel.contract.json
    - contracts/ui/panels/account_reconcile_panel.contract.json
    - contracts/ui/panels/account_incidents_panel.contract.json
    - contracts/ui/panels/account_evidence_panel.contract.json
  canonical_source_refs:
    - account_id
    - account_kind
    - session_id
    - run_id
    - trading_day
    - reducer_checkpoint_id
    - account_snapshot_ref
    - settlement_ref
    - position_carryover_ref
    - blocker_ref
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
    - browser reducer that computes account equity, settlement or tradability truth
    - Python writer that appends accepted account/funding/lifecycle truth for this panel
    - frontend raw report parser that replaces normalized account events or read models
    - disconnected account detail page that loses Account Workbench parent context
  blocker_owner_if_missing_source: external source owner or account-console-contracts, recorded as typed blocked/partial/stale fixture
```

## 4. UI Slice Contract / UI 切片合同

```text
UI Slice Contract:
  proposal_or_change_id: p004-account-workbench-summary-panel
  workbench: Account Workbench
  panel: Account Summary Panel
  route_or_parent_surface: /accounts/{account_id}
  covered_routes:
    - /accounts
    - /accounts/{account_id}
    - /accounts/{account_id}/orders
    - /accounts/{account_id}/orders/{client_order_id}
    - /accounts/{account_id}/positions
    - /accounts/{account_id}/settlement
    - /accounts/{account_id}/equity
    - /accounts/{account_id}/reconcile
    - /accounts/{account_id}/incidents
    - /accounts/{account_id}/evidence
  read_model_contract: contracts/ui/panels/account_summary_panel.contract.json
  secondary_read_model_contracts:
    - contracts/ui/panels/account_orders_panel.contract.json
    - contracts/ui/panels/account_order_detail_panel.contract.json
    - contracts/ui/panels/account_positions_panel.contract.json
    - contracts/ui/panels/account_settlement_panel.contract.json
    - contracts/ui/panels/account_equity_panel.contract.json
    - contracts/ui/panels/account_reconcile_panel.contract.json
    - contracts/ui/panels/account_incidents_panel.contract.json
    - contracts/ui/panels/account_evidence_panel.contract.json
  fixture_refs:
    - contracts/ui/fixtures/account_workbench/account_summary_happy_path.json
    - contracts/ui/fixtures/account_workbench/account_summary_empty.json
    - contracts/ui/fixtures/account_workbench/account_summary_blocked.json
    - contracts/ui/fixtures/account_workbench/account_summary_stale_stream.json
    - contracts/ui/fixtures/account_workbench/account_summary_partial_evidence.json
  states:
    - happy_path
    - empty
    - blocked
    - stale
    - partial
  data_testids:
    - account-workbench-summary-panel
    - account-workbench-context-bar
    - account-workbench-tab-list
    - account-summary-metric-strip
    - account-summary-source-ref
    - account-summary-blocker
    - account-summary-empty-state
    - account-summary-stale-state
    - account-summary-detail-drawer
    - account-orders-panel
    - account-order-detail-panel
    - account-positions-panel
    - account-settlement-panel
    - account-equity-panel
    - account-reconcile-panel
    - account-incidents-panel
    - account-evidence-panel
  user_interactions:
    - switch account context from account selector
    - open source ref detail drawer
    - open blocker detail drawer
    - navigate to account drill-down tabs without losing account context
    - open order lifecycle detail without treating final order state as lifecycle truth
    - open evidence refs without promoting raw payloads to account truth
  source_refs_displayed:
    - account_id
    - account_kind
    - portfolio_uid
    - session_id
    - run_id
    - trading_day
    - reducer_checkpoint_id
    - account_snapshot_ref
    - settlement_ref
    - position_carryover_ref
  forbidden_actions:
    - order submit/cancel/replace/modify
    - broker action
    - account lifecycle mutation
    - funding allocation mutation
    - runtime state mutation
    - admission or capital approval action
  positive_acceptance:
    - UI-WB-03
    - UI-OBS-02
    - UI-ROUTE-01
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
    - desktop, tablet and mobile screenshots show stable context, metric strip and blocker/source ref areas
  performance_acceptance:
    - account context switch does not create unbounded DOM growth
  blockers:
    - missing read model contract
    - missing account fixture state
    - missing account snapshot or settlement refs
    - unavailable browser runner
```

## 5. Design Gate / 设计门

Code implementation must not start until this proposal confirms:

1. `/accounts/{account_id}` remains the Account Workbench primary route.
2. Secondary account routes remain tabs, drawers or drill-downs under Account Workbench context.
3. Account drill-down routes remain tabs, drawers or deep links under Account Workbench context.
4. Account values are read-model projections with source refs or typed blockers.
5. Orders, fills, positions, settlement, equity, reconcile, incidents and evidence each declare panel-specific source refs before implementation.
6. No browser-side account, order lifecycle, settlement, equity, reconcile or tradability truth is introduced.
7. The proposal docs gate passes: `python scripts\check_proposal_docs.py --root . --proposal-id p004-account-workbench-summary-panel`.
7. Positive and negative acceptance IDs are mapped.
8. Forbidden actions and forbidden claims are named.
9. Stable selectors are named before implementation.
10. Browser evidence requirements are declared.
11. [P004 UI Design](./ui-design.md) and [P004 UI Acceptance](./ui-acceptance.md) have been reviewed before code starts.

## 5.1 Phase Landing Model / Phase 落地模型

P004 lands Account Workbench design and acceptance as phases. A phase may be implemented independently only if it preserves Account Workbench context and does not claim broader route completion.

| Phase | Surface | Status | Closeout requirement |
| --- | --- | --- | --- |
| Phase 1 | Summary contract and fixtures | completed | contract, fixtures and source refs |
| Phase 2 | Account Summary Panel | completed | selectors, browser evidence and forbidden scan |
| Phase 3 | Orders and order lifecycle | completed | official event lineage and report provenance evidence |
| Phase 4 | Positions | completed | carryover/settlement refs, read-only UI and browser evidence |
| Phase 5 | Settlement and equity | completed | ledger-derived settlement/equity refs, read-only UI and browser evidence |
| Phase 6 | Reconcile and incidents | completed | mismatch/incident owner and next-action refs; read-only UI and browser evidence accepted |
| Phase 7 | Evidence | completed | schema/checksum/source lineage, lazy raw payload refs, read-only UI and browser evidence accepted |
| Phase 8 | Workbench closeout | completed | local checks, browser screenshots and matrix status update |

Design-gate readiness means the route has design and acceptance boundaries. It does not mean implementation, browser evidence or runtime/account truth has been accepted.

## 6. Current Acceptance State / 当前验收状态

| Evidence | Result |
| --- | --- |
| Proposal-level UI design | ready: [P004 UI Design](./ui-design.md) |
| Proposal-level UI acceptance | ready: [P004 UI Acceptance](./ui-acceptance.md) |
| Route coverage matrix | ready: Account Workbench routes are bound to P004 design gate |
| Phase-level landing map | ready: P004 phases are declared in [phase-plan.md](./phase-plan.md), [ui-design.md](./ui-design.md), [ui-acceptance.md](./ui-acceptance.md) and [acceptance.md](./acceptance.md) |
| Read model contract and fixtures | accepted: `../../acceptance/2026-06-14-p004-phase1-summary-contract-fixtures.json`, checksum `sha256:0e1cb660e0ccb8309006b1c58ff15d8b230fffc058d6e5fdd400a35ebe97ed73` |
| Browser evidence | accepted for Phase 2 Account Summary UI only: `../../acceptance/2026-06-14-p004-phase2-summary-ui-browser-evidence.json`, checksum `sha256:6ad5b945d88b360e419292674bb0df42000a54ecf084e6c47197b974f1fe26c4` |
| Orders contract and fixtures | accepted for Phase 3 contract/fixture gate only: `../../acceptance/2026-06-14-p004-phase3-orders-contract-fixtures.json`, checksum `sha256:c494a7ad499bb93898fcd59d36b6277c19e2f24f117e4d2f10150b346d3eb814` |
| Orders browser evidence | accepted for Phase 3 orders UI only: `../../acceptance/2026-06-14-p004-phase3-orders-ui-browser-evidence.json`, checksum `sha256:26181b95bc374b5390b79407835f6c974d7b8a4ce86767dccc1efc58a4314822` |
| Positions contract and fixtures | accepted for Phase 4 contract/fixture gate only: `../../acceptance/2026-06-14-p004-phase4-positions-contract-fixtures.json`, checksum `sha256:631949614834dbb31b918e381da06c772a5579a8572fd8670c540eb8596b6c91` |
| Positions browser evidence | accepted for Phase 4 positions UI only: `../../acceptance/2026-06-14-p004-phase4-positions-ui-browser-evidence.json`, checksum `sha256:10fc038c361f025400bc2b71fde886fdfa0fa6f93c6aebd35f35aae904a413ab` |
| Settlement/equity contract and fixtures | accepted for Phase 5 contract/fixture gate only: `../../acceptance/2026-06-14-p004-phase5-settlement-equity-contract-fixtures.json`, checksum `sha256:f881d2b0dbb0b3496dacf50abb0ae84e2b84f3bfbf4ffcf04f1ac07c6ac41fa1` |
| Settlement/equity browser evidence | accepted for Phase 5 settlement/equity UI only: `../../acceptance/2026-06-14-p004-phase5-settlement-equity-ui-browser-evidence.json`, checksum `sha256:8a53d446b5f38a8c2fb59848f49016d0e73fc248cf489bb114fa6cc20c8bff37` |
| Reconcile/incidents contract and fixtures | accepted for Phase 6 contract/fixture gate only: `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-contract-fixtures.json`, checksum `sha256:7918fbe64ec607f80809dea53c107fba8f17570e18ab96ad369067a8fc1479e6` |
| Reconcile/incidents browser evidence | accepted for Phase 6 reconcile/incidents UI only: `../../acceptance/2026-06-14-p004-phase6-reconcile-incidents-ui-browser-evidence.json`, checksum `sha256:0ef92a65a91e12b6c6f70e95a55853c6f9c194cc880bef85f7cd754bfb2a6d54` |
| Evidence contract and fixtures | accepted for Phase 7 contract/fixture gate only: `../../acceptance/2026-06-14-p004-phase7-evidence-contract-fixtures.json`, checksum `sha256:f288e3b7c6e1ae5c4412d44e4b660cf3c64053661fab0d084284df10b9c4c481` |
| Evidence browser evidence | accepted for Phase 7 evidence UI only: `../../acceptance/2026-06-15-p004-phase7-evidence-ui-browser-evidence.json`, checksum `sha256:6d1f754ef2c9e676d44a109ce6cad4e9e54e68063953e5058ecf00a393bfe638` |
| Phase 8 Account Workbench closeout | accepted for P004 scoped closeout only: `../../acceptance/2026-06-15-p004-phase8-account-workbench-closeout.json`, checksum `sha256:fd725adaf513461005d0df172120049d1cc9e68ef39e68e6eadd739bdbff01d0` |

Phase 2 through Phase 7 browser evidence plus Phase 8 closeout close the P004 Account Workbench scoped phases only. They do not complete the full Account Console UI, ADR0044/ADR0045 loop, P077/P078, sibling owner work or runtime/account/ledger truth.
