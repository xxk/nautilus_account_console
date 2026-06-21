# Account Console Owner Map / 账户控制台 Owner Map

- Date: 2026-06-13
- Status: active authority map
- Scope: owner boundaries for `nautilus_account_console` UI contracts, read models, fixtures, backend query API, Rust hot path primitives and downstream acceptance
- Anchors:
  - [AGENTS.md](../../AGENTS.md)
  - [ADR-0002 business workbench navigation](../adr/0002-adopt-business-workbench-first-account-console-navigation.md)
  - [ADR-0003 contract-first UI slice development](../adr/0003-adopt-contract-first-ui-slice-development.md)
  - [ADR-0005 independent broker observation sessions](../adr/0005-account-console-independent-broker-observation-sessions.md)
  - [Contract-first UI slice development topic](../topics/contract-first-ui-slice-development.md)

## 1. Purpose / 目的

This owner map prevents a second implementation, second truth source, second runtime, second ledger or second UI authority.

Account Console is a read-only observation console. It may define display contracts, fixtures, reducers, read-model projections, browser panels and acceptance evidence. It must not become the writer for runtime truth, broker truth, account truth, admission truth, approval truth, capital truth or trading readiness.

## 2. Owner Classes / Owner 分类

| Owner class | Meaning | May write | Must not write |
| --- | --- | --- | --- |
| Producer owner | Creates canonical source artifacts, normalized events or ledgers | own canonical artifacts inside its authority boundary | Account Console UI projection state |
| Verifier owner | Reconciles producer artifacts and emits typed evidence/blockers | verifier outputs, blocker evidence, checksum checks | producer payloads or browser-only corrections |
| Projection owner | Computes read models from typed inputs | derived read models, query caches, fixture projections | source events, accepted lifecycle/allocation ledgers |
| UI/report owner | Renders read models and evidence refs | browser components, selectors, screenshot evidence | account/order/fill/position/settlement/equity truth |
| Approval owner | Accepts admission, PM approval, capital or tradability decisions | approval artifacts in the external owner system | any Account Console local path |

The `owner` field displayed in UI rows means operational responsibility for a blocker or account. It is not a code owner, truth owner or write authority.

## 3. Canonical Owner Matrix / Canonical Owner 矩阵

| Layer / Artifact | Canonical owner | Local path | Authority | Account Console allowed role | Forbidden second implementation |
| --- | --- | --- | --- | --- | --- |
| Wire contracts | `account-console-contracts` | `contracts/*.schema.json` | shared schema files | define schemas and validate payload shape | invent alternate schema family in frontend/backend |
| UI panel contracts | `account-console-contracts` | `contracts/ui/panels/*.contract.json` | panel read model contract | constrain UI fields and fixture shape | render fields not declared by panel contract |
| UI fixtures | `account-console-contracts` + proposal owner | `contracts/ui/fixtures/**` | deterministic projection examples | support UI acceptance and blocked states | treat fixture rows as account or runtime truth |
| Rust hot path primitives | `account-console-hotpath` | `hotpath-rs/` | Rust ingest, cursor/dedupe, batching, durable ledger primitives | own high-frequency primitives in this repo | reimplement high-frequency event path in Python or browser |
| Python query/control API | `account-console-backend` | `backend/` | FastAPI read/query integration | expose projections and query fixtures | append accepted ledger, broker, runtime, admission or capital truth |
| Browser projection | `account-console-frontend` | `frontend/` | TypeScript UI rendering | render read models, copy refs, capture screenshots | compute account truth or infer readiness in browser |
| Browser acceptance tests | `account-console-browser-acceptance-tests` | `frontend/tests/e2e/` | Playwright selector and route acceptance | verify canonical UI projections and produce browser evidence | create routes, fixtures, read models, runtime truth or feature-specific second UI implementations |
| UI design/acceptance | `account-console-ui-architecture` | `docs/design/`, `docs/acceptance/` | design and gate documents | define route, visual and browser acceptance | use docs alone as runtime/account truth |
| ADR/proposal governance | `architecture` + proposal owner | `docs/adr/`, `docs/topics/`, `docs/proposals/` | stable decision and implementation lane | choose canonical lane and record blockers | open parallel proposal that writes the same truth |
| External strategy/runtime artifacts | external strategy/runtime owner, e.g. `nautilus_strategies` / `strategies.vnpy_portfolio` | external `source_ref` only | normalized events, ledgers, evidence packages | display refs/checksums and typed blockers | rewrite or regenerate external artifact truth locally |
| Admission/approval/capital decisions | external approval/capital owner | no local writer | formal approval/capital artifacts outside this repo | display request/projection or blocker only | create local approval, admission or capital allocator |
| Broker/live state | broker/runtime owner | no local writer | broker/runtime APIs/artifacts outside this repo | display normalized broker/probe projections only | call broker action or certify tradability |
| Broker observation session capability | `account-console-broker-observation-session` accepted by ADR-0005 | `contracts/broker_observation/**`, `docs/proposals/p019-broker-observation-session-foundation/**`, `output/account_capability/ib-live-u3028269/**` evidence refs | governed read-only observation capability, not broker/runtime truth | define contracts, validators, read-only source packages, durable observation evidence and Account Mirror projections with command disabled | own broker/runtime/account/order truth, store raw secrets, expose command authority, or claim complete execution history from partial evidence |
| P024 paper command controls | `account-console-command-contracts` + `account-console-frontend` + external `owner://nautilus_ctp_adapter` runtime owner | `docs/proposals/p024-account-console-paper-command-controls/**`, `docs/acceptance/p024-account-console-paper-command-controls/**`, `docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/**` | guarded paper intent API, browser command-control projection, owner-runtime handoff/readiness refs, residual blocker audit, owner-runtime execution approval packet, runtime approval packet UI projection, owner-runtime execution handoff bundle, runtime handoff bundle UI projection and runtime execution gap audit | accept paper intent/control/display/handoff/readiness/approval-packet/UI-projection/handoff-bundle/browser-handoff-bundle/gap-audit gates; render owner refs/checksums/blockers; preserve external approval blocker before owner-runtime execution | call broker/runtime directly, write owner repo without approval, claim browser-triggered broker order, store raw secrets/endpoints, make Account Mirror a command writer |

## 4. Tracer Edge Authority / Tracer 边权限

Every source-to-UI edge must carry:

| Required edge field | Purpose |
| --- | --- |
| canonical identity | `account_id`, `client_order_id`, `event_id`, `run_id`, `session_id`, `trading_day` or typed equivalent |
| `source_ref` or `artifact_ref` | formal pointer to producer/projection evidence |
| `checksum` | integrity evidence when the contract requires it |
| `schema_version` | contract version for payload interpretation |
| producer/projection owner | the authority that created or reduced the value |
| rejection rule | what shortcut must fail |

Screenshots prove rendering only. They never prove account, runtime, broker, admission, approval or capital truth.

## 5. Anti-Second-Implementation Rules / 防第二实现规则

| Rule | Must pass | Must fail if |
| --- | --- | --- |
| ASI-01 Canonical owner declared | every proposal/change names producer, verifier, projection and UI owner | a feature lands with only a component owner and no truth owner boundary |
| ASI-02 No alternate truth writer | new code reads contracts/projections or records typed blockers | new code writes runtime/account/broker/admission/capital truth |
| ASI-03 Rust hot path remains canonical | high-frequency ingest/cursor/dedupe/batching stays in Rust unless an ADR changes owner | Python/browser becomes the default per-event hot path |
| ASI-04 Contract-first UI | UI fields come from `contracts/ui/panels/*` and fixtures/read models | frontend invents fields or parses raw reports as truth |
| ASI-05 External owner blockers stay blockers | missing external artifacts produce typed blocked/partial/stale UI | Account Console regenerates external strategy/runtime evidence |
| ASI-06 Request/projection boundary | account-management controls require typed request contracts | UI directly mutates accepted lifecycle/allocation ledgers |
| ASI-07 Route owner is single | primary workbench and panel owner are declared before code | a second route or page implements the same business capability |
| ASI-08 Acceptance owner is separate from screenshot | tests/contracts/checksums validate data, screenshots validate display | screenshot alone accepts a source-to-UI tracer |

## 6. P001 Owner Assignment / P001 Owner 分配

| P001 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| UI slice proposal | `account-console-ui` | `docs/proposals/p001-daily-closeout-account-health-panel/` |
| Panel contract | `account-console-contracts` | `contracts/ui/panels/account_health_panel.contract.json` |
| Fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/daily_closeout/account_health_*.json` |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx` |
| Selector/browser acceptance | `account-console-frontend` + `account-console-ui` | `frontend/tests/e2e/account-health-panel.spec.ts` |
| Backend runtime/query owner | not touched by P001 fixture slice | typed blocker if live read model endpoint is required |
| External source evidence | external strategy/runtime owner | external refs remain `source_ref` only |

P001 is accepted as a fixture-backed UI projection slice only. It does not accept closeout truth, account truth, settlement truth, PM approval, admission or capital state.

## 6.1 P077 Paper Slice Fixture Assignment / P077 Paper Slice Fixture Owner 分配

| P077 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Source lifecycle/fill/reconcile evidence | `nautilus_ctp_adapter` | external source ref only: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T112841Z/p077_t6_e86_filled_close_yesterday_reconciled.json` |
| Governance handoff and no-active-authorization evidence | `nautilus_strategies` | external source ref only: `docs/changes/20260614__paper__p077-safer-retry-lane/evidence/20260614T113441Z_e87_post_fill_owner_handoff_audit_no_send.json` |
| Panel contract | `account-console-contracts` | `contracts/ui/panels/p077_paper_slice_panel.contract.json` |
| Fixture projection | `account-console-contracts` | `contracts/ui/fixtures/p077_paper_slice/e87_close_yesterday_filled.json` |
| UI slice design gate | `account-console-ui` | `docs/proposals/p009-p077-paper-slice-evidence-panel/` |
| Browser rendering | `account-console-frontend` | P009 E93 implementation/browser evidence renders the fixture read-only under Account Workbench |

The P077 fixture is accepted as a read-only projection fixture only. It does not accept order lifecycle truth, fill truth, position truth, account truth, broker truth, Paper readiness, Live readiness, admission, capital or production state.

P009 E93 implementation/browser evidence may render this fixture as a read-only Account Workbench panel only. It must not add a top-level `/orders/p077-paper-slice` route, expose order action controls, or create runtime, ledger, admission, capital, broker or readiness truth.

## 6.2 P004 Account Workbench Summary Assignment / P004 Account Workbench Summary Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| UI slice proposal | `account-console-ui` | `docs/proposals/p004-account-workbench-summary-panel/` |
| Account Summary panel contract | `account-console-contracts` | `contracts/ui/panels/account_summary_panel.contract.json` |
| Account Summary fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_summary_*.json` |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx` |
| Selector/browser acceptance | `account-console-frontend` + `account-console-ui` | `frontend/tests/e2e/account-summary-panel.spec.ts`; `docs/acceptance/2026-06-14-p004-phase2-summary-ui-browser-evidence.json` |
| Backend runtime/query owner | not touched by P004 Phase 2 fixture slice | typed blocker if live read model endpoint is required |
| External source evidence | external strategy/runtime owner | external refs remain `source_ref` only |

P004 Phase 2 is accepted as a read-only Account Summary UI projection slice only. It does not accept account truth, order truth, position truth, settlement truth, equity truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.3 P004 Orders And Order Detail Assignment / P004 Orders Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Orders panel contract | `account-console-contracts` | `contracts/ui/panels/account_orders_panel.contract.json` |
| Order detail panel contract | `account-console-contracts` | `contracts/ui/panels/account_order_detail_panel.contract.json` |
| Orders and lifecycle fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_orders_*.json`; `contracts/ui/fixtures/account_workbench/account_order_detail_*.json` |
| External lifecycle/report provenance | external strategy/runtime owner, currently `nautilus_ctp_adapter` for E100 projection refs | external source refs only |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx`; `frontend/tests/e2e/account-orders-panel.spec.ts`; `docs/acceptance/2026-06-14-p004-phase3-orders-ui-browser-evidence.json` |

P004 Phase 3 is accepted as a read-only orders/order-detail UI projection slice only. It does not accept order truth, account truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.4 P004 Positions Contract And Fixture Assignment / P004 Positions Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Positions panel contract | `account-console-contracts` | `contracts/ui/panels/account_positions_panel.contract.json` |
| Positions fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_positions_*.json` |
| External position lifecycle context | external strategy/runtime owner, currently `nautilus_ctp_adapter` for E100 projection refs | external source refs only |
| Carryover and settlement refs | external settlement/carryover owner | typed blocked or partial fixture when refs are missing |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx`; `frontend/tests/e2e/account-positions-panel.spec.ts`; `docs/acceptance/2026-06-14-p004-phase4-positions-ui-browser-evidence.json` |

P004 Phase 4 is accepted as a read-only positions UI projection slice only. It does not accept position truth, account truth, order truth, ledger truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.5 P004 Settlement And Equity Contract Assignment / P004 Settlement And Equity Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Settlement panel contract | `account-console-contracts` | `contracts/ui/panels/account_settlement_panel.contract.json` |
| Equity panel contract | `account-console-contracts` | `contracts/ui/panels/account_equity_panel.contract.json` |
| Settlement fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_settlement_*.json` |
| Equity fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_equity_*.json` |
| External settlement/carryover/equity ledger refs | external settlement/ledger owner | typed blocked or partial fixture when refs are missing |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx`; `frontend/tests/e2e/account-settlement-equity-panel.spec.ts`; `docs/acceptance/2026-06-14-p004-phase5-settlement-equity-ui-browser-evidence.json` |

P004 Phase 5 is accepted as a read-only settlement/equity UI projection slice only. It does not accept settlement truth, equity truth, account truth, position truth, order truth, ledger truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.6 P004 Reconcile And Incidents Assignment / P004 Reconcile And Incidents Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Reconcile panel contract | `account-console-contracts` | `contracts/ui/panels/account_reconcile_panel.contract.json` |
| Incidents panel contract | `account-console-contracts` | `contracts/ui/panels/account_incidents_panel.contract.json` |
| Reconcile fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_reconcile_*.json` |
| Incidents fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_incidents_*.json` |
| External reconcile, incident and repair refs | external reconcile/incident owner | typed blocked or partial fixture when refs are missing |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx`, `frontend/src/types.ts`, `docs/acceptance/2026-06-14-p004-phase6-reconcile-incidents-ui-browser-evidence.json` |

P004 Phase 6 is accepted as a read-only reconcile/incidents UI projection slice only. It does not accept reconcile truth, incident truth, account truth, order truth, ledger truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.7 P004 Evidence Contract Assignment / P004 Evidence Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Evidence panel contract | `account-console-contracts` | `contracts/ui/panels/account_evidence_panel.contract.json` |
| Evidence fixture projections | `account-console-contracts` + `account-console-ui` | `contracts/ui/fixtures/account_workbench/account_evidence_*.json` |
| Schema/checksum/source refs | external evidence/source owner | typed blocked or partial fixture when refs are missing |
| Browser rendering | `account-console-frontend` | `frontend/src/App.tsx`, `frontend/src/types.ts`, `docs/acceptance/2026-06-15-p004-phase7-evidence-ui-browser-evidence.json` |

P004 Phase 7 is accepted as a read-only evidence UI projection slice only. It does not accept evidence truth, account truth, order truth, ledger truth, broker truth, Paper readiness, Live readiness, admission, capital, production state or full Account Console UI completion.

## 6.8 P004 Account Workbench Closeout Assignment / P004 Account Workbench 收口 Owner Assignment

| P004 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| Scoped Account Workbench closeout | `account-console-ui` + `account-console-frontend` | `docs/acceptance/2026-06-15-p004-phase8-account-workbench-closeout.json` |
| Closeout browser evidence | `account-console-frontend` | `docs/acceptance/browser-evidence/p004-phase8-account-workbench-closeout/` |
| Residual scope statement | `account-console-ui` | P004 closeout explicitly excludes ADR0044/ADR0045 loop completion, P077/P078 completion, sibling owner completion and full Account Console UI completion |

P004 Phase 8 closes the P004 Account Workbench scoped phases only. It does not accept Account Console runtime truth, account truth, order truth, ledger truth, broker truth, Paper readiness, Live readiness, admission, capital, production state, full Account Console UI completion or loop completion.

## 6.9 P019 Broker Observation Session Foundation Accepted Assignment / P019 Broker Observation Accepted Owner Assignment

P019 and ADR-0005 are accepted for the broker-observation foundation. `account-console-broker-observation-session` is an accepted guarded capability owner for read-only observation contracts, source-package projections, durable observation evidence and Account Mirror inputs. It is not a broker runtime owner, account/order truth owner, command owner, approval owner, capital owner or trading-readiness owner.

| P019 responsibility | Owner | Path / evidence |
| --- | --- | --- |
| ADR and proposal governance | `architecture` + `account-console-broker-observation-session` | `docs/adr/0005-account-console-independent-broker-observation-sessions.md`; `docs/proposals/p019-broker-observation-session-foundation/`; `docs/acceptance/2026-06-20-adr0005-broker-observation-session-acceptance.json` |
| Broker observation profile and report contracts | `account-console-contracts` + P019 owner | `contracts/broker_observation/**`; `scripts/validate_adr0005_broker_observation_contracts.py` |
| Durable observation store contract fixtures and real reload evidence | `account-console-contracts` + P019 owner | `contracts/broker_observation/fixtures/ib_tws_store_complete_reload.json`; `contracts/broker_observation/fixtures/ib_tws_store_gap_blocker.json`; `output/account_capability/ib-live-u3028269/durable-store-reload.json` |
| Account Mirror U3028269 projection | `account-console-backend` + `account-console-frontend` | `acct.ib.live.u3028269` projects read-only TWS API funds/positions when source package is ready, keeps command disabled, `raw_secret_values_recorded=false`, no broker truth, no order action and typed residual blockers for zero execution rows |
| Local TWS window confirmation evidence | operator/local desktop evidence owner | `output/debug/p019-tws-local-window-confirmation/tws-local-window-confirmation-blocker.json` records process/window title only; minimized/offscreen screenshot remains a blocker and not visual truth |
| Broker/runtime/account/order source truth | external broker/runtime owner | outside this repo; Account Console may reference owner evidence only after ADR-0005 acceptance |

P019 accepted foundation work authorizes only governed read-only observation after readiness, conflict, secret and no-command gates pass. It does not authorize Account Console to own broker live state, own account/order/fill truth, store raw secrets, infer trading readiness or expose submit/cancel/replace/modify controls. Missing owner-source or runtime evidence must remain a typed blocker such as `real_order_fill_callbacks_not_available`, not a local substitute truth writer.

## 7. Successor Proposal Owner Block / 后续 Proposal 必填 Owner Block

Each UI/backend/hotpath proposal must include:

```text
Owner Boundary:
  proposal_or_change_id:
  producer_owner:
  verifier_owner:
  projection_owner:
  ui_or_report_owner:
  approval_owner: none | external owner name
  canonical_contracts:
  canonical_source_refs:
  write_authority:
    allowed:
    forbidden:
  second_implementation_rejected:
  blocker_owner_if_missing_source:
```

If any owner is unknown, the proposal must stop at a typed blocker instead of implementing a substitute source.

