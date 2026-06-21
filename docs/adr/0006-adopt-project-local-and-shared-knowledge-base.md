---
status: proposed
owner: architecture
adr_id: "0006"
decision_status: proposed
landing_status: planned
---

# ADR-0006: Adopt Project-Local Knowledge Router And Shared Knowledge Base / 采用项目本地知识路由与共享知识库

- 日期：`2026-06-20`
- ADR 类型：governance
- 决策状态：proposed
- 落地状态：completed
- 落地摘要：completed via P020 `p020-adr0006-account-console-knowledge-router`; first landing includes project-local `docs/knowledge/`, `blocker-routing.json`, seed bug cards, adoption note and `scripts/check_knowledge_docs.py` with negative-fixture selftest
- 覆盖摘要：decision 9/9, implementation 8/8, retirement 3/3
- 适用范围：`nautilus_account_console` documentation governance, AI context routing, repeat-bug prevention, prevention gates, shared Nautilus knowledge adoption
- 决策问题：Account Console 应如何建立一个可被其他项目学习的样板知识库与知识路由机制，同时接入 `D:\Nautilus\global_docs\knowledge-common`，让 AI 遇到问题时只读取最小相关知识，并避免知识库成为第二状态源或第二 truth source？
- 当前倾向：推荐采用 `Knowledge Base + Knowledge Router + Prevention Gate` 三件套：共享知识进入 `D:\Nautilus\global_docs\knowledge-common`，Account Console 项目事实与历史 bug 进入本仓 `docs/knowledge/`，AI 通过 `blocker-routing.json` / optional router script 精准读取卡片，并以 Knowledge Gate 防漂移。
- 最终决策：待决策
- Required document order: ADR-0006 -> successor proposal/change -> `docs/knowledge/` skeleton -> `blocker-routing.json` -> Knowledge Gate -> adoption note for other projects

---

## 1. Problem Frame / 问题框架

`nautilus_account_console` 已有 ADR、proposal、acceptance、design、ownership、topics 和 workflow templates，但还没有本仓自己的 `docs/knowledge/`。当前长期知识分散在 README、AGENTS、ADR、proposal、acceptance 和一次性 evidence 中。AI 下次进入仓库时，容易出现两类问题：

1. 为了找经验读取过多历史材料，淹没当前 proposal/change 的真实约束。
2. 已经踩过的边界问题只停留在一次性 acceptance 或聊天里，后续任务仍可能重复犯错。

Account Console 的边界尤其敏感：它是 read-only account observation console，不拥有 runtime truth、broker truth、admission truth、approval truth、capital truth 或 trading readiness truth。知识库如果设计不好，会把“经验沉淀”误写成“当前状态”“已验收”“可交易”“broker source truth”，从而破坏现有架构边界。

同时，Nautilus workspace 已经存在共享知识库：

```text
D:\Nautilus\global_docs\knowledge-common
```

因此本仓不应该另起一套公共知识平台，也不应该把所有项目知识都集中到共享库。更优方案是把 Account Console 做成可复制的 project-local sample：共享原则沉淀到 `knowledge-common`，项目事实沉淀到本仓 `docs/knowledge/`，AI 通过本地 Knowledge Router 命中最小卡片集，再通过 Prevention Gate 把可重复错误变成自动检查。

### 1.1 Hard Constraints / 硬约束

1. Git-tracked Markdown is the knowledge source. Obsidian, Canvas, local workspace state or plugin state may be used only as read-only human projection.
2. `docs/knowledge/` must not contain current task state, live acceptance status, runtime readiness, broker readiness, account truth, admission truth, approval truth, capital truth or trading readiness truth.
3. Shared knowledge belongs in `D:\Nautilus\global_docs\knowledge-common`; project-local facts belong in this repo's `docs/knowledge/`.
4. Account Console knowledge cards must not contain raw passwords, auth codes, broker secrets, raw front addresses, account secrets or secret-bearing runtime material.
5. Repeated machine-checkable lessons must graduate to scripts/tests/docs gates. A knowledge card is not a substitute for a prevention gate.
6. Current task evidence remains in proposal/change/acceptance artifacts; knowledge cards may link to source refs but must not copy evidence bodies or command outputs.
7. Project-local knowledge may link to shared patterns but must not fork shared principles by copy-pasting long duplicate rules.
8. Other projects may copy this structure, but each project must rewrite owner boundaries and local bug cards for its own repo.
9. AI must not read the full shared knowledge base or full project-local knowledge base by default; it must first use current task truth and then route to matched cards.
10. Router output is advisory reading scope only. It cannot declare acceptance, readiness, owner transfer or blocker closure.

### 1.2 Explicit Non-Goals / 明确不做

1. 本 ADR 不创建 vector DB、RAG service、external memory service 或长期记忆 agent。
2. 本 ADR 不把 Obsidian `.obsidian/`、Canvas、Dataview、Tasks 或 plugin config 纳入正式治理依赖。
3. 本 ADR 不替代 ADR、architecture、proposal、change、acceptance、owner map、AGENTS 或 README。
4. 本 ADR 不落地 Account Console broker observation、IB TWS、CTP 或 Paper runtime knowledge 的敏感材料。
5. 本 ADR 不宣告任何 proposal/change 已验收，也不改变 ADR-0005 的 broker observation decision state。

### 1.3 Owner / Canonical Entry Impact

1. 新增 project-local knowledge owner：`docs/knowledge/`。
2. 新增 project-local routing owner：`docs/knowledge/blocker-routing.json`，用于 blocker/symptom/keyword -> matched cards/gates 的最小读取路由。
3. 新增 optional router entry candidate：`scripts/route_knowledge.py`，用于非必须的本地路由辅助；正式 truth 仍在 JSON/Markdown/Git。
4. 新增 recommended AI entry：current proposal/change/acceptance -> `docs/knowledge/blocker-routing.json` -> matched bug card/playbook only when relevant.
5. 新增 local gate candidate：`scripts/check_knowledge_docs.py`，用于结构、frontmatter、forbidden truth/status wording, route target existence and secret-leak checks。
6. 不新增 runtime owner、broker owner、account owner、writer、adapter、schema truth writer、API entry 或 UI route。
7. 不改变 existing proposal/acceptance truth source；knowledge base records durable lessons, routing and prevention only.

### 1.4 概念判重 / Canonical Naming Check

| Candidate term | Layer / Owner | Existing nearby term | Collision risk | Decision | Guard / Evidence |
| --- | --- | --- | --- | --- | --- |
| `Project-Local Knowledge Base` / `docs/knowledge` | docs governance / repo-local knowledge | ADR, architecture, topics, proposals, acceptance | AI may treat it as a fourth execution surface | Accept as durable knowledge only; no current state | Knowledge Gate forbids live status/acceptance truth |
| `Shared Knowledge Base` / `knowledge-common` | global docs / shared patterns | `D:\Nautilus\global_docs\knowledge-common` | Project facts may leak into shared layer | Reuse existing shared owner; link instead of fork | project cards require shared refs only when applicable |
| `Knowledge Gate` | governance check | proposal gate, owner boundary validation, harness guard | May become a parallel harness family | Accept as repo-local docs check, optionally wired into existing gates | `scripts/check_knowledge_docs.py`; no new state machine |
| `Knowledge Router` | docs governance / AI context routing | AGENTS read order, proposal workflow, blocker taxonomy | AI may treat router output as verdict or current task truth | Accept as minimal-read advisory router only | `blocker-routing.json`; gate validates targets; acceptance remains current task truth |
| `Prevention Gate` | guard / repeat-bug prevention | tests, proposal gate, owner boundary validation | May be mistaken for formal acceptance | Accept as machine-checkable prevention, not change acceptance | check scripts/tests; acceptance still records real evidence |
| `Bug Ledger` | repeat-bug memory | local issues, acceptance blockers, proposal decision logs | May duplicate current task tracking | Accept for reusable failure patterns, not open task status | bug-card template requires source_ref and prevention_gate |
| `Project Playbook` | AI/human navigation | README, AGENTS, owner map | May conflict with AGENTS instructions | Accept as secondary navigation; AGENTS and ADR boundaries win | README states precedence order |
| `Knowledge Dashboard` | index/projection | proposal dashboard, acceptance dashboard | May look like status dashboard | Accept as navigation-only dashboard | no progress, readiness, pass/fail current-state fields |

---

## 2. 与既有 ADR / Architecture 的关系 / Relationship To Existing Decisions

1. ADR-0001 remains valid: when this repo lacks a documentation template or gate capability, learn from DSLResearch/reference templates first, then adapt to Account Console boundaries.
2. ADR-0002 remains valid: knowledge navigation must support business-workbench-first product thinking, but must not become UI product state.
3. ADR-0003 remains valid: UI implementation remains contract-first panel slices; knowledge cards may warn about drift but cannot replace contracts/fixtures/acceptance.
4. ADR-0004 remains valid: Account Mirror and Account Capability Fabric remain read-only observation architecture. Knowledge cards must not create account, command, risk, approval, capital or broker truth.
5. ADR-0005 remains independent and proposed: broker observation session architecture is not decided by this ADR.
6. `D:\Nautilus\global_docs\knowledge-common` is the shared knowledge owner. This ADR adopts it; it does not create a competing shared repository.
7. Existing proposal and acceptance documents remain the only places for current implementation state and evidence.

---

## 3. 方案对比 / Options Comparison

本次对比不只比较“有没有知识库”，还比较 truth-source 分层、AI context cost、知识路由精度、跨项目复用、secret safety、gate 可执行性和未来项目 adoption 成本。

| 方案 | 核心思路 | 适用场景 | 优点 | 缺点 / 风险 | 架构一致性 | 实施成本 | 结论 | 采纳与落地 / Decision + Landing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Chat / acceptance only | 经验只留在聊天、acceptance 或 proposal notes | 一次性任务 | 零结构成本 | 下次 AI 不一定读取；重复 bug 难防；历史 evidence 被误读为当前 truth | 低 | 低 | 拒绝候选 | rejected |
| B. Project-local `docs/knowledge` only | Account Console 自己维护完整知识库 | 项目事实强绑定 | owner 边界清晰；落地快 | 通用模板和 failure pattern 会在各项目复制漂移 | 中 | 中 | 不作为唯一方案 | rejected_as_only_layer |
| C. Shared `knowledge-common` only | 所有知识都放 global_docs | 跨项目统一原则 | 统一检索；便于复用 | 项目事实混层；Account Console 边界容易覆盖其他项目 | 低 | 中 | 拒绝 | rejected |
| D. Two-layer Markdown KB + local gate | 共享库放通用模式；项目库放本地事实、bug、playbook；gate 防漂移 | 多项目 AI 开发、Account Console 做样板 | 复用和边界兼得；Git-first；可被其他项目复制；可升级为 gate | 仍依赖 AI 自觉选择相关卡片；路由不够强 | 高 | 中 | 过渡候选 | transitional |
| G. Knowledge Router + Prevention Gate | 在 D 基础上新增 `blocker-routing.json` / optional route script；AI 先识别问题类型，再读最小卡片集，修复后跑 prevention gate | 多仓、多 owner、多敏感边界、长循环 AI 开发 | token 成本最低；减少 context flooding；把可复发错误升级为检查；可复制到其他项目 | 需要维护路由规则和 route target gate | 高 | 中 | 推荐候选 | proposed |
| E. Obsidian-first vault | 让 Obsidian vault/Canvas/plugin 成为主要知识入口 | 人工图谱浏览 | 人工体验好 | 私有状态、插件和 UI 可能变成 truth source | 低 | 中 | 拒绝为正式方案 | rejected |
| F. External DB / RAG memory | 同步 Markdown 到外部检索/向量库 | 未来大规模检索 | 检索能力强 | 当前过重；外部 truth 风险；secret indexing 风险 | 中 | 高 | 未来扩展 | future |

### 3.1 Landing Evidence / 落地证据

| 方案 | decision_state | landing_state | evidence_state | evidence_ref | residual_risk |
| --- | --- | --- | --- | --- | --- |
| A | rejected | rejected_not_applicable | not_applicable | this ADR Section 3 | repeat bugs remain chat-bound |
| B | rejected_as_only_layer | not_implemented | docs_only | `nautilus_strategies/docs/knowledge` precedent | shared pattern drift |
| C | rejected | partially_implemented | docs_only | `D:\Nautilus\global_docs\knowledge-common` exists | project facts mixed into shared layer |
| D | included_as_base | planned | missing_evidence | successor proposal/change required | still needs explicit routing |
| E | rejected | rejected_not_applicable | not_applicable | global knowledge-common Obsidian guidance | plugin/local-state truth split |
| F | future | not_implemented | missing_evidence | no proposal yet | external memory governance |
| G | proposed | planned | missing_evidence | ADR-0006 successor proposal/change required | route taxonomy and gate need first landing |

### 3.2 取舍说明 / Trade-Off Notes

1. A fails the main purpose: durable repeat-bug prevention and low-cost AI routing.
2. B is useful inside a repo but insufficient as a workspace-wide learning pattern.
3. C centralizes too much and risks turning shared knowledge into project truth.
4. D is a necessary base layer because it matches current Nautilus governance: shared principles in `global_docs`, project facts in each repo, and executable checks for machine-checkable lessons.
5. E remains acceptable only as a human read-only projection over Markdown.
6. F can be revisited after Markdown knowledge and gates are stable across several repos.
7. G is the recommended architecture because it adds an explicit minimal-read router between problem symptoms and knowledge cards, preventing both all-shared centralization and full-library token waste.

---

## 4. 决策 / Decision

待决策。This ADR is opened with a recommended candidate but does not self-approve implementation.

### 4.1 决策结论 / Decision Summary

推荐接受方案 G, with D as the storage base:

```text
D:\Nautilus\global_docs\knowledge-common
  shared patterns, templates, validation playbooks, cross-project vocabulary

nautilus_account_console/docs/knowledge
  project facts, read-only account-console boundaries, local bug ledger, project playbook
  blocker-routing.json

nautilus_account_console/scripts/check_knowledge_docs.py
  structural, route target, forbidden truth-source and secret-leak checks

optional:
  nautilus_account_console/scripts/route_knowledge.py
    local helper that reads blocker-routing.json and prints matched cards
```

### 4.2 决策边界 / Decision Boundaries

1. `knowledge-common` owns cross-project reusable principles, AI loop playbooks, validation patterns, templates and generic bug patterns.
2. Account Console `docs/knowledge/` owns project-local facts, local owner boundaries, local bug ledger, read-only projection pitfalls and local gate routing.
3. `docs/knowledge/blocker-routing.json` owns local symptom/blocker-to-card routing; it does not own verdicts or acceptance.
4. Current proposal/change/acceptance status never moves into knowledge cards.
5. Account Console knowledge cards may link to ADR/proposal/acceptance source refs but must not copy secret material, raw runtime material or long evidence bodies.
6. AI must first read current task truth, then route to matched knowledge only; full-library reads require an explicit reason.
7. Other projects may copy the structure only after rewriting their local boundaries and route rules.

### 4.3 Design Kernel / 设计内核

Stable knowledge flow:

```text
Task discovers reusable lesson
  -> current proposal/change/acceptance records immediate evidence
  -> project-local bug/playbook card records repeatable lesson
  -> shared pattern added only when project-independent
  -> blocker-routing.json maps future symptoms to the card
  -> machine-checkable prevention becomes script/test/docs gate
  -> AI reads current task truth, then matched cards only
```

Runtime reading flow for AI:

```text
Problem or blocker appears
  -> classify symptom / owner / risk
  -> consult docs/knowledge/blocker-routing.json
  -> read only matched local cards and optional shared patterns
  -> act on current proposal/change/acceptance
  -> run prevention gate or record typed blocker
  -> promote new repeatable lesson only after evidence exists
```

Recommended Account Console skeleton:

```text
docs/knowledge/
  README.md
  00-dashboard.md
  project-playbook.md
  blocker-routing.json
  owner-boundaries.md
  account-console-read-model-boundary.md
  ui-projection-boundary.md
  runtime-secret-boundary.md
  bug-ledger/
    README.md
    KB-BUG-0001__readiness-claim-leaked-into-readonly-console.md
    KB-BUG-0002__raw-report-treated-as-account-truth.md
  templates/
    bug-card.md
```

### 4.4 推荐产物 / Recommended Deliverables

Successor proposal/change should deliver:

1. `docs/knowledge/README.md` with role, precedence, forbidden content and shared knowledge links.
2. `docs/knowledge/00-dashboard.md` as navigation-only dashboard.
3. `docs/knowledge/project-playbook.md` for AI/human entry routing.
4. `docs/knowledge/blocker-routing.json` with at least the first routing rules for readiness wording, raw report truth, secret/runtime material and owner-boundary confusion.
5. Three boundary cards: owner boundaries, UI projection boundary, runtime/secret boundary.
6. `docs/knowledge/bug-ledger/` with at least two seed Account Console bug cards.
7. `scripts/check_knowledge_docs.py` and a local validation command documented in README/AGENTS or proposal acceptance.
8. Optional `scripts/route_knowledge.py` only if the JSON route table needs a developer-friendly query helper; the JSON remains the canonical route source.
9. Adoption note describing how other projects should copy the skeleton without copying Account Console facts.

### 4.5 决策覆盖与落地矩阵 / Decision Coverage And Landing Matrix

| Required decision | Target state | Landing owner | Status |
| --- | --- | --- | --- |
| Shared vs project-local split | Shared principles in `global_docs`, project facts in repo | P020 + `docs/knowledge/README.md` | completed |
| Knowledge as non-truth-source | No current state, readiness, acceptance truth or secrets in cards | `scripts/check_knowledge_docs.py` | completed |
| AI routing | current task truth -> blocker routing -> matched cards only | `docs/knowledge/blocker-routing.json` | completed |
| Repeat-bug memory | bug ledger with source refs and prevention gates | `docs/knowledge/bug-ledger/` | completed |
| Prevention Gate | structural, route target and forbidden-content check | `scripts/check_knowledge_docs.py` | completed |
| Optional route helper | CLI helper prints matched card list without becoming truth source | `scripts/route_knowledge.py` | not_required_for_first_landing |
| Cross-project learning | reusable skeleton and adoption note | `docs/knowledge/adoption-note.md` | completed |
| Obsidian boundary | read-only projection only | `docs/knowledge/README.md` | completed |

---

## 5. Landing Map / 落地映射

### 5.1 Successor Proposal / Change

Successor proposal:

```text
docs/proposals/p020-adr0006-account-console-knowledge-router/
```

P020 owns implementation status, acceptance evidence and gate results for the first landing slice.

### 5.2 Retirement / Anti-Fork Table

| Legacy / risky pattern | Target | Retirement rule |
| --- | --- | --- |
| Chat-only durable lessons | `docs/knowledge/` card or shared pattern | retired by bug-card template and source-ref rule |
| Acceptance evidence copied into knowledge cards | source ref link only | retired by Knowledge Gate forbidden truth-source rules |
| Project facts copied into `knowledge-common` | project-local card | retired by adoption note and shared/project split rule |
| Knowledge dashboard used as status board | navigation-only dashboard | retired by dashboard status-drift check |
| AI reads full knowledge base for every issue | `blocker-routing.json` matched-card reading | retired by minimal-read policy and route gate |

---

## 6. Acceptance And Evidence / 验收与证据

Architecture-level acceptance for P020 first landing:

1. `docs/knowledge/` skeleton exists.
2. Knowledge cards contain required frontmatter and required body sections.
3. `docs/knowledge/blocker-routing.json` exists, references only existing local cards or approved shared patterns, and includes an explicit no-verdict/no-acceptance boundary.
4. Knowledge Gate rejects missing required files, missing bug-card fields, dangling route targets, forbidden truth/status wording and obvious secret-bearing fields.
5. At least two seed bug cards encode Account Console-specific repeat risks.
6. At least four initial route rules cover readiness wording, raw report truth, secret/runtime material and owner-boundary confusion.
7. Shared links point to `D:\Nautilus\global_docs\knowledge-common` without copying shared content wholesale.
8. Existing proposal/acceptance truth source remains unchanged.

Evidence is recorded in [P020 acceptance](../proposals/p020-adr0006-account-console-knowledge-router/acceptance.md).

---

## 7. Related Documents / 关联文档

1. `D:\Nautilus\global_docs\knowledge-common\README.md`
2. `D:\Nautilus\global_docs\knowledge-common\ai-autopilot-playbook.md`
3. `D:\Nautilus\global_docs\knowledge-common\validation-playbook.md`
4. `D:\Nautilus\global_docs\harness\Cross-Project Canonical Vocabulary Gate Contract.md`
5. `docs/adr/0001-dslresearch-first-doc-template-and-gate-capability-backfill.md`
6. `docs/adr/0004-adopt-account-mirror-observation-and-command-plane.md`
7. `docs/ownership/account-console-owner-map.md`
8. `AGENTS.md`
