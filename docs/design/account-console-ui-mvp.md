# Account Console UI MVP Design / 账户控制台 UI MVP 设计

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Status: accepted for MVP skeleton
- Scope: UI information architecture, interaction boundaries and acceptance gates

## 1. Design Positioning

Nautilus Account Console is an account observation workspace, not a trading desk and not a static report page.

The UI is optimized for:

1. Multi-account scanning.
2. Single-account debugging.
3. High-frequency order lifecycle observation.
4. Report message provenance inspection.
5. Evidence/blocker visibility.

The UI must remain read-only. It cannot submit orders, cancel orders, edit runtime state, edit broker state, write admission/capital state or declare account tradability.

## 2. First Screen Layout

MVP layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ Nautilus Account Console              stream: live / stale    │
├───────────────┬──────────────────────────────────────────────┤
│ Accounts      │ Account Summary                              │
│               │ equity / cash / margin / pnl / lag / health  │
│ paper.demo-01 │                                              │
│ paper.demo-02 │ Positions | Orders | Fills | Reconcile        │
│ live.xxx      │                                              │
├───────────────┴──────────────────────────────────────────────┤
│ Order Event Tape                                             │
│ seq | time | order_id | status | fill | latency | report ref │
│ #1  submitted                                                │
│ #2  accepted                                                 │
│ #3  partially_filled                                         │
└───────────────────────────────────────────────┬──────────────┘
                                                │ Report Msg
                                                │ raw/ref/checksum
                                                │ normalized link
                                                └──────────────
```

The current MVP scaffold implements the first version as:

1. Left account selector.
2. Account summary metrics.
3. Order event tape.
4. Adjacent selected-order execution reports panel.
5. Stream status.

The selected-order execution reports panel is the default MVP behavior: selecting any row in the order event tape selects that `client_order_id`, and the neighboring panel shows every normalized execution report/order report event for that order.

The later drawer can still be added for large raw payload inspection, but it must be opened from a selected execution report and loaded by `report_msg_ref`.

## 3. Routes

Canonical routes:

| Route | Purpose |
| --- | --- |
| `/accounts` | Multi-account overview and workspace entry |
| `/accounts/{account_id}` | Single-account detail workspace |
| `/accounts/{account_id}/events` | Deep-linkable order event tape view |

Compatibility aliases may exist later, but they must route to the same account workspace:

| Alias | Behavior |
| --- | --- |
| `/paper/accounts` | filtered `/accounts?account_kind=real_feed_sandbox_paper` |
| `/console/accounts` | optional bridge from a host console |

## 4. Page Areas

| Area | Required MVP behavior | Source |
| --- | --- | --- |
| Account Overview | select account, show account kind and health | account snapshots |
| Account Summary | equity, available cash, margin, last seq, lag and health | reduced account snapshot |
| Positions | later tab, not required in first skeleton | positions read model |
| Orders | later tab, not required in first skeleton | current order reducer |
| Fills | later tab, not required in first skeleton | fill ledger |
| Order Event Tape | latest events, cursor, event type, status, instrument and report ref/excerpt | normalized order events |
| Order Execution Reports | all execution reports for the selected `client_order_id` shown beside the tape | normalized order events scoped by account and client order |
| Report Msg Drawer | selected report raw/normalized payload detail by ref/checksum | report msg payload store |
| Reconcile | later tab for target vs actual, blockers and source refs | reconcile summary |
| Provenance | later tab for refs/checksums/runtime owner/session id | manifest/read model |

## 5. High-Frequency Interaction Rules

1. The browser must not re-render the full page for each event.
2. The visible tape keeps only a bounded latest-N window, initially 500 rows.
3. History is loaded through paginated/cursor queries.
4. Visual updates may be sampled or paused; durable ledger events must not be dropped.
5. Every stream view must expose stream status, cursor and lag.
6. Stale, missing or partial evidence must show blocker state.
7. Large report messages must be loaded on demand by `report_msg_ref`, not embedded in every stream event.

## 6. Visual Design Rules

The console should feel like an operational trading observability tool:

1. Dense but readable layout.
2. Restrained color.
3. No marketing hero.
4. No decorative cards nested inside cards.
5. Numeric columns right-aligned in later table slices.
6. Health colors:
   - live: green
   - stale: amber
   - blocked: red
   - partial: blue-gray
7. Use icons only for clear operational controls or status, with text where ambiguity would slow debugging.

## 7. Forbidden UI Behavior

The UI must not:

1. Display `Paper ready`, `Live ready`, `admitted`, `production ready`, `capital allocated` or `can trade`.
2. Add submit/cancel/replace order actions.
3. Parse raw report messages in the browser as account truth.
4. Read `latest/`, `debug/`, screenshots, stdout or report HTML as account truth.
5. Hide missing evidence or stale stream state.
6. Treat UI display as Paper/Live acceptance evidence.

## 8. MVP UI Acceptance

MVP UI acceptance is met when:

| ID | Acceptance | Current status |
| --- | --- | --- |
| UI-A1 | First screen is the account console workspace, not a landing page | pass |
| UI-A2 | Account overview supports selecting an account | pass |
| UI-A3 | Account summary shows equity, cash, margin and last cursor/seq | pass |
| UI-A4 | Order event tape renders normalized events | pass |
| UI-A5 | Selecting an order shows all execution reports for that `client_order_id` in the adjacent panel | pass |
| UI-A6 | Stream status is visible | pass |
| UI-A7 | UI has stable `data-testid` hooks for console, overview, row, detail, summary, tape, execution reports, report msg and blocker | pass |
| UI-A8 | UI does not expose trading actions | pass |
| UI-A9 | UI does not display forbidden readiness/capital/live wording | pass by static scan |
| UI-A10 | Frontend build and browser render are verified | blocked by current Node/npm environment |

## 9. Successor UI Gates

The next UI change should add:

1. Right-side report msg drawer with lazy payload fetch.
2. Virtualized event tape using `@tanstack/react-virtual`.
3. Pause/resume visual stream control.
4. Cursor and lag display in the tape header.
5. Positions, Orders, Fills and Reconcile tabs.
6. Playwright screenshot and non-overlap checks once Node/npm is available.
7. Browser backpressure test against synthetic streamed events.
8. Deep links from `/accounts/{account_id}/orders/{client_order_id}` into the selected-order report panel.

The broader capability design and UI acceptance baseline are:

```text
docs/design/account-console-capability-ui-design.md
docs/acceptance/2026-06-13-account-console-capability-ui-acceptance.md
```
