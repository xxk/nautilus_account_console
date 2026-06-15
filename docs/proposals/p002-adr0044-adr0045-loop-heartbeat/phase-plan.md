# P002 Phase Plan / 阶段计划

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p077_fill_producing_acceptance_deferred
- Updated: 2026-06-14

## Phase 0: Conflict Analysis / 冲突分析

- Status: completed_for_review
- Goal: determine whether a loop heartbeat can safely coordinate ADR-0044, ADR-0045 and Account Console ADR-0003.
- Exit signal:
  - P0 conflict matrix exists.
  - P0 blocking rules exist.
  - P077/P078/account-console ownership is preserved.
  - P0 verdict is `conditional_go`.

## Phase 1: Heartbeat Contract / 心跳合同

- Status: completed_for_review
- Goal: define the read-only heartbeat row format and owner-lane selection rule.
- Entry condition:
  - P0 acceptance reviewed.
- Exit signal:
  - heartbeat row template exists.
  - exactly-one-lane-per-heartbeat rule exists.
  - no scheduler/runtime/UI truth rule exists.
  - first landed heartbeat row exists in `heartbeat-contract.md`.

## Phase 2: First Owner Lane Selection / 首个 owner lane 选择

- Status: completed_for_review
- Goal: choose the first owner lane after P0.
- Candidate lanes:
  - `p078_a0_a3_foundation`
  - `account_console_contract_fixture_ui_slice`
  - `p077_owner_blocker_repair`
  - `ctp_market_owner_blocker_repair`
  - `wait_external_owner`
- Exit signal:
  - one lane selected.
  - entry condition and blocker condition recorded.
  - selected lane is `p078_a0_a3_foundation`.
  - first child target is `adr0044-a0-official-matching-baseline`.

## Phase 3: Closeout / 收口

- Status: completed_for_current_local_lanes
- Goal: record whether P002 remains only a governance heartbeat or should split into an implementation-bearing successor.
- Must split if:
  - scheduler implementation appears
  - runtime/account/order/fill truth appears
  - UI implementation appears without contract/fixture acceptance
  - Paper/Live/admission/capital wording appears

Current result:

- P078 A0-A3 foundation is verified in `nautilus_strategies`.
- P001 Account Console UI slice is `browser_evidence_verified`.
- P003 frontend dependency security follow-up is `verified`.
- The CTP owner returned a pass artifact for `rb2610` at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-market-freshness/p077_t6_ctp_market_freshness_20260613T194429Z.json`, checksum `sha256:dfbe8bef811104eaec39995cc91f1243dffee36c8f5b30799a85a3e464935265`, with warning `first_tick_exchange_timestamp_stale`.
- P077 recorded a read-only sandbox account/position query artifact for account `19054` at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/account_position_query/account-position-query-19054.json`, checksum `sha256:c4e2970786ef97ed8ef4d5ba978bfa1667b650d7b730d720ef0cbae434d10f5d`.
- P077 recorded a request-only controlled order envelope at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/controlled_order_request/p077-t6-controlled-order-request-rb-buy-3-001.json`, checksum `sha256:c77ffa9f7a464d03a7c35b3111cef476476f59c3d4d7c63623a7ba7a1220caaf`.
- P077 recorded a submit/status/cancel lifecycle typed unsafe-action blocker at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/submit_status_cancel_lifecycle/p077-t6-submit-status-cancel-lifecycle-unsafe-action-blocker.json`, checksum `sha256:7f9f8263b2a01f3539bb5624da80e9af13958ef67136f87872c29c8701996631`.
- P077 recorded a safe lifecycle owner contract at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/safe_lifecycle_contract/p077-t6-safe-lifecycle-owner-contract.json`, checksum `sha256:4f67dc74640f29df9134369f623e33cb868ea9025c89cac92f9c549ff04a682c`; the contract itself does not authorize runtime dispatch.
- P077 recorded an operator authorization wait blocker at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/operator_authorization_wait/p077-t6-operator-authorization-required-blocker.json`, checksum `sha256:e7dfa994202946337b4a57fe2250b601e7b6dca534107ac1ee1dc4bc9fac9fcd`; it is retained as historical boundary evidence.
- After explicit Paper-account operator authorization, the CTP adapter owner ran the official guarded Paper lifecycle runner for `rb2610 BUY OPEN 3 @ 3158`; the typed lifecycle result was `rejected`, `fill_volume=0`, no cancel was required, and post-snapshot reconcile recorded `rejected_reconciled`.
- Guarded lifecycle reconcile artifact: `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_reconcile_rejected_order.json`, checksum `sha256:3a43c8ef82f11bca5707873f01b1ace16a87d222a6cf115cc1a7eda684e6d196`.
- Rejected-order diagnosis is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_rejected_order_diagnosis.json`, checksum `sha256:2c9c0bdd0f34684806c5e5e9d39dd1ff4706025b1508a6fe138b0837d4d1e96f`.
- No-fill closeout is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_no_fill_closeout.json`, checksum `sha256:f96d944ca06cf8fd5fb38143cf48cb66ab074baaebfe358620f42cee5aa3e544`; it closes only the current guarded attempt and does not authorize retry.
- Callback decode repair is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_callback_decode_repair.json`, checksum `sha256:908a86bf4dfaf36d0cc507294522332a5af747acd4c3a4ad67fdba1ed501ab1c`; it repairs TD/MD native GB18030 callback text decoding and does not authorize retry.
- Controlled retry preflight blocker is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T070007/p077_t6_controlled_retry_preflight_blocker.json`, checksum `sha256:26b8edd710bebefeadc0321174b8102381f66bb82a99d8b952b978319174e642`; market/snapshot passed, but dry-run `rb2610 BUY OPEN 3 @ 3158` was blocked before native send by `max_net_position_exceeded`.
- Fresh exposure-reduction candidate preflight is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T072211/p077_t6_fresh_exposure_reduction_candidate_preflight.json`, checksum `sha256:d1ccc7dd7242e0c3679862c04edfa36a877eb6baf5475c58ae1057e2b8587396`; no-send `rb2610 SELL CLOSETODAY 1 @ 3161` dry-run passed with projected net position 4, but it does not authorize paper send.
- Exposure-reduction armed boundary blocker is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T073242/p077_t6_exposure_reduction_send_blocked_by_kill_switch.json`, checksum `sha256:3d3b2e55672e1901335ad8b9b4ba6550ebd09bcb21d1fc7ed4a828f4d56fbf8a`; send was blocked before native order by `kill_switch_closed` because `AllowLiveOrderSmoke=false`.
- Exposure-reduction guardrail code repair is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T074014/p077_t6_exposure_reduction_guardrail_code_repair_no_send.json`, checksum `sha256:b57ad627c0b04c9381896fe6e52d4b7cd7f1ad4e791fed50c3efb19ad9ac8e4a`; no local config change or paper/native send occurred.
- Exposure-reduction local config authorization is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T075344/p077_t6_exposure_reduction_local_config_authorized_no_send.json`, checksum `sha256:57bd11de903d6b245611cec73cec49db803105813de065d597a19fd0b7e93a10`; local gitignored config now enables only exposure-reduction smoke, no paper/native send occurred.
- Fresh authorized no-send preflight is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T080157/p077_t6_fresh_exposure_reduction_authorized_preflight_no_send.json`, checksum `sha256:5865bd05aff7e9f258f38619acfb18f368d972acdcc25662c1c70b257f0f291d`; it records dry-run `rb2610 SELL CLOSETODAY 1 @ 3162`, `paper_send_armed=false`, `submit_attempted=false`, and no post-snapshot/reconcile truth.
- Armed exposure-reduction boundary evidence is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_armed_exposure_reduction_boundary_cancelled_reconciled.json`, checksum `sha256:c78b5cc40ea5ab149a06b93bfe07a64c8548e357287d34eab9c40bf0593d4af3`; it records one guarded `rb2610 SELL CLOSETODAY 1 @ 3162`, lifecycle `cancelled`, fill `0`, post snapshot and `cancelled_reconciled` target delta `0`.
- Cancelled exposure-reduction diagnosis is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_diagnosis.json`, checksum `sha256:b26d215c8bc3f128031e6db85ffa4f7ab35fcf0705bf9a55713938ebfa1eddba`; it classifies status `53` as cancelled/no-fill and does not infer broker semantics from mojibake error text.
- Cancelled exposure-reduction no-fill closeout is recorded at `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json`, checksum `sha256:e8fb94cc4239582254c57c1be02369610663e523853c546581e639f18bfe6977`; it closes only the current guarded exposure-reduction attempt, does not authorize retry, and creates no Account Console runtime/read-model truth.
- P077 owner fill-producing acceptance deferral is recorded at `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json`, checksum `sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e`; it cites the CTP no-fill closeout and confirms retry is not authorized by the deferral artifact.
- The next unfinished stage is a separately accepted safer retry lane for fill-producing acceptance if that scope is pursued.
- P002 therefore selects `p077_fill_producing_acceptance_deferred` and must not create scheduler/runtime/account/order/fill/UI truth or treat a request envelope/blocker/contract/UI as an order result.
- Future heartbeats should either open a separately accepted safer retry lane in the correct owner boundary or keep the deferral/blocker explicit.
- The loop terminates only after all selected ADR0044/ADR0045 and sibling repo work has formal owner acceptance evidence and no active typed blockers remain.
