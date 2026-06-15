# Account Workbench Terminal UI Design / 账户工作台终端式 UI 设计

- Date: 2026-06-15
- Status: design draft
- Reference style: selective Kuaiqi 2 density/workbench reference, not a full terminal clone
- Scope: Account Workbench UI design for Account Capability Fabric observation-only P0
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Architecture anchor: [Account Capability Fabric architecture design](./account-capability-fabric-architecture-design.md)
- Topic anchor: [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
- Roadmap anchor: [T001 Account Capability Feature Roadmap](../topics/roadmap/T001-account-capability-feature-roadmap.md)

## 1. Design Intent / 设计意图

Use Kuaiqi 2 selectively as an interaction-density and multi-panel workbench reference, not as a product blueprint and not as a trading-authority reference.

The Account Workbench should feel like an operational terminal:

1. high information density;
2. persistent account context;
3. multi-panel grid;
4. tables as primary surfaces;
5. fast scanning of funds, positions, orders, fills, source health and blockers;
6. keyboard-friendly selection and copy refs;
7. no marketing layout, no oversized hero, no decorative cards.

But P0 remains observation-only:

```text
No submit.
No cancel.
No replace.
No direct broker action.
No Paper ready / Live ready / can trade wording.
```

## 1.1 Selective Reference Boundary / 选择性参考边界

Reference from Kuaiqi 2:

1. dense first-screen information layout;
2. persistent account/status bar;
3. table-first positions/orders/fills surfaces;
4. split panes for list, detail and evidence;
5. quick row selection and keyboard-friendly scanning;
6. compact numeric formatting.

Reference must be applied through T001 feature tracks in this order:

```text
F2 Observation contracts
  -> F4 Source adapters/bridges
  -> F3 Mirror projection store
  -> F5 Account Workbench API mode
```

This means the UI shape may borrow density and panel organization only after the projected data path is explicit:

| Track | UI design implication |
| --- | --- |
| F2 Observation contracts | every visible value has a declared observation/projection field before layout work |
| F4 Source adapters/bridges | source-specific details enter as refs, blockers and source health, not UI-specific parsing |
| F3 Mirror projection store | tables render mirror projections, not direct broker/native payloads |
| F5 Account Workbench API mode | terminal-style panels bind to read-only API projections and retain fixture mode |

Do not reference from Kuaiqi 2:

1. order ticket as a central workflow;
2. buy/sell/cancel/replace controls;
3. broker session control as a UI primitive;
4. trading-hotkey mental model;
5. full-market terminal complexity;
6. visual clutter that hides evidence, blockers or provenance;
7. any wording that implies tradability or readiness.

Account Console should feel operational and dense, but its first responsibility is explainability: every value should answer "where did this come from, how fresh is it, and what blocks trust?"

## 2. First View Layout / 首屏布局

Target first viewport:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Top Status Bar: account, source mode, trading day, mirror state, lag, refs   │
├───────────────┬───────────────────────────────────────────┬──────────────────┤
│ Account List  │ Account Summary / Balance Strip           │ Source Health    │
│ + Capabilities│ + Position Exposure Strip                 │ + Blockers       │
├───────────────┼───────────────────────────────────────────┼──────────────────┤
│ Instruments / │ Positions Table                           │ Evidence Drawer  │
│ Filters       │                                           │ / Details        │
├───────────────┼───────────────────────────────────────────┼──────────────────┤
│ Orders / Fills / Events Tabs                              │ Selected Row Refs│
└───────────────┴───────────────────────────────────────────┴──────────────────┘
```

Default desktop grid:

| Region | Width / Height | Purpose |
| --- | --- | --- |
| Top status bar | full width, 36-44 px | account identity, environment, source state, observed time |
| Left rail | 220-280 px | account selector, capability badges, filters |
| Center top | flexible, 100-140 px | compact funds, margin, PnL, position totals |
| Center main | flexible, 45-55% height | positions table |
| Bottom tape | full center width, 28-34% height | orders, fills, events tabs |
| Right rail | 300-380 px | source health, blockers, evidence refs, selected details |

## 3. Visual Language / 视觉语言

Use a quiet terminal palette:

| Token | Use |
| --- | --- |
| off-white / pale gray background | table areas and main workspace |
| charcoal headers | top status bar and table headers |
| red / green numeric deltas | PnL, long/short, up/down only |
| amber | stale, partial, warning |
| blue-gray | refs, checksums, source metadata |
| red outline/fill | blockers and failed gates |

Avoid:

1. large rounded cards;
2. hero sections;
3. one-note blue/purple gradients;
4. decorative icons as layout filler;
5. oversized headings inside dense panels.

## 4. Top Status Bar / 顶部状态条

Always visible:

```text
Account: acct.ctp.paper.19053
Alias: 19053
Source: ctp_trader_api / paper
Mirror: current | stale | blocked
Observed: 2026-06-15 14:59:03
Lag: 1.2s
Command: disabled
Evidence: 8 refs
```

Required interactions:

1. account dropdown;
2. copy account id;
3. copy latest source ref;
4. open capability detail;
5. open source health detail.

Must fail if:

1. top bar uses bare `19053` as canonical identity;
2. command capability is visually implied as enabled when disabled;
3. stale source appears as healthy.

## 5. Left Rail / 左侧账户与过滤栏

Left rail modules:

```text
Account selector
Capability table
Instrument filter
Position direction filter
Source mode filter
Staleness filter
```

Account selector rows:

| Field | Example |
| --- | --- |
| alias | `19053` |
| canonical id | `acct.ctp.paper.19053` |
| source kind | `ctp_trader_api` |
| mirror state | `current` |
| command mode | `disabled` |

Capability table:

```text
Track | Name        | Source          | State    | Ref
F2    | Observation | mirror stream   | current  | checkpoint
F4    | Source      | CTP paper 19053 | fixture  | source ref
F3    | Mirror      | projection      | read     | read model
F5    | Workbench   | account UI      | read-only| orders locked
```

Switching account context must reload account-scoped projections. If the target account lacks positions, orders or evidence projections, the UI must render empty or blocked projection states, not retain the prior account's rows.

## 6. Center Summary Strip / 中部摘要条

Compact metrics, not cards:

| Metric | Source |
| --- | --- |
| Equity | balance projection |
| Available cash | balance projection |
| Frozen cash | balance projection |
| Margin used | balance projection |
| Realized PnL | balance projection |
| Unrealized PnL | positions projection |
| Position count | positions projection |
| Open order count | orders projection |

Every metric must expose source/evidence on selection or hover. Values without provenance render as blocked or unavailable, not blank success.

## 7. Positions Table / 持仓表

Primary table columns:

```text
Instrument
Direction
Net
Today
Yesterday
Available
Frozen
Average Px
Market Px
Market Value
Unrealized PnL
Source
State
```

Row behavior:

1. click row updates right detail rail;
2. double click opens `/accounts/{account_id}/positions?instrument=...`;
3. keyboard arrows move selection;
4. copy source ref from row action;
5. stale row uses amber state, not hidden text.

Must fail if:

1. table computes available quantity in browser from raw broker fields;
2. missing carryover/settlement source renders as healthy;
3. source refs/checksums are omitted.

## 8. Bottom Tape / 底部事件带

Tabs:

```text
Orders
Fills
Events
Settlement
Reconcile
```

P0 may show disabled/unavailable states for tabs whose projections do not exist yet, but must explain blocker/source state.

Orders columns:

```text
Time
Instrument
Side
Qty
Filled
Status
Client Order ID
Venue Order ID
Source
State
```

Events columns:

```text
Seq
Observed At
Event Type
Account ID
Instrument
Ref
Checksum
```

This bottom tape is readback only. It must not include order entry controls.

## 9. Right Rail / 右侧证据与详情栏

Right rail sections:

```text
Selected row detail
Source health
Typed blockers
Evidence refs
Capability detail
```

Evidence rows:

| Field | Required |
| --- | --- |
| kind | yes |
| owner | yes |
| source_ref | yes |
| checksum | yes when available |
| observed_at | yes |
| authority note | yes |

Typed blockers should be readable and operational:

```text
source_stale
schema_mismatch
capability_missing
command_authority_missing
readback_reconciliation_mismatch
```

## 10. Command Capability Presentation / Command 能力展示

P0 display:

```text
Command capability: disabled
Allowed actions: none
Reason: no command capability proposal accepted
```

Do not show disabled trading buttons in P0. A disabled submit button still trains users to expect action. Use capability text/badge only.

Future command-capable UI must be designed in a separate proposal after `ADR0004-G06-PAPER-COMMAND` or `ADR0004-G07-LIVE-COMMAND` has evidence.

## 11. Responsive Behavior / 响应式行为

Desktop:

1. left rail, center tables and right rail all visible;
2. bottom tape visible in same viewport;
3. no nested cards.

Tablet:

1. left rail collapses to account/filter drawer;
2. right rail becomes side drawer;
3. positions table remains primary.

Mobile:

1. top status bar remains sticky;
2. account selector becomes segmented drawer;
3. summary strip becomes two-column metrics;
4. positions table becomes horizontally scrollable grid;
5. evidence detail opens as bottom sheet.

## 12. P0 Screen States / P0 状态

Required states:

| State | UI requirement |
| --- | --- |
| current | summary, positions and capabilities render from API projection |
| stale | values remain visible only with stale badge and observed time |
| source missing | no healthy values; blocker in center and right rail |
| capability missing | account detail blocked until capability projection exists |
| command disabled | no command controls, capability badge says disabled |
| empty positions | only valid when source explicitly observes zero positions |

## 13. Data-Test IDs / 测试钩子

Required selectors:

```text
terminal-workbench-shell
terminal-top-status-bar
account-selector
account-capability-table
account-capability-row
account-summary-metric-strip
account-positions-table
account-bottom-tape
account-source-health-panel
account-evidence-rail
account-blocker-row
account-command-capability-state
```

## 14. Implementation Slices / 实现切片

UI implementation should be split:

| Slice | Scope |
| --- | --- |
| UI-S1 shell | terminal grid, top status, rails, empty projections |
| UI-S2 summary | API-backed account summary strip |
| UI-S3 positions | positions table and row detail |
| UI-S4 capabilities | capability badges and disabled command state |
| UI-S5 evidence | source refs, checksums, blockers |
| UI-S6 bottom tape | orders/fills/events readback tabs |

P0 should target UI-S1 to UI-S5 only.

## 15. Negative Acceptance / 反向验收

Reject the UI design or implementation if:

1. it looks like a marketing dashboard instead of an operational terminal;
2. it hides source refs in a secondary route only;
3. it treats `19053` as canonical identity;
4. it calls CTP/IB/broker APIs directly from UI or Account Console API;
5. it renders values without source refs/checksums or typed blockers;
6. it shows submit/cancel/replace buttons in P0;
7. it labels command capability as ready/tradable;
8. it turns every route into a top-level navigation item;
9. it relies on color alone for stale/blocker state;
10. it keeps prior account positions/orders visible after account selector changes context;
11. it drops fixture mode while adding API mode.
