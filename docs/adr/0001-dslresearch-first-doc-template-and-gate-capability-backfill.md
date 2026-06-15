---
status: accepted
owner: architecture
adr_id: "0001"
decision_status: accepted
landing_status: completed
---

# ADR-0001: DSLresearch-First Documentation Template And Gate Capability Backfill / 文档模板与 Gate 能力缺失先向 DSLresearch 学习

- Date: 2026-06-13
- ADR type: governance
- Decision status: accepted
- Landing status: completed
- Scope: local ADRs, documentation templates, proposal templates, topic roadmap kernel, acceptance records, Gate/check scripts, governance manifests and future docs automation in `nautilus_account_console`
- Decision question: What should this repository do when it lacks a documentation template or Gate/check capability?
- Decision: Before inventing a local pattern, inspect `D:\Nautilus\DSLresearch`, copy or learn the matching documentation/Gate pattern, and adapt it to this project's read-only account-console boundaries. A reference mirror now exists under `docs/templates/dslresearch-reference/`.

---

## 1. Problem Frame / 问题框架

`nautilus_account_console` is a new independent project. Its runtime boundaries are clear, but its local documentation and governance surfaces are still thin. Without an explicit rule, future changes may create ad hoc ADR formats, acceptance templates, docs gates or validation scripts that drift away from the stronger governance patterns already present in `D:\Nautilus\DSLresearch`.

The goal is not to make this repository a copy of DSLresearch. The goal is to reuse proven documentation and Gate shapes first, then trim them to the account-console domain.

### 1.1 Hard Constraints / 硬约束

1. `D:\Nautilus\DSLresearch` is a reference source for documentation templates, Gate/check shapes, registry patterns and governance tests.
2. `D:\Nautilus\DSLresearch` is not a truth owner for account state, order state, fill state, position state, broker state, admission state, approval state, capital state or runtime state in this project.
3. Copied templates must be reduced to the smallest local shape that preserves the governance intent.
4. Copied Gates/checks must declare their verdict scope: docs structure, contract shape, build/test evidence, benchmark evidence or UI rendering evidence.
5. Copied Gates/checks must not write or infer broker, capital, runtime, admission, approval or tradability truth.
6. If a DSLresearch pattern is too broad, copy the concept and source reference, not the full workflow.
7. Any future local Gate that touches HFT acceptance must require typed benchmark evidence for durable ledger zero-loss, bounded lag, cursor replay, backpressure and virtualized browser rendering.

### 1.2 Explicit Non-Goals / 明确不做

1. Do not wholesale transplant the DSLresearch proposal system into this repository.
2. Do not import DSLresearch runtime, research, admission, approval or capital semantics.
3. Do not create a universal Gate writer or business decision writer in this project.
4. Do not treat raw report messages, screenshots, report HTML or debug payloads as account truth.
5. Do not use this ADR to implement a new Gate script immediately; it only freezes the backfill rule.

### 1.3 Owner / Canonical Entry Impact

| Concern | Current owner / entry | ADR-0001 impact |
| --- | --- | --- |
| Local ADR index | none | create `docs/adr/README.md` as the local ADR entry |
| Local documentation templates | ad hoc docs under `docs/` | future missing templates must inspect DSLresearch first |
| Local topic capability | none | create a thin local `docs/topics/` kernel without DSLresearch historical topic content |
| Local Gate/check capability | CI plus acceptance docs | future missing Gates/checks must inspect DSLresearch first and keep local verdict scope explicit |
| Runtime account truth | normalized events and reduced read models | unchanged |
| UI projection | TypeScript browser projection | unchanged; read-only consumer only |

### 1.4 Canonical Naming Check / 概念判重

| Candidate term | Layer / Owner | Existing nearby term | Collision risk | Decision | Guard / Evidence |
| --- | --- | --- | --- | --- | --- |
| `DSLresearch-first backfill` | docs governance | DSLresearch ADR template and proposal gates | medium: could be mistaken for cross-repo ownership | accepted as a local learning/copy rule only | this ADR and local ADR index |
| `documentation template` | docs | ADR template, proposal template, acceptance template | low | accepted as generic docs scaffold | cite copied source path when a future template is added |
| `Gate capability` | docs / CI / validation | Gate, Check, Proof Item in DSLresearch | high: could be mistaken for business or trading decision gate | accepted only with explicit local verdict scope | future Gate docs/tests must say what they can and cannot decide |
| `copy/learn` | execution practice | template copy, fragment pattern, manifest projection | medium: could imply wholesale transplant | accepted as thin adaptation | source reference plus local boundary review |

---

## 2. Relationship To Existing Decisions / 与既有决策关系

1. This ADR supplements the repository role in `AGENTS.md` and the ADR-0045 account-console boundary referenced from `nautilus_strategies`.
2. It learns from DSLresearch ADR-0038: use a thin base plus optional fragments instead of heavy all-purpose templates.
3. It learns from DSLresearch Gate governance: manifests or registries should own machine-readable structure, while human boards/readmes are projections.
4. It learns from DSLresearch Gate write-model governance: surfaces, adapters and read models must not become Gate verdict writers.
5. It does not make DSLresearch an upstream runtime dependency or authority for this project.
6. It copies the DSLresearch topic capability as a thin local kernel: index, status registry, roadmap root and roadmap template only.

---

## 3. Options Comparison / 方案对比

| Option | Core idea | Pros | Risks | Decision |
| --- | --- | --- | --- | --- |
| A. Invent local docs and Gates case by case | Create each missing template or Gate from scratch | fast for one change | causes drift and second patterns | rejected |
| B. Wholesale copy DSLresearch workflows | Copy complete ADR/proposal/Gate systems | preserves mature details | too heavy; imports unrelated research semantics | rejected |
| C. DSLresearch-first thin adaptation | Inspect DSLresearch first, copy/learn the thinnest useful pattern, adapt locally | reuses proven governance while preserving account-console scope | requires discipline to trim | accepted |
| D. Wait until a missing capability blocks work | Defer all governance scaffolding | avoids premature files | repeats ambiguity at each boundary | rejected |

### 3.1 Landing Evidence / 落地证据

| Option | decision_state | landing_state | evidence_state | evidence_ref | residual_risk |
| --- | --- | --- | --- | --- | --- |
| A | rejected | not_applicable | docs_only | this ADR | none |
| B | rejected | not_applicable | docs_only | this ADR | none |
| C | accepted | completed | docs_only | this ADR + `docs/adr/README.md` + `docs/templates/dslresearch-reference/` + `docs/topics/` | future Gates still need focused validation |
| D | rejected | not_applicable | docs_only | this ADR | none |

---

## 4. Decision / 决策

### 4.1 Decision Summary / 决策结论

Accepted: use option C, DSLresearch-first thin adaptation.

When this repository lacks a documentation template or Gate/check capability:

1. Search `D:\Nautilus\DSLresearch` for the closest proven pattern.
2. Copy or learn the smallest structure that solves the local problem.
3. Adapt names, owners, verdict scope and evidence expectations to `nautilus_account_console`.
4. Cite the source path or source ADR in the local doc, PR or Gate README when the pattern is introduced.
5. Add focused local validation before treating a copied Gate/check as binding.

### 4.2 Decision Boundaries / 决策边界

| Area | Allowed | Forbidden |
| --- | --- | --- |
| ADR/docs templates | copy structure, section discipline and index rules | copy unrelated DSLresearch research semantics |
| Acceptance docs | copy evidence matrix style and fail-closed language | claim implementation evidence without local command/artifact proof |
| Gate/check scripts | copy validation shape and registry/manifest ideas | write or infer account, broker, admission, approval, capital or runtime truth |
| UI/backend/hotpath | add local checks driven by local contracts and read models | read DSLresearch artifacts as account-console truth |
| HFT acceptance | require typed benchmark evidence | accept UI appearance or prose as HFT proof |

### 4.3 Design Kernel / 设计内核

Stable flow:

```text
Missing local docs template or Gate/check capability
  -> inspect D:\Nautilus\DSLresearch
     -> choose closest proven pattern
        -> thin local adaptation
           -> explicit verdict scope
              -> focused local validation
```

Stable rules:

1. DSLresearch is the first learning/copy source for docs templates and Gate capability gaps.
2. This repository keeps its own local owner boundaries and read-only account-console role.
3. A copied Gate/check is not binding until it has local scope, local evidence expectations and local validation.
4. Human-readable docs may project Gate state, but machine-readable manifests, tests or scripts own the checkable contract.
5. Any copied wording that suggests trading readiness, admission, approval or capital allocation must be removed or converted into an explicit negative rule.

### 4.4 Recommended Deliverables / 推荐产物

1. `docs/adr/README.md` as the local ADR index.
2. `docs/templates/dslresearch-reference/` as the reference-only mirror of copied DSLresearch templates.
3. `docs/topics/` as the thin local topic roadmap kernel.
4. This ADR as the binding backfill policy.
5. Future local templates or Gate/check READMEs should include a short "Source pattern" note when they adapt DSLresearch material.
6. Future Gate/check scripts should include focused tests or a validation command before being listed as binding.

### 4.5 Decision Coverage And Landing Matrix / 决策覆盖与落地矩阵

| ID | Decision | decision_state | landing_state | evidence_state | executable evidence | docs evidence | Remaining gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | Establish DSLresearch-first as the default backfill rule for docs templates and Gate capability gaps. | accepted | completed | docs_only | not_applicable | this ADR + template mirror | none |
| D2 | Keep copied patterns thin and local to account-console boundaries. | accepted | completed | docs_only | not_applicable | this ADR + `docs/templates/README.md` | future PRs must cite source/adaptation |
| D3 | Require explicit verdict scope for future copied Gates/checks. | accepted | planned | missing | future focused Gate tests | this ADR | implement when first new Gate/check is added |
| D4 | Prohibit copied Gates/checks from writing runtime, broker, admission, approval, capital or tradability truth. | accepted | completed | docs_only | not_applicable | this ADR + AGENTS.md | future source guards may strengthen it |
| D5 | Require typed benchmark evidence for future HFT acceptance Gates. | accepted | planned | missing | future benchmark artifacts/tests | this ADR + AGENTS.md | implement with HFT gate work |
| D6 | Copy Topic capability as a local docs-only kernel, without DSLresearch historical topic content or research lifecycle semantics. | accepted | completed | docs_only | not_applicable | `docs/topics/README.md` + topic registry + roadmap template | future topic gate/script can be thin-adapted later |

---

## 5. Decision + Landing / 采纳与落地

### 5.0 Accepted Decision Boundary / 已接受决策边界

Accepted:

1. Missing documentation templates and Gate/check capability must inspect DSLresearch first.
2. Copying into `docs/templates/dslresearch-reference/` is allowed as a reference mirror; promotion into local templates still requires thin local adaptation.
3. Local account-console boundaries remain authoritative.
4. Future copied Gates/checks must be scoped, validated and read-only with respect to business/runtime truth.

### 5.0.1 Not Accepted By This ADR / 本 ADR 不接受

1. No DSLresearch runtime dependency.
2. No DSLresearch owner authority over this project's account state.
3. No new writer for runtime, admission, approval, capital or broker truth.
4. No broad proposal workflow transplant.
5. No Gate that upgrades UI/docs appearance into business readiness.

### 5.0.2 Successor Proposal Boundary / 后续 Proposal 边界

This ADR does not require an immediate successor proposal. The reference mirror was copied into `docs/templates/dslresearch-reference/`, and the topic capability was copied as a thin docs-only kernel under `docs/topics/`. Each future local template, topic gate or Gate/check capability should apply this ADR at the point of need and carry its own focused acceptance evidence.

### 5.1 Legacy Retirement And Documentation Closure / 旧路径退役与文档收口

No legacy local ADR template or Gate/check path is retired by this ADR. Future ad hoc templates or Gates that conflict with this policy should be replaced by thin DSLresearch-derived local patterns.

---

## 6. ADR-Level Acceptance Only / 仅限 ADR 级验收

This ADR is accepted when:

1. The ADR exists under `docs/adr/`.
2. `docs/adr/README.md` indexes it as binding.
3. The repository README points to `docs/adr/` and `docs/templates/`.
4. `docs/templates/dslresearch-reference/` contains the copied DSLresearch template mirror.
5. `docs/topics/` contains the thin local topic kernel.
6. The rule preserves the repository's read-only account-console boundary.

Future implementation acceptance for any copied Gate/check must live with that Gate/check or its change record, not inside this ADR.

### 6.1 Architecture-Level Acceptance For Future Work

A future docs template or Gate/check introduced under this ADR should prove:

1. The source DSLresearch pattern was inspected and named.
2. The local adaptation removed unrelated research/runtime semantics.
3. The local owner and verdict scope are explicit.
4. The validation command or focused test is documented.
5. The change does not create a second account, broker, admission, approval, capital or runtime truth source.

### 6.2 ADR Closeout Distillation / ADR closeout 沉淀

| Distillation target | Stable conclusion distilled from this ADR | Do not copy forward | Closeout action |
| --- | --- | --- | --- |
| `docs/adr/README.md` | ADR-0001 is binding local governance | option comparison details | index now |
| `README.md` | ADR docs exist and carry local governance | full ADR body | add docs map entry |
| `docs/templates/README.md` | copied templates are reference-only until locally adapted | source template body | add reference rules |
| `docs/topics/README.md` | topic capability exists as a local docs-only kernel | DSLresearch historical topic content | add topic kernel |
| Future Gate/check docs | cite DSLresearch source and local verdict scope | unrelated DSLresearch workflow body | apply when needed |

---

## 7. Related Documents / 关联文档

1. `AGENTS.md`
2. `README.md`
3. `docs/architecture/github-project-architecture.md`
4. `docs/templates/README.md`
5. `docs/topics/README.md`
6. `D:\Nautilus\DSLresearch\docs\topics\README.md`
7. `D:\Nautilus\DSLresearch\docs\topics\主题状态注册表_Topic State Registry.yaml`
8. `D:\Nautilus\DSLresearch\docs\adr\ADR模板_ADR Template.md`
9. `D:\Nautilus\DSLresearch\docs\adr\0038-proposal-template-thin-base-and-fragment-pattern.md`
10. `D:\Nautilus\DSLresearch\docs\adr\0092-canonical-gate-write-model-and-snapshot-owner-governance.md`
11. `D:\Nautilus\DSLresearch\docs\workflows\proposal-gates\README.md`
