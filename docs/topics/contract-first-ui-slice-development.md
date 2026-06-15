# Contract-First UI Slice Development Topic / 契约优先 UI 切片开发专题

- Updated: 2026-06-13
- Status: active
- Scope: long-term implementation method for Account Console UI delivery
- Decision anchor: [ADR-0003](../adr/0003-adopt-contract-first-ui-slice-development.md)
- Navigation anchor: [ADR-0002](../adr/0002-adopt-business-workbench-first-account-console-navigation.md)
- Acceptance anchor: [Account Console capability UI acceptance](../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
- UI implementation design: [Account Console UI implementation design](../design/account-console-ui-implementation-design.md)
- UI implementation acceptance: [Account Console UI implementation acceptance](../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- UI anti-drift acceptance: [Account Console UI anti-drift acceptance](../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
- UI route coverage matrix: [Account Console UI route coverage matrix](../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
- Owner map: [Account Console owner map](../ownership/account-console-owner-map.md)

## 1. Purpose / 目的

This topic owns the long-term implementation method for AI-assisted Account Console UI development.

ADR-0003 records why the project chooses contract-first UI slices. This topic records how successor proposals and changes should apply that decision without drifting into page-first, mock-only or invented-data development.

## 2. Standard Slice Chain / 标准切片链路

Every UI implementation slice should follow this chain:

```text
Workbench
  -> Panel
  -> Read Model Contract
  -> Fixture
  -> UI Slice
  -> Acceptance
```

The default unit is one panel inside one business workbench. A proposal may include multiple panels only when it declares why they must be delivered together and how each panel keeps its own contract and acceptance.

Route hierarchy is fixed unless a successor proposal changes it:

1. Seven primary workbench pages are the product entry points.
2. The 26-route map is a deep-link capability map, not a flat navigation menu.
3. Secondary routes must remain tabs, drawers, drill-downs or deep links under a parent workbench.
4. Any promotion of a secondary route to a primary page needs proposal-level UI design and UI acceptance.

## 3. Recommended Contract Layout / 推荐契约布局

```text
contracts/ui/
  workbenches/
    daily_closeout.contract.json
    intraday_monitor.contract.json
    account_workbench.contract.json
    allocation_admin.contract.json
    risk_reconcile.contract.json
    evidence_explorer.contract.json
    stream_ops.contract.json

  panels/
    account_health_panel.contract.json
    exception_queue_panel.contract.json
    order_event_tape.contract.json
    report_detail_panel.contract.json
    funding_allocation_panel.contract.json

  fixtures/
    daily_closeout/
      happy_path.json
      blocked_settlement.json
      stale_stream.json
    account_workbench/
      order_lifecycle_with_reports.json
```

This is a recommended target shape. A proposal should create only the smallest subset it needs.

## 4. Required Slice Contract / 必需切片合同

Every implementation proposal or successor change must fill this block before coding:

```text
UI Slice Contract:
  proposal_or_change_id:
  workbench:
  panel:
  route_or_parent_surface:
  read_model_contract:
  fixture_refs:
  states:
    - happy_path
    - empty
    - blocked
    - stale_or_partial
  data_testids:
  user_interactions:
  source_refs_displayed:
  forbidden_actions:
  positive_acceptance:
  negative_acceptance:
  visual_acceptance:
  performance_acceptance:
  blockers:
```

Every UI proposal/change must also fill the anti-drift checklist from [Account Console UI anti-drift acceptance](../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md).

Every UI proposal/change that touches a route must confirm or update the route row in [Account Console UI route coverage matrix](../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md).

Every UI proposal/change that introduces a producer, verifier, projection, request surface or panel must confirm the [Account Console owner map](../ownership/account-console-owner-map.md) and fill an Owner Boundary block before coding.

Each UI implementation proposal should also include:

```text
ui-design.md      panel-level layout, state matrix, interactions, visual rules and test hooks
ui-acceptance.md  panel-level positive, negative, browser, selector and screenshot acceptance
```

## 5. AI Implementation Workflow / AI 实现流程

AI should implement UI slices in this order:

1. Select one workbench and one panel.
2. Fill the UI Slice Contract.
3. Land panel-level UI design and UI acceptance.
4. Add or update the read model contract.
5. Add happy-path and negative/blocked/stale fixtures.
6. Implement the panel or route composition.
7. Add deterministic tests and `data-testid` hooks.
8. Run build, test and forbidden wording scans.
9. Update acceptance evidence.

AI must stop, split or record a typed blocker if:

1. A panel needs fields that no read model contract provides.
2. A request/projection control would mutate accepted ledger truth.
3. A page needs multiple unimplemented panels to be useful.
4. The slice requires backend/Rust behavior outside its declared contract.
5. Visual or performance acceptance cannot be run and no blocker is recorded.

## 6. First Slice Roadmap / 首批切片路线

| Order | Workbench | Panel | Proposal status | Why first |
| --- | --- | --- | --- | --- |
| 1 | Daily Closeout | Account Health Panel | [P001](../proposals/p001-daily-closeout-account-health-panel/README.md) | first-screen control tower and closeout health |
| 2 | Intraday Monitor | Exception Queue Panel | candidate | exception-first operations workflow |
| 3 | Account Workbench | Order Event Tape | candidate | official order lifecycle is core truth projection |
| 4 | Account Workbench | Report Detail Panel | candidate | report provenance and lazy payload boundary |
| 5 | Allocation Admin | Account Registry Panel | candidate | account management entry, request/projection boundary |
| 6 | Allocation Admin | Funding Allocation Replay Panel | candidate | funding conservation and replay visibility |
| 7 | Stream Ops | Stream Health Panel | candidate | HFT and hot path observability foundation |

## 7. Topic-Level Acceptance / 专题级验收

| Acceptance | Required evidence | Must fail if |
| --- | --- | --- |
| Slice contract exists | each UI implementation proposal includes workbench, panel, read model contract, fixtures and acceptance IDs | implementation starts from a whole page without a panel contract |
| Fixture-first behavior | happy, empty, blocked and stale/partial fixtures exist or typed blockers are filed | UI uses imagined API response fields |
| Read-only boundary | panel declares source refs and forbidden actions | UI mutates runtime/account/broker/admission/capital truth |
| Testability | stable `data-testid` hooks and deterministic tests are added for the slice | visual behavior is only manually inspected |
| Scope discipline | one workbench/panel is the default unit; multi-panel work must justify split/aggregation | AI lands an entire workbench without slice contracts |
| Acceptance linkage | slice maps to UI acceptance IDs in `docs/acceptance/2026-06-13-account-console-capability-ui-acceptance.md` | slice cannot be tied to an acceptance row |
| Route hierarchy | proposal declares whether it touches a primary workbench or secondary deep link | AI turns the route map into a flat 26-page product menu |
| Anti-drift checklist | proposal/change includes route tier, parent context, forbidden actions and forbidden claims | implementation starts before anti-drift acceptance is filled |
| Route coverage | proposal/change confirms coverage matrix rows for every route touched | a route is implemented without tier, parent workbench, acceptance IDs and proposal status |
| Owner boundary | proposal/change declares producer, verifier, projection, UI/report and approval owner | implementation creates a second source writer, second runtime or ambiguous owner lane |

## 8. Forbidden Drift / 禁止跑偏

1. Do not create a second runtime truth, matching truth, ledger truth, capital truth or broker truth.
2. Do not make raw reports the primary user workflow; raw reports remain provenance and debug drill-down.
3. Do not show `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated`, `can trade`, `submit order`, `place order`, `cancel order` or `replace order`.
4. Do not implement account creation, funding or allocation as direct state mutation unless a proposal defines a request/projection contract and acceptance.
5. Do not treat visual mockups or screenshots as a substitute for read model contracts and fixtures.
