# ADR Index / ADR 索引

- Updated: 2026-06-20
- Project: `nautilus_account_console`
- Template: [ADR模板 / ADR Template](ADR模板_ADR%20Template.md)

## Current Binding ADRs

| ADR | Title | Binding rule |
| --- | --- | --- |
| [ADR-0001](0001-dslresearch-first-doc-template-and-gate-capability-backfill.md) | DSLresearch-first doc template and Gate capability backfill | When this repo lacks a documentation template or Gate/check capability, use `docs/templates/dslresearch-reference/` or inspect `D:\Nautilus\DSLresearch` first, then adapt the matching pattern to this repo's read-only account-console boundary. |
| [ADR-0002](0002-adopt-business-workbench-first-account-console-navigation.md) | Business workbench first account console navigation | Organize Account Console UI by Daily Closeout, Intraday Monitor, Account Workbench, Allocation Admin, Risk And Reconcile, Evidence Explorer and Stream Ops first; artifact routes are drill-downs, not the primary business model. |
| [ADR-0003](0003-adopt-contract-first-ui-slice-development.md) | Contract-first UI slice development | Future UI work must use contract-first panel slices; detailed implementation method, slice queue and change acceptance live in topic/proposal docs. |
| [ADR-0004](0004-adopt-account-mirror-observation-and-command-plane.md) | Account Capability Fabric with mirror readback | Account Console binds account identity to explicit observation, command, risk/approval, reconciliation and evidence capabilities; Account Mirror remains read-only and future commands must reconcile through mirror readback. |
| [ADR-0005](0005-account-console-independent-broker-observation-sessions.md) | Account Console Independent Broker Observation Sessions | Account Console may own governed read-only broker observation sessions through shared contracts, no-secret/no-command gates, durable observation evidence and Account Mirror projection; broker truth, command authority and complete-history claims remain external or typed blocked. |

## Proposed ADRs

| ADR | Title | Proposed question |
| --- | --- | --- |
| [ADR-0006](0006-adopt-project-local-and-shared-knowledge-base.md) | Project-Local Knowledge Router And Shared Knowledge Base | Decide how Account Console should establish a reusable project-local knowledge router and knowledge-base sample while adopting `D:\Nautilus\global_docs\knowledge-common`, minimizing AI context reads and avoiding a second truth source. |

## Usage Rules

1. Local ADRs govern `nautilus_account_console` only.
2. `D:\Nautilus\DSLresearch` is a reference source for documentation and governance patterns, not an account, broker, admission, capital or runtime truth owner for this project.
3. If a copied pattern conflicts with this repository's read-only boundaries, this repository's AGENTS.md and ADR-0045 account-console role win.
4. ADRs record stable decisions and option comparison. Implementation methods, task queues and change-level acceptance should be placed in `docs/topics/` and `docs/proposals/`.
