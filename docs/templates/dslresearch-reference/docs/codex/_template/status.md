# Codex 任务状态 / Codex Task Status

---

## 元数据

| 字段 | 值 |
|---|---|
| task-name | {{YYYYMMDD-slug}} |
| status | draft |
| 关联 change | {{change-id 或 "无"}} |
| 创建人 | {{Copilot Chat / 人工}} |
| 创建日期 | {{YYYY-MM-DD}} |
| 预估 Task 数 | {{N}} |

---

## 发送前检查 / Pre-Send Checklist

> status 从 `draft` 改为 `ready` 的前提条件。

- [ ] Objective 一句话能看懂改什么
- [ ] Context 包含当前代码状态（常量名、类名、字段名）
- [ ] 每个 Task 有明确文件路径
- [ ] 每个 Task 有代码片段（不是只描述方向）
- [ ] 每个 Task 有独立的验证命令
- [ ] Hard Rules 至少包含编码规则和禁区
- [ ] Final Gate 是可执行命令（不是"请确认"）
- [ ] 没有依赖外部网络/数据库/远端服务
- [ ] 没有引用 Codex 看不到的文件（必要上下文已内联）
- [ ] prompt 长度在 Codex 上下文窗口内

---

## 执行记录 / Execution Log

> Codex 执行完成后，在此记录回收结果。

### 发送

| 字段 | 值 |
|---|---|
| 发送时间 | |
| Codex session/branch | |

### 目标修订

> 若在发送后对 prompt 目标做了修订，在此记录。无修订则留空。

| 字段 | 值 |
|---|---|
| 修订时间 | |
| 修订内容 | |
| 修订原因 | |

### 回收

| 字段 | 值 |
|---|---|
| Codex 自报状态 | pass / partial / fail |
| 本地 Final Gate | |
| 本地 pytest 结果 | |
| diff 审查 | |

### Task 逐项结果

> 每个 Task 一行；`Codex 结果` 填 completed / partial / fail；`本地验证` 填 通过 / 失败。

| Task | Codex 结果 | 本地验证 | 备注 |
|---|---|---|---|
| T1 {{描述}} | | | |
| T2 {{描述}} | | | |

---

## Diff 审查检查清单 / Diff Review Checklist

> Codex 分支 merge 前，逐项检查。全部通过才可 merge。

- [ ] **Scope 守卫**：`git diff --name-only` 只含 prompt 中 Scope Guard 声明的文件
- [ ] **无越界改动**：没有改 input/、docs/changes/、AGENTS.md 等只读文件
- [ ] **无兜底/兼容**：diff 中无 `try/except` 吞异常、无 `or default_value`、无 fallback 分支
- [ ] **无多余改动**：没有 Codex 自行"改进"的非任务代码（reformat、加注释、改命名）
- [ ] **类型注解完整**：新增函数都有 `-> ReturnType`
- [ ] **CONTRACT-LOCK 未被动**：没有修改/删除任何 `# [CONTRACT-LOCK: ...]` 断言
- [ ] **测试未被改弱**：没有删除/弱化已有断言
- [ ] **pytest 全绿**：`python -m pytest tests/ -x -q` 通过
- [ ] **反模式扫描**：`python scripts/check_antipatterns.py` 输出 `ERROR: 0`
- [ ] **编码正确**：文件为 UTF-8 无 BOM

---

## 执行问题 / Execution Issues

> 记录 Codex 执行中暴露的问题：prompt 歧义、上下文不足、重复改错文件、遗漏约束等。
> 每条问题标注严重程度（P0 阻塞 / P1 需修复 / P2 可改进）。
> **无问题时写"无"**。

无

---

## 续做 / Follow-up

| 项目 | 内容 |
|---|---|
| 失败 Tasks | |
| 失败原因 | |
| 续做方式 | |
| 续做执行人 | |

---

## 复盘 / Retrospective

> 任务完成或放弃后填写，用于改进后续 prompt 质量。

1. 哪些 Tasks 一次通过？
2. 哪些 Tasks 失败？原因？
3. 本地与 Codex 报告是否一致？
4. 下次类似任务，prompt 需要调整什么？
| 本地 pytest 结果 | X passed, Y failed |
| diff 审查 | 合规 / 发现问题: ... |

### Task 逐项结果

| Task | Codex 结果 | 本地验证 | 备注 |
|---|---|---|---|
| T1 | | | |
| T2 | | | |
| T3 | | | |
| ... | | | |

---

## 续做 / Follow-up

> 若 status 为 partial 或 failed，记录后续处理。

| 项目 | 内容 |
|---|---|
| 失败 Tasks | |
| 失败原因 | prompt 歧义 / 依赖遗漏 / 环境差异 / 其他 |
| 续做方式 | Copilot Chat 修复 / 修正 prompt 重试 / 人工处理 |
| 续做执行人 | |

---

## 复盘 / Retrospective

> 2 分钟回答，执行完成后填写。

1. 哪些 Tasks 一次通过？
2. 哪些 Tasks 失败？原因？
3. 本地与 Codex 报告是否一致？
4. 下次类似任务，prompt 需要调整什么？
