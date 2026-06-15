# Frontend Tests Owner Boundary

- Owner: `account-console-browser-acceptance-tests`
- Scope: Playwright browser acceptance tests under `frontend/tests/e2e`.
- Runtime authority: none.

This directory owns browser acceptance checks for Account Console UI projections. It may start the Vite dev server through Playwright, navigate accepted routes, assert stable selectors, and capture browser evidence.

It must not own route registration, read-model reduction, fixture generation, account/order/ledger truth, runtime truth, broker action authority, admission authority, capital authority, Paper readiness, Live readiness, or proposal completion.

Production UI code belongs under `frontend/src`. Contract fixtures belong under `contracts/ui/fixtures`. Browser evidence belongs under `docs/acceptance/browser-evidence`. Tests may reference those artifacts, but must not replace them.

Required boundary rules:

1. No production code imports from `frontend/tests`.
2. No test file creates a second route registry or feature-specific UI implementation.
3. No test file writes accepted contracts, fixtures, runtime artifacts, ledgers, or readiness evidence.
4. Screenshots, traces, and Playwright state prove display behavior only.
5. Feature-specific tests must exercise the canonical owner route and panel instead of adding a special runtime path.
