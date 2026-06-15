# Proposal Workflow Stage Contract Board / Proposal 工作流阶段契约看板

This board is the human-readable projection of `proposal_gate_manifest.yaml`.

本看板帮助人工和 AI 快速判断 Account Console proposal 是否能进入下一阶段。

## Terms

| Formal term | Short name | Machine value | Layer | Controls | Must not do |
| --- | --- | --- | --- | --- | --- |
| Proposal Gate | P-Gate | `proposal_gate` | proposal workflow | proposal phase advancement | write runtime/account/broker/admission/capital/trading-readiness truth |
| Source Gate | S-Gate | `source_gate` | owner source evidence | contracts, fixtures, UI rendering, backend/Rust/frontend evidence | be inferred from proposal prose alone |

## Stage Contract View

| Stage | Advance Gate | Checks | Proof Items |
| --- | --- | --- | --- |
| scaffold | PG-S0-SCAFFOLD | `proposal_scaffold_required_fragments` | `README.md`; `phase-plan.md`; `acceptance.md` |
| workflow_contract | PG-S1-WORKFLOW-CONTRACT | `workflow_contract_boundary`; `owner_boundary_present` | workflow metadata; Owner Boundary; non-goals |
| ui_design_acceptance | PG-S2-UI-DESIGN-ACCEPTANCE | `ui_design_acceptance_present`; `route_matrix_mapped`; `anti_drift_present` | `ui-design.md`; `ui-acceptance.md`; route coverage row; anti-drift block |
| source_contracts | PG-S3-SOURCE-CONTRACTS | `source_contracts_or_blockers_present`; `fixtures_or_blockers_present` | contracts; fixtures; typed blockers |
| implementation_evidence | PG-S4-IMPLEMENTATION-EVIDENCE | `implementation_evidence_present_or_blocked`; `browser_evidence_present_or_blocked` | build/test output; browser screenshots; typed blockers |
| issue_ledger | PG-S5-ISSUE-LEDGER | `issue_ledger_mapping_present_when_needed` | issue/blocker rows; current acceptance landing; next action |
| closeout | PG-S6-CLOSEOUT | `local_checks_pass`; `forbidden_scan_pass`; `matrix_status_truthful` | proposal docs gate; owner boundary validation; forbidden scan; route matrix update |

| Stage | Gate ID | Human question | Machine check | Missing signal |
| --- | --- | --- | --- | --- |
| Scaffold | PG-S0-SCAFFOLD | Proposal 是否有必需文档? | `proposal_scaffold_required_fragments` | `missing_proposal_scaffold` |
| Workflow Contract | PG-S1-WORKFLOW-CONTRACT | Proposal 是否声明 workflow / owner boundary 且没有第二 owner? | `workflow_contract_boundary` | `missing_workflow_contract_boundary` |
| UI Design Acceptance | PG-S2-UI-DESIGN-ACCEPTANCE | UI proposal 是否有设计、验收、anti-drift 和 route matrix 映射? | `ui_design_acceptance_present` | `missing_ui_design_acceptance` |
| Source Contracts | PG-S3-SOURCE-CONTRACTS | 需要 contract/fixture 时是否已有证据或 typed blocker? | `source_contracts_or_blockers_present` | `missing_source_contract_or_blocker` |
| Implementation Evidence | PG-S4-IMPLEMENTATION-EVIDENCE | 实现后是否有 build/test/browser/render 证据或 typed blocker? | `implementation_evidence_present_or_blocked` | `missing_implementation_evidence` |
| Issue Ledger | PG-S5-ISSUE-LEDGER | 本轮发现的 bug/blocker/carry-forward 是否写入 proposal-local ledger? | `issue_ledger_mapping_present_when_needed` | `missing_issue_ledger_entry` |
| Closeout | PG-S6-CLOSEOUT | closeout 是否区分 design gate 与 browser verified，且本地检查通过? | `matrix_status_truthful` | `closeout_gate_failed` |

## Non-Authority Rules

1. This board must not add gates absent from the manifest.
2. Proposal Gates cannot write source/runtime/account truth.
3. UI design text cannot count as browser-render evidence.
4. Missing required proof after its phase must fail or produce a typed blocker.
5. Gate growth should happen as Checks or Proof Items unless a durable stage boundary is added.
