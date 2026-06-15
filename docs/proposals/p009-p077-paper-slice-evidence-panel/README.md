# P009: P077 Paper Slice Evidence Package Projection

- Proposal ID: `p009-p077-paper-slice-evidence-panel`
- Status: readonly_fixture_refresh
- Updated: 2026-06-14
- Owner: account-console-ui
- ADR anchor: [ADR-0003](../../adr/0003-adopt-contract-first-ui-slice-development.md)
- Topic anchor: [Contract-first UI slice development](../../topics/contract-first-ui-slice-development.md)
- Parent design gate: [P004 Account Workbench](../p004-account-workbench-summary-panel/README.md)
- Route coverage anchor: [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
- Owner map: [Account Console owner map](../../ownership/account-console-owner-map.md)
- UI design: [P009 UI Design](./ui-design.md)
- UI acceptance: [P009 UI Acceptance](./ui-acceptance.md)

## 1. Purpose / 目的

This proposal defines the proposal-level UI slice contract for rendering the P077 bounded Paper slice read model first created by E90 and currently refreshed from E100/E101/E102 as an Account Evidence package projection.

It answers one operator question:

```text
What exactly happened in the bounded P077 Paper slice, which owner artifacts prove it, and what must remain blocked before any runtime, readiness or admission claim?
```

P009 now includes a read-only frontend implementation and browser evidence for the P077 fixture through the generic Account Evidence Panel, with the current fixture bound to E100 filled/reconciled evidence, E101 no-send evidence hygiene audit and E102 no-active-authorization closeout. It does not submit an order, mutate account state or turn Account Console into runtime truth.

## 2. Scope / 范围

In scope:

1. Bind the P077 Paper slice as an evidence package under Account Workbench evidence context.
2. Define the panel-level UI design and UI acceptance before implementation.
3. Require typed E87/E88/E89/E90/E91/E100/E101/E102 refs, checksums, owners and rejection rules.
4. Preserve the P077 fixture as read-only projection evidence only.
5. Keep `/orders/p077-paper-slice` as a fixture contract route identifier while the product UI renders under Account Workbench route hierarchy.
6. Record browser evidence for desktop, tablet and mobile viewports.

Out of scope:

1. Adding a new top-level `/orders/p077-paper-slice` product route.
2. Order submit, cancel, replace, broker action or Paper retry.
3. Runtime, ledger, account, broker, admission, approval, capital or readiness truth.
4. Treating fixture content, UI text, screenshots, latest/debug paths, raw reports or stdout as source truth.

## 3. Owner Boundary / Owner 边界

```text
Owner Boundary:
  proposal_or_change_id: p009-p077-paper-slice-evidence-panel
  producer_owner: nautilus_ctp_adapter for E100 lifecycle/fill/reconcile source artifact and E101 evidence hygiene audit; nautilus_strategies for E102 governance closeout
  verifier_owner: account-console-contracts for contract/fixture shape; account-console-ui for future panel acceptance
  projection_owner: account-console-contracts for deterministic fixture before any live endpoint
  ui_or_report_owner: account-console-frontend only after implementation proposal/change starts
  approval_owner: none
  canonical_contracts:
    - contracts/ui/panels/p077_paper_slice_panel.contract.json
  canonical_source_refs:
    - D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T112841Z/p077_t6_e86_filled_close_yesterday_reconciled.json
    - D:/Nautilus/nautilus_strategies/docs/changes/20260614__paper__p077-safer-retry-lane/evidence/20260614T113441Z_e87_post_fill_owner_handoff_audit_no_send.json
    - D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T130516Z/p077_t6_e100_bounded_paper_close_yesterday_filled_reconciled.json
    - D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T130516Z/p077_t6_e101_post_e100_evidence_hygiene_status_audit_no_send.json
    - D:/Nautilus/nautilus_strategies/docs/changes/20260614__paper__p077-safer-retry-lane/evidence/20260614T131947Z_p077_t6_e102_post_e101_formal_closeout_decision_no_send.json
    - D:/Nautilus/nautilus_account_console/docs/acceptance/2026-06-14-p077-e87-account-console-read-model-blocker.json
    - D:/Nautilus/nautilus_account_console/docs/acceptance/2026-06-14-p077-e90-ui-route-acceptance-blocker.json
  write_authority:
    allowed:
      - proposal-level UI design docs
      - proposal-level UI acceptance docs
    - future read-only Account Evidence Panel code after implementation starts
      - future browser acceptance evidence after implementation starts
    forbidden:
      - runtime truth
      - ledger truth
      - account truth
      - broker truth
      - admission truth
      - approval truth
      - capital truth
      - Paper readiness or Live readiness truth
      - order submit/cancel/replace action
  second_implementation_rejected:
    - top-level order page outside Account Workbench hierarchy
    - P077-specific frontend route branch or component outside the Account Evidence owner
    - browser reducer that recomputes fills, positions or reconcile state
    - frontend parser that turns raw report/debug/latest payloads into order truth
    - second fixture or schema family that duplicates p077_paper_slice_panel.v1
    - UI wording that upgrades a bounded filled slice into Paper readiness or broker tradability
  blocker_owner_if_missing_source: nautilus_ctp_adapter, nautilus_strategies or account-console-contracts, recorded as typed blocker
```

## 4. UI Slice Contract / UI 切片合同

```text
UI Slice Contract:
  proposal_or_change_id: p009-p077-paper-slice-evidence-panel
  workbench: Account Workbench
  panel: Account Evidence Panel with P077 evidence package row
  route_or_parent_surface: /accounts/{account_id}/orders/{client_order_id}
  secondary_parent_surface: /accounts/{account_id}/evidence
  contract_route_identifier: /orders/p077-paper-slice
  route_mapping_rule: do not implement /orders/p077-paper-slice as a top-level route or P077-specific frontend branch; render it through Account Evidence context or record a typed blocker
  read_model_contract: contracts/ui/panels/p077_paper_slice_panel.contract.json
  fixture_refs:
    - contracts/ui/fixtures/p077_paper_slice/e87_close_yesterday_filled.json
    - contracts/ui/fixtures/p077_paper_slice/e100_close_yesterday_filled_e102_closeout.json
  states:
    - filled_bounded_slice
    - blocked_missing_ref
    - stale_or_mismatched_checksum
    - no_active_authorization
  data_testids:
    - account-evidence-panel
    - account-evidence-context-bar
    - account-evidence-table
    - account-evidence-package-row
    - account-evidence-boundary-list
    - account-evidence-source-ref
    - account-evidence-rejection-rule
    - account-evidence-blocker
  user_interactions:
    - open evidence ref detail drawer
    - copy source ref and checksum
    - switch between slice summary, lifecycle evidence and boundary evidence tabs
  source_refs_displayed:
    - account_id
    - instrument_id
    - side
    - offset
    - quantity
    - lifecycle source_ref and checksum
    - governance handoff source_ref and checksum
    - producer_owner
    - projection_owner
  forbidden_actions:
    - order submit/cancel/replace
    - broker action
    - runtime mutation
    - account lifecycle mutation
    - admission or capital approval action
    - Paper retry authorization
  positive_acceptance:
    - UI-OBS-05
    - UI-OBS-06
    - UI-OBS-12
    - UI-ROUTE-02
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
    - desktop, tablet and mobile screenshots show source refs, boundary flags and rejection rules without overlap
  performance_acceptance:
    - deterministic fixture render does not create unbounded DOM growth
  blockers:
    - missing proposal-level browser evidence
    - missing or stale P077 fixture
    - contract route cannot be mapped under Account Workbench context
    - forbidden readiness or order-action wording appears
```

## 5. Current Acceptance Evidence / 当前验收证据

| Evidence | Result |
| --- | --- |
| E90 read-only contract/fixture | available and bound by checksum |
| E91 UI route blocker | resolved for this read-only projection by E92 design gate plus E93 implementation/browser evidence |
| E93 implementation/browser evidence | `../../acceptance/2026-06-14-p077-p009-ui-implementation-browser-evidence.json`, checksum `sha256:4fc4cedaa0c6f7bb67ab1e6dca1302ffa51ae9838faff61e7a3eca892ee270ed` |
| E100/E102 fixture refresh | `../../acceptance/2026-06-14-p077-e100-e102-readonly-fixture-refresh.json`, checksum `sha256:4387706e6a740f3267091c009ae556a78bab6ca26e721279bc3290fd8479974c` |
| Frontend implementation | P077 read-only evidence package rendered by the generic Account Evidence Panel under `/accounts/acct.demo-19053/evidence` |
| Browser evidence | desktop/tablet/mobile screenshots under `../../acceptance/browser-evidence/p009-p077-paper-slice-evidence-panel/` |
| Boundary | read-only UI projection only; no runtime, ledger, account, broker, readiness, admission or capital truth |
