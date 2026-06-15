# P003 Phase Plan / 阶段计划

- Proposal ID: `p003-frontend-dependency-security-followup`
- Status: verified
- Updated: 2026-06-13

## Phase 0: Audit Baseline / 审计基线

- Status: completed
- Evidence: `npm audit --audit-level=high` reports high severity `vite -> esbuild` findings on Vite 7.3.5 / esbuild 0.27.7.

## Phase 1: Dependency Upgrade / 依赖升级

- Status: completed
- Target:
  - `vite` to the latest non-vulnerable major available to this environment.
  - `@vitejs/plugin-react` to the compatible latest major.

## Phase 2: Regression Gates / 回归验证

- Status: completed
- Required checks:
  - `npm audit --audit-level=high`
  - `npm run build`
  - `npm run test`
  - `npm run test:e2e`
  - forbidden wording/action scan

## Phase 3: Closeout / 收口

- Status: verified
- Close as:
  - `verified` if all gates pass.
  - `blocked` with typed evidence if upgrade breaks P001 acceptance or audit still fails.

Closeout evidence:

- `npm audit --audit-level=high`: pass, `found 0 vulnerabilities`
- `npm run build`: pass
- `npm run test`: pass
- `npm run test:e2e`: pass for desktop, tablet and mobile
- forbidden wording/action scan: pass
