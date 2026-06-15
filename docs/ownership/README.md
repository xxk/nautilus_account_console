# Ownership Index / Owner 索引

- Updated: 2026-06-13
- Project: `nautilus_account_console`

## Canonical Owner Documents

| Document | Purpose |
| --- | --- |
| [Account Console owner map](./account-console-owner-map.md) | Authority owner, projection owner, UI owner and anti-second-implementation rules for Account Console. |

## Usage Rules

1. Use this folder for stable owner and authority boundaries.
2. Do not treat UI fixture `owner` fields as code owner or truth owner. Those fields are displayed operational owners only.
3. When a proposal introduces a new producer, verifier, projection, request surface or UI panel, it must update or explicitly confirm the owner map.
4. A blocker owned by an external repository or human authority must stay a typed blocker; Account Console must not implement a substitute writer.
