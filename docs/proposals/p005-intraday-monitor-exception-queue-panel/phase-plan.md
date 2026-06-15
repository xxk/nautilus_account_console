# P005 Phase Plan

- Proposal ID: `p005-intraday-monitor-exception-queue-panel`
- Status: phase2_monitor_ui_browser_evidence_passed
- Updated: 2026-06-15

## Phase 0: Design Gate

- Status: completed
- Goal: confirm proposal-level Intraday Monitor UI design and acceptance before implementation.
- Exit evidence:
  - `ui-design.md` defines `/monitor` layout, states, interactions and stable selectors.
  - `ui-acceptance.md` defines positive, negative, browser, selector and blocker acceptance.
  - Owner Boundary block is present in [README](./README.md).
  - UI Anti-Drift Acceptance block is present in [acceptance](./acceptance.md).
  - route coverage matrix binds `/monitor` to P005.

## Phase 1: Monitor Contract And Fixture Gate

- Status: completed
- Goal: add the Intraday Monitor read-model contract and deterministic fixture states.
- Exit evidence:
  - `contracts/ui/panels/intraday_monitor_panel.contract.json` exists before implementation.
  - current, empty, blocked, stale and partial fixtures exist under `contracts/ui/fixtures/intraday_monitor/`.
  - fixtures include source refs or typed blockers for exceptions, stream state, lag and incidents.
  - machine-readable acceptance evidence: `../../acceptance/2026-06-15-p005-phase1-intraday-monitor-contract-fixtures.json`.
  - no frontend implementation, browser evidence, runtime, account, order, ledger, broker, readiness, admission, capital, HFT, Account Console UI completion or loop-completion truth is created.

## Phase 2: Monitor UI Slice

- Status: completed
- Goal: implement the smallest read-only `/monitor` panel from the accepted P005 contract and fixtures.
- Exit evidence:
  - `/monitor` renders context, lag strip, exception queue, stream state, incidents, blockers and source refs.
  - stable `data-testid` hooks exist.
  - desktop, tablet and mobile browser evidence exists in `../../acceptance/browser-evidence/p005-intraday-monitor-exception-queue-panel/`.
  - machine-readable acceptance evidence: `../../acceptance/2026-06-15-p005-phase2-intraday-monitor-ui-browser-evidence.json`.
  - no runtime, stream, scheduler, broker, account, order, ledger, readiness, admission, capital, HFT, Account Console UI completion or loop-completion truth is created.
