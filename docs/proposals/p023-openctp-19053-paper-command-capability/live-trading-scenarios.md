# P023 Live Trading Scenario Catalog / 实盘交易场景清单与验收设计

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted
- Primary ADR: ADR-0007
- Scope: derive live-trading scenarios, then map them to OpenCTP 19053 7x24 paper acceptance or live-blocked gates.

## Principle

实盘交易验收不能只证明“能发出一笔委托”。必须证明 command path 在正常、异常、恢复和审计场景下都不会绕过 authority、risk、approval、readback 和 reconciliation。

OpenCTP 19053 是 7x24 paper lane。它可以覆盖大部分 command workflow，但不能证明 live readiness、capital approval、生产 admission 或真实资金风险。

## Scenario Groups

| Group | Live trading concern | 19053 paper coverage | Live acceptance state |
| --- | --- | --- | --- |
| G1 Pre-trade readiness | session, account, instrument, trading window, risk/admission/capital | paper session + account/instrument query | live blocked until external owners provide refs |
| G2 Submit | new order intent, limit price, side, qty, TIF, idempotency | paper submit with small qty and safe limit price | live blocked unless `live_armed` |
| G3 Cancel | cancel open order by readback identity | paper cancel from `ReqQryOrder` identity | live blocked unless order owner and approval pass |
| G4 Fill lifecycle | full fill, partial fill, no fill | paper full/no-fill; partial may be simulated or blocked if unavailable | live requires real fill evidence |
| G5 Reject/block | broker reject, risk block, approval block, invalid instrument, insufficient margin | risk/approval negative fixtures and paper reject where available | live must fail closed |
| G6 Connectivity | disconnect, timeout, reconnect, stale readback | typed blockers and retry policy | live cannot continue without fresh readback |
| G7 Session conflict | duplicate login, wrong owner, stale flow path | observation/session conflict evidence | live blocked on ambiguity |
| G8 Emergency controls | kill switch, disable account, cancel all future | design only; no cancel-all in P023 | live requires separate ADR/proposal |
| G9 Audit and reconciliation | command audit, readback, mismatch, replay | paper command audit and reconciliation artifacts | live requires immutable audit retention |
| G10 UI safety | buttons, status, disabled/live banners | Playwright paper/disabled states | live controls hidden unless `live_armed` |

## Detailed Scenarios

| ID | Scenario | Acceptance design | Pass evidence | Must fail if |
| --- | --- | --- | --- | --- |
| LT-01 | Preflight account ready | Query funds, positions, orders, fills before command | source refs for account/order/fill readback | command starts from stale/missing account state |
| LT-02 | Instrument tradability shape | Validate instrument exists, tick size, lot size, exchange, product type | instrument query artifact | UI free-text instrument bypasses contract |
| LT-03 | Trading window | Paper 7x24 may pass; live requires market/session/admission ref | trading-window decision artifact | 7x24 paper is claimed as live market open |
| LT-04 | Risk limit pass | Quantity, notional, exposure, max submits/minute pass policy | `RiskDecision.pass` | missing risk decision still sends order |
| LT-05 | Risk limit block | Oversized qty/notional/exposure blocked | `RiskDecision.block` | blocked intent reaches gateway |
| LT-06 | Approval/admission pass | Paper policy or live approver ref allows command | `ApprovalDecision.pass` | approval is inferred from account kind |
| LT-07 | Approval/admission block | Missing/expired approval blocks | typed blocker | live command sends without approval |
| LT-08 | Submit limit order | Send one guarded limit order | gateway event + post-submit `ReqQryOrder` | gateway ack marked final without readback |
| LT-09 | Submit idempotency | Retry same intent/idempotency key | one broker order identity | duplicate broker orders appear |
| LT-10 | Submit reject | Broker or gateway rejects invalid request | rejected event + no success readback | rejection hidden as pending/success |
| LT-11 | Cancel open order | Cancel order by readback identity | cancel event + terminal readback | cancel uses UI text/screenshot/latest path |
| LT-12 | Cancel idempotency | Retry same cancel intent | one cancel command, terminal state stable | repeated cancel creates inconsistent state without blocker |
| LT-13 | Cancel after fill | Cancel request races with fill | terminal filled/cancel-rejected reconciliation | UI says cancelled when filled |
| LT-14 | Partial fill then cancel | Observe partial fill and remaining qty cancel | fill + order status readback | remaining qty inferred without source evidence |
| LT-15 | Full fill | Observe complete fill | `ReqQryTrade` / fill report evidence | filled state comes only from gateway ack |
| LT-16 | No fill working order | Working order remains open | order readback `remaining_quantity > 0` | no-fill treated as failure without policy |
| LT-17 | Readback timeout | Post-submit/cancel readback missing | typed timeout blocker | timeout is accepted as pass |
| LT-18 | Readback mismatch | Broker identity/status differs from command audit | reconciliation mismatch artifact | mismatch hidden from UI |
| LT-19 | Disconnect before submit | Session unavailable | command blocked before gateway | command sends during unknown session |
| LT-20 | Disconnect after gateway ack | Ack received, readback unavailable | uncertain/blocked status | UI marks final state |
| LT-21 | Reconnect recovery | Reconnect and query current orders/trades | recovery readback + reconciliation | old in-memory state is trusted |
| LT-22 | Session conflict | Another owner/session may be active | conflict blocker | Account Console steals live session silently |
| LT-23 | Kill switch disabled account | Account command mode disabled | command capability blocker | UI keeps active controls |
| LT-24 | Secret redaction | Artifacts contain refs/checksums only | redaction validator | raw password/front/auth/token appears |
| LT-25 | Operator audit | Every action has operator/session/ref/checksum | command audit record | command cannot be reconstructed |
| LT-26 | UI disabled default | Command disabled before paper/live armed | Playwright no controls | submit/cancel controls appear early |
| LT-27 | Paper armed UI | Paper controls visible with paper banner | Playwright evidence | live-like wording shown for paper lane |
| LT-28 | Live dry run | Validate live intent without mutation | dry-run event only | live dry-run sends broker mutation |
| LT-29 | Live armed | Real live mutation allowed only with full refs | live-arm evidence bundle | any missing owner ref still enables live command |
| LT-30 | Post-session closeout | Persist audit/readback/reconcile artifacts | closeout manifest | browser text alone closes acceptance |

## 19053 Paper Acceptance Subset

The first executable P023 runtime should cover:

1. LT-01 preflight account ready
2. LT-02 instrument tradability shape
3. LT-04 risk limit pass
4. LT-05 risk limit block
5. LT-06 paper approval pass
6. LT-08 submit limit order
7. LT-09 submit idempotency
8. LT-11 cancel open order
9. LT-12 cancel idempotency
10. LT-17 readback timeout blocker
11. LT-18 readback mismatch blocker
12. LT-24 secret redaction
13. LT-25 operator audit
14. LT-26 UI disabled default
15. LT-27 paper armed UI
16. LT-30 post-session closeout

Partial fill, full fill and cancel-after-fill may be accepted as typed runtime blockers if the 7x24 paper lane does not naturally produce those states during the run. They cannot be faked as pass.

## Live Blocked Until

Live command is blocked until all are present:

1. `live_armed` capability evidence
2. risk owner ref
3. approval/admission owner ref
4. capital owner ref
5. command gateway owner ref
6. broker session owner/ref
7. trading-window decision ref
8. kill-switch state ref
9. post-command readback/reconciliation gates
10. redaction gate

## Closeout Shape

Each scenario closeout must record:

1. scenario id
2. command mode
3. input artifact refs
4. risk and approval refs
5. gateway event refs
6. readback refs
7. reconciliation refs
8. UI evidence refs where applicable
9. pass/block verdict
10. typed blocker when not pass
