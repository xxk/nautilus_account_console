# P023 UI Design / OpenCTP 19053 Paper Command

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted

## Screen

Route: `/accounts/acct.ctp.paper.19053`

Command UI remains hidden while `command.mode=disabled`. When `paper_armed`, Account Workbench adds a compact command strip and command status panel inside the existing account surface.

## Controls

| Control | State | Notes |
| --- | --- | --- |
| Submit | hidden until `paper_armed` | Creates `OrderIntent`; never calls broker directly from browser |
| Cancel | hidden until `paper_armed` and row has readback identity | Creates `CancelIntent` from row provenance |
| Replace | hidden | Out of scope |
| Risk evidence | visible after command attempt | Links risk decision ref |
| Readback evidence | visible after command attempt | Links Account Mirror readback ref |

## Data Test IDs

| Test ID | Purpose |
| --- | --- |
| `account-command-mode` | command mode display |
| `account-paper-command-banner` | paper-only warning |
| `account-submit-order-button` | guarded submit action |
| `account-cancel-order-button` | guarded cancel action on eligible row |
| `account-command-status-panel` | command audit status |
| `account-command-risk-ref` | risk evidence ref |
| `account-command-approval-ref` | approval evidence ref |
| `account-command-readback-ref` | readback evidence ref |
| `account-command-reconciliation-ref` | reconciliation evidence ref |

## Layout

The command strip must be dense and operational, not a marketing hero. It belongs near the open-order/fill area so the operator can compare intent, gateway event and readback state.

## Disabled State

When disabled, the page should not reserve empty command controls. It should keep the existing observation-only layout and expose the disabled command state in the source/capability panel.
