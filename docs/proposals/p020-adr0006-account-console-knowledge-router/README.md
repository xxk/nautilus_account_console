# P020 ADR-0006 Account Console Knowledge Router / Account Console 知识路由

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->
<!-- PROPOSAL-ADR-CARRIER-GATE:v1 -->

- Proposal ID: `p020-adr0006-account-console-knowledge-router`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20
- Owner: account-console-governance / account-console-docs
- ADR anchor: [ADR-0006](../../adr/0006-adopt-project-local-and-shared-knowledge-base.md)
- Shared knowledge owner: `D:\Nautilus\global_docs\knowledge-common`

## 1. Purpose / 目的

P020 is the successor proposal for ADR-0006. It lands the acceptance-first governance plan for an Account Console project-local knowledge router, local knowledge base skeleton and prevention gate.

The proposal intentionally starts with acceptance and anti-drift boundaries before creating the actual `docs/knowledge/` files. The target architecture is:

```text
current proposal/change/acceptance truth
  -> docs/knowledge/blocker-routing.json
  -> matched local cards and optional shared patterns only
  -> prevention gate
```

## 2. Scope / 范围

In scope:

1. Freeze acceptance criteria for ADR-0006 landing.
2. Define anti-drift checks for full-library reads, shared/project fact mixing, current-state leakage and route target drift.
3. Define the required `docs/knowledge/` skeleton and initial route families.
4. Define the first Prevention Gate expectations for `scripts/check_knowledge_docs.py`.
5. Define how other projects should learn the structure without copying Account Console facts.

Out of scope:

1. Implementing all `docs/knowledge/` cards in this first acceptance slice.
2. Creating a vector database, RAG service, Obsidian plugin dependency or external memory service.
3. Moving current proposal/change/acceptance status into knowledge cards.
4. Storing raw passwords, auth codes, broker secrets, raw endpoints, account secrets or secret-bearing runtime material.
5. Changing ADR-0005/P019 broker observation decisions or acceptance.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p020-adr0006-account-console-knowledge-router
  architecture_owner: nautilus_account_console
  knowledge_owner: docs/knowledge/
  route_owner: docs/knowledge/blocker-routing.json
  prevention_gate_owner: scripts/check_knowledge_docs.py
  shared_knowledge_owner: D:/Nautilus/global_docs/knowledge-common
  write_authority:
    allowed:
      - project-local knowledge navigation and bug cards
      - blocker-to-card routing rules
      - route target and forbidden-content validation
      - adoption note for other projects
    forbidden:
      - current task status as knowledge truth
      - acceptance pass/fail verdicts as knowledge truth
      - runtime, account, broker, admission, approval, capital or trading-readiness truth
      - raw secrets or secret-bearing runtime material
      - shared knowledge copying project-local facts
  second_implementation_rejected:
    - knowledge base as proposal/change/acceptance state machine
    - router output as verdict, readiness, owner transfer or blocker closeout
    - shared knowledge base as project owner map or local evidence owner
    - Obsidian, Canvas or plugin state as governance truth
    - prevention gate pass as formal proposal acceptance without required artifacts
```

## 4. Review Verdict / 评审结论

**Current verdict**: `proposed`

| Item | Verdict |
| --- | --- |
| Formal proposal needed | yes |
| Requires ADR acceptance | yes, ADR-0006 |
| Requires child changes | yes |
| Allows full-library AI read by default | no |
| Allows shared knowledge to own project facts | no |
| Allows knowledge cards to close acceptance | no |

## 5. Document Map / 文档地图

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | proposal scope and owner boundary | present |
| `phase-plan.md` | ADR decision coverage and implementation phases | present |
| `acceptance.md` | acceptance-first baseline and anti-drift matrix | present |

## 6. Graduation / Closeout Matrix

| Graduation item | Policy | Target | Status |
| --- | --- | --- | --- |
| ADR landing pointer | required | [ADR-0006](../../adr/0006-adopt-project-local-and-shared-knowledge-base.md) | planned |
| Knowledge skeleton | required | `docs/knowledge/` | completed |
| Prevention gate | required | `scripts/check_knowledge_docs.py` | completed |
| Proposal-local evidence | archive_only | `acceptance.md` | completed |
