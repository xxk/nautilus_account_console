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

