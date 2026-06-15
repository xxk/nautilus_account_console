# P002 Lane Selection / Lane 选择

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p077_fill_producing_acceptance_deferred
- Updated: 2026-06-14

## 1. Current Selection / 当前选择

Selected lane:

```text
p077_fill_producing_acceptance_deferred
```

Selected blocker target:

```text
p077-t6-fill-producing-acceptance-deferral
```

## 2. Why This Lane / 为什么先选它

P078 A0-A3 foundation is closed with typed evidence.

Account Console P001 Daily Closeout Account Health Panel is `browser_evidence_verified`, and P003 frontend dependency security follow-up is `verified`.

The CTP owner returned a pass artifact for `rb2610` on `freshness_basis=received_at`, P077 recorded a read-only Nautilus sandbox account/position query artifact for account `19054`, P077 recorded a request-only controlled order envelope for `rb BUY 3`, P077 recorded a typed unsafe-action blocker for submit/status/cancel lifecycle, P077 recorded a safe lifecycle owner contract, and P077 recorded an operator authorization wait blocker. After explicit Paper-account operator authorization, the CTP adapter owner ran its official guarded Paper lifecycle runner for `rb2610 BUY OPEN 3 @ 3158`; the typed lifecycle result was `rejected`, `fill_volume=0`, no cancel was required, and post-snapshot reconcile recorded `rejected_reconciled`. The no-fill closeout artifact accepts closeout for the current guarded attempt only and does not authorize retry. The callback decode repair artifact records TD/MD native GB18030 decode repair and focused gate `44 passed`, but it does not reinterpret the previous rejected order or authorize retry. A fresh controlled retry preflight then blocked dry-run `rb2610 BUY OPEN 3 @ 3158` before native send because current `rb2610` long quantity is 5 and projected net position would be 8 above guard max 5. The CTP owner then recorded exposure-reduction candidate/preflight, default-off guardrail repair, local config authorization, one guarded `rb2610 SELL CLOSETODAY 1 @ 3162` attempt, cancelled/no-fill reconciliation, cancelled-attempt diagnosis, and current no-fill closeout artifact `D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T082239/p077_t6_cancelled_exposure_reduction_no_fill_closeout.json`, checksum `sha256:e8fb94cc4239582254c57c1be02369610663e523853c546581e639f18bfe6977`. P077 then recorded typed deferral artifact `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json`, checksum `sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e`. The closeout and deferral apply only to the current guarded exposure-reduction/fill-producing acceptance boundary, do not authorize retry, and do not create Account Console runtime/read-model truth. The next unfinished dependency is a separately accepted safer retry lane if fill-producing acceptance is pursued; Account Console must not turn the request envelope, blocker, contract, UI, screenshots, route config, stdout, latest/debug paths or browser state into order result truth.

## 3. Entry Condition / 入口条件

Before resuming P077 T6 closeout/visibility continuation, the P077/strategies or CTP adapter owner must provide:

```text
Callback Decode/Status Repair Or Split Follow-up Evidence:
  owner: owner://nautilus_ctp_adapter.guarded_paper_order_loop or owner://p077_workflow_closeout
  account: CTP Paper account alias 19053 for the guarded lifecycle artifact; Nautilus sandbox account 19054 remains UI projection evidence only
  required_fields:
    - owner
    - source_ref
    - checksum
    - client_order_id
    - order_lifecycle_disposition
    - fill_volume
    - cancel_required
    - reconciliation_disposition
    - diagnosis_ref
    - diagnosis_checksum
    - next_decision
  accepted_outcomes:
    - typed smaller risk-bounded retry preflight/lifecycle artifact
    - typed exposure-reduction lane artifact
    - typed risk-guard owner update artifact
    - typed split follow-up artifact if retry is deferred
    - typed owner blocker with retry condition
  current_outcome:
    artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_reconcile_rejected_order.json
    checksum: sha256:3a43c8ef82f11bca5707873f01b1ace16a87d222a6cf115cc1a7eda684e6d196
    client_order_id: p077-t6-rb2610-buy3-061440
    order_lifecycle_disposition: rejected
    fill_volume: 0
    cancel_required: false
    reconciliation_disposition: rejected_reconciled
    diagnosis_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_rejected_order_diagnosis.json
    diagnosis_checksum: sha256:2c9c0bdd0f34684806c5e5e9d39dd1ff4706025b1508a6fe138b0837d4d1e96f
    no_fill_closeout_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_no_fill_closeout.json
    no_fill_closeout_checksum: sha256:f96d944ca06cf8fd5fb38143cf48cb66ab074baaebfe358620f42cee5aa3e544
    callback_decode_repair_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T061416/p077_t6_callback_decode_repair.json
    callback_decode_repair_checksum: sha256:908a86bf4dfaf36d0cc507294522332a5af747acd4c3a4ad67fdba1ed501ab1c
    controlled_retry_preflight_blocker_artifact: D:/Nautilus/nautilus_ctp_adapter/output/reports/p077-paper-lifecycle/20260614T070007/p077_t6_controlled_retry_preflight_blocker.json
    controlled_retry_preflight_blocker_checksum: sha256:26b8edd710bebefeadc0321174b8102381f66bb82a99d8b952b978319174e642
    blocker_reason: max_net_position_exceeded
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
    retry_condition: separately accepted safer retry lane for fill-producing acceptance; do not bypass owner guardrails
  safe_contract:
    artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/safe_lifecycle_contract/p077-t6-safe-lifecycle-owner-contract.json
    checksum: sha256:4f67dc74640f29df9134369f623e33cb868ea9025c89cac92f9c549ff04a682c
    runtime_dispatch_allowed_by_contract: false
    operator_authorization_required: true
  operator_authorization_wait:
    artifact: D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/operator_authorization_wait/p077-t6-operator-authorization-required-blocker.json
    checksum: sha256:e7dfa994202946337b4a57fe2250b601e7b6dca534107ac1ee1dc4bc9fac9fcd
    status: historical_wait_boundary_superseded_by_operator_authorized_guarded_runner
  forbidden_truth_sources:
    - request envelope as order result
    - UI action/click as lifecycle truth
    - stdout/log text
    - latest/debug paths
    - process/window state
    - UI/browser state
    - screenshots
    - DB rows without owner checksum
```

## 4. Exit Signal / 出口信号

This lane has recorded the historical unsafe-action/request blocker, safe lifecycle owner contract, operator authorization wait blocker, the operator-authorized guarded lifecycle reconcile artifact, a rejected-order diagnosis artifact, a no-fill closeout artifact, a callback decode repair artifact, a controlled retry preflight blocker, no-send exposure-reduction candidate/preflight evidence, the armed exposure-reduction boundary artifact, the cancelled-attempt diagnosis artifact, the current no-fill closeout artifact, and the P077 fill-producing acceptance deferral artifact from the correct owner boundaries. The latest P077 deferral is `D:/Nautilus/nautilus_strategies/output/paper_nodes/real-paper/sessions/p077-t6-sandbox-order-ui-acceptance-001/nautilus-sandbox-paper/p077-t6-fill-producing-acceptance-deferral.json`, checksum `sha256:974ca63b4750f77b638bb6e996768fa452057b4447276378076acf615be5249e`; it confirms fill-producing acceptance remains unsatisfied and does not authorize retry. It does not proceed to Account Console runtime truth or loop termination until a separately accepted safer retry lane is recorded or the scope remains explicitly deferred.

It must not exit on route selection, local UI pass, screenshots, logs, browser evidence or any order status/fill/cancel/reconcile claim.

This lane selection is not the same as loop termination. The next heartbeat should choose the smallest safe follow-up: separately accepted safer retry lane for fill-producing acceptance, or keep the typed deferral active. The overall loop terminates only when all selected ADR0044/ADR0045 and sibling repo tasks have owner acceptance evidence and no active typed blockers remain.

## 5. Deferred Lanes / 暂缓 lanes

| Lane | Deferred until | Reason |
| --- | --- | --- |
| `p078_a0_a3_foundation` | successor A4+ proposal/change opens | A0-A3 foundation closeout is already verified |
| `account_console_contract_fixture_ui_slice` | next Account Console UI slice is explicitly opened with contract/fixture acceptance | P001 and P003 are verified |
| `ctp_market_owner_blocker_repair` | a future market freshness blocker appears | current CTP artifact passed on received-at freshness with stale exchange timestamp warning |
| `sandbox_account_position_query` | a future account/position query blocker appears | current query artifact is recorded for account `19054` |
| `controlled_order_request` | a future request envelope blocker appears | current request envelope is recorded for `rb BUY 3` without submit/result claim |
| `wait_operator_authorized_sandbox_lifecycle_runner` | superseded | operator authorization was provided and guarded lifecycle runner evidence exists |
| `wait_p077_rejected_order_diagnosis_or_no_fill_closeout` | superseded | rejected-order diagnosis is recorded |
| `wait_p077_no_fill_closeout_or_callback_decode_repair` | superseded | no-fill closeout is recorded for the current guarded attempt |
| `wait_p077_callback_decode_status_repair_before_retry` | superseded | callback text decoding repair is recorded by the CTP owner |
| `p077_callback_decode_repair_recorded_retry_preflight_next` | superseded | controlled retry preflight blocker is recorded by the CTP owner |
| `p077_controlled_retry_preflight_blocked_max_net_position` | superseded by candidate preflight record | retry is blocked by max-net-position guard until smaller risk-bounded order, exposure-reduction lane or risk-guard owner update exists |
| `p077_exposure_reduction_candidate_preflight_recorded_no_send` | superseded by fresh candidate record | no-send `rb2610 SELL CLOSETODAY 1 @ 3158` candidate preflight passed, but send still requires separate accepted exposure-reduction lane or updated retry target |
| `p077_fresh_exposure_reduction_candidate_preflight_recorded_no_send` | superseded by kill-switch blocker | fresh no-send `rb2610 SELL CLOSETODAY 1 @ 3161` candidate preflight passed, but send still requires separate accepted exposure-reduction lane or updated retry target |
| `p077_exposure_reduction_send_blocked_by_kill_switch` | superseded by guardrail code repair | armed boundary check was blocked by `kill_switch_closed`; risk-guard owner repair was selected next |
| `p077_exposure_reduction_guardrail_code_repair_no_send` | superseded by config authorization | default-off exposure-reduction-only Paper smoke gate is implemented |
| `p077_exposure_reduction_local_config_authorized_no_send` | superseded by fresh authorized no-send preflight | local Paper config authorizes exposure-reduction-only smoke; fresh market/snapshot/order preflight was run as no-send evidence |
| `p077_fresh_exposure_reduction_authorized_preflight_no_send` | superseded by armed cancelled/reconciled boundary | fresh authorized dry-run preflight exists for `rb2610 SELL CLOSETODAY 1 @ 3162` |
| `p077_armed_exposure_reduction_cancelled_reconciled` | superseded by cancelled-attempt diagnosis | armed `rb2610 SELL CLOSETODAY 1 @ 3162` produced lifecycle `cancelled`, fill `0`, post snapshot and `cancelled_reconciled` |
| `p077_cancelled_exposure_reduction_diagnosed` | superseded by no-fill closeout | diagnosis artifact classifies status `53` as cancelled/no-fill with semantic reason undetermined |
| `p077_cancelled_exposure_reduction_no_fill_closeout` | superseded by P077 deferral | closeout artifact accepts no-fill closeout for the cancelled exposure-reduction attempt only and does not authorize retry |
| `p077_fill_producing_acceptance_deferred` | selected now | P077 deferral artifact records fill-producing acceptance unsatisfied and no retry authorized; next boundary is a separately accepted safer retry lane or continuing typed deferral |

## 6. Selection Acceptance / 选择验收

| ID | Must pass | Must fail if |
| --- | --- | --- |
| P002-LANE-01 | exactly one lane is selected | heartbeat selects runtime and UI lanes together |
| P002-LANE-02 | selected lane has an owner outside P002 | P002 becomes owner of implementation evidence |
| P002-LANE-03 | selected lane has entry and exit conditions | next action is vague |
| P002-LANE-04 | deferred lanes are recorded | Account Console UI starts with invented fields |
| P002-LANE-05 | forbidden claims remain listed | heartbeat can imply readiness |
