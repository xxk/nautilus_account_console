export type AccountKind =
  | "sandbox_paper"
  | "real_feed_sandbox_paper"
  | "broker_paper_probe"
  | "live_broker"
  | "backtest_replay";

export interface AccountSnapshot {
  account_id: string;
  account_kind: AccountKind;
  portfolio_uid: string;
  session_id: string;
  equity: number;
  available_cash: number;
  margin_used: number;
  position_count: number;
  open_order_count: number;
  fill_count_today: number;
  event_lag_ms: number;
  health: string;
  blocker_id: string | null;
  last_seq: number;
  source_ref: string;
  checksum: string;
}

export interface OrderEvent {
  event_id: string;
  seq: number;
  ts_event: string;
  ts_recv: string;
  account_id: string;
  account_kind: AccountKind;
  portfolio_uid: string;
  strategy_id: string;
  instrument_id: string;
  client_order_id: string;
  venue_order_id: string | null;
  event_type: string;
  order_status: string;
  side: string;
  price: number | null;
  quantity: number | null;
  filled_qty: number;
  last_px: number | null;
  last_qty: number | null;
  leaves_qty: number | null;
  reason: string | null;
  latency_ms: number | null;
  report_msg_type: string | null;
  report_msg_ref: string | null;
  report_msg_checksum: string | null;
  report_msg_excerpt: string | null;
  source_ref: string;
  checksum: string;
}

export interface OrderExecutionReports {
  account_id: string;
  client_order_id: string;
  reports: OrderEvent[];
}

export interface MirrorCapabilityState {
  enabled: boolean;
  mirror_state?: string | null;
  mode?: string | null;
  allowed_actions?: string[];
}

export interface MirrorCapabilities {
  observation: MirrorCapabilityState;
  command: MirrorCapabilityState;
}

export interface MirrorCommandStatusProjection {
  schema_version?: string;
  status?: string | null;
  command_audit_ref?: string | null;
  risk_decision_refs?: string[];
  approval_decision_refs?: string[];
  gateway_event_refs?: string[];
  readback_refs?: string[];
  reconciliation_ref?: string | null;
  gateway_ack_is_final_state?: boolean | null;
  readback_required?: boolean | null;
  reconciliation_required?: boolean | null;
  blockers?: Record<string, unknown>[];
}

export interface MirrorAccountSummary {
  account_id: string;
  display_alias: string;
  source_kind: string;
  source_mode: string;
  account_domain: string;
  route_id: string;
  evidence_partition: string;
  mirror_state: string;
  command_enabled: boolean;
  command_mode: string;
  balance_count: number;
  position_count: number;
  order_count: number;
  fill_count: number;
  blocker_count: number;
  projection_checkpoint_id: string;
  projection_checksum: string;
  source_ref: string;
  source_checksum: string;
}

export interface MirrorListResponse {
  schema_version: "account_mirror_list.v1";
  accounts: MirrorAccountSummary[];
}

export interface MirrorAccountProjection {
  schema_version: "account_mirror_projection.v1";
  account_id: string;
  display_alias: string;
  source_kind: string;
  source_mode: string;
  account_domain: string;
  capabilities: MirrorCapabilities;
  balances: Record<string, unknown>[];
  positions: Record<string, unknown>[];
  orders: Record<string, unknown>[];
  fills: Record<string, unknown>[];
  source_health: Record<string, unknown>;
  command_status?: MirrorCommandStatusProjection | null;
  blockers: Record<string, unknown>[];
  projection_checkpoint_id: string;
  projection_checksum: string;
  source_ref: string;
  source_checksum: string;
  route_context: Record<string, unknown>;
  boundaries: Record<string, unknown>;
}

export interface MirrorSourceHealthResponse {
  schema_version: "account_mirror_source_health.v1";
  account_id: string;
  state: string;
  source_ref: string;
  source_checksum: string;
  observed_at: string;
  projection_checkpoint_id: string;
  projection_checksum: string;
  blockers: Record<string, unknown>[];
  boundaries: Record<string, unknown>;
}

export interface MirrorEvidenceItem {
  kind: string;
  owner: string;
  source_ref: string;
  checksum: string;
  authority: string;
}

export interface MirrorEvidenceResponse {
  schema_version: "account_mirror_evidence.v1";
  account_id: string;
  projection_checkpoint_id: string;
  projection_checksum: string;
  source_ref: string;
  source_checksum: string;
  evidence: MirrorEvidenceItem[];
  blockers: Record<string, unknown>[];
  boundaries: Record<string, unknown>;
}

export interface OrderIntentRequest {
  schema_version: "account_command.order_intent.v1";
  intent_id: string;
  account_id: "acct.ctp.paper.19053";
  mode: "paper_armed";
  action: "submit";
  instrument: string;
  exchange: string;
  side: "BUY" | "SELL";
  quantity: number;
  order_type: "LIMIT";
  limit_price: number;
  time_in_force: "GFD" | "IOC" | "FAK" | "FOK";
  offset: "OPEN" | "CLOSE" | "CLOSETODAY" | "CLOSEYESTERDAY";
  idempotency_key: string;
  operator_ref: string;
  preflight_ref: string;
  raw_secret_values_recorded: false;
  raw_broker_endpoint_recorded: false;
}

export interface CancelIntentRequest {
  schema_version: "account_command.cancel_intent.v1";
  intent_id: string;
  account_id: "acct.ctp.paper.19053";
  mode: "paper_armed";
  action: "cancel";
  instrument: string;
  exchange: string;
  client_order_id: string;
  venue_order_id: string;
  order_ref: string;
  front_id: number;
  session_id: number;
  idempotency_key: string;
  operator_ref: string;
  readback_ref: string;
  raw_secret_values_recorded: false;
  raw_broker_endpoint_recorded: false;
}

export interface CommandApiBlocker {
  blocker_id: string;
  type: string;
  stage: string;
  reason: string;
  source_ref: string;
  next_action: string;
}

export interface CommandApiResult {
  schema_version: "account_command.command_api_result.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: string;
  action: "submit" | "cancel";
  mode: string;
  status: "accepted_for_risk" | "blocked";
  command_id: string;
  intent_id: string;
  intent_ref: string;
  idempotency_key: string;
  idempotency_enforced: boolean;
  next_required_stage: string;
  blockers: CommandApiBlocker[];
  risk_decision_ref?: string | null;
  approval_decision_ref?: string | null;
  gateway_event_refs: string[];
  readback_refs: string[];
  reconciliation_ref?: string | null;
  gateway_ack_is_final_state: false;
  gateway_send_attempted: false;
  broker_order_created: false;
  runtime_duplicate_send_attempted: false;
  raw_secret_values_recorded: false;
  raw_broker_endpoint_recorded: false;
}

export interface CommandRuntimeCloseout {
  schema_version: "account_command.runtime_closeout.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  run_id: string;
  mode: "paper_armed";
  status: "reconciled";
  closeout_manifest_ref: string;
  closeout_manifest_checksum: string;
  command_audit_ref: string;
  command_audit_checksum: string;
  intent_refs: string[];
  risk_decision_refs: string[];
  approval_decision_refs: string[];
  gateway_event_refs: string[];
  readback_refs: string[];
  reconciliation_ref: string;
  artifact_checksums: Record<string, string>;
  runtime_gateway_send_observed: true;
  broker_order_created: true;
  browser_triggered_broker_order: false;
  gateway_ack_is_final_state: false;
  raw_secret_values_recorded: false;
  raw_broker_endpoint_recorded: false;
  runtime_duplicate_send_attempted: false;
  source_owner_ref: string;
  explicit_non_claims: string[];
}

export interface CommandRuntimeRunRequest {
  schema_version: "account_command.owner_runtime_run_request.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  action: "submit" | "cancel";
  mode: "paper_armed";
  status: "blocked_until_owner_runtime_invocation";
  command_id: string;
  intent_id: string;
  intent_ref: string;
  idempotency_key: string;
  owner_runtime_owner_ref: "owner://nautilus_ctp_adapter";
  owner_runtime_repo_ref: "owner-repo://nautilus_ctp_adapter";
  owner_runtime_entrypoint_ref: string;
  owner_runtime_config_ref: string;
  source_preflight_ref: string;
  readback_ref?: string | null;
  expected_output_root_ref: string;
  runtime_invocation_attempted: false;
  browser_triggered_broker_order: false;
  gateway_send_attempted: false;
  broker_order_created: false;
  raw_secret_values_recorded: false;
  raw_broker_endpoint_recorded: false;
  external_write_approval_required: true;
  blockers: CommandApiBlocker[];
  explicit_non_claims: string[];
  run_request_checksum: string;
}

export interface CommandRuntimeInvocationReadiness {
  schema: "account-console.p024.owner-runtime-invocation-readiness.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  status: "blocked_waiting_for_external_owner_runtime_write_approval";
  verdict: "readiness_package_passed_runtime_not_invoked";
  reviewed_at: string;
  owner_runtime: {
    owner_ref: string;
    owner_repo_ref: string;
    owner_repo_path: string;
    config_ref: string;
    config_file_exists_on_owner_node: boolean;
    config_raw_content_read: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
  };
  entrypoints: Array<{
    action: "submit" | "cancel";
    entrypoint_ref: string;
    owner_path: string;
    checksum: string;
    armed_flag: string;
    required_arguments: string[];
  }>;
  predecessor_evidence: Record<string, unknown>;
  external_write_approval_request: {
    required: true;
    obtained: false;
    approval_path: string;
    write_scope: string[];
    reason: string;
    expected_impact: string[];
    approval_prompt_required_before_execution: true;
  };
  planned_runtime_commands: Array<{
    action: "submit" | "cancel";
    entrypoint_ref: string;
    command_template: string;
    runtime_invocation_attempted: false;
  }>;
  acceptance_after_owner_run: {
    required_owner_artifacts: string[];
    required_browser_evidence: string[];
    required_validators: string[];
  };
  negative_assertions: {
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    browser_triggered_broker_order: false;
    gateway_send_attempted: false;
    broker_order_created: false;
    live_armed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
  };
  blockers: CommandApiBlocker[];
  explicit_non_claims: string[];
}

export interface CommandRuntimeExecutionApprovalPacket {
  schema: "account-console.p024.owner-runtime-execution-approval-packet.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4a_owner_runtime_execution_approval_packet_ready";
  verdict: "approval_packet_ready_runtime_not_invoked";
  owner_runtime: {
    owner_ref: string;
    owner_repo_ref: string;
    owner_repo_path: string;
    config_ref: string;
    config_file_exists_on_owner_node: boolean;
    config_raw_content_read: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
  };
  required_operator_approval: {
    required: true;
    obtained: false;
    approval_path: string;
    reason: string;
    expected_impact: string[];
    exact_approval_text: string;
    approval_prompt_required_before_execution: true;
  };
  planned_execution: {
    execution_root_ref: string;
    debug_root_ref: string;
    predecessor_readiness_ref: string;
    predecessor_closeout_ref: string;
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
  };
  entrypoints: Array<{
    action: "submit" | "cancel";
    entrypoint_ref: string;
    owner_path: string;
    checksum: string;
    armed_flag: string;
    required_arguments: string[];
  }>;
  command_templates: Array<{
    action: "submit" | "cancel";
    template: string;
    uses_placeholders_only_for_runtime_values: true;
    runtime_invocation_attempted: false;
  }>;
  required_post_run_artifacts: string[];
  post_run_acceptance_gates: string[];
  blockers: CommandApiBlocker[];
  negative_assertions: {
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    browser_triggered_broker_order: false;
    gateway_send_attempted: false;
    broker_order_created: false;
    live_armed: false;
    account_mirror_write_authority: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
    full_runtime_acceptance_claimed: false;
  };
  explicit_non_claims: string[];
}

export interface CommandRuntimeExecutionHandoffBundle {
  schema: "account-console.p024.owner-runtime-execution-handoff-bundle.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4c_owner_runtime_execution_handoff_bundle_ready";
  verdict: "handoff_bundle_ready_runtime_not_invoked";
  depends_on: Record<string, unknown>;
  execution_guard: {
    execution_allowed: false;
    approval_required: true;
    approval_obtained: false;
    exact_approval_text_required: string;
    owner_repo_path: string;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
  };
  runtime_input_requirements: Array<{
    field: string;
    required: boolean;
    source: string;
    reason: string;
  }>;
  operator_sequence: Array<{
    step: string;
    action: string;
    entrypoint_ref?: string;
    armed_flag?: string;
    must_pass_before_next: boolean;
  }>;
  required_owner_artifacts: string[];
  post_handoff_gates: string[];
  blockers: CommandApiBlocker[];
  negative_assertions: {
    execution_allowed: false;
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    browser_triggered_broker_order: false;
    gateway_send_attempted: false;
    broker_order_created: false;
    live_armed: false;
    account_mirror_write_authority: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
    full_runtime_acceptance_claimed: false;
  };
  explicit_non_claims: string[];
}

export interface CommandPartialFillRuntimeExecutionApprovalPacket {
  schema: "account-console.p024.partial-fill-runtime-execution-approval-packet.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4j_partial_fill_runtime_execution_approval_packet_ready";
  verdict: "approval_packet_ready_runtime_not_invoked";
  owner_runtime: Record<string, unknown>;
  required_operator_approval: {
    required: true;
    obtained: false;
    approval_path: string;
    reason: string;
    expected_impact: string[];
    exact_approval_text: string;
    approval_prompt_required_before_execution: true;
  };
  planned_execution: {
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    new_order_submitted: false;
    cancel_sent: false;
    [key: string]: unknown;
  };
  entrypoints: Array<{
    action: "submit" | "cancel";
    entrypoint_ref: string;
    owner_path: string;
    checksum: string;
    armed_flag: string;
  }>;
  attempt_constraints: {
    risk_shape: string;
    preferred_instrument: string;
    maximum_submit_attempts: number;
    maximum_order_quantity: number;
    partial_fill_success_formula: string;
    terminal_cancel_success_formula: string;
    post_cancel_remaining_quantity_formula: string;
    fallback_if_no_partial_fill: string;
    [key: string]: unknown;
  };
  command_templates: Array<Record<string, unknown>>;
  required_post_run_artifacts: string[];
  post_run_acceptance_gates: string[];
  blockers: CommandApiBlocker[];
  negative_assertions: {
    approval_obtained: false;
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    new_order_submitted: false;
    cancel_sent: false;
    browser_triggered_broker_order: false;
    gateway_send_attempted: false;
    broker_order_created: false;
    live_armed: false;
    account_mirror_write_authority: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
    full_acceptance_claimed: false;
    browser_fixture_promoted_to_runtime_truth: false;
  };
  explicit_non_claims: string[];
}

export interface CommandPartialFillRuntimeExecutionHandoffBundle {
  schema: "account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4k_partial_fill_runtime_execution_handoff_bundle_ready";
  verdict: "handoff_bundle_ready_runtime_not_invoked";
  depends_on: Record<string, unknown>;
  execution_guard: {
    execution_allowed: false;
    approval_required: true;
    approval_obtained: false;
    exact_approval_text_required: string;
    owner_repo_path: string;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
  };
  runtime_input_requirements: Array<{
    field: string;
    required: boolean;
    allowed_values?: number[];
    reason: string;
  }>;
  operator_sequence: Array<{
    step: string;
    action: string;
    entrypoint_ref?: string;
    armed_flag?: string;
    must_pass_before_next: boolean;
  }>;
  success_criteria: {
    non_ui_runtime: string[];
    web_ui_runtime: string[];
  };
  fallback_classifications: string[];
  negative_assertions: {
    execution_allowed: false;
    approval_obtained: false;
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    new_order_submitted: false;
    cancel_sent: false;
    full_acceptance_claimed: false;
    browser_fixture_promoted_to_runtime_truth: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
  };
}

export interface CommandRuntimeExecutionGapAudit {
  schema: "account-console.p024.runtime-execution-gap-audit.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4e_final_runtime_execution_gap_audited";
  verdict: "blocked_pending_owner_runtime_execution";
  goal_state: "all_acceptance_requires_owner_runtime_execution_artifacts";
  accepted_scenarios: string[];
  not_accepted_scenarios: Array<{
    id: string;
    scenario: string;
    required_evidence_shape: string;
    current_status: string;
    blocker_refs: string[];
  }>;
  required_before_goal_complete: string[];
  external_write_approval: {
    required: true;
    obtained: false;
    approval_path: string;
    exact_approval_text: string;
  };
  owner_runtime_refs: {
    owner_ref: string;
    owner_repo_path: string;
    config_ref: string;
    config_raw_content_read: false;
    submit_entrypoint_ref: string;
    cancel_entrypoint_ref: string;
  };
  required_owner_artifacts: string[];
  post_execution_gates: string[];
  residual_blockers: CommandApiBlocker[];
  negative_assertions: {
    final_acceptance_claimed: false;
    runtime_invocation_attempted: false;
    owner_repo_write_attempted: false;
    browser_triggered_broker_order: false;
    gateway_send_attempted: false;
    broker_order_created: false;
    live_armed: false;
    account_mirror_write_authority: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_read: false;
  };
  explicit_non_claims: string[];
}

export interface CommandPartialFillOwnerRepairImplementationPlan {
  schema: "account-console.p024.partial-fill-owner-repair-implementation-plan.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4r_owner_close_offset_repair_implementation_plan_ready";
  verdict: "owner_repair_plan_ready_no_owner_write_attempted";
  depends_on: Record<string, unknown>;
  owner_read_context: {
    owner_repo_ref: string;
    owner_repo_path: string;
    owner_repo_write_attempted: false;
    source_refs: Array<{
      source_id: string;
      ref: string;
      symbol: string;
      observed_current_behavior: string;
    }>;
  };
  planned_owner_changes_after_exact_approval: Array<{
    change_id: string;
    target_ref: string;
    target_symbol: string;
    implementation_shape: string;
    must_preserve?: string[];
    must_assert?: string[];
  }>;
  post_repair_validator_sequence: Array<{
    stage: string;
    command: string;
    required_before_retry: boolean;
  }>;
  post_repair_runtime_attempt_gate: {
    runtime_attempt_allowed_by_this_plan: false;
    fresh_approval_required: true;
    maximum_additional_attempts_after_repair: number;
    risk_shape: string;
    success_formula: string;
    terminal_cancel_formula: string;
  };
  forbidden_repair_shapes: string[];
  negative_assertions: {
    owner_repo_write_attempted_by_this_plan: false;
    owner_runtime_invocation_attempted: false;
    owner_repair_claimed_complete: false;
    runtime_retry_authorized: false;
    partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillOwnerRepairEvidenceIngestGate {
  schema: "account-console.p024.partial-fill-owner-repair-evidence-ingest-gate.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4t_owner_repair_evidence_ingest_gate_ready";
  verdict: "ingest_gate_ready_owner_repair_evidence_missing";
  depends_on: Record<string, unknown>;
  ingest_scope: {
    owner_repo_ref: string;
    owner_repo_path: string;
    raw_secret_values_allowed: false;
    raw_broker_endpoint_allowed: false;
    config_raw_content_allowed: false;
    runtime_retry_allowed_by_ingest_gate: false;
    accepts_owner_code_repair_evidence: true;
    accepts_owner_runtime_partial_fill_evidence: false;
  };
  required_owner_repair_evidence: Array<{
    evidence_id: string;
    required_shape: string;
    current_status: "missing";
    must_include: string[];
  }>;
  post_ingest_required_account_console_updates: string[];
  reject_evidence_if: string[];
  negative_assertions: {
    owner_repair_evidence_recorded: false;
    owner_repo_write_attempted_by_this_gate: false;
    owner_runtime_invocation_attempted: false;
    runtime_retry_authorized: false;
    partial_fill_runtime_claimed: false;
    web_ui_real_partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillOwnerRepairPreflightSourceAudit {
  schema: "account-console.p024.partial-fill-owner-repair-preflight-source-audit.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4v_owner_repair_preflight_source_audited";
  verdict: "owner_repair_still_required_before_runtime_retry";
  owner_repo: {
    owner_repo_ref: string;
    owner_repo_path: string;
    head_ref: string;
    write_attempted_by_audit: false;
  };
  source_checks: Array<{
    path: string;
    sha256: string;
    required_symbol_present: boolean;
    current_gap: string;
  }>;
  operator_approval_delta: {
    latest_user_approval_observed_scope: string;
    sufficient_for_owner_code_repair: false;
    sufficient_for_post_repair_runtime_retry: false;
    required_exact_approval_before_owner_write_or_retry: string;
  };
  next_required_action: {
    owner_code_repair_allowed_by_current_audit: false;
    owner_runtime_retry_allowed_by_current_audit: false;
    blind_script_retry_rejected: true;
    reason: string;
  };
  negative_assertions: {
    owner_repo_write_attempted: false;
    owner_code_repair_claimed: false;
    owner_validator_pass_claimed: false;
    owner_runtime_invocation_attempted: false;
    post_repair_runtime_retry_authorized: false;
    real_partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillOwnerRepairPatchPreview {
  schema: "account-console.p024.partial-fill-owner-repair-patch-preview.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4x_owner_repair_patch_preview_ready";
  verdict: "patch_preview_ready_owner_write_not_authorized";
  depends_on: Record<string, unknown>;
  owner_baseline: {
    owner_repo_ref: string;
    owner_repo_path: string;
    head_ref: string;
    owner_repo_write_attempted_by_preview: false;
    baseline_files: Array<{
      path: string;
      sha256: string;
      required_current_text: string[];
    }>;
  };
  previewed_owner_patch: Array<{
    patch_id: string;
    target_path: string;
    target_symbol: string;
    edit_shape: string;
    required_new_text: string[];
    must_preserve: string[];
  }>;
  post_patch_required_validators: Array<{
    command: string;
    required_exit_code: number;
    evidence_id: string;
  }>;
  post_patch_runtime_gate: {
    runtime_retry_authorized_by_preview: false;
    fresh_runtime_retry_approval_required_after_patch: true;
    maximum_runtime_attempts_after_repair: number;
    success_formula: string;
    terminal_cancel_formula: string;
  };
  forbidden_preview_shapes: string[];
  negative_assertions: {
    owner_repo_write_attempted: false;
    owner_patch_applied: false;
    owner_validator_run_claimed: false;
    owner_runtime_invocation_attempted: false;
    runtime_retry_authorized: false;
    real_partial_fill_claimed: false;
    web_ui_real_partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export type AccountHealthPanelFixtureState =
  | "happy_path"
  | "empty"
  | "blocked"
  | "stale"
  | "partial";

export type AccountHealthStateBadge =
  | "healthy"
  | "blocked"
  | "stale"
  | "partial"
  | "empty"
  | "warning";

export type AccountHealthCloseoutState =
  | "complete"
  | "blocked"
  | "stale"
  | "partial"
  | "empty";

export type AccountHealthSettlementState =
  | "settled"
  | "blocked"
  | "stale"
  | "partial"
  | "missing";

export type AccountHealthEquityContinuity =
  | "continuous"
  | "gap"
  | "stale"
  | "partial"
  | "missing";

export type AccountHealthSeverity = "info" | "warning" | "high" | "critical";

export interface AccountHealthPanelContext {
  trading_day: string;
  session_id: string;
  closeout_run_id: string;
  reducer_checkpoint_id: string;
  reducer_checkpoint_ts: string;
  stream_state: AccountHealthStateBadge;
  last_cursor: number;
  source_ref: string;
  checksum: string;
}

export interface AccountHealthPanelSummary {
  total_accounts: number;
  closeout_completed: number;
  closeout_blocked: number;
  settlement_blocked: number;
  stale_or_partial: number;
  open_blockers: number;
}

export interface AccountHealthPanelFilters {
  account_types: AccountKind[];
  closeout_states: AccountHealthCloseoutState[];
  settlement_states: AccountHealthSettlementState[];
  blocker_severities: AccountHealthSeverity[];
}

export interface AccountHealthBlocker {
  blocker_id: string;
  severity: AccountHealthSeverity;
  kind: string;
  owner: string;
  next_diagnostic_ref: string;
  source_ref: string;
}

export interface AccountHealthRow {
  account_id: string;
  account_type: AccountKind;
  owner: string;
  closeout_state: AccountHealthCloseoutState;
  settlement_state: AccountHealthSettlementState;
  equity_continuity: AccountHealthEquityContinuity;
  blocker_count: number;
  source_ref: string;
  checksum: string;
  closeout_run_id: string;
  settlement_run_id: string;
  equity_curve_artifact_id: string;
  latest_blocker_id: string | null;
  last_cursor: number;
  last_checkpoint_ts: string;
  blockers: AccountHealthBlocker[];
}

export interface AccountHealthPanelReadModel {
  schema_version: "account_health_panel.v1";
  workbench: "Daily Closeout";
  panel: "Account Health Panel";
  route: "/closeout";
  fixture_state: AccountHealthPanelFixtureState;
  context: AccountHealthPanelContext;
  summary: AccountHealthPanelSummary;
  filters: AccountHealthPanelFilters;
  accounts: AccountHealthRow[];
}

export interface EvidenceRef {
  kind: string;
  owner: string;
  source_ref: string;
  checksum: string;
  authority: string;
}

export interface P077PaperSliceContext {
  trading_day: string;
  session_id: string;
  projection_owner: string;
  producer_owner: string;
  source_ref: string;
  checksum: string;
  schema_version: string;
  rejection_rules: string[];
}

export interface P077PaperSlice {
  account_alias: string;
  instrument: string;
  side: "BUY" | "SELL";
  quantity: number;
  position_effect: "OPEN" | "CLOSE" | "CLOSETODAY" | "CLOSEYESTERDAY";
  limit_price: number;
  disposition: "filled" | "cancelled" | "rejected" | "blocked" | "unknown";
  fill_volume: number;
  trade_price: number | null;
  pre_position_qty: number;
  post_position_qty: number;
  observed_position_delta: number;
  authorization_consumed: boolean;
  active_authorization: boolean;
}

export interface P077PaperSliceBoundaries {
  read_only_projection: boolean;
  runtime_truth: boolean;
  ledger_truth: boolean;
  ui_truth: boolean;
  paper_ready: boolean;
  live_ready: boolean;
  broker_tradable: boolean;
  admission_truth: boolean;
  capital_truth: boolean;
}

export interface P077PaperSliceBlocker {
  blocker_id: string;
  owner: string;
  reason: string;
  source_ref: string;
  checksum: string;
}

export interface P077PaperSlicePanelReadModel {
  schema_version: "p077_paper_slice_panel.v1";
  workbench: "Order Observation";
  panel: "P077 Paper Slice Evidence Panel";
  route: "/orders/p077-paper-slice";
  fixture_state: "filled_reconciled" | "blocked" | "partial" | "empty";
  context: P077PaperSliceContext;
  slice: P077PaperSlice;
  evidence: EvidenceRef[];
  boundaries: P077PaperSliceBoundaries;
  blockers: P077PaperSliceBlocker[];
}

export type AccountSummaryFixtureState =
  | "happy_path"
  | "empty"
  | "blocked"
  | "stale"
  | "partial"
  | "r1_cta_core_001";

export interface AccountSummaryContext {
  trading_day: string;
  session_id: string;
  run_id: string;
  reducer_checkpoint_id: string;
  reducer_checkpoint_ts: string;
  stream_state: AccountHealthStateBadge;
  projection_owner: "account-console-contracts";
  source_authority: "deterministic_fixture" | "normalized_read_model" | "typed_blocker";
}

export interface AccountSummaryAccount {
  account_id: string;
  account_alias: string;
  account_kind: AccountKind;
  portfolio_uid: string;
  display_state: AccountHealthStateBadge;
  base_currency: string;
}

export interface AccountSummaryBalances {
  cash: number | null;
  frozen_cash: number | null;
  available_cash: number | null;
  buying_power: number | null;
}

export interface AccountSummaryCurrencyBalance {
  currency: string;
  cash: number | null;
  available_cash: number | null;
  buying_power: number | null;
  margin_used: number | null;
  equity: number | null;
  unrealized_pnl: number | null;
  exchange_rate: number | null;
  source_ref: string;
  checksum: string;
}

export interface AccountSummaryPnl {
  realized: number | null;
  unrealized: number | null;
  fees: number | null;
  taxes: number | null;
}

export interface AccountSummaryMargin {
  initial_margin: number | null;
  maintenance_margin: number | null;
  margin_ratio: number | null;
}

export interface AccountSummarySettlement {
  state: AccountHealthSettlementState;
  latest_settlement_ref: string | null;
  position_carryover_ref: string | null;
}

export interface AccountSummaryPosition {
  instrument: string;
  net_qty: number | null;
  market_value: number | null;
  source_ref: string;
  checksum: string;
}

export interface AccountSummaryBlocker {
  blocker_id: string;
  severity: AccountHealthSeverity;
  kind: string;
  owner: string;
  next_action: string;
  source_ref: string;
  checksum: string;
}

export interface AccountSummaryBoundaries extends P077PaperSliceBoundaries {
  action_controls: boolean;
}

export interface AccountSummaryPanelReadModel {
  schema_version: "account_summary_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Summary Panel";
  route: "/accounts/{account_id}";
  fixture_state: AccountSummaryFixtureState;
  context: AccountSummaryContext;
  account: AccountSummaryAccount;
  balances: AccountSummaryBalances;
  pnl: AccountSummaryPnl;
  margin: AccountSummaryMargin;
  settlement: AccountSummarySettlement;
  currency_balances?: AccountSummaryCurrencyBalance[];
  positions: AccountSummaryPosition[];
  blockers: AccountSummaryBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountSummaryBoundaries;
  rejection_rules: string[];
}

export type AccountOrdersFixtureState = "current_orders" | "empty" | "blocked" | "stale";

export type AccountOrderDetailFixtureState = "filled_lifecycle" | "blocked" | "stale";

export interface AccountOrdersContext {
  trading_day: string;
  session_id: string;
  run_id: string;
  reducer_checkpoint_id: string;
  reducer_checkpoint_ts: string;
  stream_state: AccountHealthStateBadge;
  projection_owner: "account-console-contracts";
  source_authority: "deterministic_fixture" | "normalized_read_model" | "typed_blocker";
}

export interface AccountOrdersAccount {
  account_id: string;
  account_alias: string;
  account_kind: AccountKind;
}

export interface AccountOrderRow {
  account_id: string;
  client_order_id: string;
  instrument: string;
  side: "BUY" | "SELL";
  offset: "OPEN" | "CLOSE" | "CLOSETODAY" | "CLOSEYESTERDAY" | "UNKNOWN";
  order_type: "LIMIT" | "MARKET" | "UNKNOWN";
  limit_price: number | null;
  quantity: number | null;
  filled_quantity: number | null;
  remaining_quantity: number | null;
  cancelled_quantity?: number | null;
  time_in_force?: string | null;
  destination?: string | null;
  status:
    | "filled"
    | "working"
    | "canceled"
    | "rejected"
    | "blocked"
    | "stale"
    | "unknown"
    | "partial"
    | "cancel_pending";
  lifecycle_ref: string | null;
  report_provenance_ref: string | null;
  source_ref: string;
  checksum: string;
}

export interface AccountExecutionReportRow {
  account_id: string;
  report_id: string;
  report_type: "OrderStatusReport" | "FillReport";
  client_order_id: string;
  venue_order_id: string | null;
  instrument: string;
  side: "BUY" | "SELL";
  status_or_trade: string;
  quantity: number | null;
  filled_quantity: number | null;
  remaining_quantity: number | null;
  limit_or_last_price: number | null;
  sequence: number | null;
  source_ref: string;
  checksum: string;
  reload_checkpoint_id: string | null;
}

export interface AccountOrdersBlocker {
  blocker_id: string;
  severity: AccountHealthSeverity;
  kind: string;
  owner: string;
  next_action: string;
  source_ref: string;
  checksum: string;
}

export interface AccountOrdersBoundaries extends AccountSummaryBoundaries {
  account_truth: boolean;
  order_truth: boolean;
}

export interface AccountOrdersPanelReadModel {
  schema_version: "account_orders_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Orders Panel";
  route: "/accounts/{account_id}/orders";
  fixture_state: AccountOrdersFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  orders: AccountOrderRow[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export interface AccountOrderLifecycleEvent {
  event_id: string;
  event_seq: number;
  event_type: "accepted" | "submitted" | "filled" | "canceled" | "rejected" | "unknown";
  event_ts: string;
  quantity: number | null;
  price: number | null;
  status: string;
  source_ref: string;
  checksum: string;
  authority: string;
}

export interface AccountOrderDetailPanelReadModel {
  schema_version: "account_order_detail_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Order Detail Panel";
  route: "/accounts/{account_id}/orders/{client_order_id}";
  fixture_state: AccountOrderDetailFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  order: AccountOrderRow;
  events: AccountOrderLifecycleEvent[];
  report_provenance: EvidenceRef[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountPositionsFixtureState =
  | "current_positions"
  | "empty"
  | "blocked"
  | "stale"
  | "partial"
  | "r1_cta_core_001";

export interface AccountPositionRow {
  account_id: string;
  instrument: string;
  direction: "LONG" | "SHORT" | "NET" | "UNKNOWN";
  net_qty: number | null;
  today_qty: number | null;
  yesterday_qty: number | null;
  available_qty: number | null;
  frozen_qty: number | null;
  average_price: number | null;
  market_price: number | null;
  market_value: number | null;
  unrealized_pnl: number | null;
  carryover_ref: string | null;
  settlement_ref: string | null;
  source_ref: string;
  checksum: string;
}

export interface AccountPositionsPanelReadModel {
  schema_version: "account_positions_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Positions Panel";
  route: "/accounts/{account_id}/positions";
  fixture_state: AccountPositionsFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  positions: AccountPositionRow[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountSettlementFixtureState =
  | "current_settlement"
  | "empty"
  | "blocked"
  | "stale"
  | "partial";

export interface AccountSettlementRow {
  trading_day: string;
  settlement_state: AccountHealthSettlementState | "settled";
  previous_settlement_ref: string | null;
  current_settlement_ref: string | null;
  position_carryover_ref: string | null;
  cash: number | null;
  frozen_cash: number | null;
  margin: number | null;
  realized_pnl: number | null;
  unrealized_pnl: number | null;
  fees: number | null;
  taxes: number | null;
  source_ref: string;
  checksum: string;
}

export interface AccountSettlementPanelReadModel {
  schema_version: "account_settlement_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Settlement Panel";
  route: "/accounts/{account_id}/settlement";
  fixture_state: AccountSettlementFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  settlement: AccountSettlementRow;
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountEquityFixtureState =
  | "current_equity"
  | "empty"
  | "blocked"
  | "stale"
  | "partial";

export interface AccountEquityPoint {
  point_ts: string;
  equity: number | null;
  balance: number | null;
  available_cash: number | null;
  margin: number | null;
  ledger_ref: string | null;
  curve_ref: string | null;
  source_ref: string;
  checksum: string;
}

export interface AccountEquityPanelReadModel {
  schema_version: "account_equity_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Equity Panel";
  route: "/accounts/{account_id}/equity";
  fixture_state: AccountEquityFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  equity_points: AccountEquityPoint[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountReconcileFixtureState =
  | "matched"
  | "empty"
  | "mismatch"
  | "stale"
  | "partial"
  | "r1_cta_core_001";

export interface AccountReconcileItem {
  item_id: string;
  category: string;
  severity: AccountHealthSeverity;
  status: "matched" | "mismatch" | "missing" | "stale" | "partial";
  expected_value: number | string | null;
  observed_value: number | string | null;
  delta: number | string | null;
  tolerance_ref: string | null;
  mismatch_ref: string | null;
  owner: string;
  next_action: string;
  source_ref: string;
  checksum: string;
}

export interface AccountReconcilePanelReadModel {
  schema_version: "account_reconcile_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Reconcile Panel";
  route: "/accounts/{account_id}/reconcile";
  fixture_state: AccountReconcileFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  reconcile_items: AccountReconcileItem[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountIncidentsFixtureState =
  | "active_incidents"
  | "empty"
  | "blocked"
  | "stale"
  | "partial";

export interface AccountIncidentRow {
  incident_id: string;
  category: string;
  severity: AccountHealthSeverity;
  status: "open" | "blocked" | "stale" | "partial" | "closed";
  owner: string;
  next_action: string;
  repair_ref: string | null;
  source_ref: string;
  checksum: string;
}

export interface AccountIncidentsPanelReadModel {
  schema_version: "account_incidents_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Incidents Panel";
  route: "/accounts/{account_id}/incidents";
  fixture_state: AccountIncidentsFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  incidents: AccountIncidentRow[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type AccountEvidenceFixtureState =
  | "current_evidence"
  | "empty"
  | "blocked"
  | "stale"
  | "partial"
  | "r1_cta_core_001";

export interface AccountEvidencePackage {
  package_id: string;
  kind: string;
  status: "current" | "blocked" | "stale" | "partial" | "empty";
  owner: string;
  schema_ref: string;
  schema_version_ref: string;
  checksum: string;
  run_id: string | null;
  session_id: string;
  trading_day: string;
  source_ref: string;
  normalized_ref: string | null;
  raw_payload_ref: string | null;
  next_action: string;
}

export interface AccountEvidencePanelReadModel {
  schema_version: "account_evidence_panel.v1";
  workbench: "Account Workbench";
  panel: "Account Evidence Panel";
  route: "/accounts/{account_id}/evidence";
  fixture_state: AccountEvidenceFixtureState;
  context: AccountOrdersContext;
  account: AccountOrdersAccount;
  evidence_packages: AccountEvidencePackage[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}

export type IntradayMonitorFixtureState = "current" | "empty" | "blocked" | "stale" | "partial";

export interface IntradayMonitorContext {
  trading_day: string;
  session_id: string;
  monitor_checkpoint_id: string;
  monitor_checkpoint_ts: string;
  stream_state: AccountHealthStateBadge;
  projection_owner: "account-console-contracts";
  source_authority: "deterministic_fixture" | "normalized_read_model" | "typed_blocker";
}

export interface IntradayMonitorLagSummary {
  max_lag_ms: number | null;
  stale_stream_count: number;
  open_incident_count: number;
  blocked_source_count: number;
}

export interface IntradayMonitorExceptionRow {
  exception_id: string;
  kind: "stale_stream" | "lag_spike" | "incident" | "source_blocker" | "reconcile_gap";
  severity: AccountHealthSeverity;
  owner: string;
  next_action: string;
  source_ref: string;
  checksum: string;
}

export interface IntradayMonitorStreamStateRow {
  stream_id: string;
  state: AccountHealthStateBadge;
  last_event_ts: string | null;
  lag_ms: number | null;
  source_ref: string;
  checksum: string;
}

export interface IntradayMonitorIncidentRow {
  incident_id: string;
  category: "outage" | "stale_order" | "reconcile_gap" | "writer_failure" | "source_blocker" | "lag_spike";
  severity: AccountHealthSeverity;
  status: "open" | "blocked" | "stale" | "partial";
  owner: string;
  next_action: string;
  source_ref: string;
  checksum: string;
}

export interface IntradayMonitorPanelReadModel {
  schema_version: "intraday_monitor_panel.v1";
  workbench: "Intraday Monitor";
  panel: "Intraday Monitor Exception Queue Panel";
  route: "/monitor";
  fixture_state: IntradayMonitorFixtureState;
  context: IntradayMonitorContext;
  lag_summary: IntradayMonitorLagSummary;
  exceptions: IntradayMonitorExceptionRow[];
  streams: IntradayMonitorStreamStateRow[];
  incidents: IntradayMonitorIncidentRow[];
  blockers: AccountOrdersBlocker[];
  source_refs: EvidenceRef[];
  boundaries: AccountOrdersBoundaries;
  rejection_rules: string[];
}
