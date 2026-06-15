# P003 Acceptance / 验收

- Proposal ID: `p003-frontend-dependency-security-followup`
- Status: verified
- Updated: 2026-06-13

## 1. Positive Acceptance / 正向验收

| ID | Acceptance | Evidence |
| --- | --- | --- |
| P003-POS-01 | high severity Vite/esbuild audit finding is cleared | `npm audit --audit-level=high` |
| P003-POS-02 | P001 frontend build remains valid | `npm run build` |
| P003-POS-03 | P001 fixture contract validation remains valid | `npm run test` |
| P003-POS-04 | P001 browser evidence remains valid on desktop/tablet/mobile | `npm run test:e2e` |
| P003-POS-05 | dependency upgrade does not introduce forbidden UI/action claims | forbidden wording/action scan |

## 2. Negative Acceptance / 反向验收

| ID | Must fail if |
| --- | --- |
| P003-NEG-01 | dependency security closure is claimed while `npm audit --audit-level=high` still fails |
| P003-NEG-02 | P001 browser evidence is skipped after dependency upgrade |
| P003-NEG-03 | upgrade changes runtime/account/broker/admission/capital truth |
| P003-NEG-04 | upgrade requires a second frontend runtime or second artifact truth |

## 3. Evidence / 证据

| Check | Result |
| --- | --- |
| `npm audit --audit-level=high` | pass: `found 0 vulnerabilities` |
| `npm run build` | pass |
| `npm run test` | pass |
| `npm run test:e2e` | pass: desktop/tablet/mobile |
| forbidden wording/action scan | pass: no matches in `frontend\src backend\src hotpath-rs\crates contracts\ui` |

Dependency versions:

| Package | Version |
| --- | --- |
| `vite` | `8.0.16` |
| `@vitejs/plugin-react` | `6.0.2` |

Boundary statement:

P003 verifies frontend dependency security for the P001 UI slice only. It does not verify Account Console runtime truth, Paper readiness, Live readiness, admission, capital allocation or broker tradability.
