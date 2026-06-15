# 审查发现快照模板 / Review Snapshot Template

> 用途：每次正式 review 默认先复制这份模板，记录 `架构问题列表 / Findings` 与 `问题处理结果 / Disposition`。

---

## Audit Type

`weekly-architecture-check | monthly-architecture-review | proposal-audit | closeout-audit | retirement-audit | quarterly-retirement-sweep`

显示名到 `Audit Type` 的固定映射：

1. `Weekly Architecture Check` -> `weekly-architecture-check`
2. `Monthly Structure Review` -> `monthly-architecture-review`

## Scope

`<最小可判定范围>`

## Formal Truth

1. `<AGENTS.md / frontier / runbook / proposal / change / ownership 等正式依据>`

## Findings

1. `[severity] <问题标题>`
   - 维度: `<Single Source of Truth | Owner Boundary | Semantic Naming | Hotspot / Monolith | Control Plane | Search Noise | Contract Surface | Docs <-> Code Mutual Verifiability>`
   - Surface: `<文件 / 模块 / 文档 / owner>`
   - Why It Matters: `<为什么重要>`
   - Evidence: `<命令 / 路径 / 事实>`
   - What Would Make It Acceptable: `<什么条件算通过>`

## Dimension Coverage

> `monthly-architecture-review` 必填；其他 review 类型可写 `not applicable`。

| Dimension | Coverage | Note |
| --- | --- | --- |
| Single Source of Truth | `<hit via F# | not hit in this scope>` | `<说明>` |
| Owner Boundary | `<hit via F# | not hit in this scope>` | `<说明>` |
| Semantic Naming | `<hit via F# | not hit in this scope>` | `<说明>` |
| Hotspot / Monolith | `<hit via F# | not hit in this scope>` | `<说明>` |
| Control Plane | `<hit via F# | not hit in this scope>` | `<说明>` |
| Search Noise | `<hit via F# | not hit in this scope>` | `<说明>` |
| Contract Surface | `<hit via F# | not hit in this scope>` | `<说明>` |
| Docs <-> Code Mutual Verifiability | `<hit via F# | not hit in this scope>` | `<说明>` |

## Disposition

1. `<对应 Findings #1>`：`已修复 | 已分流 | 暂缓 | 不成立 | 需 follow-up`
   - Result: `<问题处理结果>`
   - Landing: `<current change / local issue / follow-up change / proposal / direct doc fix>`

## Recommended Landing

1. `<按问题或按分组列出正式落点>`

## Suggested Gate

1. `<需要执行的最小 gate / focused test / docs gate>`

## Suggested Next Step

1. `<下一步动作>`

## Residual Risks

1. `<本轮未覆盖或暂未处理的风险>`

## Status

`draft | reviewed | landed | follow-up-opened | no-blocking-findings`
