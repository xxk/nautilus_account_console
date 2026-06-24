import type {
  AccountHealthPanelReadModel,
  AccountHealthRow,
  AccountExecutionReportRow,
  AccountEvidencePanelReadModel,
  AccountEvidencePackage,
  AccountKind,
  AccountOrderDetailPanelReadModel,
  AccountOrderLifecycleEvent,
  AccountOrderRow,
  AccountOrdersPanelReadModel,
  AccountPositionRow,
  AccountPositionsPanelReadModel,
  AccountReconcileItem,
  AccountReconcilePanelReadModel,
  AccountSettlementPanelReadModel,
  AccountSummaryBlocker,
  AccountSummaryPanelReadModel,
  AccountIncidentsPanelReadModel,
  AccountIncidentRow,
  AccountEquityPanelReadModel,
  AccountEquityPoint,
  CancelIntentRequest,
  MirrorAccountProjection,
  MirrorAccountSummary,
  MirrorEvidenceResponse,
  MirrorSourceHealthResponse,
  OrderIntentRequest
} from "./types";
import { stateTone } from "./ui-primitives";

export interface MirrorWorkbenchReadback {
  accounts: MirrorAccountSummary[];
  selected: MirrorAccountProjection;
  sourceHealth: MirrorSourceHealthResponse | null;
  evidence: MirrorEvidenceResponse | null;
}

export interface AccountWorkbenchProjection {
  summary: AccountSummaryPanelReadModel;
  orders: AccountOrdersPanelReadModel;
  orderDetail: AccountOrderDetailPanelReadModel;
  positions: AccountPositionsPanelReadModel;
  settlement: AccountSettlementPanelReadModel;
  equity: AccountEquityPanelReadModel;
  reconcile: AccountReconcilePanelReadModel;
  incidents: AccountIncidentsPanelReadModel;
  evidence: AccountEvidencePanelReadModel;
}

function blockerSeverity(type: string): AccountHealthRow["blockers"][number]["severity"] {
  if (type.includes("missing") || type.includes("unavailable")) {
    return "high";
  }
  if (type.includes("stale")) {
    return "warning";
  }
  return "info";
}

export function mirrorBlockers(blockers: Record<string, unknown>[]): AccountSummaryBlocker[] {
  const seen = new Set<string>();
  return blockers.flatMap((blocker, index) => {
    const kind = asText(blocker.type, "source_blocker");
    const blockerId = asText(blocker.blocker_id, `mirror-blocker-${index}`);
    const checksum = asText(
      blocker.checksum,
      "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    );
    const key = `${blockerId}-${checksum}`;
    if (seen.has(key)) {
      return [];
    }
    seen.add(key);
    return [{
      blocker_id: blockerId,
      severity: blockerSeverity(kind),
      kind,
      owner: asText(blocker.owner, "external_source_owner"),
      next_action: asText(
        blocker.next_action,
        "Resolve source evidence before accepting account consistency."
      ),
      source_ref: asText(blocker.source_ref, "missing_source_ref"),
      checksum
    }];
  });
}

export function mirrorEvidenceRefs(readback: MirrorWorkbenchReadback) {
  if (readback.evidence) {
    return readback.evidence.evidence;
  }
  return [
    {
      kind: "source_package",
      owner: readback.selected.source_kind,
      source_ref: readback.selected.source_ref,
      checksum: readback.selected.source_checksum,
      authority: "source artifact provenance; not broker or account truth"
    },
    {
      kind: "mirror_projection",
      owner: "account-console-backend",
      source_ref: readback.selected.projection_checkpoint_id,
      checksum: readback.selected.projection_checksum,
      authority: "Account Mirror read-only projection checkpoint"
    }
  ];
}

export function mirrorContext(readback: MirrorWorkbenchReadback) {
  const health = readback.sourceHealth;
  return {
    trading_day: "2026-06-15",
    session_id: `${readback.selected.source_kind}.${readback.selected.display_alias}`,
    run_id: readback.selected.source_ref,
    reducer_checkpoint_id: readback.selected.projection_checkpoint_id,
    reducer_checkpoint_ts: health?.observed_at ?? asText(readback.selected.source_health.observed_at, "unknown"),
    stream_state: stateTone(
      readback.selected.capabilities.observation.mirror_state ?? "blocked"
    ) as AccountHealthPanelReadModel["context"]["stream_state"],
    projection_owner: "account-console-contracts" as const,
    source_authority: readback.selected.blockers.length > 0
      ? "typed_blocker" as const
      : "normalized_read_model" as const
  };
}

export function mirrorBoundaries(readback: MirrorWorkbenchReadback) {
  return {
    read_only_projection: readback.selected.boundaries.read_only_projection === true,
    runtime_truth: readback.selected.boundaries.runtime_truth === true,
    ledger_truth: false,
    ui_truth: false,
    paper_ready: false,
    live_ready: false,
    broker_tradable: false,
    admission_truth: false,
    capital_truth: readback.selected.boundaries.capital_truth === true,
    broker_truth: readback.selected.boundaries.broker_truth === true,
    action_controls: readback.selected.boundaries.order_action === true,
    account_truth: readback.selected.boundaries.account_truth === true,
    order_truth: false
  };
}

export function mirrorSummaryReadModel(readback: MirrorWorkbenchReadback): AccountSummaryPanelReadModel {
  const selected = readback.selected;
  const balance = selected.balances.find((row) => row.currency === "USD") ?? selected.balances[0] ?? {};
  const blockers = mirrorBlockers([...(selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]);
  const currencyBalances = selected.balances
    .filter((row) => row.currency !== "BASE")
    .map((row) => ({
      currency: asText(row.currency, "unknown"),
      cash: asNumber(row.cash ?? row.total_cash ?? row.equity),
      available_cash: asNumber(row.available_cash),
      buying_power: asNumber(row.available_cash),
      margin_used: asNumber(row.margin_used),
      equity: asNumber(row.equity ?? row.net_liquidation_by_currency),
      unrealized_pnl: asNumber(row.unrealized_pnl),
      exchange_rate: asNumber(row.exchange_rate),
      source_ref: asText(row.source_ref, selected.source_ref),
      checksum: asText(row.checksum, selected.source_checksum)
    }));
  return {
    schema_version: "account_summary_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Summary Panel",
    route: "/accounts/{account_id}",
    fixture_state: blockers.length > 0 ? "blocked" : "happy_path",
    context: mirrorContext(readback),
    account: {
      account_id: selected.account_id,
      account_alias: selected.display_alias,
      account_kind: accountKindFromDomain(selected.account_domain),
      portfolio_uid: asText(selected.source_health.account_uid, selected.source_ref),
      display_state: stateTone(
        selected.capabilities.observation.mirror_state ?? "blocked"
      ) as AccountHealthPanelReadModel["context"]["stream_state"],
      base_currency: asText(balance.currency, "CNY")
    },
    balances: {
      cash: asNumber(balance.equity),
      frozen_cash: asNumber(balance.frozen_cash),
      available_cash: asNumber(balance.available_cash),
      buying_power: asNumber(balance.available_cash)
    },
    pnl: {
      realized: null,
      unrealized: asNumber(balance.unrealized_pnl ?? balance.position_profit),
      fees: null,
      taxes: null
    },
    margin: {
      initial_margin: asNumber(balance.margin_used),
      maintenance_margin: null,
      margin_ratio: null
    },
    settlement: {
      state: blockers.length > 0 ? "blocked" : "settled",
      latest_settlement_ref: selected.source_ref,
      position_carryover_ref: selected.source_ref
    },
    currency_balances: currencyBalances,
    positions: selected.positions.map((position) => ({
      instrument: asText(position.instrument),
      net_qty: asNumber(position.net_qty),
      market_value: null,
      source_ref: asText(position.source_ref, selected.source_ref),
      checksum: asText(position.checksum, selected.source_checksum)
    })),
    blockers,
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Do not treat Account Console mirror readback as broker truth.",
      "Do not infer command capability from account domain or source kind."
    ]
  };
}

export function mirrorPositionsReadModel(readback: MirrorWorkbenchReadback): AccountPositionsPanelReadModel {
  return {
    schema_version: "account_positions_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Positions Panel",
    route: "/accounts/{account_id}/positions",
    fixture_state: readback.selected.blockers.length > 0 ? "blocked" : "current_positions",
    context: mirrorContext(readback),
    account: {
      account_id: readback.selected.account_id,
      account_alias: readback.selected.display_alias,
      account_kind: accountKindFromDomain(readback.selected.account_domain)
    },
    positions: readback.selected.positions.map((position) => ({
      account_id: readback.selected.account_id,
      instrument: asText(position.instrument),
      direction: directionLabel(position.direction),
      net_qty: asNumber(position.net_qty),
      today_qty: asNumber(position.today_qty),
      yesterday_qty: asNumber(position.yesterday_qty),
      available_qty: asNumber(position.available_qty),
      frozen_qty: asNumber(position.frozen_qty),
      average_price: asNumber(position.avg_price),
      market_price: null,
      market_value: null,
      unrealized_pnl: asNumber(position.unrealized_pnl),
      carryover_ref: readback.selected.source_ref,
      settlement_ref: readback.selected.source_ref,
      source_ref: asText(position.source_ref, readback.selected.source_ref),
      checksum: asText(position.checksum, readback.selected.source_checksum)
    })),
    blockers: mirrorBlockers(readback.selected.blockers),
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: ["Do not display positions without source refs and checksums."]
  };
}

export function mirrorOrdersReadModel(readback: MirrorWorkbenchReadback): AccountOrdersPanelReadModel {
  return {
    schema_version: "account_orders_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Orders Panel",
    route: "/accounts/{account_id}/orders",
    fixture_state: readback.selected.blockers.length > 0 ? "blocked" : "current_orders",
    context: mirrorContext(readback),
    account: {
      account_id: readback.selected.account_id,
      account_alias: readback.selected.display_alias,
      account_kind: accountKindFromDomain(readback.selected.account_domain)
    },
    orders: readback.selected.orders.map((order) => {
      const quantity = asNumber(order.quantity);
      const filledQuantity = asNumber(order.filled_quantity) ?? 0;
      const remainingQuantity = asNumber(order.remaining_quantity);
      return {
        account_id: readback.selected.account_id,
        client_order_id: asText(order.client_order_id),
        instrument: asText(order.instrument),
        side: sideLabel(order.side),
        offset: "UNKNOWN",
        order_type: orderTypeLabel(order.order_type),
        limit_price: asNumber(order.limit_price ?? order.price),
        quantity,
        filled_quantity: filledQuantity,
        remaining_quantity: remainingQuantity ?? (quantity === null ? null : quantity - filledQuantity),
        cancelled_quantity: asNumber(order.cancelled_quantity ?? order.withdrawn_quantity),
        time_in_force: asText(order.time_in_force, "missing"),
        destination: asText(order.destination ?? order.exchange, "missing"),
        status: orderStatusLabel(order.status),
        lifecycle_ref: asText(order.venue_order_id, readback.selected.source_ref),
        report_provenance_ref: asText(order.report_provenance_ref, readback.selected.source_ref),
        source_ref: asText(order.source_ref, readback.selected.source_ref),
        checksum: asText(order.checksum, readback.selected.source_checksum)
      };
    }),
    blockers: mirrorBlockers(readback.selected.blockers),
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: ["Do not treat gateway acknowledgements as final account state without mirror readback."]
  };
}

function mirrorAccount(readback: MirrorWorkbenchReadback) {
  return {
    account_id: readback.selected.account_id,
    account_alias: readback.selected.display_alias,
    account_kind: accountKindFromDomain(readback.selected.account_domain)
  };
}

function mirrorOrderRows(readback: MirrorWorkbenchReadback): AccountOrderRow[] {
  return readback.selected.orders.map((order) => {
    const quantity = asNumber(order.quantity);
    const filledQuantity = asNumber(order.filled_quantity) ?? 0;
    const remainingQuantity = asNumber(order.remaining_quantity);
    return {
      account_id: readback.selected.account_id,
      client_order_id: asText(order.client_order_id),
      instrument: asText(order.instrument),
      side: sideLabel(order.side),
      offset: "UNKNOWN",
      order_type: orderTypeLabel(order.order_type),
      limit_price: asNumber(order.limit_price ?? order.price),
      quantity,
      filled_quantity: filledQuantity,
      remaining_quantity: remainingQuantity ?? (quantity === null ? null : quantity - filledQuantity),
      cancelled_quantity: asNumber(order.cancelled_quantity ?? order.withdrawn_quantity),
      time_in_force: asText(order.time_in_force, "missing"),
      destination: asText(order.destination ?? order.exchange, "missing"),
      status: orderStatusLabel(order.status),
      lifecycle_ref: asText(order.venue_order_id, readback.selected.source_ref),
      report_provenance_ref: asText(order.report_provenance_ref, readback.selected.source_ref),
      source_ref: asText(order.source_ref, readback.selected.source_ref),
      checksum: asText(order.checksum, readback.selected.source_checksum)
    };
  });
}

function mirrorPositionRows(readback: MirrorWorkbenchReadback): AccountPositionRow[] {
  return readback.selected.positions.map((position) => ({
    account_id: readback.selected.account_id,
    instrument: asText(position.instrument),
    direction: directionLabel(position.direction),
    net_qty: asNumber(position.net_qty),
    today_qty: asNumber(position.today_qty),
    yesterday_qty: asNumber(position.yesterday_qty),
    available_qty: asNumber(position.available_qty),
    frozen_qty: asNumber(position.frozen_qty),
    average_price: asNumber(position.avg_price),
    market_price: null,
    market_value: null,
    unrealized_pnl: asNumber(position.unrealized_pnl),
    carryover_ref: readback.selected.source_ref,
    settlement_ref: readback.selected.source_ref,
    source_ref: asText(position.source_ref, readback.selected.source_ref),
    checksum: asText(position.checksum, readback.selected.source_checksum)
  }));
}

function mirrorLifecycleEvents(readback: MirrorWorkbenchReadback, clientOrderId: string): AccountOrderLifecycleEvent[] {
  const orderEvents = readback.selected.orders
    .filter((order) => asText(order.client_order_id) === clientOrderId)
    .map((order, index) => ({
      event_id: asText(order.report_id, `${clientOrderId}-order-${index + 1}`),
      event_seq: asNumber(order.seq) ?? index + 1,
      event_type: mirrorEventType(order.order_status ?? order.status),
      event_ts: asText(order.updated_at ?? order.event_ts ?? order.source_ref, readback.selected.source_ref),
      quantity: asNumber(order.quantity),
      price: asNumber(order.price),
      status: reportStatusLabel(order.order_status ?? order.status),
      source_ref: asText(order.source_ref ?? order.report_provenance_ref, readback.selected.source_ref),
      checksum: asText(order.source_checksum ?? order.checksum, readback.selected.source_checksum),
      authority: "mirror order status projection"
    }));
  const fillEvents = readback.selected.fills
    .filter((fill) => asText(fill.client_order_id) === clientOrderId)
    .map((fill, index) => ({
      event_id: asText(fill.report_id, asText(fill.trade_id, `${clientOrderId}-fill-${index + 1}`)),
      event_seq: asNumber(fill.seq) ?? orderEvents.length + index + 1,
      event_type: "filled" as const,
      event_ts: asText(fill.trade_time ?? fill.event_ts ?? fill.source_ref, readback.selected.source_ref),
      quantity: asNumber(fill.last_qty ?? fill.quantity),
      price: asNumber(fill.last_px ?? fill.price),
      status: reportStatusLabel(fill.order_status ?? fill.trade_id),
      source_ref: asText(fill.source_ref, readback.selected.source_ref),
      checksum: asText(fill.source_checksum ?? fill.checksum, readback.selected.source_checksum),
      authority: "mirror fill projection"
    }));
  return [...orderEvents, ...fillEvents].sort((left, right) => left.event_seq - right.event_seq);
}

function mirrorEventType(value: unknown): AccountOrderLifecycleEvent["event_type"] {
  const normalized = asText(value).toLowerCase();
  if (normalized === "accepted" || normalized === "submitted" || normalized === "presubmitted" || normalized === "working") {
    return normalized === "accepted" ? "accepted" : "submitted";
  }
  if (normalized === "filled" || normalized === "alltraded") {
    return "filled";
  }
  if (normalized === "canceled" || normalized === "cancelled" || normalized === "cancel_pending") {
    return "canceled";
  }
  if (normalized === "rejected") {
    return "rejected";
  }
  return "unknown";
}

function mirrorSettlementReadModel(readback: MirrorWorkbenchReadback): AccountSettlementPanelReadModel {
  const summary = mirrorSummaryReadModel(readback);
  return {
    schema_version: "account_settlement_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Settlement Panel",
    route: "/accounts/{account_id}/settlement",
    fixture_state: summary.fixture_state === "blocked" ? "blocked" : "current_settlement",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    settlement: {
      trading_day: summary.context.trading_day,
      settlement_state: summary.settlement.state,
      previous_settlement_ref: null,
      current_settlement_ref: summary.settlement.latest_settlement_ref,
      position_carryover_ref: summary.settlement.position_carryover_ref,
      cash: summary.balances.cash,
      frozen_cash: summary.balances.frozen_cash,
      margin: summary.margin.initial_margin,
      realized_pnl: summary.pnl.realized,
      unrealized_pnl: summary.pnl.unrealized,
      fees: summary.pnl.fees,
      taxes: summary.pnl.taxes,
      source_ref: readback.selected.source_ref,
      checksum: readback.selected.source_checksum
    },
    blockers: mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]),
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject this mirror projection as settlement or ledger authority.",
      "Reject successful settlement display without source refs and carryover refs."
    ]
  };
}

function mirrorEquityReadModel(readback: MirrorWorkbenchReadback): AccountEquityPanelReadModel {
  const points: AccountEquityPoint[] = readback.selected.balances.map((balance, index) => ({
    point_ts: asText(balance.observed_at ?? balance.snapshot_ts, readback.sourceHealth?.observed_at ?? readback.selected.source_ref),
    equity: asNumber(balance.equity ?? balance.net_liquidation_by_currency),
    balance: asNumber(balance.total_cash ?? balance.equity),
    available_cash: asNumber(balance.available_cash),
    margin: asNumber(balance.margin_used),
    ledger_ref: null,
    curve_ref: null,
    source_ref: asText(balance.source_ref, `${readback.selected.source_ref}#balance-${index + 1}`),
    checksum: asText(balance.checksum, readback.selected.source_checksum)
  }));
  return {
    schema_version: "account_equity_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Equity Panel",
    route: "/accounts/{account_id}/equity",
    fixture_state: readback.selected.blockers.length > 0 ? "blocked" : "current_equity",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    equity_points: points,
    blockers: mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]),
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject this mirror equity curve as ledger authority.",
      "Reject trend claims when the projection has blockers or stale source health."
    ]
  };
}

function mirrorReconcileReadModel(readback: MirrorWorkbenchReadback): AccountReconcilePanelReadModel {
  const blockers = mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]);
  const items: AccountReconcileItem[] = blockers.map((blocker, index) => ({
    item_id: blocker.blocker_id,
    category: blocker.kind,
    severity: blocker.severity,
    status: blocker.kind.includes("stale") ? "stale" : blocker.kind.includes("missing") ? "missing" : "partial",
    expected_value: null,
    observed_value: null,
    delta: null,
    tolerance_ref: null,
    mismatch_ref: blocker.source_ref,
    owner: blocker.owner,
    next_action: blocker.next_action,
    source_ref: blocker.source_ref,
    checksum: blocker.checksum || `${readback.selected.source_checksum}-${index + 1}`
  }));
  return {
    schema_version: "account_reconcile_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Reconcile Panel",
    route: "/accounts/{account_id}/reconcile",
    fixture_state: items.length > 0 ? "partial" : "matched",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    reconcile_items: items,
    blockers,
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject reconcile display as proof of account or ledger truth.",
      "Treat blocker-derived reconcile rows as review obligations, not repairs."
    ]
  };
}

function mirrorIncidentsReadModel(readback: MirrorWorkbenchReadback): AccountIncidentsPanelReadModel {
  const blockers = mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]);
  const incidents: AccountIncidentRow[] = blockers.map((blocker) => ({
    incident_id: blocker.blocker_id,
    category: blocker.kind,
    severity: blocker.severity,
    status: blocker.kind.includes("stale") ? "stale" : blocker.kind.includes("missing") ? "blocked" : "partial",
    owner: blocker.owner,
    next_action: blocker.next_action,
    repair_ref: null,
    source_ref: blocker.source_ref,
    checksum: blocker.checksum
  }));
  return {
    schema_version: "account_incidents_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Incidents Panel",
    route: "/accounts/{account_id}/incidents",
    fixture_state: incidents.length > 0 ? "blocked" : "empty",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    incidents,
    blockers,
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject mirror incidents as repair completion proof.",
      "Treat blocker-derived incidents as governance prompts only."
    ]
  };
}

function mirrorEvidencePackages(readback: MirrorWorkbenchReadback): AccountEvidencePackage[] {
  const evidenceItems = readback.evidence?.evidence ?? mirrorEvidenceRefs(readback);
  return evidenceItems.map((item, index) => ({
    package_id: `mirror-evidence-${index + 1}`,
    kind: item.kind,
    status: "current",
    owner: item.owner,
    schema_ref: "mirror://account-console/evidence",
    schema_version_ref: "account_mirror_evidence.v1",
    checksum: item.checksum,
    run_id: readback.selected.projection_checkpoint_id,
    session_id: readback.selected.account_id,
    trading_day: mirrorContext(readback).trading_day,
    source_ref: item.source_ref,
    normalized_ref: item.source_ref,
    raw_payload_ref: null,
    next_action: "review source-linked evidence before making authority claims"
  }));
}

function mirrorEvidenceReadModel(readback: MirrorWorkbenchReadback): AccountEvidencePanelReadModel {
  return {
    schema_version: "account_evidence_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Evidence Panel",
    route: "/accounts/{account_id}/evidence",
    fixture_state: readback.selected.blockers.length > 0 ? "partial" : "current_evidence",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    evidence_packages: mirrorEvidencePackages(readback),
    blockers: mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]),
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject evidence package display as runtime, ledger, account or reconcile authority.",
      "Reject mirror evidence rows as write authorization or runtime readiness."
    ]
  };
}

function mirrorOrderDetailReadModel(
  readback: MirrorWorkbenchReadback,
  routeOrderId: string
): AccountOrderDetailPanelReadModel {
  const orders = mirrorOrderRows(readback);
  const order =
    orders.find(
      (candidate) =>
        candidate.client_order_id === routeOrderId ||
        candidate.lifecycle_ref === routeOrderId
    ) ?? orders[0];
  const blockers = mirrorBlockers([...(readback.selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]);
  return {
    schema_version: "account_order_detail_panel.v1",
    workbench: "Account Workbench",
    panel: "Account Order Detail Panel",
    route: "/accounts/{account_id}/orders/{client_order_id}",
    fixture_state: blockers.length > 0 ? "blocked" : "filled_lifecycle",
    context: mirrorContext(readback),
    account: mirrorAccount(readback),
    order,
    events: mirrorLifecycleEvents(readback, order?.client_order_id ?? ""),
    report_provenance: mirrorEvidenceRefs(readback),
    blockers,
    source_refs: mirrorEvidenceRefs(readback),
    boundaries: mirrorBoundaries(readback),
    rejection_rules: [
      "Reject lifecycle display as broker finality without owner-side evidence.",
      "Reject missing source refs or checksums as acceptable order detail state."
    ]
  };
}

export function mirrorWorkbenchProjection(
  readback: MirrorWorkbenchReadback,
  routeOrderId: string
): AccountWorkbenchProjection {
  const summary = mirrorSummaryReadModel(readback);
  const orders = mirrorOrdersReadModel(readback);
  const positions = mirrorPositionsReadModel(readback);
  return {
    summary,
    orders,
    orderDetail: mirrorOrderDetailReadModel(readback, routeOrderId),
    positions,
    settlement: mirrorSettlementReadModel(readback),
    equity: mirrorEquityReadModel(readback),
    reconcile: mirrorReconcileReadModel(readback),
    incidents: mirrorIncidentsReadModel(readback),
    evidence: mirrorEvidenceReadModel(readback)
  };
}

export function asNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

export function asText(value: unknown, fallback = "unknown"): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

export function directionLabel(value: unknown): "LONG" | "SHORT" | "NET" | "UNKNOWN" {
  const normalized = asText(value).toUpperCase();
  if (normalized === "LONG" || normalized === "SHORT" || normalized === "NET") {
    return normalized;
  }
  return "UNKNOWN";
}

export function sideLabel(value: unknown): "BUY" | "SELL" {
  return asText(value).toUpperCase() === "SELL" ? "SELL" : "BUY";
}

export function orderStatusLabel(value: unknown): AccountOrderRow["status"] {
  const normalized = asText(value).toLowerCase();
  if (normalized === "submitted" || normalized === "presubmitted" || normalized === "working" || normalized === "accepted") {
    return "working";
  }
  if (normalized === "filled") {
    return "filled";
  }
  if (normalized === "canceled" || normalized === "cancelled") {
    return "canceled";
  }
  if (normalized === "rejected") {
    return "rejected";
  }
  if (normalized === "partial" || normalized === "partially_filled" || normalized === "partfilled") {
    return "partial";
  }
  if (normalized === "cancel_pending" || normalized === "cancelpending" || normalized === "pending_cancel") {
    return "cancel_pending";
  }
  if (normalized === "blocked" || normalized === "stale") {
    return normalized;
  }
  return "unknown";
}

export function orderTypeLabel(value: unknown): AccountOrderRow["order_type"] {
  const normalized = asText(value).toUpperCase();
  if (normalized === "LMT" || normalized === "LIMIT") {
    return "LIMIT";
  }
  if (normalized === "MKT" || normalized === "MARKET") {
    return "MARKET";
  }
  return "UNKNOWN";
}

export function reportStatusLabel(value: unknown): string {
  const label = asText(value);
  const normalized = label.toLowerCase();
  if (
    [
      "accepted",
      "submitted",
      "working",
      "partial",
      "filled",
      "alltraded",
      "cancelled",
      "canceled",
      "rejected"
    ].includes(normalized)
  ) {
    return label.toUpperCase();
  }
  return label;
}

export function accountKindFromDomain(domain: string): AccountKind {
  if (domain === "live") {
    return "live_broker";
  }
  if (domain === "backtest") {
    return "backtest_replay";
  }
  if (domain === "paper") {
    return "broker_paper_probe";
  }
  return "sandbox_paper";
}

export function mirrorExecutionReportRows(readback: MirrorWorkbenchReadback): AccountExecutionReportRow[] {
  const storeReload = readback.selected.route_context?.store_reload as Record<string, unknown> | undefined;
  const reloadCheckpointId = storeReload
    ? asText(storeReload.reload_checkpoint_id, "unknown")
    : null;
  const orderReports = readback.selected.orders.map((order) => ({
    account_id: readback.selected.account_id,
    report_id: asText(order.report_id, asText(order.client_order_id)),
    report_type: "OrderStatusReport" as const,
    client_order_id: asText(order.client_order_id),
    venue_order_id: asText(order.venue_order_id, asText(order.lifecycle_ref, "missing")),
    instrument: asText(order.instrument_id, asText(order.instrument)),
    side: sideLabel(order.side),
    status_or_trade: reportStatusLabel(order.order_status),
    quantity: asNumber(order.quantity),
    filled_quantity: asNumber(order.filled_qty),
    remaining_quantity: asNumber(order.leaves_qty),
    limit_or_last_price: asNumber(order.price),
    sequence: asNumber(order.seq),
    source_ref: asText(order.source_ref ?? order.report_provenance_ref, readback.selected.source_ref),
    checksum: asText(order.source_checksum ?? order.checksum, readback.selected.source_checksum),
    reload_checkpoint_id: reloadCheckpointId
  }));
  const fillReports = readback.selected.fills.map((fill) => ({
    account_id: readback.selected.account_id,
    report_id: asText(fill.report_id, asText(fill.trade_id)),
    report_type: "FillReport" as const,
    client_order_id: asText(fill.client_order_id),
    venue_order_id: asText(fill.venue_order_id, "missing"),
    instrument: asText(fill.instrument_id, asText(fill.instrument)),
    side: sideLabel(fill.side),
    status_or_trade: asText(fill.trade_id, asText(fill.order_status, "unknown")),
    quantity: asNumber(fill.quantity),
    filled_quantity: asNumber(fill.last_qty),
    remaining_quantity: asNumber(fill.leaves_qty),
    limit_or_last_price: asNumber(fill.last_px),
    sequence: asNumber(fill.seq),
    source_ref: asText(fill.source_ref, readback.selected.source_ref),
    checksum: asText(fill.source_checksum ?? fill.checksum, readback.selected.source_checksum),
    reload_checkpoint_id: reloadCheckpointId
  }));
  return [...orderReports, ...fillReports];
}

export function isP024PaperArmed(readback: MirrorWorkbenchReadback | null): boolean {
  if (!readback) {
    return false;
  }
  return (
    readback.selected.account_id === "acct.ctp.paper.19053" &&
    readback.selected.account_domain === "paper" &&
    readback.selected.capabilities.command.enabled === true &&
    readback.selected.capabilities.command.mode === "paper_armed"
  );
}

export function defaultSubmitIntent(readback: MirrorWorkbenchReadback): OrderIntentRequest {
  const preflightRef = asText(readback.selected.source_ref);
  const keySeed = readback.selected.projection_checkpoint_id.replaceAll(":", "-").replaceAll("/", "-");
  return {
    schema_version: "account_command.order_intent.v1",
    intent_id: `intent.p024.ui.submit.${keySeed.slice(0, 32).toLowerCase()}` as OrderIntentRequest["intent_id"],
    account_id: readback.selected.account_id as "acct.ctp.paper.19053",
    mode: "paper_armed",
    action: "submit",
    instrument: "au2508",
    exchange: "SHFE",
    side: "BUY",
    quantity: 2,
    order_type: "LIMIT",
    limit_price: 532.4,
    time_in_force: "GFD",
    offset: "OPEN",
    idempotency_key: `p024-ui-submit-${keySeed}`.slice(0, 80),
    operator_ref: "operator://account-console-web-ui/p024",
    preflight_ref: preflightRef,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false
  };
}

export function cancelIntentForOrder(readback: MirrorWorkbenchReadback, order: AccountOrderRow): CancelIntentRequest {
  const stableOrderId = order.client_order_id || order.lifecycle_ref || order.source_ref;
  const sourceOrder =
    readback.selected.orders.find(
      (item) =>
        asText(item.client_order_id) === order.client_order_id ||
        asText(item.venue_order_id) === order.lifecycle_ref
    ) ?? {};
  const keySeed = `${readback.selected.projection_checkpoint_id}-${stableOrderId}`
    .replaceAll(":", "-")
    .replaceAll("/", "-");
  return {
    schema_version: "account_command.cancel_intent.v1",
    intent_id: `intent.p024.ui.cancel.${keySeed.slice(0, 32).toLowerCase()}`,
    account_id: readback.selected.account_id as "acct.ctp.paper.19053",
    mode: "paper_armed",
    action: "cancel",
    instrument: order.instrument,
    exchange: order.destination && order.destination !== "missing" ? order.destination : asText(sourceOrder.exchange, "SHFE"),
    client_order_id: asText(sourceOrder.client_order_id, order.client_order_id || stableOrderId),
    venue_order_id: asText(sourceOrder.venue_order_id, order.lifecycle_ref ?? stableOrderId),
    order_ref: asText(sourceOrder.order_ref, order.lifecycle_ref ?? stableOrderId),
    front_id: asNumber(sourceOrder.front_id) ?? 0,
    session_id: asNumber(sourceOrder.session_id) ?? 0,
    idempotency_key: `p024-ui-cancel-${keySeed}`.slice(0, 80),
    operator_ref: "operator://account-console-web-ui/p024",
    readback_ref: order.source_ref,
    raw_secret_values_recorded: false,
    raw_broker_endpoint_recorded: false
  };
}
