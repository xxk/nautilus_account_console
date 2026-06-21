# Proposal Templates / Proposal 模板

- Updated: 2026-06-21
- Source: `D:\Nautilus\DSLresearch\docs\proposals\_template`
- Workflow gate: [Account Console Proposal Workflow Stage Contract](../workflows/proposal-gates/README.md)

## Template Entry

| Path | Purpose |
| --- | --- |
| [_template](./_template/) | Copied DSLresearch proposal template: base files, fragments, profiles and metadata. |

## Active Proposals

| Proposal | Status | Purpose |
| --- | --- | --- |
| [P001 Daily Closeout Account Health Panel](./p001-daily-closeout-account-health-panel/README.md) | browser_evidence_verified | First contract-first UI slice for the Daily Closeout workbench; includes [UI design](./p001-daily-closeout-account-health-panel/ui-design.md), [UI acceptance](./p001-daily-closeout-account-health-panel/ui-acceptance.md) and browser evidence. |
| [P002 ADR0044 / ADR0045 / ADR0003 Loop Heartbeat](./p002-adr0044-adr0045-loop-heartbeat/README.md) | p3_account_console_handoff_ready | Read-only heartbeat contract and owner-lane selection; current Account Console handoff has P001 fixture/browser evidence without creating second scheduler/runtime/UI truth. |
| [P003 Frontend Dependency Security Follow-up](./p003-frontend-dependency-security-followup/README.md) | verified | Clears the P001 `vite -> esbuild` high severity audit finding while keeping P001 build, fixture and browser evidence green. |
| [P004 Account Workbench UI Design Gate](./p004-account-workbench-summary-panel/README.md) | phase8_account_workbench_closeout_passed | Proposal-level UI design and acceptance gate for `/accounts/{account_id}` and account drill-down routes; P004 scoped Account Workbench closeout has formal evidence while broader ADR0044/ADR0045 loop and Account Console UI remain outside this claim. |
| [P005 Intraday Monitor Exception Queue Panel](./p005-intraday-monitor-exception-queue-panel/README.md) | phase1_contract_fixture_gate_passed | Proposal-level UI design, acceptance, read-only contract and deterministic fixtures for `/monitor`; browser implementation remains pending and no runtime, stream, account, order, ledger, HFT, readiness, admission, capital or Account Console UI completion truth is created. |
| [P018 IB TWS Read-Only Account Console Landing](./p018-ib-tws-readonly-account-console/README.md) | design_gate_ready | Successor proposal for T001/P011 Phase 8: local TWS / IB Gateway live-account read-only observation through owner source packages, Account Mirror projection and Account Console UI readback; no direct TWS calls, no raw secrets and no broker order actions. |
| [P019 Broker Observation Session Foundation](./p019-broker-observation-session-foundation/README.md) | accepted_with_residual_runtime_blockers | Successor proposal for ADR-0005: broker-generic read-only observation profiles, session conflict policy, Nautilus-compatible order/fill reports, Account Mirror projection, real U3028269 funds/positions parity and residual typed blockers for zero same-slice execution rows. |
| [P020 ADR-0006 Account Console Knowledge Router](./p020-adr0006-account-console-knowledge-router/README.md) | implementation_gate_passed | Successor proposal for ADR-0006: project-local knowledge router, shared/project knowledge split, anti-drift matrix and prevention gate landed for `docs/knowledge/`. |
| [P021 Account Console Owner/Fork Governance](./p021-account-console-owner-fork-governance/README.md) | implementation_gate_passed | Governance proposal for owner ambiguity, fork risk and second-implementation risk found in Account Console route-context, source-package, synthetic-test and frontend-registry lanes. |
| [P022 OpenCTP 19053 Account Console Readback](./p022-openctp-19053-account-console-readback/README.md) | implementation_gate_passed | ADR-0005 child proposal for OpenCTP 7x24 simulation account `acct.ctp.paper.19053`: read-only funds, positions and open-order empty/table display through owner artifacts, source package, Account Mirror and browser evidence. |
| [P023 OpenCTP 19053 Paper Command Capability](./p023-openctp-19053-paper-command-capability/README.md) | paper_runtime_accepted | ADR-0007 successor proposal for OpenCTP 19053 7x24 paper submit/cancel acceptance: intent, risk/approval, command gateway, real readback reconciliation, UI command status and negative gates. |
| [P024 Account Console Paper Command Controls](./p024-account-console-paper-command-controls/README.md) | design_gate_ready | ADR-0007 successor proposal for guarded Web/API paper submit/cancel controls on `acct.ctp.paper.19053`, including partial-fill then cancel Web UI display correctness; no `live_armed` and no Account Mirror writer. |

## Usage Rules

1. Treat `_template/` as a copied starting point, not a finished account-console workflow.
2. Before creating a local proposal, trim DSLresearch-specific research/admission/capital semantics and preserve this repository's read-only account-console boundary.
3. Proposal acceptance evidence must be local to this repository: docs checks, contract tests, Rust/Python/TypeScript checks, typed benchmark artifacts or UI rendering evidence as applicable.
4. Implementation method belongs in proposal/topic documents. ADRs should remain decision records and option comparisons.
5. UI implementation proposals should include panel-level `ui-design.md` and `ui-acceptance.md` before code starts.
6. Run `python scripts\check_proposal_docs.py --root .` before closing proposal-bound documentation or UI design work.
