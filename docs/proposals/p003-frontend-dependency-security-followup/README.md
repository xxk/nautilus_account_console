# P003: Frontend Dependency Security Follow-up

- Proposal ID: `p003-frontend-dependency-security-followup`
- Status: verified
- Updated: 2026-06-13
- Owner: account-console-frontend
- Parent evidence: [P001 Daily Closeout Account Health Panel](../p001-daily-closeout-account-health-panel/README.md)

## 1. Purpose / 目的

P001 browser evidence is verified, but `npm audit --audit-level=high` reports high severity findings through `vite -> esbuild`.

This proposal owns the dependency-security follow-up only. It does not change Account Console runtime truth, account truth, broker truth, admission truth or capital truth.

## 2. Scope / 范围

In scope:

1. Upgrade frontend build dependencies enough to clear the high severity `vite -> esbuild` audit finding.
2. Keep P001 read-only UI acceptance green after the dependency upgrade.
3. Record audit, build, fixture and browser evidence.

Out of scope:

1. UI product redesign.
2. Account, order, funding, broker, runtime, scheduler or admission behavior.
3. Paper readiness, Live readiness, capital allocation or broker tradability claims.

## 3. Acceptance Boundary / 验收边界

P003 passes only when:

1. `npm audit --audit-level=high` passes.
2. `npm run build` passes.
3. `npm run test` passes.
4. `npm run test:e2e` passes for desktop, tablet and mobile.
5. Source/contracts forbidden wording/action scan has no matches.

P003 must stop as typed blocker if the dependency upgrade requires UI/runtime redesign, breaks P001 browser evidence, or requires a second runtime/account truth.

## 4. Closeout Evidence / 收口证据

| Evidence | Result |
| --- | --- |
| Dependency upgrade | `vite` upgraded to `8.0.16`; `@vitejs/plugin-react` upgraded to `6.0.2` |
| Audit | pass: `npm audit --audit-level=high` reports `found 0 vulnerabilities` |
| Build | pass: `npm run build` |
| Fixture validation | pass: `npm run test` |
| Browser evidence | pass: `npm run test:e2e`; desktop/tablet/mobile projects passed |
| Forbidden wording/action scan | pass: no matches in `frontend\src backend\src hotpath-rs\crates contracts\ui` |

Boundary remains unchanged: this closes dependency security for the P001 frontend slice only. It does not create Account Console runtime truth, Paper readiness, admission, capital allocation or broker tradability.
