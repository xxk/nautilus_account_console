# P001 Acceptance / 验收

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Status: browser_evidence_verified
- Updated: 2026-06-13
- Inherits:
  - [Account Console capability UI acceptance](../../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
  - [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)
  - [Account Console UI route coverage matrix](../../acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md)
  - [Account Console owner map](../../ownership/account-console-owner-map.md)
  - [Contract-first UI slice development topic](../../topics/contract-first-ui-slice-development.md)
  - [P001 UI Acceptance](./ui-acceptance.md)

## 1. Positive Acceptance / 正向验收

| ID | Acceptance | Evidence |
| --- | --- | --- |
| P001-POS-01 | `/closeout` shows an Account Health Panel backed by a declared read model contract | contract path and UI screenshot |
| P001-POS-02 | panel shows account/session identity, closeout state, settlement state, equity continuity and evidence references | fixture-backed UI test |
| P001-POS-03 | happy, empty, blocked and stale states render distinct operator-visible states | fixture-backed UI tests |
| P001-POS-04 | blockers and next diagnostic drill-downs are visible without claiming readiness or tradability | screenshot and forbidden wording scan |
| P001-POS-05 | panel maps to UI-WB-01 and UI-VIS-01 | acceptance evidence update |
| P001-POS-06 | panel-level UI design and UI acceptance are present before implementation | `ui-design.md` and `ui-acceptance.md` |
| P001-POS-07 | anti-drift route tier is declared as `primary_workbench` for `/closeout` | completed anti-drift checklist |
| P001-POS-08 | `/closeout` route coverage matrix row is marked `covered-proposal: P001` | route coverage matrix |
| P001-POS-09 | ADR-0044 P078 closeout-backed fixture maps A3 settlement/equity evidence into the panel read model without becoming runtime/UI truth | `contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json` |
| P001-POS-10 | P001 declares producer, verifier, projection, UI and approval owners before implementation | Owner Boundary block and owner map |

## 2. Negative Acceptance / 反向验收

| ID | Must fail if |
| --- | --- |
| P001-NEG-01 | the panel is implemented without `contracts/ui/panels/account_health_panel.contract.json` |
| P001-NEG-02 | the UI consumes fields not present in the contract or fixtures |
| P001-NEG-03 | the UI displays forbidden readiness, admission, capital or tradability claims |
| P001-NEG-04 | the UI exposes direct account creation, funding mutation, broker action or order submit/cancel/replace controls |
| P001-NEG-05 | raw reports become the first-screen workflow instead of evidence drill-down |
| P001-NEG-06 | blocked or stale states are hidden behind a generic success or empty state |
| P001-NEG-07 | `/closeout` is implemented as a raw artifact menu rather than the Daily Closeout primary workbench |
| P001-NEG-08 | P001 creates a second closeout/account/settlement truth writer instead of a fixture-backed UI projection |
| P001-NEG-09 | P001 proceeds when the source artifact owner is missing instead of recording a typed blocker |

## 2.1 UI Anti-Drift Acceptance / UI 防跑偏验收

```text
UI Anti-Drift Acceptance:
  proposal_or_change_id: p001-daily-closeout-account-health-panel
  route_tier: primary_workbench
  primary_workbench: Daily Closeout
  route_or_routes_touched:
    - /closeout
  route_coverage_matrix_rows:
    - /closeout: covered-proposal P001
  promoted_to_primary_navigation: no
  promotion_reason: already a primary workbench route
  parent_context_required: Daily Closeout workbench context
  breadcrumbs_required:
    - Daily Closeout
    - Account Health
  source_refs_required:
    - account_id
    - session_id
    - closeout_run_id
    - settlement_run_id
    - equity_curve_artifact_id
    - reducer_checkpoint_id
  read_model_contracts:
    - contracts/ui/panels/account_health_panel.contract.json
  fixture_states:
    - happy_path
    - empty
    - blocked
    - stale
    - partial
  source_backed_fixtures:
    - account_health_adr0044_foundation_closeout.json
  browser_evidence_required: yes
  screenshot_viewports:
    - 1440x900
    - 1024x768
    - 390x844
  forbidden_primary_menu_entries:
    - all 26 route-map entries as peer primary pages
  forbidden_actions:
    - broker action
    - runtime mutation
    - order submit/cancel/replace
    - direct account lifecycle mutation
    - direct funding/allocation mutation
  forbidden_claims:
    - Paper readiness
    - Live readiness
    - admission approval
    - PM approval
    - real capital allocation
    - account tradability
  positive_acceptance_ids:
    - UI-DRIFT-NAV-01
    - UI-DRIFT-NAV-03
    - UI-DRIFT-EVD-01
    - UI-DRIFT-EVD-03
    - ASI-01
    - ASI-04
  negative_acceptance_ids:
    - UI-DRIFT-CLAIM-01
    - UI-DRIFT-CLAIM-02
    - UI-DRIFT-ACT-01
    - UI-DRIFT-ACT-02
    - UI-DRIFT-ACT-03
    - ASI-02
    - ASI-05
  blocker_conditions:
    - browser evidence unavailable
    - source refs unavailable
    - fixture state unavailable
```

## 3. Replay And Conservation Acceptance / 回放与守恒验收

| ID | Acceptance |
| --- | --- |
| P001-REP-01 | the same fixture renders the same panel state across repeated frontend test runs |
| P001-REP-02 | closeout, settlement and equity continuity values are displayed as read-model projections, not recomputed UI truth |
| P001-CONS-01 | account count, closeout status count and blocked status count in the panel match fixture totals |
| P001-CONS-02 | equity continuity indicators reference an artifact ID or checkpoint ID; missing references render as blocked or incomplete |

## 4. Performance Acceptance / 性能验收

| ID | Acceptance |
| --- | --- |
| P001-PERF-01 | fixture rendering does not create unbounded DOM growth for account rows |
| P001-PERF-02 | filtering by account type and closeout state remains deterministic on the fixture dataset |

## 5. Required Validation Commands / 必跑验证

```powershell
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates
```

Frontend validation, when Node/npm is available:

```powershell
cd frontend
npm install
npm run build
npm run test
npm run test:e2e
```

## 6. Blocker Conditions / 阻塞条件

1. No frontend package manager is available for build/test.
2. Read model fields needed by the panel cannot be sourced from current contracts or fixtures.
3. Visual screenshot tooling is unavailable.
4. A requested interaction would mutate runtime/account/broker/admission/capital truth.

Current runner evidence:

- [P001 browser runner blocker resolved by portable Node](../../acceptance/browser-evidence/p001-daily-closeout-account-health-panel/2026-06-13-browser-runner-blocker.md)

## 7. Closeout Evidence / 收口证据

| Check | Result |
| --- | --- |
| `python -m compileall backend\src` | pass |
| `python scripts\validate_owner_boundaries.py` | pass |
| `cargo test --manifest-path hotpath-rs\Cargo.toml` | pass |
| `npm run build` | pass |
| `npm run test` | pass |
| `npm run test:e2e` | pass: desktop/tablet/mobile |
| forbidden wording/action scan | pass: no matches in `frontend\src backend\src hotpath-rs\crates contracts\ui` |
| browser screenshots | `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/` |

Security follow-up:

- Closed by [P003 Frontend Dependency Security Follow-up](../p003-frontend-dependency-security-followup/README.md). This does not change P001's read-only boundary and does not create runtime truth.
