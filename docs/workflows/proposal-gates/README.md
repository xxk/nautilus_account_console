# Proposal Workflow Stage Contract / Proposal 工作流阶段契约

This directory ports the DSLresearch proposal workflow gate pattern into `nautilus_account_console`, with account-console-specific boundaries.

本目录把 DSLresearch 的 proposal workflow gate 模式裁剪到 Account Console，保留 proposal 文档约束，不复制 research runtime / Case Authority 语义。

| File | Reader | Purpose |
| --- | --- | --- |
| `proposal_gate_manifest.yaml` | machine / gate owner | Stage Contract manifest; defines Stage, advance Gate, Checks, Proof Items and fail signals |
| `proposal_gate_board.md` | human / reviewer / AI operator | Human-readable board with the same Stage/Gate ids and semantics |

## Authority Boundary

1. `proposal_gate_manifest.yaml` is the machine-readable source for Account Console proposal workflow stages.
2. `proposal_gate_board.md` is a human-readable projection and must not add gates absent from the manifest.
3. Runtime/source/account truth owners remain external or owner-specific; proposal gates cannot mint those truths.
4. UI design gates cannot be counted as browser-verified implementation closeout.
5. If this workflow conflicts with [Account Console owner map](../../ownership/account-console-owner-map.md), the owner map wins and this workflow must be fixed.

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
