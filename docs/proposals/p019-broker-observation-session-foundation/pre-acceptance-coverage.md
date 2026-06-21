# P019 Pre-Acceptance Coverage Closeout / 预验收覆盖收口

- Proposal ID: `p019-broker-observation-session-foundation`
- Status: historical_pre_acceptance_retained
- Date: 2026-06-20
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)
- Scope: preserve the historical pre-acceptance coverage table after ADR-0005 acceptance, while pointing current closeout to the accepted P019/ADR-0005 validators.

## 1. Closeout Rule

ADR-0005 is now accepted and P019 foundation closeout is accepted with residual runtime blockers. This historical closeout remains to prevent two drift modes:

1. treating pre-acceptance fixtures, blocked UI states or local TWS window titles as live broker/account truth;
2. treating open post-ADR evidence requirements as if they were not tracked.

Funds and positions acceptance must come from an authorized TWS API login / owner runtime source / Account Mirror projection chain. Screenshots may confirm local operator/window state only; they must not be used as funds truth, positions truth, account truth, execution report truth or trading-readiness evidence.

Synthetic ready-path fixtures may prove contract mapping from TWS API query artifacts, normalized report batches and durable-store reload checkpoints into source packages and Account Mirror projections, but they cannot close real U3028269 funds parity, positions parity, real order/fill callback parity, UI parity, P018 owner source-package acceptance or ADR-0005 direct observation acceptance.

Current real U3028269 TWS API evidence proves funds/positions collection and UI parity are ready, and it also proves a read-only `reqExecutions` / `ExecutionFilter` query succeeded with `execution_report_rows=0`, `complete_history_claimed=false` and `order_action_sent=false`. That empty executions result is typed evidence, not report parity: real order/fill callback parity, execution report table parity and durable-store reload parity remain blocked until authorized same-slice execution rows exist. The current real durable reload artifact is therefore `partial` / `blocked`, references `durable-store-reload.json`, and must not be treated as a complete report-row reload.

ADR-0005 is now accepted. The post-ADR observation evidence for real U3028269 funds/positions is produced from authorized TWS API / Account Mirror sources and passes UI parity. Real order/fill report-row parity remains blocked by zero same-slice executions.

## 2. Acceptance Coverage Matrix

| Acceptance | Current coverage status | Pre-acceptance evidence | Required post-ADR evidence |
| --- | --- | --- | --- |
| A1 | pre-acceptance partial | `validate_p019_profile_security_provenance.py`, `validate_p019_api_boundary.py`, blocked profile fixture | accepted read-only observation profile plus conflict-policy pass from owner/runtime source |
| A2 | pre-acceptance partial | owner config/secret refs only, `raw_secret_values_recorded=false`, profile/security validator | owner-owned config/secret resolution evidence with raw values kept outside this worktree |
| A3 | pre-acceptance partial | session conflict schema/fixture plus ADR-0005 contract validator | real runtime conflict evaluation for username/client id/session slot/Nautilus active trading session |
| A4 | pre-acceptance partial | report mapping matrix maps IB `orderStatus` to `OrderStatusReport` | callback mapper tests against authorized same-slice broker observation data |
| A5 | pre-acceptance partial | report mapping matrix maps IB `execDetails` and `commissionReport` to `FillReport`; real `output/account_capability/ib-live-u3028269/tws-api/executions.json` records read-only `reqExecutions` success with `execution_report_rows=0`, `complete_history_claimed=false` and no order action | callback mapper tests with non-empty fill/commission rows from authorized same-slice source evidence |
| A6 | pre-acceptance partial | raw payload policy stores ref/checksum/redacted excerpt only; browser parsing forbidden | production observation artifacts proving raw payload remains provenance-only |
| A7 | pre-acceptance partial | U3028269 exposed only through Account Mirror blocked projection; direct broker routes absent | Account Mirror projection populated from accepted TWS API / owner runtime source without bypass route |
| A8 | pre-acceptance partial | freshness sequence checkpoint fixture rejects realtime/complete-history claims from gap state | live or replayed freshness cursors proving sequence continuity, lag and snapshot boundaries |
| A9 | pre-acceptance partial | API command routes absent; U3028269 command disabled; synthetic positive `OrderStatusReport` / `FillReport` rows render without order action controls | real owner/runtime report-row UI/API evidence still showing no order action controls or endpoints |
| A10 | pre-acceptance partial | cross-broker matrix keeps IB TWS, CTP, stock broker, CQG and TT on shared contracts | accepted adapter implementations must continue using the shared broker-neutral contract family |
| A11 | pre-acceptance partial | durable store complete reload fixture rejects live-memory reload dependency; real `output/account_capability/ib-live-u3028269/durable-store-reload.json` reloads persisted source/executions artifacts with no live memory and remains `partial` / `blocked` while real execution rows are absent | durable store restart/reload test from authorized non-empty observation report records |
| A12 | pre-acceptance partial | durable store gap blocker fixture and memory-only negative fixture | real replay gap/checksum/missing startup report blockers from runtime/store evidence |
| A13 | pre-acceptance partial | Playwright blocked route renders `tws-execution-reports-table` and typed blocker row; synthetic ready route renders two normalized report rows, deterministic sequence, provenance refs and store reload checkpoint; real UI evidence records `execution_report_rows=0` and keeps report table/persistence parity blocked | real owner/runtime normalized report-row table with deterministic identity, ordering, provenance and durable-store reload parity from non-empty report rows |
| A14 | pre-acceptance partial | Playwright blocked route renders `tws-multi-currency-funds-table`, funds blocker and FX/base-currency provenance surfaces | positive per-currency funds evidence obtained through authorized TWS API / owner runtime source, with base-currency rollup provenance; screenshots cannot satisfy funds parity |

## 3. Pre-Code Gate Coverage Matrix

| Gate | Current status | Evidence / blocker | Required before implementation closeout |
| --- | --- | --- | --- |
| PRE-G01 | accepted | ADR-0005 is accepted; `adr0005_not_accepted` is retired as an architecture blocker | keep residual runtime blockers typed |
| PRE-G02 | accepted | owner map records accepted guarded `account-console-broker-observation-session` with no broker truth, command or direct session authority | preserve owner-map guard |
| PRE-G03 | pre-acceptance partial | `evidence-lane-manifest.json` and validator keep P018 owner-source-package evidence separate from P019 governed observation evidence | explicit artifact mapping before any cross-lane evidence reuse |
| PRE-G04 | pre-acceptance partial | profile/security/provenance validator and contract negatives reject raw secrets | runtime owner evidence must continue storing only refs/checksums/redacted shapes |
| PRE-G05 | pre-acceptance partial | normalized report batch and report mapping matrix are contract-checked | live callback mapper tests for `OrderStatusReport` and `FillReport` |
| PRE-G06 | pre-acceptance partial | durable store complete reload and gap blocker fixtures are contract-checked; current real persisted-artifact reload is `partial` / `blocked` on zero execution rows without live memory | restart/reload/gap tests against real durable observation store records with non-empty report rows |
| PRE-G07 | pre-acceptance partial | API boundary validator proves U3028269 is mirror-only and direct broker/TWS routes are absent | accepted observation source populates Account Mirror without bypass routes |
| PRE-G08 | pre-acceptance partial | blocked UI parity evidence records funds, positions, orders/fills, execution reports and persistence parity as `blocked`; current real UI parity passes funds/positions but records `execution_report_rows=0`, so orders/fills, execution reports and persistence parity remain blocked | same-slice TWS API / owner runtime source report/store parity evidence after ADR acceptance and owner source availability; screenshot evidence is forbidden for funds and positions truth |
| PRE-G09 | pre-acceptance partial | API boundary plus blocked and synthetic positive report-row browser projections reject command/action drift | accepted real report-row UI still has no submit/cancel/replace/modify controls |

## 4. Required Verification Commands

| Command | Pass signal |
| --- | --- |
| `python scripts/validate_p019_preacceptance_coverage.py` | `P019_PREACCEPTANCE_COVERAGE_OK: acceptance=14 gates=9 status=historical_retained` |
| `python scripts/probe_p019_tws_api_readiness.py` then `python scripts/validate_p019_tws_api_readiness_probe.py` | `P019_TWS_API_READINESS_PROBE_OK: status=ready account_query_sent=false` or a typed blocked signal before collection |
| `python scripts/validate_p019_broker_observation_foundation.py` | `P019_BROKER_OBSERVATION_FOUNDATION_OK: status=accepted residual_blockers=real_parity` |

## 5. Non-Completion Assertions

1. Historical `pre-acceptance partial` rows remain retained for audit context only; current closeout status is accepted with residual runtime blockers.
2. `PRE-G01` and `PRE-G02` are accepted by ADR-0005 and owner-map alignment.
3. Local TWS window title evidence is process/window confirmation only; it must not satisfy broker truth, account truth, funds parity, positions parity, order truth, execution report parity or trading readiness.
4. No P019 evidence in this worktree may record raw secrets, raw broker endpoints, auth codes, passwords or account secret values.
5. Funds and positions closeout requires TWS API / owner runtime source data; screenshots are never acceptable evidence for those values.
6. A local TWS window title is insufficient for funds/positions queries; the readiness probe must pass or carry typed blocker `tws_api_readiness_missing` before any real funds/positions collection work proceeds.
7. Synthetic ready-path fixtures are contract guards only; they must remain separated from real funds/positions parity, real order/fill callback parity, durable owner/runtime reload parity and owner source-package evidence.
8. Real `reqExecutions` success with zero rows must remain a typed empty-state blocker, not a real report parity pass.
9. Durable reload from persisted artifacts with zero report rows must remain `partial` / `blocked`, not complete.
