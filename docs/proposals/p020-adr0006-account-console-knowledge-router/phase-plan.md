# P020 ADR-0006 Account Console Knowledge Router Phase Plan / 分阶段推进计划

- Proposal ID: `p020-adr0006-account-console-knowledge-router`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20
- Linked proposal: [README.md](README.md)
- Linked acceptance: [acceptance.md](acceptance.md)
- ADR anchor: [ADR-0006](../../adr/0006-adopt-project-local-and-shared-knowledge-base.md)

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - docs/knowledge/
    - scripts/check_knowledge_docs.py
  allowed_evidence_roots:
    - docs/proposals/p020-adr0006-account-console-knowledge-router/
  source_issue_lists: []
  source_input_templates: []
  source_contract_templates:
    - D:/Nautilus/global_docs/knowledge-common/
    - docs/templates/dslresearch-reference/
```

## ADR Decision Coverage Mapping

Primary ADR: `ADR-0006`

| ADR decision item | Phase | Work | Acceptance row |
| --- | --- | --- | --- |
| D1 Shared vs project-local split | Phase 1 | local skeleton links to shared knowledge without copying project facts | A1, N2 |
| D2 Knowledge as non-truth-source | Phase 1 / 3 | README/card rules and forbidden status/truth wording gate | A2, N1, N3 |
| D3 Knowledge Router | Phase 2 | `blocker-routing.json` with matched-card routing only | A3, N4 |
| D4 Prevention Gate | Phase 3 | `check_knowledge_docs.py` validates structure, route targets and forbidden content | A4, N5 |
| D5 Repeat-bug memory | Phase 2 | bug-ledger template and seed bug cards with source refs/prevention gates | A5 |
| D6 AI minimal-read discipline | Phase 2 / 3 | route rules forbid default full-library reads | A6, N4 |
| D7 Cross-project learning | Phase 4 | adoption note states copy structure, rewrite facts | A7, N6 |
| D8 Obsidian boundary | Phase 1 / 4 | read-only projection wording, no plugin truth dependency | A8 |
| D9 Secret/runtime boundary | Phase 3 | gate rejects obvious secret-bearing and runtime truth fields | A9, N7 |

## Phase Status Board / Phase 状态表

| Phase | Goal | Current status | Evidence / Current facts | Next action |
| --- | --- | --- | --- | --- |
| Phase 0 Acceptance and anti-drift convergence | Land proposal README, phase-plan and acceptance before implementation | `completed` | P020 proposal opened with ADR-0006 coverage and anti-drift matrix; proposal docs gate passes | Phase 1-4 executed in same landing slice |
| Phase 1 Knowledge skeleton | Create `docs/knowledge/` entry files and boundary docs | `completed` | `docs/knowledge/README.md`, dashboard, playbook, boundary docs, bug ledger and template exist | keep docs under Knowledge Gate |
| Phase 2 Knowledge router and seed cards | Add `blocker-routing.json`, bug template and seed bug cards | `completed` | router has four initial route families; two seed bug cards exist | expand only through source-ref-backed cards |
| Phase 3 Prevention gate | Add `scripts/check_knowledge_docs.py` | `completed` | `python scripts/check_knowledge_docs.py --root . --selftest` passes with eight negative fixtures | wire into future governance checks if desired |
| Phase 4 Cross-project adoption note | Document how other projects copy the pattern safely | `completed` | `docs/knowledge/adoption-note.md` exists and forbids copying Account Console facts | use as local sample for other projects |

## Verification Commands

```bash
python scripts/check_proposal_docs.py --root . --proposal-id p020-adr0006-account-console-knowledge-router
python scripts/check_knowledge_docs.py --root .
```

Current verification:

| Command | Pass signal |
| --- | --- |
| `python scripts/check_knowledge_docs.py --root .` | `KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2` |
| `python scripts/check_knowledge_docs.py --root . --selftest` | `KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2 negative_fixtures=8` |
| `python scripts/route_knowledge.py --root . --query "can trade"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2` |
| `python scripts/route_knowledge.py --root . --query "raw broker payload screenshot truth"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2` |
| `python scripts/route_knowledge.py --root . --query "unrelated styling typo"` | `ROUTE_KNOWLEDGE_NO_MATCH: read=0 action=current_task_truth` |
| `python scripts/check_proposal_docs.py --root .` | `PROPOSAL_DOCS_OK: proposals=10` |

## Continuous Advancement Rule

P020 implementation gate has passed for the first landing slice. Future cards/routes must remain source-ref-backed and pass `check_knowledge_docs.py`.
