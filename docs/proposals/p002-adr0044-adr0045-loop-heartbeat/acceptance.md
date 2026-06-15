# P002 Acceptance / 验收

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p077_fill_producing_acceptance_deferred
- Updated: 2026-06-14

## 1. Acceptance Boundary / 验收边界

P002 accepts P0 conflict analysis, P1 heartbeat contract landing, P078-first owner lane selection and the post-P078 Account Console handoff lane selection only.

P002 does not accept:

1. ADR-0044 implementation completion.
2. ADR-0045 implementation completion.
3. Account Console ADR-0003 implementation completion.
4. P077 workflow completion.
5. P078 A0-A3 completion.
6. Paper readiness, Live readiness, admission, production readiness, capital allocation or tradability.

## 2. Positive Acceptance / 正向验收

| ID | Must pass | Evidence |
| --- | --- | --- |
| P002-P0-01 | P0 conflict analysis exists and names known conflicts | [p0-conflict-analysis.md](./p0-conflict-analysis.md) |
| P002-P0-02 | P077 remains the only scheduler/checkpoint/lock/resume owner | owner map and conflict matrix |
| P002-P0-03 | P078 remains the ADR-0044 A0-A3 foundation lane | owner map and P0-C4 |
| P002-P0-04 | Account Console ADR-0003 remains UI slice decomposition only | owner map and P0-C8 |
| P002-P0-05 | P0 exit is `conditional_go`, not implementation pass | README and P0 verdict |
| P002-P0-06 | P1 cannot run more than one owner lane per heartbeat | phase plan and P1 recommended shape |
| P002-P1-01 | heartbeat row contract exists | [heartbeat-contract.md](./heartbeat-contract.md) |
| P002-P1-02 | exactly-one-lane-per-heartbeat rule exists | heartbeat contract |
| P002-P1-03 | first heartbeat row selects `p078_a0_a3_foundation` | heartbeat contract |
| P002-P1-04 | blocker handling rule requires owner-side repair before treating a blocker as wait-only | [heartbeat-contract.md](./heartbeat-contract.md) |
| P002-P1-05 | loop termination requires all scoped ADR0044/ADR0045 and sibling repo tasks complete with no active blockers | [heartbeat-contract.md](./heartbeat-contract.md) |
| P002-P2-01 | first selected child target is `adr0044-a0-official-matching-baseline` | [lane-selection.md](./lane-selection.md) |
| P002-P2-02 | deferred UI lane is recorded until P078 source contract/fixture/blocker exists | lane selection |
| P002-P3-01 | P078 A0-A3 foundation closeout allows selecting `account_console_contract_fixture_ui_slice` | `D:/Nautilus/nautilus_strategies/output/adr0044/foundation_closeout/p078_foundation_closeout_evidence_summary.json` |
| P002-P3-02 | Account Console handoff fixture exists without writing runtime/UI truth | `contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json` |
| P002-P3-03 | Browser UI evidence blocker was explicitly recorded and then resolved with a portable Node/npm runner | `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/2026-06-13-browser-runner-blocker.md` |
| P002-P3-04 | P001 browser evidence exists for desktop, tablet and mobile without becoming runtime/UI truth | `docs/acceptance/browser-evidence/p001-daily-closeout-account-health-panel/*-{happy,adr0044-source-backed,blocked,stale,empty,partial}.png` |
| P002-P3-05 | P001 frontend dependency security follow-up is closed without changing Account Console truth boundaries | `docs/proposals/p003-frontend-dependency-security-followup/acceptance.md` |
| P002-P3-06 | After P001/P003 local lanes close, current selected lane becomes `wait_market_freshness_retry` for CTP market freshness | [lane-selection.md](./lane-selection.md) |
| P002-P3-07 | CTP owner returned a pass artifact for `rb2610`, so the loop can return to P077 owner stages while Account Console remains projection-only | latest artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-market-freshness/p077_t6_ctp_market_freshness_20260613T194429Z.json`; checksum `sha256:dfbe8bef811104eaec39995cc91f1243dffee36c8f5b30799a85a3e464935265`; warning `first_tick_exchange_timestamp_stale` |
| P002-P3-08 | P077 returned a sandbox account/position query owner artifact for `19054`, so the loop can advance to the next P077 owner stage while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/account_position_query/account-position-query-19054.json`; checksum `sha256:c4e2970786ef97ed8ef4d5ba978bfa1667b650d7b730d720ef0cbae434d10f5d`; `dispatches_runtime=false` |
| P002-P3-09 | P077 returned a controlled order request envelope, so the loop can advance to lifecycle evidence or typed unsafe-action blocker while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/controlled_order_request/p077-t6-controlled-order-request-rb-buy-3-001.json`; checksum `sha256:c77ffa9f7a464d03a7c35b3111cef476476f59c3d4d7c63623a7ba7a1220caaf`; `dispatch_authorized=false`; `result_claimed=false` |
| P002-P3-10 | P077 returned a submit/status/cancel lifecycle typed unsafe-action blocker, so the loop must wait for a safe lifecycle owner contract while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/submit_status_cancel_lifecycle/p077-t6-submit-status-cancel-lifecycle-unsafe-action-blocker.json`; checksum `sha256:7f9f8263b2a01f3539bb5624da80e9af13958ef67136f87872c29c8701996631`; source request checksum `sha256:c77ffa9f7a464d03a7c35b3111cef476476f59c3d4d7c63623a7ba7a1220caaf`; `dispatches_runtime=false`; `submit_attempted=false`; `cancel_request_emitted=false`; `result_claimed=false` |
| P002-P3-11 | P077 returned a safe lifecycle owner contract, so the loop must wait for operator authorization and sandbox-only lifecycle runner evidence while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/safe_lifecycle_contract/p077-t6-safe-lifecycle-owner-contract.json`; checksum `sha256:4f67dc74640f29df9134369f623e33cb868ea9025c89cac92f9c549ff04a682c`; `runtime_dispatch_allowed_by_contract=false`; `operator_authorization_required=true`; `dispatches_runtime=false`; `result_claimed=false` |
| P002-P3-12 | P077 returned an operator authorization wait blocker, so the loop must remain wait-only until explicit operator authorization plus sandbox-only lifecycle runner evidence exists | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/operator_authorization_wait/p077-t6-operator-authorization-required-blocker.json`; checksum `sha256:e7dfa994202946337b4a57fe2250b601e7b6dca534107ac1ee1dc4bc9fac9fcd`; source contract checksum `sha256:4f67dc74640f29df9134369f623e33cb868ea9025c89cac92f9c549ff04a682c`; `operator_authorization_present=false`; `sandbox_lifecycle_runner_present=false`; `dispatches_runtime=false`; `result_claimed=false` |
| P002-P3-13 | After explicit Paper-account operator authorization, the CTP owner returned guarded lifecycle reconcile evidence for a rejected/no-fill order, so the loop can move from authorization wait to rejected-order diagnosis or no-fill closeout while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_reconcile_rejected_order.json`; checksum `sha256:3a43c8ef82f11bca5707873f01b1ace16a87d222a6cf115cc1a7eda684e6d196`; `client_order_id=p077-t6-rb2610-buy3-061440`; `order_lifecycle_disposition=rejected`; `fill_volume=0`; `cancel_required=false`; `reconciliation.disposition=rejected_reconciled`; no readiness/admission/capital/tradability claim |
| P002-P3-14 | CTP owner returned rejected-order diagnosis evidence, so the loop can move to accepted no-fill closeout/follow-up or callback decode/status repair before retry while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_rejected_order_diagnosis.json`; checksum `sha256:2c9c0bdd0f34684806c5e5e9d39dd1ff4706025b1508a6fe138b0837d4d1e96f`; `diagnosis_disposition=classified_rejected_from_callback_error_message`; semantic rejection reason remains undetermined until native callback text/status decoding is repaired |
| P002-P3-15 | CTP owner returned no-fill closeout evidence for the current guarded attempt, so retry remains blocked on callback text/status decoding repair or a split follow-up while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_no_fill_closeout.json`; checksum `sha256:f96d944ca06cf8fd5fb38143cf48cb66ab074baaebfe358620f42cee5aa3e544`; `closeout_decision=accepted_no_fill_closeout_for_current_guarded_attempt`; `retry_authorized_by_this_artifact=false`; readiness claims remain false |
| P002-P3-16 | CTP owner returned callback decode repair evidence, so the loop can move to a fresh controlled retry preflight/lifecycle lane or split a retry-deferral follow-up while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_callback_decode_repair.json`; checksum `sha256:908a86bf4dfaf36d0cc507294522332a5af747acd4c3a4ad67fdba1ed501ab1c`; TD/MD ctypes share GB18030 fallback decode helper; focused CTP gate returned `44 passed`; `retry_authorized_by_this_artifact=false`; readiness claims remain false |
| P002-P3-17 | CTP owner returned a controlled retry preflight blocker, so the loop must not retry until a smaller risk-bounded order, exposure-reduction lane or risk-guard owner update exists while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T070007/p077_t6_controlled_retry_preflight_blocker.json`; checksum `sha256:26b8edd710bebefeadc0321174b8102381f66bb82a99d8b952b978319174e642`; `blocker_reason=max_net_position_exceeded`; `current_rb2610_long_qty=5`; `projected_net_position=8`; `max_net_position=5`; `paper_send_armed=false`; `submit_attempted=false`; readiness claims remain false |
| P002-P3-18 | CTP owner returned a no-send exposure-reduction candidate preflight, so the loop has a typed candidate but must not send until a separate accepted lane or updated retry target exists while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T071038/p077_t6_exposure_reduction_candidate_preflight.json`; checksum `sha256:d7a3ed4bfb07f2f0a6856c503c69f6e5c3f3a7b44cc6d965cd49d1d89fb3dbf1`; dry-run checksum `sha256:90ad3fa0e6d25b2c550aaf607bb8148adccb6744e8e896ff129215ee81d9d70c`; candidate `rb2610 SELL CLOSETODAY 1 @ 3158`; projected net position 4; `paper_send_armed=false`; `submit_attempted=false`; readiness claims remain false |
| P002-P3-19 | CTP owner returned a fresh no-send exposure-reduction candidate preflight, so the loop has current typed candidate evidence but must not send until a separate accepted lane or updated retry target exists while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T072211/p077_t6_fresh_exposure_reduction_candidate_preflight.json`; checksum `sha256:d1ccc7dd7242e0c3679862c04edfa36a877eb6baf5475c58ae1057e2b8587396`; fresh market checksum `sha256:52ee76db3e7cbd2d7948b666d0693bf50885bd83e74034197050da642d5d5cc4`; fresh snapshot checksum `sha256:2ed9dce04421de4ff107a1545a75379e96a86a6b124c36a5b6907727aa147be5`; fresh dry-run checksum `sha256:09a0b710b937c7c46834011e9b0bbd00ab10b55b2bf696ecd752b0347903411a`; candidate `rb2610 SELL CLOSETODAY 1 @ 3161`; projected net position 4; `paper_send_armed=false`; `submit_attempted=false`; readiness claims remain false |
| P002-P3-20 | CTP owner returned an armed-boundary kill-switch blocker, so the loop must not bypass `AllowLiveOrderSmoke=false` while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T073242/p077_t6_exposure_reduction_send_blocked_by_kill_switch.json`; checksum `sha256:3d3b2e55672e1901335ad8b9b4ba6550ebd09bcb21d1fc7ed4a828f4d56fbf8a`; boundary checksum `sha256:a6cff105436565e35fcd00d4b265eb7261735b2049a8b5956b28315af95eddc5`; blocker reason `kill_switch_closed`; `AllowLiveOrderSmoke=false`; `native_send_allowed=false`; `submit_attempted=false`; readiness claims remain false |
| P002-P3-21 | CTP owner returned a default-off exposure-reduction guardrail code repair, so the loop can proceed only after explicit config authorization and fresh typed preflight while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T074014/p077_t6_exposure_reduction_guardrail_code_repair_no_send.json`; checksum `sha256:b57ad627c0b04c9381896fe6e52d4b7cd7f1ad4e791fed50c3efb19ad9ac8e4a`; focused gates `56 passed` and `15 passed`; `paper_send_attempted=false`; `native_send_attempted=false`; readiness claims remain false |
| P002-P3-22 | CTP owner returned local exposure-reduction config authorization, so the loop can proceed only through fresh typed market/snapshot/order preflight while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T075344/p077_t6_exposure_reduction_local_config_authorized_no_send.json`; checksum `sha256:57bd11de903d6b245611cec73cec49db803105813de065d597a19fd0b7e93a10`; `allow_live_order_smoke=false`; `allow_exposure_reduction_order_smoke=true`; focused gate `56 passed`; `paper_send_attempted=false`; `native_send_attempted=false`; readiness claims remain false |
| P002-P3-23 | CTP owner returned fresh authorized no-send exposure-reduction preflight, so the loop can proceed only to a fresh armed boundary plus post-snapshot/reconcile if send occurs while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T080157/p077_t6_fresh_exposure_reduction_authorized_preflight_no_send.json`; checksum `sha256:5865bd05aff7e9f258f38619acfb18f368d972acdcc25662c1c70b257f0f291d`; dry-run `rb2610 SELL CLOSETODAY 1 @ 3162`; projected net position 4; `paper_send_armed=false`; `submit_attempted=false`; CTP focused gate `59 passed`; no post-snapshot/reconcile truth; readiness claims remain false |
| P002-P3-24 | CTP owner returned an armed exposure-reduction boundary with post-snapshot reconcile, so the loop can move to cancelled-attempt diagnosis/typed deferral while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_armed_exposure_reduction_boundary_cancelled_reconciled.json`; checksum `sha256:c78b5cc40ea5ab149a06b93bfe07a64c8548e357287d34eab9c40bf0593d4af3`; `client_order_id=p077-t6-rb2610-close1-armed-20260614T082239`; lifecycle `cancelled`; `fill_volume=0`; `reconciliation.disposition=cancelled_reconciled`; target position delta `0`; Account Console creates no runtime/read-model truth; readiness claims remain false |
| P002-P3-25 | CTP owner returned cancelled-attempt diagnosis, so the loop can move to typed deferral/no-fill closeout or a separately accepted safer retry lane while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_diagnosis.json`; checksum `sha256:b26d215c8bc3f128031e6db85ffa4f7ab35fcf0705bf9a55713938ebfa1eddba`; `diagnosis_disposition=classified_cancelled_from_ctp_status_53_no_fill`; semantic cancel reason is undetermined because callback error text is mojibake; Account Console creates no runtime/read-model truth; readiness claims remain false |
| P002-P3-26 | CTP owner returned no-fill closeout for the cancelled exposure-reduction attempt, so the loop can only proceed via separately accepted safer retry or typed deferral while Account Console remains projection-only | artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json`; checksum `sha256:e8fb94cc4239582254c57c1be02369610663e523853c546581e639f18bfe6977`; `closeout_decision=accepted_no_fill_closeout_for_cancelled_exposure_reduction_attempt`; `retry_authorized_by_this_artifact=false`; Account Console creates no runtime/read-model truth; readiness claims remain false |
| P002-P3-27 | P077 owner returned typed deferral for fill-producing acceptance, so Account Console must keep projection-only state and require a separately accepted safer retry lane before any fill-producing claim | artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json`; checksum `sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e`; `fill_producing_acceptance_satisfied=false`; `retry_authorized_by_this_artifact=false`; Account Console creates no runtime/read-model truth; readiness claims remain false |

## 3. Negative Acceptance / 反向验收

| ID | Must fail if |
| --- | --- |
| P002-NEG-01 | P002 starts a new recurring scheduler, daemon, lock or checkpoint system |
| P002-NEG-02 | P002 writes runtime/account/order/fill/settlement artifacts |
| P002-NEG-03 | P002 accepts UI screenshots, DB rows, stdout, latest/debug paths or report HTML as owner truth |
| P002-NEG-04 | P002 declares ADR0044, ADR0045 or ADR0003 complete from coordination evidence |
| P002-NEG-05 | P002 bypasses P078 A0-A3 foundation for real-feed/high-fidelity Paper claims |
| P002-NEG-06 | P002 bypasses Account Console contract/fixture/UI acceptance for UI claims |
| P002-NEG-07 | P002 mixes Nautilus sandbox account alias `19054` with CTP/broker-paper account truth |
| P002-NEG-08 | P002 selects more than one owner lane in one heartbeat |
| P002-NEG-09 | P002 treats lane selection as P078 child implementation evidence |
| P002-NEG-10 | P002 starts Account Console data panel implementation before source contract, fixture or typed blocker exists |
| P002-NEG-11 | P002 terminates the loop because a blocker exists while owner-side repair or retry remains possible |
| P002-NEG-12 | P002 marks the loop complete before all selected ADR0044/ADR0045 and sibling repo tasks have formal owner acceptance evidence |

## 4. P0 Conflict Checklist / P0 冲突清单

| Conflict | Resolution required before P1 |
| --- | --- |
| P077 vs P002 heartbeat | P002 is read-only governance; P077 remains scheduler |
| P078 foundation vs Account Console UI | UI shell may proceed; data-backed account panels need typed artifacts or blockers |
| ADR-0045 legacy `/accounts` route vs Account Console workbench routes | local account_console route coverage matrix governs product navigation |
| P077 `19054` visibility vs broker-paper aliasing | keep Nautilus sandbox `19054` source refs/checksums distinct |
| "全部落地" wording | only owner child acceptance can claim implementation completion |

## 5. Required Checks / 必跑检查

Minimum repo checks after P3 handoff fixture changes:

```powershell
python -m compileall backend\src
cargo test --manifest-path hotpath-rs\Cargo.toml
node frontend\scripts\validate-account-health-fixtures.mjs
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order|latest/debug|raw report.*truth|runtime truth|capital truth" frontend\src backend\src hotpath-rs\crates contracts\ui
```

Environment fallback:

If local `node` or `npm` is unavailable, the same validator may be executed through the Codex Node REPL by importing `frontend/scripts/validate-account-health-fixtures.mjs`. This is an execution-environment workaround only; it must not change the validator logic or become a second UI truth.

## 6. P0 Closeout Verdict / P0 收口结论

```text
verdict: conditional_go
next_allowed_step: open a separately accepted safer retry lane for fill-producing acceptance, or keep typed deferral active; Account Console data-backed panels still wait for typed runtime/account/order/read-model artifacts
current_landing:
  heartbeat_contract: landed
  lane_selection: p077_fill_producing_acceptance_deferred
  first_child_target: p077-t6-fill-producing-acceptance-deferral
  source_backed_fixture: contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json
  external_owner_required: owner://ctp_market_owner
  external_owner_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-market-freshness/p077_t6_ctp_market_freshness_20260613T194429Z.json
  external_owner_checksum: sha256:dfbe8bef811104eaec39995cc91f1243dffee36c8f5b30799a85a3e464935265
  external_owner_status: passed
  external_owner_freshness_basis: received_at
  external_owner_warning: first_tick_exchange_timestamp_stale
  sandbox_account_position_query_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/account_position_query/account-position-query-19054.json
  sandbox_account_position_query_checksum: sha256:c4e2970786ef97ed8ef4d5ba978bfa1667b650d7b730d720ef0cbae434d10f5d
  sandbox_account_position_query_status: passed_read_only_owner_artifact
  controlled_order_request_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/controlled_order_request/p077-t6-controlled-order-request-rb-buy-3-001.json
  controlled_order_request_checksum: sha256:c77ffa9f7a464d03a7c35b3111cef476476f59c3d4d7c63623a7ba7a1220caaf
  controlled_order_request_status: passed_request_only_no_submit
  submit_status_cancel_lifecycle_blocker_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/submit_status_cancel_lifecycle/p077-t6-submit-status-cancel-lifecycle-unsafe-action-blocker.json
  submit_status_cancel_lifecycle_blocker_checksum: sha256:7f9f8263b2a01f3539bb5624da80e9af13958ef67136f87872c29c8701996631
  submit_status_cancel_lifecycle_blocker_status: typed_unsafe_action_blocker_no_submit_status_cancel
  safe_lifecycle_owner_contract_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/safe_lifecycle_contract/p077-t6-safe-lifecycle-owner-contract.json
  safe_lifecycle_owner_contract_checksum: sha256:4f67dc74640f29df9134369f623e33cb868ea9025c89cac92f9c549ff04a682c
  safe_lifecycle_owner_contract_status: contract_recorded_operator_authorization_required_no_runtime_dispatch
  operator_authorization_wait_blocker_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/operator_authorization_wait/p077-t6-operator-authorization-required-blocker.json
  operator_authorization_wait_blocker_checksum: sha256:e7dfa994202946337b4a57fe2250b601e7b6dca534107ac1ee1dc4bc9fac9fcd
  operator_authorization_wait_blocker_status: historical_wait_boundary_superseded_by_operator_authorized_guarded_runner
  guarded_lifecycle_reconcile_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_reconcile_rejected_order.json
  guarded_lifecycle_reconcile_checksum: sha256:3a43c8ef82f11bca5707873f01b1ace16a87d222a6cf115cc1a7eda684e6d196
  guarded_lifecycle_reconcile_status: rejected_reconciled_no_fill_no_cancel_required
  guarded_lifecycle_client_order_id: p077-t6-rb2610-buy3-061440
  rejected_order_diagnosis_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_rejected_order_diagnosis.json
  rejected_order_diagnosis_checksum: sha256:2c9c0bdd0f34684806c5e5e9d39dd1ff4706025b1508a6fe138b0837d4d1e96f
  rejected_order_diagnosis_status: classified_rejected_from_callback_error_message_semantic_reason_undetermined
  no_fill_closeout_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_no_fill_closeout.json
  no_fill_closeout_checksum: sha256:f96d944ca06cf8fd5fb38143cf48cb66ab074baaebfe358620f42cee5aa3e544
  no_fill_closeout_status: accepted_no_fill_closeout_for_current_guarded_attempt_no_retry_authorized
  callback_decode_repair_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_callback_decode_repair.json
  callback_decode_repair_checksum: sha256:908a86bf4dfaf36d0cc507294522332a5af747acd4c3a4ad67fdba1ed501ab1c
  callback_decode_repair_status: native_td_md_gb18030_decode_repair_recorded_no_retry_authorized
  controlled_retry_preflight_blocker_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T070007/p077_t6_controlled_retry_preflight_blocker.json
  controlled_retry_preflight_blocker_checksum: sha256:26b8edd710bebefeadc0321174b8102381f66bb82a99d8b952b978319174e642
  controlled_retry_preflight_blocker_status: blocked_max_net_position_no_send
  exposure_reduction_candidate_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T071038/p077_t6_exposure_reduction_candidate_preflight.json
  exposure_reduction_candidate_checksum: sha256:d7a3ed4bfb07f2f0a6856c503c69f6e5c3f3a7b44cc6d965cd49d1d89fb3dbf1
  exposure_reduction_candidate_status: candidate_passed_no_send
  fresh_exposure_reduction_candidate_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T072211/p077_t6_fresh_exposure_reduction_candidate_preflight.json
  fresh_exposure_reduction_candidate_checksum: sha256:d1ccc7dd7242e0c3679862c04edfa36a877eb6baf5475c58ae1057e2b8587396
  fresh_exposure_reduction_candidate_status: fresh_candidate_passed_no_send
  exposure_reduction_send_blocker_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T073242/p077_t6_exposure_reduction_send_blocked_by_kill_switch.json
  exposure_reduction_send_blocker_checksum: sha256:3d3b2e55672e1901335ad8b9b4ba6550ebd09bcb21d1fc7ed4a828f4d56fbf8a
  exposure_reduction_send_blocker_status: blocked_by_kill_switch_no_send
  exposure_reduction_guardrail_repair_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T074014/p077_t6_exposure_reduction_guardrail_code_repair_no_send.json
  exposure_reduction_guardrail_repair_checksum: sha256:b57ad627c0b04c9381896fe6e52d4b7cd7f1ad4e791fed50c3efb19ad9ac8e4a
  exposure_reduction_guardrail_repair_status: partial_repair_no_send_config_authorization_pending
  exposure_reduction_config_authorization_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T075344/p077_t6_exposure_reduction_local_config_authorized_no_send.json
  exposure_reduction_config_authorization_checksum: sha256:57bd11de903d6b245611cec73cec49db803105813de065d597a19fd0b7e93a10
  exposure_reduction_config_authorization_status: config_authorized_no_send_fresh_preflight_superseded_by_no_send_preflight
  fresh_exposure_reduction_authorized_preflight_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T080157/p077_t6_fresh_exposure_reduction_authorized_preflight_no_send.json
  fresh_exposure_reduction_authorized_preflight_checksum: sha256:5865bd05aff7e9f258f38619acfb18f368d972acdcc25662c1c70b257f0f291d
  fresh_exposure_reduction_authorized_preflight_status: authorized_dry_run_no_send
  armed_exposure_reduction_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_armed_exposure_reduction_boundary_cancelled_reconciled.json
  armed_exposure_reduction_checksum: sha256:c78b5cc40ea5ab149a06b93bfe07a64c8548e357287d34eab9c40bf0593d4af3
  armed_exposure_reduction_status: cancelled_reconciled_no_fill
  cancelled_exposure_reduction_diagnosis_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_diagnosis.json
  cancelled_exposure_reduction_diagnosis_checksum: sha256:b26d215c8bc3f128031e6db85ffa4f7ab35fcf0705bf9a55713938ebfa1eddba
  cancelled_exposure_reduction_diagnosis_status: diagnosed_status_53_no_fill_semantic_reason_undetermined
  cancelled_exposure_reduction_no_fill_closeout_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json
  cancelled_exposure_reduction_no_fill_closeout_checksum: sha256:e8fb94cc4239582254c57c1be02369610663e523853c546581e639f18bfe6977
  cancelled_exposure_reduction_no_fill_closeout_status: accepted_no_fill_closeout_no_retry_authorized
  fill_producing_acceptance_deferral_artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json
  fill_producing_acceptance_deferral_checksum: sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e
  fill_producing_acceptance_deferral_status: typed_deferral_recorded_no_retry_authorized
  latest_heartbeat_decision: p077_fill_producing_acceptance_deferred
  latest_heartbeat_local_time: 2026-06-14T09:02:26+08:00
  latest_heartbeat_artifact_policy: use owner pass artifact; do not use screenshot/stdout/UI as truth
blocked_from:
  - runtime/account/order/fill truth
  - UI truth claim
  - ADR completion claim
  - readiness/admission/capital/tradability claim
loop_termination:
  allowed_only_when: all selected ADR0044/ADR0045 and sibling repo tasks have formal owner acceptance and no active typed blockers remain
  blocked_by_current_state: controlled retry preflight blocks BUY OPEN on max net position; exposure-reduction guardrail repair and local config authorization exist; current armed exposure-reduction attempt cancelled with fill zero, reconciled no position delta, diagnosed as status 53/no-fill, closed out without retry authorization, and P077 has recorded typed deferral for fill-producing acceptance; Account Console runtime/read-model truth is not complete
  blocker_policy: try owner-side repair/retry first when the owner repo is available; otherwise keep typed blocker with retry condition and continue heartbeat loop
```
