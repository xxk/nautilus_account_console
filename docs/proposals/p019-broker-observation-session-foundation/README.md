# P019 Broker Observation Session Foundation / Broker 观测会话基础

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->

- Proposal ID: `p019-broker-observation-session-foundation`
- Status: proposed
- Created: 2026-06-20
- Updated: 2026-06-20
- Owner: account-console-architecture / account-console-contracts
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)
- Related proposal: [P018 IB TWS Read-Only Account Console Landing](../p018-ib-tws-readonly-account-console/README.md)
- Related topic: [IB TWS](../../topics/ib-tws/README.md)

## 1. Purpose / 目的

P019 is the successor proposal for ADR-0005. It prepares Account Console to own governed, read-only broker observation sessions for CTP, IB TWS / IB Gateway, stock broker APIs, CQG and TT without becoming an execution owner.

The proposal focuses on contracts, owner boundaries, durable observation storage, report mapping and drift guards before any live broker connection is implemented. Every observed broker order/fill callback must be recorded as a Nautilus-compatible `OrderStatusReport` or `FillReport` projection, with raw broker payloads retained only as provenance.

## 2. Scope / 范围

In scope:

1. Define `Broker Observation Profile` contract shape for CTP / IB / stock / CQG / TT.
2. Define session conflict policy and typed blockers for observation sessions.
3. Define Nautilus-compatible order status and fill report contracts for observed callbacks.
4. Define raw broker payload provenance refs and redaction rules.
5. Define durable local observation store requirements for order/fill reports, funds snapshots, positions snapshots, session health and freshness cursors.
6. Define Account Mirror input/projection boundary for broker observation sessions.
7. Add focused anti-drift tests proving no command capability, no raw secrets, no memory-only report loss and no broker-specific report truth path.

Out of scope:

1. Broker order submit, cancel, replace or modify.
2. CTP order insert/action, IB `placeOrder`/`cancelOrder`, CQG/TT/stock mutation APIs.
3. Broker credential, auth code, front address, API key, 2FA or launcher implementation.
4. Live trading readiness, admission, capital approval or broker tradability.
5. Replacing P018 same-slice IB source-package work; P019 defines the broker-generic foundation that future IB/CTP lanes must align to.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p019-broker-observation-session-foundation
  architecture_owner: nautilus_account_console
  contract_owner: account-console-contracts
  observation_session_owner: account-console-broker-observation-session
  projection_owner: account-console-account-mirror
  ui_or_report_owner: account-console-frontend
  execution_owner: Nautilus / future Execution Gateway, not Account Console observation
  approval_owner: none
  write_authority:
    allowed:
      - broker observation profile contracts
      - session conflict policy contracts
      - Nautilus-compatible observed order/fill report contracts
      - durable local observation store contracts
      - Account Mirror projection contracts and typed blockers
      - read-only UI/API projection of observation state
    forbidden:
      - raw broker secrets, auth codes, front addresses, API keys or 2FA material
      - broker order submit/cancel/replace/modify
      - broker runtime truth
      - broker order truth outside normalized Nautilus-compatible reports
      - capital, approval, readiness or tradability truth
  second_implementation_rejected:
    - broker-specific Account Console UI truth paths
    - browser parsing raw broker payloads as order truth
    - command capability inferred from connected observation session
    - per-broker order report schemas replacing Nautilus-compatible reports
  blocker_owner_if_missing_source: broker observation profile owner or runtime source owner
```

## 4. Architecture Shape / 架构形态

```text
Broker Observation Profile
  -> read-only broker observation adapter
  -> session conflict policy
  -> observed account/order/fill callbacks
  -> Nautilus-compatible OrderStatusReport / FillReport
  -> durable local observation store
  -> Account Mirror input and projection
  -> Account Console API/UI readback
```

Command remains outside this proposal and requires a separate ADR/proposal.

## 5. Development Tasks / 开发任务

1. Add broker observation profile schema and positive/negative fixtures.
2. Add session conflict policy schema and blocker fixtures.
3. Add Nautilus-compatible observed order status report schema and fixtures.
4. Add Nautilus-compatible observed fill report schema and fixtures.
5. Add raw broker payload provenance schema with redaction requirements.
6. Add durable observation store contract for reports, snapshots, session health, freshness cursors and replay gap markers.
7. Add Account Mirror mapper contract for observed broker reports.
8. Add focused tests rejecting command APIs, raw secret leakage, memory-only report loss, broker-specific report schemas and browser raw-payload parsing.
9. Update owner map and ADR-0005 landing references after design review.
10. Keep the pre-implementation audit current until ADR-0005 is accepted and implementation evidence closes its gates.

## 6. Review Verdict / 评审结论

**Current verdict**: `proposed`

| Item | Verdict |
| --- | --- |
| Formal proposal needed | yes |
| Requires ADR acceptance | yes, ADR-0005 |
| Requires child changes | yes |
| Allows broker order action | no |
| Allows raw broker secrets | no |
| Allows direct broker observation session | only if ADR-0005 is accepted and conflict policy passes |

## 7. Document Map / 文档地图

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | scope, boundary and architecture shape | present |
| `phase-plan.md` | phase order and gate plan | present |
| `acceptance.md` | proposal acceptance and anti-drift requirements | present |
| `pre-implementation-audit.md` | pre-code conflict/drift audit against ADR-0005, owner map and P018 | present |
| `pre-acceptance-coverage.md` | A1-A14 and PRE-G01..PRE-G09 partial/blocker coverage closeout, including screenshot-not-truth guard for funds and positions | present |
| `tws-today-slice-acceptance.md` | scoped TWS-only function list and acceptance matrix for the first implementation slice | present |
| `tws-account-workbench-ui-acceptance.md` | required Web UI Account Workbench acceptance for `acct.ib.live.u3028269`, funds, multi-currency funds and positions | present |
| `tws-api-runtime-recovery-runbook.md` | no-secret/no-screenshot runtime recovery path from current TWS API socket blocker to real read-only TWS API collection and Account Mirror validation | present |
| `workspace-home-runbook-intake.md` | read-only intake of workspace/home runbooks adopted for TWS API handshake and firewall/network recovery posture | present |
| `../../topics/ib-tws/README.md` | long-lived non-secret IB TWS topic entry, including the U3028269 login/API knowledge card | present |
| `../../topics/ib-tws/u3028269-tws-login-and-api-knowledge.md` | repeatable non-secret U3028269 TWS login/API enablement knowledge, safe success backfill template and forbidden secret/truth boundaries | present |
| `p019-completion-audit.json` | machine-readable completion audit proving P019 remains not complete until ADR-0005, real TWS API funds/positions, source package and UI parity evidence close | present |
