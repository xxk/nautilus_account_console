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
}

export interface MirrorCapabilities {
  observation: MirrorCapabilityState;
  command: MirrorCapabilityState;
}

export interface MirrorAccountSummary {
  account_id: string;
  display_alias: string;
  source_kind: string;
  source_mode: string;
  account_domain: string;
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
  blockers: Record<string, unknown>[];
  projection_checkpoint_id: string;
  projection_checksum: string;
  source_ref: string;
  source_checksum: string;
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
  | "partial";

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
  status: "filled" | "working" | "canceled" | "rejected" | "blocked" | "stale" | "unknown" | "partial";
  lifecycle_ref: string | null;
  report_provenance_ref: string | null;
  source_ref: string;
  checksum: string;
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
  | "partial";

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
  | "partial";

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
  | "partial";

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
