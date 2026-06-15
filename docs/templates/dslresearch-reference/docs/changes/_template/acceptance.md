# <变更名称> 验收方案 / Acceptance Plan

<!-- CHANGE-ANTI-DRIFT-GATE:v1 -->

**模板标识 / Template Marker**：standard
**变更目录 / Change Root**：./
**状态**：⬜ 待执行
**日期**：YYYY-MM-DD
**范围**：[影响目录/模块]
**proposal-id**：[可选；若当前 change 由 proposal 编排则填写，例如 p012-case-short-reference-numbering]
**topic-id**：[可选；若当前 change 同时归属长期 roadmap/topic 则填写]
**change-id**：{{change-id}}
**当前展示名 / Current Display Name**：[可选；当当前正式名称与历史 change-id 指向名称不一致时填写]
**关联 plan**：./plan.md
**关联 ai_constraints**：./ai_constraints.md
**长期归宿 / Long-Term Target**：[长期文档主归宿或 无]

> 说明：`change-id` 是当前变更的唯一标识，不应与其他 change 共用。若当前 change 由 proposal 编排，应优先填写 `proposal-id` 作为直接上层关联；只有当该 change 同时归属长期 roadmap/topic 时，才补充 `topic-id` 作为长期追踪锚点。
> 命名规则：若当前正式展示名已调整，但历史 `change-id` 作为证据锚点不便回改，应填写 `当前展示名 / Current Display Name`，并在这里说明“旧 `change-id` 仅保留用于维持证据链与回链稳定性”。若不存在展示名与 `change-id` 名称分离，可删除该字段。
> **元数据主来源规则：**通用变更元数据以 sibling `plan.md` 头部为准；本文件只保留验收收口必需字段，避免与 `plan.md` 长期双向同步。
> **由人填写，在提给 AI 之前写好。AI 可以执行验收并更新验收结论；只要是真实环境、真实入口、真实证据满足出口条件，AI 可直接宣告本 change 验收通过。仅凭 mock/stub 结果不得宣告正式验收通过。**
> **写权限规则：**人工负责验收目标、范围、前置条件、出口条件定义与场景定义。`AI-STATUS` YAML 是唯一 **AI 执行状态源**；AI 可更新 `AI-STATUS`、执行记录、证据清单，并按 YAML 同步 Dashboard 与最终结论中的派生值。
> **顶部状态规则：**顶部 `**状态**` 由当前验收阶段驱动，不得长期停留在模板默认值。AI 完成真实执行留证且满足出口条件后，应直接把它更新为 `✅ 已验收`；若尚未满足出口条件，则保持为进行中或未通过状态，不得使用人工确认占位态作为中间态。
> **开发方法规则：**本 change 默认采用 **Acceptance-First / ATDD-lite**。这里的重点是“先定义 acceptance”，不是“用 test 代替验收”。`acceptance.md` 是正式验收主约束文件：**test 只能锁定 contract 与 function，不能拿来做 change 验收；正式验收不能 mock，不能用 pytest/unittest/dotnet test 结果直接充当通过依据。**
> **场景数量规则：**每个 change 正式验收场景默认不少于 6 个，建议结构为 3 个 success、2 个 failure、1 个 boundary。若确实少于 6 个，必须在本文件明确写出豁免理由、风险边界与为什么仍足以判定通过。
> **闭环验证规则：**若本轮声称某个 blocker、gap、negative case 或 `next_action` 已消解，必须补一条真实闭环回验证据，至少覆盖 `expected artifact -> reverify command -> observed result -> gap status`；只写“已修复”“页面已更新”或只贴 test 绿灯，不构成正式通过依据。
> **收口信号规则：**本文件必须显式写出“唯一通过信号 / Single Pass Signal”与“最小闭环回验 / Minimum Closed-loop Reverify”。若两者任一缺失，AI 不得把“测试全绿”“页面可打开”“命令跑完”写成正式通过结论。
> **证据真实性规则：**本文件引用的测试名、probe 名、命令、artifact 路径必须能在仓库、正式入口或证据目录中核对到真实对象；不得引用不存在、已改名或无法定位的对象作为通过证据。
> **Artifact Root Rule / Artifact 根约束：**本文件出现的正式 artifact 路径必须属于 sibling `plan.md` 头部 `artifact_boundary.trusted_artifact_roots`；repo-local 证据归档只能放在 `artifact_boundary.allowed_evidence_roots`。不得把其他 case、其他 proposal、debug 历史目录或临时产物写成当前 change 的正式证据。

---

<!-- AI-STATUS-BEGIN — AI 只应更新此 YAML 块中的验收执行状态 -->

```yaml
conclusion: pending          # pending | passed | partial | failed
allow_declare_pass: false
last_updated: "YYYY-MM-DD HH:MM"
concluded_by: ""

exit_conditions:
  E1_success_scenarios: pending    # pending | passed | failed
  E2_failure_scenarios: pending
  E3_verification_cmds: pending
  E4_evidence_collected: pending
  E5_real_acceptance_only: pending
  E6_minimum_scenarios: pending
  E7_closed_loop_reverify: pending

scenarios:
  A1: { exec: false, result: null, blocking: true }
  A2: { exec: false, result: null, blocking: true }
  A3: { exec: false, result: null, blocking: true }
  A4: { exec: false, result: null, blocking: true }
  A5: { exec: false, result: null, blocking: true }
  A6: { exec: false, result: null, blocking: true }
  # A7, A8... 按需追加

# 语义约束：
# - exec=true 只表示“本轮已执行/已尝试”，不表示通过。
# - result=passed|failed 才表示场景结果；exec=true 且 result=failed 是合法且常见状态。
# - AI 不得把“任务存在 / 入口已映射 / 命令已触发”推断成 passed，除非成功信号满足场景定义。

```

<!-- AI-STATUS-END -->

## 状态图标约定 / Status Legend

| 图标 | 含义 | YAML 值 | 说明 |
| :---: | ------ | --------- | ------ |
| ⬜ | 未执行 | `pending` | 尚未开始 |
| 🔄 | 执行中 | `in_progress` | 正在进行 |
| ✅ | 通过 | `passed` | 本轮已验证通过 |
| ❌ | 未通过 | `failed` | 本轮验证失败 |
| 📎 | 历史参考 | `historical` | 以前做过，**不算**本轮通过 |

---

## 总览看板 / Dashboard

> 本看板是上方 `AI-STATUS` 的**派生视图 / generated dashboard**，也是脚本同步区。AI 每次更新 YAML 后，必须同步这里的验收结论、AI 建议、时间、执行人、出口条件与场景结果；若两者冲突，以 YAML 为准并立即修正派生行。场景看板中的 `执行/结论/证据备注` 应由 AI 在本轮真实执行后主动回填，不得留空等待补写。

### 验收总状态 / Overall

| 项目 | 值 | 说明 |
| --- | :---: | --- |
| 验收结论 | ⬜ 待执行 | 由 `AI-STATUS conclusion` 派生 |
| AI 建议宣告通过 | 否 | 由 `AI-STATUS allow_declare_pass` 派生 |
| 最后更新 | YYYY-MM-DD HH:MM | |
| AI 执行人 | — | 由 `AI-STATUS concluded_by` 派生 |

### 出口条件 / Exit Criteria

| # | 出口条件 | 状态 | 判定规则 | 证据 |
| --- | --- | :---: | --- | --- |
| E1 | 关键成功场景全部通过 | ⬜ | | |
| E2 | 关键失败场景符合预期 | ⬜ | | |
| E3 | 必跑验证命令已完成 | ⬜ | | |
| E4 | 关键证据已留存 | ⬜ | 证据至少能回链到真实命令、artifact、测试或 probe，且引用对象可核对 | |
| E5 | 正式验收不依赖 mock 或 test | ⬜ | 只接受真实入口、真实环境、真实产物与真实证据；test 仅用于 contract/function 锁定 | |
| E6 | 正式场景数不少于 6 个 | ⬜ | 少于 6 个时必须存在明确豁免理由与风险边界 | |
| E7 | 涉及修复/消解时已完成闭环回验 | ⬜ | 若本轮声称 gap、blocker、negative case 或 next action 已消解，必须记录 `expected artifact -> reverify command -> observed result -> gap status` | |

### 场景看板 / Scenario Board

> 阻塞=是 的场景未通过时，总结论不得写 已验收。
> `执行` 只回答“本轮有没有真的跑/试过”；`结论` 才回答“跑出来是通过还是失败”。
> 因此 `执行=✅, 结论=❌` 表示“真实执行过，但本轮失败”，不得再写成通过。
> 非阻塞场景可以作为边界探索、风险暴露或补充信息保留在表中；它们若失败，必须解释影响范围与为什么不推翻最终验收结论。
> 不要再新增单独的“是否已验收 / 是否成功验收”列；场景层只表达执行与结果，正式验收只在总览看板顶部状态与“最终结论”中表达。

| # | 场景 | 执行 | 结论 | 阻塞 | 证据/备注 |
| --- | --- | :---: | :---: | :---: | --- |
| A1 | Success 1: 主路径成功 | ⬜ | ⬜ | 是 | |
| A2 | Success 2: 次主路径成功 | ⬜ | ⬜ | 是 | |
| A3 | Success 3: 关键变体成功 | ⬜ | ⬜ | 是 | |
| A4 | Failure 1: 关键失败路径 | ⬜ | ⬜ | 是 | |
| A5 | Failure 2: 另一类失败路径 | ⬜ | ⬜ | 是 | |
| A6 | Boundary 1: 边界场景 | ⬜ | ⬜ | 否 | |

### 判断规则 / Quick-Judge

1. 任一 阻塞=是 的场景结论不是 ✅ → 最终结论不得写 已验收
2. 📎 只表示历史做过，**不算**本轮通过
3. 若 `AI-STATUS` 与总览看板中的派生行冲突，以 `AI-STATUS` 为准并立即同步看板
4. E1-E7 全 ✅ 且所有阻塞场景均为 `执行=✅ / 结论=✅` → AI 应把“AI 建议宣告通过=是”，并可直接把顶部 `**状态**` 与最终结论更新为“已验收”；若存在非阻塞场景失败，必须同时写清影响范围、保留风险与为什么仍不否定验收目标
5. 只有最终结论明确写为“已验收”，才算正式验收完成
6. `执行=✅` 不得被解释为 `结论=✅`；若场景真实执行但失败，必须显式写成 `执行=✅ / 结论=❌` 并回填失败根因。
7. 任何 mock/stub/test 输出都不能单独满足 E5；若正式场景不足 6 个，E6 不得写通过。
8. 若本轮声称已修复断链或已消解 blocker/gap，而 E7 仍非 ✅，最终结论不得写“已验收”。
9. 若「唯一通过信号 / Single Pass Signal」未被真实命中或其闭环回验尚未完成，最终结论不得写“已验收”。

---

## 一、验收目标 / Goals

用结果语言书写：

1. 证明 …
2. 证明 …

填写提醒：

1. 目标要能倒推出开发范围。
2. 目标要能被实际验证，而不是抽象口号。
3. 若这里写不清楚，默认说明功能定义还不完整，应先澄清再开发。

---

## 一点五、单一通过信号与闭环回验 / Single Pass Signal And Closed-loop Reverify

先写清楚“什么现象出现才算这次 change 真的成立”，再写场景矩阵。该区块用于防止执行过程中把“代码已改”“测试绿灯”“页面打开了”误判成通过。

| 项 | 当前填写 |
| --- | --- |
| 唯一通过信号 / Single Pass Signal | <一句话写出 change 真正成立时，外界能观察到的结果> |
| 不算通过的伪信号 / Non-Pass Signals | <例如 test 绿灯 / 页面能打开 / 日志无报错，这些为什么不能单独判定通过> |
| 最小闭环回验 / Minimum Closed-loop Reverify | <哪个正式 reader / reducer / projection / surface 必须重新读取新 artifact 或新状态> |
| 失效即停止扩面 / Stop-Expand Condition | <若该信号被证伪，本轮必须先修同一 slice，不得扩到第二战场> |

填写规则：

1. `唯一通过信号` 必须是可观察结果，不得写成“代码存在”“入口已接入”“测试通过”。
1. `最小闭环回验` 必须指向正式 consumer，而不是开发期 stub、手工推断或仅开发态日志。
1. 若当前 change 是修复断链、消解 blocker 或完成 `next_action`，`最小闭环回验` 应直接覆盖那条断链的正式读路径。
1. 若这里写不清楚，说明验收目标还没收敛；应先修正文档，不要直接进入实现。

---

## 二、验收范围 / Scope

### 覆盖（In Scope）

1. …

### 不覆盖（Out of Scope）

1. …

---

## 三、前置条件 / Prerequisites

| 条件 | 类型 | 阻断开发 | 阻断验收 | 状态 | 备注 |
| --- | --- | :---: | :---: | :---: | --- |
| [示例：目标环境可执行 Python] | 环境 | 是 | 是 | ⬜ | |
| [示例：通知凭据已配置] | 凭据 | 否 | 是 | ⬜ | |

---

## 四、验收专属 AI 边界 / Acceptance-Only AI Boundaries

1. 任务级修改边界、正式入口、必跑验证命令，以 sibling `plan.md` 的「三、AI 执行约束」为准；本节不重复维护。
2. 本节只补充验收收口专属边界，例如：哪些证据算有效、哪些场景必须真实执行、哪些结论 AI 不得改写。
3. AI 可以更新 `AI-STATUS`、Dashboard 派生值、场景看板、证据清单与最终结论。
4. 正式验收只接受真实入口、真实环境、真实产物、真实记录与真实证据；`pytest`、`unittest`、`dotnet test`、mock、stub、monkeypatch、假对象、伪造返回值都不能单独构成正式通过结论。
5. test 只用于锁定 contract 与 function，可作为开发质量证据单独记录，但不得写成当前 change 的正式验收通过依据。
6. change 实现完成后、回填本文件证据前，必须编写 `[CONTRACT-LOCK]` 测试锁定本次引入或修复的关键行为；断言行尾标注 `# [CONTRACT-LOCK: <行为描述>]`，测试默认放在 `tests/<domain>/test_<module>.py`；若改动影响 UI surface / context_builder / template，可按 owner 落在 `tests/report_surfaces/` 或 `tests/orchestration/`。未写即回填视为证据不足，不得宣告验收通过。
7. 默认必须定义至少 6 个正式验收场景；若少于 6 个，必须在本文件明确补写"豁免说明 / Scenario Waiver"，写清减少原因、遗漏风险与为什么仍足够判定。
8. AI 应先对照本文件确认"做成什么才算通过"，再回到 `plan.md` 拆解任务；不得先写实现、最后才回来补验收口径。
9. 若本轮目标包含修复断链、消解 blocker/gap 或完成 `next_action`，AI 必须追加一次真实闭环回验：至少让正式 reader、reducer、projection、surface 或等价正式入口重新读取新 artifact 或新状态。
10. AI 不得把不存在、已改名或无法定位的测试、probe、命令或 artifact 写成通过证据；发现引用漂移时，必须先更正文档或补真实证据，再谈通过。
11. 任何正式 artifact 引用都必须回链到 sibling `plan.md` 的 `artifact_boundary.trusted_artifact_roots`；若 evidence path 超出该边界，即使对象真实存在，也不得作为当前 change 的通过证据。
12. 非阻塞场景可以失败，但不得被忽略；必须在场景备注、证据清单或“未通过处理”中写清失败根因、影响边界与是否需要 follow-up。

---

## 七、UI Surface Freeze 证据 / UI Surface Freeze Evidence

> 当 sibling `plan.md` 的 `ui_surface_freeze.required=true`，或本 change 明确触及 UI surface owner 时，必须填写本节；否则可删除。

| 锁 | 证据摘要 | 证据路径/命令 |
| --- | --- | --- |
| Visibility Contract Lock | 哪些 CONTRACT-LOCK / focused tests 锁住旧功能、新功能、DOM marker、links、blockers | `python -m pytest <focused-ui-tests>` |
| Read-Model Boundary Lock | 页面只读取哪个 canonical payload；本轮如何证明没有 route-time artifact scan / case-id dispatch | `<projection / owner test or evidence path>` |
| Live Surface Smoke Lock | 哪个 live route/surface 被 smoke；本轮断言了哪些 marker、links、blockers、错误状态 | `<live route command or evidence path>` |

---

## 五、验收场景 / Scenarios

> **成功信号写法（ATDD-lite）**：填可观测结果，而非抽象描述。
>
> - ✅ `退出码=0`、`JSON 含 "status": "ok"`、`日志关键字 "已初始化"`
> - ❌ `验证正常`、`无报错`、`调用成功`（不可观测，不算通过信号）
> - 若仓库内尚无独立 ATDD-lite 规范文档，以本表中的“执行命令/步骤 + 预期结果 + 成功信号 + 失败口径”四列作为最小冻结口径。

| # | 场景 | 执行命令/步骤 | 预期结果 | 成功信号 | 失败口径 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Success 1: 主路径成功 | | | | | |
| A2 | Success 2: 次主路径成功 | | | | | |
| A3 | Success 3: 关键变体成功 | | | | | |
| A4 | Failure 1: 关键失败路径 | | | | | |
| A5 | Failure 2: 另一类失败路径 | | | | | |
| A6 | Boundary 1: 边界场景 | | | | | |

补充规则：

1. 若当前 change 的目标是“修复断链后重新打通主路径”，建议追加 `A7 Closed-loop Reverify` 场景，专门证明新 artifact 已被正式 consumer 重新读取。
2. `A7` 的成功信号应优先写成可观测的 reader/reducer/surface 结果，而不是“代码已修改”或“测试已通过”。
3. 至少一个阻塞型 success 场景应直接覆盖上方 `Single Pass Signal`，不要把最关键通过信号只留在边界场景或备注里。

---

## 六、证据清单 / Evidence

> **记录原则 / Evidence Logging Rule**
>
> 1. `acceptance.md` 默认只保留“证据索引 + 关键摘要 + 判定关系”，作为验收总控页。
> 2. 单条命令、短摘要、可在 3-5 行内说清的证据，可直接写在本文件。
> 3. 原始长输出、完整日志、JSON/HTML 报告、截图、benchmark 明细，默认优先落到 sibling `plan.md` 声明的 repo-local evidence roots，必要时再在当前 change 下保留简短 `执行证据_Execution Evidence.md` 索引页。
> 4. `执行证据_Execution Evidence.md` 若存在，默认只做“场景 -> 证据路径 -> 关键结论”的人读摘要，不重复堆放原始日志。
> 5. 无论证据是否外置，本表都必须写清：它证明哪个场景/出口条件、路径在哪、为什么足够。
> 6. 不要把大段原始输出整段粘贴进本文件，避免验收结论被噪音淹没。
> 7. 若涉及闭环回验，证据摘要至少写清 `expected artifact -> reverify command -> observed result -> gap status`，避免只留下结果判断而没有回验链路。
> 8. 本表引用的测试、probe、命令、artifact 路径必须可核对；若对象已改名或消失，应先修正引用，不得继续作为通过依据。
>
> 9. 若这里记录的是正式 artifact，而不是 repo-local 执行留痕，其路径必须位于 sibling `plan.md` 声明的 `artifact_boundary.trusted_artifact_roots`；否则视为跨 case / 跨 change 引用。

| # | 证据类型 | 路径/链接 | 说明 |
| --- | --- | --- | --- |
| 1 | | | |

---

## 八、未通过处理 / On Failure

1. 回退到 plan.md 重新制定修复计划
2. 不得覆盖已通过的历史证据；需修复时新开 change-id
3. 是否允许带已知问题进入下一阶段：是 / 否
4. 重新发起验收负责人：

---

## 九、豁免说明 / Scenario Waiver

> 默认要求是至少 6 个正式验收场景。只有在场景确实无法再细分、且减少不会削弱判定力时，才允许填写本节；否则本节可删除。

| 项目 | 内容 |
| --- | --- |
| 当前场景总数 | |
| 少于 6 个的原因 | |
| 缺失场景带来的风险 | |
| 仍足以判定通过的理由 | |
| 审核结论 | |

---

## 十、真实验收待办清单 / Pending E2E Checklist

> 当某个场景当前只有 contract/function test、局部预验证或其他非正式证据时，必须补这张表，明确“下一步真实验收还差什么”。

| # | 对应场景 | 当前阶段结果 | 还缺的真实验证 | 真实入口/命令 | 通过信号 | 阻塞项 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | A1 | 例：contract/function test 通过 | 例：真实 SMTP 投递到收件箱 | | | | |
| R2 | A4 | 例：contract/function test 通过 | 例：80.56 远端真实链路执行 | | | | |

填写规则：

1. 只要某场景当前只拿到了 contract/function test 或其他预验证结果，就应至少补一条 `R*` 待办。
2. `当前阶段结果` 固定写清：是“contract/function test 通过”“预验收通过”还是其他中间状态。
3. `还缺的真实验证` 要写具体依赖，不要只写“联调”或“E2E”。
4. `真实入口/命令` 优先填写正式入口，例如远端任务、正式 CLI、真实收件箱确认步骤。
5. 这张表未清空前，总结论默认不得写“已验收”。
6. 若本轮宣称已修复某个 gap/blocker，但这里只留下 test 或预验证结果、没有真实闭环回验，则对应项不得关闭。

---

## 十一、Contract/Function 锁定证据（可选）

> 本节仅记录 test 对 contract 与 function 的锁定情况。它不参与正式验收结论判定，不能替代上方真实场景。

| 项目 | 路径/命令 | 说明 |
| --- | --- | --- |
| Contract 锁定 | | |
| Function 锁定 | | |

---

## 十一、最终结论 / Final Verdict

### 最终结论 / Final Verdict

- **结论**：⬜ 待执行

- **日期**：

- **执行人**：

- **建议**：暂不建议宣告通过 / 可宣告通过

- **说明**：

说明：最终结论用于表达“本 change 是否已完成真实执行、留证并正式验收通过”。若仍停留在“待执行 / 执行中 / 未通过”，则任务尚未完成正式验收闭环。

补充：`scripts/tools/update_ai_status.py` 与 `scripts/tools/sync_acceptance_dashboard.py` 只负责同步 AI 派生值，不负责额外交互确认；是否可宣告通过，以本文件出口条件与证据是否满足为准。
