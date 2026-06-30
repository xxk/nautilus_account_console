# Proposal Workflow Stage Contract / Proposal 工作流阶段契约

This directory keeps the local Account Console proposal workflow contract. It is not a workspace-level Shared Contract source.

本目录保留 Account Console proposal workflow 本地契约；本仓不放置全仓 shared contract 权威，也不作为其兼容入口。

| File | Reader | Purpose |
| --- | --- | --- |
| `proposal_gate_manifest.yaml` | machine / local contract | Local Account Console proposal workflow contract |
| `proposal_gate_board.md` | human / reviewer / AI operator | Human-readable board with the same Stage/Gate ids and semantics |

## Authority Boundary

1. Local `proposal_gate_manifest.yaml` is Account Console's local proposal workflow contract, not a Shared Contract alias/source.
2. `proposal_gate_board.md` is a human-readable local projection and must not create gates absent from the local manifest plus Account Console owner boundaries.
3. Workspace projections must not list this directory as a Shared Contract source.
4. Runtime/source/account truth owners remain external or owner-specific; proposal gates cannot mint those truths.
5. UI design gates cannot be counted as browser-verified implementation closeout.
6. If this workflow conflicts with [Account Console owner map](../../ownership/account-console-owner-map.md), the owner map wins and this workflow must be fixed.

## Two-Term Boundary

| Term | Short name | Machine value | Layer | Writes source truth? | Role |
| --- | --- | --- | --- | --- | --- |
| Proposal Gate | P-Gate | `proposal_gate` | proposal workflow | no | Blocks or allows proposal phase advancement. |
| Source Gate | S-Gate | `source_gate` | source/runtime/backend/frontend owner | yes, within its owner boundary | Produces source evidence, read models, browser evidence or typed blockers. |

P-Gates may require evidence produced by S-Gates. They must not write, mint, upgrade or infer source/runtime/account/browser closeout truth.

## Stage / Gate / Check / Proof Boundary

1. Stage is the top-level workflow unit.
2. Gate is the Stage advance verdict.
3. Check is the concrete condition evaluated inside a Gate.
4. Proof Item is the source evidence used by a Check.
5. New detail should become a Check or Proof Item by default; new Stages or Gates require real phase boundaries.
