# P001 UI Acceptance: Daily Closeout Account Health Panel

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Status: browser_evidence_verified
- Updated: 2026-06-13
- UI design: [P001 UI Design](./ui-design.md)
- Parent acceptance: [Account Console capability UI acceptance](../../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
- Anti-drift acceptance: [Account Console UI anti-drift acceptance](../../acceptance/2026-06-13-account-console-ui-anti-drift-acceptance.md)

## 1. Required UI Evidence / 必需 UI 证据

| Evidence | Required artifact |
| --- | --- |
| Desktop screenshot | `/closeout` with happy-path fixture |
| Mobile screenshot | `/closeout` with happy-path fixture |
| Blocked screenshot | `/closeout` with blocked settlement fixture |
| Stale screenshot | `/closeout` with stale stream fixture |
| Partial screenshot | `/closeout` with partial evidence fixture |
| Empty screenshot | `/closeout` with empty fixture |
| DOM/test evidence | stable `data-testid` hooks for panel, filters, table, drawers and state rows |
| Forbidden wording scan | source scan and browser text scan |
| Fixture replay evidence | repeated fixture render produces same visible counts and row states |
| Anti-drift evidence | completed anti-drift checklist in [P001 acceptance](./acceptance.md) |

## 2. Positive UI Acceptance / 正向 UI 验收

| ID | Must pass | Evidence |
| --- | --- | --- |
| P001-UI-POS-01 | `/closeout` first viewport shows Account Health Panel before raw artifact menus | desktop screenshot |
| P001-UI-POS-02 | header shows trading day, session id, closeout run id and reducer checkpoint id | DOM test or screenshot |
| P001-UI-POS-03 | metric strip shows total accounts, closeout blocked, settlement blocked and stale/partial counts | fixture-backed test |
| P001-UI-POS-04 | account rows show account id, type, owner, closeout state, settlement state, equity continuity, blocker count and source ref | fixture-backed test |
| P001-UI-POS-05 | selecting an account opens read-only detail drawer with blockers and evidence refs | interaction test |
| P001-UI-POS-06 | opening an evidence ref shows artifact id, schema version, checksum and run/session/trading-day refs | interaction test |
| P001-UI-POS-07 | happy, empty, blocked, stale and partial states render distinct visual states | state screenshots |
| P001-UI-POS-08 | desktop and mobile layouts have no overlapping labels, clipped state badges or hidden blocker text | screenshot review |

## 3. Negative UI Acceptance / 反向 UI 验收

| ID | Must fail if |
| --- | --- |
| P001-UI-NEG-01 | Account Health Panel appears without a declared read model contract and fixture state |
| P001-UI-NEG-02 | raw artifact menus or raw report payloads are the first visible workflow |
| P001-UI-NEG-03 | blocked, stale or partial states collapse into a generic healthy or empty state |
| P001-UI-NEG-04 | visible UI uses forbidden readiness, admission, capital or tradability wording |
| P001-UI-NEG-05 | UI exposes broker action, order submit/cancel/replace, direct funding mutation or direct account lifecycle mutation |
| P001-UI-NEG-06 | a displayed value has no source ref, checksum, run/session/trading-day ref or typed blocker |
| P001-UI-NEG-07 | visual layout uses nested cards, decorative hero layout or marketing copy as the main screen |
| P001-UI-NEG-08 | `/closeout` appears as one item in a flat 26-route primary menu instead of the Daily Closeout workbench entry |

## 4. Data Test ID Acceptance / 测试钩子验收

All required hooks from [P001 UI Design](./ui-design.md) must exist.

Minimum required selectors:

```text
[data-testid="daily-closeout-account-health-panel"]
[data-testid="daily-closeout-filter-toolbar"]
[data-testid="daily-closeout-metric-strip"]
[data-testid="daily-closeout-account-health-row"]
[data-testid="daily-closeout-closeout-state"]
[data-testid="daily-closeout-settlement-state"]
[data-testid="daily-closeout-equity-continuity"]
[data-testid="daily-closeout-blocker"]
[data-testid="daily-closeout-evidence-ref"]
[data-testid="daily-closeout-detail-drawer"]
[data-testid="daily-closeout-evidence-drawer"]
```

## 5. Browser Acceptance / 浏览器验收

Required viewport checks:

| Viewport | Width x height | Required proof |
| --- | --- | --- |
| Desktop | 1440 x 900 | full panel, metrics, table and drawer |
| Tablet | 1024 x 768 | no overlap, filters usable |
| Mobile | 390 x 844 | stacked rows, full-screen drawer, no clipped state text |

Must pass:

1. No horizontal overflow caused by state labels, account ids or checksum refs.
2. Drawer does not cover table headers in desktop layout.
3. Mobile full-screen sheet has a visible close affordance.
4. Metric strip values do not resize the page when fixture changes.

## 6. Required Validation Commands / 必跑验证

Minimum repo checks:

```powershell
python -m compileall backend\src
python scripts\validate_owner_boundaries.py
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates
```

Frontend checks when dependencies are available:

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
  missing_anti_drift_checklist:
  missing_viewport_evidence:
  unavailable_browser_runner:
  violated_boundary:
  next_owner:
```

Current runner evidence:

- [P001 browser runner blocker resolved by portable Node](../../acceptance/browser-evidence/p001-daily-closeout-account-health-panel/2026-06-13-browser-runner-blocker.md)
