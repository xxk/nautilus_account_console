# Cross-Project Adoption Note

Other projects may copy this structure:

```text
docs/knowledge/
  README.md
  00-dashboard.md
  project-playbook.md
  blocker-routing.json
  bug-ledger/
  templates/
```

They must rewrite:

1. Owner boundaries.
2. Route ids and route triggers.
3. Local bug cards.
4. Local commands and prevention gates.
5. Project-specific forbidden claims.

They must not copy Account Console owner facts, broker examples, P019/P020 evidence, UI labels or bug cards as their own project truth.

Shared reusable patterns belong in `D:\Nautilus\global_docs\knowledge-common`; project facts stay in the project-local knowledge base.

