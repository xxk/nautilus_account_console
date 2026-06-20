---
id: NAC-KB-BOUNDARY-0003
type: boundary
scope: project-local
area: ui-projection
status: active
source_ref: AGENTS.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/validation-playbook.md
---

# UI Projection Boundary

UI may show source health, lag, blockers and readback state. UI must not promote observation into admission, approval, capital, broker tradability or command authorization.

Use wording such as:

1. `source blocked`
2. `readback unavailable`
3. `command disabled`
4. `typed blocker`

Do not use UI wording to claim operational readiness or ability to trade.

