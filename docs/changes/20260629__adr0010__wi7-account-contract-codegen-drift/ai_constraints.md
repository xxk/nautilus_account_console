---
work_item_type: governance
work_item_layer: change
surface_mode: none
action_mode: read_only
---

# AI Constraints

- Do not edit generated account JSON schema or generated TypeScript account contract types by hand.
- Use `python scripts/generate_account_contracts.py` after changing `AccountKind`, `AccountSnapshot`, `AccountEvent`, `OrderEvent`, or `OrderExecutionReports`.
- Keep browser evidence retirement out of this WI-7 change.
- Do not broaden this child change into UI panel contract generation.

