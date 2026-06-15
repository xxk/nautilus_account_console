# P001 Browser Runner Blocker

- Proposal ID: `p001-daily-closeout-account-health-panel`
- Recorded: 2026-06-13
- Status: resolved_by_portable_node_runner
- Scope: browser screenshot and Playwright evidence only

## Original UI Acceptance Blocker

```text
UI Acceptance Blocker:
  missing_tool:
    - npm is not available in the current PowerShell PATH.
    - corepack and npx are not available in the current PowerShell PATH.
    - node resolves to the Codex app packaged node.exe and is rejected by the OS with access denied.
    - no bundled workspace Node/npm runtime is configured for this thread.
  missing_contract: none
  missing_fixture: none
  missing_anti_drift_checklist: none
  missing_viewport_evidence:
    - desktop 1440x900 screenshot
    - tablet 1024x768 screenshot
    - mobile 390x844 screenshot
    - happy/blocked/stale/empty/partial Playwright screenshots
  unavailable_browser_runner:
    - npm run build cannot be executed in this local environment.
    - npm run test:e2e cannot be executed in this local environment.
  violated_boundary: none
  next_owner: account-console-ui environment owner
```

## Evidence Already Available

| Evidence | Result |
| --- | --- |
| Python backend compile | pass: `python -m compileall backend\src` |
| Rust hotpath tests | pass: `cargo test --manifest-path hotpath-rs\Cargo.toml` |
| Account Health fixture validator | pass via Codex Node REPL importing `frontend/scripts/validate-account-health-fixtures.mjs` |
| Forbidden wording/action scan | pass for `frontend\src backend\src hotpath-rs\crates contracts\ui` |

## Runner Recheck

| Check | Result |
| --- | --- |
| `Get-Command node,npm,pnpm,yarn` | only Codex app packaged `node.exe` is visible; `npm`, `pnpm` and `yarn` are unavailable |
| `Get-Command corepack,npx` | unavailable |
| `frontend\node_modules` | absent |
| `frontend\package-lock.json` | absent |
| `frontend\pnpm-lock.yaml` | absent |
| `frontend\yarn.lock` | absent |
| bundled workspace dependencies | none configured |

## Resolution

| Resolution item | Evidence |
| --- | --- |
| Portable Node/npm runner | `D:\Nautilus\.tools\node-v22.22.3-win-x64`; Node `v22.22.3`; npm `10.9.8` |
| Frontend dependencies | `npm install` completed and generated `frontend\package-lock.json` |
| Build validation | pass: `npm run build` |
| Contract fixture validation | pass: `npm run test` |
| Browser validation | pass: `npm run test:e2e`; desktop/tablet/mobile projects all passed |
| Browser evidence | screenshots under `docs\acceptance\browser-evidence\p001-daily-closeout-account-health-panel\` |
| Test selector repair | `frontend\tests\e2e\account-health-panel.spec.ts` now asserts the ADR-0044 account id through the account row `data-testid` instead of ambiguous page text |

## Security Follow-up

Closed by `docs/proposals/p003-frontend-dependency-security-followup/`: `npm audit --audit-level=high` now passes after the frontend dependency upgrade.

## Boundary

This resolved blocker does not promote Account Console to runtime truth. Browser evidence proves only the P001 read-only panel rendering against fixtures. It does not prove Account Console runtime truth, Paper readiness, admission, capital allocation or broker tradability.

