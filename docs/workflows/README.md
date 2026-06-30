# Workflow Reading Guide / 工作流阅读指南

- Updated: 2026-06-14
- Project: `nautilus_account_console`

This directory defines local workflow constraints for proposal-bound Account Console work. It does not place or adopt a workspace-level Shared Contract.

本目录约束 Account Console 的 proposal 推进方式；本仓不放置也不采用全仓 Shared Contract。

## Authorized Machine Contract

| Path | Role |
| --- | --- |
| [proposal-gates/proposal_gate_manifest.yaml](./proposal-gates/proposal_gate_manifest.yaml) | local Account Console proposal workflow contract |
| [proposal-gates/proposal_gate_board.md](./proposal-gates/proposal_gate_board.md) | human-readable projection of the same local stages and gates |

## Boundary

1. Account Console keeps only its local proposal workflow contract; it must not appear as a Shared Contract source in workspace projections.
2. Workflow gates are Proposal Gates. They may block proposal advancement but cannot write runtime, broker, account, admission, approval, capital or trading-readiness truth.
3. UI/browser evidence proves rendering only. It never proves account, order, fill, position, settlement, equity, broker, admission or capital truth.
4. Missing required proof after its phase must become a typed blocker, not a warning-only note.
5. Proposal phases must keep design-gate readiness separate from implementation/browser-verified closeout.
6. This workflow does not replace proposal-local `acceptance.md`, `phase-plan.md`, `ui-design.md`, `ui-acceptance.md` or issue/blocker ledgers.

## Local Gate Command

```powershell
python scripts\check_proposal_docs.py --root .
python scripts\check_proposal_docs.py --root . --proposal-id p004-account-workbench-summary-panel
```
