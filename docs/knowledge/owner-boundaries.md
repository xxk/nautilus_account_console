---
id: NAC-KB-BOUNDARY-0001
type: boundary
scope: project-local
area: owner-boundary
status: active
source_ref: AGENTS.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/ai-autopilot-playbook.md
---

# Owner Boundaries

Account Console owns read-only account observation contracts, reducers, APIs and UI projections.

It does not own:

1. Trading runtime truth.
2. Broker truth.
3. Account truth outside normalized read models.
4. Admission, approval, capital or trading-readiness truth.
5. Broker order submit, cancel, replace or modify authority.

If a task appears to require those owners, record a typed blocker or route to the owner repo. Do not create a second implementation inside Account Console.

