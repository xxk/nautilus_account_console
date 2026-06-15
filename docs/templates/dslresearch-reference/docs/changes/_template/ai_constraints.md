# OpenSpec-lite AI 执行约束 / OpenSpec-lite AI Execution Constraints

<!-- CHANGE-ANTI-DRIFT-GATE:v1 -->

**模板标识 / Template Marker**：standard
**变更目录 / Change Root**：./
**change-id**：{{change-id}}
**关联 acceptance**：./acceptance.md
**关联 plan**：./plan.md

> 通用变更元数据以 sibling `plan.md` 头部为准；本文件只保留启动执行所需锚点，避免和 `plan.md` 双向同步同一批头字段。

## 最低内容门槛 / Minimum-Depth Contract

`ai_constraints.md` 不要求写成长文，但对 `medium/high` change，至少必须独立回答下面四个问题：

1. **入口补齐**：若当前只拿到本文件，AI 该先读哪些 sibling 文档。
2. **任务边界**：本 change 明确不能改什么、不能靠什么捷径通过。
3. **最小验证**：做完后最少必须跑哪些命令或检查哪些正式入口。
4. **收尾动作**：若涉及 proposal / 长期文档 / related changes，同步要求是什么。

若正文不足以独立回答这四类问题，即使存在 `change-id`、`关联 acceptance`、`关联 plan` 头字段，也不算满足 minimum-depth contract。

建议最少保留以下 5 个一级章节：

1. `单文档启动 / Standalone Kickoff`
2. `方法论 / Working Mode`
3. `启动步骤 / Kickoff`
4. `边界 / Boundaries`
5. `收尾 / Wrap-up`

## 单文档启动 / Standalone Kickoff

若当前只把本文件发给 AI，本文件可直接作为启动提示。默认规则不是“先停下来等用户继续补材料”，而是“先主动补齐 sibling docs，再开始执行”。只有在确实无法读取关联文档时，才允许停下索取补充材料。

### 单文档启动硬规则 / Hard Rules For Standalone Kickoff

1. 若 AI 运行在仓库/IDE 工作区内，且可访问文件系统，**必须主动读取**当前 change 目录下的 `acceptance.md` 与 `plan.md`，不得因为用户只贴了 `ai_constraints.md` 就先停下来提问。
2. `关联 acceptance` 与 `关联 plan` 是默认读取入口；若头部仍为相对路径 `./acceptance.md`、`./plan.md`，应将其解释为“相对于当前 `ai_constraints.md` 所在目录”的 sibling 文件。
3. 只要 sibling 文件可读，就应直接进入执行循环：读取约束、锁定最小阻塞、实施修改、运行验证、回填状态。
4. 只有在以下任一条件成立时，才允许先停止并向人工索取补充信息：

   - 关联文档不存在或无法访问
   - 关联文档彼此冲突，且无法从仓库事实中消解
   - 验收目标本身缺失，无法判断“做成什么才算完成”
   - 缺少必要权限、环境或外部依赖，导致无法继续执行
5. 若 AI 不具备文件系统访问能力，只拿到纯文本粘贴内容，则必须明确说明缺的是哪份 sibling 文档或哪项环境上下文；但只要在 VS Code / 仓库代理环境中能自行读取文件，就不得把“请把 acceptance.md 也发我”当默认第一步。

补齐顺序如下：

- 先把 `变更目录 / Change Root` 视为当前 change 根目录。
- 先读取 `关联 acceptance`，确认验收目标、出口条件、场景与 AI 写权限。
- 再读取 `关联 plan`，确认任务拆解、修改边界、验证动作与长期回写目标。
- 只有在 `acceptance.md` 与 `plan.md` 都可访问时，才进入开发/验证循环。
- 若任一关联文档缺失、路径失效或内容矛盾，必须先停止执行并明确索取缺失文档或人工澄清，而不是基于猜测直接编码。

## 方法论 / Working Mode

本 change 默认采用 **Acceptance-First / ATDD-lite**：先定义验收收敛目标，再进入实现与验证。这里的 ATDD-lite 指“先定义 acceptance”，**不表示可以用 test、mock 或 stub 替代正式 change 验收**：

1. 先确认功能目标与验收目标，再开始开发。
2. 开发计划必须围绕验收场景、出口条件和证据要求展开，而不是先写代码再补验收。
3. 开发完成不等于任务完成；只有回到 `acceptance.md` 完成场景验证、补齐证据并收敛结论，才算真正收口。
4. 若功能定义尚不稳定、验收目标不清晰、成功信号不可验证，优先先补文档澄清，不要直接进入实现。
5. 正式验收必须走真实入口、真实环境、真实数据或真实产物路径；禁止把 `pytest`、`unittest`、`dotnet test`、mock、stub、monkeypatch、假对象、伪造返回值写成正式通过证据。
6. test 只用于锁定 contract 与 function；即便 test 全绿，也不能单独宣告当前 change 已验收。

请以 plan.md 和 acceptance.md 为唯一约束，持续推进 `change-id`，直到满足正式验收条件或遇到真实阻塞再停。**不要把“已读 ai_constraints.md”当成完成；必须继续主动读 sibling docs 并进入执行。**

### 启动步骤 / Kickoff

1. 若当前只收到本文件，先按上方「单文档启动 / Standalone Kickoff」主动补齐 `acceptance.md` 与 `plan.md`，而不是先等待用户追加发送。
2. 读取 acceptance 的出口条件看板和场景看板，找出当前阻塞总体验收的最小缺口。
3. 读取 plan.md 的「能力映射」与「三、AI 执行约束」，确认长期回写目标、任务级边界和必跑验证。
4. 回到 `plan.md` 的「防跑偏收敛卡 / Anti-Drift Convergence Card」，锁定 `单一收敛目标 / 第一刀落点 / 首个验证动作 / 超范围触发条件`。
5. 若 `acceptance.md` 与 `plan.md` 均可访问，则默认视为“允许开始执行”；除非文档明确要求先人工确认，否则不得停在纯分析阶段。

## 防跑偏执行节奏 / Anti-Drift Execution Cadence

1. 第一次实质编辑必须优先作用于 `第一刀落点`；若该位置只是 wiring/forwarding，应只前进一步到直接控制行为的 owner，不得同时扫多条邻接路径。
2. 第一次实质编辑后，下一步必须执行 `首个验证动作`；不得先继续补第二组改动、扩读相邻模块或顺手清理无关问题。
3. 若首个验证失败但仍定位在同一 slice，先修同一 slice 并重跑同一验证，不得立刻切到第二个实现面。
4. 若首个验证推翻当前判断，只允许一跳到更直接控制行为的代码，再重复“小改动 -> focused validation”循环。
5. 命中 `超范围触发条件` 时，必须先停止扩面、回填计划或拆 follow-up change；不得把新目标直接并入当前 change。

### 每轮迭代 / Per-Round

1. 一次只解决一个最小阻塞。
1. 每轮必须完成：修改代码或文档、运行最小验证、判断是否推进了验收状态。
1. **若阻塞原因是代码行为不满足验收条件，必须写代码修复，不得仅更新文档来规避。**
1. **新增或修改被测代码时，必须配套合理的 test；禁止只改实现而不补或更新对应测试。**
1. 每轮结束时汇报：解决了哪个阻塞项、哪些项仍未通过、下一轮做什么。
1. 若当前轮次没有真实阻塞，AI 不得以“还需要更多说明”为由空转；应继续执行下一个最小步骤。

### 边界 / Boundaries

1. 不允许越过既定边界：不改交易主链路、不加兜底逻辑、不自动 merge、不自动发布。
2. 若需要引用 artifact、report、projection 或 governance 证据，先回到 sibling `plan.md` 检查 `artifact_boundary`；凡不在受信根内的 artifact，一律不得被当前 change 当作正式输入或正式证据。
3. 若 sibling `plan.md` 命中 `ui_surface_freeze.required=true`，必须先补齐页面三锁回答，再实施代码改动；不得只写 UI 文案而不说明 visibility contract、read-model owner 和 live smoke。
4. 若遇到真实阻塞，必须说明阻塞点、缺什么证据或权限、建议如何解除。

### 跨 Tracer 回归门禁 / Cross-Tracer Regression Gate

```yaml
cross_tracer_regression_required: false
affected_capabilities: []
affected_tracers: []
required_gate: targeted
```

填写规则：

1. 若本 change 修改 `docs/governance/shared_module_registry.yaml` 中登记的共享模块，必须把 `cross_tracer_regression_required` 改为 `true`。
2. `affected_capabilities` 与 `affected_tracers` 必须从 `shared_module_registry.yaml` 推导；不得只写自然语言说明。
3. `required_gate` 仅允许 `targeted` 或 `cross_tracer`；若为 `cross_tracer`，收尾前必须运行 `python -m unittest tests.orchestration.test_cross_tracer_invariants -v` 或等价正式入口。
4. 不允许把 hash lock、graduation、archive migration 或 batch runner 当作本字段的替代验证。

### 状态管理 / Status

1. `AI-STATUS` YAML 是唯一 AI 执行状态源；每次更新 YAML 后必须同步 Dashboard 中的 AI 派生行，不允许让 AI 行停留在旧值。
2. Dashboard 同步只回填 YAML 可直接推出的 AI 派生值；不得借此改写出口条件定义、阻塞级别或场景定义。
3. 阻塞项全部通过后，AI 应直接把结论收敛为“已验收”；仅 mock/stub 通过只能写「预验收通过 / 正式验收待完成」，不得写“已验收”。
4. 若 `acceptance.md` 中正式场景少于 6 个，AI 不得直接宣告已验收，除非文档已明确写出豁免理由且该豁免本身有真实证据支持。

### 收尾 / Wrap-up

1. 若 `affects_long_term_rules=是` 且 `long_term_target != 无`，收尾前必须检查目标长期文档是否已回写，并在其 `## 相关变更 / Related Changes` 登记 `change-id`；若本轮不回写，必须记录原因。
