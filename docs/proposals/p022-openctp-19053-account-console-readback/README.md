# P022 OpenCTP 19053 Account Console Readback / OpenCTP 19053 账户显示

<!-- PROPOSAL-ANTI-DRIFT-GATE:v1 -->

- Proposal ID: `p022-openctp-19053-account-console-readback`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20
- Owner: account-console-broker-observation-session / account-console-frontend
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)
- Related proposal: [P019 Broker Observation Session Foundation](../p019-broker-observation-session-foundation/README.md)

## 1. Purpose

P022 lands the OpenCTP 7x24 simulation account `acct.ctp.paper.19053` in Account Console using the ADR-0005 read-only broker observation boundary.

The implementation must display funds, positions and open orders through Account Mirror from owner-produced `nautilus_ctp_adapter` artifacts. It must not own CTP secrets, raw front addresses, order submission, cancellation, replacement, broker truth, account truth, trading readiness or capital authority.

## 2. Scope

In scope:

1. Build `output/account_capability/ctp-paper-19053/source-package.json` from owner repo read-only artifacts.
2. Project CNY funds, CTP positions and open-order empty proof through Account Mirror.
3. Render `/accounts/acct.ctp.paper.19053` with funds, positions and an orders table/empty state.
4. Preserve source refs, checksums and no-command boundaries.
5. Add proposal-specific validators and browser evidence.

Out of scope:

1. CTP order insert/action, cancel, replace or modify.
2. Storing raw CTP password, auth code, raw front address or broker secret in this worktree.
3. Claiming broker/account/trading-readiness truth from Account Console.
4. Fabricating open orders when owner evidence reports zero current-session order events.

## 3. Owner Boundary

```text
Owner Boundary:
  proposal_or_change_id: p022-openctp-19053-account-console-readback
  source_owner: nautilus_ctp_adapter
  projection_owner: account-console-account-mirror
  ui_owner: account-console-frontend
  execution_owner: Nautilus / CTP adapter, not Account Console
  write_authority:
    allowed:
      - source package generated from owner artifact refs and checksums
      - read-only Account Mirror projection
      - UI readback of funds, positions and open-order empty/provenanced rows
    forbidden:
      - raw CTP secrets, auth codes, raw front addresses or broker secrets
      - CTP order insert/action/cancel/replace/modify
      - broker truth, account truth, live readiness, capital or approval claims
  second_implementation_rejected:
    - Account Console direct CTP session as command runtime
    - browser parsing raw CTP payloads as truth
    - repo-local sample rows displayed as current OpenCTP truth
```

## 4. Evidence Shape

Current implementation evidence is:

1. `owner://nautilus_ctp_adapter/output/account-console-ctp19053-readback/<session>/account_query.json`
2. `owner://nautilus_ctp_adapter/output/account-console-ctp19053-readback/<session>/paper_readonly_snapshot.json`
3. `output/account_capability/ctp-paper-19053/source-package.json`
4. `/api/mirror/accounts/acct.ctp.paper.19053`
5. Playwright evidence for `/accounts/acct.ctp.paper.19053`

Open orders are accepted as a typed empty state only when owner evidence reports zero current-session order events. A screenshot or absence of rows alone is insufficient.
