---
id: NAC-KB-BOUNDARY-0002
type: boundary
scope: project-local
area: read-model
status: active
source_ref: docs/adr/0004-adopt-account-mirror-observation-and-command-plane.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/validation-playbook.md
---

# Account Console Read-Model Boundary

Account Console UI and API must consume typed read models, source packages or Account Mirror projections.

Raw broker callback payloads, screenshots and provenance blobs may help debugging, but they are not canonical account, order, fill, funds or position truth.

When raw report wording appears in a task, check whether the current path maps it into normalized read models before any UI or acceptance claim.

