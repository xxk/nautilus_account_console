# T001 Account Capability Feature Roadmap / T001 账户能力功能路线图

- Date: 2026-06-15
- Status: planning
- Topic anchor: [T001 Account Mirror Observation Plane](../T001-account-mirror-observation-plane.md)
- Architecture design: [Account Capability Fabric architecture design](../../design/account-capability-fabric-architecture-design.md)
- UI design: [Account Workbench terminal UI design](../../design/account-workbench-terminal-ui-design.md)
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Acceptance anchor: [ADR-0004 Account Capability Fabric acceptance](../../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md)
- CTP 19053 UI readback acceptance: [CTP 19053 UI readback acceptance](../../acceptance/2026-06-15-ctp19053-ui-readback-acceptance.md)
- CTP 025292 real-account consistency acceptance: [CTP 025292 real account consistency acceptance](../../acceptance/2026-06-15-ctp025292-real-account-consistency-acceptance.md)

## 1. Planning Goal / 规划目标

This roadmap decomposes account capability work into safe feature slices before implementation starts.

It prioritizes observation-only Account Mirror work first, then source health and evidence, then command capability design. It intentionally avoids broker action controls until command capability gates are accepted.

## 2. Feature Tracks / 功能轨道

| Track | Purpose | First target |
| --- | --- | --- |
| F1 Account identity and registry | canonical accounts, aliases and domains | `acct.nautilus.paper.demo`, `acct.ctp.paper.19053` |
| F2 Observation contracts | common envelope and typed payloads | balance and position |
| F3 Mirror projection store | file/SQLite-backed read models | accounts, balances, positions, capabilities |
| F4 Source adapters/bridges | source artifact to canonical observations | Nautilus Paper, CTP Paper 19053 |
| F5 Account Workbench API mode | UI reads API projections when available | summary and positions |
| F6 Source health and blockers | staleness, lag and typed blocker visibility | stale/missing source |
| F7 Evidence explorer integration | source refs, checksums and owner evidence | account-bound evidence drawer |
| F8 IB TWS source | second external broker observation | IB paper account |
| F9 Stock source | future stock observation support | stock paper account |
| F10 Command capability design | order intent and execution readback | Nautilus Paper command proposal |
| F11 CTP live read-only consistency | real-account read-only funds, positions and orders comparison | `acct.ctp.live.025292` |
| F12 Observation freshness upgrade | snapshot -> polling -> event-driven source freshness | CTP order/trade readback |

## 3. P0 Landing Sequence / P0 落地顺序

P0 proves that the architecture works for two account worlds without command controls.

| Step | Feature | Deliverable | Required Gate | Must not do |
| --- | --- | --- | --- | --- |
| P0.1 | Account identity registry | canonical account registry contract and fixture | `ADR0004-G01-IDENTITY` | store bare `19053` as canonical account id |
| P0.2 | Observation envelope | `account_observation` contract | `T001-GATE-OBSERVATION-CONTRACT` | expose broker-native payload as UI contract |
| P0.3 | Balance observation | `account_balance` contract and fixture | `ADR0004-G02-PROVENANCE` | render balance without source refs/checksum |
| P0.4 | Position observation | `position_snapshot` contract and fixture | `ADR0004-G02-PROVENANCE` | render empty positions for stale source |
| P0.5 | Capability registry minimum | capability contract, observation-enabled fixture and disabled-command fixture | `ADR0004-G03-CAPABILITY-REGISTRY`, `ADR0004-G05-COMMAND-DISABLED-DEFAULT` | infer command ability from paper/live account kind |
| P0.6 | Mirror projection reader | file-backed projection reader for accounts/balances/positions/capabilities | `ADR0004-G04-FABRIC-FIT` | add broker-specific API families |
| P0.7 | Nautilus Paper bridge | first-party paper observations | `T001-GATE-SOURCE-PROVENANCE` | treat sandbox fixture as the only source model |
| P0.8 | CTP Paper 19053 bridge | read-only bridge from `nautilus_ctp_adapter` artifact | `T001-GATE-SOURCE-PROVENANCE` | call CTP Trader API from Account Console |
| P0.9 | API-backed Account Workbench | `/accounts/{account_id}`, `/positions`, `/capabilities` | `ADR0004-G10-FAIL-CLOSED-BLOCKERS` | remove deterministic fixture mode |
| P0.10 | Browser/readback evidence | open both account routes and record browser/API evidence | UI implementation acceptance | show command controls |

P0 acceptance closeout must map to ADR-0004 layers:

```text
L0-ARCH: architecture design reviewed
L1-CONTRACT: identity, balance, position and capability contracts accepted
L2-MIRROR: Nautilus Paper and CTP Paper 19053 source artifacts project through Account Mirror
L3-UI-READBACK: UI matches pinned projections for funds, positions, source health and evidence
L4-COMMAND-BOUNDARY: command capability disabled; no order controls
L5-CLOSEOUT: commands, API captures, browser evidence, checksums and blockers recorded
```

P0 cannot be accepted by screenshots alone. It needs source/projection comparison evidence.

## 4. P1 Expansion / P1 扩展

| Step | Feature | Deliverable | Gate |
| --- | --- | --- | --- |
| P1.1 | Source health panel | source lag, last observed time, source mode and blocker rows | `ADR0004-G10-FAIL-CLOSED-BLOCKERS` |
| P1.2 | Orders/fills observations | order state and fill observation contracts | `ADR0004-G02-PROVENANCE` |
| P1.3 | Settlement/equity observations | settlement and equity point observations | `ADR0004-G02-PROVENANCE` |
| P1.4 | Evidence drawer integration | account-bound source refs and checksums | evidence capability |
| P1.5 | IB TWS paper bridge | IB account summary and position observations | `ADR0004-G04-FABRIC-FIT` |
| P1.6 | Replay source | replay observations into mirror projection | source provenance gate |
| P1.7 | CTP Live 025292 read-only source | pinned read-only CTP source package for funds, positions, orders and fills when present | `ADR0004-G02-PROVENANCE`, `ADR0004-G08-OWNER-SEPARATION` |
| P1.8 | CTP Live 025292 UI consistency | UI/API comparison against pinned Account Mirror projection | `ADR0004-G10-FAIL-CLOSED-BLOCKERS`, CTP 025292 real-account consistency acceptance |

P1 orders/execution-report closeout additionally requires:

1. order and execution-report contracts;
2. Account Mirror projection evidence for orders, fills and report refs;
3. UI table/detail/evidence readback comparison;
4. negative proof that execution reports are provenance/evidence, not final broker truth;
5. command controls remain disabled unless a separate command proposal is accepted.

P1 CTP Live 025292 closeout additionally requires:

1. capability registry entry exists for `acct.ctp.live.025292` with observation enabled and command disabled;
2. read-only CTP query artifact for `QryTradingAccount`, `QryInvestorPosition`, `QryOrder` and `QryTrade` when fills exist;
3. immutable source ref and checksum with masked investor/session identifiers;
4. Account Mirror projection checkpoint derived from the same source package;
5. UI comparison for funds, positions, orders, fills when present, source health and evidence;
6. negative proof that Account Console UI/backend do not call CTP Trader API directly;
7. command capability disabled and no submit/cancel/replace controls visible.

P1 may claim only `observation_mode=snapshot` unless polling refresh is implemented and accepted. It must not claim realtime order/trade UI behavior.

## 5. P2 Expansion / P2 扩展

| Step | Feature | Deliverable | Gate |
| --- | --- | --- | --- |
| P2.1 | Stock paper bridge | stock account balances and positions | fabric fit gate |
| P2.2 | Multi-currency balances | currency-aware balance projection | observation contract gate |
| P2.3 | Instrument taxonomy | futures/equity/option/fx metadata bridge | no UI broker branching |
| P2.4 | Portfolio/account grouping | account group read model | owner boundary gate |
| P2.5 | Command capability ADR | order intent, risk/approval, execution gateway and mirror readback design | `ADR0004-G06-PAPER-COMMAND` planned |
| P2.6 | CTP polling freshness | repeated read-only CTP query packages projected through Account Mirror | UI refreshes from newer checkpoints within declared polling SLA |
| P2.7 | CTP event-driven readback design | `OnRtnOrder` / `OnRtnTrade` observation contracts, lag metrics and reconciliation blockers | design accepted before realtime UI claim |
| P2.8 | CTP event-driven UI readback | orders/fills/positions update from event observations plus reconciliation queries | UI reflects trade/order events within declared latency SLA |

## 6. Account Workbench Feature Shape / Account Workbench 功能形态

Primary account page:

```text
/accounts/{account_id}
  identity
  capability badges
  balance summary
  position summary
  source health strip
  evidence refs
  blockers
```

Positions page:

```text
/accounts/{account_id}/positions
  instrument
  direction
  net/today/yesterday/available/frozen qty
  average price
  market price
  market value
  unrealized pnl
  carryover/settlement/source refs
  stale/blocker state
```

Capabilities page or panel:

```text
/accounts/{account_id}/capabilities
  observation capability
  command capability
  reconciliation capability
  evidence requirement
  owner refs
  disabled/blocked reasons
```

## 7. Proposal / Phase Slicing / Proposal 与 Phase 切片

T001 uses one umbrella proposal for this account-capability landing:

```text
docs/proposals/p011-account-capability-contracts/
```

The earlier P012-P017 names are not separate proposals. They are folded into P011 phases to keep one acceptance spine and avoid proposal drift.

| P011 phase | Former slice name | Scope | Why |
| --- | --- | --- | --- |
| Phase 1 | P011 Account Capability Contracts | identity, observation envelope, balance, position, capability contracts and fixtures | contract-first foundation |
| Phase 2 | P012 Mirror Projection Reader | file-backed projection reader and API endpoints for P0 accounts | backend/API slice |
| Phase 3 | P013 Nautilus Paper And CTP 19053 Bridges | source artifact bridge into canonical observations | first two-source proof |
| Phase 4 | P014 Account Workbench API Mode | summary/positions/capabilities panels read API projections | UI slice |
| Phase 5 | P015 Source Health And Evidence | source health panel, blockers, evidence drawer | operations slice |
| Phase 6 | P017 CTP 025292 Real Account Consistency | read-only live CTP source package, mirror projection and UI/API comparison for funds, positions and orders | real-account consistency without command capability |
| Phase 7 | P016 Command Capability Design Gate | order intent/risk/gateway/readback design only | future command boundary |

## 8. Non-Goals Until Command Capability / Command 能力前非目标

Do not implement:

1. submit order;
2. cancel order;
3. replace order;
4. direct broker login/session control from UI;
5. funding transfer;
6. allocation mutation;
7. live trading readiness labels;
8. broker tradability certification.

## 9. Open Design Questions / 开放设计问题

| Question | Default for P0 |
| --- | --- |
| File-backed JSONL or SQLite first? | choose simplest reader that preserves envelope/projection contracts |
| Does CTP 19053 bridge read latest artifact or a pinned artifact root? | use pinned artifact first, then add latest pointer with source health |
| How should CTP 025292 live reads be accepted? | pinned read-only source package and Account Mirror checkpoint; never moving latest UI comparison |
| Can CTP fills update Web UI immediately? | not in snapshot phase; add polling first, then event-driven `OnRtnOrder`/`OnRtnTrade` lane with explicit SLA |
| Should capability registry be generated or hand-authored for P0? | hand-authored deterministic fixture first, generated projection later |
| Should `/capabilities` be visible in UI P0? | show compact badges first; deep page can wait |
| How to handle multiple currencies? | single-currency CNY for P0, contract allows currency field |
