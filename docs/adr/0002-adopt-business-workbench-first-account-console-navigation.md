---
status: accepted
owner: architecture
adr_id: "0002"
decision_status: accepted
landing_status: completed
---

# ADR-0002: Adopt Business Workbench First Account Console Navigation / 采用业务工作台优先的账户控制台导航

- Date: 2026-06-13
- ADR type: UI architecture
- Decision status: accepted
- Landing status: completed
- Scope: `nautilus_account_console` navigation, UI information architecture and UI acceptance
- Decision question: Should the Account Console UI be organized by artifact routes or by business workflows?
- Decision: Organize the UI by business workbenches first, with artifact/detail routes as drill-down panels inside those workbenches.

---

## 1. Problem Frame / 问题框架

The initial capability UI design listed many artifact-oriented views: accounts, orders, fills, positions, settlement, equity, reconcile, incidents, evidence, funding, portfolio and stream operations.

That is technically complete, but a professional quant team first asks workflow questions:

1. What needs attention today?
2. Which accounts are unclosed, unreconciled or blocked?
3. Which order/fill/position/account numbers explain the issue?
4. Which account-management or funding request is pending?
5. Which evidence package can an operator, PM, risk reviewer or AI repair agent use?

Therefore, the UI must prioritize business workbenches and expose artifact routes as drill-downs.

### 1.1 Hard Constraints / 硬约束

1. The first screen must be an account control tower, not a marketing page and not a raw artifact menu.
2. The UI remains read-only with respect to runtime truth, account truth, broker truth, admission truth and capital truth.
3. Account-management UI is request/projection-only until a typed request contract and accepted ledger event pipeline exist.
4. Evidence views must expose refs/checksums/schema/run/session/trading-day provenance.
5. HFT stream and benchmark UI must be isolated from ordinary account closeout workflows.
6. No UI surface may display `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade`.

### 1.2 Explicit Non-Goals / 明确不做

1. Do not implement trading actions, order entry, cancel, replace or broker actions.
2. Do not make Account Console the Paper runtime, account ledger or capital approval owner.
3. Do not make PM closeout UI a source of admission, capital or tradability truth.
4. Do not remove artifact routes; they remain drill-down surfaces.

## 2. Decision / 决策

Adopt seven business workbenches:

| Workbench | Primary users | Primary question | Default route |
| --- | --- | --- | --- |
| Daily Closeout | PM, risk, operations | Can today's Paper accounts close cleanly? | `/closeout` |
| Intraday Monitor | trader, operations | Which account/order/stream needs attention now? | `/monitor` |
| Account Workbench | strategy owner, researcher, developer | How did this account/order/fill/position state happen? | `/accounts/{account_id}` |
| Allocation Admin | PM, account admin | Which Paper accounts, assignments and virtual funding events are effective or requested? | `/management/accounts` |
| Risk And Reconcile | risk, operations | Which risk/reconcile gaps block trust? | `/risk-reconcile` |
| Evidence Explorer | developer, auditor, AI repair | Which refs/checksums/artifacts prove or block the state? | `/evidence` |
| Stream Ops | platform, HFT owner | Are ingest, ledger, replay, backpressure and browser rendering healthy? | `/ops/stream` |

Artifact routes remain supported as deep links:

```text
/accounts
/accounts/{account_id}/orders/{client_order_id}
/accounts/{account_id}/positions
/accounts/{account_id}/settlement
/accounts/{account_id}/equity
/portfolio/*
/ops/*
```

## 3. Design Acceptance / 设计验收

| Acceptance | Required evidence | Must fail if |
| --- | --- | --- |
| Business-first first screen | `/closeout` or `/accounts` presents account health, settlement state, blockers and drill-down links before raw artifact menus | first screen is only a route list or artifact table |
| Exception-driven workflow | blocked, stale, unreconciled and unclosed accounts are visually prioritized | user must inspect every account manually to find issues |
| Drill-down lineage | account/order/fill/position/evidence routes are reachable from workbench context | artifact route is isolated from business context |
| Request/projection account management | account create/suspend/retire/assign/fund controls are request-only and display typed status | UI mutates accepted account/funding truth |
| HFT isolation | `/ops/*` carries stream and benchmark evidence without overloading PM closeout | HFT metrics dominate daily account closeout |
| Forbidden wording | UI and fixtures avoid readiness/admission/capital/tradability wording | forbidden wording appears in user-visible implementation |

## 4. Consequences / 后果

Positive:

1. PM and operations users see daily account health before raw technical evidence.
2. Developers and AI repair agents still have artifact/evidence drill-downs.
3. Account-management workflows stay request/projection-only.
4. HFT and benchmark UI can evolve without distorting ordinary account workflows.

Trade-offs:

1. More navigation structure is required than a simple route list.
2. UI tests must validate both workflow pages and deep-link artifact pages.
3. Fixture design must include business states such as blocked, stale, partial and unclosed.

