# P011 Acceptance / 验收基线

**proposal-id**：`p011-account-capability-contracts`
**Proposal ID**：`p011-account-capability-contracts`
**状态**：in_progress_waiting_for_ctp_source_owner_packages

## Scope / 验收范围

This proposal accepts phased landing for ADR-0004 and is now constrained by ADR-0047 unified broker account runtime routing. P011 is an umbrella proposal. A phase may pass only its own acceptance rows; passing one phase does not imply later phases are complete.

After ADR-0047, real-account consistency acceptance is not a single UI task. It requires:

1. a source-owner package from `nautilus_ctp_adapter`;
2. an Account Console projection that preserves or blocks route/context fields;
3. UI/API comparison against the pinned projection;
4. negative evidence that Account Console did not become broker/runtime/account/order truth.

In scope:

1. Phase 1 account capability contracts and deterministic fixtures;
2. Phase 2 Account Mirror projection reader;
3. Phase 3 Nautilus Paper and CTP Paper `19053` source bridges;
4. Phase 4 Account Workbench API mode;
5. Phase 5 source health and evidence;
6. Phase 6 CTP Paper `19053` and CTP Live `025292` source-package UI consistency;
7. Phase 6a ADR-0047 `AccountRuntimeContext` projection alignment;
8. Phase 7 command capability design gate.

Out of scope:

1. submit/cancel/replace commands;
2. Account Console backend/UI direct broker calls;
3. live trading readiness;
4. capital allocation or approval;
5. treating P011 phase evidence as broker/account truth.

## Mandatory Gate Coverage / 必需 Gate 覆盖

| Gate | Requirement | Applies when | Must fail if | Status |
| --- | --- | --- | --- | --- |
| G1 | ADR-0004 decision coverage is mapped to contract deliverables | all P011 work | a contract is added without ADR decision mapping | passed_for_phase_1 |
| G2 | positive and negative contract acceptance both exist | each contract | only happy-path fixture exists | passed_for_phase_1 |
| G3 | anti-drift guard rejects broker-specific UI/API contracts | all schemas | schema introduces CTP-only UI fields or direct broker endpoint fields | passed_for_phase_1 |
| G4 | command capability defaults disabled | all account fixtures | fixture infers command ability from paper/live account kind | passed_for_phase_1 |
| G5 | source provenance is required | all live-looking values | balance/position/order/fill can exist without source ref/checksum or typed blocker | passed_for_phase_1 |
| G6 | phase ordering is enforced | each phase closeout | later phase passes while its prerequisite phase is unmapped or blocked without an explicit independent design-gate exception | passed_for_phase_7 |
| G7 | CTP `19053` and `025292` consistency uses pinned source/projection packages | Phase 6 | moving latest endpoint, repo-local sample, screenshot-only evidence or direct broker UI call is accepted | blocked_waiting_for_source_owner_packages |
| G8 | command design gate remains design-only | Phase 7 | submit/cancel/replace UI, API or gateway implementation appears from P011 Phase 7 | passed_for_phase_7 |
| G9 | ADR-0047 route/context separation is preserved | Phase 6a and later | `market_data_source` implies `execution_adapter` or `account_truth`; route context is missing but UI claims real-account consistency | passed_for_phase_6a |
| G10 | readiness substitution is rejected | Phase 6a and later | source package, CTP login, endpoint probe, UI screenshot or source health is treated as Paper ready, Live ready, broker tradable, capital allocated or can trade | passed_for_phase_6a |

## ADR Carrier Acceptance Matrix

| ID | Primary ADR | ADR decision item | ADR successor scenario | Positive path | Must fail if | Authority / retirement boundary | Minimal evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | ADR-0004 | D1 | Canonical account identity | schemas and fixtures use `acct.*` IDs and display aliases | bare `19053` or `025292` is canonical identity | Account Console owns display projection only | `python scripts\validate_account_capability_contracts.py` | passed_for_phase_1 |
| A2 | ADR-0004 | D2 | Observation provenance | observation contracts require source owner/ref/checksum/observed time or blocker | live-looking value lacks provenance | source remains external truth owner | `invalid_missing_provenance.json` rejected | passed_for_phase_1 |
| A3 | ADR-0004 | D3 | Account Mirror read-only boundary | contracts describe observations/projections only | contract contains submit/cancel/replace/write fields | Account Mirror is not command owner | command disabled assertions in validator | passed_for_phase_1 |
| A4 | ADR-0004 | D4 | Capability registry | account capability contract declares observation, command, reconciliation and evidence capability | UI can infer capability from account kind | registry is projection contract, not broker truth | three account capability fixtures validate | passed_for_phase_1 |
| A5 | ADR-0004 | D6 | Fail-closed blockers | missing/stale/source mismatch/capability missing states are typed | empty success replaces blocker | no fallback truth writer | 19053/025292 pending source blockers validate | passed_for_phase_1 |
| A6 | ADR-0004 | D7 | Capability extension rule | new account behavior must map to accepted capability | broker-specific plane or UI branch appears | ADR/topic/proposal accepts new capability | schema + proposal phase mapping | passed_for_phase_1 |
| A7 | ADR-0004 | D5 | Command separated from observation | command design gate defines order intent/risk/approval/gateway/event/readback/reconciliation without implementation | command UI or gateway implementation appears from P011 evidence alone | command authority remains separate | `python scripts\validate_command_capability_design_gate.py` | passed_design_gate_only |
| A8 | ADR-0047 | D2 | AccountRuntimeContext route model | projection carries `route_id`, `account_alias` and route/context refs or typed blocker | UI claims real-account consistency without route/context partition | Account Console projects context only; runtime owner remains external | `python scripts\validate_adr0047_route_context_alignment.py` | passed_for_phase_6a |
| A9 | ADR-0047 | D4 | Capability separation | projection separates `market_data_source`, `execution_adapter` and `account_truth` | CTP market data source becomes account truth or execution adapter by inference | Account Console cannot infer broker capability from source kind | `ADR0047_ROUTE_CONTEXT_ALIGNMENT_OK: accounts=4 route_contexts=4 negatives=2` | passed_for_phase_6a |
| A10 | ADR-0047 | D5 | Evidence partition | orders/fills/account/position/reconcile evidence is partitioned by route/account/truth/evidence partition | evidence rows are joined by display alias, latest path or screenshot text | evidence owner remains source/runtime/account ledger owner | mirror list/detail exposes `route_id` and `evidence_partition` | passed_for_phase_6a |
| A11 | ADR-0047 | D6 | Readiness gates do not substitute | UI/source evidence remains observation-only | source package, CTP login or UI pass claims Paper ready, Live ready or tradable | readiness/admission/capital owners remain external | route context gate plus boundary checks keep readiness truth false | passed_for_phase_6a |

## Phase Acceptance Matrix / Phase 验收矩阵

| Phase | Acceptance target | Positive proof | Must fail if | Status |
| --- | --- | --- | --- | --- |
| Phase 1 | contracts and deterministic fixtures | schema validation and positive/negative fixtures for identity, observations, blockers and capabilities | contract contains direct broker endpoint or command writer fields | passed |
| Phase 2 | Account Mirror projection reader | source artifact projects to checkpointed read model with refs/checksums | projection mutates broker/runtime truth or silently repairs source data | passed |
| Phase 3 | source bridges | Nautilus Paper and CTP Paper `19053` emit canonical observations | Account Console backend/UI calls broker APIs directly | passed |
| Phase 4 | API-backed Account Workbench | UI/API read projections and retain deterministic fixture fallback | UI renders broker-specific branches or command controls | passed |
| Phase 5 | source health and evidence | stale/missing/checksum/blocker states render with evidence refs | missing source is hidden as empty success | passed |
| Phase 6 | CTP `19053` / `025292` source-package UI consistency | pinned source/projection/UI comparison for funds, positions, orders and fills when present | values mismatch, source package is unpinned, sample data is treated as broker truth, direct CTP calls appear in Account Console, or command controls appear | blocked_waiting_for_source_owner_packages |
| Phase 6a | ADR-0047 route/context projection alignment | route/context fields are projected or blocked; market data, execution adapter and account truth remain separate | route context missing but UI claims consistency, market data becomes account truth, or readiness is inferred | passed_for_phase_6a |
| Phase 7 | command design gate | future command contract boundaries accepted without implementation | submit/cancel/replace is implemented or implied | passed_design_gate_only |

## Scenario Matrix / 场景矩阵

| ID | Type | Scenario | Acceptance method | Pass signal | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | success | `acct.ctp.paper.19053` fixture validates with display alias `19053` and command disabled | schema/fixture validation | valid fixture | passed |
| S2 | success | `acct.ctp.live.025292` fixture validates with display alias `025292`, observation enabled and command disabled | schema/fixture validation | valid fixture | passed |
| S3 | success | order/fill contracts carry source refs and account/order lineage | schema/fixture validation | valid fixture | passed |
| N1 | failure | bare account alias is used as canonical id | negative fixture validation | rejected | passed |
| N2 | failure | balance/position/order value lacks source provenance | negative fixture validation | rejected | passed |
| N3 | failure | command controls or gateway authority are inferred from `source_mode=live_observation` | negative fixture validation | rejected | passed |
| N4 | drift | schema adds direct CTP/IB/stock UI endpoint fields | schema audit | rejected | passed_for_phase_1 |
| N5 | drift | later P011 phase closes without prerequisite phase evidence | phase acceptance audit | rejected | planned |
| N6 | failure | CTP `19053` or `025292` acceptance uses moving latest data, repo-local sample as broker truth or screenshot-only evidence | Phase 6 audit | rejected | planned |
| N7 | blocker | CTP `19053` or `025292` pinned source package is missing | Phase 6 harness | `ctp19053_source_unavailable` / `ctp025292_source_unavailable` | passed |
| N8 | failure | P011 Phase 7 exposes command UI/API or broker gateway implementation | command design gate validator | rejected | passed |
| N9 | failure | `market_data_source=CTP 025292` is treated as a trading account or `account_truth=broker_ctp` for `simulated-001` | Phase 6a ADR-0047 alignment audit | rejected | passed_for_phase_6a |
| N10 | failure | source package, UI value match or source health is used to claim Paper ready, Live ready, broker tradable, can trade, production ready or capital allocated | Phase 6a forbidden-claim audit | rejected | passed_for_phase_6a |
| N11 | failure | Account Console adds a runtime resolver, CTP adapter, order writer, account ledger writer or order event truth writer | owner-boundary and code audit | rejected | planned |

## Evidence

| Evidence | Path or command | Conclusion |
| --- | --- | --- |
| Proposal docs gate | `python scripts\check_proposal_docs.py --root .` | `PROPOSAL_DOCS_OK: proposals=7` |
| Owner boundary gate | `python scripts\validate_owner_boundaries.py` | `owner boundary validation passed` |
| ADR004/P011 landing consistency gate | `python scripts\validate_adr004_p011_landing_consistency.py` | `ADR004_P011_LANDING_CONSISTENCY_OK: accounts=4 routes=4 screenshots=12 blockers=ctp19053_source_unavailable,ctp025292_source_unavailable` |
| P011 account capability contract validation | `python scripts\validate_account_capability_contracts.py` | `ACCOUNT_CAPABILITY_CONTRACTS_OK: positive=3 negative=3` |
| P011 Account Mirror projection validation | `python scripts\validate_account_mirror_projection.py` | `ACCOUNT_MIRROR_PROJECTION_OK: projections=4` |
| P011 source bridge validation | `python scripts\validate_account_source_bridges.py` | `ACCOUNT_SOURCE_BRIDGES_OK: bundles=4 projections=4` |
| P011 mirror API validation | `python scripts\validate_account_mirror_api.py` | `ACCOUNT_MIRROR_API_OK: accounts=4` |
| P011 source health/evidence validation | `python scripts\validate_account_source_health_evidence.py` | `ACCOUNT_SOURCE_HEALTH_EVIDENCE_OK: ready=2 blocked=2` |
| P011 command capability design gate | `python scripts\validate_command_capability_design_gate.py` | `COMMAND_CAPABILITY_DESIGN_GATE_OK: phase=p011.phase_7 status=design_gate_only` |
| P011 UI readback evidence validation | `python scripts\validate_p011_ui_readback_evidence.py` | `P011_UI_READBACK_EVIDENCE_OK: routes=4 screenshots=12 verdict=passed` |
| P079 Stage 2 simulated-001 Account Console gate | `python scripts\validate_p079_stage2_simulated_001.py` | `P079_STAGE2_SIMULATED_001_OK: account=simulated-001 market_source=025292 role=market_data_only screenshots=3`; acceptance: `../../acceptance/2026-06-15-p079-stage2-simulated-001-account-console-acceptance.md` |
| P011 Account Workbench API-backed UI readback | `cd frontend && npx playwright test tests/e2e/account-terminal-workbench.spec.ts` | CTP Paper `19053` and CTP Live `025292` render fail-closed blocked projections until real-login source packages exist; R1/P079 Stage 2 `simulated-001` is visible as Nautilus Sandbox Paper / simulated ledger only with broker submission disabled; desktop/tablet/mobile browser evidence recorded at `../../acceptance/2026-06-15-p011-account-workbench-api-readback-browser-evidence.json` |
| CTP 19053 real-login UI acceptance | `cd frontend && npx playwright test tests/e2e/ctp19053-ui-funds-positions.spec.ts --project=desktop` | `verdict=blocked`; UI displays typed blocker and does not display repo-local sample funds/positions as real account truth |
| CTP 025292 real-login UI acceptance | `cd frontend && npx playwright test tests/e2e/ctp025292-ui-funds-positions.spec.ts --project=desktop` | `verdict=blocked`; UI displays typed blocker and does not display repo-local sample funds/positions as real account truth |
| CTP 19053 default real-source harness | `python scripts\validate_ctp19053_consistency.py --write-blocker` | `CTP19053_CONSISTENCY_BLOCKED: blocker=ctp19053_source_unavailable`; real source package expected from source owner at `output/account_capability/ctp-paper-19053/source-package.json` |
| CTP 19053 sample consistency harness | `python scripts\validate_ctp19053_consistency.py --source-package contracts\source_artifacts\samples\ctp_paper_19053_sample_source.json` | `CTP19053_CONSISTENCY_OK: verdict=passed`; proves comparison logic only, not current broker truth |
| CTP 025292 default consistency harness | `python scripts\validate_ctp025292_consistency.py --write-blocker` | `CTP025292_CONSISTENCY_BLOCKED: blocker=ctp025292_source_unavailable`; real source package expected from source owner at `output/account_capability/ctp-live-025292/source-package.json` |
| ADR-0047 route/context alignment gate | `python scripts\validate_adr0047_route_context_alignment.py` | `ADR0047_ROUTE_CONTEXT_ALIGNMENT_OK: accounts=4 route_contexts=4 negatives=2`; proves or blocks `route_id`, `account_alias`, `market_data_source`, `execution_adapter`, `account_truth`, `risk_domain` and `evidence_partition`; rejects market-data-as-account-truth and readiness substitution |
| CTP 025292 sample consistency harness | `python scripts\validate_ctp025292_consistency.py --source-package contracts\source_artifacts\samples\ctp_live_025292_sample_source.json` | `CTP025292_CONSISTENCY_OK: verdict=passed` |
| Backend tests | `python -m pytest backend\tests` | `20 passed` |
| Frontend build | `cd frontend && npm run build` | build passed |

## Closeout Checklist

1. Contract files and fixtures exist under the trusted artifact roots.
2. Positive and negative fixture validation evidence is recorded.
3. ADR-0004 acceptance rows A1-A6 are updated from `planned`.
4. T001 roadmap remains aligned with P011 as the first implementation proposal.
5. No source connectivity, broker read or UI rendering is claimed beyond the phase evidence that has passed.
6. Phase 6 remains blocked until the external source owner provides pinned CTP `19053` and `025292` read-only packages. The blockers are accepted evidence of fail-closed behavior, not passed real-account consistency runs.
7. Phase 6a passes as a projection alignment gate. It does not accept real-account UI consistency, runtime builder implementation, broker tradability, readiness or can-trade.
8. Phase 7 accepts only the command design gate. It does not accept submit, cancel, replace, broker gateway, approval, risk, capital or live trading readiness implementation.
