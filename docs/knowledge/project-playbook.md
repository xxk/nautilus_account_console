---
id: NAC-KB-PLAYBOOK-0001
type: playbook
scope: project-local
area: ai-routing
status: active
source_ref: docs/adr/0006-adopt-project-local-and-shared-knowledge-base.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/ai-autopilot-playbook.md
---

# Project Playbook

## AI Reading Order

1. Read current task truth first: active proposal/change/acceptance, AGENTS and owner docs.
2. If a known risk appears, consult [blocker-routing.json](blocker-routing.json).
3. Read only the matched local cards and optional shared pattern files.
4. Fix or record the current task in its proposal/change/acceptance.
5. Add or update knowledge only after the current task has a source reference.

## Promotion Loop

```text
current evidence
  -> project-local bug card
  -> shared pattern only if project-independent
  -> prevention gate when machine-checkable
```

Knowledge lookup is conditional and subordinate to current task truth.

