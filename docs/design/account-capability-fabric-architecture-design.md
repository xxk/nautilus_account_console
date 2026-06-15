# Account Capability Fabric Architecture Design / 账户能力织构架构设计

- Date: 2026-06-15
- Status: architecture design draft
- Scope: architecture design for ADR-0004 landing without implementation drift
- ADR anchor: [ADR-0004 Account Capability Fabric With Mirror Readback](../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- Topic anchor: [T001 Account Mirror Observation Plane](../topics/T001-account-mirror-observation-plane.md)
- Acceptance anchor: [ADR-0004 Account Capability Fabric acceptance](../acceptance/2026-06-15-adr0004-account-capability-fabric-acceptance.md)

## 1. Design Intent / 设计意图

This design turns ADR-0004 into implementation architecture without starting implementation.

This design must be reviewed before successor proposals implement ADR-0004. Acceptance Gates validate this design and ADR-0004 together; they do not replace this design.

The goal is to prevent three architecture errors:

1. Account Console accidentally becoming a broker/runtime writer.
2. Broker-specific branches leaking into UI and API surfaces.
3. Future command entry being bolted onto Account Mirror instead of gated by explicit capabilities.

The core rule:

```text
Account is identity.
Capability is what the system may do with that identity.
Projection is what the UI may display.
Command is what an authorized gateway may attempt.
Evidence is why we believe or block it.
```

## 2. System Boundary / 系统边界

```text
External source owners
  - Nautilus Paper runtime
  - nautilus_ctp_adapter
  - IB TWS adapter
  - future stock adapter
  - replay / fixture producers

          produce read-only observations
                    |
                    v
nautilus_account_console
  - contracts
  - mirror ingest
  - projection store
  - capability registry projection
  - read-only API
  - Account Workbench UI

          may display projections and blockers
          must not write broker/runtime truth
```

Account Console may own local mirror projections. It must not own broker state, runtime state, admission, approval, capital allocation or trading readiness.

## 3. Bounded Contexts / 有界上下文

| Context | Responsibility | Owns | Must not own |
| --- | --- | --- | --- |
| Source Adapter | produce source observations or source artifacts | broker/runtime-specific read-only payloads, source refs | Account Console UI state |
| Observation Contract | canonical observation envelope and payload schemas | schema versions, validation rules | broker action semantics |
| Account Mirror | ingest observations and reduce projections | mirror ledger, projection state, source health | broker truth, order execution |
| Capability Registry | declare explicit account capabilities | observation/command/reconciliation/evidence capability projection | hidden authorization or account truth |
| Account Console API | expose read-only projections | query endpoints, blockers, refs | direct broker calls, mutation |
| Account Workbench UI | render projections | panels, selectors, evidence drawers | account calculations as truth, command actions |
| Future Command Capability | order intent and execution path | command contracts, gateway ownership, readback requirements | Account Mirror mutation |

## 4. Reference Architecture / 参考架构

```text
Source Adapter
  -> Canonical Observation Envelope
  -> Mirror Ingest
  -> Mirror Ledger
  -> Projector
  -> Projection Store
  -> Capability Registry Projection
  -> Read-only API
  -> Account Workbench UI
```

Future command path:

```text
Order Intent
  -> Risk / Approval Capability
  -> Execution Gateway
  -> Execution Event
  -> Account Mirror Readback
  -> Reconciliation Projection
  -> UI command status
```

No edge may skip from UI to broker/runtime.

## 5. Canonical Identity / 标准身份

Internal account identity must be namespace-qualified:

```text
acct.nautilus.paper.<account>
acct.ctp.paper.19053
acct.ctp.live.<account>
acct.ib.paper.<account>
acct.ib.live.<account>
acct.stock.paper.<broker>.<account>
acct.stock.live.<broker>.<account>
```

Display aliases are presentation only:

```text
19053
Nautilus Paper Demo
IB Paper DU123456
```

Design rule: no storage key, URL param, source ref, checksum record or test fixture may rely on a bare alias as canonical identity.

## 6. Observation Envelope / 观测信封

All sources should bridge into a common envelope before projection:

```text
observation_id
schema_version
observed_at
received_at
source_id
source_kind
source_mode
account_id
instrument_id?
observation_type
payload
source_ref
checksum
producer_owner
projection_owner
```

Required `observation_type` baseline:

```text
account_balance
position_snapshot
order_state
fill
settlement
equity_point
source_health
capability_state
```

Do not let broker-native payloads become UI contracts. Broker payloads are source evidence only.

## 7. Capability Model / 能力模型

Capability registry is a projection. It controls what UI/API may expose.

Minimum shape:

```text
account_id
observation.enabled
observation.source_kind
observation.mirror_state
reconciliation.enabled
evidence.required
command.enabled
command.mode
command.gateway_kind
command.allowed_actions
command.requires_risk_check
command.requires_approval
command.authority_ref
source_ref
checksum
```

Capability states:

```text
disabled
enabled
stale
blocked
unknown
```

Command modes:

```text
disabled
paper
live
```

Fail-closed rule: `unknown`, missing, stale or blocked command capability renders no command controls.

## 8. Projection Store / 投影存储

The projection store should keep read models separate by responsibility:

```text
accounts
balances
positions
orders
fills
settlement
equity
source_health
capabilities
evidence
blockers
```

Each projection row must carry:

```text
account_id
projection_version
source_ref
checksum
observed_at
projected_at
staleness_state
blocker_id?
```

The first implementation may be file-backed JSONL/SQLite. The contract boundary matters more than storage choice.

## 9. API Surface / API 面

Read-only API baseline:

```text
GET /api/accounts
GET /api/accounts/{account_id}
GET /api/accounts/{account_id}/balances
GET /api/accounts/{account_id}/positions
GET /api/accounts/{account_id}/orders
GET /api/accounts/{account_id}/fills
GET /api/accounts/{account_id}/settlement
GET /api/accounts/{account_id}/equity
GET /api/accounts/{account_id}/capabilities
GET /api/accounts/{account_id}/source-health
GET /api/accounts/{account_id}/evidence
```

Forbidden in Account Console API until a separate command proposal:

```text
POST /orders
POST /cancel
POST /replace
POST /funding
POST /allocation
```

Future command APIs belong to a command authority surface, not Account Mirror.

## 10. UI Design Boundary / UI 设计边界

Account Workbench may show:

1. account identity and alias;
2. capability badges;
3. balances and positions;
4. order/fill readback;
5. source health;
6. evidence refs and blockers.

Account Workbench must not show command controls unless all command capability gates pass.

Allowed disabled presentation:

```text
Command capability: disabled
Reason: no command authority accepted for this account
```

Forbidden presentation:

```text
Paper ready
Live ready
Can trade
Submit order
Cancel order
Replace order
```

## 11. Source Adapter Patterns / Source 接入模式

### Nautilus Paper

Preferred first source because it is first-party and safe for contract iteration.

```text
Nautilus Paper runtime/read model
  -> account_balance observations
  -> position_snapshot observations
  -> order/fill observations
```

### CTP Paper 19053

Preferred bridge:

```text
nautilus_ctp_adapter source artifact
  -> canonical observations
  -> Account Mirror projection
```

Do not let Account Console call CTP Trader API directly.

### IB TWS

IB should use its own source adapter:

```text
IB TWS account summary / positions / portfolio updates
  -> canonical observations
```

Do not encode IB account summary fields directly in UI.

### Future Stock

Stock support must enter through the same envelope and capability registry. Asset class differences belong in instrument metadata, not UI branching.

## 12. Staleness And Blockers / 新鲜度与阻塞

Staleness is not failure by itself, but it must be visible.

Typed blocker baseline:

```text
source_unavailable
source_stale
schema_mismatch
checksum_mismatch
owner_boundary_missing
capability_missing
command_authority_missing
risk_or_approval_missing
readback_reconciliation_mismatch
```

No projection may silently convert missing source evidence into healthy empty state.

## 13. Future Command Capability / 未来命令能力

Command capability must be added through a separate ADR/proposal. Required chain:

```text
order_intent
  -> pre_trade_check
  -> approval_or_risk_gate
  -> execution_gateway
  -> execution_event
  -> account_mirror_readback
  -> reconciliation
```

The command gateway may submit to Nautilus Paper, CTP, IB TWS or stock brokers. Account Mirror only observes the result.

Design invariant:

```text
Gateway response != final account state
Mirror readback + reconciliation = UI-visible command result
```

## 14. First Landing Slice / 首个落地切片

Do not start with IB or stock. First prove two-source mirror consistency:

```text
acct.nautilus.paper.demo
acct.ctp.paper.19053
```

Minimum slice:

1. observation envelope contract;
2. balance observation contract;
3. position observation contract;
4. capability registry contract;
5. file-backed or artifact-backed observations;
6. projection reader;
7. `/accounts/{account_id}` and `/positions` API;
8. UI read-only Account Summary and Positions panels in API mode;
9. typed stale/missing/capability blockers;
10. no command controls.

## 15. Architecture Review Checklist / 架构评审清单

Before implementation starts, reviewers must answer:

| Check | Question | Fail if |
| --- | --- | --- |
| Identity | Are all account IDs namespace-qualified? | bare alias is canonical |
| Source boundary | Does Account Console avoid direct broker/runtime calls? | UI/API calls broker |
| Contract boundary | Are broker payloads bridged into canonical observations? | UI consumes native broker payloads |
| Capability | Is command ability explicit and fail-closed? | UI infers from account type |
| Provenance | Does every displayed value carry source refs/checksums? | values lack evidence |
| Staleness | Are stale/missing states visible? | stale becomes healthy |
| Owner separation | Are observation, command, risk/approval and UI owners separate? | Mirror or UI is execution authority |
| Command future | Does the design preserve order intent and mirror readback? | gateway response is final state |
| Extensibility | Would IB/stock add sources without UI branching? | new broker requires new UI model |

## 16. Anti-Patterns / 反模式

Reject these designs:

1. FastAPI endpoint calls CTP/IB directly to fill a UI table.
2. React component switches on `broker_kind` to parse fields.
3. `19053` is stored as canonical account ID.
4. Empty positions are shown when source is stale or missing.
5. Command buttons appear because account domain is `paper`.
6. Account Mirror writes order commands.
7. Gateway response is rendered as final account state without mirror readback.
8. New broker support creates a parallel account API family.
9. Source refs/checksums are optional for live-looking values.
10. Capability registry is treated as broker authorization truth instead of local projection.
