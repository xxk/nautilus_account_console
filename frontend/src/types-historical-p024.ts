import type { CommandApiBlocker } from "./types-shared";

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

export interface CommandPartialFillOwnerRepairApprovalPacket {
  schema: "account-console.p024.partial-fill-owner-repair-approval-packet.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4p_owner_close_offset_repair_approval_packet_ready";
  verdict: "owner_repair_approval_required_before_retry";
  depends_on: Record<string, unknown>;
  current_thread_approval_assessment: {
    approval_text_observed: boolean;
    approval_scope: string;
    approval_path: string;
    approved_expected_impact: string;
    matches_current_next_action: false;
    reason: string;
    runtime_retry_authorized_by_this_packet: false;
    owner_code_repair_authorized_by_this_packet: false;
  };
  required_owner_repair_approval: {
    required: true;
    obtained: false;
    approval_path: string;
    exact_approval_text_required: string;
    reason: string;
  };
  required_owner_repair_scope: {
    owner_repo_ref: string;
    owner_repo_path: string;
    allowed_write_scope_after_approval: string[];
    expected_owner_changes: string[];
    required_owner_validators_before_retry: string[];
    required_account_console_followup_before_retry: string[];
  };
  retry_gate: {
    additional_partial_fill_order_authorized: false;
    runtime_invocation_allowed: false;
    owner_repair_required_first: true;
    owner_repair_evidence_required: true;
    fresh_post_repair_runtime_attempt_approval_required: true;
    reason: string;
  };
  residual_blockers: Array<{
    blocker_id: string;
    type: string;
    next_action: string;
  }>;
  negative_assertions: {
    owner_repo_write_attempted_by_this_packet: false;
    owner_runtime_invocation_attempted: false;
    owner_code_repair_authorized_by_current_thread_text: false;
    additional_order_authorized: false;
    partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillRemainingAcceptanceCurrentState {
  schema: "account-console.p024.partial-fill-remaining-acceptance-current-state.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4q_remaining_acceptance_current_state_audited";
  verdict: "not_fully_accepted_pending_owner_repair_and_real_partial_fill";
  current_authoritative_state: {
    account_console_worktree_clean_at_review: boolean;
    owner_repo_code_change_recorded_for_close_offset_repair: false;
    owner_repo_runtime_artifacts_present: boolean;
    latest_real_partial_fill_attempt_classification: string;
    latest_owner_repair_gate: string;
    full_acceptance_claimed: false;
  };
  accepted_evidence_groups: Array<{
    group_id: string;
    status: string;
    evidence_refs: string[];
  }>;
  remaining_acceptance_requirements: Array<{
    requirement_id: string;
    required_evidence_shape: string;
    current_status: "missing";
    current_blocker_id?: string;
    required_commands?: string[];
  }>;
  next_authorized_action: {
    owner_code_repair_allowed: false;
    owner_runtime_retry_allowed: false;
    account_console_only_work_allowed: true;
    required_exact_approval_before_owner_repair_or_retry: string;
  };
  negative_assertions: {
    full_acceptance_claimed: false;
    owner_repair_claimed: false;
    post_repair_runtime_retry_claimed: false;
    real_partial_fill_claimed: false;
    web_ui_real_partial_fill_claimed: false;
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

export interface CommandPartialFillOwnerRepairEvidenceIngestAudit {
  schema: "account-console.p024.partial-fill-owner-repair-evidence-ingest-audit.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4zd_owner_repair_evidence_ingested";
  verdict: "owner_repair_evidence_recorded_runtime_retry_packet_required";
  depends_on: Record<string, unknown>;
  owner_repair_evidence: {
    owner_repo_ref: string;
    owner_repo_path: string;
    owner_branch_or_ref: string;
    owner_repair_commit_ref: string;
    owner_repair_commit_subject: string;
    approval_text_ref: string;
    owner_repo_write_attempted: boolean;
    owner_runtime_invocation_attempted: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
  post_repair_source_checksums: Array<{
    path: string;
    sha256: string;
    required_symbol: string;
    repair_assertion: string;
  }>;
  owner_validator_refs: Array<{
    evidence_id: string;
    command: string;
    exit_code: number;
    stdout_tail: string;
    validator_run_sha256: string;
  }>;
  ingest_decision: {
    owner_repair_evidence_recorded: true;
    owner_validators_passed: true;
    account_console_approval_packets_updated: boolean;
    runtime_retry_authorized: false;
    requires_post_repair_runtime_retry_packet: true;
    maximum_runtime_attempts_after_repair: number;
  };
  remaining_runtime_evidence_required: string[];
  negative_assertions: {
    owner_runtime_invocation_attempted: false;
    post_repair_runtime_retry_claimed: false;
    real_partial_fill_claimed: false;
    web_ui_real_partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillPostRepairRuntimeRetryApprovalPacket {
  schema: "account-console.p024.partial-fill-post-repair-runtime-retry-approval-packet.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4ze_post_repair_runtime_retry_approval_packet_ready";
  verdict: "one_guarded_post_repair_paper_attempt_authorized";
  depends_on: Record<string, unknown>;
  operator_approval: {
    approval_obtained: true;
    approval_path: string;
    approval_text_ref: string;
    scope: string;
    expected_impact: string;
  };
  runtime_retry_guard: {
    runtime_retry_authorized_by_packet: true;
    maximum_attempts: number;
    account_id: "acct.ctp.paper.19053";
    simulation_user: string;
    mode: "paper_armed";
    exposure_reduction_only: true;
    small_order_only: true;
    owner_repo_ref: string;
    owner_repo_path: string;
    submit_entrypoint_ref: string;
    cancel_entrypoint_ref: string;
    owner_config_ref: string;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
  required_runtime_evidence: string[];
  success_formula: Record<string, string>;
  fallback_if_not_partial: Record<string, unknown>;
  negative_assertions_before_runtime: {
    owner_runtime_invocation_attempted_by_packet: false;
    paper_order_created_by_packet: false;
    paper_cancel_sent_by_packet: false;
    real_partial_fill_claimed: false;
    web_ui_real_partial_fill_claimed: false;
    full_acceptance_claimed: false;
    raw_secret_values_recorded: false;
    raw_broker_endpoint_recorded: false;
    config_raw_content_recorded: false;
  };
}

export interface CommandPartialFillPostRepairRuntimeAttemptAudit {
  schema: "account-console.p024.partial-fill-post-repair-runtime-attempt-audit.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4zf_post_repair_runtime_attempt_full_fill_blocker_recorded";
  verdict: "real_paper_order_filled_not_partial_fill_no_cancel_remainder";
  depends_on: Record<string, unknown>;
  owner_runtime_attempt: Record<string, unknown>;
  owner_artifact_refs: Array<{ artifact_id: string; ref: string; sha256: string }>;
  runtime_observation: Record<string, unknown>;
  position_readback_delta: Record<string, unknown>;
  acceptance_decision: Record<string, unknown>;
  negative_assertions: Record<string, boolean>;
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

export interface CommandPartialFillOwnerRepairExecutionHandoffBundle {
  schema: "account-console.p024.partial-fill-owner-repair-execution-handoff-bundle.v1";
  proposal_id: "p024-account-console-paper-command-controls";
  account_id: "acct.ctp.paper.19053";
  reviewed_at: string;
  status: "phase4z_owner_repair_execution_handoff_bundle_ready";
  verdict: "handoff_bundle_ready_owner_write_not_invoked";
  depends_on: Record<string, unknown>;
  execution_guard: {
    execution_allowed: false;
    owner_repo_write_allowed_by_this_bundle: false;
    owner_runtime_invocation_allowed_by_this_bundle: false;
    runtime_retry_authorized_by_this_bundle: false;
    requires_exact_owner_repair_approval: true;
    required_exact_approval_text: string;
  };
  owner_repo_context: {
    owner_repo_ref: string;
    owner_repo_path: string;
    baseline_head_ref: string;
    patch_preview_ref: string;
  };
  operator_sequence_after_exact_approval: Array<{
    step: string;
    command?: string;
    required_output_shape: string;
    execution_allowed_before_approval: false;
  }>;
  required_post_handoff_artifacts: string[];
  success_criteria_before_runtime_retry: string[];
  negative_assertions: {
    execution_allowed: false;
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
