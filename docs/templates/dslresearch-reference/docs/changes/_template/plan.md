---
change-id: "{{change-id}}"
governance_risk: "medium"  # low | medium | high
artifact_boundary:
  trusted_artifact_roots: []
    # 若本文档或 sibling docs 会引用正式 artifact，必须显式列出当前 change 允许信任的 artifact 根。
    # 示例：
    # - <当前 change 唯一允许信任的 case artifact root>
  allowed_evidence_roots:
    - output/debug/change_evidence/{{change-id}}/
    - output/reports/{{change-id}}/
dependencies:
  hard_blocking: []
    # 示例：
    # - id: 20260330__other-change-id
    #   reason: "必须先完成 XX 功能的 wiring"
    #   expected_status: in_progress
  soft_dependency: []
    # 示例：
    # - id: 20260329__another-change-id
    #   reason: "需要了解 XX 的数据冻结时间点"
    #   expected_status: completed
  blocked_by: []
    # 自动从其他 change 的 hard_blocking 反推，通常不需手工填写
ui_surface_freeze:
  required: false
  surfaces: []
    # 命中 report_surfaces/、*.html.j2、context_builder.py、Factor Board、Portal Case、Dev Home、Case Assurance 等 UI surface 时，
    # 必须设为 true，并列出当前冻结的 surface owner 或 surface id。
---

# <变更名称> 开发计划

<!-- CHANGE-ANTI-DRIFT-GATE:v1 -->

**状态**：draft
**进度**：0%
**日期**：YYYY-MM-DD
**范围**：[影响目录/模块]
**治理风险等级**：medium（low / medium / high）
**proposal-id**：[可选；若当前 change 由 proposal 编排则填写，例如 p012-case-short-reference-numbering]
**topic-id**：[可选；若当前 change 同时归属长期 roadmap/topic 则填写；例如 datareadiness]
**change-id**：{{change-id}}
**当前展示名 / Current Display Name**：[可选；当当前正式名称与历史 change-id 指向名称不一致时填写]
**关联 acceptance**：./acceptance.md

> 说明：`change-id` 是当前变更的唯一标识，不应与其他 change 共用。若当前 change 由 proposal 编排，应优先填写 `proposal-id` 作为直接上层关联；只有当该 change 同时归属长期 roadmap/topic 时，才补充 `topic-id` 作为长期追踪锚点。
> 命名规则：若当前正式展示名已调整，但历史 `change-id` 作为证据锚点不便回改，应填写 `当前展示名 / Current Display Name`，并在这里说明“旧 `change-id` 仅保留用于维持证据链与回链稳定性”。若不存在展示名与 `change-id` 名称分离，可删除该字段。
> **Artifact Trust Boundary / Artifact 信任边界：**proposal、acceptance、ai_constraints 以及相关 evidence 若引用正式 artifact，**只能**引用 `artifact_boundary.trusted_artifact_roots` 与 `artifact_boundary.allowed_evidence_roots` 下的对象。禁止引用其他 case、其他 change、debug 历史残留或未在此声明的外部 artifact；发现越界路径时应直接视为文档不合格，而不是靠人工解释兜底。
> AI 阅读入口：先读 acceptance.md 的"验收标准"与"禁止行为"，再读本文的「能力映射」「任务清单」与「完成定义」，最后按 sibling `ai_constraints.md` 的执行循环推进；以验收标准为唯一收敛目标，不得自行扩大改动范围。
> **元数据主来源规则：**本文件头部是当前 change 的通用元数据主来源；sibling docs 只保留执行或验收收口所必需的最小字段，避免重复维护同一批元数据。
> 开发方法默认采用 **Acceptance-First / ATDD-lite**：先确认"功能做成什么才算通过"，再拆开发任务；计划中的每一步都应能映射回 acceptance 场景、出口条件或证据要求。**正式 change 验收只接受真实入口、真实环境、真实产物与真实证据；test 仅用于锁定 contract 与 function，不能单独构成 change 验收结论。**
> 文档治理采用风险分级：`medium/high` 默认采用 `plan.md + acceptance.md + ai_constraints.md`；`low` 允许仅保留 `plan.md`，走“commit message + 定向 test pass”轻量闭环。**默认不创建 `design.md`**；只有在满足以下任一门槛时，才允许新增 `design.md`：1）存在两个及以上可行方案且需要明确取舍；2）正式入口或主要实现落点容易改错；3）涉及发布/部署/迁移回滚策略；4）需要提前冻结长期接口、返回码、状态文件或目录归属等设计口径。

## Work Item Contract Metadata

| Field | Value |
| --- | --- |
| work_item_type | delivery |
| work_item_layer | change |
| surface_mode | none |
| action_mode | execution_capable |

> Source: `docs/governance/work_item_contract.yaml`. Change metadata classifies the executable slice; it does not create a second owner or proposal taxonomy.

## 最小必填章节 / Required Minimum

小变更只需保留以下章节，其余标有"（可选）"的章节可直接删除：

| 必填 | 条件必填 |
| --- | --- |
| 一、需求简述 | 十一、规则增量摘要（change_type ≠ 纯实现/验证确认时） |
| 一点五、防跑偏收敛卡 | |
| 二、能力映射 | 十二、回写与相关变更（long_term_target ≠ 无时） |
| 三、AI 执行约束 | |
| 七、任务清单 | |

---

## 一、需求简述

必须在计划开头先用极短摘要写清楚：

1. 这次变更要解决什么问题
1. 本次明确要交付什么
1. 本次明确不做什么
1. 做完之后要以什么验收信号判断“功能真的成立”

要求：

1. 只写结果导向的摘要，不重复完整需求文档
1. 控制在 3 到 5 行内，或一个短段落加不超过 3 条要点
1. 背景复杂时，在下方「背景与约束」可选章节中展开，不需要另建文件

---

## 一点五、防跑偏收敛卡 / Anti-Drift Convergence Card

在开始实现前，先用下面 4 项冻结本次 change 的最小收敛面。这里不是长方案，而是执行期间的局部锚点：一旦开始做事，默认先围绕这 4 项推进，而不是边做边扩 scope。

| 项 | 当前填写 |
| --- | --- |
| 单一收敛目标 / Single Outcome | <本轮只允许收敛这一件事；若出现第二目标，默认拆 follow-up> |
| 第一刀落点 / First Edit Surface | <第一处应修改的 owner / file / surface；优先写最直接控制行为的落点> |
| 首个验证动作 / First Validation | <第一处实质编辑后立刻执行的 focused test / command / gate> |
| 超范围触发条件 / Split Triggers | <出现哪些新范围时必须停下改计划或拆 follow-up，而不是顺手扩面> |

填写规则：

1. `单一收敛目标` 只允许写一个结果，不要把“顺手补文档/顺手清理技术债/顺手做第二能力”并进来。
1. `第一刀落点` 应尽量写到直接控制行为的 owner；若当前位置只是 wiring/forwarding，应写明下一跳的真实控制点。
1. `首个验证动作` 必须是本 change 最便宜、最能证伪当前判断的 focused validation；若这里写不出来，说明验收口径或控制路径还没收敛，应先补文档而不是直接编码。
1. `超范围触发条件` 要写具体触发信号，例如“需要新增第二 owner”“需要改第二条正式入口”“需要补一个不属于当前 acceptance 的 UI surface”。

---

## 一点六、Current Micro Brief

在开始搜索、编码或验证前，先把**当前会话**要完成的最小切片收敛成下面 4 行；这里服务的是本轮执行，不替代 proposal、change 三件套或长期状态源。

```text
目标：<这一次会话要达成的单一行为>
锚点文件/符号：<唯一文件 + 尽量唯一符号>
当前失败/缺口：<当前断言失败、行为缺失或控制路径缺口>
验收命令：<最小可执行验证命令>
```

填写规则：

1. 每次会话默认只维护 1 个 `Current Micro Brief`；若出现第二目标，先拆 follow-up，不要并入当前会话。
1. `锚点文件/符号` 至少写到 1 个文件；优先再写函数、类、测试名、CLI 子命令或模板名，避免执行时重新大范围搜索。
1. `验收命令` 默认先写最小验证：先单测/单文件，再 focused smoke，最后才是聚合测试；不要把大套件写成当前会话的默认第一验收。
1. 若当前会话只承接 proposal、change 或聊天需求，而没有现成执行切片，AI 应先在这里补齐 `Current Micro Brief`，再开始搜索和修改。

---

## 二、能力映射 / Capability Mapping

这组字段用于把本次 change 绑定到长期知识归宿，避免“改完了但不知道该回写哪里”。

```text
- capability_id: <稳定主题标识>
- capability_name: <中文主题 / English Topic>
- long_term_target: <长期文档主归宿，若无则写 无>
- secondary_targets: <可选的次级回写目标，若无则写 无>
- decision_target: <若涉及长期取舍，填写 ADR 路径；否则写 无>
- affects_long_term_rules: 是 / 否
- change_type: 新增规则 / 修改规则 / 废弃规则 / 纯实现 / 验证确认
```

填写约束：

1. `long_term_target` 只能有一个主归宿，写到具体文档路径，不要只写目录名。
1. `affects_long_term_rules=否` 或 `change_type=纯实现` 或 `change_type=验证确认` 时，也必须显式写 `long_term_target: 无`。
1. 若后续确实发生长期回写，必须在目标长期文档底部维护 `## 相关变更 / Related Changes`，登记当前 `change-id`。
1. 若文档会引用正式 artifact，则 `artifact_boundary.trusted_artifact_roots` 必须填写当前 change 唯一允许信任的 artifact 根；`allowed_evidence_roots` 只用于 repo-local 证据归档，不得把其他 case root 塞进该字段伪装成本地证据。

---

## 三、AI 执行约束

> 分工约定：本节只写“任务级修改边界、正式入口、必跑验证”；验收专属口径写入 `acceptance.md`，启动/执行协议写入 `ai_constraints.md`，不要三处重复抄写同一套边界。

建议至少写清楚：

1. 允许修改的目录或文件
1. 禁止修改的目录或文件
1. 本次应修改的正式入口与主要实现落点
1. 当前 change 允许引用哪些 artifact 根，哪些根明确禁止引用
1. AI 开始前必须阅读的上下文文档
1. 改完后必须执行的验证命令
1. 若验收目标不明确，优先补 acceptance，不得直接跳过进入编码

补充硬规则：

1. 若计划中引用 `L3`，默认语义是“发布前静态收口”，对应 `python scripts/verify.py --profile l3`，**不包含回测冒烟**。
1. 若需要回测链路冒烟，必须显式写为 `release` 或单独写“回测冒烟”，对应 `python scripts/verify.py --profile release`；禁止把回测冒烟混写进 `L3`。
1. 若当前仓库提供 `python scripts/run_layered_tests.py <scope>`，ordinary change 默认应先写清 `L0` 文档守卫与 `L1` 定向测试；只有确实需要专项分层回归时，才在 `fast / default / runtime / all` 中声明目标测试层。
1. `python scripts/run_layered_tests.py all` 或等价 `alltest` 只用于最终发布、最终验收或 topic 明确要求的收口；不得把 `all` 写成普通 change 的日常默认命令。
1. 风险分级要求：`governance_risk=low` 可省略 `acceptance.md` 与 `ai_constraints.md`；`governance_risk=medium/high` 必须保留三件套并通过 `check_change_docs.py` 门禁。
1. 若当前 change 进入正式验收，默认必须在 `acceptance.md` 定义至少 6 个真实验收场景；少于 6 个时，必须在 `acceptance.md` 明确写出豁免理由与风险边界。
1. `pytest`、`unittest`、`dotnet test` 等 test 命令只可作为 contract/function 锁定证据，不得写成正式 change 验收通过依据。
1. 若 `plan.md`、`acceptance.md`、`ai_constraints.md` 中出现 artifact 路径，必须全部落在 `artifact_boundary.trusted_artifact_roots` 或 `artifact_boundary.allowed_evidence_roots` 下；不得引用 sibling change、其他 case、历史 debug 输出或“这次顺手可复用”的外部 artifact。
1. 第一处实质编辑应优先落在「防跑偏收敛卡」声明的 `第一刀落点`；除非验证结果证明该处不控制目标行为，否则不要先并行改第二处实现。
1. 第一处实质编辑后，下一步必须执行「防跑偏收敛卡」声明的 `首个验证动作`；不得先继续补第二组改动、扩读相邻模块或顺手清理无关问题。
1. 若执行过程中命中 `超范围触发条件`，必须先回填计划、收窄范围或拆 follow-up change，不得把新目标直接并入当前 change。

## 首批 Guard 引用 / First-Batch Guard References

若当前 change 触及以下任一类 guard，建议在计划中显式引用对应口径与最小锁定：

1. `Schema Guard / 对象边界守卫`
2. `Smoke Guard / 正式入口守卫`
3. `Layer Guard / 分层边界守卫`
4. `Fail-fast Guard / 红线拒绝守卫`
5. `Harness Integration / 套件接入口`

原则：

1. 不是所有 change 都必须覆盖全部 5 类 guard。
2. 但若 change 本身就在修改这些边界，就不应只写“改文档”而不写 guard 回链。
3. 推荐在「三、AI 执行约束」或「七、任务清单」里写明本次引用了哪一类 guard、最小验证是什么。

---

## 四、背景与约束（可选）

## 四、UI Surface Freeze 三锁 / UI Surface Freeze Three Locks

> 当本 change 修改 `report_surfaces/`、`*.html.j2`、`context_builder.py`、Factor Board、Portal Case、Dev Home、Case Assurance 或其他 live UI surface 时，必须填写本节；否则可删除。

| 锁 | 当前回答 |
| --- | --- |
| Visibility Contract Lock | 锁定了哪些旧功能/新功能/DOM marker/links/blockers；对应 focused tests 在哪里 |
| Read-Model Boundary Lock | 页面消费哪个 canonical read-model / projection payload；如何证明没有 route-time artifact scan / case-id dispatch |
| Live Surface Smoke Lock | 哪个 live route 或 surface 做了 smoke；断言了哪些 marker、links、blockers 和错误状态 |

---

## 五、背景与约束（可选）

> 背景复杂、目标边界需要明确时展开本章节；简单变更可删除此章。

建议写清楚：

1. 目标（2-4句）
1. 范围与非目标
1. 成功标准
1. 必读上下文文档
1. 影响面概览

---

## 六、设计方案（可选）

> 方案分叉明显、需记录入口落点或发布回滚方案时展开本章节；简单变更可删除此章。

建议写清楚：

1. 现状与正式入口落点
1. 设计方案（总体思路、关键模块改动、异常处理口径）
1. 备选方案（至少一个）+ 选择理由
1. 发布回滚与退出策略（仅指发布/部署/迁移层面，不等于运行时 fallback）
1. 风险与影响面
1. 需沉淀为长期规则的内容

---

## 七、阶段划分（可选）

> 单阶段即可完成的小变更可删除此章。

按阶段说明这次实施如何推进。

示例：

1. 阶段 1：补齐入口与骨架
1. 阶段 2：补齐测试与验证
1. 阶段 3：补齐文档与验收记录

---

## 八、任务清单

| 步骤 | 任务 | 来源 | 修改文件 | 产出 | 验证动作 | 回写目标 | 完成定义 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | <示例：新增统一入口脚本> | <A1 / capability:xxx / 长期规则:xxx> | <文件路径> | <脚本文件> | <命令> | <长期文档路径或 无> | <命令可运行，返回码正确> | 未开始 |
| P2 | <示例：补齐状态文件输出> | <A2 / capability:xxx> | <文件路径> | <状态文件/日志> | <命令或检查项> | <长期文档路径或 无> | <输出字段与设计一致> | 未开始 |
| P3 | <示例：补齐测试> | <E3 / 长期规则:xxx> | <文件路径> | <测试文件> | <pytest 命令> | <长期文档路径或 无> | <关键测试通过> | 未开始 |
| P4 | <示例：补齐文档> | <change_type / rule delta> | <文件路径> | <专题文档/README> | <对照检查> | <long_term_target 或 decision_target> | <与实现一致> | 未开始 |
| P5 | <示例：执行验收> | <A1-A3 / Exit Criteria> | <文件路径> | <验收记录> | <验收命令> | <相关变更登记或 无> | <关键场景验证完成> | 未开始 |

状态建议统一使用：

- `未开始`
- `进行中`
- `已完成`
- `阻塞`

补充约束：

1. 任务顺序默认应体现“先澄清验收，再开发实现，再执行验收”。
1. 若某任务无法映射到 acceptance 场景、出口条件或证据要求，应先解释其必要性，否则不要加入计划。
1. 当 `change_type=验证确认` 时，任务清单允许不含代码实现步骤；只需列出验证动作、证据收集与结论记录，即可直接进入验收闭环。
1. 第一条“实质编辑”任务后面，默认应紧跟一条 focused validation；不要把所有验证堆到最后一次性执行。

<!-- TASK-LIST-BEGIN
- [ ] T1: [第一个原子任务]
- [ ] T2: [第二个原子任务]
- [ ] T3: [第三个原子任务]
TASK-LIST-END -->

---

## 九、任务说明（可选）

> 任务清单表格已足够描述时可删除此章。

如果某些步骤较复杂，可在这里补充每一步的细节。

建议写清楚：

1. 依赖谁先做
1. 修改哪些文件
1. 是否需要联调
1. 是否需要远程环境配合

---

## 九、验证动作（可选）

> 任务清单表格的“验证动作”列已足够时可删除此章。

列出开发过程中每个阶段的验证动作，不要只在最后一次性验证。

建议至少包含：

1. 本地命令验证
1. 测试验证
1. 关键日志/状态文件验证
1. 远程或集成验证
1. 反模式扫描

示例：

```text
1. python <script> --help
2. pytest tests/<target> -q
3. python scripts/verify.py --profile l3
4. python scripts/verify.py --profile release  # 仅当本次明确需要回测冒烟
5. 检查 latest_status.json 字段是否齐全
6. 检查 workflow / dispatch / issue comment 是否串联
7. python scripts/check_antipatterns.py
```

---

## 十、完成定义（可选）

> acceptance.md 已明确完成定义时可删除此章；首次使用模板建议保留作为提醒。

这一节必须明确“开发完成”不等于“验收完成”。

建议采用两层定义：

### 开发完成

满足以下条件：

1. 代码已实现
1. 关键测试已通过
1. 相关文档已更新
1. 反模式扫描已执行并确认结果
1. 已具备进入 `acceptance.md` 执行验收的前提，而不是停留在“我觉得已经差不多”

### 交付完成

除开发完成外，还需满足：

1. `acceptance.md` 中关键场景已执行
1. 验收结论已记录
1. 证据路径已补齐并可追溯
1. 高频原始证据已按需外置到 `output/`，change bundle 仅保留摘要与索引
1. 长期文档或 `ADR` 已按需回写，或显式说明“本次无长期沉淀项”

提示：本模板默认不是“先开发、再顺手补验收”，而是“以验收倒推开发，再以验收收口交付”。

---

## 十一、长期规则增量摘要 / Long-Term Rule Delta Summary

这一节只写本次 change 对长期规则的增量，不重复实现细节。

```text
### 新增规则
- <规则 1>

### 修改规则
- <规则 2：从什么改成什么>

### 废弃规则
- <规则 3>
```

如果 `change_type=纯实现` 或 `change_type=验证确认`，也请显式写：

```text
本次无长期规则增量，仅涉及局部实现 / 仅验证确认。
```

---

## 十二、回写与相关变更 / Write-back & Related Changes

当 `long_term_target != 无` 时，收尾前必须明确这一条链是否闭合：

1. `plan.md` 已声明 `long_term_target`
1. 长期文档已完成回写，或已记录“本轮暂不回写”的原因
1. 若已回写，在目标长期文档底部维护：

```markdown
## 相关变更 / Related Changes

1. `docs/changes/{{change-id}}/`
```

1. 若本次涉及长期取舍，`decision_target` 对应的 `ADR` 已补齐或已明确不需要

---

## 十三、阻塞项（可选）

> 无阻塞时可删除此章。

记录当前阻塞实施的事项。

建议写清楚：

1. 阻塞内容
1. 影响范围
1. 临时处理方式
1. 解除阻塞条件

如果没有，可写：

```text
当前无阻塞项。
```

---

## 十四、进度记录（可选）

> 单轮即完成的小变更可删除此章。

建议按精确到分钟的时间追加简短记录，统一使用 `YYYY-MM-DD HH:MM` 格式。

示例：

```text
2026-03-14 09:30：完成入口脚本骨架与状态文件定义。
2026-03-15 15:30：完成测试补齐，开始联调验证。
```

如无需记录过程，可直接删除本章。
保留本章时，最后一条记录后不要再留空白段。
