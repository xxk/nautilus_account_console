# P011 Account Capability Fabric Landing / 账户能力织构落地

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->
<!-- PROPOSAL-ADR-CARRIER-GATE:v1 -->

**proposal-id**：`p011-account-capability-contracts`
**Proposal ID**：`p011-account-capability-contracts`
**状态**：in_progress_waiting_for_ctp_source_owner_packages
**范围**：single umbrella proposal for ADR-0004 landing phases, now constrained by ADR-0047: contracts, Account Mirror projection, source bridges, API/UI mode, source health/evidence, read-only CTP `19053` / `025292` source-package consistency, AccountRuntimeContext projection alignment and command design gate

| 顶部状态块 / Top Status Block | 值 |
| --- | --- |
| ADR carrier | yes |
| Primary ADR | ADR-0004 |
| Carrier naming note | Account Capability Fabric umbrella landing proposal |
| Tracer input case dir | not_applicable |
| Tracer case id | not_applicable |
| Tracer case ref | not_applicable |

## 一句话结论

P011 is the single landing proposal for ADR-0004. The former P012-P017 slices are folded into P011 phases so contract, mirror, source, UI, real-account consistency and command-design work advance under one acceptance spine.

## Goals / 目标

1. Define namespace-qualified account identity and display alias rules.
2. Define canonical observation envelope and source provenance fields.
3. Define balance, position, order, fill/trade, source health and typed blocker contracts.
4. Define capability registry minimum fields, including disabled command capability.
5. Implement Account Mirror projection reader and API-backed Account Workbench mode through later phases.
6. Land source bridges for Nautilus Paper, CTP Paper `19053` and read-only CTP Live `025292` consistency.
7. Keep command design as a gate only until a separate command authority is accepted.

## Non-Goals / 非目标

1. No submit, cancel, replace, approval, allocation or trading-readiness capability.
2. No direct CTP/IB/stock broker calls from Account Console backend or UI.
3. No claim that CTP `025292` live values are accepted until the dedicated P011 Phase 6 evidence passes.
4. No broker-specific UI/API branches.

## Architecture Anchors / 架构锚点

| Anchor | Path |
| --- | --- |
| ADR | [ADR-0004](../../adr/0004-adopt-account-mirror-observation-and-command-plane.md) |
| Architecture design | [Account Capability Fabric architecture design](../../design/account-capability-fabric-architecture-design.md) |
| Topic | [T001 Account Mirror Observation Plane](../../topics/T001-account-mirror-observation-plane.md) |
| Roadmap | [T001 Account Capability Feature Roadmap](../../topics/roadmap/T001-account-capability-feature-roadmap.md) |
| ADR acceptance | [ADR-0004 acceptance](../../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md) |

## Current Status Snapshot / 当前状态快照

| Dimension | Current fact | Evidence |
| --- | --- | --- |
| ADR status | ADR-0004 is accepted and routes implementation through T001 | ADR-0004 |
| Topic status | T001 active; capability registry minimum precedes CTP `025292` consistency | T001 topic / roadmap |
| Proposal shape | P011 is the umbrella proposal; P012-P017 are not separate proposals | this README / roadmap |
| Contract status | Phase 1 passed with positive/negative contract fixtures | phase-plan.md / acceptance.md |
| Runtime status | observation stack implemented through Phase 5 plus R1/P079 Stage 2 `simulated-001` UI/read-model fixture; Phase 6 waits for pinned CTP `19053` and `025292` source-owner packages; Phase 6a ADR-0047 route/context projection alignment passes as a projection-only gate; Phase 7 command design gate complete | phase-plan.md / acceptance.md |
| Browser evidence | Account Workbench API readback has desktop/tablet/mobile screenshots for CTP Paper `19053`, blocked CTP Live `025292` and R1/P079 Stage 2 `simulated-001` | `../../acceptance/2026-06-15-p011-account-workbench-api-readback-browser-evidence.json` |

## Graduation / Closeout Matrix

| Graduation item | Policy | Target | Status |
| --- | --- | --- | --- |
| ADR backfill | required | ADR-0004 decision coverage matrix and current UI gate evidence | in_progress |
| Architecture / ownership backfill | required | Account Capability Fabric architecture design and owner map if contract owners change | planned |
| Proposal-local evidence | archive_only | `acceptance.md` | active |

## Document Map / 文档地图

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | proposal scope and ADR carrier declaration | present |
| `phase-plan.md` | phase order and trust boundary | present |
| `acceptance.md` | contract acceptance baseline | present |

## Open For Implementation / 可开工范围

Implementation may continue within the P011 phase spine, but the current real-account task must be finer than one UI task.

Phase 1 through Phase 5 are accepted for their scoped repo-local deliverables. Phase 6 remains blocked until the source owner publishes pinned read-only CTP Paper `19053` and CTP Live `025292` source packages. Phase 6a route/context separation is accepted as an Account Console projection gate, and Phase 7 is accepted as a design gate only; neither authorizes submit, cancel or replace implementation.

ADR-0047 alignment rule:

1. Account Console may project `account_id`, display alias, source health, balances, positions, orders, fills, reconciliation and evidence refs.
2. Account Console must not own `AccountRegistry`, `route_id`, `AccountRuntimeContext`, runtime builder, broker connectivity, account truth, order truth or readiness truth.
3. Any displayed real-account value must join through an explicit route/context projection carrying `market_data_source`, `execution_adapter`, `account_truth`, `risk_domain` and `evidence_partition`, or fail closed with a typed blocker.
4. `market_data_source` must never imply `execution_adapter` or `account_truth`; this is especially required for CTP `025292` market-data-only use in R1/P079 Stage 2 `simulated-001`.

P011 phase spine:

| Phase | Former slice | Scope |
| --- | --- | --- |
| Phase 1 | P011 | account capability contracts and deterministic fixtures |
| Phase 2 | P012 | Account Mirror projection reader |
| Phase 3 | P013 | Nautilus Paper and CTP Paper `19053` source bridges |
| Phase 4 | P014 | Account Workbench API mode |
| Phase 5 | P015 | source health and evidence |
| Phase 6 | P017 | CTP `19053` / `025292` source-owner package and UI consistency |
| Phase 6a | included in Phase 6 | ADR-0047 `AccountRuntimeContext` projection alignment gate |
| Phase 7 | P016 | command capability design gate |

## Command Capability Boundary

Phase 7 is complete only as architecture/design acceptance. The accepted gate is [Account Command Capability design gate](../../design/account-command-capability-design-gate.md) plus `contracts/account_capability/command_capability_design_gate.json`.

The next command proposal must still provide concrete command contracts, fixtures, risk/approval authority, execution gateway ownership, readback reconciliation and UI/API acceptance before any order action is exposed.
