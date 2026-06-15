# P005 UI Design: Intraday Monitor

- Proposal ID: `p005-intraday-monitor-exception-queue-panel`
- Status: design_gate_ready
- Updated: 2026-06-15
- Parent design: [Account Console UI implementation design](../../design/account-console-ui-implementation-design.md)

## 1. Design Intent

The Intraday Monitor at `/monitor` is a dense operational read-only surface for active exceptions, stale streams, lag states, incidents and blocker refs.

It must show what needs attention and which typed source refs prove the projection. It must not control runtimes, repair streams, mutate incidents, submit orders, mark readiness or replace owner artifacts.

## 2. Route And Placement

| Item | Design |
| --- | --- |
| Route | `/monitor` |
| Workbench | Intraday Monitor |
| Panel | Intraday Monitor Exception Queue Panel |
| Primary users | operations, risk, AI repair reviewer |
| First viewport | context bar, lag strip, exception queue and blocker/source refs |

## 3. Layout

Desktop layout:

```text
+--------------------------------------------------------------------------------+
| Context: trading day | session | monitor checkpoint | stream state | lag bucket |
+--------------------------------------------------------------------------------+
| Lag strip: max lag | stale streams | open incidents | blocked sources           |
+--------------------------------------------------------------------------------+
| Exception queue: severity | kind | owner | next action | source ref | checksum   |
+--------------------------------------------------------------------------------+
| Stream state and incident refs | blocker refs | read-only detail drawer        |
+--------------------------------------------------------------------------------+
```

Mobile layout:

1. Context stacks above the queue.
2. Lag strip becomes a compact two-column grid.
3. Exception rows become scannable blocks with source refs below the summary.
4. Detail drawer becomes a read-only sheet.

## 4. Required UI Components

| Component | Required content | Must not do |
| --- | --- | --- |
| Context bar | trading day, session id, monitor checkpoint, stream state | imply runtime control |
| Lag strip | max lag ms, stale stream count, open incident count, blocked source count | claim HFT readiness |
| Exception queue | severity, kind, owner, next action, source ref, checksum | resolve or accept incidents |
| Stream state list | stream id, status, last event timestamp, lag ms, source ref | start/stop streams |
| Blocker list | blocker id, severity, owner, next action, source ref | hide blocked sources |
| Source ref drawer | source ref, checksum, owner, authority | treat latest/debug path as truth |

## 5. Data Test ID Hooks

Required Data Test ID hooks:

```text
intraday-monitor-panel
intraday-monitor-context-bar
intraday-monitor-lag-strip
intraday-monitor-exception-queue
intraday-monitor-stream-state
intraday-monitor-incident-row
intraday-monitor-source-ref
intraday-monitor-blocker
intraday-monitor-detail-drawer
```

## 6. Interactions

| Interaction | Expected behavior | Must not do |
| --- | --- | --- |
| Open exception detail | opens read-only source and blocker details | mutate incident state |
| Copy source ref | copies exact displayed ref/checksum | alter evidence |
| Filter severity | filters fixture-backed rows locally | change source owner state |
| Open incident ref | opens read-only detail drawer or evidence route | mark resolved |

