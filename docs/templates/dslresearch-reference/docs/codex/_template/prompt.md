# Codex Prompt: {{任务标题}}

- 日期：{{YYYY-MM-DD}}
- 关联 change：{{change-id 或 "无"}}
- 关联 ADR：{{ADR 路径 或 "无"}}
- Phase：{{Phase N 或 "N/A"}}
- 预估 Task 数量：{{N}}

---

## 以下为发送给 Codex 的完整内容

> 将 ```` 之间的内容整体复制粘贴到 Codex 的 prompt 输入框。

````text
You are working on the {{项目名}} Python project at the repository root.
Python venv: .venv (already installed, use `python -m pytest` to run tests).

## Objective

{{一句话说明：改什么、为什么}}

## Context

{{当前代码状态：
- 关键文件位置
- 已有约束
- 相关常量/类/函数名
- 如果有 ADR，写出路径让 Codex 先读}}

## Tasks

### T1. `{{文件相对路径}}` — {{一句话标题}}

**文件**：`{{相对路径}}`

**改动**：

{{文字描述改动目标}}

```python
# 给出具体代码，不是方向描述
```

**验证**：`{{一条可在终端执行的命令}}`

### T2. ...

（按顺序列出所有 Tasks，每个 Task 包含：文件、改动、验证）

## Scope Guard

Codex may ONLY modify files listed below. Any file not listed here is OFF-LIMITS.

**Allowed files** (exhaustive list):
- `{{file1.py}}`
- `{{file2.py}}`
- `tests/{{test_file.py}}`

**Read-only reference** (read but do NOT modify):
- `AGENTS.md`
- `{{reference_file}}`

If a task requires changing a file not in the allowed list, STOP and report it
in the task output instead of making the change.

## Hard Rules

1. **Encoding**: All files must remain UTF-8 without BOM.
2. **No body drift**: Only change what the Task explicitly describes. Do not "improve" neighboring code.
3. **No fallback/compat/silent-fail**: Do NOT introduce `try/except` that swallows errors, default values that mask failures, or fallback branches. If something fails, let it fail loudly.
4. **No new dependencies**: Do not add `import` for packages not already in use, unless a Task explicitly requires it.
5. **No input/archive touching**: Do NOT modify anything under `input/` or `docs/changes/` unless a Task explicitly requires it.
6. **No docstring/comment additions**: Do NOT add docstrings or comments to code you didn't change.
7. **Type annotations**: All new functions must have parameter and return type annotations.
8. **CONTRACT-LOCK**: Do NOT modify any line with `# [CONTRACT-LOCK: ...]`. If a test fails because of CONTRACT-LOCK, report it instead of changing the assertion.
9. **Test isolation**: Do NOT modify existing test assertions. Only add new tests if a Task requires it.
10. **Per-Task validation**: After each Task, run its validation command and confirm it passes before proceeding.
11. {{额外仓库特有规则}}

## Execution Order

{{标注任务间依赖关系}}

T1 → T2 → T3 → (T4, T5 parallel) → T6

## Final Gate

The task is DONE only when ALL of these pass:

```bash
# 1. Full regression
python -m pytest tests/ -x -q

# 2. Anti-pattern scan
python scripts/check_antipatterns.py   # target: ERROR: 0

# 3. Scope check — only allowed files changed
git diff --name-only HEAD  # must be subset of Scope Guard list
```

- If any gate fails, fix the issue and re-run. Do NOT skip gates.
- {{其他验证命令 + 期望输出}}

## Environment

- OS: Windows 11
- Python: 3.12
- venv: .venv
- Test runner: pytest
- Encoding: UTF-8, no BOM
````
