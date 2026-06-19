# T001 Account Mirror Observation Plane Topic / T001 账户镜像观测面专题

- Updated: 2026-06-15
- Status: active
- Topic ID: T001
- Topic slug: `T001-account-mirror-observation-plane`
- Scope: implementation roadmap for Account Capability Fabric observation sources, Account Mirror projections and future command capability boundary
- Decision anchor: [ADR-0004](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Cross-repo routing anchor: ADR-0047 `nautilus_strategies/docs/adr/0047-adopt-unified-broker-account-runtime-routing.md`
- Architecture design anchor: [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)
- ADR acceptance anchor: [ADR-0004 Account Capability Fabric acceptance](../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md)
- Feature roadmap: [T001 Account Capability Feature Roadmap](./roadmap/T001-account-capability-feature-roadmap.md)
- UI slice anchor: [ADR-0003](../adr/0003-adopt-contract-first-ui-slice-development.md)
- Owner map: [Account Console owner map](../ownership/account-console-owner-map.md)

## 1. Purpose / 目的

This topic prepares landing work for the Account Capability Fabric's observation capability. Account Mirror is the read-only implementation that can display Nautilus Paper Sandbox, CTP Paper `19053`, CTP Live `025292` read-only snapshots, IB TWS and future stock accounts through one Account Workbench.

The topic also records the future command capability boundary: Account Mirror observes and reconciles; it does not submit, cancel, replace, approve or allocate.

T001 starts after ADR-0004 and the Account Capability Fabric architecture design. T001 Gates apply the ADR acceptance to roadmap/proposal slices; they do not replace architecture design review.

ADR-0047 adds a stricter route/context boundary for current real-account work. T001 may project route/account context fields from accepted artifacts, but it must not create the upstream `AccountRegistry`, `route_id` resolver, `AccountRuntimeContext`, runtime builder, adapter contract or account/order truth. Any real-account consistency task must therefore separate source-owner package production from Account Console projection/UI acceptance.

## 2. Target Shape / 目标形态

```text
Account Capability Fabric
  -> observation capability
  -> canonical observation contract
  -> Account Mirror ledger
  -> account projections
  -> Account Console API
  -> Account Workbench panels
```

First-class source kinds:

| Source kind | First account target | Landing priority |
| --- | --- | --- |
| `nautilus_paper_runtime` | `acct.nautilus.paper.demo` | P0 |
| `ctp_trader_api` | `acct.ctp.paper.19053` | P0 |
| `ctp_trader_api` | `acct.ctp.live.025292` | P1 |
| `ib_tws` | `acct.ib.paper.<account>` | P1 |
| `stock_broker_api` | `acct.stock.paper.<broker>.<account>` | P2 |
| `replay_file` | account-bound replay | P1 |
| `deterministic_fixture` | acceptance fixtures | always |

## 3. Phase Roadmap / 阶段路线

| Phase | Goal | Deliverables | Gate |
| --- | --- | --- | --- |
| M1 contracts | Define canonical account observations | `account_observation`, `account_balance_observation`, `position_observation`, source health schema | schema validation and owner map update |
| M2 Nautilus Paper source | baseline first-party source | file/API bridge for Nautilus Paper account balances and positions | one account visible via API-backed Account Workbench |
| M3 CTP Paper 19053 source | real paper account bridge | CTP paper `19053` balance and position observations from `nautilus_ctp_adapter` output or read-only query artifact | `acct.ctp.paper.19053` summary and positions visible with source refs |
| M4 projection store | durable mirror read models | append-only ledger reader plus balance/position projection store | cursor replay, checksum, stale/blocker tests |
| M5 UI switch | fixture-to-API workbench mode | Account Summary and Positions panels read API when available and retain fixture states | browser evidence for Nautilus Paper and CTP 19053 |
| M6 source health | operational diagnostics | lag, source status, last observation, typed blockers | stale/offline source acceptance |
| M7 capability registry | account observation/command capability model | minimum capability contract, disabled-command fixture, blockers and API projection | UI cannot infer actions from account type |
| M8 CTP 19053/025292 consistency | real-account read-only verification | source-owner pinned `19053` and `025292` funds, positions, orders and fills source packages through Account Mirror | UI/API values match source/projection package without command controls and pass ADR-0047 route/context alignment |
| M8a ADR-0047 route context alignment | prevent market data, execution and account truth collapse | projection carries or blocks `route_id`, `account_alias`, `market_data_source`, `execution_adapter`, `account_truth`, `risk_domain` and `evidence_partition` | market data cannot become account truth; source/UI evidence cannot imply readiness |
| M9 IB TWS source | second external broker | IB paper balance and positions bridge | same UI panels without broker-specific branches |
| M10 stock source | future equity broker support | stock paper account bridge | equity positions displayed through canonical contract |
| M11 command-plane ADR | future order entry design | separate ADR/proposal for order intent, risk/approval, execution gateways and readback | no order controls before acceptance |

### 3.1 Observation Freshness Roadmap / 观测新鲜度路线

T001 intentionally separates account consistency from realtime delivery. CTP fills and order changes may appear in the Web UI only after the source adapter emits observations and Account Mirror projects them. UI must never call CTP directly to look "more realtime".

Long-term delivery order:

| Stage | Observation mode | Source input | UI behavior | Acceptance claim |
| --- | --- | --- | --- | --- |
| `OBS-SNAPSHOT` | pinned snapshot | read-only query artifact, for example `QryTradingAccount`, `QryInvestorPosition`, `QryOrder`, `QryTrade` | render checkpointed funds, positions and orders with source refs | UI matches pinned source/projection package |
| `OBS-POLLING` | polling refresh | repeated read-only query packages with checkpoints | refresh panels from newer Account Mirror projection; show last observed time and lag | UI updates after polling within declared refresh SLA |
| `OBS-EVENT-DRIVEN` | event-driven realtime | CTP `OnRtnOrder` / `OnRtnTrade` events plus reconciliation queries | update orders/fills/positions/balances from event observations and mark reconciliation state | UI reflects CTP order/trade events within declared latency SLA |

`OBS-SNAPSHOT` is enough for first real-account consistency acceptance. `OBS-POLLING` and `OBS-EVENT-DRIVEN` are future enhancements and must not be claimed by snapshot-only work.

Every account projection should expose:

```text
observation_mode = snapshot | polling | event_driven
source_observed_at
source_received_at
projected_at
ui_seen_at
source_lag_ms
projection_lag_ms
reconciliation_state
```

If event delivery is not implemented, the capability/projection must say:

```text
event_stream = not_implemented
```

The UI may show snapshot or polling state, but it must not display realtime wording until event-driven acceptance exists.

## 4. Topic Gates / Topic 门禁

T001 uses sparse Gates and detailed Checks. Gates block topic phase advancement but must not write runtime, broker, account, admission, approval, capital or trading-readiness truth.

| Gate ID | Gate | Required before | Must fail if |
| --- | --- | --- | --- |
| `T001-GATE-OBSERVATION-CONTRACT` | canonical observation contracts are explicit | M2 source work | balance/position/source health fields are implemented without schemas |
| `T001-GATE-SOURCE-PROVENANCE` | every source value has owner, source ref, timestamp and checksum or blocker | API-backed UI rendering | live-looking values render without provenance |
| `T001-GATE-CAPABILITY-REGISTRY` | observation, command, reconciliation and evidence capabilities are explicit and fail closed | any account action surface or API-backed account closeout | UI infers capability from account type, route or broker |
| `T001-GATE-READBACK-RECONCILIATION` | command status can only close through execution event plus Account Mirror readback | any future command-plane UI | button click or gateway response is treated as final account state |
| `T001-GATE-ADR0047-ROUTE-CONTEXT` | route/account context is projected or blocked without Account Console owning runtime routing | real-account consistency closeout after ADR-0047 | `market_data_source` implies `execution_adapter` or `account_truth`, or UI/source evidence claims readiness |

### T001-GATE-CAPABILITY-REGISTRY / 账户能力注册门

Purpose: ensure account capability is a typed fabric projection, not an implicit account type.

Checks:

| Check ID | Requirement | Proof item | Must fail if |
| --- | --- | --- | --- |
| `T001-CAP-01` | canonical `account_id` is namespace-qualified and has display alias only as presentation | capability fixture or API payload | bare `19053` is used as canonical identity |
| `T001-CAP-02` | `observation.enabled`, `observation.source_kind` and `observation.mirror_state` are present | capability contract + fixture/API sample | UI renders account detail without observation capability |
| `T001-CAP-03` | `command.enabled`, `command.mode`, `gateway_kind`, `allowed_actions`, risk/approval flags, `authority_ref`, `source_ref` and checksum are present | capability contract + fixture/API sample | command capability is inferred from `account_domain`, broker, route or UI state |
| `T001-CAP-04` | missing or disabled command capability hides submit/cancel/replace controls | browser/API acceptance | any command control appears for disabled capability |
| `T001-CAP-05` | paper command capability remains blocked until command-plane proposal acceptance exists | proposal/ADR ref + capability payload | paper actions bypass order intent or mirror readback |
| `T001-CAP-06` | live command capability requires authority, risk/approval, session state and readback gates | command-plane acceptance evidence | live action appears with missing authority or stale readback |
| `T001-CAP-07` | observation owner, command owner, risk/approval owner and UI owner are separate fields | owner boundary evidence | Account Mirror or UI becomes execution authority |
| `T001-CAP-08` | reconciliation mismatch produces typed blocker | blocker fixture/API payload | UI shows success when execution and mirror readback disagree |
| `T001-CAP-09` | any new account behavior maps to an accepted Account Capability Fabric capability | ADR/topic/proposal evidence | implementation creates an ad hoc plane or broker-specific UI branch |

Gate verdict states:

```text
planned
blocked
passed_for_observation_only
passed_for_paper_command
passed_for_live_command
```

The MVP target for T001 is `passed_for_observation_only`.

## 5. MVP Acceptance / MVP 验收

MVP is accepted only when both accounts can be displayed from API-backed projections:

```text
/accounts/acct.nautilus.paper.demo
/accounts/acct.nautilus.paper.demo/positions
/accounts/acct.ctp.paper.19053
/accounts/acct.ctp.paper.19053/positions
```

Required evidence:

1. account balance and position observation schemas exist;
2. source refs and checksums are present for every displayed balance/position value;
3. stale or missing source produces typed blocker UI, not blank success;
4. UI contains no order action controls;
5. Account Workbench still passes fixture acceptance;
6. API-backed mode and fixture mode are both testable.
7. capability registry marks both MVP accounts as `command.mode=disabled` unless a separate command proposal is accepted.
8. no command action controls are rendered for disabled command capability.

CTP Live `025292` is not required for P0 MVP. It is accepted by the separate real-account consistency acceptance:

```text
docs/acceptance/2026-06-15-ctp025292-real-account-consistency-acceptance.md
```

That acceptance requires pinned source/projection comparison for funds, positions and orders before any UI claim of real-account consistency.

After ADR-0047, the same rule applies to CTP Paper `19053`: UI readback is accepted only against a source-owner pinned package at `output/account_capability/ctp-paper-19053/source-package.json`, not against repo-local sample projections. Both CTP `19053` and `025292` must pass the route/context alignment gate before closeout can say the UI is consistent with a real account.

## 6. Account Identity Rules / 账户身份规则

Canonical identity must be namespace-qualified:

```text
acct.nautilus.paper.<account>
acct.ctp.paper.19053
acct.ctp.live.025292
acct.ctp.live.<account>
acct.ib.paper.<account>
acct.ib.live.<account>
acct.stock.paper.<broker>.<account>
acct.stock.live.<broker>.<account>
```

Display aliases may be short:

```text
19053
IB Paper DU123456
Nautilus Paper Demo
```

UI links, API paths, source refs, evidence and tests must use canonical `account_id`.

## 7. Owner Boundary / Owner 边界

| Layer | Owner | May do | Must not do |
| --- | --- | --- | --- |
| Source adapter | source repo, for example `nautilus_ctp_adapter` or Nautilus Paper runtime owner | produce source observations or source artifacts | write Account Console UI state |
| Account Mirror contracts | `account-console-contracts` | define canonical observation/projection schemas | define broker execution behavior |
| Account Mirror projector | `account-console-backend` / projector owner | reduce observations into read models | mint broker/account truth or repair source data silently |
| Account Console UI | `account-console-frontend` | render read models, source refs and blockers | call broker APIs or expose order actions |
| Command Plane | future command owner | order intent, risk/approval, execution gateways | reuse Account Mirror as command writer |
| Capability Registry | `account-console-contracts` plus future command authority | declare observation/command capability projection | infer authority from account kind or UI route |

## 8. Typed Blockers / 类型化阻塞

Missing source data must produce explicit blocker states:

| Blocker | Meaning | UI behavior |
| --- | --- | --- |
| `source_unavailable` | source cannot be reached or artifact missing | show last known value only if provenance is present |
| `source_stale` | last observation exceeds source SLA | mark stale and show lag |
| `schema_mismatch` | source payload cannot validate | block projection and show schema evidence |
| `checksum_mismatch` | source checksum differs from expected | block projection |
| `owner_boundary_missing` | source owner or authority not declared | block closeout |
| `capability_missing` | observation or command capability is not declared | hide action controls and show typed blocker where capability is required |
| `command_authority_missing` | command capability lacks authority ref or owner | block command UI |
| `risk_or_approval_missing` | command capability requires risk/approval evidence that is absent | block command UI |
| `readback_reconciliation_mismatch` | execution event and mirror readback disagree | show reconciliation blocker, not success |

## 9. Capability Acceptance / 能力验收

Before any account is considered ready for API-backed UI rendering, it must have a capability projection:

```text
account_id
observation.enabled
observation.mirror_state
command.enabled
command.mode
reconciliation.enabled
evidence.required
command.gateway_kind
command.allowed_actions
command.requires_risk_check
command.requires_approval
command.authority_ref
source_ref
checksum
```

Acceptance matrix:

| Scenario | Required UI/API result |
| --- | --- |
| observation enabled, command disabled | balances/positions may render; no command controls |
| observation stale, command disabled | stale blocker renders; no command controls |
| observation enabled, paper command enabled | command entry may render only after command-plane proposal acceptance |
| live command enabled | live command entry remains blocked unless authority, risk, approval, session and readback gates pass |
| capability missing | account action surface fails closed |
| readback mismatch | command status displays reconciliation blocker |

## 10. Future Command Plane / 未来命令面

Order entry is intentionally out of MVP scope. It becomes eligible only after a separate command capability ADR/proposal defines:

1. `order_intent` contract;
2. pre-trade check and risk/approval owners;
3. Nautilus Paper executor as first execution gateway;
4. CTP/IB/stock execution gateway contracts;
5. execution event ledger;
6. Account Mirror readback and reconciliation rules;
7. UI authorization and forbidden-action acceptance.
8. account capability registry fields and blockers.

Until then, Account Console must not show submit, cancel, replace or broker action controls.
