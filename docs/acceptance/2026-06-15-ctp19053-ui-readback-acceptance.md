# CTP 19053 UI Readback Acceptance / CTP 19053 UI 回读一致性验收

- Date: 2026-06-15
- Status: implementation browser evidence available
- Scope: UI readback acceptance for CTP Paper account `acct.ctp.paper.19053`
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Topic anchor: [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
- Architecture design: [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)
- UI design: [Account Workbench terminal UI design](../design/account-workbench-terminal-ui-design.md)
- Real source package template: `contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json`

## 1. Acceptance Boundary / 验收边界

This acceptance verifies that Account Console UI renders the same account readback values as the trusted CTP 19053 observation artifact or read model for the same snapshot.

It does not make UI a broker truth source. It does not certify Paper readiness, Live readiness, tradability, admission, approval or capital allocation.

Correct wording:

```text
UI matches the trusted CTP 19053 observation snapshot.
```

Incorrect wording:

```text
UI proves the real broker account truth.
```

## 2. ADR-0004 Layer Coverage / ADR-0004 分层覆盖

This acceptance is the concrete `L3-UI-READBACK` proof for CTP Paper `19053`. It may also provide evidence for `L2-MIRROR`, `L4-COMMAND-BOUNDARY` and `L5-CLOSEOUT` when the required artifacts exist.

| ADR-0004 layer | CTP 19053 evidence here | Pass condition |
| --- | --- | --- |
| `L1-CONTRACT` | source/projection payload follows accepted identity, balance, position, order, execution report and capability contracts | schemas or typed fixtures exist and match payload shape |
| `L2-MIRROR` | pinned source package and Account Mirror projection are both captured with checksums | projection is derived from canonical observation, not direct UI/broker call |
| `L3-UI-READBACK` | browser selectors compare UI funds, positions, orders and execution reports against pinned projection | UI values match projection within declared tolerance |
| `L4-COMMAND-BOUNDARY` | command capability state is visible as disabled for P0 | submit/cancel/replace controls are absent |
| `L5-CLOSEOUT` | acceptance record captures commands, artifacts, screenshots, checksums, blockers and verdict | evidence is durable enough to rerun or audit |

Covered ADR-0004 Gates:

```text
ADR0004-G01-IDENTITY
ADR0004-G02-PROVENANCE
ADR0004-G03-CAPABILITY-REGISTRY
ADR0004-G05-COMMAND-DISABLED-DEFAULT
ADR0004-G08-OWNER-SEPARATION
ADR0004-G10-FAIL-CLOSED-BLOCKERS
```

When order/execution-report projections exist, this acceptance also covers the UI-readback part of `ADR0004-G09-READBACK-RECONCILIATION`; it does not accept command execution.

## 3. Trusted Source Requirement / 受信来源要求

Every UI readback acceptance run must pin a source package:

```text
account_id: acct.ctp.paper.19053
display_alias: 19053
source_owner: nautilus_ctp_adapter
source_kind: ctp_trader_api
source_mode: paper
source_ref: <pinned artifact or read-model URI>
source_checksum: <sha256>
observed_at: <source observation timestamp>
projection_ref: <Account Mirror projection artifact/API response>
projection_checksum: <sha256>
```

The UI may be compared only against that pinned source/projection pair. Latest/debug paths are not enough unless they resolve to an immutable source ref and checksum.

## 4. Required UI Routes / 必需 UI 路由

Minimum routes:

```text
/accounts/acct.ctp.paper.19053
/accounts/acct.ctp.paper.19053/positions
/accounts/acct.ctp.paper.19053/orders
/accounts/acct.ctp.paper.19053/orders/{client_order_id}
/accounts/acct.ctp.paper.19053/evidence
```

Optional when projections exist:

```text
/accounts/acct.ctp.paper.19053/fills
/accounts/acct.ctp.paper.19053/settlement
/accounts/acct.ctp.paper.19053/equity
/accounts/acct.ctp.paper.19053/reconcile
/accounts/acct.ctp.paper.19053/incidents
```

## 5. Required Comparison Matrix / 必需对账矩阵

| Domain | UI selector | Source/projection fields | Tolerance | Must fail if |
| --- | --- | --- | --- | --- |
| Identity | account header/status bar | `account_id`, `display_alias`, `source_kind`, `source_mode` | exact | UI uses bare `19053` as canonical id |
| Capability | capability badges | observation, command, reconciliation, evidence capability fields | exact | command controls appear without accepted command capability |
| Funds | summary strip / balance panel | equity, available cash, frozen cash, margin used, realized/unrealized PnL, fees | numeric exact or declared decimal tolerance | UI value differs or lacks source ref/checksum |
| Positions | positions table | instrument, direction, net/today/yesterday/available/frozen qty, avg price, market price, market value, unrealized PnL | qty exact; prices/PnL declared decimal tolerance | row missing, extra, stale or mismatched |
| Orders | orders table / bottom tape | client order id, venue order id, instrument, side, qty, filled qty, status, event seq/ref | exact | UI invents order state or omits source ref |
| Execution reports | order detail drawer / evidence drawer | report msg type, report status, client order id, venue order id, report seq/ref, normalized event link, checksum | exact for ids/status/refs/checksum | execution report is not visible, not linked, or replaces normalized order truth |
| Fills | fills tab | trade id, order id, instrument, qty, price, fee, timestamp | exact for ids/qty; price tolerance | fill appears without order/account lineage |
| Source health | source health panel | observed_at, received_at, lag, stale/blocker state | exact state; lag within run tolerance | stale source shown as healthy |
| Evidence | evidence rail/drawer | source_ref, checksum, schema_version, owner | exact | UI values cannot be traced to evidence |
| Blockers | blocker rows | blocker_id, type, owner, next_action | exact | missing source is hidden as empty success |
| Account switching | account selector table | selected `account_id`, display alias, stream state, account-scoped projections | exact | switching account keeps prior account positions/orders visible |

## 6. Snapshot Consistency Rule / 快照一致性规则

Funds, positions and orders must be compared from the same accepted observation snapshot or a declared projection checkpoint:

```text
projection_checkpoint_id
projection_checkpoint_ts
source_observed_at
source_ref
source_checksum
```

If source values change during UI verification, the run must either:

1. pin a new checkpoint and rerun the comparison; or
2. record `source_changed_during_acceptance` as a typed blocker.

## 7. UI Evidence Requirement / UI 证据要求

Each accepted run must produce:

1. API response capture for source/projection values;
2. browser evidence for desktop route rendering;
3. at least one positions table screenshot or Playwright selector evidence;
4. at least one funds/summary selector evidence;
5. at least one orders selector evidence when order projection exists;
6. at least one execution report detail/evidence selector when execution reports exist;
7. evidence drawer/source ref selector evidence;
8. command-disabled selector evidence for P0.

Recommended selectors:

```text
terminal-top-status-bar
account-command-capability-state
account-selector
account-capability-table
account-capability-row
account-summary-metric-strip
account-positions-table
account-bottom-tape
account-order-execution-report
account-order-report-ref
account-source-health-panel
account-evidence-rail
account-blocker-row
```

## 8. Positive Acceptance / 正向验收

The CTP 19053 UI readback passes when:

1. UI opens `/accounts/acct.ctp.paper.19053`.
2. Canonical account id is displayed or copyable as `acct.ctp.paper.19053`.
3. Display alias is `19053`.
4. Funds in UI match the pinned projection/source package.
5. Positions in UI match the pinned projection/source package.
6. Orders in UI match the pinned projection/source package when orders exist.
7. Execution reports are visible from the order row/detail path when report refs exist.
8. Execution reports show source refs/checksums and link to the normalized order event or evidence package.
9. Every displayed value has visible or drill-down source refs/checksums.
10. Source health shows current/stale/blocked state consistently with the source package.
11. P0 command capability is disabled and no command controls render.
12. Account selector can switch observation context without carrying over another account's positions or orders.
13. Fixture mode remains available for deterministic UI tests.

## 9. Negative Acceptance / 反向验收

The CTP 19053 UI readback must fail if:

1. UI calls CTP Trader API directly.
2. Backend Account Console API calls CTP Trader API directly instead of reading canonical observations/projections.
3. UI uses `19053` as canonical account id.
4. Funds differ from the pinned projection beyond declared tolerance.
5. A position row is missing, extra or mismatched.
6. An order row is missing, extra or has invented status.
7. Execution report refs exist in source/projection but are not visible in UI.
8. Raw execution report text is treated as account/order truth instead of provenance linked to normalized events.
9. Source refs/checksums are absent for live-looking values.
10. Stale or missing source renders as healthy/empty success.
11. Submit, cancel or replace controls appear before command capability acceptance.
12. Account switching preserves prior selected account rows, funds or orders when the target account lacks those projections.
13. Screenshot-only evidence is used without API/source comparison.

## 10. Typed Blockers / 类型化阻塞

Allowed blocker outcomes:

```text
ctp19053_source_unavailable
ctp19053_source_changed_during_acceptance
ctp19053_projection_missing
ctp19053_projection_schema_mismatch
ctp19053_ui_value_mismatch
ctp19053_ui_evidence_missing
ctp19053_execution_report_missing
ctp19053_execution_report_unlinked
ctp19053_browser_tooling_unavailable
ctp19053_command_capability_unaccepted
```

Blockers must include owner, source ref if available, attempted command, timestamp and next action.

## 11. Acceptance Record Template / 验收记录模板

```text
CTP19053 UI Readback Acceptance:
  account_id: acct.ctp.paper.19053
  display_alias: 19053
  source_ref:
  source_checksum:
  projection_ref:
  projection_checksum:
  projection_checkpoint_id:
  observed_at:
  ui_url:
  api_captures:
  browser_evidence:
  funds_match: pass | fail | blocked
  positions_match: pass | fail | blocked
  orders_match: pass | fail | blocked | not_available
  execution_reports_visible: pass | fail | blocked | not_available
  evidence_visible: pass | fail | blocked
  command_disabled: pass | fail
  account_switch_isolated: pass | fail
  blockers:
  verdict: passed | failed | blocked
```

## 12. Executable UI Acceptance / 可执行 UI 验收

The current API-backed UI acceptance binds the design to Playwright:

```powershell
cd frontend
npx playwright test tests/e2e/account-terminal-workbench.spec.ts
```

The real-login funds/positions UI acceptance is also executable and fails closed until the real-login source package is available:

```powershell
cd frontend
npx playwright test tests/e2e/ctp19053-ui-funds-positions.spec.ts --project=desktop
```

Covered assertions:

1. `/accounts/acct.ctp.paper.19053` renders `terminal-workbench-shell`.
2. readback mode shows `mirror API`, not fixture fallback.
3. the account selector lists `acct.ctp.paper.19053` and `acct.nautilus.paper.demo`.
4. capability table renders F2, F4, F3 and F5 rows.
5. F4 row identifies CTP paper 19053 as the source lane.
6. without `output/account_capability/ctp-paper-19053/source-package.json`, funds show `missing` and the UI renders a typed blocker instead of repo-local sample values.
7. without the real-login source package, positions and orders tables remain empty fail-closed.
8. with the real-login source package present, funds and positions must match that package exactly through the mirror API.
9. execution reports are optional until the real-login source package carries order/report rows; if report refs exist, they must be visible.
10. source health shows `typed_blocker` while blocked and `normalized_read_model` only after real-login source package ingestion.
11. evidence rail shows `source package` and `mirror projection`.
12. command capability state shows `observation only` and `none mounted`.
13. `/accounts/acct.ctp.live.025292` renders as a fail-closed blocked projection with `source unavailable`.
14. `/accounts/simulated-001` renders as Nautilus Sandbox Paper / simulated ledger only with broker submission disabled.
15. command controls and readiness wording remain absent across desktop/tablet/mobile.

Machine-readable evidence:

```text
docs/acceptance/2026-06-15-p011-account-workbench-api-readback-browser-evidence.json
docs/acceptance/2026-06-15-ctp19053-real-login-ui-acceptance-evidence.json
docs/acceptance/2026-06-15-ctp19053-real-login-ui-readback-blocker.json
docs/acceptance/browser-evidence/p011-account-workbench-api-readback/
```

## 13. Real Source Package Harness / 真实 source package 钩子

The current UI evidence does not accept repo-local sample values as real CTP Paper broker truth. Account Console now fails closed for `acct.ctp.paper.19053` unless the real-login source package below exists and passes validation.

Real CTP Paper `19053` funds and positions require a pinned source package at:

```text
output/account_capability/ctp-paper-19053/source-package.json
```

Source-owner template:

```text
contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json
```

Fail-closed blocker command:

```powershell
python scripts\validate_ctp19053_consistency.py --write-blocker
```

Sample harness command, which proves comparison logic only:

```powershell
python scripts\validate_ctp19053_consistency.py --source-package contracts\source_artifacts\samples\ctp_paper_19053_sample_source.json
```

Current blocker:

```text
blocker_id: ctp19053_real_login_source_unavailable
source_ref: output/account_capability/ctp-paper-19053/source-package.json
```

Attempted real-login read-only commands are recorded in:

```text
docs/acceptance/2026-06-15-ctp19053-real-login-ui-readback-blocker.json
```

The latest attempt was blocked by `PyO3 TD bridge unavailable`; the blocker must remain until the source owner repairs the TD bridge / dependent DLL load path, publishes `account_query.json` and `position_query.json`, then builds the pinned source package with:

```powershell
python scripts\build_ctp19053_source_package_from_real_login.py
```

UI screenshots alone cannot close this real-source acceptance.
