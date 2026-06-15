# UI Design Index / UI 设计索引

- Updated: 2026-06-14
- Project: `nautilus_account_console`

## Design Documents

| Document | Status | Purpose |
| --- | --- | --- |
| [Account Console UI MVP](./account-console-ui-mvp.md) | baseline | MVP UI skeleton and first operational direction. |
| [Account Console capability UI design](./account-console-capability-ui-design.md) | baseline | Business capability surfaces, routes and workbench-level UI design. |
| [Account Console UI implementation design](./account-console-ui-implementation-design.md) | active | Global implementation-level UI design rules for AI-assisted panel slices. |
| [Account Console UI landing blueprint](./account-console-ui-landing-blueprint.md) | active | Product-level landing guardrails that prevent implementation drift. |
| [Account Console UI landing preview](./account-console-ui-landing-preview.html) | preview | Static visual preview for review before product implementation. |
| [Account Console order observation preview](./account-console-order-observation-preview.html) | preview | Static visual preview for the Account Workbench Orders and Order Lifecycle surface. |

## Usage Rules

1. Use capability UI design to understand the business surface.
2. Use implementation UI design before coding any route, panel or component.
3. Use the landing blueprint to freeze first viewport, navigation, copy, evidence and closeout behavior before implementation.
4. Each proposal should add its own panel-level `ui-design.md` when it owns a concrete UI slice.
