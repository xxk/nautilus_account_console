# 试点Case12证据模板 / Pilot Case 12 Evidence Template

**创建日期**：2026-04-29
**最后更新**：2026-04-29
**状态**：待回填（Pending Evidence Fill-In）
**所属 proposal**：[README.md](README.md)
**关联清单**：[试点Case12规范验收清单_Pilot Case 12 Normative Acceptance Checklist.md](%E8%AF%95%E7%82%B9Case12%E8%A7%84%E8%8C%83%E9%AA%8C%E6%94%B6%E6%B8%85%E5%8D%95_Pilot%20Case%2012%20Normative%20Acceptance%20Checklist.md)

---

## 使用说明

1. 执行 Phase 7 前先复制本模板，作为本次 pilot closeout 的唯一证据入口。
2. 所有命令、页面、文件清单、结论都回填到同一份文档，不要分散在聊天记录。
3. 未实际执行的项保留 `pending`，不要提前改成 `passed`。

---

## 一、基础信息

| 字段 | 值 |
| --- | --- |
| 日期 | `[待回填]` |
| 执行人 | `[待回填]` |
| 所属 proposal | `p016-external-verifier-research-governance-loop` |
| 关联 change-id | `[待回填]` |
| `case_ref` | `#12` |
| `case_ref_number` | `12` |
| `case_id` | `cffex_index_if_ic_allswitch_myvnpy_rollover_1h_20220104_20260224` |
| `strategy_key` | `if_ic_allswitch_myvnpy_rollover` |
| `canonical_root` | `\\10.168.80.58\Data\artifact_store\DSLReserach\cases\12` |
| policy mode | `[off / advisory / blocking]` |
| verifier profile | `[待回填]` |
| Portal URL | `[待回填]` |
| Dev Home URL | `[待回填]` |

---

## 二、共享执行入口

| 用途 | 实际入口 / 命令 | 结果 | 备注 |
| --- | --- | --- | --- |
| compiled_input writer | `[待回填]` | `[pending]` | |
| formal run entry | `[待回填]` | `[pending]` | |
| reports writer | `[待回填]` | `[pending]` | |
| acceptance / governance writer | `[待回填]` | `[pending]` | |
| external verifier | `[待回填]` | `[pending]` | |
| gate / projection refresh | `[待回填]` | `[pending]` | |
| Portal 打开入口 | `[待回填]` | `[pending]` | |
| Dev Home 打开入口 | `[待回填]` | `[pending]` | |

---

## 三、共享文件清单

| 项目 | 路径 | 是否存在 | 备注 |
| --- | --- | --- | --- |
| manifest | `cases/12/governance/case_manifest.json` | `[pending]` | |
| compiled_input root | `cases/12/compiled_input/` | `[pending]` | |
| runs root | `cases/12/runs/` | `[pending]` | |
| reports root | `cases/12/reports/` | `[pending]` | |
| acceptance root | `cases/12/acceptance/` | `[pending]` | |
| governance root | `cases/12/governance/` | `[pending]` | |
| verifier root | `cases/12/governance/verifier/` | `[pending]` | |
| legacy research path touched? | `research/<case_id>/...` | `[yes/no]` | 若为 `yes` 直接阻断 closeout |

---

## 四、场景汇总看板

| 场景 | 结果 | 核心证据 | 备注 |
| --- | --- | --- | --- |
| A1 | `[pending/pass/fail]` | `[待回填]` | |
| A2 | `[pending/pass/fail]` | `[待回填]` | |
| A3 | `[pending/pass/fail]` | `[待回填]` | |
| A4 | `[pending/pass/fail]` | `[待回填]` | |
| A5 | `[pending/pass/fail]` | `[待回填]` | |
| A6 | `[pending/pass/fail]` | `[待回填]` | |
| A7 | `[pending/pass/fail]` | `[待回填]` | |
| A8 | `[pending/pass/fail]` | `[待回填]` | |
| A9 | `[pending/pass/fail]` | `[待回填]` | |
| A10 | `[pending/pass/fail]` | `[待回填]` | |
| A11 | `[pending/pass/fail]` | `[待回填]` | |
| A12 | `[pending/pass/fail]` | `[待回填]` | |

---

## 五、逐项证据模板

### A1 Manifest Identity 对齐

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- manifest 关键片段：`[待回填]`
- 通过判定：`case_ref=#12`、`case_ref_number=12`、`case_id`、`strategy_key`、`case_artifact_dir=...\cases\12`
- 备注：`[待回填]`

### A2 Compiled Input 写入新路径

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- 产物路径：`[待回填]`
- 旧路径排除证据：`[待回填]`
- 备注：`[待回填]`

### A3 Run Artifacts 写入新路径

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- `run_id`：`[待回填]`
- 目录清单：`[待回填]`
- 备注：`[待回填]`

### A4 Reports 写入新路径

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- report URI / 文件清单：`[待回填]`
- 旧 URI 排除证据：`[待回填]`
- 备注：`[待回填]`

### A5 Acceptance / Governance 写入新路径

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- acceptance 摘要：`[待回填]`
- governance 摘要：`[待回填]`
- 备注：`[待回填]`

### A6 Verifier Artifacts 写入新路径

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- `verifier_run_id`：`[待回填]`
- `export_manifest.json`：`[待回填]`
- `verdict.json`：`[待回填]`
- `report.md`：`[待回填]`
- 备注：`[待回填]`

### A7 Status 词典符合新规范

- 实际检查对象：`[verdict / projection / UI]`
- 结果：`[pending/pass/fail]`
- status 片段：`[待回填]`
- `failure_family` 片段：`[待回填]`
- `block` status 排除证据：`[待回填]`
- 备注：`[待回填]`

### A8 P0 Rules 与 Artifact Truth 一致

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- 关键 `rule_id` / `status`：`[待回填]`
- `summary / evidence_summary`：`[待回填]`
- 备注：`[待回填]`

### A9 Clean/Ready Gate 不误阻断

- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- gate 摘要：`[待回填]`
- `recommended_next_action`：`[待回填]`
- 备注：`[待回填]`

### A10 Required Artifact 缺失时 Blocking Fail 生效

- 缺失/损坏对象：`[待回填]`
- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- top blocker：`[待回填]`
- `failure_family`：`[待回填]`
- blocked reason：`[待回填]`
- 恢复动作：`[待回填]`

### A11 Repair 后生成新的 Verifier Run

- repair 动作：`[待回填]`
- 实际执行入口：`[待回填]`
- 结果：`[pending/pass/fail]`
- old `verifier_run_id`：`[待回填]`
- new `verifier_run_id`：`[待回填]`
- old/new 对比摘要：`[待回填]`

### A12 Ledger / Projection / Portal / Dev Home 一致展示 Latest Truth

- projection refresh 入口：`[待回填]`
- Portal 链接：`[待回填]`
- Dev Home 链接：`[待回填]`
- ledger 摘要：`[待回填]`
- latest verdict / next action 摘要：`[待回填]`
- 结果：`[pending/pass/fail]`

---

## 六、最终结论

| 项目 | 值 |
| --- | --- |
| 通过场景数 | `[待回填]` |
| 是否达到 10+ 场景要求 | `[yes/no]` |
| 是否存在 legacy `research/<case_id>` formal 依赖 | `[yes/no]` |
| 是否建议 closeout | `[yes/no]` |
| 剩余阻塞 | `[待回填]` |

结论摘要：`[待回填]`
