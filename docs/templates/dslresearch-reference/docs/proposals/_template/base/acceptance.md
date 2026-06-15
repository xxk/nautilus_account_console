# Acceptance / 验收基线

**proposal-id**：`<proposal-id>`
**状态**：draft

---

## 验收范围 / Scope

当前 proposal 验收以下内容：

1. <in-scope 目标 1>
2. <in-scope 目标 2>

当前 proposal 不验收以下内容：

1. <out-of-scope 事项 1>
2. <out-of-scope 事项 2>

---

## Artifact Root Rule

本文件引用的 formal artifact、projection、report、verdict 必须属于 sibling `phase-plan.md` 中声明的 `Artifact Trust Boundary`。

未冻结唯一受信根前，只允许记录“待冻结”或 repo-local 诊断留痕，不得把 proposal 外部 artifact 写成当前 proposal 的完成证据。

---

## Acceptance Evidence Boundary

1. `pytest`、`unittest`、`dotnet test`、mock、stub、monkeypatch 或其他 test-only 输出，只能作为 contract/function guard evidence，不得单独充当 proposal 正式验收证据。
2. proposal 验收场景若要写成 `passed`、`completed` 或等价完成结论，至少还需要一类非 test-only 证据：真实命令执行结果、受信 formal artifact、projection/read-model 结果、live/rendered surface 证据，或可复核的 source evidence。
3. 若当前只有 test/mock 结果，而没有真实入口、真实 artifact 或真实 consumer 证据，只能记录为 guard/reference，不得把该 proposal 场景写成正式收口完成。
4. A repo-local repairable blocker must not be used as a reason to stop; it needs a repair attempt, focused gate result, and updated acceptance evidence.
5. A blocker that depends on an external owner, real data, or human approval must not be faked; it must produce typed waiting/blocked evidence, blockers, next_action, and carry-forward mapping.
6. A proposal closeout may remain `blocked` only after code/contract blockers have been handled and the remaining blocker is outside the current authority boundary.

---

## Acceptance Scenario Auto-Fill / 验收场景自动补全

<!-- PROPOSAL-ACCEPTANCE-AUTOFILL:v1 -->

新 proposal 创建后必须保留本节。AI 开发时先从本表生成验收场景，再把每个场景落到下面的 `Mandatory Gate Coverage`、`Positive-to-Negative Coverage Map`、`Anti-Drift Matrix`、`Scenario Matrix` 或 `ADR Carrier Acceptance Matrix`。

| ID | Scenario family | Auto-filled acceptance row | Must fail if | Status |
| --- | --- | --- | --- | --- |
| AF1 | ADR full coverage | 若 README 声明 `ADR carrier=yes` 或 `Primary ADR` 不是 `not_applicable`，逐项接全 Primary ADR 的 decision item、successor scenario、positive path、negative/fail-fast path、authority boundary 与 minimal evidence。 | ADR 验收只覆盖部分决策、只有正向路径、没有 retire/authority 边界，或没有映射到 acceptance 行。 | planned |
| AF2 | negative/counterexample acceptance | 每条可通过的正向验收行必须映射至少一条负向 / counterexample 行。 | 正向验收可以通过，但没有对应拒绝信号、typed blocker 或 fail-fast 证据。 | planned |
| AF3 | anti-drift acceptance | 每个 proposal 必须有 anti-drift 行，证明陈旧证据、外部 artifact、旧 read-model、字段漂移或 proposal-only 证据不能误判为完成。 | 缺 anti-drift 行，或 anti-drift 未绑定到测试、source guard、artifact audit、readback evidence 或 typed blocker。 | planned |
| AF4 | research-case own input | proposal-bound research case 必须拥有当前 input package，并验证不能从 proposal/readback evidence alone 完成。 | 当前 case 没有 `input/<case-slug>/study_request/request.json`，或复用上游 input 目录当成本 case input。 | planned |
| AF5 | case Gate Claim-Proof all PASS | 研发 case closeout 目标必须明确包含 `Research PASS`、`Evidence Closeout PASS`、`Formal Readiness PASS`。 | Research、Evidence Closeout 或 Formal Readiness 仍是 BLOCKED、NOT_SURFACED、missing 或 stale 时关闭 proposal。 | planned |
| AF6 | research-view readback | research workflow 必须先用 research-view/report readback 验证，再进入 downstream owner action。 | 从 proposal 文本、business-view、PM decision、production owner action、paper/live 或 capital truth 直接写完成结论。 | planned |
| AF7 | RDG carry-forward | 若本轮发现 RDG / 复发缺陷 / issue-list carry-forward，必须映射到当前验收行或下一枚 tracer 的验收要求。 | RDG 问题只留在聊天、临时 evidence、commit message 或 issue-list 未映射行中。 | planned |
| AF8 | Dev Home discoverability | proposal-bound research case 若声明当前-facing Home 可见，必须有 formal registry identity、Case Authority materialization 和 `18765` live Home/API readback。 | 只有 proposal/input/file projection 证据，或 `http://127.0.0.1:18765/` / `/api/live-case-projection.json` 读不到当前 case。 | planned |
| AF9 | Proposal Workflow Stage Contract | P178+ proposal 必须显式接入 `docs/workflows/proposal-gates`，区分 Proposal Gate 和 Research Gate，并说明 Stage / Gate / Check / Proof Item 层级。 | proposal 只列 gate 名称但没有 Stage Contract、P-Gate/R-Gate 边界，或 Proposal Gate 推断 Research Gate verdict。 | planned |

---

## Mandatory Gate Coverage / 必需 Gate 覆盖

These gates are blocking. A proposal cannot close if an applicable gate is missing, unmapped, positive-only, or anti-drift-free.

| Gate | Requirement | Applies when | Must fail if | Status |
| --- | --- | --- | --- | --- |
| G1 | ADR full coverage: if the proposal has an ADR carrier or Primary ADR, it must map all ADR decision items, successor scenarios, positive paths, negative paths, authority / retirement boundaries, and minimal evidence. | ADR carrier is `yes` or Primary ADR is not `not_applicable` | ADR acceptance is partial, placeholder-only, positive-only, or unmapped to acceptance rows | planned |
| G2 | negative/counterexample acceptance: every positive row that can pass implementation must map to at least one negative / counterexample row. | Any positive scenario can become `passed`, `completed`, or equivalent | A positive row is marked passed without a mapped negative rejection or typed blocker | planned |
| G3 | anti-drift acceptance: anti-drift rows must be present and closeout-bound to focused tests, source guards, artifact audits, readback evidence, or typed blockers. | All non-draft proposals | Anti-drift matrix is missing, stale, ignored during closeout, or unsupported by evidence / blocker mapping | planned |
| G4 | research workflow uses research-view/report readback before downstream owner action. | Proposal represents a research case, tracer, formal case, or case-bound successor | Production owner action, PM decision, business-view, paper/live, admission, or capital truth is written from proposal evidence | planned |
| G5 | research-case own input: every proposal-bound research case must have its own current input package before closeout. | Proposal represents a research case, tracer, formal case, or case-bound successor | The proposal is completed from proposal/readback evidence only, or an upstream input directory is counted as the current case input | planned |
| G6 | case Gate Claim-Proof all PASS: a proposal-bound research case must carry an explicit target that Research, Evidence Closeout, and Formal Readiness all reach PASS before case closeout. | Proposal represents a research case, tracer, formal case, or case-bound successor | The proposal research task closes while Research, Evidence Closeout, or Formal Readiness remains BLOCKED / NOT_SURFACED / missing | planned |
| G9 | Dev Home discoverability: a proposal-bound research case that claims Home visibility must be registered, materialized into Case Authority, and read back from `18765` Home/API. | Proposal represents a research case, tracer, formal case, or case-bound successor | The case only exists in proposal/input/file projection, or current-facing Dev Home/API cannot find the case | planned |
| G10 | Proposal Workflow Stage Contract: P178+ proposal must reference `docs/workflows/proposal-gates`, keep Stage as the top-level unit, and keep Gate sparse with Checks and Proof Items absorbing detail growth. | Proposal number is P178 or later | Stage Contract is missing, or detailed validation growth becomes new Gate families without phase-boundary justification | planned |
| G11 | Proposal Gate / Research Gate boundary: Proposal Gate may block proposal advancement but must not write, mint, upgrade, or infer Research Gate verdict. | Proposal uses workflow gates or reads research/runtime evidence | Proposal Gate writes Research PASS, Evidence Closeout PASS, Formal Readiness PASS, or any business/research verdict | planned |

---

## Positive-to-Negative Coverage Map

| Positive row | Required negative / anti-drift rows | Coverage rule |
| --- | --- | --- |
| A1 | N1 | A1 cannot pass unless the mapped rejection row proves stale/proposal-only evidence is rejected. |
| A2 | N2 | Proposal Workflow Stage Contract cannot pass unless Stage/Gate/Check/Proof hierarchy and P-Gate/R-Gate boundary are explicit. |

---

## Anti-Drift Matrix / 防跑偏验收

| ID | 类型 | Must fail if | 验收方式 | 预期拒绝信号 | Status |
| --- | --- | --- | --- | --- | --- |
| N1 | drift | stale, foreign, proposal-only, or unmapped evidence is counted as closeout evidence | focused test / source guard / artifact audit / readback evidence / typed blocker | explicit BLOCKED / rejected / missing_evidence signal | planned |
| N2 | workflow-stage drift | `docs/workflows/proposal-gates` is absent, Stage Contract is missing, or Proposal Gate writes Research Gate verdict | proposal docs gate / source review | workflow_stage_contract_missing_or_boundary_violation | planned |

---

## 场景矩阵 / Scenario Matrix

| ID | 类型 | 场景 | 验收方式 | 通过信号 | 状态 |
| --- | --- | --- | --- | --- | --- |
| A1 | success | 核心 happy path 完成 | <命令/检查> | <通过信号> | planned |
| A2 | failure | 缺关键证据时拒绝通过 | <命令/检查> | <拒绝信号> | planned |
| A3 | regression | 旧语义不会从公开入口回流 | <命令/检查> | <无回流> | planned |

---

## ADR Carrier Acceptance Matrix

> 仅当 README 顶部状态块 `ADR carrier` 为 `yes` 时必填；否则写 `not_applicable`。ADR carrier acceptance rows are incomplete until mapped.

ADR-carrier proposal 的验收矩阵必须逐项覆盖 `phase-plan.md` 中的 `Covered decisions`，并把每个 ADR decision item 映射到 ADR successor scenario、positive path、negative/fail-fast path、authority / retirement boundary 和最小证据。

| ID | Primary ADR | ADR decision item | ADR successor scenario | Positive path | Must fail if | Authority / retirement boundary | Minimal evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-ADR-1 | ADR-00xx | D1 | <ADR Section 6.2 successor scenario> | <expected accepted path> | <negative path that must reject> | <owner / authority / retirement boundary> | <command, artifact, projection, or source evidence> | planned |

---

## Evidence

| 证据 | 路径或命令 | 结论 |
| --- | --- | --- |
| <证据名称> | <路径或命令> | <结论> |

---

## Closeout Checklist

1. 所有 in-scope 场景都有证据。
2. 所有 formal artifact 引用都位于 proposal 已声明的受信 artifact roots 内。
3. residual risk 已回填到 proposal / phase-plan / follow-up child change。
4. 若属于持续曳光弹 / tracer proposal，`issue-list.md` 中每条未完全关闭的问题都已映射到当前验收行或下一枚 tracer 的 carry-forward 验收要求。
5. 任何 proposal 场景都不得仅凭 test/mock 结果写成正式验收通过；若 test 是当前唯一证据，必须显式标注为 guard/reference，而不是 closeout evidence。
