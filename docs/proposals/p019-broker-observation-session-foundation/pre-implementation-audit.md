# P019 Pre-Implementation Audit / 开工前文档审核

- Proposal ID: `p019-broker-observation-session-foundation`
- Status: active audit
- Date: 2026-06-20
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)
- Scope: detect document conflicts, owner drift and acceptance gaps before ADR-0005 implementation work starts.

## 1. Audit Verdict / 审核结论

P019 is directionally valid, but implementation must not start as a direct TWS connection until the required governance gates below are resolved or carried as typed blockers.

The main conflict is intentional but not yet closed: P018 currently forbids Account Console direct TWS / IB Gateway session ownership, while ADR-0005/P019 proposes allowing governed read-only broker observation sessions if ADR-0005 is accepted and the conflict policy passes. That is an architecture boundary change, not a small implementation detail.

## 2. Conflict And Drift Matrix / 冲突与漂移矩阵

| ID | Source | Current statement | P019/ADR-0005 direction | Risk | Required action before closeout |
| --- | --- | --- | --- | --- | --- |
| AUD-01 | ADR-0005 | `decision_status=proposed`, Section 4 still pending decision | P019 assumes candidate C: Account Console may own governed read-only observation sessions | Implementation may treat an unaccepted ADR as authority | Accept ADR-0005 or keep implementation as contract/prototype with typed blocker `adr0005_not_accepted` |
| AUD-02 | Owner map | Account Console is read-only projection console; Broker/live state has `no local writer` and display-only role | P019 adds proposed `account-console-broker-observation-session` owner | Second broker runtime/truth writer can appear silently | Update owner map only after ADR-0005 acceptance; until then P019 must record this as pending alignment |
| AUD-03 | P018 | Account Console must not own TWS / IB Gateway session, import `ibapi`, or collect live account data directly | P019 says TWS can be today's first direct read-only observation slice after ADR acceptance | P018 and P019 could both claim IB TWS ownership | Keep P018 as owner-source-package lane; P019 as ADR-0005 governed observation-session lane. Evidence must not be reused across lanes without explicit mapping |
| AUD-04 | ADR-0004 / Account Mirror | Account Mirror is read-only projection and command stays separate | P019 feeds Account Mirror from broker observation session | Backend observation might bypass Account Mirror and become UI truth | Implementation must expose UI through Account Mirror/API projection, not broker adapter endpoints |
| AUD-05 | Sensitive material policy | Worktree must not own passwords, auth codes, raw fronts, endpoints, broker secrets or account secrets | P019 needs broker profile and TWS source refs | Credentials or connection details may leak into docs/tests/evidence | Profiles and evidence must store refs/checksums/redacted shape only and `raw_secret_values_recorded=false` |
| AUD-06 | Order report requirement | Existing P018 execution reports are owner-package execution events | ADR-0005 requires Nautilus-compatible `OrderStatusReport` / `FillReport` for all observed callbacks | Broker-specific report schema or raw payload may become canonical | Add contract tests for normalized reports before UI reads order/fill rows |
| AUD-07 | Durable observation store | ADR-0005 requires local durable store for reports/snapshots/session state | P019 currently has acceptance but no implementation contract | Startup-only report callbacks can be lost after session | Add store schema/reload/gap tests before claiming post-session review support |
| AUD-08 | Account Workbench UI | Current baseline route renders demo fixture for `acct.ib.live.u3028269` | P019 requires U3028269 TWS funds, positions and Execution Reports tables | Browser may pass from fixture-only or wrong account | UI closeout must prove route identity, source/projection parity and no demo fallback |
| AUD-09 | Multi-currency funds | Existing UI can show metric-strip summaries | P019 requires per-currency funds table plus base-currency rollup provenance | Currencies can be collapsed into misleading totals | Browser tests must target `tws-multi-currency-funds-table`, row counts and FX/provenance |
| AUD-10 | Execution Reports UI | User requires Execution Reports as a table | P019 now defines table columns, parity, persistence and blockers | Rows can be hidden in cards/order status or lost after reload | Browser tests must target `tws-execution-reports-table` and durable-store parity |
| AUD-11 | Command drift | Users also discuss future order capability | This ADR focuses on observation; command belongs in a separate ADR/proposal | Observation session could grow submit/cancel/replace controls | Add negative API/UI tests and keep order-command ADR separate |
| AUD-12 | Cross-broker extension | User wants future CTP, stock, CQG, TT extension | Today only TWS development | First slice could hard-code IB semantics | TWS contracts must use broker-neutral profile/mapper/store shape and reject IB-only UI truth |

## 3. Required Pre-Code Gates / 开发前 Gate

| Gate | Requirement | Evidence to unblock | Current status |
| --- | --- | --- | --- |
| PRE-G01 ADR decision gate | ADR-0005 accepted or implementation explicitly marked as pre-acceptance prototype/blocker | ADR-0005 Section 4 decision or typed blocker carried in P019 | open |
| PRE-G02 Owner-map alignment gate | owner map describes the accepted observation-session owner and keeps broker truth/execution forbidden | owner map update after ADR acceptance | open |
| PRE-G03 P018/P019 lane separation | P018 source-package lane and P019 direct observation lane cannot both claim the same evidence without mapping | P019 audit entry plus future evidence manifest lane id | documented here, open for implementation |
| PRE-G04 Secret boundary gate | no raw broker secrets, endpoints, auth codes, client id secrets or account secrets in docs/tests/artifacts | redaction/schema scan and `raw_secret_values_recorded=false` fixtures | pre-acceptance fixture covered by `validate_adr0005_broker_observation_contracts.py`; implementation scan still required |
| PRE-G05 Report contract gate | `OrderStatusReport` and `FillReport` compatible schemas/fixtures exist before UI/report rendering | schema + mapper tests | pre-acceptance fixture covered by `validate_adr0005_broker_observation_contracts.py`; live mapper tests still required |
| PRE-G06 Durable store gate | normalized reports, funds snapshots, positions snapshots, session health and cursors reload after restart | persistence/reload tests and gap negative tests | pre-acceptance gap blocker fixture covered by `validate_adr0005_broker_observation_contracts.py`; real reload test still required |
| PRE-G07 Account Mirror gate | UI/API reads Account Mirror projection, not broker adapter payload | API route/projection tests and frontend negative scan | pre-acceptance partial via `validate_p019_api_boundary.py`; accepted source population still required |
| PRE-G08 Browser parity gate | Web UI route for `acct.ib.live.u3028269` compares rendered funds, positions and execution reports against same-slice TWS/API/source package | Playwright evidence plus machine-readable parity artifact | pre-acceptance partial as blocked UI parity only; funds and positions truth still require authorized TWS API / owner runtime source evidence, never screenshots |
| PRE-G09 Command-negative gate | no submit/cancel/replace/modify/order action controls or endpoints in observation slice | backend route scan/test and Playwright negative assertion | pre-acceptance partial via API boundary and blocked projection tests; positive report-row negative still required |

## 4. Current Baseline Facts / 当前事实

1. ADR-0005 is still `proposed`; it does not yet authorize direct implementation as accepted architecture.
2. P019 is present and scoped as the successor proposal for ADR-0005.
3. P018 remains a valid design-gate proposal for IB source-package readback and explicitly forbids direct TWS session ownership by Account Console.
4. The current Account Workbench route for `/accounts/acct.ib.live.u3028269` renders the U3028269 blocked projection through Account Mirror, not the old demo fallback.
5. The current blocked projection proves surface routing and typed blockers only; it does not prove TWS source parity, multi-currency funds values, positions values, Execution Reports row parity or durable-store replay from real source data.
6. No raw broker secrets or credentials are required or recorded by this audit.
7. Pre-acceptance contract fixtures and `python scripts/validate_adr0005_broker_observation_contracts.py` now cover the blocked TWS profile shape, normalized order/fill report shape, durable store gap blocker, and negative cases for raw secrets, command actions, raw payload truth and store truth claims.
8. Funds and positions closeout must come from authorized TWS API / owner runtime source data projected through Account Mirror. Screenshots or window titles can confirm local TWS operator/window state only and cannot prove funds, positions, account truth, execution report truth or trading readiness.

## 5. Implementation Start Rule / 开工规则

Implementation may begin only in one of these modes:

1. **Accepted ADR mode**: ADR-0005 is accepted, owner map alignment is updated, and P019 gates become implementation requirements.
2. **Pre-acceptance contract mode**: code is limited to schemas, fixtures, typed blockers, negative tests and UI blocked states; any direct broker connection is blocked by `adr0005_not_accepted`.
3. **P018 compatibility mode**: implementation stays on the owner-produced source-package lane and does not introduce Account Console-owned TWS connectivity.

Direct TWS observation from Account Console without one of the modes above is a drift failure.

## 6. Acceptance Impact / 对验收的影响

P019 closeout must include this audit in its evidence package. A green docs gate alone is not enough. Closeout must prove:

1. the accepted owner boundary matches ADR-0005 and the owner map;
2. P018 and P019 evidence lanes are not mixed;
3. TWS U3028269 UI readback is compared against same-slice TWS/API/source data;
4. funds are table-based and multi-currency capable;
5. Execution Reports are table-based, normalized, provenanced and reloadable from durable store;
6. command surfaces remain absent;
7. missing source, stale source, replay gaps and checksum mismatches produce typed blockers.
