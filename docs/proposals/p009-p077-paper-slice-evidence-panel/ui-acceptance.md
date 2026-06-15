# P009 UI Acceptance: P077 Paper Slice Evidence Panel

- Proposal ID: `p009-p077-paper-slice-evidence-panel`
- Status: readonly_fixture_refresh
- Updated: 2026-06-14
- UI design: [P009 UI Design](./ui-design.md)
- Parent acceptance: [Account Console UI implementation acceptance](../../acceptance/2026-06-13-account-console-ui-implementation-acceptance.md)
- Anti-drift acceptance: [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)

## 1. Required UI Evidence / 必需 UI 证据

| Evidence | Required artifact |
| --- | --- |
| Read model contract | `contracts/ui/panels/p077_paper_slice_panel.contract.json` |
| Filled bounded slice fixture | `contracts/ui/fixtures/p077_paper_slice/e100_close_yesterday_filled_e102_closeout.json` |
| Route hierarchy proof | Account Workbench parent route mapping, not top-level `/orders/p077-paper-slice` |
| Desktop screenshot | Account Workbench panel with current P077 fixture after implementation |
| Tablet screenshot | Account Workbench panel with current P077 fixture after implementation |
| Mobile screenshot | Account Workbench panel with current P077 fixture after implementation |
| DOM/test evidence | stable `data-testid` hooks for context, summary, refs, boundaries and blockers |
| Forbidden wording scan | source scan and browser text scan |
| Fixture replay evidence | repeated fixture render produces the same slice state and boundary flags |

## 2. Positive UI Acceptance / 正向 UI 验收

| ID | Must pass | Evidence |
| --- | --- | --- |
| P009-UI-POS-01 | panel opens under Account Workbench context with account id and breadcrumbs | desktop screenshot |
| P009-UI-POS-02 | slice summary displays instrument, side, offset, quantity, lifecycle state and reconcile state from fixture | fixture-backed test |
| P009-UI-POS-03 | evidence refs display source ref, checksum, owner, schema and authority | DOM test |
| P009-UI-POS-04 | boundary list displays all false readiness/truth flags without upgrading them to pass claims | DOM test |
| P009-UI-POS-05 | rejection rules are visible and tied to the fixture/contract | fixture-backed test |
| P009-UI-POS-06 | blocked or stale source refs render as blockers with owner and next action | blocked fixture or typed blocker |
| P009-UI-POS-07 | desktop, tablet and mobile layouts have no overlap, clipped refs or hidden boundary rows | screenshot review |

## 3. Negative UI Acceptance / 反向 UI 验收

| ID | Must fail if |
| --- | --- |
| P009-UI-NEG-01 | package renders without Account Workbench parent context |
| P009-UI-NEG-02 | `/orders/p077-paper-slice` is implemented as a top-level primary route |
| P009-UI-NEG-02A | frontend adds a P077-specific route branch or second rendering component outside Account Evidence |
| P009-UI-NEG-03 | UI treats the filled slice as Paper readiness, Live readiness, broker tradability, admission, production or capital evidence |
| P009-UI-NEG-04 | UI exposes order submit, cancel, replace, retry authorization or broker action controls |
| P009-UI-NEG-05 | UI computes lifecycle, fill, position or reconcile truth in the browser |
| P009-UI-NEG-06 | displayed values lack source refs, checksums, owners or rejection rules |
| P009-UI-NEG-07 | raw report/debug/latest/stdout content becomes first-screen truth |

## 4. Data Test ID Acceptance / 测试钩子验收

Minimum required selectors:

```text
[data-testid="account-evidence-panel"]
[data-testid="account-evidence-context-bar"]
[data-testid="account-evidence-table"]
[data-testid="account-evidence-package-row"]
[data-testid="account-evidence-boundary-list"]
[data-testid="account-evidence-source-ref"]
[data-testid="account-evidence-rejection-rule"]
[data-testid="account-evidence-blocker"]
[data-testid="account-evidence-detail-drawer"]
```

## 5. Browser Acceptance / 浏览器验收

Required viewport checks after implementation:

| Viewport | Width x height | Required proof |
| --- | --- | --- |
| Desktop | 1440 x 900 | context, summary, evidence refs and boundary list |
| Tablet | 1024 x 768 | tabs/drawer usable, refs visible |
| Mobile | 390 x 844 | stacked summary, readable refs, full-screen drawer |

Must pass:

1. No horizontal overflow from account id, source refs or checksums.
2. Boundary rows remain visible without implying readiness.
3. Evidence drawer does not hide account context on desktop.
4. Mobile sheet has a visible close affordance.
5. Browser evidence is captured after the final implementation change.

## 6. Required Validation Commands / 必跑验证

Minimum repo checks:

```powershell
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|broker tradable|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates
```

Frontend checks when implementation starts and dependencies are available:

```powershell
cd frontend
npm run build
npm run test
npm run test:e2e
```

## 7. Blocker Recording / 阻塞记录

If UI acceptance cannot be completed, the implementation change must record:

```text
UI Acceptance Blocker:
  missing_tool:
  missing_contract:
  missing_fixture:
  missing_route_mapping:
  missing_viewport_evidence:
  unavailable_browser_runner:
  violated_boundary:
  next_owner:
```
