# P009 Acceptance / 验收

- Proposal ID: `p009-p077-paper-slice-evidence-panel`
- Status: account_evidence_owner_unified
- Updated: 2026-06-14
- Inherits:
  - [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
  - [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
  - [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
  - [P009 UI Acceptance](./ui-acceptance.md)

## 1. Positive Acceptance / 正向验收

| ID | Acceptance | Evidence |
| --- | --- | --- |
| P009-POS-01 | P077 Paper slice evidence package has proposal-level UI design and UI acceptance before implementation | [ui-design.md](./ui-design.md), [ui-acceptance.md](./ui-acceptance.md) |
| P009-POS-02 | package is bound to Account Workbench evidence context instead of a new top-level route or P077-specific frontend route branch | [README](./README.md), route coverage matrix |
| P009-POS-03 | E90 contract and fixture are named as read-only projection inputs | [README](./README.md) |
| P009-POS-04 | E91 UI route blocker retry condition is satisfied at design-gate level only | this file |
| P009-POS-05 | forbidden actions and forbidden claims are listed before code starts | [README](./README.md), [ui-acceptance.md](./ui-acceptance.md) |
| P009-POS-06 | Implementation/browser evidence exists for the P077 read-only evidence package through Account Evidence owner; broader Account Workbench rows remain separately gated | E93 implementation/browser evidence plus owner-unified e2e |
| P009-POS-07 | Account Evidence Panel renders read-only E90/E100/E102 fields as a source-linked package under Account Workbench evidence context | E93 `../../acceptance/2026-06-14-p077-p009-ui-implementation-browser-evidence.json`, checksum `sha256:4fc4cedaa0c6f7bb67ab1e6dca1302ffa51ae9838faff61e7a3eca892ee270ed` |
| P009-POS-08 | desktop/tablet/mobile browser evidence exists for P009 and P001 regression remains green | E93 browser evidence and `npm run test:e2e` result |
| P009-POS-09 | panel fixture is refreshed from E100/E101/E102 source refs/checksums without creating runtime, ledger, trading, readiness, admission or capital truth | `../../acceptance/2026-06-14-p077-e100-e102-readonly-fixture-refresh.json`, checksum `sha256:4387706e6a740f3267091c009ae556a78bab6ca26e721279bc3290fd8479974c` |
| P009-POS-10 | E105 non-ready/no-active-authorization status is aligned as governance provenance only and does not require a frontend/runtime mutation | `../../acceptance/2026-06-14-p077-e105-status-normalization-readonly-alignment.json`, checksum `sha256:b6f913a24613e83386f18d7ef2c41d8183adc43fed30a732a9099b415a603450` |

## 2. Negative Acceptance / 反向验收

| ID | Must fail if |
| --- | --- |
| P009-NEG-01 | `/orders/p077-paper-slice` is implemented as a flat top-level route without accepted route hierarchy update |
| P009-NEG-01A | frontend introduces a P077-specific route branch or second rendering component instead of projecting through Account Evidence owner |
| P009-NEG-02 | UI treats E87 filled slice as Paper readiness, broker tradability, admission, production or capital evidence |
| P009-NEG-03 | UI exposes order submit, cancel, replace, retry authorization or broker actions |
| P009-NEG-04 | browser code recomputes fills, positions, lifecycle state or reconcile truth |
| P009-NEG-05 | source refs, checksums, owners or rejection rules are missing from visible evidence |
| P009-NEG-06 | implementation closeout is claimed from proposal docs without browser evidence or typed blocker |
| P009-NEG-07 | E100/E101/E102 read-only fixture refresh is treated as Paper readiness, loop completion, retry authorization or Account Console runtime truth |
| P009-NEG-08 | E105 status normalization is rendered or accepted as runtime truth, UI truth, readiness, retry authorization, action permission or loop completion |

## 2.1 UI Anti-Drift Acceptance / UI 防跑偏验收

```text
UI Anti-Drift Acceptance:
  proposal_or_change_id: p009-p077-paper-slice-evidence-panel
  route_tier: account_drilldown
  primary_workbench: Account Workbench
  route_or_routes_touched:
    - /accounts/{account_id}/orders/{client_order_id}
    - /accounts/{account_id}/evidence
  route_coverage_matrix_rows:
    - /accounts/{account_id}/orders/{client_order_id}: covered-design-gate P004 only; P077 no longer owns a special frontend order-detail branch
    - /accounts/{account_id}/evidence: covered-design-gate P004 plus P009 implementation/browser evidence for the P077 read-only evidence package through Account Evidence owner
  promoted_to_primary_navigation: no
  promotion_reason: P077 panel remains a secondary Account Workbench evidence/order-detail panel
  parent_context_required: Account Workbench context with account id and source refs
  breadcrumbs_required:
    - Account Workbench
    - Orders
    - P077 Paper Slice Evidence
  source_refs_required:
    - lifecycle source_ref
    - lifecycle checksum
    - governance handoff source_ref
    - governance handoff checksum
    - producer_owner
    - projection_owner
    - schema_version
  read_model_contracts:
    - contracts/ui/panels/p077_paper_slice_panel.contract.json
  fixture_states:
    - filled_bounded_slice
    - blocked_missing_ref
    - stale_or_mismatched_checksum
    - no_active_authorization
  browser_evidence_required: yes
  screenshot_viewports:
    - 1440x900
    - 1024x768
    - 390x844
  closeout_ui_open_required: yes
  closeout_ui_open_evidence: recorded for the P077 read-only evidence package only
  forbidden_primary_menu_entries:
    - /orders/p077-paper-slice
  forbidden_actions:
    - order submit/cancel/replace
    - Paper retry authorization
    - broker action
    - runtime mutation
    - account lifecycle mutation
    - admission or capital approval action
  forbidden_claims:
    - Paper readiness
    - Live readiness
    - broker tradability
    - admission approval
    - production readiness
    - capital allocation
    - Account Console runtime truth
  positive_acceptance_ids:
    - UI-OBS-05
    - UI-OBS-06
    - UI-OBS-12
    - UI-ROUTE-02
  negative_acceptance_ids:
    - UI-DRIFT-CLAIM-01
    - UI-DRIFT-CLAIM-02
    - UI-DRIFT-CLAIM-05
    - UI-DRIFT-CLAIM-06
    - UI-DRIFT-ACT-01
    - UI-DRIFT-ACT-02
  blocker_conditions:
    - browser evidence unavailable
    - route mapping not accepted
    - E90 fixture stale or checksum mismatch
    - source refs unavailable
```

## 3. Implementation/browser Evidence / 实现与浏览器证据

Implementation/browser evidence now exists in E93:

- Evidence: `../../acceptance/2026-06-14-p077-p009-ui-implementation-browser-evidence.json`
- Checksum: `sha256:4fc4cedaa0c6f7bb67ab1e6dca1302ffa51ae9838faff61e7a3eca892ee270ed`
- Browser screenshots:
  - `../../acceptance/browser-evidence/p009-p077-paper-slice-evidence-panel/desktop-p077-e90.png`
  - `../../acceptance/browser-evidence/p009-p077-paper-slice-evidence-panel/tablet-p077-e90.png`
  - `../../acceptance/browser-evidence/p009-p077-paper-slice-evidence-panel/mobile-p077-e90.png`

This evidence proves read-only UI rendering only through the Account Evidence owner. It does not create runtime, ledger, admission, capital, broker or readiness truth.

## 3.1 E100/E102 Read-Only Fixture Refresh / 只读 Fixture 刷新

The latest Account Console fixture refresh projects the current P077 bounded close-yesterday slice:

- Evidence: `../../acceptance/2026-06-14-p077-e100-e102-readonly-fixture-refresh.json`
- Checksum: `sha256:4387706e6a740f3267091c009ae556a78bab6ca26e721279bc3290fd8479974c`
- Fixture: `../../contracts/ui/fixtures/p077_paper_slice/e100_close_yesterday_filled_e102_closeout.json`
- Fixture checksum: `sha256:4c751c917bf63811055cda2de52343731a4f6e22360c923945539d79bcc27cb0`

This refresh binds E100 filled/reconciled owner evidence, E101 no-send evidence hygiene audit and E102 P077 no-active-authorization closeout. It is read-only projection evidence only and creates no runtime, ledger, broker, admission, capital, readiness, retry authorization or loop-completion truth.

## 3.2 E105 Status Normalization Read-Only Alignment / 只读状态对齐

The latest Account Console status alignment binds the existing read-only fixture posture to P077 E105:

- Evidence: `../../acceptance/2026-06-14-p077-e105-status-normalization-readonly-alignment.json`
- Checksum: `sha256:b6f913a24613e83386f18d7ef2c41d8183adc43fed30a732a9099b415a603450`
- Source status: P077 T6 `running` / `non_ready_human_review_recommended`
- Fixture behavior: reuse the existing E100/E102 fixture with no frontend, runtime, ledger, Paper or broker mutation.

This alignment is governance/status provenance only. It does not create runtime truth, ledger truth, UI truth, readiness, retry authorization, action controls or loop-completion truth.

## 4. Current Gate Evidence / 当前门禁证据

| Gate | Status | Evidence |
| --- | --- | --- |
| proposal docs | passed | `python scripts/check_proposal_docs.py --root .` -> `PROPOSAL_DOCS_OK: proposals=5` |
| owner boundary | passed | `python scripts/validate_owner_boundaries.py` -> `owner boundary validation passed` |
| frontend fixture validation | passed | `$env:PATH='D:\Nautilus\.tools\node-v22.22.3-win-x64;' + $env:PATH; D:/Nautilus/.tools/node-v22.22.3-win-x64/npm.cmd test` |
| frontend build | passed | `$env:PATH='D:\Nautilus\.tools\node-v22.22.3-win-x64;' + $env:PATH; D:/Nautilus/.tools/node-v22.22.3-win-x64/npm.cmd run build` |
| browser evidence | passed | `$env:PATH='D:\Nautilus\.tools\node-v22.22.3-win-x64;' + $env:PATH; D:/Nautilus/.tools/node-v22.22.3-win-x64/npm.cmd run test:e2e` -> 6 passed |
| E100/E102 fixture refresh | passed | `python -m json.tool contracts/ui/fixtures/p077_paper_slice/e100_close_yesterday_filled_e102_closeout.json`; `python scripts/validate_owner_boundaries.py`; `npm test`; `npm run build`; `npm run test:e2e` -> 6 passed; `python scripts/check_proposal_docs.py --root .`; `python -m compileall backend/src`; `cargo test --manifest-path hotpath-rs/Cargo.toml` |
| E105 status alignment | passed | `python -m json.tool docs/acceptance/2026-06-14-p077-e105-status-normalization-readonly-alignment.json`; Account Console lightweight gates recorded in the heartbeat closeout |
