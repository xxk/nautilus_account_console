# P002: ADR0044 / ADR0045 / Account Console ADR0003 Loop Heartbeat

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p077_fill_producing_acceptance_deferred
- Updated: 2026-06-14
- Owner: account-console-governance
- Work item type: tracer / heartbeat governance
- Scope: P0 conflict analysis before opening any implementation loop
- Strategy ADR anchors:
  - `D:/Nautilus/nautilus_strategies/docs/adr/0044-adopt-real-feed-sandbox-paper-as-default-paper-route.md`
  - `D:/Nautilus/nautilus_strategies/docs/adr/0045-adopt-event-driven-universal-account-console.md`
- Account Console ADR anchor:
  - [ADR-0003 contract-first UI slice development](../../adr/0003-adopt-contract-first-ui-slice-development.md)
- Existing strategy loop anchor:
  - `D:/Nautilus/nautilus_strategies/docs/proposals/p077-p076-timed-paper-loop-workflow/`
- Existing ADR0044 foundation anchor:
  - `D:/Nautilus/nautilus_strategies/docs/proposals/p078-ADR0044-real-feed-sandbox-paper-foundation/`

## 1. Purpose / 目的

Open a controlled Loop Heartbeat entry to push ADR-0044, ADR-0045 and Account Console ADR-0003 toward implementation without creating a second runtime, second scheduler, second ledger truth or second UI truth.

P0 is conflict analysis only. It answers:

```text
Can a heartbeat safely coordinate ADR0044 -> ADR0045 -> Account Console ADR0003 landing,
or does it conflict with existing P077/P078/account-console boundaries?
```

## 2. P0 Decision / P0 判断

P0 result:

```text
conditional_go
```

The heartbeat can proceed only as a read-only governance heartbeat that reuses existing owner lanes:

1. P077 remains the strategy-side timed loop / scheduler workflow owner.
2. P078 remains the ADR-0044 A0-A3 foundation delivery lane.
3. Account Console P001 and successors remain the ADR-0045 / ADR-0003 UI slice delivery lane.
4. This P002 heartbeat must not become runtime truth, account truth, order truth, UI truth, scheduler truth or proposal closeout truth.

## 3. Non-Goals / 非目标

P002 P0 does not:

1. Start a new automation daemon or recurring scheduler.
2. Replace P077 heartbeat/checkpoint/lock/resume semantics.
3. Implement ADR-0044 A0-A3 foundation work.
4. Implement Account Console UI code.
5. Claim ADR-0044, ADR-0045 or ADR-0003 complete.
6. Claim Paper readiness, Live readiness, admission, production readiness, capital allocation or tradability.

## 4. Heartbeat Model / 心跳模型

Allowed heartbeat behavior:

```text
read current owner state
  -> detect conflicts/blockers
  -> select one next owner lane
  -> if blocked, first try owner-side repair inside the named owner repo
  -> write a governance recommendation, typed owner artifact or typed blocker
  -> yield this heartbeat turn; continue the loop on the next heartbeat unless termination criteria are met
```

Forbidden heartbeat behavior:

```text
run sustained daemon
write runtime/account/order/fill/settlement truth
write UI readiness truth
skip P078 A0-A3 foundation evidence
skip account-console contract/fixture/UI acceptance
close owner work from heartbeat evidence
terminate the loop while ADR0044/ADR0045/sibling owner tasks remain incomplete
```

## 4.1 Blocker Handling And Loop Termination / 阻塞处理与 Loop 终止

Blocked is not a default terminal state for the loop. When a heartbeat observes a typed blocker, it must first decide whether the blocker can be handled inside an owned repository boundary:

1. If the blocker names `nautilus_strategies`, `nautilus_account_console`, `nautilus_ctp_adapter` or another available sibling owner, enter that owner repo, make the smallest safe owner-side repair, run that repo's lightweight gates, and return a typed pass artifact or typed blocker.
2. If the blocker names an unavailable external resource, market window, credential, endpoint permission, broker account approval, capital/admission approval or unsafe order action, record a typed blocker with retry conditions and keep the loop alive for the next heartbeat.
3. The loop must not convert a blocker into pass evidence from route config, stdout, logs, screenshots, latest/debug paths, UI/browser/process/window state or DB rows without owner checksum.

The loop terminates only when all scoped ADR0044/ADR0045 and sibling repo tasks selected by the loop have formal owner acceptance evidence and no active typed blockers remain. Coordination evidence alone cannot terminate the loop.

## 5. P0 Artifacts / P0 产物

| File | Purpose |
| --- | --- |
| [p0-conflict-analysis.md](./p0-conflict-analysis.md) | conflict analysis and resolution rules |
| [heartbeat-contract.md](./heartbeat-contract.md) | read-only heartbeat row contract, lane selection rule and first landed heartbeat row |
| [lane-selection.md](./lane-selection.md) | first lane selection and entry/exit contract for the next owner lane |
| [phase-plan.md](./phase-plan.md) | P0 -> P1 heartbeat phase plan |
| [acceptance.md](./acceptance.md) | P0 acceptance and anti-drift gates |

## 5.1 Current Landing / 当前落地

P1 heartbeat contract has landed. P078 A0-A3, P001 and P003 local lanes are now closed for their scoped evidence.

Current selected next owner lane:

```text
p077_fill_producing_acceptance_deferred
```

Current selected blocker target:

```text
p077-t6-fill-producing-acceptance-deferral
```

This selection is a governance recommendation only. The required CTP owner returned a typed market freshness pass for `rb2610`, then the guarded Paper lifecycle runner attempted one authorized Paper order: `rb2610 BUY OPEN 3 @ 3158`, client order id `p077-t6-rb2610-buy3-061440`. Lifecycle was `rejected`, `fill_volume=0`, no open order existed to cancel, and post-snapshot reconcile recorded `rejected_reconciled`. Reconcile artifact checksum: `sha256:3a43c8ef82f11bca5707873f01b1ace16a87d222a6cf115cc1a7eda684e6d196`. Rejected-order diagnosis checksum: `sha256:2c9c0bdd0f34684806c5e5e9d39dd1ff4706025b1508a6fe138b0837d4d1e96f`. No-fill closeout artifact checksum: `sha256:f96d944ca06cf8fd5fb38143cf48cb66ab074baaebfe358620f42cee5aa3e544`; it closes only the current guarded attempt and does not authorize retry. Callback decode repair artifact checksum: `sha256:908a86bf4dfaf36d0cc507294522332a5af747acd4c3a4ad67fdba1ed501ab1c`; it records TD/MD native callback GB18030 decode repair and focused gate `44 passed`, but does not reinterpret the previous rejected order or authorize retry. Controlled retry preflight blocker artifact: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T070007/p077_t6_controlled_retry_preflight_blocker.json`, checksum `sha256:26b8edd710bebefeadc0321174b8102381f66bb82a99d8b952b978319174e642`; market/snapshot passed, but dry-run `rb2610 BUY OPEN 3 @ 3158` was blocked before native send by `max_net_position_exceeded` with `current_rb2610_long_qty=5`, `projected_net_position=8`, `max_net_position=5`, `paper_send_armed=false`, `submit_attempted=false`. Exposure-reduction candidate artifact: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T071038/p077_t6_exposure_reduction_candidate_preflight.json`, checksum `sha256:d7a3ed4bfb07f2f0a6856c503c69f6e5c3f3a7b44cc6d965cd49d1d89fb3dbf1`; no-send `rb2610 SELL CLOSETODAY 1 @ 3158` candidate dry-run passed with projected net position 4, but it does not authorize paper send. P077 T6 remains incomplete until a separately accepted exposure-reduction send lane, updated risk-bounded retry target, or risk-guard owner update is followed by fresh preflight.

Fresh candidate update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T072211/p077_t6_fresh_exposure_reduction_candidate_preflight.json`, checksum `sha256:d1ccc7dd7242e0c3679862c04edfa36a877eb6baf5475c58ae1057e2b8587396`, refreshes market/snapshot evidence and records no-send `rb2610 SELL CLOSETODAY 1 @ 3161` with projected net position 4; it still does not authorize paper send.

Armed boundary update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T073242/p077_t6_exposure_reduction_send_blocked_by_kill_switch.json`, checksum `sha256:3d3b2e55672e1901335ad8b9b4ba6550ebd09bcb21d1fc7ed4a828f4d56fbf8a`, records `kill_switch_closed` because `AllowLiveOrderSmoke=false`; no native send occurred.

Guardrail repair update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T074014/p077_t6_exposure_reduction_guardrail_code_repair_no_send.json`, checksum `sha256:b57ad627c0b04c9381896fe6e52d4b7cd7f1ad4e791fed50c3efb19ad9ac8e4a`, records a default-off exposure-reduction-only Paper smoke code repair. It does not change Account Console truth, does not authorize UI action controls, and does not create runtime/order/fill/read-model truth.

Config authorization update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T075344/p077_t6_exposure_reduction_local_config_authorized_no_send.json`, checksum `sha256:57bd11de903d6b245611cec73cec49db803105813de065d597a19fd0b7e93a10`, records local gitignored Paper config authorization for exposure-reduction-only smoke while keeping general live order smoke disabled. It still does not create Account Console runtime truth.

Fresh authorized no-send preflight update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T080157/p077_t6_fresh_exposure_reduction_authorized_preflight_no_send.json`, checksum `sha256:5865bd05aff7e9f258f38619acfb18f368d972acdcc25662c1c70b257f0f291d`, records fresh CTP owner market/snapshot evidence plus dry-run `rb2610 SELL CLOSETODAY 1 @ 3162`; `paper_send_armed=false`, `submit_attempted=false`, and no post-snapshot/reconcile truth exists. It still does not create Account Console runtime truth.

Armed exposure-reduction update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_armed_exposure_reduction_boundary_cancelled_reconciled.json`, checksum `sha256:c78b5cc40ea5ab149a06b93bfe07a64c8548e357287d34eab9c40bf0593d4af3`, records one guarded `rb2610 SELL CLOSETODAY 1 @ 3162`, lifecycle `cancelled`, fill `0`, post snapshot and `cancelled_reconciled` target delta `0`. It still does not create Account Console runtime truth or readiness/admission/capital/tradability truth.

Cancelled exposure-reduction diagnosis update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_diagnosis.json`, checksum `sha256:b26d215c8bc3f128031e6db85ffa4f7ab35fcf0705bf9a55713938ebfa1eddba`, classifies the lifecycle status `53` as cancelled/no-fill and leaves broker semantic reason undetermined because callback error text is mojibake. It still does not create Account Console runtime truth or readiness/admission/capital/tradability truth.

Cancelled exposure-reduction no-fill closeout update: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json`, checksum `sha256:e8fb94cc4239582254c57c1be02369610663e523853c546581e639f18bfe6977`, accepts no-fill closeout for the current guarded exposure-reduction attempt only. It does not authorize retry, does not create Account Console runtime/read-model truth, and does not create readiness/admission/capital/tradability truth. This closeout is now followed by the P077 typed deferral artifact.

Fill-producing acceptance deferral update: `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json`, checksum `sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e`, records a P077 owner typed deferral because no separately accepted safer retry lane or fill-producing lifecycle artifact exists. It does not authorize retry, does not create Account Console runtime/read-model truth, and does not create readiness/admission/capital/tradability truth.

P002 must not synthesize this evidence from Account Console UI, screenshots, route config, stdout/log text, latest/debug paths, process/window state, browser state or DB rows without owner checksum, and must not treat a request envelope as order result truth.

Handoff evidence:

| Evidence | Ref |
| --- | --- |
| ADR-0044 P078 closeout summary | `D:/Nautilus/nautilus_strategies/output/adr0044/foundation_closeout/p078_foundation_closeout_evidence_summary.json` |
| closeout checksum | `7f3f9b310d5f2703f17398f5bedaad2c7f9d015dc33fdabc159c67560a7bf6a1` |
| Account Console read-model fixture | `contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json` |
| P001 browser evidence | `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/` |
| P003 dependency security closeout | `docs/proposals/p003-frontend-dependency-security-followup/acceptance.md` |
| CTP owner artifact | `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-market-freshness/p077_t6_ctp_market_freshness_20260613T194429Z.json` |
| Sandbox account/position query artifact | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/account_position_query/account-position-query-19054.json` |
| Controlled order request envelope | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/controlled_order_request/p077-t6-controlled-order-request-rb-buy-3-001.json` |
| Submit/status/cancel lifecycle blocker | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/submit_status_cancel_lifecycle/p077-t6-submit-status-cancel-lifecycle-unsafe-action-blocker.json` |
| Safe lifecycle owner contract | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/safe_lifecycle_contract/p077-t6-safe-lifecycle-owner-contract.json` |
| Operator authorization wait blocker | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/operator_authorization_wait/p077-t6-operator-authorization-required-blocker.json` |
| Guarded Paper lifecycle reconcile | `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_reconcile_rejected_order.json` |
| Rejected-order diagnosis | `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_rejected_order_diagnosis.json` |
| Cancelled exposure-reduction no-fill closeout | `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json` |
| Fill-producing acceptance deferral | `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json` |
| No-fill closeout | `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_no_fill_closeout.json` |

## 6. P0 Exit / P0 出口

P0 exits as `conditional_go` when:

1. All known conflicts have explicit resolution rules.
2. P002 is confirmed not to replace P077 or P078.
3. Account Console ADR-0003 remains UI delivery decomposition only.
4. Any implementation heartbeat after P0 must pick exactly one next owner lane.

P0 exits as `blocked` if:

1. The heartbeat needs a new scheduler or persistent daemon.
2. The heartbeat needs to write runtime, account, order or UI truth.
3. The heartbeat tries to claim ADR0044/ADR0045/ADR0003 completion from coordination evidence.
