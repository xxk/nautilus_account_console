# Legacy acct.demo-19053 Simulated 001 ag2612 UI Acceptance

- Date: 2026-06-16
- Status: implementation_browser_evidence
- Manual URL: `http://127.0.0.1:5173/accounts/acct.demo-19053`
- Executable route: `/accounts/acct.demo-19053`
- Canonical account: `simulated-001`
- Account UID: `sandbox-paper.simulated-001`
- Scenario: sandbox paper buy one `ag2612`
- Evidence output: `docs/acceptance/2026-06-16-legacy-acct-demo-19053-simulated-001-ag2612-ui-acceptance-evidence.json`
- Browser evidence dir: `docs/acceptance/browser-evidence/legacy-simulated-001-ag2612/`

## Acceptance Boundary

This acceptance verifies that the legacy Account Workbench URL `acct.demo-19053` opens the Simulated 001 sandbox paper projection and displays the result of a sandbox paper buy-one-lot `ag2612` scenario.

The UI does not submit the order. The order, position and account values are read-only projection inputs owned by `nautilus_strategies.sandbox_paper_runtime` and rendered by Account Console. Account Console remains projection-only and does not write ledger, order, fill, position, account, admission, approval, capital or broker truth.

## Required Projection

The source projection is:

```text
contracts/source_artifacts/account_sources/nautilus_sandbox_paper_simulated_001_source.json
```

Required source facts:

```text
account_id: simulated-001
account_uid: sandbox-paper.simulated-001
source_kind: nautilus_sandbox_paper
ledger_type: simulated_sandbox_ledger
broker_order_submission: false
trading_adapter: disabled
scenario: ag2612_buy_one_lot
```

## Positive UI Acceptance

The UI acceptance passes only when opening `http://127.0.0.1:5173/accounts/acct.demo-19053` shows:

1. readback mode `mirror API`;
2. canonical account `simulated-001`, alias `Simulated 001`, and UID `sandbox-paper.simulated-001`;
3. funds from the Simulated 001 projection, including equity, available cash and margin;
4. one `ag2612` long position with net quantity `1` and available quantity `1`;
5. one order `simulated-001-ag2612-buy-1-001` with side `BUY`, status `FILLED`, quantity `1` and filled quantity `1`;
6. execution report provenance for the same order;
7. source/evidence refs and projection checksum;
8. command plane remains `observation only` / `none mounted`.

## Negative UI Acceptance

This acceptance must fail if:

1. `acct.demo-19053` renders `acct.ctp.live.025292` or any account other than `simulated-001`;
2. the UI offers submit, cancel, replace or live order controls;
3. the UI claims Paper ready, Live ready, admitted, production ready, capital allocated, broker tradable or can trade;
4. `ag2612` position or order rows are missing while the scenario is declared passed;
5. browser evidence is used as sandbox ledger truth.

## Browser Acceptance

Run:

```powershell
cd frontend
npx playwright test tests/e2e/legacy-simulated-001-ag2612-ui-acceptance.spec.ts --project=desktop
```

Expected result:

```text
verdict: passed
canonical_account_id: simulated-001
scenario: sandbox_paper_buy_one_ag2612
```

This evidence proves UI rendering and projection consistency only. It does not prove runtime dispatch, broker order submission or trading readiness.
