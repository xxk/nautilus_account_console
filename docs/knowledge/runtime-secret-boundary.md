---
id: NAC-KB-BOUNDARY-0004
type: boundary
scope: project-local
area: secret-boundary
status: active
source_ref: AGENTS.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/bug-patterns/README.md
---

# Runtime Secret Boundary

This repository must not become the owner of raw broker secrets, account secrets, raw endpoint values or secret-bearing runtime material.

Use references only:

1. `ctp_config_ref`
2. `ctp_secret_ref`
3. `broker_profile_ref`
4. `owner_repo_path`
5. redacted shape or checksum
6. `raw_secret_values_recorded=false`

If a task needs sensitive runtime material, resolve owner references from the appropriate owner repo and keep raw values out of docs, evidence, logs and chat.

