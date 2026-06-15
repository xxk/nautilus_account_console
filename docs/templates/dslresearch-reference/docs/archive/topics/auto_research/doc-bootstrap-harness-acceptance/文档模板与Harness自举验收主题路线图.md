# 文档模板与Harness自举验收主题路线图 / Document Template And Harness Bootstrap Acceptance Topic Roadmap

- 创建日期：2026-03-31
- 最后更新：2026-04-03（topic 已迁出 roadmap，转入 archive）
- 状态：archived（仅用于历史回溯，不再作为当前正式入口）
- topic-id：`doc-bootstrap-harness-acceptance`
- 所属域：`auto_research`
- 当前正式入口：[`../../../../doc_harness_kit/README.md`](../../../../doc_harness_kit/README.md)
- 当前治理入口：[`../../../../../AGENTS.md`](../../../../../AGENTS.md)

> 本文档仅用于回溯“topic/child 模板与文档门禁自举验证”这次历史试点，不再作为当前 topic roadmap 入口。

---

## 0. 归档说明

### 0.1 归档原因

1. 本 topic 的目标是一次性验证“新建 topic + child change 文档包”能否被现有模板与门禁正常接纳。
2. 当前验证目标已完成，且现行正式入口已经是 `doc_harness_kit` 与仓库级 `AGENTS.md`，不再需要该 topic 继续承担导航职责。
3. 若继续保留在 `docs/topics/roadmap/` 下，会被 topic/harness 扫描逻辑继续识别为当前 topic，增加误判成本。

### 0.2 现行正式入口

1. 规则入口：[`../../../../doc_harness_kit/README.md`](../../../../doc_harness_kit/README.md)
2. 治理入口：[`../../../../../AGENTS.md`](../../../../../AGENTS.md)
3. 历史 child change：[`../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/plan.md`](../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/plan.md)

---

## 1. 历史状态速览

| 维度 | 历史结论 | 说明 |
| --- | --- | --- |
| topic 定位 | 已冻结 | 只负责验证“新建 topic + child change 文档包”可被现有模板与门禁正常接纳 |
| child 拆分 | 已完成 | 本 topic 只保留 1 个验证确认型 child，不扩展为实现型任务 |
| 正式验收 | 已完成 | 已通过定向 `check_change_docs`、`check_topic_docs` 与全仓 `check_harness` 联合验证 |

一句话结论：

`DSLResearch 的 topic roadmap、child change 三件套模板，以及 child/topic 文档门禁与 harness，自举创建后可以被正常识别和验收。`

---

## 2. 为什么当时单独开这个 topic

1. 需要用一个真实、最小、可回放的 topic/child 组合验证“模板本身可用”，而不是只靠模板说明文本自证。
2. 需要证明新增 topic 不会破坏现有 `AI-TASK-QUEUE`、`check_change_docs`、`check_topic_docs` 与 `check_harness` 的收口逻辑。
3. 需要为后续“先建 topic、再挂 child、再跑门禁”的流程提供一个可直接模仿的最小样板。

## 3. topic 范围

### 3.1 In Scope

1. 新建 1 个独立 topic roadmap。
2. 新建 1 个独立 child change 三件套。
3. 用真实门禁命令验证这套文档包可被现有 harness 接纳。

### 3.2 Out Of Scope

1. 不新增任何业务实现代码。
2. 不修改现有 `s5-nautilus-python-composite` 主题逻辑。
3. 不重写 `doc_harness_kit` 模板本身。

## 4. 历史 child 拆分与状态

| # | change-id slug | 目标 | 类型 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | `bootstrap-and-harness-smoke` | 建立最小 topic + child，并验证模板与门禁可用 | 验证确认 | ✅ 已验收 |

## 5. 历史通过条件

1. 新建 roadmap 的元数据、目录名、`topic-id` 与 `AI-TASK-QUEUE` 能被 `check_topic_docs.py` 正确识别。
2. 新建 child 的 `plan.md`、`acceptance.md`、`ai_constraints.md` 能被 `check_change_docs.py` 正确识别。
3. 新增 topic 不影响现有仓库的 `scripts/check_harness.py --root . --check-change-docs --check-topic-docs` 通过。
4. 证据必须落在 child 目录内，不能引用“当前对话终端输出”作为唯一留证。

## 6. 历史证据入口

1. child 三件套：[`../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/plan.md`](../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/plan.md)
2. child 验收：[`../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/acceptance.md`](../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/acceptance.md)
3. child 证据：[`../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/自举验收证据.md`](../../../../changes/_archive/20260331__doc-bootstrap-harness-acceptance__bootstrap-and-harness-smoke/%E8%87%AA%E4%B8%BE%E9%AA%8C%E6%94%B6%E8%AF%81%E6%8D%AE.md)
