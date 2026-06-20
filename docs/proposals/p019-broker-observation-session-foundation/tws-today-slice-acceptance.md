# P019 TWS Today Slice Acceptance / TWS 当日开发切片验收

- Proposal ID: `p019-broker-observation-session-foundation`
- Slice: `tws_observation_first_slice`
- Status: planned
- Date: 2026-06-20
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)

## 1. ADR-0005 Functional List / 功能列表

| ID | Function | Scope | Today |
| --- | --- | --- | --- |
| F1 | Broker Observation Profile | Broker-neutral profile with account id, source kind, session owner and secret/config refs | TWS only |
| F2 | Read-only Broker Session | Governed observation connection/session lifecycle | TWS only |
| F3 | Session Conflict Policy | Fail closed for username/client id/session owner conflicts | TWS only |
| F4 | Account Snapshot Observation | Account summary, balances, margins and source health | TWS only |
| F5 | Position Observation | Positions with instrument, quantity, price/value/PnL and provenance | TWS only |
| F6 | Order Observation | Open/recent orders as observed state, not command authority | TWS only |
| F7 | Nautilus-Compatible OrderStatusReport | Map observed order callbacks/status rows to Nautilus-compatible report shape | TWS only |
| F8 | Nautilus-Compatible FillReport | Map executions/fills to Nautilus-compatible fill report shape | TWS only |
| F9 | Raw Payload Provenance | Raw broker payload refs/checksums/redacted excerpts only | TWS only |
| F10 | Execution Reports Table | Render normalized order/fill reports as a durable, parity-checkable table for review | TWS only |
| F11 | Durable Observation Store | Persist order/fill reports, funds snapshots, positions snapshots, session health and freshness cursors | TWS only |
| F12 | Account Mirror Projection | TWS observation feeds existing Account Mirror projection boundary | TWS only |
| F13 | Freshness / Lag / Sequence | observed/received/projected timestamps, sequence/cursor and staleness | TWS only |
| F14 | UI/API Readback | Account Console shows read-only observation state and blockers | TWS only if backend/API ready |
| F15 | Command Drift Guard | No submit/cancel/replace/modify from observation surface | TWS only |
| F16 | Cross-Broker Extension Rule | CTP/stock/CQG/TT must reuse the same profile/mapper model later | Not today |

## 2. Today Scope / 今日范围

Today only develops TWS / IB Gateway read-only observation under ADR-0005.

In scope today:

1. `source_kind=ib_tws_observation`.
2. TWS observation profile contract/fixture using refs only.
3. TWS read-only connection/session health surface or typed blocked state.
4. TWS account snapshot shape for account summary/funds.
5. TWS positions shape.
6. TWS open orders / order status report mapping.
7. TWS executions / fill report mapping.
8. Raw TWS payload provenance refs and redaction.
9. Execution Reports table shape for normalized order/fill reports.
10. Durable local observation store for TWS reports, funds snapshots, positions snapshots and source health.
11. Account Mirror projection for the TWS account.
12. Negative gates for no command and no raw secrets.

Out of scope today:

1. CTP, stock, CQG or TT adapter implementation.
2. Any order submit, cancel, replace or modify.
3. Credential storage, 2FA automation or TWS launcher automation.
4. Live trading readiness, capital approval, admission or tradability.

## 3. Today Acceptance Matrix / 今日验收矩阵

| ID | Function | Acceptance requirement | Must fail if | Minimal evidence |
| --- | --- | --- | --- | --- |
| TWS-A1 | F1 Profile | TWS profile uses `acct.ib.*`, `source_kind=ib_tws_observation`, session owner and secret/config refs only | raw username/password/2FA/host/port/client id secret is stored as Account Console truth | schema/fixture test |
| TWS-A2 | F2 Session | TWS observation session reports `connected`, `blocked`, `stale` or `disconnected` with typed reason | missing connection is shown as healthy | backend/API test or blocked fixture |
| TWS-A3 | F3 Conflict | same client id/session owner/unknown owner conflict returns typed blocker | Account Console steals or silently reuses Nautilus TWS session | conflict-policy test |
| TWS-A4 | F4 Account snapshot | account summary/funds include source timestamp, received timestamp, checksum, provenance and table-ready per-currency rows | values appear without provenance or funds are only representable as single-currency metric cards | projection/API test |
| TWS-A5 | F5 Positions | positions preserve instrument id, quantity, avg price, market price/value, PnL and provenance | empty/inferred rows replace missing source data | projection/API test |
| TWS-A6 | F6 Orders | observed orders include client/venue order ids, status, side, type, quantity, filled qty, price and timestamps | order row enables action controls | projection/API test + UI/API negative |
| TWS-A7 | F7 OrderStatusReport | TWS order callback/status row maps to Nautilus-compatible `OrderStatusReport` fields | broker-native order object becomes canonical report truth | mapper contract test |
| TWS-A8 | F8 FillReport | TWS execution/fill maps to Nautilus-compatible `FillReport` fields | fill exists only as raw broker payload | mapper contract test |
| TWS-A9 | F9 Raw provenance | raw TWS payload is linked by ref/checksum and redacted excerpt only | browser parses raw payload as order/account truth | backend schema + browser/API negative |
| TWS-A10 | F10 Execution Reports table | normalized order/fill reports render as a table with report type, report id, client/venue order ids, instrument, side, status/trade id, quantity, filled/remaining quantity, price, timestamp, sequence/cursor and provenance | reports render only as cards/free text or raw payload dump | Playwright table/column assertion |
| TWS-A11 | F10 Execution Reports parity | table rows match Nautilus-compatible `OrderStatusReport` / `FillReport` source rows and preserve deterministic sort by sequence/cursor or timestamp/report id fallback | UI drops/merges rows, loses report id/provenance or changes report ordering without an explicit user sort | Playwright + report parity artifact |
| TWS-A12 | F11 Durable store | order/fill reports, funds snapshots, positions snapshots, session health and freshness cursors survive process restart or reload from local store | reports exist only in memory/startup callback stream and disappear after restart | persistence/reload test |
| TWS-A13 | F11 Replay gaps | missing startup replay, sequence gap, report-store gap or store checksum mismatch produces typed blocker in API and Execution Reports table | UI claims complete order lifecycle from partial local data | gap/replay negative test + browser blocked-state assertion |
| TWS-A14 | F12 Mirror | TWS observation appears through Account Mirror/API shape, not a broker-specific UI path | frontend calls a TWS adapter endpoint directly for account truth | API route test |
| TWS-A15 | F13 Freshness | projection exposes observed/received/projected timestamps and sequence/cursor/staleness | UI claims realtime from unordered or snapshot-only data | API contract test |
| TWS-A16 | F15 No command | no submit/cancel/replace/modify endpoints or controls are reachable | any order mutation route/control exists in today slice | backend grep/test + UI/API negative |

## 4. Functional Coverage Traceability / 功能覆盖追溯

| Function | Today coverage | Acceptance IDs | Coverage note |
| --- | --- | --- | --- |
| F1 Broker Observation Profile | covered | TWS-A1 | TWS-only profile with refs and no raw secrets |
| F2 Read-only Broker Session | covered | TWS-A2 | May pass as connected or typed blocked state |
| F3 Session Conflict Policy | covered | TWS-A3 | Protects Nautilus/session ownership |
| F4 Account Snapshot Observation | covered | TWS-A4 | Funds/account summary with provenance and table-ready multi-currency rows |
| F5 Position Observation | covered | TWS-A5 | Position rows must preserve source fields |
| F6 Order Observation | covered | TWS-A6 | Observed orders only, no actions |
| F7 Nautilus-Compatible OrderStatusReport | covered | TWS-A7 | Mapper contract required |
| F8 Nautilus-Compatible FillReport | covered | TWS-A8 | Mapper contract required |
| F9 Raw Payload Provenance | covered | TWS-A9 | Provenance only, not truth |
| F10 Execution Reports Table | covered | TWS-A10, TWS-A11 | Required for report review, row-level parity and deterministic readback |
| F11 Durable Observation Store | covered | TWS-A12, TWS-A13 | Required for post-session review, table reload and replay-gap blockers |
| F12 Account Mirror Projection | covered | TWS-A14 | No broker-specific UI truth path |
| F13 Freshness / Lag / Sequence | covered | TWS-A15 | Required before realtime claims |
| F14 UI/API Readback | conditionally covered | TWS-A14, TWS-A16 | API required; UI only if backend/API slice reaches UI today |
| F15 Command Drift Guard | covered | TWS-A16 | No mutation route/control |
| F16 Cross-Broker Extension Rule | scoped out today, guarded | Closeout Rule | TWS pass must not imply CTP/stock/CQG/TT support |

## 5. Suggested Verification Commands / 建议验证命令

```bash
python scripts/check_proposal_docs.py --root . --proposal-id p019-broker-observation-session-foundation
```

Implementation-specific tests must be added with the TWS slice before closeout. Suggested names:

```text
tests/test_ib_tws_observation_profile.py
tests/test_ib_tws_session_conflict_policy.py
tests/test_ib_tws_order_report_mapping.py
tests/test_ib_tws_observation_store.py
tests/test_ib_tws_account_mirror_projection.py
tests/test_ib_tws_execution_reports_table_contract.py
```

## 6. Closeout Rule / 收口规则

The TWS slice can close only when TWS-A1 through TWS-A16 pass or produce typed blockers. Passing TWS does not imply CTP, stock, CQG or TT support, and does not authorize command capability.
