---
status: accepted
owner: architecture
adr_id: "0004"
decision_status: accepted
landing_status: observation_only_in_progress
---

# ADR-0004: Adopt Account Capability Fabric With Mirror Readback / 采用带镜像回读的账户能力织构

- 日期：`2026-06-15`
- ADR 类型：standard
- 决策状态：accepted
- 落地状态：observation-only in progress via T001/P011
- 落地摘要：P011 has implemented account capability contracts, Account Mirror projection, source bridges, API-backed Account Workbench readback and command design gate; CTP `025292` real-account consistency remains blocked pending pinned source package.
- 覆盖摘要：observation-only layers L1-L4 have repo-local executable evidence; live command and CTP `025292` real-account consistency are not accepted.
- 适用范围：`nautilus_account_console` account capabilities, Account Mirror, future Command Plane boundary, multi-source account support
- 决策问题：Account Console 如何支持 Nautilus Paper Sandbox、CTP、IB TWS 与未来 stock accounts，同时不成为 broker/runtime truth writer，也不阻断未来 order entry？
- 当前倾向：采用 Account Capability Fabric；Account Mirror 只实现 read-only observation / reconciliation，未来 command 通过独立 Command Capability、risk/approval、Execution Gateway 与 mirror readback 闭环。
- 最终决策：accepted；采用 Account Capability Fabric with mirror readback，Account Mirror 保持 read-only，future command 通过独立 capability/gateway/readback 闭环。
- Architecture design anchor: [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)
- Acceptance anchor: [ADR-0004 Account Capability Fabric acceptance](../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md)
- Executable landing consistency gate: `python scripts\validate_adr004_p011_landing_consistency.py`
- Required document order: ADR-0004 -> architecture design -> acceptance -> T001 topic/roadmap -> proposal -> implementation

---

## 1. Problem Frame / 问题框架

Account Console 需要展示真实 operational accounts 的 account state，包括 balances、positions、orders、fills、settlement、equity、source health 与 evidence。目标 account source 至少覆盖：

1. Nautilus Paper Sandbox accounts。
2. CTP paper / live accounts，包括当前 paper account alias `19053`。
3. IB TWS paper / live accounts。
4. 未来 stock broker paper / live accounts。

现有 Account Workbench 已经通过 fixture-backed `acct.demo-19053` 证明 UI projection 可以工作，但 fixture projection 不能代表 live operation。项目需要一条路径，让 UI 能显示真实 account observation，同时保持仓库边界：Account Console 是 read-only projection / evidence surface，不是 runtime truth、broker truth、account truth、admission truth、approval truth、capital truth 或 trading-readiness truth 的 writer。

同一个架构也不能封死未来 order entry。未来可以有 submit / cancel / replace，但不能通过 Account Mirror 或 Account Console projection 直接 mutate broker/runtime state。Command 必须走独立 authority、risk/approval、Execution Gateway 与 mirror readback。

此外，账户能力不应只被拆成 “observation plane” 与 “command plane”。未来可能出现 allocation、funding transfer、borrow、hedging、rebalance、portfolio routing 或 broker-specific operational controls。若每个 concern 都新增一个 top-level plane，会形成 architecture sprawl。长期稳定抽象应是 Account Capability，而不是 broker type、route type 或 plane count。

### 1.1 Hard Constraints / 硬约束

1. Account Console UI 不得直接调用 CTP、IB TWS、stock broker 或 Nautilus runtime APIs。
2. Account Mirror 不得 send、cancel、replace、approve orders，也不得 allocate capital 或 certify trading readiness。
3. UI、API、ledger 与 evidence references 必须使用 namespace-qualified `account_id`；`19053` 只能作为 display alias。
4. 每个显示出的 balance、position、order、fill、settlement、equity 值必须带 source provenance，或显示 typed blocker。
5. Command-capable account 必须由 Capability Registry 明确声明，不得从 broker/account kind、route 或 UI state 推断。
6. Observation owner、command owner、risk/approval owner 与 UI owner 必须分离。

### 1.2 Explicit Non-Goals / 明确不做

1. 本 ADR 不实现 live broker connectivity 或 broker account truth。
2. 本 ADR 不接受 order-entry UI、submit/cancel/replace route 或 execution gateway implementation。
3. 本 ADR 不决定 admission、approval、capital allocation 或 trading readiness。
4. 本 ADR 不把 Account Mirror 升级为 command writer。
5. 本 ADR 不要求一次性落地 IB TWS、stock sources 或 live command capability。

### 1.3 Owner / Canonical Entry Impact

1. 新增 canonical architecture term：`Account Capability Fabric`。
2. `Account Mirror` 保持 read-only observed-account model / projection owner，不获得 broker/runtime write authority。
3. 未来 `Command Plane` / `Execution Gateway` 是独立 authority owner；本 ADR 只冻结边界，不指定最终 implementation owner。
4. `Capability Registry` 成为 UI 是否可展示 account-level state / action 的 projection contract，不是 broker truth 或 account truth。
5. 旧 fixture-only Account Workbench 不立即退役；它降级为 deterministic acceptance fixture，正式 real-account path 由 T001 承接。

### 1.4 概念判重 / Canonical Naming Check

| Candidate term | Layer / Owner | Existing nearby term | Collision risk | Decision | Guard / Evidence |
| --- | --- | --- | --- | --- | --- |
| `Account Capability Fabric` | architecture / account capability contract | Account Workbench, Account Mirror | AI 可能把它误读成 broker truth 或 runtime owner | 新增为 account-level permission / projection / evidence model | ADR-0004 + T001 capability registry gate |
| `Account Mirror` | read model / projection owner | fixture projection, Account Workbench | 可能被误用为 command writer | 保留为 read-only observation / reconciliation implementation | ADR0004-G02/G08/G09 |
| `Command Capability` | future command authority contract | order entry, broker action | 可能从 account type 推断 command ability | 只能由 Capability Registry 声明 | ADR0004-G03/G05/G06/G07 |
| `Mirror Readback` | reconciliation boundary | gateway response, button click | UI 可能把 gateway response 当 final account state | command status 必须通过 execution event + Account Mirror observation reconcile | ADR0004-G09 |
| `Typed Blocker` | projection / evidence state | hidden error, empty state | 缺证据时 UI 可能显示健康状态 | 缺 source/capability/risk/approval/readback 时 fail closed | ADR0004-G10 |

本 ADR 没有新增 lifecycle `status`、formal `verdict` 或 rule-family vocabulary；相关状态词仅在 account capability / projection owner 层内使用。

---

## 2. 与既有 ADR / Architecture 的关系 / Relationship To Existing Decisions

1. ADR-0002 决定 Account Console 的 product/navigation model：以 business workbench 组织 UI，artifact routes 作为 drill-down。
2. ADR-0003 决定 UI implementation decomposition：未来 UI 必须按 `Workbench -> Panel -> Read Model Contract -> Fixture -> UI Slice -> Acceptance` 切片。
3. 本 ADR 补充 account architecture：定义 Account Capability Fabric、Account Mirror read-only boundary、future Command Plane boundary 与 capability-gated UI 行为。
4. T001 Account Mirror Observation Plane 承接本 ADR 的 first implementation lane：先落 observation capability、canonical observations、Account Mirror projections 与 capability registry blockers。
5. [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md) 先把 implementation architecture、owner boundaries 与 source/API/UI contract shape 固定下来。
6. [ADR-0004 acceptance](../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md) 在 architecture design 之后承接 architecture-level Gates；真实 phase evidence 留在 T001 / proposal / child change，不复制进 ADR。

本 ADR 不替代 ADR-0002 / ADR-0003；它把 Account Workbench 下的 account state 与 future action authority 收敛为 capability-driven architecture。

---

## 3. 方案对比 / Options Comparison

本次对比不只比较“能否显示账户数据”，还比较 truth-source 分层、write-authority 边界、future command 扩展性、UI 分支成本、replay/testability 与治理成本。

| 方案 | 核心思路 | 适用场景 | 优点 | 缺点 / 风险 | 架构一致性 | 实施成本 | 结论 | 采纳与落地 / Decision + Landing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. UI calls broker APIs directly | React/FastAPI 直接调用 CTP、IB 或 stock APIs | 快速 demo | 路径最短 | UI/backend 变成 broker client 与第二 truth path；难审计、难 replay；未来 actions 不安全 | 低 | 低 | 拒绝 | rejected |
| B. Broker-specific adapters feed UI endpoints | `ctp/accounts`、`ib/accounts`、`stock/accounts` 分别供 UI | broker 数量少、短期清晰 | source 名称直接 | UI 累积 broker branches；Nautilus Paper / replay / fixtures 难统一；cross-source tests 弱 | 中低 | 中 | 拒绝 | rejected |
| C. Normalized broker adapter layer | broker adapters 写 shared account snapshot model | 只做 broker normalization | 比 B 更可复用 | 仍以 broker 为中心；Nautilus Paper、replay、fixtures 特殊化；command path 容易后补 | 中 | 中 | 拒绝为不完整 | rejected as incomplete |
| D. Account Mirror observation plane | source emits canonical observations into mirror ledger/projections | observation-only MVP | source-neutral；支持 replay / fixtures / provenance | 架构中心仍是 observation；future command/allocation/funding 容易外接不均 | 中高 | 中高 | 作为 implementation component 采纳 | accepted as component |
| E. Account Mirror also sends orders | Mirror 同时读写 account state 与 orders | 想减少概念数 | 概念少 | 混合 observation 与 mutation；UI projection 可能变成 trading authority | 低 | 中 | 拒绝 | rejected |
| F. Separate observation plane and command plane | Mirror read-only；order intent 走 checks、approval/risk、Execution Gateway | 未来 order entry | authority split 清晰；Mirror 可做 readback | 模块与 contracts 更多 | 高 | 高 | 采纳为边界 | accepted |
| G. Account Capability Fabric with mirror readback | account identity 绑定 observation、command、risk/approval、reconciliation、evidence capabilities | 长期 multi-source account architecture | 可扩展；UI registry-driven；Mirror read-only；新行为不必新增 top-level plane | 需要 capability contracts 与 gate discipline | 高 | 高 | 推荐 | accepted as top-level decision |

### 3.1 Landing Evidence / 落地证据

| 方案 | decision_state | landing_state | evidence_state | evidence_ref | residual_risk |
| --- | --- | --- | --- | --- | --- |
| A | rejected | rejected_not_applicable | not_applicable | ADR-0004 Section 3 | 无 |
| B | rejected | rejected_not_applicable | not_applicable | ADR-0004 Section 3 | 无 |
| C | rejected | rejected_not_applicable | not_applicable | ADR-0004 Section 3 | 无 |
| D | included | observation_only_implemented | executable_evidence | P011 phases 1-5 + UI readback evidence | CTP `025292` real consistency still needs pinned source package |
| E | rejected | rejected_not_applicable | not_applicable | ADR0004-G08/G09 negative acceptance | 无 |
| F | included | design_gate_only | executable_design_evidence | P011 phase 7 + future command proposal required | command owner / gateway / risk approval implementation 未落地 |
| G | accepted | observation_only_in_progress | executable_evidence | ADR acceptance + T001 + P011 gates | live command capability and CTP `025292` real consistency 未落地 |

### 3.2 取舍说明 / Trade-Off Notes

1. A/B/C 可以更快演示，但都会让 UI 或 broker adapter 形成第二 truth path，因此不能作为长期正式路径。
2. D 是首个 implementation component，但不是顶层架构；observation-only 不能表达 future command、risk/approval、reconciliation 与 evidence owner。
3. E 明确拒绝，因为它会把 Account Mirror 从 read model 推向 execution authority。
4. F 保留为 future command boundary，但必须被 G 的 Capability Registry 管住，避免 plane count 继续膨胀。
5. G 的成本更高，但能把新 account behavior 收敛到 capability model，而不是 broker-specific UI branches。

---

## 4. 决策 / Decision

### 4.1 决策结论 / Decision Summary

1. 采用 `Account Capability Fabric` 作为 account-level permission、projection 与 evidence model。
2. `Account Identity` 是稳定 identity；`Capability` 表达系统可对该 identity 做什么；`Projection` 表达 UI 可显示什么；`Command` 表达授权 gateway 可尝试什么；`Evidence` 表达为什么相信或阻断。
3. `Account Mirror` 只实现 observation / reconciliation capabilities，不作为 order writer、approval owner、capital owner 或 readiness owner。
4. 未来 order entry 必须通过 `Command Capability -> Order Intent -> Risk / Approval -> Execution Gateway -> Execution Event -> Account Mirror Readback -> Reconciliation`。
5. Account Mirror observation freshness 支持 `snapshot`、`polling` 与 `event_driven` 三种长期模式；UI freshness claims 必须来自 Mirror projection，不得绕过 Mirror 直连 source。
6. 拒绝 UI direct broker APIs、broker-specific UI endpoints、Account Mirror sends orders，以及从 broker/account kind 推断 command ability。

### 4.2 决策边界 / Decision Boundaries

1. Broker/runtime/account truth 仍归 source system；Account Console 只消费 observation / projection / evidence。
2. Account Mirror 可以 ingest permitted observations、produce projections、report staleness/lag/checksum/source health 与 typed blockers。
3. Account Mirror 不得 mutate broker/runtime state，不得 submit/cancel/replace orders，不得 approve trading，不得 allocate capital。
4. Capability Registry 不是 broker truth；它是 authorization/projection contract，用来告诉 UI 哪些 state/action surface 可出现，以及需要哪些 readback evidence。
5. Command-capable account 必须同时保留 observation 与 command owner separation。
6. Live command capability 必须 fail closed：authority、risk、approval、session state 或 readback reconciliation evidence 缺失时不得显示可执行 action。
7. Snapshot-only implementations must expose `observation_mode=snapshot` and must not claim realtime order/trade behavior.
8. Polling or event-driven freshness must still flow through Account Mirror; Account Console UI and API must not bypass Mirror for fresher broker state.
9. Realtime UI claims require accepted event-driven observation contracts, lag metrics and reconciliation blockers.

### 4.3 Design Kernel / 设计内核

Account Capability Fabric 的稳定结构：

```text
Account Identity
        |
        v
Account Capability Registry
        |
        +-- Observation Capability
        |     -> Account Observation Sources
        |     -> Account Mirror
        |     -> balances / positions / orders / fills
        |
        +-- Command Capability
        |     -> order intent
        |     -> execution gateway
        |
        +-- Risk / Approval Capability
        |     -> pre-trade checks
        |     -> authorization evidence
        |
        +-- Reconciliation Capability
        |     -> execution event + mirror readback
        |     -> mismatch blockers
        |
        +-- Evidence Capability
              -> source refs
              -> checksums
              -> typed blockers
```

Account Mirror observation flow：

```text
Account Observation Sources
  - nautilus.paper
  - ctp.paper / ctp.live
  - ib.paper / ib.live
  - stock.paper / stock.live
  - replay / deterministic fixtures
        |
        v
Account Mirror Ingest
        |
        v
Canonical Account Observation Ledger
        |
        v
Account Projection Store
        |
        v
Account Console API / UI
```

Observation freshness is an Account Mirror concern：

```text
snapshot
  -> pinned read-only source package
  -> Account Mirror checkpoint
  -> UI consistency against checkpoint

polling
  -> repeated read-only source packages
  -> newer Account Mirror checkpoints
  -> UI refresh with declared lag/staleness

event_driven
  -> source event observations, for example CTP OnRtnOrder / OnRtnTrade
  -> Account Mirror projection
  -> reconciliation with query/readback evidence
  -> UI freshness claim with lag metrics
```

Stable freshness fields：

```text
observation_mode = snapshot | polling | event_driven
event_stream = not_implemented | connected | disconnected | blocked
source_observed_at
source_received_at
projected_at
ui_seen_at
source_lag_ms
projection_lag_ms
reconciliation_state
```

`snapshot` is sufficient for first read-only real-account consistency. `polling` and `event_driven` are future freshness upgrades and must be accepted by successor proposal evidence before UI copy or tests claim realtime behavior.

Future command flow：

```text
Order Intent UI or Strategy
        |
        v
Order Intent Contract
        |
        v
Pre-trade Checks / Risk / Approval
        |
        v
Execution Gateway
  - Nautilus Paper executor
  - CTP executor
  - IB TWS executor
  - Stock executor
        |
        v
Broker/runtime execution
        |
        v
Account Mirror observes readback and reconciliation
```

Canonical account IDs：

```text
acct.nautilus.paper.<account>
acct.ctp.paper.<account>
acct.ctp.live.<account>
acct.ib.paper.<account>
acct.ib.live.<account>
acct.stock.paper.<broker>.<account>
acct.stock.live.<broker>.<account>
```

Source fields 必须显式建模，避免 broker-specific UI branches：

```text
source_kind = nautilus_paper_runtime | ctp_trader_api | ib_tws | stock_broker_api | replay_file | deterministic_fixture
source_mode = live_observation | delayed_snapshot | replay | deterministic_fixture
account_domain = sandbox | paper | live | backtest
```

Capability Registry 最小字段形态：

```text
account_id
observation.enabled
observation.source_kind
observation.mirror_state
reconciliation.enabled
evidence.required
command.enabled
command.mode = disabled | paper | live
command.gateway_kind = nautilus_paper | ctp | ib_tws | stock
command.allowed_actions = submit | cancel | replace
command.requires_risk_check
command.requires_approval
command.authority_ref
command.capability_checksum
```

### 4.4 推荐产物 / Recommended Deliverables

1. Canonical account observation contracts：balance、position、order、fill、settlement、equity、source health 与 typed blocker。
2. Account Mirror ledger / projection contracts 与 checksum / staleness fields。
3. Observation freshness fields for snapshot, polling and event-driven modes.
4. Capability Registry contract 与 deterministic fixtures。
5. Account Console API read-only endpoints：

```text
GET /api/accounts
GET /api/accounts/{account_id}
GET /api/accounts/{account_id}/balances
GET /api/accounts/{account_id}/positions
GET /api/accounts/{account_id}/orders
GET /api/accounts/{account_id}/fills
GET /api/accounts/{account_id}/settlement
GET /api/accounts/{account_id}/equity
GET /api/accounts/{account_id}/evidence
GET /api/accounts/{account_id}/source-health
```

6. Account Workbench panels 显示 source refs、checksums、observed timestamps、staleness、observation mode 与 typed blockers。
7. Future command proposal：定义 Order Intent、risk/approval owner、Execution Gateway、execution event、mirror readback 与 UI authorization boundary。
8. Focused contract / fixture / backend / browser tests 对齐 ADR0004 Gates。

### 4.5 决策覆盖与落地矩阵 / Decision Coverage And Landing Matrix

| 决策项 | 必须覆盖的落点 | 覆盖状态 | 承接 proposal / change | executable evidence | docs evidence | 剩余缺口 |
| --- | --- | --- | --- | --- | --- | --- |
| D1. Canonical account identity | contract / API / UI / evidence | passed_for_observation_only | P011 phases 1-4 | `validate_account_capability_contracts.py`, `validate_account_mirror_api.py`, Playwright UI readback | CTP `025292` real package still blocked |
| D2. Observation provenance | contract / projector / UI | passed_for_observation_only | P011 phases 1-5 | `validate_account_mirror_projection.py`, `validate_account_source_bridges.py`, `validate_p011_ui_readback_evidence.py` | broker/runtime truth not claimed |
| D3. Account Mirror read-only boundary | owner / backend / UI | passed_for_observation_only | T001 + P011 + owner boundary gate | `validate_owner_boundaries.py`, backend tests, no command controls in Playwright | future command owner remains separate |
| D4. Capability Registry | contract / fixture / API / UI | passed_for_observation_only | P011 phases 1 and 4 | capability fixtures, mirror API payloads, UI command-disabled assertions | paper/live command not accepted |
| D5. Command Capability separated from observation | future command contract / owner | passed_design_gate_only | P011 phase 7; future command-plane proposal still required | `validate_command_capability_design_gate.py` | no submit/cancel/replace implementation accepted |
| D6. Fail-closed blockers | contract / UI / acceptance | passed_for_observation_only | P011 phase 5 + CTP `025292` blocker | `validate_account_source_health_evidence.py`, blocked 025292 UI screenshots | CTP `025292` real consistency remains blocked |
| D7. Capability Fabric extension rule | architecture / docs / review gate | passed_for_observation_only | T001 + P011 proposal docs | `check_proposal_docs.py`, `validate_owner_boundaries.py` | future new behavior needs accepted capability |
| D8. Observation freshness modes | contract / projector / UI source health | snapshot_only_started | T001 + P011 phases | source health/evidence fields and blocked source acceptance | polling/event-driven not accepted |

---

## 5. Landing Map / 落地映射

本 ADR 只表达 architecture rollout shape；实时 phase 状态以 T001、successor proposal、child change 与 acceptance evidence 为准。

Required landing document order:

```text
ADR-0004
  -> Account Capability Fabric architecture design
  -> ADR-0004 Account Capability Fabric acceptance
  -> T001 topic / roadmap
  -> scoped proposal
  -> implementation
```

Architecture design must be reviewed before any successor proposal implementation starts. Acceptance Gates validate both this ADR and the architecture design; they are not a substitute for the design.

### 5.0 Accepted Decision Boundary / 已接受决策边界

（待决策后填写）

若本 ADR 被 accepted，接受范围应限于：

1. Account Capability Fabric 作为长期 account capability abstraction。
2. Account Mirror read-only observation / reconciliation boundary。
3. Capability Registry 作为 UI state/action eligibility contract。
4. Future command 通过 independent Command Capability、risk/approval、Execution Gateway 与 mirror readback 闭环。

### 5.0.1 Not Accepted By This ADR / 本 ADR 不接受

1. 不接受 Account Console 或 Account Mirror 成为 broker/runtime/account truth writer。
2. 不接受 UI direct broker APIs。
3. 不接受从 broker/account kind 推断 command ability。
4. 不接受在本 ADR 中落地 order-entry implementation。
5. 不接受把 readiness、admission、capital allocation 或 tradability claim 显示为 Account Console truth。

### 5.0.2 Successor Proposal Boundary / 后续 Proposal 边界

| Phase | 目标 | 承接 proposal / change | 退出条件 | retirement 影响 | 承接状态 / Landing Status |
| --- | --- | --- | --- | --- | --- |
| Phase 0 | 冻结 ADR、architecture design 与 acceptance gates | ADR-0004 + architecture design + acceptance doc | ADR accepted, architecture design reviewed and linked from ADR index | 无 | ADR/design planned |
| Phase 1 | canonical observation contracts | T001 M1 | balance/position/source health contracts exist | fixture-only path begins downgrade | planned via T001 |
| Phase 2 | Nautilus Paper + CTP Paper `19053` observation | T001 M2-M3 | two account IDs render from API-backed projections with provenance | demo-only account alias must not be canonical | planned via T001 |
| Phase 3 | Account Mirror projection store and source health | T001 M4-M6 | replay/checksum/staleness/blocker evidence exists | stale hidden-success behavior retired | planned via T001 |
| Phase 4 | Capability Registry | T001 M9 | observation/command capability fixtures and API projections exist | command inferred from type/route retired | planned via T001 |
| Phase 5 | Observation freshness upgrades | T001 / P011 successor phases | snapshot/polling/event-driven fields and acceptance evidence exist | realtime wording without event evidence retired | planned via T001 |
| Phase 6 | Future command architecture | future command-plane ADR/proposal | order intent, risk/approval, gateway and readback contracts accepted | no command UI before acceptance | future extension |
| Final | docs and fixture closure | successor closeout | ADR index, topic, owner map and tests aligned | fixture-only real-account narrative retired | planned |

### 5.1 旧代码退役与文档收口 / Legacy Retirement And Documentation Closure

| 旧项 / 路径 | 当前职责 | 新归宿 / 替代物 | 处理动作 | 暂留边界 | 最终移除条件 | 文档同步项 | 承接状态 / Landing Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fixture-only Account Workbench real-account narrative | 用 deterministic fixture 证明 account UI | API-backed Account Mirror projections + deterministic fixtures for acceptance | 降级为 acceptance fixture，不作为 real account truth | 可继续用于 deterministic UI tests | T001 API-backed projections verified | ADR-0003, T001, acceptance docs | planned via T001 |
| bare alias `19053` as identity | 人类可读 account alias | `acct.ctp.paper.19053` canonical ID + display alias | 禁止作为 canonical identity | 只允许 display label | identity tests verified | ADR0004-G01 | planned via T001 |
| broker-specific UI branching | 可能直接按 CTP/IB/stock 分支渲染 | source_kind/source_mode + canonical projections | 不进入正式路径 | 无 | capability/projection tests verified | ADR0004-G02/G04 | planned via T001 |

---

## 6. Acceptance And Evidence / 验收与证据

### 6.0 ADR-Level Acceptance Only / 仅限 ADR 级验收

本 ADR 的 acceptance 只证明 architecture conformance，不证明 live broker connectivity、order entry、capital allocation、approval 或 trading readiness。任何 phase claiming ADR-0004 coverage 必须把真实命令、artifact path、run id、browser screenshot 与 closeout evidence 写入 successor proposal / child change acceptance。

### 6.1 通用验收纪律 / General Acceptance Rules

1. 每个 child change 在声明 Gate pass 前，必须先补对应 focused contract / fixture / backend / browser check。
2. 缺 source、缺 capability、stale source、risk/approval missing 或 readback mismatch 必须产生 typed blocker。
3. 不得以手工点页面、口头判断或临时截图替代正式验收。
4. Browser screenshot 只能证明 rendering，不证明 broker/account truth。
5. Command controls 不得在 validated Capability Registry entry 缺失时出现。

### 6.2 Successor Proposal Acceptance Scenario Requirements / 后续 Proposal 验收场景要求

| ADR decision item | Required acceptance scenario | Positive path | Must fail if | Authority / retirement boundary | Minimal evidence |
| --- | --- | --- | --- | --- | --- |
| D1. Canonical account identity | namespace-qualified account identity | API/fixture uses `acct.ctp.paper.19053` with alias `19053` | bare `19053` is canonical identity | Account Console owns display projection only | focused contract/fixture test |
| D2. Observation provenance | every displayed value has provenance | balance/position payload includes `source_ref`, `observed_at`, checksum or blocker | UI renders live-looking value without provenance | source remains external truth owner | contract + browser evidence |
| D3. Account Mirror read-only boundary | Mirror cannot become writer | Mirror only ingests observations and projects read models | Mirror sends/cancels/replaces/approves | command owner is separate | negative test or owner boundary gate |
| D4. Capability Registry | UI state/action eligibility is explicit | account payload declares observation/command/reconciliation/evidence capabilities | UI infers command from broker/account kind | registry is projection contract, not broker truth | schema + fixture + UI test |
| D5. Command separated from observation | future order entry uses command path | order intent -> risk/approval -> gateway -> event -> mirror readback | gateway response or button click is final account state | Execution Gateway owns attempt; Mirror owns readback | future command proposal evidence |
| D6. Fail-closed blockers | missing evidence blocks or hides action | stale source/capability missing/risk missing shows typed blocker | UI silently hides evidence or shows success | no fallback truth writer | blocker fixture + browser test |
| D7. Capability Fabric extension rule | new behavior maps to accepted capability | proposal names capability owner and evidence | new top-level plane or broker-specific UI branch appears | ADR/proposal must accept new capability | docs gate or focused review check |
| D8. Observation freshness modes | UI freshness claim maps to Mirror mode | snapshot shows checkpoint; polling/event-driven show lag and reconciliation fields | UI claims realtime from snapshot or direct broker path | Account Mirror owns freshness projection | successor proposal contract + browser/API evidence |

### 6.3 Architecture-Level Acceptance / 架构级验收

1. D1-D4 与 D6 至少进入 `verified`，才能称 observation-only Account Mirror MVP 架构落地。
2. D5 必须由 future command-plane ADR/proposal 验证后，任何 submit/cancel/replace UI 才能出现。
3. D7 必须成为 review/gate 纪律，确保未来 allocation、funding、borrow、hedging、rebalance 等行为以 capability extension 进入，而不是新增 ad hoc plane。
4. D8 必须确保 freshness claim 不绕过 Account Mirror；snapshot-only implementation 不得声称 realtime。
5. ADR closeout 不复制 successor proposal 的 acceptance 明细，只沉淀稳定 owner boundary、canonical entries 与 retired legacy narratives。

### 6.4 ADR Closeout Distillation / ADR closeout 沉淀

（closeout 后回填）

| Distillation target | Stable conclusion distilled from this ADR | Source proposal / change / evidence | Do not copy forward | Closeout action |
| --- | --- | --- | --- | --- |
| `docs/adr/README.md` | ADR-0004 binding rule and status | ADR-0004 + T001 closeout | phase evidence and screenshots | update index |
| `docs/topics/T001-account-mirror-observation-plane.md` | observed-account implementation boundary | T001 acceptance | temporary logs/artifacts | update topic if scope changes |
| `docs/ownership/account-console-owner-map.md` | observation / command / risk / UI owner separation | successor proposal evidence | command outputs | update owner map when owners are concrete |

---

## 7. 关联文档 / Related Documents

1. [ADR-0002 Business workbench first account console navigation](0002-adopt-business-workbench-first-account-console-navigation.md)
2. [ADR-0003 Contract-first UI slice development](0003-adopt-contract-first-ui-slice-development.md)
3. [ADR-0004 Account Capability Fabric acceptance](../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md)
4. [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
5. [T001 Account Capability Feature Roadmap](../topics/roadmap/T001-account-capability-feature-roadmap.md)
6. [Account Console owner map](../ownership/account-console-owner-map.md)
7. [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)

---

## Optional Fragments / 可选片段

### A. Red Lines

1. Account Console UI must not call broker APIs directly。
2. Account Mirror must not send、cancel、replace、approve orders or allocate capital。
3. `19053` must not be used as canonical `account_id`。
4. Command controls must not render without validated Capability Registry evidence。
5. Gateway response or button click must not be treated as final account state。
6. Missing source, stale source, missing capability, failed risk, missing approval or reconciliation mismatch must fail closed through typed blocker。
