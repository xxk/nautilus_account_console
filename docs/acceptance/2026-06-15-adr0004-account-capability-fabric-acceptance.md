# ADR-0004 Account Capability Fabric Acceptance / ADR-0004 账户能力织构验收

- Date: 2026-06-15
- Status: active ADR acceptance baseline
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Architecture design anchor: [Account Capability Fabric architecture design](../design/account-capability-fabric-architecture-design.md)
- Topic anchor: [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
- Scope: required acceptance gates for Account Capability Fabric, Account Mirror readback, capability registry and future command capability
- Discussion alias: `T0004` / `T004` in planning discussion means this ADR-0004 scheme acceptance unless a separate canonical topic is created

## 1. Acceptance Boundary / 验收边界

This document accepts architecture conformance only. It validates implementation and proposal evidence against ADR-0004 and the Account Capability Fabric architecture design. It does not replace architecture design review.

It does not accept live broker connectivity, broker account truth, runtime truth, admission, approval, capital allocation, trading readiness or order-entry implementation.

ADR-0004 implementation can advance only when the relevant Gate evidence exists. Missing evidence must produce a typed blocker, not an implicit pass.

Required document order:

```text
ADR-0004
  -> Account Capability Fabric architecture design
  -> this acceptance
  -> T001 topic / roadmap
  -> scoped proposal
  -> implementation
```

## 2. Scheme Acceptance Model / 方案验收模型

ADR-0004 is accepted by layered evidence. A later implementation proposal may claim only the layers it actually proves.

| Layer | Acceptance target | Owner boundary | Required proof | Must fail if |
| --- | --- | --- | --- | --- |
| `L0-ARCH` | Architecture design is coherent before implementation | architecture / owner map | ADR-0004, architecture design, owner boundaries and negative constraints are linked and reviewed | proposal starts implementation before architecture design review |
| `L1-CONTRACT` | Account identity, observation envelope and capability registry are explicit | contracts / schemas | schema or typed fixture examples for identity, balances, positions, orders, fills, source health and capabilities | UI/backend invents fields without contract |
| `L2-MIRROR` | Account Mirror is the only Account Console read model path for source observations | mirror / backend | source artifact -> canonical observation -> projection evidence with source refs, checksum and checkpoint | UI/API calls broker/runtime directly or reads ad hoc broker payloads |
| `L3-UI-READBACK` | UI matches pinned projections for target accounts | frontend / browser acceptance | Playwright/API comparison evidence for funds, positions, orders, execution reports, source health and evidence | UI value differs from pinned projection or lacks provenance |
| `L4-COMMAND-BOUNDARY` | Command ability is disabled by default and gated when introduced | command owner / risk / gateway | capability registry shows disabled command for P0; future command proposal defines order intent, risk/approval, gateway and mirror readback | submit/cancel/replace controls appear without accepted command capability |
| `L5-CLOSEOUT` | Evidence is durable and repeatable | proposal / acceptance owner | local commands, artifacts, screenshots, checksums, blockers and verdict are recorded in proposal acceptance | acceptance is based on manual inspection or screenshots only |

Layer ordering:

```text
L0-ARCH
  -> L1-CONTRACT
  -> L2-MIRROR
  -> L3-UI-READBACK
  -> L4-COMMAND-BOUNDARY
  -> L5-CLOSEOUT
```

P0 can pass as observation-only with `L0-L3` and command-disabled proof from `L4`. It does not need paper or live order submission.

## 3. Required Gates / 必需门禁

| Gate ID | Gate | Required evidence | Must fail if |
| --- | --- | --- | --- |
| `ADR0004-G01-IDENTITY` | Account identity | namespace-qualified `account_id`, display alias, source kind and source mode | UI/API uses bare `19053` as canonical identity |
| `ADR0004-G02-PROVENANCE` | Observation provenance | every displayed balance, position, order, fill, settlement or equity value has source ref, observed timestamp and checksum or typed blocker | live-looking values render without provenance |
| `ADR0004-G03-CAPABILITY-REGISTRY` | Capability registry | each account has explicit observation, command, reconciliation and evidence capability entries | UI infers capability from broker, account kind, route or visible state |
| `ADR0004-G04-FABRIC-FIT` | Capability fabric fit | each new account behavior maps to observation, command, risk/approval, reconciliation, evidence or a newly accepted capability | implementation creates an ungoverned plane or broker-specific UI branch |
| `ADR0004-G05-COMMAND-DISABLED-DEFAULT` | Command disabled default | accounts without validated command capability render no submit, cancel or replace controls | any command action appears by default |
| `ADR0004-G06-PAPER-COMMAND` | Paper command gate | paper command capability declares gateway, allowed actions, risk checks, order intent contract and mirror readback | paper actions bypass order intent or readback |
| `ADR0004-G07-LIVE-COMMAND` | Live command gate | live command capability declares authority, risk/approval, session state, allowed actions, execution gateway and reconciliation | live action appears with missing authority or stale readback |
| `ADR0004-G08-OWNER-SEPARATION` | Owner separation | observation owner, command owner, risk/approval owner and UI owner are declared separately | Account Mirror or UI becomes execution authority |
| `ADR0004-G09-READBACK-RECONCILIATION` | Mirror readback reconciliation | command status reconciles execution events with Account Mirror observations | UI treats button click or gateway response alone as final account state |
| `ADR0004-G10-FAIL-CLOSED-BLOCKERS` | Fail-closed blockers | missing source, stale source, missing capability, failed risk, missing approval and reconciliation mismatch produce typed blockers | UI silently hides evidence or shows success |

### 3.1 Gate To Layer Mapping / Gate 与分层映射

| Gate | Required layers | First target account | Evidence owner |
| --- | --- | --- | --- |
| `ADR0004-G01-IDENTITY` | `L1`, `L3` | `acct.ctp.paper.19053` | contract + UI |
| `ADR0004-G02-PROVENANCE` | `L1`, `L2`, `L3` | `acct.ctp.paper.19053` | source bridge + mirror + UI |
| `ADR0004-G03-CAPABILITY-REGISTRY` | `L1`, `L3`, `L4` | both MVP accounts | contract + UI |
| `ADR0004-G04-FABRIC-FIT` | `L0`, `L1`, `L2` | all new account sources | architecture + proposal |
| `ADR0004-G05-COMMAND-DISABLED-DEFAULT` | `L3`, `L4` | both MVP accounts | UI + capability registry |
| `ADR0004-G06-PAPER-COMMAND` | `L0`, `L1`, `L2`, `L4`, `L5` | future paper command account | future command proposal |
| `ADR0004-G07-LIVE-COMMAND` | `L0`, `L1`, `L2`, `L4`, `L5` | future live command account | future command proposal |
| `ADR0004-G08-OWNER-SEPARATION` | `L0`, `L2`, `L4` | all source/command paths | owner map |
| `ADR0004-G09-READBACK-RECONCILIATION` | `L2`, `L4`, `L5` | future command account | command + mirror |
| `ADR0004-G10-FAIL-CLOSED-BLOCKERS` | `L2`, `L3`, `L5` | both MVP accounts | backend + UI |

## 4. MVP Gate Target / MVP 门禁目标

The first ADR-0004 implementation target is observation-only:

```text
ADR0004-G01-IDENTITY = pass
ADR0004-G02-PROVENANCE = pass
ADR0004-G03-CAPABILITY-REGISTRY = pass_for_observation_only
ADR0004-G04-FABRIC-FIT = pass
ADR0004-G05-COMMAND-DISABLED-DEFAULT = pass
ADR0004-G06-PAPER-COMMAND = not_applicable_until_command_proposal
ADR0004-G07-LIVE-COMMAND = not_applicable_until_command_proposal
ADR0004-G08-OWNER-SEPARATION = pass_for_observation_only
ADR0004-G09-READBACK-RECONCILIATION = planned
ADR0004-G10-FAIL-CLOSED-BLOCKERS = pass_for_observation_only
```

MVP account targets:

```text
acct.nautilus.paper.demo
acct.ctp.paper.19053
```

Real-account read-only consistency target:

```text
acct.ctp.live.025292
```

`acct.ctp.live.025292` is accepted by pinned source/projection/UI comparison only. It does not imply command capability, live trading readiness or broker truth ownership.

## 5. Acceptance Scenarios / 验收场景

The scheme is not accepted by one happy path. It needs scenario coverage.

| Scenario ID | Scenario | Positive proof | Negative proof |
| --- | --- | --- | --- |
| `S1-IDENTITY` | CTP Paper `19053` is represented as `acct.ctp.paper.19053` | selector, API payload and evidence use namespace-qualified id with alias `19053` | bare `19053` rejected as canonical id |
| `S2-FUNDS` | funds/equity/margin render from pinned projection | UI values match projection/source package within declared decimal tolerance | mismatched funds produce `ctp19053_ui_value_mismatch` |
| `S3-POSITIONS` | positions render from pinned projection | row count and instrument/direction/qty/price/PnL fields match projection | missing, extra or stale rows fail |
| `S4-ORDERS` | order rows render when order observations exist | order id, status, qty, filled qty and source refs match projection | invented order state or missing refs fail |
| `S5-EXEC-REPORTS` | execution reports are visible and linked | report refs/checksums are visible from order detail/evidence path | execution report hidden or treated as final truth fails |
| `S6-SOURCE-HEALTH` | source status is honest | healthy/stale/blocked status matches source package lag and blockers | stale source shown as healthy fails |
| `S7-COMMAND-DISABLED` | observation-only account has no command surface | submit/cancel/replace controls absent; capability says disabled | command controls appear before command proposal acceptance |
| `S8-ACCOUNT-SWITCH` | account-scoped projections do not leak across accounts | switching to a blocked/empty account clears funds/positions/orders from prior account | previous account rows remain visible |
| `S9-FABRIC-EXTENSION` | IB/stock/Nautilus paper use the same capability/mirror path | new source maps to accepted capability + canonical projection | broker-specific UI/API branch appears |
| `S10-CTP025292-REAL-ACCOUNT-CONSISTENCY` | CTP Live `025292` funds, positions and orders match a pinned read-only source snapshot through Account Mirror | UI/API values match the source/projection package for `acct.ctp.live.025292`; command remains disabled | UI/backend calls CTP directly, source package is unpinned, values mismatch, or command controls appear |

## 6. Required Evidence Shape / 必需证据形态

Each proposal or topic phase that claims an ADR-0004 Gate must record:

```text
gate_id:
status:
account_ids:
contracts:
fixtures_or_api_samples:
source_refs:
checksums:
owner_boundary:
positive_evidence:
negative_evidence:
typed_blockers:
local_commands:
```

For UI readback acceptance, the record must also include:

```text
ui_route:
api_response_ref:
browser_screenshot_ref:
selector_assertions:
projection_checkpoint_id:
source_observed_at:
tolerance_policy:
comparison_result:
```

## 7. Verdict Rules / 裁决规则

Allowed verdicts:

```text
passed_for_architecture_design
passed_for_observation_only
passed_for_paper_command_design
passed_for_live_command_design
failed
blocked
not_applicable_until_command_proposal
```

P0 observation-only acceptance requires:

1. `L0-ARCH` pass.
2. `L1-CONTRACT` pass for identity, balance, position and capability registry.
3. `L2-MIRROR` pass for Nautilus Paper and CTP Paper `19053` projection path.
4. `L3-UI-READBACK` pass for funds, positions, source health and evidence.
5. `L4-COMMAND-BOUNDARY` pass as disabled command only.
6. `L5-CLOSEOUT` pass with durable artifacts and blocker records.

P1 orders/execution-report acceptance adds:

1. order observation contract and projection evidence;
2. execution report observation or provenance refs;
3. UI order table and order detail/evidence path comparison;
4. negative proof that execution report text is not treated as account truth.

Future command acceptance cannot reuse observation-only verdicts. It needs a separate command proposal or ADR with order intent, authority, risk/approval, execution gateway and mirror readback evidence.

## 8. Negative Acceptance / 反向验收

ADR-0004 acceptance must fail if:

1. Account Console UI calls CTP, IB TWS, stock broker or Nautilus runtime APIs directly.
2. Account identity uses unqualified aliases such as `19053` as canonical IDs.
3. Account Mirror sends, cancels, replaces, approves or allocates.
4. Broker-specific UI branches bypass canonical projections.
5. Command controls appear without capability registry evidence.
6. Paper command bypasses order intent or mirror readback.
7. Live command appears without authority, risk/approval, session state and readback gates.
8. A gateway response or button click is treated as final account state.
9. Missing or stale source evidence is hidden behind a healthy display.
10. New account behaviors create ad hoc planes instead of accepted capabilities.

## 9. Local Validation / 本地验证

Minimum local documentation gates:

```powershell
python scripts\check_proposal_docs.py --root .
python scripts\validate_owner_boundaries.py
python scripts\validate_adr004_p011_landing_consistency.py
```

When implementation lands, successor proposals must add focused contract, fixture, backend and browser checks for the touched Gates.

## 10. Current UI Gate Evidence / 当前 UI 门禁证据

API-backed Account Workbench browser acceptance:

```powershell
cd frontend
npx playwright test tests/e2e/account-terminal-workbench.spec.ts
```

Gate coverage:

| Gate | Evidence | Current status |
| --- | --- | --- |
| `ADR0004-G01-IDENTITY` | account selector and top status use namespace-qualified IDs for `acct.ctp.paper.19053`, blocked `acct.ctp.live.025292` and `simulated-001` with aliases only as display text | pass for observation-only API-backed mode |
| `ADR0004-G02-PROVENANCE` | CTP Paper `19053` positions/orders/execution report refs and evidence rail render source refs from mirror API; blocked CTP `025292` exposes typed blocker instead of values | pass for observation-only API-backed mode |
| `ADR0004-G03-CAPABILITY-REGISTRY` | capability table renders F2/F4/F3/F5 rows and command state from registry payloads instead of inferring from broker/account kind | pass for observation-only |
| `ADR0004-G05-COMMAND-DISABLED-DEFAULT` | command capability state renders observation-only/none-mounted and forbidden command wording is absent across desktop/tablet/mobile | pass |
| `ADR0004-G08-OWNER-SEPARATION` | owner boundary validator and API/UI tests show Account Console projects only; no broker/runtime write path is introduced | pass for observation-only |
| `ADR0004-G10-FAIL-CLOSED-BLOCKERS` | blocked CTP `025292` renders no positions/orders/execution reports and shows source unavailable / typed blocker state; `simulated-001` shows broker submission disabled | pass for observation-only |

Browser evidence is recorded in:

```text
docs/acceptance/2026-06-15-p011-account-workbench-api-readback-browser-evidence.json
docs/acceptance/browser-evidence/p011-account-workbench-api-readback/
```

This evidence is not acceptance of live CTP, IB TWS, stock or Nautilus runtime connectivity. It accepts only Account Console read-only projection/UI behavior against pinned repo-local source artifacts and typed blockers. CTP `025292` real-account consistency remains blocked until a pinned read-only source package is provided.
