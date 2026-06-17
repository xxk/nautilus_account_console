# P018 IB TWS Read-Only Account Console Landing / IB TWS 只读账户台落地

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->

- Proposal ID: `p018-ib-tws-readonly-account-console`
- Status: design_gate_ready
- Updated: 2026-06-17
- Owner: account-console-ui / account-console-contracts
- Successor of: `p011-account-capability-contracts` Phase 8
- Roadmap anchor: [T001 Account Capability Feature Roadmap](../../topics/roadmap/T001-account-capability-feature-roadmap.md)
- ADR anchor: [ADR-0004](../../adr/0004-adopt-account-mirror-observation-and-command-plane.md)
- UI design: [P018 UI Design](./ui-design.md)
- UI acceptance: [P018 UI Acceptance](./ui-acceptance.md)

## 1. Purpose / 目的

This proposal lands the first IB TWS read-only account observation path for Account Console. The target operator outcome is a multi-account Account Workbench route that can display IB live account funds, positions, orders and fills from a local TWS / IB Gateway source package while preserving the Account Console read-only boundary.

The initial target account is represented inside Account Console as `acct.ib.live.u3028269`. The exact broker account id, local TWS endpoint, port, client id, credentials and any account secret remain owned by the IB runtime owner configuration and must not be copied into Account Console docs, fixtures, source, logs or chat. Account Console records only owner config refs, entrypoint refs, redacted shape/checksum and `raw_secret_values_recorded=false`.

## 2. Scope / 范围

In scope:

1. Add an IB source package contract for account summary, cash/funds, positions, open orders and executions/fills.
2. Define the owner-runtime boundary for local TWS / IB Gateway read-only collection.
3. Project an owner-produced IB source package into Account Mirror observations.
4. Expose the IB account through existing Account Workbench API/UI surfaces.
5. Validate UI readback from `nautilus_account_console` for funds, positions, orders, fills, source health, evidence refs and blockers.
6. Preserve multi-account management semantics: IB, CTP, Nautilus Paper and sandbox accounts share canonical Account Mirror contracts instead of broker-specific UI branches.

Out of scope:

1. Submit, cancel, replace or modify orders.
2. Funding transfer, allocation mutation or capital approval.
3. Account Console direct connection to TWS / IB Gateway.
4. Storing TWS credentials, exact endpoint, port, client id or raw broker account identifiers in Account Console.
5. Claiming broker tradability, can-trade, live readiness, production readiness or capital allocation.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p018-ib-tws-readonly-account-console
  broker_runtime_owner: nautilus_strategies
  source_package_owner: nautilus_strategies
  projection_owner: nautilus_account_console
  ui_or_report_owner: nautilus_account_console
  approval_owner: none
  write_authority:
    allowed:
      - Account Console contracts for IB source package shape
      - Account Mirror projection code and fixtures
      - Account Workbench API/UI readback
      - typed blockers and evidence refs
    forbidden:
      - TWS / IB Gateway session ownership
      - broker credentials, raw endpoint, raw account secret or auth material
      - broker order action
      - broker account truth
      - order truth
      - capital truth
      - readiness or tradability truth
  second_implementation_rejected:
    - Account Console backend opens a TWS socket
    - Account Console imports ibapi or Nautilus IB adapter to collect live account data
    - UI derives funds, positions, orders or fills from broker-native payload without Account Mirror projection
    - UI shows action controls or readiness labels from observation data
  blocker_owner_if_missing_source: nautilus_strategies source package owner
```

## 4. Architecture Shape / 架构形态

```text
local TWS / IB Gateway
  -> nautilus_strategies read-only collector
  -> pinned IB source package + checksum + redacted owner refs
  -> nautilus_account_console source package validator
  -> Account Mirror canonical observations
  -> Account Workbench API
  -> Account Console UI readback
```

Account Console must fail closed if the owner source package is missing, stale, checksum-mismatched, schema-mismatched, or lacks the required read-only fields.

## 5. Account Identity / 账户身份

| Field | Rule |
| --- | --- |
| Canonical account id | `acct.ib.live.u3028269` |
| Display alias | `IB Live U***8269` |
| Broker account source | owner config ref only |
| Runtime source | owner entrypoint ref only |
| Secret handling | `raw_secret_values_recorded=false` |

The canonical Account Console identity is stable and namespaced. The exact broker account id is validated by owner package metadata but is not stored as Account Console runtime secret material.

## 6. Development Tasks / 开发任务

1. Add `ib_tws_account_source_package.v1` schema and positive/negative fixture packages.
2. Add source package validator with negative cases for missing funds, stale package, checksum mismatch, broker action fields and raw secret leakage.
3. Add Account Mirror projection for IB funds, positions, orders and fills.
4. Add API readback for `acct.ib.live.u3028269`.
5. Add Account Workbench UI row/page coverage for IB multi-account management.
6. Add source health and evidence drawer rows for owner config ref, entrypoint ref, package checksum and collection time.
7. Add browser acceptance for desktop/tablet/mobile views.
8. Add regression guard proving Account Console does not connect to TWS directly and does not expose order action controls.

## 7. Review Verdict / 评审结论

**Current verdict**: `design_gate_ready`

| Item | Verdict |
| --- | --- |
| Formal proposal needed | yes |
| Roadmap needed | no; T001 already has IB TWS source lane |
| Requires child changes | yes |
| Requires owner source package | yes, from `nautilus_strategies` |
| Allows broker order action | no |

## 8. Document Map / 文档地图

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | scope, boundary and development design | present |
| `phase-plan.md` | phase order, source boundary and gate plan | present |
| `acceptance.md` | proposal acceptance rows and anti-drift gates | present |
| `ui-design.md` | Account Workbench UI shape and test ids | present |
| `ui-acceptance.md` | browser, negative and blocker acceptance | present |
| `ui-refactor-plan.md` | Account Workbench region architecture and staged UI refactor plan | present |
| `ui-detailed-screen.html` | high-fidelity local UI target for the P018 Account Workbench refactor | present |
