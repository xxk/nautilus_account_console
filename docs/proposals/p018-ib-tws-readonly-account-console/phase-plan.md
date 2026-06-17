# P018 IB TWS Read-Only Account Console Phase Plan / 分阶段推进计划

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready
- Created: 2026-06-17
- Updated: 2026-06-17
- Linked proposal: [README.md](README.md)
- Linked acceptance: [acceptance.md](acceptance.md)

## Artifact Trust Boundary

```yaml
artifact_boundary:
  trusted_artifact_roots:
    - contracts/account_capability/
    - contracts/source_artifacts/account_sources/
    - contracts/ui/fixtures/account_capability/
    - data/account_mirror/
    - output/account_capability/ib-live-u3028269/
  allowed_evidence_roots:
    - docs/acceptance/
    - docs/acceptance/browser-evidence/p018-ib-tws-readonly-account-console/
    - output/debug/p018-ib-tws-readonly-account-console/
  source_issue_lists: []
  source_input_templates: []
  source_contract_templates:
    - docs/proposals/p011-account-capability-contracts/
    - ../nautilus_strategies/cfgs/ib_paper.json
    - ../nautilus_strategies/scripts/probe_tws_version.py
```

The `source_contract_templates` are recall/template refs only. They are not P018 pass evidence. Formal pass evidence for live IB readback must be a same-slice owner-produced IB source package plus Account Console projection/UI readback.

## ADR Decision Coverage Mapping

Primary ADR: `ADR-0004`
Covered decisions: `D1`, `D2`, `D3`, `D4`, `D5`, `D6`, `D7`

| ADR decision item | ADR section / successor scenario | Phase | Work | Acceptance row |
| --- | --- | --- | --- | --- |
| D1 | Canonical account identity | Phase 1 | IB account id alias and registry projection | A1 |
| D2 | Observation provenance | Phase 1 / 2 | source package metadata, checksum and owner refs | A2 |
| D3 | Account Mirror read-only boundary | Phase 2 / 3 | package validation and projection only | A3 |
| D4 | Capability Registry | Phase 2 / 3 | observation enabled, command disabled | A4 |
| D5 | Command separated from observation | Phase 4 / 5 | no order action controls | A5 |
| D6 | Fail-closed blockers | Phase 2 / 5 | stale/missing/mismatch blockers | A6 |
| D7 | Capability Fabric extension rule | All phases | broker-neutral mirror contracts | A7 |

## AI Tracking Status

<!-- AI-PHASE-STATUS-BEGIN
reviewed_at: 2026-06-17
reviewer: Codex
overall_status: design_gate_ready
phases:
  - id: phase_0_proposal_convergence
    status: completed
    ai_progress: 100
    evidence: "proposal docs, UI design and acceptance scaffolded"
  - id: phase_1_owner_source_package_contract
    status: planned
    ai_progress: 0
    evidence: "pending ib_tws_account_source_package.v1 schema and fixtures"
  - id: phase_2_projection_and_fail_closed
    status: planned
    ai_progress: 0
    evidence: "pending Account Mirror IB projection and typed blockers"
  - id: phase_3_api_and_multi_account_surface
    status: planned
    ai_progress: 0
    evidence: "pending API readback for acct.ib.live.u3028269"
  - id: phase_4_ui_readback
    status: planned
    ai_progress: 0
    evidence: "pending browser evidence"
  - id: phase_5_closeout_and_regression_gates
    status: planned
    ai_progress: 0
    evidence: "pending focused gates"
AI-PHASE-STATUS-END -->

## Phase Status Board / Phase 状态表

| Phase | Goal | Current status | AI progress | Evidence / Current facts | Next action |
| --- | --- | --- | ---: | --- | --- |
| Phase 0 Proposal convergence | Freeze IB live read-only scope, boundaries and acceptance | `completed` | 100% | proposal docs created | start Phase 1 |
| Phase 1 Owner source package contract | Define IB source package schema and fixtures | `planned` | 0% | TWS implementation exists in `nautilus_strategies`; Account Console has no IB source package contract yet | add schema, positive fixture and negative fixtures |
| Phase 2 Projection and fail-closed behavior | Project IB package into Account Mirror or typed blockers | `planned` | 0% | Account Mirror already supports source bridges for other accounts | add IB source bridge and validator |
| Phase 3 API and multi-account surface | Expose `acct.ib.live.u3028269` through Account Workbench APIs | `planned` | 0% | API mode exists for current accounts | add API fixture/readback coverage |
| Phase 4 UI readback | Show funds, positions, orders, fills, source health and evidence in UI | `planned` | 0% | Account Workbench UI exists | add browser specs and evidence |
| Phase 5 Closeout and regression gates | Prove no direct TWS connection, no raw secret leakage and no command controls | `planned` | 0% | proposal-only acceptance scaffolded | run focused gates and closeout |

## Phase 1: Owner Source Package Contract

### Goal

Freeze the IB source package shape that Account Console may consume.

### Deliverables

1. `contracts/source_artifacts/account_sources/ib_tws_account_source_package.schema.json`
2. Positive fixture for `acct.ib.live.u3028269` with redacted owner refs.
3. Negative fixtures for missing funds, missing positions, stale source, checksum mismatch, raw secret leakage and forbidden broker action fields.

### Runtime / Command Freeze

No TWS runtime is executed by Account Console in this phase. Any real TWS read-only collection command must be owned by `nautilus_strategies` and recorded only as owner entrypoint ref plus output package checksum.

### Exit Conditions

1. Schema validates positive fixture.
2. Schema/validator rejects negative fixtures.
3. Package metadata includes `owner_repo_ref`, `owner_entrypoint_ref`, `owner_config_ref`, `source_collected_at`, `source_checksum`, `raw_secret_values_recorded=false`.
4. Owner package metadata includes same-slice `tws_connectivity_status=connected` only when the owner runtime has completed a read-only TWS / IB Gateway connection and account-summary readback for the target account.

## Phase 2: Projection and Fail-Closed Behavior

### Goal

Convert the owner-produced IB source package into canonical Account Mirror observations.

### Deliverables

1. IB source bridge in Account Console.
2. Projection coverage for funds, positions, orders, fills, source health and evidence refs.
3. Typed blockers for missing/stale/mismatched owner source packages.

### Exit Conditions

1. `acct.ib.live.u3028269` projection exists from valid package.
2. Invalid package produces blocked source health instead of fabricated account values.
3. Capability registry marks observation enabled and command disabled.
4. Funds projection preserves `net_liquidation`, `cash_balance`, `available_funds`, margins, excess liquidity, currency, source timestamp and source checksum without broker-native UI fields.
5. Missing or stale funds produce typed blocker instead of zero, blank or inferred values.
6. Multi-currency projection preserves every returned original-currency row and separates those rows from declared base-currency totals.
7. FX translation source, translation timestamp and comparison tolerance are present before base-currency totals can pass.
8. U3028269 position projection preserves every owner source position row with stable identity, exchange, asset class, currency, quantity, prices, market value, PnL and source checksum.
9. Missing/stale/mismatched positions produce typed blockers instead of empty or inferred UI rows.
10. TWS page sections are represented in Account Mirror source coverage metadata: balances, margin requirements, available-for-trading, real FX balances, portfolio, filters, update metadata and account type.
11. Segment columns and value semantics are preserved or explicitly blocked.
12. Any source/API section without a Web UI region materializes a typed missing-region blocker.

## Phase 3: API and Multi-Account Surface

### Goal

Expose IB as a peer account in the Account Workbench API without broker-specific API families.

### Deliverables

1. API readback for account summary.
2. API readback for positions, orders, fills and capabilities.
3. Evidence ref API fields for source package checksum and owner refs.

### Exit Conditions

1. Existing CTP/Nautilus Paper routes continue to pass.
2. IB route uses the same Account Mirror response shape.
3. No Account Console API endpoint accepts TWS host, port, client id, credentials or order action input.
4. IB funds API response matches Account Mirror projection and carries source/projection checksums.
5. IB multi-currency API response includes `currency_balances[]`, `base_currency`, `base_currency_totals`, FX/provenance metadata and validator tolerance.
6. IB positions API response includes stable position identities, exchange, asset class, currency, quantity, average price, market price, market value, PnL, source timestamp and checksum.
7. IB Account Workbench API includes section coverage metadata, segment columns, update timestamp, account type and filter state.
8. API exposes missing-region blocker payloads for required sections not yet implemented in Web UI.

## Phase 4: UI Readback

### Goal

Validate the IB account from the Account Console UI.

### Deliverables

1. `/accounts/acct.ib.live.u3028269` summary readback.
2. Funds, positions, orders and fills sections.
3. Source health strip and evidence drawer.
4. Desktop/tablet/mobile browser evidence.

### Exit Conditions

1. UI values match Account Mirror API.
2. Missing source package shows blocker state.
3. No submit/cancel/replace controls are visible.
4. Funds summary values match Account Mirror API and owner source package checksum; screenshot-only evidence cannot pass funds acceptance.
5. Multi-currency funds view shows original-currency rows and base-currency totals with labels, source refs and no hidden currency collapse.
6. Positions table values match Account Mirror API and owner source package checksum; screenshot-only evidence cannot pass U3028269 position acceptance.
7. Account Workbench UI shows every in-scope TWS page section or a typed blocker/out-of-scope marker.
8. Missing Web UI regions show stable blocker markers and cannot count as full section pass.

## Phase 5: Closeout and Regression Gates

### Goal

Close the proposal only after repo-local gates and same-slice evidence pass.

### Verification Commands

```bash
python scripts/check_proposal_docs.py --root . --proposal-id p018-ib-tws-readonly-account-console
python scripts/validate_account_capability_contracts.py
python scripts/validate_account_source_bridges.py
python scripts/validate_account_mirror_api.py
python scripts/validate_ib_tws_funds_readback.py
python scripts/validate_ib_tws_multi_currency_funds_readback.py
python scripts/validate_ib_tws_positions_readback.py
python scripts/validate_ib_tws_account_workbench_section_coverage.py
python scripts/validate_ib_tws_missing_ui_regions.py
npm run test -- --run
npm run build
```

Additional implementation-specific validators should be added during Phase 1-4 and listed here before closeout.

## Closeout Checklist

1. Owner source package exists for the same slice and is checksum-pinned.
2. Owner runtime connectivity evidence proves local TWS / IB Gateway connection and account-summary readback; probe-only or historical connection evidence is rejected.
3. Account Console records no raw endpoint, credential, auth code, client secret or broker secret.
4. Account Console does not import or call `ibapi`, Nautilus IB adapter, TWS socket, TWS REST/Web API or broker order APIs.
5. UI/API readback matches Account Mirror projection.
6. Multi-currency funds readback includes every returned currency row, base-currency totals and FX/provenance refs.
7. U3028269 position readback includes every returned position row, stable identity, exchange, asset class, currency, quantity, value, PnL and source refs.
8. TWS Account Workbench section coverage readback includes balances, margin, available-for-trading, real FX balances, portfolio filters, update metadata, account type and segment columns.
9. Missing Web UI regions, if any, are represented as typed blockers and the proposal status remains partial/blocked rather than full pass.
10. Browser evidence covers desktop/tablet/mobile.
11. Commands remain disabled and no readiness/can-trade claim is shown.
