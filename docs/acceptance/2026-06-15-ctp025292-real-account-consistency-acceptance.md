# CTP 025292 Real Account Consistency Acceptance / CTP 025292 真实账户一致性验收

- Date: 2026-06-15
- Status: blocked_waiting_for_real_login_source_package
- Scope: read-only consistency acceptance for CTP real account `acct.ctp.live.025292`
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Architecture design: [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)
- Topic anchor: [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
- Roadmap anchor: [T001 Account Capability Feature Roadmap](../topics/roadmap/T001-account-capability-feature-roadmap.md)
- Related paper acceptance: [CTP 19053 UI readback acceptance](./2026-06-15-ctp19053-ui-readback-acceptance.md)
- Current blocker record: [CTP 025292 real account consistency blocker](./2026-06-15-ctp025292-real-account-consistency-blocker.json)
- Real-login UI blocker: [CTP 025292 real-login UI readback blocker](./2026-06-15-ctp025292-real-login-ui-readback-blocker.json)
- Real-login UI evidence: [CTP 025292 real-login UI evidence](./2026-06-15-ctp025292-real-login-ui-acceptance-evidence.json)
- Source package template: `contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json`

## 1. Acceptance Boundary / 验收边界

This acceptance verifies that Account Console UI displays the same funds, positions and orders as a pinned read-only CTP source snapshot for account `025292`, after that snapshot is normalized through Account Mirror.

It does not make Account Console, Account Mirror or UI the CTP broker truth source. It does not certify tradability, capital sufficiency, live readiness, admission, approval or order-entry capability.

Correct wording:

```text
UI matches the pinned CTP 025292 read-only source snapshot through Account Mirror.
```

Incorrect wording:

```text
UI proves the real broker account truth or live trading readiness.
```

## 2. Canonical Identity / 标准身份

The account must be represented as:

```text
account_id: acct.ctp.live.025292
display_alias: 025292
source_owner: nautilus_ctp_adapter
source_kind: ctp_trader_api
source_mode: live_observation
observation_mode: snapshot
event_stream: not_implemented
command.mode: disabled
```

`025292` is a display alias only. It must not be used as the canonical account id in storage, API paths, projection keys, evidence refs or browser selectors.

## 3. Trusted Source Read / 受信源读取

The only acceptable CTP read path is:

```text
CTP Trader API read-only query
  -> nautilus_ctp_adapter source artifact
  -> canonical account observation envelope
  -> Account Mirror projection
  -> Account Console API
  -> Account Workbench UI
```

Account Console backend and frontend must not call CTP Trader API directly.

Each acceptance run must pin an immutable source package:

```text
account_id: acct.ctp.live.025292
trading_day:
broker_id:
investor_id_hash_or_masked_ref:
source_session_ref:
source_ref:
source_checksum:
source_observed_at:
query_started_at:
query_completed_at:
projection_ref:
projection_checksum:
projection_checkpoint_id:
projection_checkpoint_ts:
schema_version:
```

The source package must include raw or normalized read-only records for:

1. `QryTradingAccount` / funds;
2. `QryInvestorPosition` / positions;
3. `QryOrder` / current trading-day orders;
4. `QryTrade` when fills exist or order fill state needs verification.

Sensitive credentials, full investor secrets, auth codes and session passwords must not be stored in acceptance artifacts.

## 4. Snapshot Consistency Rule / 快照一致性规则

Funds, positions and orders must come from one declared read window:

```text
query_window_id
query_started_at
query_completed_at
trading_day
source_checksum
projection_checkpoint_id
```

The read window is acceptable only if:

1. all required CTP queries complete successfully;
2. the projection checkpoint is derived from the same source package;
3. UI comparison uses that projection checkpoint, not a moving latest endpoint;
4. source health reports the same `trading_day`, `observed_at` and staleness state.
5. UI displays or exposes `observation_mode=snapshot` and does not claim realtime behavior.

If the account changes during verification, the run must be marked:

```text
ctp025292_source_changed_during_acceptance
```

Then acceptance must pin a new source package and rerun.

This acceptance does not require `OnRtnOrder` or `OnRtnTrade`. Those event streams may be added later, but they need separate polling/event-driven acceptance before the UI can claim immediate trade or order updates.

## 4.1 Future Freshness Modes / 未来新鲜度模式

Future implementations may extend this acceptance in two steps:

| Mode | Source input | UI claim allowed | Required extra evidence |
| --- | --- | --- | --- |
| `polling` | repeated read-only query packages | UI refreshes after polling within declared SLA | checkpoint sequence, refresh interval, lag metrics and stale blockers |
| `event_driven` | CTP `OnRtnOrder` / `OnRtnTrade` event observations plus reconciliation queries | UI reflects order/trade events within declared latency SLA | event contract, event sequence, mirror projection lag, reconciliation proof and mismatch blockers |

Until those modes are accepted, the valid claim is snapshot consistency only.

## 5. Required UI Routes / 必需 UI 路由

Minimum routes:

```text
/accounts/acct.ctp.live.025292
/accounts/acct.ctp.live.025292/positions
/accounts/acct.ctp.live.025292/orders
/accounts/acct.ctp.live.025292/evidence
```

Required when order rows exist:

```text
/accounts/acct.ctp.live.025292/orders/{client_order_id}
/accounts/acct.ctp.live.025292/fills
```

Optional when projections exist:

```text
/accounts/acct.ctp.live.025292/settlement
/accounts/acct.ctp.live.025292/equity
/accounts/acct.ctp.live.025292/reconcile
/accounts/acct.ctp.live.025292/incidents
```

## 6. Comparison Matrix / 对账矩阵

| Domain | CTP source query | Mirror projection | UI surface | Tolerance | Must fail if |
| --- | --- | --- | --- | --- | --- |
| Identity | investor/account metadata | `account_id`, `display_alias`, `source_kind`, `source_mode` | top status bar / selector | exact | UI uses bare `025292` as canonical id |
| Funds | `QryTradingAccount` | equity, balance, available cash, withdraw quota, frozen margin, frozen cash, margin used, close profit, position profit, commission | summary strip / funds panel | exact after declared decimal normalization | UI value differs, rounds invisibly or lacks source ref |
| Positions | `QryInvestorPosition` | instrument, exchange, direction, position date, total/today/yesterday qty, available qty, frozen qty, long/short frozen, position cost, average price, market value, unrealized PnL | positions table | qty exact; money/price within declared decimal tolerance | missing, extra, stale or mismatched row |
| Orders | `QryOrder` | client order id, CTP order ref/sys id, exchange, instrument, direction, offset, hedge flag, limit price, total volume, traded volume, remaining volume, order status, submit status, insert time, update time | orders table / bottom tape | exact for ids/status/qty; price tolerance | UI invents status, hides active/cancelled order or omits source ref |
| Trades/fills | `QryTrade` | trade id, order ref/sys id, instrument, direction, offset, price, volume, trade time, commission if available | fills table / order detail | exact for ids/qty; price tolerance | fill appears without account/order lineage |
| Source health | query result and adapter status | observed_at, received_at, lag, stale/blocker state, query errors | source health panel | exact state; lag within run policy | failed/stale query shown as healthy |
| Observation mode | source/projection metadata | `observation_mode`, `event_stream`, lag timestamps | top status bar / source health panel | exact | UI claims realtime when event stream is not implemented |
| Evidence | source package metadata | source refs, checksums, schema version, owner refs | evidence rail/drawer | exact | UI values cannot be traced to source/projection |
| Command boundary | capability registry | `command.enabled=false`, `command.mode=disabled` | command capability state | exact | submit/cancel/replace controls appear |
| Account isolation | selected account context | account-scoped projection checkpoint | account selector and all panels | exact | switching accounts leaks another account's funds, positions or orders |

## 7. Required Evidence / 必需证据

Each accepted run must produce:

1. pinned CTP source package path and checksum;
2. Account Mirror projection artifact/API capture and checksum;
3. Account Console API response captures for account summary, positions, orders, fills when present, source health and evidence;
4. browser selector evidence for funds, positions, orders and evidence refs;
5. screenshot evidence for the primary account page and orders page;
6. negative evidence that command controls are absent;
7. comparison report showing pass/fail/blocker per domain;
8. local commands used to collect source, build projection and run UI acceptance.

Recommended selectors:

```text
terminal-top-status-bar
account-selector
account-summary-metric-strip
account-funds-panel
account-positions-table
account-orders-table
account-order-detail-drawer
account-fills-table
account-source-health-panel
account-evidence-rail
account-command-capability-state
account-blocker-row
```

## 8. Positive Acceptance / 正向验收

CTP 025292 real-account consistency passes only when:

1. the UI opens `/accounts/acct.ctp.live.025292`;
2. canonical account id is `acct.ctp.live.025292` and display alias is `025292`;
3. the source package contains successful read-only funds, positions and orders queries;
4. Account Mirror projection checksum is pinned and linked to the same source checksum;
5. funds in UI match the pinned projection/source package;
6. positions in UI match the pinned projection/source package;
7. orders in UI match the pinned projection/source package;
8. trades/fills match when `QryTrade` records exist;
9. every displayed value has visible or drill-down source refs/checksums;
10. source health reports current/stale/blocked state consistently with the source package;
11. UI shows or exposes `observation_mode=snapshot` and `event_stream=not_implemented`;
12. command capability is disabled and no submit/cancel/replace controls render;
13. switching to another account does not preserve `025292` funds, positions or orders;
14. deterministic fixture acceptance remains available and separate from this live-read acceptance.

## 9. Negative Acceptance / 反向验收

CTP 025292 real-account consistency must fail if:

1. Account Console UI calls CTP Trader API directly;
2. Account Console backend calls CTP Trader API directly instead of reading canonical observations/projections;
3. UI uses `025292` as canonical account id;
4. source package is not pinned or lacks checksum;
5. projection checkpoint is not derived from the pinned source package;
6. funds differ from the pinned source/projection beyond declared tolerance;
7. any position row is missing, extra, stale or mismatched;
8. any order row is missing, extra, stale, status-mismatched or source-ref-missing;
9. fills appear without order/account lineage;
10. source query error is rendered as healthy state;
11. source changes during verification and the run is still marked passed;
12. UI claims realtime or immediate trade/order updates while `event_stream=not_implemented`;
13. submit, cancel or replace controls appear before command capability acceptance;
14. screenshot-only evidence is used without API/source comparison;
15. sensitive credentials are stored in acceptance artifacts.

## 10. Typed Blockers / 类型化阻塞

Allowed blocker outcomes:

```text
ctp025292_source_unavailable
ctp025292_source_auth_failed
ctp025292_source_query_failed
ctp025292_source_changed_during_acceptance
ctp025292_source_package_unpinned
ctp025292_projection_missing
ctp025292_projection_schema_mismatch
ctp025292_projection_checksum_mismatch
ctp025292_ui_funds_mismatch
ctp025292_ui_positions_mismatch
ctp025292_ui_orders_mismatch
ctp025292_ui_fills_mismatch
ctp025292_ui_evidence_missing
ctp025292_realtime_claim_unaccepted
ctp025292_browser_tooling_unavailable
ctp025292_command_controls_visible
ctp025292_sensitive_artifact_detected
```

Blockers must include owner, source ref if available, attempted command, timestamp, affected domain and next action.

## 11. Acceptance Record Template / 验收记录模板

```text
CTP025292 Real Account Consistency Acceptance:
  account_id: acct.ctp.live.025292
  display_alias: 025292
  trading_day:
  source_ref:
  source_checksum:
  source_observed_at:
  observation_mode: snapshot | polling | event_driven
  event_stream: not_implemented | connected | disconnected | blocked
  query_window_id:
  query_started_at:
  query_completed_at:
  projection_ref:
  projection_checksum:
  projection_checkpoint_id:
  ui_url:
  api_captures:
  browser_evidence:
  funds_match: pass | fail | blocked
  positions_match: pass | fail | blocked
  orders_match: pass | fail | blocked
  fills_match: pass | fail | blocked | not_available
  source_health_match: pass | fail | blocked
  observation_mode_visible: pass | fail
  evidence_visible: pass | fail | blocked
  command_disabled: pass | fail
  account_switch_isolated: pass | fail
  sensitive_artifact_check: pass | fail
  blockers:
  verdict: passed | failed | blocked
```

## 12. Implementation Handoff / 实施交接

This acceptance should be implemented after:

1. ADR-0004 architecture design review is complete;
2. identity, funds, position, order, trade/fill and capability contracts exist;
3. `nautilus_ctp_adapter` can emit a read-only pinned source package for `025292`;
4. Account Mirror can project that package without broker-specific UI/API branches;
5. Account Workbench can render API-backed account summary, positions, orders, source health and evidence.

The first implementation proposal that claims this acceptance must add executable comparison tooling. Manual visual inspection is not sufficient.

## 13. Current Executable Harness / 当前可执行验收钩子

The comparison harness exists and fails closed until the pinned source package is available:

```powershell
python scripts\validate_ctp025292_consistency.py --write-blocker
```

The UI acceptance is executable and also fails closed until the real-login source package is available:

```powershell
cd frontend
npx playwright test tests/e2e/ctp025292-ui-funds-positions.spec.ts --project=desktop
```

Current blocker:

```text
blocker_id: ctp025292_source_unavailable
source_ref: output/account_capability/ctp-live-025292/source-package.json
template: contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json
next_action: Produce pinned read-only CTP 025292 source package at output/account_capability/ctp-live-025292/source-package.json from the template and source-owner read-only query output
```

Real-login attempt blocker:

```text
blocker_id: ctp025292_real_login_td_bridge_unavailable
source_ref: output/account_capability/ctp-live-025292/source-package.json
attempted_account_query: D:\Nautilus\nautilus_ctp_adapter\scripts\ctp_account_query_smoke.py
attempted_position_query: D:\Nautilus\nautilus_ctp_adapter\scripts\ctp_position_query_smoke.py
observed_failure: PyO3 TD bridge unavailable; run maturin develop or pip install -e . before TD operations
```

After source-owner repair, build the package from real-login read-only query outputs:

```powershell
python scripts\build_ctp025292_source_package_from_real_login.py
```

The sample harness proves the comparison logic only; it does not prove real account consistency:

```powershell
python scripts\validate_ctp025292_consistency.py --source-package contracts\source_artifacts\samples\ctp_live_025292_sample_source.json
```

This acceptance remains blocked for real `025292` until the source owner provides the pinned read-only package. The blocked UI projection is accepted as fail-closed evidence, not as a passed real-account consistency run.
