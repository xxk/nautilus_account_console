---
status: accepted
owner: architecture
adr_id: "0005"
decision_status: accepted
landing_status: foundation_accepted
---

# ADR-0005: Account Console Independent Broker Observation Sessions / Account Console 独立 Broker 观测会话

- 日期：`2026-06-20`
- ADR 类型：standard
- 决策状态：accepted
- 落地状态：foundation_accepted via P019
- 落地摘要：ADR-0005 accepts governed read-only broker observation sessions as an Account Console capability owner, with command, broker truth, account truth, secret and screenshot boundaries enforced by P019 contract/API/browser/runtime gates.
- 覆盖摘要：decision 6/6, implementation foundation 12/12, retirement 2/2; real U3028269 funds/positions parity is ready, while real order/fill report-row parity remains typed partial because the same-slice read-only `reqExecutions` query returned zero execution rows.
- 适用范围：`nautilus_account_console` Account Capability Fabric, Account Mirror, CTP / IB TWS / stock / CQG / TT broker account observation, Nautilus-compatible order/fill reports, high-frequency test observation
- 决策问题：Account Console 是否可以拥有独立 broker 观测会话，以便在高频测试期间观测 CTP、IB TWS、股票、CQG、TT 等账户，同时不成为第二个交易执行 owner？
- 当前倾向：accepted；Account Console may own governed read-only broker observation sessions, with broker-specific profiles, Nautilus-compatible order/fill reports, explicit session conflict policy, durable observation store and Account Mirror projection boundary.
- 最终决策：accepted；采用 Option C as the first local capability owner, while rejecting direct full broker clients and preserving Nautilus/future Execution Gateway as command owner.
- Acceptance anchor: [ADR-0005 Broker Observation Session acceptance closeout](../acceptance/2026-06-20-adr0005-broker-observation-session-acceptance.json)
- Executable landing consistency gate: `python scripts\validate_adr0005_acceptance.py`
- Required document order: ADR-0005 -> P019 successor proposal -> contract/API/browser/runtime gates -> acceptance closeout

---

## 1. Problem Frame / 问题框架

Account Console 当前定位是 read-only observation console。ADR-0004 已接受 Account Capability Fabric with mirror readback，并明确 Account Mirror 保持 observation-only，future command 必须通过独立 Command Capability、risk/approval、Execution Gateway 与 mirror readback 闭环。

新的触发场景是：在高频测试或实时运维观测中，仅依赖 Nautilus Trader / execution runtime 的投影可能不足以满足 operator 对账户状态、订单状态、成交回报、连接健康、延迟与 staleness 的直接观察需求。用户希望 Account Console 对 CTP、IB TWS / IB Gateway 以及未来股票、CQG、TT 等接入具备自己的登录或连接能力，用于独立观测账户。

独立观测不仅要显示当前订单行，还必须记录每个收到的 broker order callback / order status / fill callback 对应的 order report。该 report 的 canonical shape 必须与 Nautilus `OrderStatusReport` / `FillReport` 对齐，Account Console 只消费 normalized report 和 provenance refs；broker raw payload 只能作为 evidence / debug drill-down，不能成为 browser 或 UI projection 的 order truth。

Broker order/fill reports also require durable local maintenance. Some brokers or gateways may only replay order reports at session startup, or may provide incomplete historical replay after disconnect. If Account Console observes a report and then loses it from memory, post-session review, reconciliation and incident analysis become unreliable. ADR-0005 therefore requires a local durable observation store for normalized reports, source snapshots and provenance metadata. This store is an observation/evidence store, not broker truth and not execution authority.

这里的核心矛盾不是“能不能登录 broker”，而是“登录或连接 broker 后 Account Console 是否会变成第二个 broker runtime / execution owner”。CTP TD、IB TWS API、stock broker API、CQG/TT gateway 通常都同时具备查询与交易能力。若 Account Console 直接获得无约束 broker client 能力，会与 Nautilus Trader 的 execution authority、session ownership、order lifecycle truth 和 Account Mirror projection boundary 发生冲突。

本 ADR 只比较长期架构方案，不实现 broker 连接，不保存 CTP/IB/stock/CQG/TT username/password/2FA/auth code/front address/API key 等敏感材料，不创建或复制任何 secret-bearing config。

### 1.1 Hard Constraints / 硬约束

1. Account Console 不得保存或成为 CTP/IB/stock/CQG/TT raw password、2FA、auth code、front address、API key、broker secret、account secret 的 owner；任何本地 profile 只能记录 redacted alias、secret ref、config ref、session ref 或 operator-provided local endpoint ref。
2. Account Console 的独立 broker 能力若被接受，第一阶段只能是 read-only observation capability，不得调用 `placeOrder`、`cancelOrder`、order modify、CTP order insert/action 或任何 broker mutation API。
3. Nautilus Trader / execution gateway 仍是 order submit、cancel、replace、execution lifecycle 的 owner；Account Console 不得通过 TWS connectivity 推断 command capability。
4. Broker session conflict 必须 fail closed：同一 broker username/session、同一 host/port/clientId/front/session slot、未知 session owner 或 Nautilus trading session 冲突时，不得静默抢占或降级。
5. 所有 UI 展示必须通过 Account Mirror / typed projection / source provenance 暴露，不能把 browser snapshot 当作 broker truth。
6. 高频观测需要显式 lag / freshness / event sequence / source health 字段；不能用“页面刷新成功”代表实时账户真值。
7. 每个收到的 broker order callback / trade callback 必须写入 normalized order report artifact；report 字段语义必须对齐 Nautilus `OrderStatusReport` / `FillReport`，至少覆盖 `account_id`、`instrument_id`、`client_order_id`、`venue_order_id`、side、order type、time in force、status、quantity、filled quantity、price/avg price、report id、event timestamps、cancel/reject reason、trade id、last price/quantity、commission/liquidity side where applicable。
8. Account Console 不得发明 broker-specific order report schema 作为正式 truth；CTP、IB、stock、CQG、TT 的原始回报只能映射为 Nautilus-compatible report plus raw payload provenance。
9. Account Console 必须维护 durable local observation store：observed order status reports、fill reports、account/funds snapshots、positions snapshots、session health、freshness cursors 和 provenance refs 必须可在重启后用于回放、盘后复盘、reconciliation 和 evidence drill-down。
10. Durable observation store 不得被提升为 broker/account/order truth writer；它只能声明 `observed_by_account_console` / `projection_cache` / `evidence_store` 语义，并必须保留 source timestamps、received timestamps、projection timestamps、checksums 和 replay gap blockers。

### 1.2 Explicit Non-Goals / 明确不做

1. 本 ADR 不接受 Account Console 下单、撤单、改单或成为 execution owner。
2. 本 ADR 不决定 broker credential 管理、2FA 自动化、CTP front discovery、TWS/IB Gateway launcher、CQG/TT gateway launcher 或 stock broker OAuth/API-key rotation 细节。
3. 本 ADR 不替代 Nautilus Trader 的 IB adapter / execution adapter / strategy runtime。
4. 本 ADR 不承诺 live trading readiness、capital approval、risk approval 或 production admission。
5. 本 ADR 不逐一实现 CTP、IB、股票、CQG、TT 连接；它只决定这些接入是否共用同一个 broker observation session 架构。

### 1.3 Owner / Canonical Entry Impact

1. 可能新增 canonical owner：`account-console-broker-observation-session`，仅限 read-only broker observation session lifecycle。
2. 可能新增 canonical source kinds：`ctp_observation`、`ib_tws_observation`、`stock_broker_observation`、`cqg_observation`、`tt_observation`，用于 Account Capability / Account Mirror projection，不代表 command authority。
3. 可能新增 backend public entries：broker session health、connect/disconnect request、read-only account snapshot、event stream；这些 entry 不得暴露 order mutation。
4. 需要收紧旧表述：ADR-0004 中 “Account Console UI 不得直接调用 CTP、IB TWS、stock broker APIs” 可能需要具体化为 “UI 不得直接调用；backend may own governed read-only broker observation sessions if this ADR is accepted”。
5. 可能新增 canonical artifact family：`nautilus_order_status_report` / `nautilus_fill_report` compatible projections，作为 broker observation sessions 输出到 Account Mirror 的 order report contract。
6. 可能新增 canonical local store：`broker_observation_store`，用于持久化 normalized reports、snapshots、session events、provenance refs 和 replay/gap markers。
7. 若本 ADR accepted，必须由 successor proposal 更新 owner map、capability bundle schema、backend API contracts、frontend session UI、order report contracts、durable observation store contracts 和 negative tests。

### 1.4 概念判重 / Canonical Naming Check

| Candidate term | Layer / Owner | Existing nearby term | Collision risk | Decision | Guard / Evidence |
| --- | --- | --- | --- | --- | --- |
| `Broker Observation Session` | broker observation runtime / Account Console backend | Account Mirror observation capability, source bridge | AI may treat observation session as broker truth or execution authority | proposed new owner-local term; read-only only | successor contract lock must reject command mutation |
| `Independent TWS Observation Session` | IB/TWS-specific broker observation profile | IB TWS account source, Account Capability Fabric | May be confused with independent trading login | proposed term; must include `observation` and `read_only` in contract shape | profile schema and UI copy must show command disabled |
| `Independent CTP Observation Session` | CTP-specific broker observation profile | CTP source package, CTP TD/MD runtime | May be confused with CTP order-capable TD owner | proposed term; TD/MD observation only unless future command ADR accepts mutation | profile schema must record secret/config refs only |
| `Broker Observation Profile` | source profile contract | Account Capability bundle, source bridge | Broker-specific config may leak into UI/projection truth | proposed shared abstraction for CTP/IB/stock/CQG/TT | schema must require source_kind, account_id, session_owner and secret refs |
| `Nautilus-Compatible Order Report` | order observation artifact / Account Mirror input | Nautilus `OrderStatusReport`, `FillReport`, current order report provenance refs | Broker-specific callbacks may create parallel report semantics | proposed canonical report shape for all observed broker order/fill callbacks | contract tests must reject broker-specific report truth without Nautilus-compatible mapping |
| `Raw Broker Order Payload` | provenance / evidence only | report_msg_ref, report_msg_checksum, raw payload drill-down | UI may parse raw callback as order truth | legacy/evidence-only; never canonical order truth | browser and backend tests must consume normalized report first |
| `Broker Observation Store` | durable local observation/evidence store | Account Mirror projection cache, order report provenance, hot path ledger primitives | AI may treat local store as broker/order truth writer | proposed durable observation store; replay/cache/evidence only | tests must reject truth/readiness claims from local store alone |
| `Session Conflict Policy` | runtime safety / admission guard | Capability Registry blocker, source health blocker | May silently downgrade to shared session without operator awareness | proposed required contract section | tests must cover same username/clientId/session-owner conflict blockers |
| `Observation Gateway` | backend facade / projection source | Execution Gateway | May be mistaken for command gateway | proposed only if implemented; explicitly not execution gateway | naming guard: no order mutation methods exposed |
| `TWS Login` | operator-facing phrase | TWS API connection, IBKR brokerage session | Users may expect Account Console to own username/password login | avoid as canonical term; use `TWS observation profile` and `API session` | docs must distinguish operator login, TWS API connection, broker credentials |

---

## 2. 与既有 ADR / Architecture 的关系 / Relationship To Existing Decisions

1. ADR-0002 remains valid: Account Console navigation stays business-workbench-first; broker observation should surface under Account Workbench / Stream Ops / Intraday Monitor, not as a parallel broker-specific app.
2. ADR-0003 remains valid: any UI work must be contract-first panel slice development.
3. ADR-0004 remains valid: Account Capability Fabric and Account Mirror readback remain the top-level account architecture; this ADR is a supplement that decides whether Account Console may own a governed broker observation session feeding that fabric.
4. This ADR does not supersede the command boundary in ADR-0004. Even if independent broker observation is accepted, command capability remains separate and disabled until a future command ADR/proposal accepts it.
5. Current owner map says Account Console must not become runtime truth, broker truth, account truth, admission truth, approval truth, capital truth or trading-readiness writer. This ADR can only add a read-only observation session owner if the owner map is updated with explicit anti-second-implementation rules.
6. Existing CTP real-account consistency work remains source-package / mirror-projection based and blocked without pinned source evidence until a CTP observation profile/proposal accepts a governed read-only path. This ADR can include CTP as a broker observation source but does not authorize CTP direct command or direct broker truth writing.

---

## 3. 方案对比 / Options Comparison

本次对比不只比较“Account Console 能不能看到 broker 账户”，还比较 session ownership、Nautilus execution isolation、truth-source 分层、高频观测能力、operator ergonomics、secret boundary、future CTP/IB/stock/CQG/TT 扩展性、future command 扩展性与治理成本。

| 方案 | 核心思路 | 适用场景 | 优点 | 缺点 / 风险 | 架构一致性 | 实施成本 | 结论 | 采纳与落地 / Decision + Landing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Keep Account Console projection-only | Account Console 只读 Nautilus / source package / Account Mirror 投影，不拥有任何 broker session | 最保守的 read-only dashboard；Nautilus 已提供足够观测 | 不新增 broker session owner；最符合现有 ADR-0004 原文 | 高频测试时观测链路依赖 Nautilus；无法独立验证 broker account state；operator 排障能力弱 | 高 | 低 | 评审中 | possible rejected or baseline |
| B. Share Nautilus broker session | Nautilus owns CTP/IB/stock/CQG/TT trading session; Account Console 通过 Nautilus telemetry / local API 读取 | broker 只允许一条 session；必须避免并发登录 | 不抢 broker session；order lifecycle 单 owner | Account Console 不是真正独立观测；Nautilus 故障时观测也丢失；高频观测受 execution runtime API 限制 | 中高 | 中 | 评审中 | possible included as fallback |
| C. Independent read-only broker observation sessions | Account Console backend 连接 dedicated broker observation endpoints，用 broker-specific profile 做只读观测；order/fill callbacks 归一成 Nautilus-compatible reports，写入 durable observation store，再投影到 Account Mirror | 高频测试、operator 需要独立账户观测；CTP/IB/stock/CQG/TT 都需要可扩展接入；盘后复盘需要本地 report/snapshot 历史 | 独立观测能力强；可采集 health/lag/events/order reports；可盘后复盘；不依赖 Nautilus telemetry；新增 broker 只扩 profile/adapter/mapper | 需要 per-broker session conflict policy；并发登录限制复杂；必须严禁 order mutation；report mapper 必须严格对齐 Nautilus；local store 不能漂成 truth writer | 高 | 高 | 采纳 | accepted |
| D. Account Console direct full broker clients | Account Console 直接成为完整 CTP/IB/stock/CQG/TT client，读写都可做 | 想快速实现“登录+下单+观测”一体 | 短期功能完整 | 直接成为第二 execution owner；与 ADR-0004 冲突；抢 session/order lifecycle；高风险 | 低 | 中 | 拒绝候选 | rejected if decision accepts current boundaries |
| E. External Observation Gateway service | 单独服务拥有 broker observation sessions，Account Console 只连该服务；Nautilus 也可消费 | 多 broker、多语言、高频观测集中治理 | owner 分离清晰；可独立扩缩容；Account Console 不直接连 broker | 新服务治理成本高；初期链路更长；需要跨 repo owner | 高 | 高 | 未来扩展候选 | future extension |
| F. Manual operator broker console only | 人工打开 TWS/CTP terminal/stock/CQG/TT UI 观察，Account Console 不接 broker | 极早期或无法授权开发时 | 零开发；无 session API 风险 | 无结构化证据、无 lag metrics、无法自动验收、无法接 Account Mirror | 低 | 低 | 拒绝长期方案 | manual-only fallback |

### 3.1 Landing Evidence / 落地证据

| 方案 | decision_state | landing_state | evidence_state | evidence_ref | residual_risk |
| --- | --- | --- | --- | --- | --- |
| A | included | partially_implemented | docs_only | ADR-0004; owner map projection-only boundary | 高频独立观测不足 |
| B | future | not_implemented | missing_evidence | no accepted Nautilus telemetry bridge in Account Console yet | Nautilus failure couples observation failure |
| C | accepted | foundation_accepted | executable_evidence | P019 foundation, ADR-0005 acceptance closeout, real U3028269 TWS API funds/positions parity | real order/fill report-row parity waits for non-empty same-slice executions |
| D | rejected | rejected_not_applicable | not_applicable | ADR-0004 command separation | 无，除非 future command ADR reopens |
| E | future | not_implemented | missing_evidence | no external observation gateway owner yet | cross-repo governance and latency budget |
| F | rejected | rejected_not_applicable | not_applicable | manual UI observation only | cannot support contract-first high-frequency evidence |

### 3.2 取舍说明 / Trade-Off Notes

1. A is the safest continuation of current architecture, but it does not satisfy the new requirement for Account Console to independently observe broker account state during high-frequency testing.
2. B protects a single execution session and is useful when only one broker username/session is available, but it should be treated as shared-session observation rather than Account Console independent login.
3. C is the preferred candidate because it gives Account Console its own governed observation capability while preserving Nautilus as execution owner. Its acceptance depends on strict read-only API surface, secret/config refs only, explicit per-broker session conflict blockers, a shared Account Mirror projection contract, durable local observation storage, and Nautilus-compatible order/fill report mapping.
4. D must be rejected under current ADR-0004 boundaries because it collapses observation and command into one UI/backend runtime and creates a second execution path.
5. E is architecturally clean for a larger multi-broker estate but too heavy as the first implementation unless the workspace decides broker observation should be a shared external platform owner.
6. F may remain an operational emergency fallback, but it cannot be the formal Account Console architecture because it produces no structured, replayable, contract-locked evidence.

---

## 4. 决策 / Decision

ADR-0005 is accepted. Account Console may own a governed, read-only broker observation session capability for CTP, IB TWS / IB Gateway, stock broker APIs, CQG and TT, provided every implementation stays behind the boundaries below:

1. Observation sessions are read-only and cannot expose submit, cancel, replace, modify, CTP order insert/action, IB `placeOrder` / `cancelOrder`, or equivalent mutation APIs.
2. Broker/account/order truth remains with the broker/runtime/source owner. Account Console writes only contracts, normalized observation artifacts, projection caches, evidence refs and typed blockers.
3. Account Mirror is the UI/API projection boundary. The browser must not call broker adapters directly or parse raw broker payloads as truth.
4. Raw passwords, auth codes, 2FA material, front addresses, API keys, broker secrets and account secrets remain outside this worktree. Local artifacts may record owner refs, redacted aliases, checksums and negative assertions only.
5. Every broker observation family must use the shared profile, session-conflict, report-mapping, freshness and durable-store contract family unless a later ADR accepts a fork.
6. Durable observation storage is an evidence/projection cache only. It may support replay and incident review, but must not claim broker truth, command authority, trading readiness or complete history without source evidence.

### 4.1 决策结论 / Decision Summary

Option C, independent read-only broker observation sessions, is accepted as the first implementation direction. Option A remains a safe fallback for accounts without an accepted observation profile; Option B remains a compatibility bridge where Nautilus owns the only session; Option E may be revisited as a future external gateway. Option D and any direct full broker client in Account Console are rejected.

The accepted local owner is `account-console-broker-observation-session`, limited to read-only observation profiles, normalized Nautilus-compatible reports, durable observation-store evidence and Account Mirror input packages. Nautilus / future Execution Gateway remains the command and execution owner.

### 4.2 决策边界 / Decision Boundaries

1. `account-console-broker-observation-session` may collect or project read-only account/funds/positions/report observations only after readiness and conflict gates pass.
2. A connected observation session never implies command capability, live trading readiness, broker tradability, admission, approval or capital authority.
3. Missing source evidence, sequence gaps, checksum drift, conflict ambiguity, unavailable execution rows or incomplete replay must produce typed blockers.
4. Screenshots may support UI rendering or local operator/window context, but never funds, positions, order, fill, broker, account or readiness truth.
5. Real U3028269 TWS API funds and positions are accepted only through the same-slice TWS API query -> source package -> Account Mirror -> UI parity chain recorded by P019.
6. Real U3028269 order/fill callback parity is not claimed while the current read-only `reqExecutions` evidence has zero rows; this is a typed residual runtime condition, not a reason to reopen the architecture decision.

### 4.3 Design Kernel / 设计内核

```text
Broker Observation Profile
  -> readiness and session-conflict gates
  -> read-only broker observation adapter
  -> normalized Nautilus-compatible OrderStatusReport / FillReport
  -> durable observation/evidence store
  -> Account Mirror projection
  -> Account Console API/UI readback
```

The browser consumes Account Mirror projections only. Raw broker payloads remain provenance/debug evidence by ref and checksum.

### 4.4 推荐产物 / Recommended Deliverables

The accepted foundation deliverables are:

1. broker observation profile, session-conflict, report batch, report mapping, freshness, durable-store and cross-broker extension schemas/fixtures;
2. negative validators rejecting raw secrets, command drift, raw payload truth, broker-specific contract forks, realtime claims from snapshots and memory-only reload pass claims;
3. Account Mirror API projection for `acct.ib.live.u3028269` with command disabled and no broker/order/account truth;
4. real U3028269 read-only TWS API pipeline, source-package builder, query/source parity validator and UI parity harness;
5. durable store reload proof from persisted source/executions artifacts with no live-memory dependency;
6. P019 evidence lanes and runtime redaction/freshness validators.

### 4.5 决策覆盖与落地矩阵 / Decision Coverage And Landing Matrix

| Decision item | Status | Evidence |
| --- | --- | --- |
| D1 Observation-only broker session | accepted | `validate_p019_api_boundary.py`, `validate_p019_profile_security_provenance.py`, Account Mirror U3028269 projection |
| D2 Secret/config boundary | accepted | profile/security validators, runtime redaction gate, owner refs only |
| D3 Session conflict fail-closed | accepted | `session_conflict_policy.schema.json`, blocked/negative fixtures |
| D4 Nautilus-compatible order status report | accepted foundation | report mapping matrix and synthetic positive report-row UI; real row parity waits for non-empty same-slice executions |
| D5 Nautilus-compatible fill report | accepted foundation | report mapping matrix, synthetic fill path, real `reqExecutions` zero-row typed blocker |
| D6 Raw payload provenance only | accepted | report batch/mapping validators and browser negative gates |
| D7 Account Mirror projection boundary | accepted | `validate_account_mirror_api.py`, P019 API boundary, real UI parity |
| D8 Freshness and sequence discipline | accepted foundation | freshness/sequence schema, runtime freshness gates; realtime claims remain blocked without event evidence |
| D9 No command drift from reports | accepted | API boundary and Playwright synthetic report-row test |
| D10 Cross-broker extension shape | accepted | cross-broker extension matrix covering IB TWS, CTP, stock broker, CQG and TT |
| D11 Durable observation store | accepted foundation | complete/gap fixtures plus real persisted-artifact reload proof |
| D12 Replay gap blockers | accepted | gap fixture, checksum/memory-only negative tests and real zero-execution partial blocker |

---

---

## 5. Landing Map / 落地映射

P019 is the accepted successor proposal for the ADR-0005 foundation. Future broker-specific implementations inherit the same contract family and must add child-change evidence instead of reopening the architecture decision.

### 5.0 Accepted Decision Boundary / 已接受决策边界

The accepted boundary is read-only broker observation only:

1. observation profiles and source packages may be owned locally when all readiness, conflict, secret and no-command gates pass;
2. normalized reports and durable observation-store artifacts may be persisted locally as evidence/projection cache;
3. Account Mirror remains the only UI/API readback boundary;
4. broker/runtime/account/order truth, command authority, approvals, capital and tradability remain external or future-owner concerns.

### 5.0.1 Not Accepted By This ADR / 本 ADR 不接受

This ADR does not accept order submission, cancellation, replacement, modification, command UI, raw credential ownership, broker tradability, production admission, capital allocation, or complete execution-history claims from partial observation evidence.

### 5.0.2 Successor Proposal Boundary / 后续 Proposal 边界

P019 is the successor proposal for the accepted foundation. It closes the shared broker-observation contract/API/UI/runtime gates and leaves only source-specific runtime evidence to future child changes.

| Phase | 目标 | 承接 proposal / change | 退出条件 | retirement 影响 | 承接状态 / Landing Status |
| --- | --- | --- | --- | --- | --- |
| Phase 0 | Accept architecture and owner boundary | ADR-0005 + P019 | ADR accepted, owner map aligned, no-command/secret/truth gates pass | pre-decision blocker retired | completed |
| Phase 1 | Contract family | P019 | schemas, positive fixtures and negative fixtures pass | broker-specific schema forks rejected | completed |
| Phase 2 | Account Mirror readback | P019 U3028269 | U3028269 projects through Account Mirror only | direct browser/broker route rejected | completed |
| Phase 3 | Real funds/positions parity | P019 U3028269 real closeout | TWS API query/source/UI parity pass | screenshot and sample truth rejected | completed |
| Phase 4 | Report/store foundation | P019 report/store gates | synthetic positive and real persisted-artifact reload evidence pass; zero real execution rows typed partial | memory-only report/store pass rejected | completed_with_residual_runtime_blocker |
| Phase 5 | Future broker expansion | future child proposals | each broker extends shared contracts and preserves command boundary | ad hoc broker UI truth rejected | future |

### 5.1 旧代码退役与文档收口 / Legacy Retirement And Documentation Closure

P019 retires the pre-ADR blocker as an architecture blocker. Runtime blockers remain typed evidence when specific broker/source conditions are absent, for example zero same-slice execution rows, missing startup replay, checksum drift, or session conflicts.

| 旧项 / 路径 | 当前职责 | 新归宿 / 替代物 | 处理动作 | 暂留边界 | 最终移除条件 | 文档同步项 | 承接状态 / Landing Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `adr0005_not_accepted` blocker | pre-decision architecture gate | runtime/source-specific typed blockers | retire as architecture blocker | historical evidence may mention it as non-claim | ADR acceptance validator passes | P019 completion audit, owner map | retired_for_architecture |
| P019 blocked UI projection | fail-closed rendering guard | synthetic blocked contract evidence | keep as negative UI contract | does not describe current real TWS ready state | blocked UI validator passes | P019 acceptance | retained_as_negative_fixture |
| synthetic ready report rows | positive UI/report/store contract guard | real owner/runtime report rows when available | keep synthetic-only boundary | cannot prove real U3028269 order/fill truth | same-slice non-empty executions evidence | P019 evidence lane manifest | retained_as_contract_fixture |

---

## 6. Acceptance And Evidence / 验收与证据

ADR-0005 architecture acceptance is complete for the P019 foundation. This section records the stable acceptance shape; detailed commands and artifacts remain in P019 and the machine-readable acceptance closeout.

### 6.0 ADR-Level Acceptance Only / 仅限 ADR 级验收

ADR-0005 的验收只证明 Account Console broker observation 架构没有 drift 成 command / execution / broker truth owner。它不证明任何真实 broker 登录成功、live trading readiness、capital approval、risk approval、production admission 或 order mutation capability。

任何真实连接、profile、event stream、report artifact、browser screenshot、run id、checksum 或命令输出，都必须写入 successor proposal / child change acceptance；ADR closeout 只能沉淀稳定边界与最终 owner 结论。

### 6.1 通用验收纪律 / General Acceptance Rules

1. 每个 broker observation adapter 必须先有 focused contract / backend negative tests，再声明可被 Account Mirror 或 UI 消费。
2. 缺少 broker source evidence、session owner、secret/config ref、report mapper、checksum、timestamp、sequence 或 provenance 时，必须产生 typed blocker，不得显示为健康状态。
3. Browser screenshot 只能证明 rendering，不证明 broker/account/order truth。
4. Raw broker payload 只能作为 provenance / evidence / debug drill-down；backend 和 browser 必须消费 Nautilus-compatible normalized report。
5. 任何 `submit`、`cancel`、`replace`、`modify`、CTP order insert/action、IB `placeOrder`/`cancelOrder`、CQG/TT/stock mutation API 出现在 ADR-0005 implementation surface 中，必须 fail。
6. Session conflict policy 必须 fail closed；未知 session owner、同一 client id/front/session slot 冲突、同一 broker username 并发冲突或 Nautilus trading session 冲突不得 silent downgrade。
7. All order/fill report mappings must preserve account identity, client order id, venue order id, report id, event timestamp, receive/project timestamps and source checksum where available.
8. Account Console UI must not infer command capability from a connected observation session, healthy source state, account kind, broker kind or order report presence.
9. Durable local observation store must persist normalized order/fill reports and account/position/funds snapshots across process restarts.
10. Replay gaps, missing startup reports, truncated callback streams and store checksum mismatches must produce typed blockers instead of fabricated complete history.

### 6.2 Successor Proposal Acceptance Scenario Requirements / 后续 Proposal 验收场景要求

| ADR decision item | Required acceptance scenario | Positive path | Must fail if | Authority / retirement boundary | Minimal evidence |
| --- | --- | --- | --- | --- | --- |
| D1. Observation-only broker session | Account Console can own read-only broker observation session without becoming execution owner | broker profile connects or projects a typed read-only blocked state with `command.enabled=false` | any order mutation method is exposed, imported into public API, or reachable from UI | Nautilus / future Execution Gateway remains execution owner | focused backend test + owner boundary gate |
| D2. Secret/config boundary | broker profile records refs only | profile contains `secret_ref` / `config_ref` / redacted alias and `raw_secret_values_recorded=false` | raw password, auth code, front address, API key, 2FA or account secret is recorded in repo docs/tests/artifacts/UI | sensitive material remains with source owner / secured runtime owner | schema test + redaction fixture |
| D3. Session conflict fail-closed | conflicts block observation instead of stealing sessions | same username/clientId/front/session slot conflict returns typed blocker | Account Console silently reuses, steals, or downgrades conflicting trading session | Nautilus trading session cannot be displaced by observation | backend conflict-policy test |
| D4. Nautilus-compatible order status report | observed broker order callback maps to Nautilus `OrderStatusReport` shape | normalized report includes account id, instrument id, client/venue order ids, side, type, TIF, status, quantity, filled qty, price/avg price, report id and timestamps | broker-specific report schema becomes canonical truth | normalized report is Account Mirror input; raw broker callback is provenance only | report mapper contract test |
| D5. Nautilus-compatible fill report | observed broker trade/fill callback maps to Nautilus `FillReport` shape | normalized report includes trade id, venue order id, client order id, last px/qty, commission/liquidity side where available, report id and timestamps | fill is represented only as broker raw payload or UI-invented row | normalized fill report feeds Account Mirror / order event tape | report mapper contract test |
| D6. Raw payload provenance only | raw broker callback is preserved without becoming truth | report has `report_msg_ref`, checksum and optional redacted excerpt linked from normalized report | browser parses raw payload as account/order truth | raw payload remains evidence/debug artifact | browser negative test + backend schema test |
| D7. Account Mirror projection boundary | observation reports project through Account Mirror | `/api/mirror/accounts/{account_id}` or successor endpoint exposes order/fill projection with provenance and freshness | frontend calls broker adapter directly or bypasses Account Mirror for fresher state | Account Mirror owns projection/readback freshness | API test + Playwright route assertion |
| D8. Freshness and sequence discipline | high-frequency observation exposes ordering and lag | event/report has source observed/received/projected timestamps, sequence or monotonic cursor, lag/staleness fields | UI claims realtime from snapshot-only or unordered callbacks | freshness is projection metadata, not UI guess | focused API contract test |
| D9. No command drift from reports | order report presence does not enable action | UI shows observation-only/read-only command state with no submit/cancel/replace controls | command buttons appear because order row/report exists | command capability requires separate ADR/proposal | Playwright negative test |
| D10. Cross-broker extension shape | CTP/IB/stock/CQG/TT adapters share contract shape | adding a broker only adds source profile/adapter/mapper while preserving normalized reports | broker-specific UI branch or second report schema is introduced | Account Console remains broker-neutral projection surface | schema test + docs gate |
| D11. Durable observation store | observed reports and snapshots survive restart for replay/review | local store can reload order/fill reports, funds snapshots, positions snapshots and source health with checksums | reports exist only in memory or only in startup callback stream | store is evidence/projection cache, not broker truth writer | persistence/reload test |
| D12. Replay gap blockers | incomplete local history fails closed | missing startup replay, sequence gap or checksum mismatch emits typed blocker | UI shows complete lifecycle from partial local data | replay completeness is explicit and provenanced | gap/replay negative test |

### 6.3 Architecture-Level Acceptance / 架构级验收

1. D1-D3 must be verified before any real or simulated broker observation profile is exposed to operators.
2. D4-D6 must be verified before any order/fill callback can be displayed as an order report in Account Console.
3. D7-D8 must be verified before UI copy, tests or docs claim high-frequency or realtime account/order observation.
4. D9 must be verified before any order detail or order report panel is accepted under this ADR.
5. D10 must be verified before adding a second broker family under ADR-0005; otherwise a new ADR is required to explain the fork.
6. D11-D12 must be verified before order report UI, post-session review, reconciliation or incident analysis can claim durable replay support.
7. ADR-0005 cannot be marked `accepted + implemented` while command mutation APIs are present in the Account Console observation surface.

### 6.4 ADR Closeout Distillation / ADR closeout 沉淀

ADR-0005 closeout is recorded by `docs/acceptance/2026-06-20-adr0005-broker-observation-session-acceptance.json` and validated by `python scripts/validate_adr0005_acceptance.py`.

| Distillation target | Stable conclusion distilled from this ADR | Source proposal / change / evidence | Do not copy forward | Closeout action |
| --- | --- | --- | --- | --- |
| `docs/adr/README.md` | ADR-0005 is a binding accepted ADR | ADR-0005 + acceptance closeout | transient runtime logs | move from proposed to current binding ADRs |
| `docs/ownership/account-console-owner-map.md` | `account-console-broker-observation-session` is accepted for read-only observation only | P019 + owner-map alignment validator | command/trading/readiness claims | update pending owner to accepted guarded owner |
| P019 docs | P019 foundation is accepted with residual runtime blockers for real report rows | P019 completion audit | synthetic-as-real claims | mark foundation accepted and preserve typed blockers |

---

## 7. 关联文档 / Related Documents

1. [ADR-0002 Business workbench first account console navigation](./0002-adopt-business-workbench-first-account-console-navigation.md)
2. [ADR-0003 Contract-first UI slice development](./0003-adopt-contract-first-ui-slice-development.md)
3. [ADR-0004 Account Capability Fabric with mirror readback](./0004-adopt-account-mirror-observation-and-command-plane.md)
4. [Account Console Owner Map](../ownership/account-console-owner-map.md)
5. [P019 Broker Observation Session Foundation](../proposals/p019-broker-observation-session-foundation/README.md)

---

## Optional Fragments / 可选片段

### A. Red Lines

1. Account Console observation sessions must not expose submit/cancel/replace/modify/order-insert/order-action APIs.
2. Connected broker observation must not imply command capability, broker tradability, admission, capital approval or live readiness.
3. Raw CTP/IB/stock/CQG/TT secrets, auth codes, front addresses, API keys, passwords or 2FA material must not be copied into this repo, fixtures, docs, evidence or chat.
4. Raw broker order payloads must not be parsed by the browser as account/order truth; Nautilus-compatible normalized reports are the canonical order/fill observation shape.
5. Session conflicts must fail closed and produce typed blockers; Account Console must not steal, reuse, or silently downgrade a Nautilus trading session.
6. A new broker family must extend `Broker Observation Profile` + normalized report mapper + Account Mirror projection, not create a broker-specific Account Console truth path.
7. Observed order/fill reports and account/funds/position snapshots must not be memory-only; if durable storage is unavailable, UI must show blocked/partial replay state.
8. Local durable observation store must not be used to claim broker truth, order finality, readiness or command authorization without source provenance and reconciliation.
