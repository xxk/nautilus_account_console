# P011 Account Capability Fabric Landing Phase Plan / 分阶段推进计划

**创建日期**：2026-06-15
**最后更新**：2026-06-15
**状态**：in_progress_waiting_for_ctp_source_owner_packages
**proposal-id**：`p011-account-capability-contracts`
**Proposal ID**：`p011-account-capability-contracts`
**关联提案**：[README.md](README.md)
**关联验收**：[acceptance.md](acceptance.md)

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - contracts/account_capability/
    - contracts/ui/fixtures/account_capability/
    - data/account_mirror/
    - output/account_capability/
  allowed_evidence_roots:
    - docs/acceptance/
    - output/debug/p011-account-capability-contracts/
  source_issue_lists: []
  source_input_templates: []
  source_contract_templates:
    - contracts/ui/panels/account_summary_panel.contract.json
    - contracts/ui/fixtures/account_workbench/
```

Contract fixtures are deterministic examples only. They must not be treated as broker, runtime, account, capital, admission, approval, readiness or trading truth.

## ADR Decision Coverage Mapping

Primary ADR: `ADR-0004`
Cross-repo architecture constraint: `ADR-0047` in `nautilus_strategies`
Covered decisions: `D1`, `D2`, `D3`, `D4`, `D5`, `D6`, `D7`

ADR-0047 constrains this proposal after Phase 5. P011 may implement Account Console projection and UI readback, but it must not implement or replace the upstream `AccountRegistry`, `route_id` resolver, `AccountRuntimeContext`, runtime builder, CTP adapter, IB adapter, account ledger truth or order event truth.

The current real-account task is therefore split into:

1. source-owner package production in `nautilus_ctp_adapter`;
2. ADR-0047 route/context projection alignment in Account Console;
3. Account Mirror ingestion/projection;
4. UI readback comparison against pinned package/API projection.

| ADR decision item | ADR section / successor scenario | Phase | Child change or proposal-only work | Acceptance row |
| --- | --- | --- | --- | --- |
| D1 | Canonical account identity | Phase 1 | proposal implementation | A1 |
| D2 | Observation provenance | Phase 1 | proposal implementation | A2 |
| D3 | Account Mirror read-only boundary | Phase 1 | contract authority fields only | A3 |
| D4 | Capability Registry | Phase 1 | proposal implementation | A4 |
| D5 | Command separated from observation | Phase 7 | command design gate only | A7 |
| D6 | Fail-closed blockers | Phase 1 | typed blocker contract | A5 |
| D7 | Capability Fabric extension rule | Phase 0 / all phases | docs and schema review | A6 |
| ADR0047-D2 | AccountRuntimeContext route model | Phase 6a | projection alignment only; no runtime resolver | A8 |
| ADR0047-D4 | Capability separation | Phase 6a | market data, execution adapter and account truth must remain separate | A9 |
| ADR0047-D5 | Evidence partition by route/account | Phase 6a | route/account/source package evidence fields projected or blocked | A10 |
| ADR0047-D6 | Readiness gates do not substitute | Phase 6a / Phase 7 | no source/login/UI evidence implies Paper ready, Live ready or tradable | A11 |

## AI Tracking Status

<!-- AI-PHASE-STATUS-BEGIN
reviewed_at: 2026-06-15
reviewer: Codex
overall_status: in_progress_waiting_for_ctp_source_owner_packages
phases:
  - id: phase_0_proposal_convergence
    status: completed
    ai_progress: 100
    evidence: "README.md, phase-plan.md and acceptance.md created"
  - id: phase_1_contracts_and_fixtures
    status: completed
    ai_progress: 100
    evidence: "contracts/account_capability/account_capability_bundle.schema.json; contracts/ui/fixtures/account_capability; python scripts/validate_account_capability_contracts.py"
  - id: phase_2_mirror_projection_reader
    status: completed
    ai_progress: 100
    evidence: "backend/src/nautilus_account_console/account_mirror.py; scripts/validate_account_mirror_projection.py; backend/tests/test_account_mirror.py"
  - id: phase_3_source_bridges
    status: completed
    ai_progress: 100
    evidence: "contracts/source_artifacts/account_sources; backend/src/nautilus_account_console/source_bridge.py; scripts/validate_account_source_bridges.py; backend/tests/test_source_bridge.py"
  - id: phase_4_account_workbench_api_mode
    status: completed
    ai_progress: 100
    evidence: "backend/src/nautilus_account_console/main.py mirror endpoints; scripts/validate_account_mirror_api.py; backend/tests/test_mirror_api.py"
  - id: phase_5_source_health_and_evidence
    status: completed
    ai_progress: 100
    evidence: "account_mirror_source_health.v1 and account_mirror_evidence.v1 API responses; scripts/validate_account_source_health_evidence.py; backend/tests/test_mirror_api.py"
  - id: phase_6_ctp_real_account_consistency
    status: blocked
    ai_progress: 75
    evidence: "scripts/validate_ctp19053_consistency.py; scripts/validate_ctp025292_consistency.py; real-login UI fail-closed evidence; sample source package harness pass"
  - id: phase_6a_adr0047_route_context_alignment
    status: completed
    ai_progress: 100
    evidence: "route_context projected through source_bridge, AccountMirrorStore and mirror APIs; python scripts/validate_adr0047_route_context_alignment.py"
  - id: phase_7_command_capability_design_gate
    status: completed
    ai_progress: 100
    evidence: "docs/design/account-command-capability-design-gate.md; contracts/account_capability/command_capability_design_gate.json; scripts/validate_command_capability_design_gate.py"
AI-PHASE-STATUS-END -->

## Phase Status Board / Phase 状态表

| Phase | Goal | Current status | AI progress | Evidence / Current facts | Next action |
| --- | --- | --- | ---: | --- | --- |
| Phase 0 Proposal convergence | Freeze scope, ADR mapping and acceptance boundary | `completed` | 100% | proposal docs created | start Phase 1 contract implementation |
| Phase 1 Contracts and fixtures | Add account capability contracts and deterministic fixtures | `completed` | 100% | schema, positive fixtures, negative fixtures and validator exist; `ACCOUNT_CAPABILITY_CONTRACTS_OK: positive=3 negative=3` | start Phase 2 mirror projection reader |
| Phase 2 Mirror projection reader | Read canonical observations into account projections | `completed` | 100% | `ACCOUNT_MIRROR_PROJECTION_OK: projections=4`; backend mirror tests passed | start Phase 3 source bridges |
| Phase 3 Source bridges | Produce canonical observations from Nautilus Paper, CTP Paper `19053`, CTP Live `025292` and R1/P079 Stage 2 sandbox paper `simulated-001` artifacts | `completed` | 100% | `ACCOUNT_SOURCE_BRIDGES_OK: bundles=4 projections=4`; backend source bridge tests passed | start Phase 4 Account Workbench API mode |
| Phase 4 Account Workbench API mode | Expose API-backed account summary, positions, orders and capabilities to UI | `completed` | 100% | `/api/mirror/accounts*` endpoints validate; `ACCOUNT_MIRROR_API_OK: accounts=4`; desktop/tablet/mobile UI readback for blocked CTP `19053`, blocked CTP `025292` and `simulated-001` passes | start Phase 5 source health and evidence |
| Phase 5 Source health and evidence | Add source health, blockers and evidence drawer integration | `completed` | 100% | `ACCOUNT_SOURCE_HEALTH_EVIDENCE_OK: ready=2 blocked=2`; backend tests passed | start Phase 6 real-login CTP account consistency |
| Phase 6 CTP real-account consistency | Compare UI/API against pinned real-login CTP `19053` and `025292` source-owner packages | `blocked` | 75% | harnesses ready; default runs materialize source unavailable blockers; real-login UI specs pass fail-closed; sample package paths prove comparison logic only | source owner repairs PyO3 TD bridge, provides pinned packages at `output/account_capability/ctp-paper-19053/source-package.json` and `output/account_capability/ctp-live-025292/source-package.json`, then rerun |
| Phase 6a ADR-0047 route/context alignment | Ensure Account Console projections carry or block route context without becoming runtime owner | `completed` | 100% | `route_context` is projected through source bridges, mirror projection and API list/detail; `python scripts/validate_adr0047_route_context_alignment.py` returns `ADR0047_ROUTE_CONTEXT_ALIGNMENT_OK: accounts=4 route_contexts=4 negatives=2` | keep Phase 6 blocked on source-owner packages; keep route/context gate in regression |
| Phase 7 Command capability design gate | Freeze future command design without implementation | `completed` | 100% | command design gate doc, machine-readable gate and validator exist; no submit/cancel/replace implementation accepted | future command proposal must satisfy this gate before exposing actions |

## Phase 1 Deliverables

1. Account identity contract.
2. Account observation envelope contract.
3. Balance observation contract.
4. Position observation contract.
5. Order and fill/trade observation contracts.
6. Source health and typed blocker contracts.
7. Capability registry contract with disabled command capability.
8. Deterministic fixtures for:
   - `acct.nautilus.paper.demo`
   - `acct.ctp.paper.19053`
   - `acct.ctp.live.025292`

## Phase 2 Deliverables

1. Account Mirror projection reader for deterministic account observation artifacts.
2. Projection checkpoint metadata with source refs, checksums and replay cursor.
3. Negative projection behavior for stale, missing, schema-mismatched or checksum-mismatched sources.

## Phase 3 Deliverables

1. Nautilus Paper source artifact bridge.
2. CTP Paper `19053` real-login source package gate.
3. CTP Live `025292` real-login source package gate.
4. R1/P079 Stage 2 `simulated-001` sandbox paper fixture-only read-model bridge.
5. Source adapter boundary evidence proving Account Console backend/UI do not call broker APIs directly.

## Phase 4 Deliverables

1. Read-only Account Console API endpoints for account summary, balances, positions, orders, fills, source health, capabilities and evidence where supported.
2. Account Workbench API mode with deterministic fixture fallback.
3. Browser/API readback evidence for Nautilus Paper, blocked CTP Paper `19053`, blocked CTP Live `025292` and R1/P079 Stage 2 `simulated-001` where the corresponding route is in scope.

## Phase 5 Deliverables

1. Source health panel/read model.
2. Evidence rail/drawer source refs and checksums.
3. Typed blocker rendering for stale, missing, schema mismatch, checksum mismatch and capability missing.

## Phase 6 Deliverables

Phase 6 is intentionally split by owner.

Source-owner deliverables, outside Account Console authority:

1. Pinned CTP Paper `19053` real-login read-only source package.
2. Pinned CTP Live `025292` real-login read-only source package.
3. Read-only query evidence for funds, positions, orders and fills when present.

Account Console deliverables:

1. Source package validation and fail-closed typed blockers.
2. Account Mirror projection checkpoints derived from those packages.
3. UI/API comparison evidence for funds, positions, orders and fills when present.
4. Negative proof that command controls remain absent and Account Console does not call CTP directly.

## Phase 6a ADR-0047 Route Context Alignment Deliverables

1. Projection/acceptance fields for `route_id`, `account_alias`, `market_data_source`, `execution_adapter`, `account_truth`, `risk_domain` and `evidence_partition`, or typed blockers when the upstream route context artifact is missing.
2. Negative test: `market_data_source=ctp_md.025292` cannot become `execution_adapter=ctp_td.025292` or `account_truth=broker_ctp`.
3. Negative test: source package existence, UI render, CTP login, broker endpoint probe or source health cannot imply Paper ready, Live ready, production ready, capital allocated, broker tradable or can trade.
4. Negative test: Account Console does not introduce a runtime resolver, direct broker endpoint, second CTP adapter, second account ledger truth or second order event truth.
5. Positive test: each real-account UI row can explain source owner, source ref, checksum, route/account partition and projection checksum.

## Phase 7 Deliverables

1. Command capability design gate document: `docs/design/account-command-capability-design-gate.md`.
2. Machine-readable gate: `contracts/account_capability/command_capability_design_gate.json`.
3. Order intent, risk/approval, execution gateway, execution event, mirror readback and reconciliation contract shape defined for future proposal use.
4. Explicit statement that no submit/cancel/replace implementation is accepted by P011 Phase 7.
5. Executable gate: `python scripts\validate_command_capability_design_gate.py`.

## Runtime / Command Freeze

Phase 1 does not run broker, runtime, CTP, IB TWS or stock commands. Any command evidence in this proposal is contract validation only.

Phase 6 may run read-only CTP source collection only through the source adapter owner path and only to produce a pinned source package. Account Console backend/UI must not perform broker calls.
