import {
  AlertTriangle,
  Clipboard,
  Database,
  FileSearch,
  Gauge,
  Landmark,
  Layers,
  ListFilter,
  Radio,
  ShieldAlert,
  Waypoints
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import adr0044Fixture from "../../contracts/ui/fixtures/daily_closeout/account_health_adr0044_foundation_closeout.json";
import blockedFixture from "../../contracts/ui/fixtures/daily_closeout/account_health_blocked_settlement.json";
import emptyFixture from "../../contracts/ui/fixtures/daily_closeout/account_health_empty.json";
import happyFixture from "../../contracts/ui/fixtures/daily_closeout/account_health_happy_path.json";
import partialFixture from "../../contracts/ui/fixtures/daily_closeout/account_health_partial_evidence.json";
import staleFixture from "../../contracts/ui/fixtures/daily_closeout/account_health_stale_stream.json";
import accountSummaryBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_blocked.json";
import accountSummaryEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_empty.json";
import accountSummaryHappyFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_happy_path.json";
import accountSummaryPartialFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_partial_evidence.json";
import accountSummaryR1CtaCoreFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_r1_cta_core_001.json";
import accountSummaryStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_summary_stale_stream.json";
import accountOrderDetailBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_order_detail_blocked_missing_events.json";
import accountOrderDetailFilledFixture from "../../contracts/ui/fixtures/account_workbench/account_order_detail_e100_filled_lifecycle.json";
import accountOrdersBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_orders_blocked_missing_lifecycle.json";
import accountOrdersCurrentFixture from "../../contracts/ui/fixtures/account_workbench/account_orders_current_e100.json";
import accountOrdersEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_orders_empty.json";
import accountOrdersStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_orders_stale_stream.json";
import accountPositionsBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_blocked_missing_carryover.json";
import accountPositionsCurrentFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_current_e100.json";
import accountPositionsEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_empty.json";
import accountPositionsPartialFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_partial_missing_settlement.json";
import accountPositionsR1CtaCoreFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_r1_cta_core_001.json";
import accountPositionsStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_positions_stale_stream.json";
import accountSettlementBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_settlement_blocked_missing_current.json";
import accountSettlementCurrentFixture from "../../contracts/ui/fixtures/account_workbench/account_settlement_current.json";
import accountSettlementEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_settlement_empty.json";
import accountSettlementPartialFixture from "../../contracts/ui/fixtures/account_workbench/account_settlement_partial_missing_carryover.json";
import accountSettlementStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_settlement_stale_stream.json";
import accountEquityBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_equity_blocked_missing_ledger.json";
import accountEquityCurrentFixture from "../../contracts/ui/fixtures/account_workbench/account_equity_current.json";
import accountEquityEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_equity_empty.json";
import accountEquityPartialFixture from "../../contracts/ui/fixtures/account_workbench/account_equity_partial_missing_curve.json";
import accountEquityStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_equity_stale_stream.json";
import accountIncidentsActiveFixture from "../../contracts/ui/fixtures/account_workbench/account_incidents_active.json";
import accountIncidentsBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_incidents_blocked_source.json";
import accountIncidentsEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_incidents_empty.json";
import accountIncidentsPartialFixture from "../../contracts/ui/fixtures/account_workbench/account_incidents_partial_missing_repair.json";
import accountIncidentsStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_incidents_stale_stream.json";
import accountEvidenceBlockedFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_blocked_missing_schema.json";
import accountEvidenceCurrentFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_current.json";
import accountEvidenceEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_empty.json";
import accountEvidencePartialFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_partial_missing_raw_payload.json";
import accountEvidenceR1CtaCoreFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_r1_cta_core_001.json";
import accountEvidenceStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_stale_stream.json";
import accountReconcileEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_empty.json";
import accountReconcileMatchedFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_matched.json";
import accountReconcileMismatchFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_mismatch.json";
import accountReconcilePartialFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_partial_missing_tolerance.json";
import accountReconcileR1CtaCoreFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_r1_cta_core_001.json";
import accountReconcileStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_stale_stream.json";
import intradayMonitorBlockedFixture from "../../contracts/ui/fixtures/intraday_monitor/intraday_monitor_blocked.json";
import intradayMonitorCurrentFixture from "../../contracts/ui/fixtures/intraday_monitor/intraday_monitor_current.json";
import intradayMonitorEmptyFixture from "../../contracts/ui/fixtures/intraday_monitor/intraday_monitor_empty.json";
import intradayMonitorPartialFixture from "../../contracts/ui/fixtures/intraday_monitor/intraday_monitor_partial.json";
import intradayMonitorStaleFixture from "../../contracts/ui/fixtures/intraday_monitor/intraday_monitor_stale.json";
import type {
  AccountEquityFixtureState,
  AccountEquityPanelReadModel,
  AccountEquityPoint,
  AccountEvidenceFixtureState,
  AccountEvidencePackage,
  AccountEvidencePanelReadModel,
  AccountHealthCloseoutState,
  AccountHealthPanelFixtureState,
  AccountHealthPanelReadModel,
  AccountHealthRow,
  AccountHealthSettlementState,
  AccountIncidentRow,
  AccountIncidentsFixtureState,
  AccountIncidentsPanelReadModel,
  AccountKind,
  AccountOrderDetailFixtureState,
  AccountOrderDetailPanelReadModel,
  AccountExecutionReportRow,
  AccountOrdersFixtureState,
  AccountOrdersPanelReadModel,
  AccountOrderRow,
  AccountPositionRow,
  AccountPositionsFixtureState,
  AccountPositionsPanelReadModel,
  AccountSummaryBlocker,
  AccountReconcileFixtureState,
  AccountReconcileItem,
  AccountReconcilePanelReadModel,
  AccountSettlementFixtureState,
  AccountSettlementPanelReadModel,
  AccountSummaryFixtureState,
  AccountSummaryPanelReadModel,
  IntradayMonitorExceptionRow,
  IntradayMonitorFixtureState,
  IntradayMonitorIncidentRow,
  IntradayMonitorPanelReadModel,
  IntradayMonitorStreamStateRow,
  MirrorAccountProjection,
  MirrorAccountSummary,
  MirrorEvidenceResponse,
  MirrorSourceHealthResponse
} from "./types";
import {
  fetchMirrorAccount,
  fetchMirrorAccounts,
  fetchMirrorEvidence,
  fetchMirrorSourceHealth
} from "./api";

type AccountHealthFixtureId = AccountHealthPanelFixtureState | "adr0044_foundation";

interface MirrorWorkbenchReadback {
  accounts: MirrorAccountSummary[];
  selected: MirrorAccountProjection;
  sourceHealth: MirrorSourceHealthResponse | null;
  evidence: MirrorEvidenceResponse | null;
}

const mirrorRouteAliases: Record<string, string> = {
  "acct.demo-19053": "simulated-001"
};

function resolveMirrorRouteAccountId(routeAccountId: string, accounts: MirrorAccountSummary[]) {
  const canonicalRouteAccountId = mirrorRouteAliases[routeAccountId] ?? routeAccountId;
  if (accounts.some((account) => account.account_id === canonicalRouteAccountId)) {
    return canonicalRouteAccountId;
  }
  return accounts[0]?.account_id;
}

const fixtureMap: Record<AccountHealthFixtureId, AccountHealthPanelReadModel> = {
  happy_path: happyFixture as AccountHealthPanelReadModel,
  adr0044_foundation: adr0044Fixture as AccountHealthPanelReadModel,
  empty: emptyFixture as AccountHealthPanelReadModel,
  blocked: blockedFixture as AccountHealthPanelReadModel,
  stale: staleFixture as AccountHealthPanelReadModel,
  partial: partialFixture as AccountHealthPanelReadModel
};

const fixtureLabels: Record<AccountHealthFixtureId, string> = {
  happy_path: "happy path",
  adr0044_foundation: "ADR-0044 source-backed",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
};

const accountSummaryFixtureMap: Record<AccountSummaryFixtureState, AccountSummaryPanelReadModel> = {
  happy_path: accountSummaryHappyFixture as AccountSummaryPanelReadModel,
  empty: accountSummaryEmptyFixture as AccountSummaryPanelReadModel,
  blocked: accountSummaryBlockedFixture as AccountSummaryPanelReadModel,
  stale: accountSummaryStaleFixture as AccountSummaryPanelReadModel,
  partial: accountSummaryPartialFixture as AccountSummaryPanelReadModel,
  r1_cta_core_001: accountSummaryR1CtaCoreFixture as AccountSummaryPanelReadModel
};

const accountSummaryFixtureLabels: Record<AccountSummaryFixtureState, string> = {
  happy_path: "happy path",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001"
};

const accountOrdersFixtureMap: Record<AccountOrdersFixtureState, AccountOrdersPanelReadModel> = {
  current_orders: accountOrdersCurrentFixture as AccountOrdersPanelReadModel,
  empty: accountOrdersEmptyFixture as AccountOrdersPanelReadModel,
  blocked: accountOrdersBlockedFixture as AccountOrdersPanelReadModel,
  stale: accountOrdersStaleFixture as AccountOrdersPanelReadModel
};

const accountOrdersFixtureLabels: Record<AccountOrdersFixtureState, string> = {
  current_orders: "current orders",
  empty: "empty",
  blocked: "blocked",
  stale: "stale"
};

const accountOrderDetailFixtureMap: Record<AccountOrderDetailFixtureState, AccountOrderDetailPanelReadModel> = {
  filled_lifecycle: accountOrderDetailFilledFixture as AccountOrderDetailPanelReadModel,
  blocked: accountOrderDetailBlockedFixture as AccountOrderDetailPanelReadModel,
  stale: accountOrderDetailBlockedFixture as AccountOrderDetailPanelReadModel
};

const accountOrderDetailFixtureLabels: Record<AccountOrderDetailFixtureState, string> = {
  filled_lifecycle: "filled lifecycle",
  blocked: "blocked",
  stale: "stale"
};

const accountPositionsFixtureMap: Record<AccountPositionsFixtureState, AccountPositionsPanelReadModel> = {
  current_positions: accountPositionsCurrentFixture as AccountPositionsPanelReadModel,
  empty: accountPositionsEmptyFixture as AccountPositionsPanelReadModel,
  blocked: accountPositionsBlockedFixture as AccountPositionsPanelReadModel,
  stale: accountPositionsStaleFixture as AccountPositionsPanelReadModel,
  partial: accountPositionsPartialFixture as AccountPositionsPanelReadModel,
  r1_cta_core_001: accountPositionsR1CtaCoreFixture as AccountPositionsPanelReadModel
};

const accountPositionsFixtureLabels: Record<AccountPositionsFixtureState, string> = {
  current_positions: "current positions",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001"
};

const accountSettlementFixtureMap: Record<AccountSettlementFixtureState, AccountSettlementPanelReadModel> = {
  current_settlement: accountSettlementCurrentFixture as AccountSettlementPanelReadModel,
  empty: accountSettlementEmptyFixture as AccountSettlementPanelReadModel,
  blocked: accountSettlementBlockedFixture as AccountSettlementPanelReadModel,
  stale: accountSettlementStaleFixture as AccountSettlementPanelReadModel,
  partial: accountSettlementPartialFixture as AccountSettlementPanelReadModel
};

const accountSettlementFixtureLabels: Record<AccountSettlementFixtureState, string> = {
  current_settlement: "current settlement",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
};

const accountEquityFixtureMap: Record<AccountEquityFixtureState, AccountEquityPanelReadModel> = {
  current_equity: accountEquityCurrentFixture as AccountEquityPanelReadModel,
  empty: accountEquityEmptyFixture as AccountEquityPanelReadModel,
  blocked: accountEquityBlockedFixture as AccountEquityPanelReadModel,
  stale: accountEquityStaleFixture as AccountEquityPanelReadModel,
  partial: accountEquityPartialFixture as AccountEquityPanelReadModel
};

const accountEquityFixtureLabels: Record<AccountEquityFixtureState, string> = {
  current_equity: "current equity",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
};

const accountReconcileFixtureMap: Record<AccountReconcileFixtureState, AccountReconcilePanelReadModel> = {
  matched: accountReconcileMatchedFixture as AccountReconcilePanelReadModel,
  empty: accountReconcileEmptyFixture as AccountReconcilePanelReadModel,
  mismatch: accountReconcileMismatchFixture as AccountReconcilePanelReadModel,
  stale: accountReconcileStaleFixture as AccountReconcilePanelReadModel,
  partial: accountReconcilePartialFixture as AccountReconcilePanelReadModel,
  r1_cta_core_001: accountReconcileR1CtaCoreFixture as AccountReconcilePanelReadModel
};

const accountReconcileFixtureLabels: Record<AccountReconcileFixtureState, string> = {
  matched: "matched",
  empty: "empty",
  mismatch: "mismatch",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001"
};

const accountIncidentsFixtureMap: Record<AccountIncidentsFixtureState, AccountIncidentsPanelReadModel> = {
  active_incidents: accountIncidentsActiveFixture as AccountIncidentsPanelReadModel,
  empty: accountIncidentsEmptyFixture as AccountIncidentsPanelReadModel,
  blocked: accountIncidentsBlockedFixture as AccountIncidentsPanelReadModel,
  stale: accountIncidentsStaleFixture as AccountIncidentsPanelReadModel,
  partial: accountIncidentsPartialFixture as AccountIncidentsPanelReadModel
};

const accountIncidentsFixtureLabels: Record<AccountIncidentsFixtureState, string> = {
  active_incidents: "active incidents",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
};

const accountEvidenceFixtureMap: Record<AccountEvidenceFixtureState, AccountEvidencePanelReadModel> = {
  current_evidence: accountEvidenceCurrentFixture as AccountEvidencePanelReadModel,
  empty: accountEvidenceEmptyFixture as AccountEvidencePanelReadModel,
  blocked: accountEvidenceBlockedFixture as AccountEvidencePanelReadModel,
  stale: accountEvidenceStaleFixture as AccountEvidencePanelReadModel,
  partial: accountEvidencePartialFixture as AccountEvidencePanelReadModel,
  r1_cta_core_001: accountEvidenceR1CtaCoreFixture as AccountEvidencePanelReadModel
};

const accountEvidenceFixtureLabels: Record<AccountEvidenceFixtureState, string> = {
  current_evidence: "current evidence",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001"
};

const intradayMonitorFixtureMap: Record<IntradayMonitorFixtureState, IntradayMonitorPanelReadModel> = {
  current: intradayMonitorCurrentFixture as IntradayMonitorPanelReadModel,
  empty: intradayMonitorEmptyFixture as IntradayMonitorPanelReadModel,
  blocked: intradayMonitorBlockedFixture as IntradayMonitorPanelReadModel,
  stale: intradayMonitorStaleFixture as IntradayMonitorPanelReadModel,
  partial: intradayMonitorPartialFixture as IntradayMonitorPanelReadModel
};

const intradayMonitorFixtureLabels: Record<IntradayMonitorFixtureState, string> = {
  current: "current",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
};

const portfolioOwnerConsoleUrl =
  "http://127.0.0.1:4185/console/portfolios/CTA-CORE-001?view=portfolio-owner&origin=account-console&portfolio_uid=CTA-CORE-001";

const workbenches = [
  { label: "Daily Closeout", path: "/closeout", icon: Gauge },
  { label: "Intraday Monitor", path: "/monitor", icon: Radio },
  { label: "Account Workbench", path: "/accounts/acct.demo-19053", icon: Database },
  { label: "Allocation Admin", path: "/management/accounts", icon: Layers },
  { label: "Risk And Reconcile", path: "/risk-reconcile", icon: ShieldAlert },
  { label: "Evidence Explorer", path: "/evidence", icon: FileSearch },
  { label: "Stream Ops", path: "/ops/stream", icon: Waypoints }
];

function formatLabel(value: string): string {
  return value.replaceAll("_", " ");
}

function stateTone(value: string): string {
  if (value === "blocked" || value === "gap" || value === "missing") {
    return "blocked";
  }
  if (value === "stale") {
    return "stale";
  }
  if (value === "partial" || value === "warning") {
    return "partial";
  }
  if (value === "empty") {
    return "empty";
  }
  return "healthy";
}

function asNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function asText(value: unknown, fallback = "unknown"): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

function directionLabel(value: unknown): AccountPositionRow["direction"] {
  const normalized = asText(value).toUpperCase();
  if (normalized === "LONG" || normalized === "SHORT" || normalized === "NET") {
    return normalized;
  }
  return "UNKNOWN";
}

function sideLabel(value: unknown): AccountOrderRow["side"] {
  return asText(value).toUpperCase() === "SELL" ? "SELL" : "BUY";
}

function orderStatusLabel(value: unknown): AccountOrderRow["status"] {
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

function orderTypeLabel(value: unknown): AccountOrderRow["order_type"] {
  const normalized = asText(value).toUpperCase();
  if (normalized === "LMT" || normalized === "LIMIT") {
    return "LIMIT";
  }
  if (normalized === "MKT" || normalized === "MARKET") {
    return "MARKET";
  }
  return "UNKNOWN";
}

function reportStatusLabel(value: unknown): string {
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

function accountKindFromDomain(domain: string): AccountKind {
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

function blockerSeverity(type: string): AccountHealthRow["blockers"][number]["severity"] {
  if (type.includes("missing") || type.includes("unavailable")) {
    return "high";
  }
  if (type.includes("stale")) {
    return "warning";
  }
  return "info";
}

function mirrorBlockers(blockers: Record<string, unknown>[]): AccountSummaryBlocker[] {
  const seen = new Set<string>();
  return blockers.flatMap((blocker, index) => {
    const kind = asText(blocker.type, "source_blocker");
    const blockerId = asText(blocker.blocker_id, `mirror-blocker-${index}`);
    const checksum = asText(blocker.checksum, "sha256:0000000000000000000000000000000000000000000000000000000000000000");
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
      next_action: asText(blocker.next_action, "Resolve source evidence before accepting account consistency."),
      source_ref: asText(blocker.source_ref, "missing_source_ref"),
      checksum
    }];
  });
}

function mirrorEvidenceRefs(readback: MirrorWorkbenchReadback) {
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

function mirrorContext(readback: MirrorWorkbenchReadback) {
  const health = readback.sourceHealth;
  return {
    trading_day: "2026-06-15",
    session_id: `${readback.selected.source_kind}.${readback.selected.display_alias}`,
    run_id: readback.selected.source_ref,
    reducer_checkpoint_id: readback.selected.projection_checkpoint_id,
    reducer_checkpoint_ts: health?.observed_at ?? asText(readback.selected.source_health.observed_at, "unknown"),
    stream_state: stateTone(readback.selected.capabilities.observation.mirror_state ?? "blocked") as AccountHealthPanelReadModel["context"]["stream_state"],
    projection_owner: "account-console-contracts" as const,
    source_authority: readback.selected.blockers.length > 0 ? "typed_blocker" as const : "normalized_read_model" as const
  };
}

function mirrorBoundaries(readback: MirrorWorkbenchReadback) {
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

function mirrorSummaryReadModel(readback: MirrorWorkbenchReadback): AccountSummaryPanelReadModel {
  const selected = readback.selected;
  const balance = selected.balances.find((row) => row.currency === "USD") ?? selected.balances[0] ?? {};
  const blockers = mirrorBlockers([...(selected.blockers ?? []), ...(readback.sourceHealth?.blockers ?? [])]);
  const currencyBalances = selected.balances.filter((row) => row.currency !== "BASE").map((row) => ({
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
      display_state: stateTone(selected.capabilities.observation.mirror_state ?? "blocked") as AccountHealthPanelReadModel["context"]["stream_state"],
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

function mirrorPositionsReadModel(readback: MirrorWorkbenchReadback): AccountPositionsPanelReadModel {
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

function mirrorOrdersReadModel(readback: MirrorWorkbenchReadback): AccountOrdersPanelReadModel {
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

function mirrorExecutionReportRows(readback: MirrorWorkbenchReadback): AccountExecutionReportRow[] {
  const storeReload = readback.selected.source_health.store_reload as Record<string, unknown> | undefined;
  const reloadCheckpointId = storeReload
    ? asText(storeReload.reload_checkpoint_id, "unknown")
    : null;
  const orderRows = readback.selected.orders.map((order) => ({
    account_id: readback.selected.account_id,
    report_id: asText(order.report_id, asText(order.client_order_id)),
    report_type: "OrderStatusReport" as const,
    client_order_id: asText(order.client_order_id),
    venue_order_id: asText(order.venue_order_id, asText(order.lifecycle_ref, "missing")),
    instrument: asText(order.instrument_id, asText(order.instrument)),
    side: sideLabel(order.side),
    status_or_trade: reportStatusLabel(order.order_status ?? order.status),
    quantity: asNumber(order.quantity),
    filled_quantity: asNumber(order.filled_quantity),
    remaining_quantity: asNumber(order.remaining_quantity),
    limit_or_last_price: asNumber(order.price ?? order.limit_price),
    sequence: asNumber(order.sequence),
    source_ref: asText(order.source_ref ?? order.report_provenance_ref, readback.selected.source_ref),
    checksum: asText(order.source_checksum ?? order.checksum, readback.selected.source_checksum),
    reload_checkpoint_id: reloadCheckpointId
  }));
  const fillRows = readback.selected.fills.map((fill) => ({
    account_id: readback.selected.account_id,
    report_id: asText(fill.report_id, asText(fill.trade_id)),
    report_type: "FillReport" as const,
    client_order_id: asText(fill.client_order_id),
    venue_order_id: asText(fill.venue_order_id, "missing"),
    instrument: asText(fill.instrument_id, asText(fill.instrument)),
    side: sideLabel(fill.side),
    status_or_trade: asText(fill.trade_id, asText(fill.order_status, "unknown")),
    quantity: asNumber(fill.quantity),
    filled_quantity: asNumber(fill.filled_quantity),
    remaining_quantity: asNumber(fill.remaining_quantity),
    limit_or_last_price: asNumber(fill.last_px ?? fill.price),
    sequence: asNumber(fill.sequence),
    source_ref: asText(fill.source_ref, readback.selected.source_ref),
    checksum: asText(fill.source_checksum ?? fill.checksum, readback.selected.source_checksum),
    reload_checkpoint_id: reloadCheckpointId
  }));
  return [...orderRows, ...fillRows].sort((left, right) => {
    const leftSeq = left.sequence ?? Number.MAX_SAFE_INTEGER;
    const rightSeq = right.sequence ?? Number.MAX_SAFE_INTEGER;
    if (leftSeq !== rightSeq) {
      return leftSeq - rightSeq;
    }
    return left.report_id.localeCompare(right.report_id);
  });
}

function commandStatusRefs(value: unknown): string[] {
  return Array.isArray(value) ? value.map((item) => asText(item)).filter((item) => item !== "unknown") : [];
}

function commandStatusBlockerText(blocker: Record<string, unknown>) {
  return [
    asText(blocker.stage, "command_status"),
    asText(blocker.reason, asText(blocker.kind, "missing evidence")),
    asText(blocker.source_ref, "missing source ref")
  ].join(" | ");
}

export function App() {
  const currentPath = window.location.pathname;
  const isIntradayMonitorRoute = currentPath === "/monitor";
  const isAccountWorkbenchRoute = currentPath.startsWith("/accounts/");
  const isAccountOrderDetailRoute = /^\/accounts\/[^/]+\/orders\/[^/]+/.test(currentPath);
  const isAccountOrdersRoute = /^\/accounts\/[^/]+\/orders\/?$/.test(currentPath);
  const isAccountPositionsRoute = /^\/accounts\/[^/]+\/positions\/?$/.test(currentPath);
  const isAccountSettlementRoute = /^\/accounts\/[^/]+\/settlement\/?$/.test(currentPath);
  const isAccountEquityRoute = /^\/accounts\/[^/]+\/equity\/?$/.test(currentPath);
  const isAccountReconcileRoute = /^\/accounts\/[^/]+\/reconcile\/?$/.test(currentPath);
  const isAccountIncidentsRoute = /^\/accounts\/[^/]+\/incidents\/?$/.test(currentPath);
  const isAccountEvidenceRoute = /^\/accounts\/[^/]+\/evidence\/?$/.test(currentPath);
  const [fixtureState, setFixtureState] = useState<AccountHealthFixtureId>("happy_path");
  const [accountSummaryFixtureState, setAccountSummaryFixtureState] =
    useState<AccountSummaryFixtureState>("happy_path");
  const [accountOrdersFixtureState, setAccountOrdersFixtureState] =
    useState<AccountOrdersFixtureState>("current_orders");
  const [accountOrderDetailFixtureState, setAccountOrderDetailFixtureState] =
    useState<AccountOrderDetailFixtureState>("filled_lifecycle");
  const [accountPositionsFixtureState, setAccountPositionsFixtureState] =
    useState<AccountPositionsFixtureState>("current_positions");
  const [accountSettlementFixtureState, setAccountSettlementFixtureState] =
    useState<AccountSettlementFixtureState>("current_settlement");
  const [accountEquityFixtureState, setAccountEquityFixtureState] =
    useState<AccountEquityFixtureState>("current_equity");
  const [accountReconcileFixtureState, setAccountReconcileFixtureState] =
    useState<AccountReconcileFixtureState>("mismatch");
  const [accountIncidentsFixtureState, setAccountIncidentsFixtureState] =
    useState<AccountIncidentsFixtureState>("active_incidents");
  const [accountEvidenceFixtureState, setAccountEvidenceFixtureState] =
    useState<AccountEvidenceFixtureState>("current_evidence");
  const [intradayMonitorFixtureState, setIntradayMonitorFixtureState] =
    useState<IntradayMonitorFixtureState>("current");
  const [accountTypeFilter, setAccountTypeFilter] = useState<AccountKind | "all">("all");
  const [closeoutFilter, setCloseoutFilter] = useState<AccountHealthCloseoutState | "all">("all");
  const [settlementFilter, setSettlementFilter] = useState<AccountHealthSettlementState | "all">("all");
  const fixture = fixtureMap[fixtureState];
  const accountSummaryFixture = accountSummaryFixtureMap[accountSummaryFixtureState];
  const accountOrdersFixture = accountOrdersFixtureMap[accountOrdersFixtureState];
  const accountOrderDetailFixture = accountOrderDetailFixtureMap[accountOrderDetailFixtureState];
  const accountPositionsFixture = accountPositionsFixtureMap[accountPositionsFixtureState];
  const accountSettlementFixture = accountSettlementFixtureMap[accountSettlementFixtureState];
  const accountEquityFixture = accountEquityFixtureMap[accountEquityFixtureState];
  const accountReconcileFixture = accountReconcileFixtureMap[accountReconcileFixtureState];
  const accountIncidentsFixture = accountIncidentsFixtureMap[accountIncidentsFixtureState];
  const accountEvidenceFixture = accountEvidenceFixtureMap[accountEvidenceFixtureState];
  const intradayMonitorFixture = intradayMonitorFixtureMap[intradayMonitorFixtureState];
  const routeAccountId = decodeURIComponent(currentPath.split("/")[2] ?? "");
  const [mirrorReadback, setMirrorReadback] = useState<MirrorWorkbenchReadback | null>(null);
  const [mirrorReadbackError, setMirrorReadbackError] = useState<string | null>(null);
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(
    fixture.accounts[0]?.account_id ?? null
  );

  const visibleRows = useMemo(
    () =>
      fixture.accounts.filter((account) => {
        if (accountTypeFilter !== "all" && account.account_type !== accountTypeFilter) {
          return false;
        }
        if (closeoutFilter !== "all" && account.closeout_state !== closeoutFilter) {
          return false;
        }
        if (settlementFilter !== "all" && account.settlement_state !== settlementFilter) {
          return false;
        }
        return true;
      }),
    [accountTypeFilter, closeoutFilter, fixture.accounts, settlementFilter]
  );

  useEffect(() => {
    setSelectedAccountId((current) => {
      if (visibleRows.some((account) => account.account_id === current)) {
        return current;
      }
      return visibleRows[0]?.account_id ?? null;
    });
  }, [visibleRows]);

  const selectedAccount =
    visibleRows.find((account) => account.account_id === selectedAccountId) ?? visibleRows[0] ?? null;
  const terminalSummary = mirrorReadback ? mirrorSummaryReadModel(mirrorReadback) : accountSummaryFixture;
  const terminalPositions = mirrorReadback ? mirrorPositionsReadModel(mirrorReadback) : accountPositionsFixture;
  const terminalOrders = mirrorReadback ? mirrorOrdersReadModel(mirrorReadback) : accountOrdersFixture;

  useEffect(() => {
    if (
      !isAccountWorkbenchRoute ||
      isAccountOrderDetailRoute ||
      !(routeAccountId.startsWith("acct.") || routeAccountId === "simulated-001")
    ) {
      setMirrorReadback(null);
      setMirrorReadbackError(null);
      return;
    }

    let active = true;
    async function loadMirrorReadback() {
      try {
        const list = await fetchMirrorAccounts();
        const accountId = resolveMirrorRouteAccountId(routeAccountId, list.accounts);
        if (!accountId) {
          throw new Error("mirror account list is empty");
        }
        const [selected, sourceHealth, evidence] = await Promise.all([
          fetchMirrorAccount(accountId),
          fetchMirrorSourceHealth(accountId),
          fetchMirrorEvidence(accountId)
        ]);
        if (active) {
          setMirrorReadback({ accounts: list.accounts, selected, sourceHealth, evidence });
          setMirrorReadbackError(null);
        }
      } catch (error) {
        if (active) {
          setMirrorReadback(null);
          setMirrorReadbackError(error instanceof Error ? error.message : "mirror readback unavailable");
        }
      }
    }

    void loadMirrorReadback();
    return () => {
      active = false;
    };
  }, [isAccountOrderDetailRoute, isAccountWorkbenchRoute, routeAccountId]);

  return (
    <main className="shell" data-testid="account-console">
      <aside className="primary-nav" aria-label="Primary workbenches">
        <div className="brand-lockup">
          <strong>Nautilus</strong>
          <span>Account Console</span>
        </div>
        <nav>
          {workbenches.map((item) => {
            const Icon = item.icon;
            const active =
              (currentPath.startsWith("/accounts") && item.label === "Account Workbench") ||
              (!currentPath.startsWith("/accounts") &&
                (currentPath === item.path || (currentPath === "/" && item.path === "/closeout")));
            return (
              <a
                aria-current={active ? "page" : undefined}
                className={active ? "nav-item active" : "nav-item"}
                href={item.path}
                key={item.path}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>
        <div className="external-console-rail" aria-label="External console handoff">
          <span>外仓连接</span>
          <a
            className="nav-item external-console-link"
            data-testid="portfolio-owner-console-nav-link"
            href={portfolioOwnerConsoleUrl}
          >
            <Landmark size={16} />
            <span>Portfolio Owner Console</span>
          </a>
        </div>
      </aside>

      <section className="workspace">
        {isIntradayMonitorRoute ? (
          <>
            <header className="topbar">
              <div>
                <h1>Intraday Monitor</h1>
                <p>
                  {intradayMonitorFixture.context.trading_day} ·{" "}
                  {intradayMonitorFixture.context.session_id} ·{" "}
                  {intradayMonitorFixture.context.monitor_checkpoint_id}
                </p>
              </div>
              <div
                className={`stream-pill ${stateTone(intradayMonitorFixture.context.stream_state)}`}
                data-testid="intraday-monitor-stream-state"
              >
                <Radio size={16} />
                {intradayMonitorFixture.context.stream_state}
              </div>
            </header>

            <section className="checkpoint-strip" aria-label="Intraday monitor source checkpoint">
              <Ref label="Monitor checkpoint" value={intradayMonitorFixture.context.monitor_checkpoint_id} />
              <Ref label="Checkpoint time" value={intradayMonitorFixture.context.monitor_checkpoint_ts} />
              <Ref label="Projection" value={intradayMonitorFixture.context.projection_owner} />
              <Ref label="Authority" value={intradayMonitorFixture.context.source_authority} />
            </section>

            <IntradayMonitorPanel
              fixture={intradayMonitorFixture}
              fixtureState={intradayMonitorFixtureState}
              onFixtureState={setIntradayMonitorFixtureState}
            />
          </>
        ) : isAccountWorkbenchRoute ? (
          <>
            <header className="topbar">
              <div>
                <h1>Account Workbench</h1>
                <p>
                  {terminalSummary.context.trading_day} ·{" "}
                  {terminalSummary.account.account_id} · {terminalSummary.context.run_id}
                </p>
              </div>
              <div
                className={`stream-pill ${stateTone(terminalSummary.context.stream_state)}`}
                data-testid="account-workbench-stream-state"
              >
                <Landmark size={16} />
                {terminalSummary.context.stream_state}
              </div>
            </header>

            <section className="checkpoint-strip" aria-label="Account source checkpoint">
              <Ref label="Reducer checkpoint" value={terminalSummary.context.reducer_checkpoint_id} />
              <Ref label="Checkpoint time" value={terminalSummary.context.reducer_checkpoint_ts} />
              <Ref label="Projection" value={terminalSummary.context.projection_owner} />
              <Ref label="Authority" value={terminalSummary.context.source_authority} />
              <Ref
                label="Readback"
                value={mirrorReadback ? "mirror API" : mirrorReadbackError ? "fixture fallback" : "loading"}
              />
            </section>

            {isAccountOrderDetailRoute ? (
              <AccountOrderDetailPanel
                fixture={accountOrderDetailFixture}
                fixtureState={accountOrderDetailFixtureState}
                onFixtureState={setAccountOrderDetailFixtureState}
              />
            ) : isAccountOrdersRoute ? (
              <AccountOrdersPanel
                fixture={accountOrdersFixture}
                fixtureState={accountOrdersFixtureState}
                onFixtureState={setAccountOrdersFixtureState}
              />
            ) : isAccountPositionsRoute ? (
              <AccountPositionsPanel
                fixture={accountPositionsFixture}
                fixtureState={accountPositionsFixtureState}
                onFixtureState={setAccountPositionsFixtureState}
              />
            ) : isAccountSettlementRoute ? (
              <AccountSettlementPanel
                fixture={accountSettlementFixture}
                fixtureState={accountSettlementFixtureState}
                onFixtureState={setAccountSettlementFixtureState}
              />
            ) : isAccountEquityRoute ? (
              <AccountEquityPanel
                fixture={accountEquityFixture}
                fixtureState={accountEquityFixtureState}
                onFixtureState={setAccountEquityFixtureState}
              />
            ) : isAccountReconcileRoute ? (
              <AccountReconcilePanel
                fixture={accountReconcileFixture}
                fixtureState={accountReconcileFixtureState}
                onFixtureState={setAccountReconcileFixtureState}
              />
            ) : isAccountIncidentsRoute ? (
              <AccountIncidentsPanel
                fixture={accountIncidentsFixture}
                fixtureState={accountIncidentsFixtureState}
                onFixtureState={setAccountIncidentsFixtureState}
              />
            ) : isAccountEvidenceRoute ? (
              <AccountEvidencePanel
                fixture={accountEvidenceFixture}
                fixtureState={accountEvidenceFixtureState}
                onFixtureState={setAccountEvidenceFixtureState}
              />
            ) : (
              <AccountWorkbenchTerminalPanel
                mirrorAccounts={mirrorReadback?.accounts ?? null}
                mirrorReadback={mirrorReadback}
                mirrorReadbackError={mirrorReadbackError}
                sourceHealthDetails={mirrorReadback?.selected.source_health ?? null}
                summary={terminalSummary}
                positions={terminalPositions}
                orders={terminalOrders}
                fixtureState={accountSummaryFixtureState}
                onFixtureState={setAccountSummaryFixtureState}
              />
            )}
          </>
        ) : (
          <>
            <header className="topbar">
              <div>
                <h1>Daily Closeout</h1>
                <p>
                  {fixture.context.trading_day} · {fixture.context.session_id} · {fixture.context.closeout_run_id}
                </p>
              </div>
              <div
                className={`stream-pill ${stateTone(fixture.context.stream_state)}`}
                data-testid="event-stream-status"
              >
                <Radio size={16} />
                {fixture.context.stream_state}
              </div>
            </header>

            <section className="checkpoint-strip" aria-label="Source checkpoint">
              <Ref label="Reducer checkpoint" value={fixture.context.reducer_checkpoint_id} />
              <Ref label="Checkpoint time" value={fixture.context.reducer_checkpoint_ts} />
              <Ref label="Last cursor" value={String(fixture.context.last_cursor)} />
              <Ref label="Source ref" value={fixture.context.source_ref} />
            </section>

            <AccountHealthPanel
              accountTypeFilter={accountTypeFilter}
              closeoutFilter={closeoutFilter}
              fixture={fixture}
              fixtureState={fixtureState}
              onAccountTypeFilter={setAccountTypeFilter}
              onCloseoutFilter={setCloseoutFilter}
              onFixtureState={setFixtureState}
              onSelectAccount={setSelectedAccountId}
              onSettlementFilter={setSettlementFilter}
              selectedAccount={selectedAccount}
              selectedAccountId={selectedAccountId}
              settlementFilter={settlementFilter}
              visibleRows={visibleRows}
            />
          </>
        )}
      </section>
    </main>
  );
}

function formatMoney(value: number | null, currency = "CNY"): string {
  if (value === null) {
    return "missing";
  }
  return `${currency} ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

function formatLag(value: number | null): string {
  if (value === null) {
    return "missing";
  }
  if (value >= 1000) {
    return `${(value / 1000).toLocaleString(undefined, { maximumFractionDigits: 1 })}s`;
  }
  return `${value.toLocaleString()}ms`;
}

function IntradayMonitorPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: IntradayMonitorPanelReadModel;
  fixtureState: IntradayMonitorFixtureState;
  onFixtureState: (value: IntradayMonitorFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Stream authority");

  return (
    <section className="intraday-monitor-grid" data-testid="intraday-monitor-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="intraday-monitor-context-bar">
              {fixture.workbench} / {fixture.context.trading_day} / {fixture.context.session_id}
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as IntradayMonitorFixtureState)}
              value={fixtureState}
            >
              {Object.entries(intradayMonitorFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="intraday-monitor-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale monitor checkpoint {fixture.context.monitor_checkpoint_id} at{" "}
              {fixture.context.monitor_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="intraday-monitor-empty-state">
            No monitor exceptions are present in this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip intraday-monitor-lag-strip" data-testid="intraday-monitor-lag-strip">
          <Metric label="Max lag" value={formatLag(fixture.lag_summary.max_lag_ms)} />
          <Metric label="Stale streams" value={String(fixture.lag_summary.stale_stream_count)} />
          <Metric label="Open incidents" value={String(fixture.lag_summary.open_incident_count)} />
          <Metric label="Blocked sources" value={String(fixture.lag_summary.blocked_source_count)} />
          <Metric label="Exceptions" value={String(fixture.exceptions.length)} />
          <Metric label="Streams" value={String(fixture.streams.length)} />
        </div>

        <section className="summary-section" data-testid="intraday-monitor-exception-queue">
          <h3>Exception Queue</h3>
          {fixture.exceptions.length > 0 ? (
            <div className="order-list">
              {fixture.exceptions.map((exception) => (
                <IntradayExceptionCard exception={exception} key={exception.checksum} />
              ))}
            </div>
          ) : (
            <p className="muted">No exception rows in this read-only fixture projection.</p>
          )}
        </section>

        <section className="summary-section" data-testid="intraday-monitor-stream-state-list">
          <h3>Stream State</h3>
          {fixture.streams.length > 0 ? (
            <div className="monitor-stream-grid">
              {fixture.streams.map((stream) => (
                <IntradayStreamCard key={stream.checksum} stream={stream} />
              ))}
            </div>
          ) : (
            <p className="muted">No stream rows in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="intraday-monitor-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="intraday-monitor-detail-drawer">
        <div className="drawer-section">
          <h3>Incidents</h3>
          {fixture.incidents.length > 0 ? (
            <div className="order-list">
              {fixture.incidents.map((incident) => (
                <IntradayIncidentCard incident={incident} key={incident.checksum} />
              ))}
            </div>
          ) : (
            <p className="muted">No incident rows in this fixture projection.</p>
          )}
        </div>

        <BlockerList blockers={fixture.blockers} testId="intraday-monitor-blocker" />
        <SourceRefsList refs={fixture.source_refs} testId="intraday-monitor-source-ref" title="Source Refs" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="intraday-monitor-rejection-rule" />
      </aside>
    </section>
  );
}

function IntradayExceptionCard({ exception }: { exception: IntradayMonitorExceptionRow }) {
  return (
    <article className="order-card" data-testid="intraday-monitor-exception-row">
      <div className="order-card-head">
        <div>
          <strong>{exception.exception_id}</strong>
          <span>{formatLabel(exception.kind)}</span>
        </div>
        <StateBadge value={exception.severity} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Owner</dt>
          <dd>{exception.owner}</dd>
        </div>
        <div>
          <dt>Next action</dt>
          <dd>{exception.next_action}</dd>
        </div>
      </dl>
      <CopyableCode label="exception source ref" value={exception.source_ref} />
      <CopyableCode label="exception checksum" value={exception.checksum} />
    </article>
  );
}

function IntradayStreamCard({ stream }: { stream: IntradayMonitorStreamStateRow }) {
  return (
    <article className="order-card" data-testid="intraday-monitor-stream-state">
      <div className="order-card-head">
        <div>
          <strong>{stream.stream_id}</strong>
          <span>{stream.last_event_ts ?? "missing event time"}</span>
        </div>
        <StateBadge value={stream.state} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Lag</dt>
          <dd>{formatLag(stream.lag_ms)}</dd>
        </div>
        <div>
          <dt>Source</dt>
          <dd>
            <CopyableCode label="stream source ref" value={stream.source_ref} />
          </dd>
        </div>
      </dl>
    </article>
  );
}

function IntradayIncidentCard({ incident }: { incident: IntradayMonitorIncidentRow }) {
  return (
    <article className="order-card" data-testid="intraday-monitor-incident-row">
      <div className="order-card-head">
        <div>
          <strong>{incident.incident_id}</strong>
          <span>{formatLabel(incident.category)}</span>
        </div>
        <StateBadge value={incident.status} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Severity</dt>
          <dd>
            <StateBadge value={incident.severity} />
          </dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{incident.owner}</dd>
        </div>
        <div>
          <dt>Next action</dt>
          <dd>{incident.next_action}</dd>
        </div>
      </dl>
      <CopyableCode label="incident source ref" value={incident.source_ref} />
    </article>
  );
}

function numberTone(value: number | null): string {
  if (value === null || value === 0) {
    return "neutral";
  }
  return value > 0 ? "positive" : "negative";
}

function AccountWorkbenchTerminalPanel({
  mirrorAccounts,
  mirrorReadback,
  mirrorReadbackError,
  sourceHealthDetails,
  summary,
  positions,
  orders,
  fixtureState,
  onFixtureState
}: {
  mirrorAccounts: MirrorAccountSummary[] | null;
  mirrorReadback: MirrorWorkbenchReadback | null;
  mirrorReadbackError: string | null;
  sourceHealthDetails: Record<string, unknown> | null;
  summary: AccountSummaryPanelReadModel;
  positions: AccountPositionsPanelReadModel;
  orders: AccountOrdersPanelReadModel;
  fixtureState: AccountSummaryFixtureState;
  onFixtureState: (value: AccountSummaryFixtureState) => void;
}) {
  const baseCurrency = summary.account.base_currency;
  const accountRows = mirrorAccounts
    ? mirrorAccounts.map((account) => ({
        state: null,
        account: {
          account_id: account.account_id,
          account_alias: account.display_alias,
          account_kind: accountKindFromDomain(account.account_domain)
        },
        streamState: stateTone(account.mirror_state),
        href: `/accounts/${encodeURIComponent(account.account_id)}`
      }))
    : Object.entries(accountSummaryFixtureMap).map(([state, fixture]) => ({
        state: state as AccountSummaryFixtureState,
        account: fixture.account,
        streamState: fixture.context.stream_state,
        href: null
      }));
  const visiblePositions = positions.positions.filter(
    (position) => position.account_id === summary.account.account_id
  );
  const visibleOrders = orders.orders.filter((order) => order.account_id === summary.account.account_id);
  const executionReportRows = mirrorReadback
    ? mirrorExecutionReportRows(mirrorReadback).filter((report) => report.account_id === summary.account.account_id)
    : visibleOrders
        .filter((order) => order.report_provenance_ref)
        .map((order, index) => ({
          account_id: order.account_id,
          report_id: `${order.client_order_id}-${order.report_provenance_ref}`,
          report_type: "OrderStatusReport" as const,
          client_order_id: order.client_order_id,
          venue_order_id: order.lifecycle_ref,
          instrument: order.instrument,
          side: order.side,
          status_or_trade: order.status,
          quantity: order.quantity,
          filled_quantity: order.filled_quantity,
          remaining_quantity: order.remaining_quantity,
          limit_or_last_price: order.limit_price,
          sequence: index + 1,
          source_ref: order.report_provenance_ref ?? order.source_ref,
          checksum: order.checksum,
          reload_checkpoint_id: null
        }));
  const allBlockers: AccountSummaryBlocker[] = Array.from(
    new Map(
      [
        ...summary.blockers,
        ...(visiblePositions.length > 0 ? positions.blockers : []),
        ...(visibleOrders.length > 0 ? orders.blockers : [])
      ].map((blocker) => [`${blocker.blocker_id}-${blocker.checksum}`, blocker])
    ).values()
  );
  const allSourceRefs = [...summary.source_refs, ...positions.source_refs, ...orders.source_refs];
  const capabilityRows = [
    {
      track: "F2",
      name: "Observation",
      source: "mirror stream",
      state: summary.context.stream_state,
      ref: summary.context.reducer_checkpoint_id
    },
    {
      track: "F4",
      name: "Source",
      source: "CTP paper 19053",
      state: summary.context.source_authority,
      ref: "fixture bridge"
    },
    {
      track: "F3",
      name: "Mirror",
      source: "projection store",
      state: summary.context.projection_owner,
      ref: "read model"
    },
    {
      track: "F5",
      name: "Workbench",
      source: "account UI",
      state: "read-only",
      ref: "orders locked"
    }
  ];

  return (
    <section className="terminal-workbench-shell" data-testid="terminal-workbench-shell">
      <header className="terminal-status-bar" data-testid="terminal-top-status-bar">
        <div className="terminal-status-main">
          <Landmark size={18} />
          <div>
            <h2>{summary.account.account_id}</h2>
            <p data-testid="account-workbench-context-bar">
              {summary.workbench} / {summary.account.account_alias} / {summary.account.portfolio_uid}
            </p>
          </div>
        </div>
        <div className="terminal-status-grid">
          <span>
            <strong>Trading day</strong>
            {summary.context.trading_day}
          </span>
          <span>
            <strong>Checkpoint</strong>
            {summary.context.reducer_checkpoint_id}
          </span>
          <span>
            <strong>Observed</strong>
            {summary.context.reducer_checkpoint_ts}
          </span>
          <span>
            <strong>Stream</strong>
            <StateBadge value={summary.context.stream_state} />
          </span>
        </div>
      </header>

      <div className="terminal-layout">
        <aside className="terminal-left-rail">
          <section className="terminal-panel" data-testid="account-readback-mode">
            <div className="terminal-panel-header">
              <h3>Readback</h3>
              <StateBadge value={mirrorAccounts ? "healthy" : mirrorReadbackError ? "warning" : "stale"} />
            </div>
            <dl className="detail-list">
              <div>
                <dt>Mode</dt>
                <dd>{mirrorAccounts ? "mirror API" : "deterministic fixture fallback"}</dd>
              </div>
              <div>
                <dt>Endpoint</dt>
                <dd>/api/mirror/accounts</dd>
              </div>
              {mirrorReadbackError ? (
                <div>
                  <dt>Fallback reason</dt>
                  <dd>{mirrorReadbackError}</dd>
                </div>
              ) : null}
            </dl>
          </section>

          <section className="terminal-panel">
            <div className="terminal-panel-header">
              <h3>Accounts</h3>
              <StateBadge value={summary.account.display_state} />
            </div>
            <div className="terminal-mini-table-wrap" data-testid="account-selector">
              <table className="terminal-mini-table">
                <thead>
                  <tr>
                    <th>Alias</th>
                    <th>ID</th>
                    <th>Kind</th>
                    <th>State</th>
                  </tr>
                </thead>
                <tbody>
                  {accountRows.map((row) => (
                    <tr
                      className={
                        row.account.account_id === summary.account.account_id || row.state === fixtureState
                          ? "selected"
                          : undefined
                      }
                      key={`${row.account.account_id}-${row.state ?? "mirror"}`}
                    >
                      <td>{row.account.account_alias}</td>
                      <td>
                        {row.href ? (
                          <a className="table-link-button" href={row.href}>
                            {row.account.account_id}
                          </a>
                        ) : (
                          <button
                            className="table-link-button"
                            onClick={() => row.state && onFixtureState(row.state)}
                            type="button"
                          >
                            {row.account.account_id}
                          </button>
                        )}
                      </td>
                      <td>{formatLabel(row.account.account_kind)}</td>
                      <td>
                        <StateBadge value={row.streamState} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="terminal-panel">
            <div className="terminal-panel-header">
              <h3>Capability Gate</h3>
            </div>
            <div className="terminal-mini-table-wrap">
              <table className="terminal-mini-table" data-testid="account-capability-table">
                <thead>
                  <tr>
                    <th>Track</th>
                    <th>Name</th>
                    <th>Source</th>
                    <th>State</th>
                    <th>Ref</th>
                  </tr>
                </thead>
                <tbody>
                  {capabilityRows.map((row) => (
                    <tr data-testid="account-capability-row" key={row.track}>
                      <td>{row.track}</td>
                      <td>{row.name}</td>
                      <td>{row.source}</td>
                      <td>
                        <StateBadge value={row.state} />
                      </td>
                      <td>{row.ref}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </aside>

        <main className="terminal-center">
          {mirrorAccounts ? null : (
            <div className="filter-toolbar account-summary-toolbar terminal-fixture-toolbar">
              <label>
                <ListFilter size={14} />
                Fixture
                <select
                  onChange={(event) => onFixtureState(event.target.value as AccountSummaryFixtureState)}
                  value={fixtureState}
                >
                  {Object.entries(accountSummaryFixtureLabels).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          )}

          {summary.fixture_state === "stale" ? (
            <div className="state-callout stale" data-testid="account-summary-stale-state">
              <AlertTriangle size={16} />
              <span>
                Stale checkpoint {summary.context.reducer_checkpoint_id} at {summary.context.reducer_checkpoint_ts}
              </span>
            </div>
          ) : null}

          {summary.fixture_state === "empty" ? (
            <div className="state-callout empty-callout" data-testid="account-summary-empty-state">
              No account summary values are available for this deterministic fixture state.
            </div>
          ) : null}

          <section data-testid="account-workbench-summary-panel" aria-label="Account summary">
            <div className="terminal-summary-strip" data-testid="account-summary-metric-strip">
              <Metric
                label="Cash"
                testId="account-summary-cash"
                value={formatMoney(summary.balances.cash, baseCurrency)}
              />
              <Metric
                label="Available"
                testId="account-summary-available-cash"
                value={formatMoney(summary.balances.available_cash, baseCurrency)}
              />
              <Metric
                label="Buying power"
                testId="account-summary-buying-power"
                value={formatMoney(summary.balances.buying_power, baseCurrency)}
              />
              <Metric
                label="Margin"
                testId="account-summary-margin"
                value={formatMoney(summary.margin.initial_margin, baseCurrency)}
              />
              <Metric
                label="Unrealized PnL"
                testId="account-summary-unrealized-pnl"
                value={formatMoney(summary.pnl.unrealized, baseCurrency)}
              />
              <Metric label="Positions" testId="account-summary-position-count" value={String(visiblePositions.length)} />
            </div>
            <div className="terminal-panel terminal-table-panel terminal-funds-panel">
              <div className="terminal-panel-header">
                <h3>Funds</h3>
                <span>{summary.context.reducer_checkpoint_id}</span>
              </div>
              <div className="terminal-data-table-wrap">
                <table className="terminal-data-table compact" data-testid="tws-multi-currency-funds-table">
                  <thead>
                    <tr>
                      <th>Currency</th>
                      <th>Cash</th>
                      <th>Available</th>
                      <th>Buying power</th>
                      <th>Margin</th>
                      <th>Equity/net liq</th>
                      <th>Unrealized PnL</th>
                      <th>FX/provenance</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {summary.fixture_state === "blocked" && allBlockers.length > 0 ? (
                      allBlockers.map((blocker) => (
                        <tr data-testid="tws-funds-blocker" key={`funds-${blocker.blocker_id}`}>
                          <td data-label="Currency">blocked</td>
                          <td className="numeric-cell" data-label="Cash">missing</td>
                          <td className="numeric-cell" data-label="Available">missing</td>
                          <td className="numeric-cell" data-label="Buying power">missing</td>
                          <td className="numeric-cell" data-label="Margin">missing</td>
                          <td className="numeric-cell" data-label="Equity/net liq">missing</td>
                          <td className="numeric-cell" data-label="Unrealized PnL">missing</td>
                          <td data-label="FX/provenance" data-testid="tws-fx-provenance">
                            {formatLabel(blocker.kind)}
                          </td>
                          <td data-label="Source">
                            <CopyableCode label="funds blocker source ref" value={blocker.source_ref} />
                          </td>
                        </tr>
                      ))
                    ) : (summary.currency_balances ?? []).length > 0 ? (
                      (summary.currency_balances ?? []).map((balance) => (
                      <tr data-testid="tws-currency-balance-row" key={`funds-${balance.currency}`}>
                        <td data-label="Currency">{balance.currency}</td>
                        <td className="numeric-cell" data-label="Cash">
                          {formatMoney(balance.cash, balance.currency)}
                        </td>
                        <td className="numeric-cell" data-label="Available">
                          {formatMoney(balance.available_cash, balance.currency)}
                        </td>
                        <td className="numeric-cell" data-label="Buying power">
                          {formatMoney(balance.buying_power, balance.currency)}
                        </td>
                        <td className="numeric-cell" data-label="Margin">
                          {formatMoney(balance.margin_used, balance.currency)}
                        </td>
                        <td className="numeric-cell" data-label="Equity/net liq">
                          {formatMoney(balance.equity, balance.currency)}
                        </td>
                        <td className={`numeric-cell ${numberTone(balance.unrealized_pnl)}`} data-label="Unrealized PnL">
                          {formatMoney(balance.unrealized_pnl, balance.currency)}
                        </td>
                        <td data-label="FX/provenance" data-testid="tws-fx-provenance">
                          {balance.exchange_rate === null ? "source currency" : `FX ${balance.exchange_rate.toLocaleString()}`}
                        </td>
                        <td data-label="Source">
                          <CopyableCode label="funds source ref" value={balance.source_ref} />
                        </td>
                      </tr>
                      ))
                    ) : summary.balances.cash !== null ||
                      summary.balances.available_cash !== null ||
                      summary.margin.initial_margin !== null ||
                      summary.pnl.unrealized !== null ? (
                      <tr data-testid="tws-currency-balance-row">
                        <td data-label="Currency">{baseCurrency}</td>
                        <td className="numeric-cell" data-label="Cash">
                          {formatMoney(summary.balances.cash, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Available">
                          {formatMoney(summary.balances.available_cash, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Buying power">
                          {formatMoney(summary.balances.buying_power, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Margin">
                          {formatMoney(summary.margin.initial_margin, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Equity/net liq">
                          {formatMoney(summary.balances.cash, baseCurrency)}
                        </td>
                        <td className={`numeric-cell ${numberTone(summary.pnl.unrealized)}`} data-label="Unrealized PnL">
                          {formatMoney(summary.pnl.unrealized, baseCurrency)}
                        </td>
                        <td data-label="FX/provenance" data-testid="tws-fx-provenance">
                          source currency
                        </td>
                        <td data-label="Source">
                          <CopyableCode label="funds source ref" value={summary.source_refs[0]?.source_ref ?? summary.context.run_id} />
                        </td>
                      </tr>
                    ) : (
                      <tr data-testid="tws-funds-empty-state">
                        <td colSpan={9}>No funds rows in this fixture projection.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              <div className="funds-rollup" data-testid="tws-base-currency-rollup">
                <span>Base currency rollup</span>
                <StateBadge value={summary.fixture_state === "blocked" ? "blocked" : "healthy"} />
                <span>{summary.fixture_state === "blocked" ? "blocked until source package" : baseCurrency}</span>
              </div>
            </div>
          </section>

          <section className="terminal-panel terminal-table-panel">
            <div className="terminal-panel-header">
              <h3>Positions</h3>
              <span>{positions.context.reducer_checkpoint_id}</span>
            </div>
            <div className="terminal-data-table-wrap">
              <table className="terminal-data-table" data-testid="account-positions-table">
                <thead>
                  <tr>
                    <th>Instrument</th>
                    <th>Direction</th>
                    <th>Net</th>
                    <th>Today</th>
                    <th>Available</th>
                    <th>Avg</th>
                    <th>Last</th>
                    <th>Value</th>
                    <th>UPnL</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                    {visiblePositions.length > 0 ? (
                    visiblePositions.map((position, index) => (
                      <tr data-testid="account-position-projection-row" key={`${position.checksum}-${index}`}>
                        <td data-label="Instrument">{position.instrument}</td>
                        <td data-label="Direction">
                          <StateBadge value={position.direction} />
                        </td>
                        <td className="numeric-cell" data-label="Net">
                          {position.net_qty ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Today">
                          {position.today_qty ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Available">
                          {position.available_qty ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Avg">
                          {position.average_price ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Last">
                          {position.market_price ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Value">
                          {formatMoney(position.market_value, baseCurrency)}
                        </td>
                        <td className={`numeric-cell ${numberTone(position.unrealized_pnl)}`} data-label="UPnL">
                          {formatMoney(position.unrealized_pnl, baseCurrency)}
                        </td>
                        <td data-label="Source">
                          <CopyableCode label="position source ref" value={position.source_ref} />
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={10}>No position rows in this fixture projection.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="terminal-panel terminal-bottom-tape" data-testid="account-bottom-tape">
            <div className="terminal-panel-header">
              <h3>Open Orders / 挂单</h3>
              <span data-testid="tws-open-order-count">{visibleOrders.length}</span>
            </div>
            <div className="terminal-data-table-wrap">
              <table className="terminal-data-table compact" data-testid="tws-open-orders-table">
                <thead>
                  <tr>
                    <th>Client order</th>
                    <th>Instrument</th>
                    <th>Side</th>
                    <th>Status</th>
                    <th>Limit</th>
                    <th>Qty</th>
                    <th>Filled</th>
                    <th>Remaining</th>
                    <th>Cancelled</th>
                    <th>Evidence</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleOrders.length > 0 ? (
                    visibleOrders.map((order) => (
                      <tr data-testid="tws-open-order-row" key={`${order.source_ref}-${order.client_order_id}`}>
                        <td data-label="Client order" data-testid="tws-open-order-client-order-id">
                          <span>{order.client_order_id}</span>
                          <span data-testid="account-order-identity">{order.lifecycle_ref ?? order.client_order_id}</span>
                        </td>
                        <td data-label="Instrument" data-testid="tws-open-order-instrument">{order.instrument}</td>
                        <td data-label="Side" data-testid="tws-open-order-side">
                          <StateBadge value={order.side} />
                        </td>
                        <td data-label="Status" data-testid="tws-open-order-status">
                          <span data-testid="account-order-status">
                            <StateBadge value={order.status} />
                          </span>
                          {order.status === "partial" ? (
                            <span data-testid="account-order-partial-fill-row">partial</span>
                          ) : null}
                          {order.status === "cancel_pending" ? (
                            <span data-testid="account-cancel-pending-ref">
                              {order.report_provenance_ref ?? order.source_ref}
                            </span>
                          ) : null}
                        </td>
                        <td className="numeric-cell" data-label="Limit" data-testid="tws-open-order-limit-price">
                          {order.limit_price ?? "missing"}
                        </td>
                        <td className="numeric-cell" data-label="Qty" data-testid="tws-open-order-quantity">
                          <span data-testid="account-order-submitted-quantity">{order.quantity ?? "missing"}</span>
                        </td>
                        <td className="numeric-cell" data-label="Filled" data-testid="tws-open-order-filled">
                          <span data-testid="account-order-filled-quantity">{order.filled_quantity ?? "missing"}</span>
                        </td>
                        <td className="numeric-cell" data-label="Remaining" data-testid="tws-open-order-remaining">
                          <span data-testid="account-order-remaining-quantity">{order.remaining_quantity ?? "missing"}</span>
                          {order.status === "partial" || order.status === "working" ? (
                            <span data-testid="account-remaining-cancel-quantity">
                              {order.remaining_quantity ?? "missing"}
                            </span>
                          ) : null}
                        </td>
                        <td className="numeric-cell" data-label="Cancelled" data-testid="tws-open-order-cancelled">
                          <span data-testid="account-order-cancelled-quantity">
                            {order.cancelled_quantity ?? "missing"}
                          </span>
                        </td>
                        <td data-label="Evidence" data-testid="tws-open-order-source-ref">
                          <CopyableCode label="order source ref" value={order.source_ref} />
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={10} data-testid="tws-open-order-empty-state">No open order rows in this mirror projection.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="terminal-panel" data-testid="account-fills-tape">
            <div className="terminal-panel-header">
              <h3>Fills / 成交单</h3>
              <span data-testid="tws-fill-count">
                {executionReportRows.filter((report) => report.report_type === "FillReport").length}
              </span>
            </div>
            <div className="terminal-data-table-wrap">
              <table className="terminal-data-table compact" data-testid="tws-fills-table">
                <thead>
                  <tr>
                    <th>Report id</th>
                    <th>Client order</th>
                    <th>Venue order</th>
                    <th>Instrument</th>
                    <th>Side</th>
                    <th>Trade/status</th>
                    <th>Filled</th>
                    <th>Last price</th>
                    <th>Sequence</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {executionReportRows.filter((report) => report.report_type === "FillReport").length > 0 ? (
                    executionReportRows
                      .filter((report) => report.report_type === "FillReport")
                      .map((report) => (
                        <tr data-testid="tws-fill-row" key={`${report.report_id}-${report.source_ref}`}>
                          <td data-label="Report id" data-testid="tws-fill-report-id">{report.report_id}</td>
                          <td data-label="Client order" data-testid="tws-fill-client-order-id">
                            {report.client_order_id}
                          </td>
                          <td data-label="Venue order" data-testid="tws-fill-venue-order-id">
                            {report.venue_order_id ?? "missing"}
                          </td>
                          <td data-label="Instrument" data-testid="tws-fill-instrument">{report.instrument}</td>
                          <td data-label="Side" data-testid="tws-fill-side">
                            <StateBadge value={report.side} />
                          </td>
                          <td data-label="Trade/status" data-testid="tws-fill-status-or-trade">
                            {report.status_or_trade}
                          </td>
                          <td className="numeric-cell" data-label="Filled" data-testid="tws-fill-filled-quantity">
                            <span data-testid="account-fill-quantity">{report.filled_quantity ?? "missing"}</span>
                          </td>
                          <td className="numeric-cell" data-label="Last price" data-testid="tws-fill-last-price">
                            <span data-testid="account-fill-price">{report.limit_or_last_price ?? "missing"}</span>
                          </td>
                          <td data-label="Sequence" data-testid="tws-fill-sequence">
                            {report.sequence ?? "missing"}
                          </td>
                          <td data-label="Source" data-testid="tws-fill-source-ref">
                            <span data-testid="account-fill-source-ref">
                              <CopyableCode label="fill source ref" value={report.source_ref} />
                            </span>
                          </td>
                        </tr>
                      ))
                  ) : (
                    <tr data-testid="tws-fill-empty-state">
                      <td colSpan={10}>No fill rows in this mirror projection.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="terminal-panel" data-testid="account-order-execution-report">
            <div className="terminal-panel-header">
              <h3>Execution Reports</h3>
              <span>{executionReportRows.length}</span>
            </div>
            <div className="terminal-data-table-wrap">
              <table className="terminal-data-table compact" data-testid="tws-execution-reports-table">
                <thead>
                  <tr>
                    <th>Report type</th>
                    <th>Client order</th>
                    <th>Venue order</th>
                    <th>Instrument</th>
                    <th>Side</th>
                    <th>Status/trade</th>
                    <th>Quantity</th>
                    <th>Filled</th>
                    <th>Remaining</th>
                    <th>Limit/last</th>
                    <th>Sequence</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {executionReportRows.length > 0 ? (
                    executionReportRows
                      .map((report) => (
                        <tr
                          data-testid="tws-execution-report-row"
                          key={`${report.report_id}-${report.source_ref}`}
                        >
                          <td data-label="Report type" data-testid="tws-execution-report-type">
                            {report.report_type}
                          </td>
                          <td data-label="Client order" data-testid="tws-execution-report-client-order-id">
                            {report.client_order_id}
                          </td>
                          <td data-label="Venue order" data-testid="tws-execution-report-venue-order-id">
                            {report.venue_order_id ?? "missing"}
                          </td>
                          <td data-label="Instrument">{report.instrument}</td>
                          <td data-label="Side">
                            <StateBadge value={report.side} />
                          </td>
                          <td data-label="Status/trade">{report.status_or_trade}</td>
                          <td className="numeric-cell" data-label="Quantity">
                            {report.quantity ?? "missing"}
                          </td>
                          <td className="numeric-cell" data-label="Filled">
                            {report.filled_quantity ?? "missing"}
                          </td>
                          <td className="numeric-cell" data-label="Remaining">
                            {report.remaining_quantity ?? "missing"}
                          </td>
                          <td className="numeric-cell" data-label="Limit/last">
                            {report.limit_or_last_price ?? "missing"}
                          </td>
                          <td data-label="Sequence" data-testid="tws-execution-report-sequence">
                            {report.sequence ?? "missing"}
                          </td>
                          <td data-label="Source" data-testid="tws-execution-report-source-ref">
                            <CopyableCode
                              label="report provenance ref"
                              value={report.source_ref}
                            />
                            {report.reload_checkpoint_id ? (
                              <small data-testid="tws-execution-report-reload-ref">
                                {report.reload_checkpoint_id}
                              </small>
                            ) : null}
                          </td>
                        </tr>
                      ))
                  ) : allBlockers.length > 0 ? (
                    allBlockers.map((blocker) => (
                      <tr data-testid="tws-execution-report-blocker" key={`execution-report-${blocker.blocker_id}`}>
                        <td data-label="Report type">blocked</td>
                        <td data-label="Client order" colSpan={2}>
                          {blocker.blocker_id}
                        </td>
                        <td data-label="Instrument">missing</td>
                        <td data-label="Side">missing</td>
                        <td data-label="Status/trade">{formatLabel(blocker.kind)}</td>
                        <td className="numeric-cell" data-label="Quantity">
                          missing
                        </td>
                        <td className="numeric-cell" data-label="Filled">
                          missing
                        </td>
                        <td className="numeric-cell" data-label="Remaining">
                          missing
                        </td>
                        <td className="numeric-cell" data-label="Limit/last">
                          missing
                        </td>
                        <td data-label="Sequence">blocked</td>
                        <td data-label="Source">
                          <CopyableCode label="execution report blocker source ref" value={blocker.source_ref} />
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr data-testid="tws-execution-report-empty-state">
                      <td colSpan={12}>No execution report provenance rows in this projection.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </main>

        <aside className="terminal-right-rail">
          <section className="terminal-panel" data-testid="account-source-health-panel">
            <div className="terminal-panel-header">
              <h3>Source Health</h3>
              <StateBadge value={summary.fixture_state} />
            </div>
            <dl className="detail-list">
              <div>
                <dt>Authority</dt>
                <dd>{summary.context.source_authority}</dd>
              </div>
              <div>
                <dt>Projection owner</dt>
                <dd>{summary.context.projection_owner}</dd>
              </div>
              <div>
                <dt>Session</dt>
                <dd>{summary.context.session_id}</dd>
              </div>
              <div>
                <dt>Run</dt>
                <dd>{summary.context.run_id}</dd>
              </div>
              {sourceHealthDetails?.market_source ? (
                <div>
                  <dt>Market</dt>
                  <dd>{asText(sourceHealthDetails.market_source)}</dd>
                </div>
              ) : null}
              {sourceHealthDetails?.execution_target ? (
                <div>
                  <dt>Execution</dt>
                  <dd>{asText(sourceHealthDetails.execution_target)}</dd>
                </div>
              ) : null}
              {sourceHealthDetails?.orders_scope ? (
                <div>
                  <dt>Orders</dt>
                  <dd>{asText(sourceHealthDetails.orders_scope)}</dd>
                </div>
              ) : null}
              {typeof sourceHealthDetails?.broker_order_submission === "boolean" ? (
                <div>
                  <dt>Broker submission</dt>
                  <dd>{sourceHealthDetails.broker_order_submission ? "enabled" : "disabled"}</dd>
                </div>
              ) : null}
              {sourceHealthDetails?.ledger_type ? (
                <div>
                  <dt>Ledger</dt>
                  <dd>{asText(sourceHealthDetails.ledger_type)}</dd>
                </div>
              ) : null}
              {sourceHealthDetails?.stage ? (
                <div>
                  <dt>Stage</dt>
                  <dd>{asText(sourceHealthDetails.stage)}</dd>
                </div>
              ) : null}
            </dl>
          </section>

          <section className="terminal-panel" data-testid="account-command-capability-state">
            <div className="terminal-panel-header">
              <h3>Command Plane</h3>
              <StateBadge value={summary.boundaries.action_controls ? "warning" : "empty"} />
            </div>
            <dl className="detail-list">
              <div>
                <dt>Mode</dt>
                <dd data-testid="account-command-mode">observation only</dd>
              </div>
              <div>
                <dt>Controls</dt>
                <dd>none mounted</dd>
              </div>
              <div>
                <dt>Broker adapter</dt>
                <dd>not bound in this view</dd>
              </div>
            </dl>
          </section>

          <CommandStatusPanel status={mirrorReadback?.selected.command_status ?? null} />

          <section className="terminal-panel" data-testid="account-summary-boundary-list">
            <div className="terminal-panel-header">
              <h3>Boundaries</h3>
              <StateBadge value="read-only" />
            </div>
            <div className="boundary-grid terminal-boundary-grid">
              <div className="boundary-item">
                <span>Read-only projection</span>
                <StateBadge value={summary.boundaries.read_only_projection ? "healthy" : "empty"} />
              </div>
              <div className="boundary-item">
                <span>UI authority</span>
                <StateBadge value={summary.boundaries.ui_truth ? "warning" : "empty"} />
              </div>
              <div className="boundary-item">
                <span>Action controls</span>
                <StateBadge value={summary.boundaries.action_controls ? "warning" : "empty"} />
              </div>
            </div>
          </section>

          <section className="terminal-panel terminal-evidence-rail" data-testid="account-evidence-rail">
            <div className="terminal-panel-header">
              <h3>Evidence</h3>
              <span>{allSourceRefs.length} refs</span>
            </div>
            <div className="evidence-stack">
              {allSourceRefs.slice(0, 6).map((source, index) => (
                <article
                  className="evidence-item"
                  data-testid="account-summary-source-ref"
                  key={`${source.kind}-${source.checksum}-${index}`}
                >
                  <strong>{formatLabel(source.kind)}</strong>
                  <span>{source.owner}</span>
                  <CopyableCode label="source ref" value={source.source_ref} />
                </article>
              ))}
            </div>
          </section>

          <section className="terminal-panel">
            <div className="terminal-panel-header">
              <h3>Blockers</h3>
              <span>{allBlockers.length}</span>
            </div>
            {allBlockers.length > 0 ? (
              <div className="blocker-list">
                {allBlockers.map((blocker) => (
                  <article
                    className="blocker-item"
                    data-testid="account-blocker-row"
                    key={`${blocker.blocker_id}-${blocker.checksum}`}
                  >
                    <div className="blocker-head">
                      <StateBadge value={blocker.severity} />
                      <strong data-testid="account-summary-blocker">{formatLabel(blocker.kind)}</strong>
                    </div>
                    <dl className="detail-list">
                      <div>
                        <dt>Owner</dt>
                        <dd>{blocker.owner}</dd>
                      </div>
                      <div>
                        <dt>Next action</dt>
                        <dd>{blocker.next_action}</dd>
                      </div>
                    </dl>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">No blockers in this read-only fixture projection.</p>
            )}
          </section>
        </aside>
      </div>
    </section>
  );
}

function AccountSummaryPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountSummaryPanelReadModel;
  fixtureState: AccountSummaryFixtureState;
  onFixtureState: (value: AccountSummaryFixtureState) => void;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Paper state flag", fixture.boundaries.paper_ready],
    ["Live state flag", fixture.boundaries.live_ready],
    ["Broker action flag", fixture.boundaries.broker_tradable],
    ["Admission authority", fixture.boundaries.admission_truth],
    ["Capital authority", fixture.boundaries.capital_truth],
    ["Action controls", fixture.boundaries.action_controls]
  ];

  return (
    <section className="account-summary-grid" data-testid="account-workbench-summary-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-workbench-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / {fixture.account.portfolio_uid}
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountSummaryFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountSummaryFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-summary-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-summary-empty-state">
            No account summary values are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-summary-metric-strip">
          <Metric label="Cash" value={formatMoney(fixture.balances.cash, fixture.account.base_currency)} />
          <Metric
            label="Available cash"
            value={formatMoney(fixture.balances.available_cash, fixture.account.base_currency)}
          />
          <Metric
            label="Buying power"
            value={formatMoney(fixture.balances.buying_power, fixture.account.base_currency)}
          />
          <Metric
            label="Initial margin"
            value={formatMoney(fixture.margin.initial_margin, fixture.account.base_currency)}
          />
          <Metric label="Realized PnL" value={formatMoney(fixture.pnl.realized, fixture.account.base_currency)} />
          <Metric
            label="Unrealized PnL"
            value={formatMoney(fixture.pnl.unrealized, fixture.account.base_currency)}
          />
        </div>

        <div className="account-summary-sections">
          <section className="summary-section" data-testid="account-workbench-tab-list">
            <h3>Account Context</h3>
            <dl className="detail-list two-column">
              <div>
                <dt>Account ID</dt>
                <dd>{fixture.account.account_id}</dd>
              </div>
              <div>
                <dt>Account kind</dt>
                <dd>{formatLabel(fixture.account.account_kind)}</dd>
              </div>
              <div>
                <dt>Display state</dt>
                <dd>
                  <StateBadge value={fixture.account.display_state} />
                </dd>
              </div>
              <div>
                <dt>Settlement</dt>
                <dd>
                  <StateBadge value={fixture.settlement.state} />
                </dd>
              </div>
            </dl>
          </section>

          <section className="summary-section" data-testid="account-positions-panel">
            <h3>Positions</h3>
            {fixture.positions.length > 0 ? (
              <div className="position-list">
                {fixture.positions.map((position) => (
                  <article className="position-item" key={`${position.instrument}-${position.checksum}`}>
                    <strong>{position.instrument}</strong>
                    <span>Net {position.net_qty ?? "missing"}</span>
                    <span>{formatMoney(position.market_value, fixture.account.base_currency)}</span>
                    <CopyableCode label="position source ref" value={position.source_ref} />
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">No position rows in this fixture state.</p>
            )}
          </section>
        </div>

        <div className="boundary-grid" data-testid="account-summary-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-summary-detail-drawer">
        <div className="drawer-section">
          <h3>Source Refs</h3>
          <div className="evidence-stack">
            {fixture.source_refs.map((source, index) => (
              <article
                className="evidence-item"
                data-testid="account-summary-source-ref"
                key={`${source.checksum}-${index}`}
              >
                <strong>{formatLabel(source.kind)}</strong>
                <dl className="detail-list">
                  <div>
                    <dt>Owner</dt>
                    <dd>{source.owner}</dd>
                  </div>
                  <div>
                    <dt>Authority</dt>
                    <dd>{source.authority}</dd>
                  </div>
                  <div>
                    <dt>Source</dt>
                    <dd>
                      <CopyableCode label="source ref" value={source.source_ref} />
                    </dd>
                  </div>
                  <div>
                    <dt>Checksum</dt>
                    <dd>
                      <CopyableCode label="checksum" value={source.checksum} />
                    </dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        </div>

        <div className="drawer-section">
          <h3>Blockers</h3>
          {fixture.blockers.length > 0 ? (
            <div className="blocker-list">
              {fixture.blockers.map((blocker) => (
                <article className="blocker-item" data-testid="account-summary-blocker" key={blocker.blocker_id}>
                  <div className="blocker-head">
                    <StateBadge value={blocker.severity} />
                    <strong>{formatLabel(blocker.kind)}</strong>
                  </div>
                  <dl className="detail-list">
                    <div>
                      <dt>Owner</dt>
                      <dd>{blocker.owner}</dd>
                    </div>
                    <div>
                      <dt>Next action</dt>
                      <dd>{blocker.next_action}</dd>
                    </div>
                    <div>
                      <dt>Source</dt>
                      <dd>
                        <CopyableCode label="blocker source ref" value={blocker.source_ref} />
                      </dd>
                    </div>
                  </dl>
                </article>
              ))}
            </div>
          ) : (
            <p className="muted">No blockers in this read-only fixture projection.</p>
          )}
        </div>
      </aside>
    </section>
  );
}

function AccountOrdersPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountOrdersPanelReadModel;
  fixtureState: AccountOrdersFixtureState;
  onFixtureState: (value: AccountOrdersFixtureState) => void;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Account authority", fixture.boundaries.account_truth],
    ["Order authority", fixture.boundaries.order_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Broker action flag", fixture.boundaries.broker_tradable],
    ["Action controls", fixture.boundaries.action_controls]
  ];

  return (
    <section className="account-summary-grid" data-testid="account-orders-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-orders-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Orders
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountOrdersFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountOrdersFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-orders-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale order checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-orders-empty-state">
            No order rows are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-orders-metric-strip">
          <Metric label="Orders" value={String(fixture.orders.length)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
          <Metric label="Checkpoint" value={fixture.context.reducer_checkpoint_id} />
          <Metric label="Stream" value={fixture.context.stream_state} />
        </div>

        <section className="summary-section" data-testid="account-orders-table">
          <h3>Order Rows</h3>
          {fixture.orders.length > 0 ? (
            <div className="order-list">
              {fixture.orders.map((order) => (
                <OrderRowCard order={order} key={`${order.source_ref}-${order.client_order_id}`} />
              ))}
            </div>
          ) : (
            <p className="muted">No order rows in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-orders-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-orders-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-orders-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-orders-blocker" />
      </aside>
    </section>
  );
}

function AccountPositionsPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountPositionsPanelReadModel;
  fixtureState: AccountPositionsFixtureState;
  onFixtureState: (value: AccountPositionsFixtureState) => void;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Account authority", fixture.boundaries.account_truth],
    ["Position authority", false],
    ["Order authority", fixture.boundaries.order_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Broker action flag", fixture.boundaries.broker_tradable],
    ["Action controls", fixture.boundaries.action_controls]
  ];

  return (
    <section className="account-summary-grid" data-testid="account-positions-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-positions-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Positions
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountPositionsFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountPositionsFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-positions-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale position checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-positions-empty-state">
            No position rows are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-positions-metric-strip">
          <Metric label="Positions" value={String(fixture.positions.length)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
          <Metric label="Checkpoint" value={fixture.context.reducer_checkpoint_id} />
          <Metric label="Stream" value={fixture.context.stream_state} />
          <Metric label="Carryover refs" value={String(fixture.positions.filter((row) => row.carryover_ref).length)} />
          <Metric label="Settlement refs" value={String(fixture.positions.filter((row) => row.settlement_ref).length)} />
        </div>

        <section className="summary-section" data-testid="account-positions-table">
          <h3>Position Rows</h3>
          {fixture.positions.length > 0 ? (
            <div className="order-list">
              {fixture.positions.map((position) => (
                <PositionRowCard position={position} key={`${position.account_id}-${position.instrument}-${position.checksum}`} />
              ))}
            </div>
          ) : (
            <p className="muted">No position rows in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-positions-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-positions-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-positions-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-positions-blocker" />
        <div className="drawer-section">
          <h3>Rejection Rules</h3>
          <div className="rule-list">
            {fixture.rejection_rules.map((rule) => (
              <div className="rule-item" data-testid="account-positions-rejection-rule" key={rule}>
                <AlertTriangle size={14} />
                <span>{rule}</span>
              </div>
            ))}
          </div>
        </div>
      </aside>
    </section>
  );
}

function AccountSettlementPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountSettlementPanelReadModel;
  fixtureState: AccountSettlementFixtureState;
  onFixtureState: (value: AccountSettlementFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Settlement authority");
  const settlement = fixture.settlement;

  return (
    <section className="account-summary-grid" data-testid="account-settlement-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-settlement-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Settlement
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountSettlementFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountSettlementFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-settlement-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale settlement checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-settlement-empty-state">
            No settlement values are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-settlement-metric-strip">
          <Metric label="Cash" value={formatMoney(settlement.cash)} />
          <Metric label="Frozen cash" value={formatMoney(settlement.frozen_cash)} />
          <Metric label="Margin" value={formatMoney(settlement.margin)} />
          <Metric label="Realized PnL" value={formatMoney(settlement.realized_pnl)} />
          <Metric label="Unrealized PnL" value={formatMoney(settlement.unrealized_pnl)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
        </div>

        <section className="summary-section" data-testid="account-settlement-table">
          <h3>Settlement Refs</h3>
          <dl className="detail-list two-column" data-testid="account-settlement-row">
            <div>
              <dt>Trading day</dt>
              <dd>{settlement.trading_day}</dd>
            </div>
            <div>
              <dt>State</dt>
              <dd>
                <StateBadge value={settlement.settlement_state} />
              </dd>
            </div>
            <div>
              <dt>Previous settlement ref</dt>
              <dd>
                {settlement.previous_settlement_ref ? (
                  <CopyableCode label="previous settlement ref" value={settlement.previous_settlement_ref} />
                ) : (
                  "missing"
                )}
              </dd>
            </div>
            <div>
              <dt>Current settlement ref</dt>
              <dd>
                {settlement.current_settlement_ref ? (
                  <CopyableCode label="current settlement ref" value={settlement.current_settlement_ref} />
                ) : (
                  "missing"
                )}
              </dd>
            </div>
            <div>
              <dt>Position carryover ref</dt>
              <dd>
                {settlement.position_carryover_ref ? (
                  <CopyableCode label="position carryover ref" value={settlement.position_carryover_ref} />
                ) : (
                  "missing"
                )}
              </dd>
            </div>
            <div>
              <dt>Source ref</dt>
              <dd>
                <CopyableCode label="settlement source ref" value={settlement.source_ref} />
              </dd>
            </div>
          </dl>
        </section>

        <div className="boundary-grid" data-testid="account-settlement-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-settlement-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-settlement-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-settlement-blocker" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-settlement-rejection-rule" />
      </aside>
    </section>
  );
}

function AccountEquityPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountEquityPanelReadModel;
  fixtureState: AccountEquityFixtureState;
  onFixtureState: (value: AccountEquityFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Equity authority");
  const latestPoint = fixture.equity_points.at(-1) ?? null;
  const firstPoint = fixture.equity_points[0] ?? null;
  const equityDelta =
    latestPoint?.equity != null && firstPoint?.equity != null ? latestPoint.equity - firstPoint.equity : null;

  return (
    <section className="account-summary-grid" data-testid="account-equity-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-equity-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Equity
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountEquityFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountEquityFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-equity-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale equity checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-equity-empty-state">
            No equity points are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-equity-metric-strip">
          <Metric label="Latest equity" value={formatMoney(latestPoint?.equity ?? null)} />
          <Metric label="Latest balance" value={formatMoney(latestPoint?.balance ?? null)} />
          <Metric label="Available cash" value={formatMoney(latestPoint?.available_cash ?? null)} />
          <Metric label="Margin" value={formatMoney(latestPoint?.margin ?? null)} />
          <Metric label="Equity delta" value={formatMoney(equityDelta)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
        </div>

        <section className="summary-section" data-testid="account-equity-table">
          <h3>Equity Points</h3>
          {fixture.equity_points.length > 0 ? (
            <div className="order-list">
              {fixture.equity_points.map((point) => (
                <EquityPointCard key={point.checksum} point={point} />
              ))}
            </div>
          ) : (
            <p className="muted">No equity points in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-equity-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-equity-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-equity-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-equity-blocker" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-equity-rejection-rule" />
      </aside>
    </section>
  );
}

function AccountReconcilePanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountReconcilePanelReadModel;
  fixtureState: AccountReconcileFixtureState;
  onFixtureState: (value: AccountReconcileFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Reconcile authority");
  const mismatchCount = fixture.reconcile_items.filter((item) => item.status === "mismatch").length;
  const missingRefs = fixture.reconcile_items.filter((item) => !item.tolerance_ref || !item.mismatch_ref).length;

  return (
    <section className="account-summary-grid" data-testid="account-reconcile-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-reconcile-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Reconcile
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountReconcileFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountReconcileFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-reconcile-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale reconcile checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-reconcile-empty-state">
            No reconcile rows are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-reconcile-metric-strip">
          <Metric label="Reconcile rows" value={String(fixture.reconcile_items.length)} />
          <Metric label="Mismatches" value={String(mismatchCount)} />
          <Metric label="Missing refs" value={String(missingRefs)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
          <Metric label="Checkpoint" value={fixture.context.reducer_checkpoint_id} />
          <Metric label="Stream" value={fixture.context.stream_state} />
        </div>

        <section className="summary-section" data-testid="account-reconcile-table">
          <h3>Reconcile Items</h3>
          {fixture.reconcile_items.length > 0 ? (
            <div className="order-list">
              {fixture.reconcile_items.map((item) => (
                <ReconcileItemCard item={item} key={`${item.item_id}-${item.checksum}`} />
              ))}
            </div>
          ) : (
            <p className="muted">No reconcile rows in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-reconcile-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-reconcile-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-reconcile-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-reconcile-blocker" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-reconcile-rejection-rule" />
      </aside>
    </section>
  );
}

function AccountIncidentsPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountIncidentsPanelReadModel;
  fixtureState: AccountIncidentsFixtureState;
  onFixtureState: (value: AccountIncidentsFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Incident authority");
  const openCount = fixture.incidents.filter((incident) => incident.status === "open").length;
  const missingRepairRefs = fixture.incidents.filter((incident) => !incident.repair_ref).length;

  return (
    <section className="account-summary-grid" data-testid="account-incidents-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-incidents-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Incidents
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountIncidentsFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountIncidentsFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-incidents-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale incident checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-incidents-empty-state">
            No incident rows are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-incidents-metric-strip">
          <Metric label="Incidents" value={String(fixture.incidents.length)} />
          <Metric label="Open" value={String(openCount)} />
          <Metric label="Missing repair refs" value={String(missingRepairRefs)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
          <Metric label="Checkpoint" value={fixture.context.reducer_checkpoint_id} />
          <Metric label="Stream" value={fixture.context.stream_state} />
        </div>

        <section className="summary-section" data-testid="account-incidents-table">
          <h3>Incident Rows</h3>
          {fixture.incidents.length > 0 ? (
            <div className="order-list">
              {fixture.incidents.map((incident) => (
                <IncidentRowCard incident={incident} key={incident.checksum} />
              ))}
            </div>
          ) : (
            <p className="muted">No incident rows in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-incidents-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-incidents-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-incidents-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-incidents-blocker" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-incidents-rejection-rule" />
      </aside>
    </section>
  );
}

function AccountEvidencePanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountEvidencePanelReadModel;
  fixtureState: AccountEvidenceFixtureState;
  onFixtureState: (value: AccountEvidenceFixtureState) => void;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Evidence authority");
  const missingRawPayloadRefs = fixture.evidence_packages.filter((item) => !item.raw_payload_ref).length;
  const missingNormalizedRefs = fixture.evidence_packages.filter((item) => !item.normalized_ref).length;

  return (
    <section className="account-summary-grid" data-testid="account-evidence-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-evidence-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / Evidence
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountEvidenceFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountEvidenceFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-evidence-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale evidence checkpoint {fixture.context.reducer_checkpoint_id} at{" "}
              {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        {fixture.fixture_state === "empty" ? (
          <div className="state-callout empty-callout" data-testid="account-evidence-empty-state">
            No evidence packages are available for this deterministic fixture state.
          </div>
        ) : null}

        <div className="metric-strip account-summary-metrics" data-testid="account-evidence-metric-strip">
          <Metric label="Packages" value={String(fixture.evidence_packages.length)} />
          <Metric label="Blockers" value={String(fixture.blockers.length)} />
          <Metric label="Missing raw refs" value={String(missingRawPayloadRefs)} />
          <Metric label="Missing normalized refs" value={String(missingNormalizedRefs)} />
          <Metric label="Checkpoint" value={fixture.context.reducer_checkpoint_id} />
          <Metric label="Stream" value={fixture.context.stream_state} />
        </div>

        <section className="summary-section" data-testid="account-evidence-table">
          <h3>Evidence Packages</h3>
          {fixture.evidence_packages.length > 0 ? (
            <div className="order-list">
              {fixture.evidence_packages.map((evidencePackage) => (
                <EvidencePackageCard evidencePackage={evidencePackage} key={evidencePackage.checksum} />
              ))}
            </div>
          ) : (
            <p className="muted">No evidence packages in this fixture projection.</p>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-evidence-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-evidence-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-evidence-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-evidence-blocker" />
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-evidence-rejection-rule" />
      </aside>
    </section>
  );
}

function AccountOrderDetailPanel({
  fixture,
  fixtureState,
  onFixtureState
}: {
  fixture: AccountOrderDetailPanelReadModel;
  fixtureState: AccountOrderDetailFixtureState;
  onFixtureState: (value: AccountOrderDetailFixtureState) => void;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Account authority", fixture.boundaries.account_truth],
    ["Order authority", fixture.boundaries.order_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Action controls", fixture.boundaries.action_controls]
  ];

  return (
    <section className="account-summary-grid" data-testid="account-order-detail-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>{fixture.panel}</h2>
            <p data-testid="account-order-detail-context-bar">
              {fixture.workbench} / {fixture.account.account_alias} / {fixture.order.client_order_id}
            </p>
          </div>
          <StateBadge value={fixture.fixture_state} />
        </div>

        <div className="filter-toolbar account-summary-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountOrderDetailFixtureState)}
              value={fixtureState}
            >
              {Object.entries(accountOrderDetailFixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <OrderRowCard order={fixture.order} />

        <section className="summary-section" data-testid="account-order-lifecycle-events">
          <h3>Lifecycle Events</h3>
          {fixture.events.length > 0 ? (
            <div className="event-timeline">
              {fixture.events.map((event) => (
                <article className="timeline-item" key={event.event_id}>
                  <div>
                    <strong>
                      #{event.event_seq} {formatLabel(event.event_type)}
                    </strong>
                    <span>{event.event_ts}</span>
                  </div>
                  <StateBadge value={event.event_type === "filled" ? "healthy" : "partial"} />
                  <dl className="detail-list">
                    <div>
                      <dt>Status</dt>
                      <dd>{event.status}</dd>
                    </div>
                    <div>
                      <dt>Quantity</dt>
                      <dd>{event.quantity ?? "missing"}</dd>
                    </div>
                    <div>
                      <dt>Price</dt>
                      <dd>{event.price ?? "missing"}</dd>
                    </div>
                    <div>
                      <dt>Authority</dt>
                      <dd>{event.authority}</dd>
                    </div>
                    <div>
                      <dt>Source</dt>
                      <dd>
                        <CopyableCode label="event source ref" value={event.source_ref} />
                      </dd>
                    </div>
                  </dl>
                </article>
              ))}
            </div>
          ) : (
            <div className="state-callout blocked" data-testid="account-order-detail-blocked-state">
              Official order events are missing for this fixture state.
            </div>
          )}
        </section>

        <div className="boundary-grid" data-testid="account-order-detail-boundary-list">
          {boundaryRows.map(([label, value]) => (
            <div className="boundary-item" key={label}>
              <span>{label}</span>
              <StateBadge value={value ? "healthy" : "empty"} />
            </div>
          ))}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="account-order-detail-drawer">
        <SourceRefsList refs={fixture.source_refs} testId="account-order-detail-source-ref" />
        <SourceRefsList refs={fixture.report_provenance} title="Report Provenance" testId="account-order-report-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-order-detail-blocker" />
      </aside>
    </section>
  );
}

function PositionRowCard({ position }: { position: AccountPositionRow }) {
  return (
    <article className="order-card" data-testid="account-position-row">
      <div className="order-card-head">
        <div>
          <strong>{position.instrument}</strong>
          <span>
            {position.direction} / account {position.account_id}
          </span>
        </div>
        <StateBadge value={position.carryover_ref && position.settlement_ref ? "healthy" : "partial"} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Net quantity</dt>
          <dd>{position.net_qty ?? "missing"}</dd>
        </div>
        <div>
          <dt>Today / Yesterday</dt>
          <dd>
            {position.today_qty ?? "missing"} / {position.yesterday_qty ?? "missing"}
          </dd>
        </div>
        <div>
          <dt>Available / Frozen</dt>
          <dd>
            {position.available_qty ?? "missing"} / {position.frozen_qty ?? "missing"}
          </dd>
        </div>
        <div>
          <dt>Average price</dt>
          <dd>{position.average_price ?? "missing"}</dd>
        </div>
        <div>
          <dt>Market price</dt>
          <dd>{position.market_price ?? "missing"}</dd>
        </div>
        <div>
          <dt>Market value</dt>
          <dd>{position.market_value ?? "missing"}</dd>
        </div>
        <div>
          <dt>Unrealized PnL</dt>
          <dd>{position.unrealized_pnl ?? "missing"}</dd>
        </div>
        <div>
          <dt>Checksum</dt>
          <dd>
            <CopyableCode label="position checksum" value={position.checksum} />
          </dd>
        </div>
      </dl>
      <div className="position-ref-grid">
        <Ref label="Carryover ref" value={position.carryover_ref ?? "missing"} />
        <Ref label="Settlement ref" value={position.settlement_ref ?? "missing"} />
        <Ref label="Source ref" value={position.source_ref} />
      </div>
    </article>
  );
}

function OrderRowCard({ order }: { order: AccountOrderRow }) {
  return (
    <article className="order-card" data-testid="account-order-row">
      <div className="order-card-head">
        <div>
          <strong data-testid="tws-open-order-client-order-id">{order.client_order_id}</strong>
          <span>
            <span data-testid="tws-open-order-instrument">{order.instrument}</span> ·{" "}
            <span data-testid="tws-open-order-side">{order.side}</span> · {order.offset}
          </span>
        </div>
        <span data-testid="tws-open-order-status">
          <StateBadge value={order.status} />
        </span>
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Type</dt>
          <dd>{order.order_type}</dd>
        </div>
        <div>
          <dt>Limit</dt>
          <dd data-testid="tws-open-order-limit-price">{order.limit_price ?? "missing"}</dd>
        </div>
        <div>
          <dt>Quantity</dt>
          <dd data-testid="tws-open-order-quantity">{order.quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>Filled</dt>
          <dd data-testid="tws-open-order-filled">{order.filled_quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>Remaining</dt>
          <dd data-testid="tws-open-order-remaining">{order.remaining_quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>TIF</dt>
          <dd data-testid="tws-open-order-time-in-force">{order.time_in_force ?? "missing"}</dd>
        </div>
        <div>
          <dt>Destination</dt>
          <dd data-testid="tws-open-order-destination">{order.destination ?? "missing"}</dd>
        </div>
        <div>
          <dt>Lifecycle ref</dt>
          <dd>{order.lifecycle_ref ? <CopyableCode label="lifecycle ref" value={order.lifecycle_ref} /> : "missing"}</dd>
        </div>
      </dl>
      <span data-testid="tws-open-order-source-ref">
        <CopyableCode label="order source ref" value={order.source_ref} />
      </span>
    </article>
  );
}

function SourceRefsList({
  refs,
  testId,
  title = "Source Refs"
}: {
  refs: Array<{ kind: string; owner: string; source_ref: string; checksum: string; authority: string }>;
  testId: string;
  title?: string;
}) {
  return (
    <div className="drawer-section">
      <h3>{title}</h3>
      <div className="evidence-stack">
        {refs.map((source) => (
          <article className="evidence-item" data-testid={testId} key={`${testId}-${source.checksum}`}>
            <strong>{formatLabel(source.kind)}</strong>
            <dl className="detail-list">
              <div>
                <dt>Owner</dt>
                <dd>{source.owner}</dd>
              </div>
              <div>
                <dt>Authority</dt>
                <dd>{source.authority}</dd>
              </div>
              <div>
                <dt>Source</dt>
                <dd>
                  <CopyableCode label="source ref" value={source.source_ref} />
                </dd>
              </div>
              <div>
                <dt>Checksum</dt>
                <dd>
                  <CopyableCode label="checksum" value={source.checksum} />
                </dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </div>
  );
}

function RejectionRuleList({ rules, testId }: { rules: string[]; testId: string }) {
  return (
    <div className="drawer-section">
      <h3>Rejection Rules</h3>
      <div className="rule-list">
        {rules.map((rule) => (
          <div className="rule-item" data-testid={testId} key={rule}>
            <AlertTriangle size={14} />
            <span>{rule}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function accountBoundaryRows(
  boundaries: {
    read_only_projection: boolean;
    runtime_truth: boolean;
    account_truth: boolean;
    order_truth: boolean;
    ledger_truth: boolean;
    ui_truth: boolean;
    broker_tradable: boolean;
    action_controls: boolean;
  },
  domainAuthorityLabel: string
): Array<[string, boolean]> {
  return [
    ["Read-only projection", boundaries.read_only_projection],
    ["Runtime authority", boundaries.runtime_truth],
    ["Account authority", boundaries.account_truth],
    [domainAuthorityLabel, false],
    ["Order authority", boundaries.order_truth],
    ["Ledger authority", boundaries.ledger_truth],
    ["UI authority", boundaries.ui_truth],
    ["Broker action flag", boundaries.broker_tradable],
    ["Action controls", boundaries.action_controls]
  ];
}

function formatMaybeValue(value: number | string | null): string {
  if (value === null) {
    return "missing";
  }
  return String(value);
}

function ReconcileItemCard({ item }: { item: AccountReconcileItem }) {
  return (
    <article className="order-card" data-testid="account-reconcile-row">
      <div className="order-card-head">
        <div>
          <strong>{item.item_id}</strong>
          <span>{formatLabel(item.category)}</span>
        </div>
        <StateBadge value={item.status} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Severity</dt>
          <dd>
            <StateBadge value={item.severity} />
          </dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{item.owner}</dd>
        </div>
        <div>
          <dt>Expected</dt>
          <dd>{formatMaybeValue(item.expected_value)}</dd>
        </div>
        <div>
          <dt>Observed</dt>
          <dd>{formatMaybeValue(item.observed_value)}</dd>
        </div>
        <div>
          <dt>Delta</dt>
          <dd>{formatMaybeValue(item.delta)}</dd>
        </div>
        <div>
          <dt>Next action</dt>
          <dd>{item.next_action}</dd>
        </div>
        <div>
          <dt>Tolerance ref</dt>
          <dd>{item.tolerance_ref ? <CopyableCode label="tolerance ref" value={item.tolerance_ref} /> : "missing"}</dd>
        </div>
        <div>
          <dt>Mismatch ref</dt>
          <dd>{item.mismatch_ref ? <CopyableCode label="mismatch ref" value={item.mismatch_ref} /> : "missing"}</dd>
        </div>
      </dl>
      <CopyableCode label="reconcile source ref" value={item.source_ref} />
    </article>
  );
}

function IncidentRowCard({ incident }: { incident: AccountIncidentRow }) {
  return (
    <article className="order-card" data-testid="account-incident-row">
      <div className="order-card-head">
        <div>
          <strong>{incident.incident_id}</strong>
          <span>{formatLabel(incident.category)}</span>
        </div>
        <StateBadge value={incident.status} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Severity</dt>
          <dd>
            <StateBadge value={incident.severity} />
          </dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{incident.owner}</dd>
        </div>
        <div>
          <dt>Next action</dt>
          <dd>{incident.next_action}</dd>
        </div>
        <div>
          <dt>Repair ref</dt>
          <dd>{incident.repair_ref ? <CopyableCode label="repair ref" value={incident.repair_ref} /> : "missing"}</dd>
        </div>
      </dl>
      <CopyableCode label="incident source ref" value={incident.source_ref} />
    </article>
  );
}

function EvidencePackageCard({ evidencePackage }: { evidencePackage: AccountEvidencePackage }) {
  return (
    <article className="order-card" data-testid="account-evidence-package-row">
      <div className="order-card-head">
        <div>
          <strong>{evidencePackage.package_id}</strong>
          <span>{formatLabel(evidencePackage.kind)}</span>
        </div>
        <StateBadge value={evidencePackage.status} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Owner</dt>
          <dd>{evidencePackage.owner}</dd>
        </div>
        <div>
          <dt>Trading day</dt>
          <dd>{evidencePackage.trading_day}</dd>
        </div>
        <div>
          <dt>Schema</dt>
          <dd>
            <CopyableCode label="schema ref" value={evidencePackage.schema_ref} />
          </dd>
        </div>
        <div>
          <dt>Schema version</dt>
          <dd>{evidencePackage.schema_version_ref}</dd>
        </div>
        <div>
          <dt>Run</dt>
          <dd>{evidencePackage.run_id ?? "missing"}</dd>
        </div>
        <div>
          <dt>Session</dt>
          <dd>{evidencePackage.session_id}</dd>
        </div>
        <div>
          <dt>Normalized ref</dt>
          <dd>
            {evidencePackage.normalized_ref ? (
              <CopyableCode label="normalized ref" value={evidencePackage.normalized_ref} />
            ) : (
              "missing"
            )}
          </dd>
        </div>
        <div>
          <dt>Raw payload ref</dt>
          <dd>
            {evidencePackage.raw_payload_ref ? (
              <CopyableCode label="raw payload ref" value={evidencePackage.raw_payload_ref} />
            ) : (
              "missing"
            )}
          </dd>
        </div>
        <div>
          <dt>Next action</dt>
          <dd>{evidencePackage.next_action}</dd>
        </div>
      </dl>
      <CopyableCode label="evidence source ref" value={evidencePackage.source_ref} />
      <CopyableCode label="evidence checksum" value={evidencePackage.checksum} />
    </article>
  );
}

function EquityPointCard({ point }: { point: AccountEquityPoint }) {
  return (
    <article className="order-card" data-testid="account-equity-point-row">
      <div className="order-card-head">
        <div>
          <strong>{point.point_ts}</strong>
          <span>Equity point</span>
        </div>
        <StateBadge value={point.ledger_ref && point.curve_ref ? "healthy" : "partial"} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Equity</dt>
          <dd>{formatMoney(point.equity)}</dd>
        </div>
        <div>
          <dt>Balance</dt>
          <dd>{formatMoney(point.balance)}</dd>
        </div>
        <div>
          <dt>Available cash</dt>
          <dd>{formatMoney(point.available_cash)}</dd>
        </div>
        <div>
          <dt>Margin</dt>
          <dd>{formatMoney(point.margin)}</dd>
        </div>
        <div>
          <dt>Ledger ref</dt>
          <dd>{point.ledger_ref ? <CopyableCode label="ledger ref" value={point.ledger_ref} /> : "missing"}</dd>
        </div>
        <div>
          <dt>Curve ref</dt>
          <dd>{point.curve_ref ? <CopyableCode label="curve ref" value={point.curve_ref} /> : "missing"}</dd>
        </div>
      </dl>
      <CopyableCode label="equity source ref" value={point.source_ref} />
    </article>
  );
}

function BlockerList({
  blockers,
  testId
}: {
  blockers: Array<{ blocker_id: string; severity: string; kind: string; owner: string; next_action: string; source_ref: string }>;
  testId: string;
}) {
  return (
    <div className="drawer-section">
      <h3>Blockers</h3>
      {blockers.length > 0 ? (
        <div className="blocker-list">
          {blockers.map((blocker) => (
            <article className="blocker-item" data-testid={testId} key={blocker.blocker_id}>
              <div className="blocker-head">
                <StateBadge value={blocker.severity} />
                <strong>{formatLabel(blocker.kind)}</strong>
              </div>
              <dl className="detail-list">
                <div>
                  <dt>Owner</dt>
                  <dd>{blocker.owner}</dd>
                </div>
                <div>
                  <dt>Next action</dt>
                  <dd>{blocker.next_action}</dd>
                </div>
                <div>
                  <dt>Source</dt>
                  <dd>
                    <CopyableCode label="blocker source ref" value={blocker.source_ref} />
                  </dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      ) : (
        <p className="muted">No blockers in this read-only fixture projection.</p>
      )}
    </div>
  );
}


function AccountHealthPanel({
  accountTypeFilter,
  closeoutFilter,
  fixture,
  fixtureState,
  onAccountTypeFilter,
  onCloseoutFilter,
  onFixtureState,
  onSelectAccount,
  onSettlementFilter,
  selectedAccount,
  selectedAccountId,
  settlementFilter,
  visibleRows
}: {
  accountTypeFilter: AccountKind | "all";
  closeoutFilter: AccountHealthCloseoutState | "all";
  fixture: AccountHealthPanelReadModel;
  fixtureState: AccountHealthFixtureId;
  onAccountTypeFilter: (value: AccountKind | "all") => void;
  onCloseoutFilter: (value: AccountHealthCloseoutState | "all") => void;
  onFixtureState: (value: AccountHealthFixtureId) => void;
  onSelectAccount: (value: string) => void;
  onSettlementFilter: (value: AccountHealthSettlementState | "all") => void;
  selectedAccount: AccountHealthRow | null;
  selectedAccountId: string | null;
  settlementFilter: AccountHealthSettlementState | "all";
  visibleRows: AccountHealthRow[];
}) {
  return (
    <section className="panel-grid" data-testid="daily-closeout-account-health-panel">
      <div className="panel-main">
        <div className="panel-header">
          <div>
            <h2>Account Health Panel</h2>
            <p>{fixture.panel} · {fixture.workbench}</p>
          </div>
          <span className={`state-badge ${stateTone(fixture.fixture_state)}`}>
            {fixtureLabels[fixtureState]}
          </span>
        </div>

        <div className="filter-toolbar" data-testid="daily-closeout-filter-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountHealthFixtureId)}
              value={fixtureState}
            >
              {Object.entries(fixtureLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <SelectFilter
            label="Account type"
            onChange={(value) => onAccountTypeFilter(value as AccountKind | "all")}
            options={fixture.filters.account_types}
            value={accountTypeFilter}
          />
          <SelectFilter
            label="Closeout"
            onChange={(value) => onCloseoutFilter(value as AccountHealthCloseoutState | "all")}
            options={fixture.filters.closeout_states}
            value={closeoutFilter}
          />
          <SelectFilter
            label="Settlement"
            onChange={(value) => onSettlementFilter(value as AccountHealthSettlementState | "all")}
            options={fixture.filters.settlement_states}
            value={settlementFilter}
          />
        </div>

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="daily-closeout-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
            </span>
          </div>
        ) : null}

        <div className="metric-strip" data-testid="daily-closeout-metric-strip">
          <Metric label="Total accounts" value={String(fixture.summary.total_accounts)} />
          <Metric label="Closeout completed" value={String(fixture.summary.closeout_completed)} />
          <Metric label="Closeout blocked" value={String(fixture.summary.closeout_blocked)} />
          <Metric label="Settlement blocked" value={String(fixture.summary.settlement_blocked)} />
          <Metric label="Stale or partial" value={String(fixture.summary.stale_or_partial)} />
          <Metric label="Open blockers" value={String(fixture.summary.open_blockers)} />
        </div>

        <div className="health-table-wrap">
          {visibleRows.length > 0 ? (
            <table className="health-table">
              <thead>
                <tr>
                  <th>Account</th>
                  <th>Type</th>
                  <th>Owner</th>
                  <th>Closeout</th>
                  <th>Settlement</th>
                  <th>Equity</th>
                  <th>Blockers</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {visibleRows.map((account) => (
                  <tr
                    className={account.account_id === selectedAccountId ? "selected" : undefined}
                    data-testid="daily-closeout-account-health-row"
                    key={account.account_id}
                    onClick={() => onSelectAccount(account.account_id)}
                  >
                    <td data-label="Account">
                      <button className="row-select" type="button">
                        {account.account_id}
                      </button>
                    </td>
                    <td data-label="Type">{formatLabel(account.account_type)}</td>
                    <td data-label="Owner">{account.owner}</td>
                    <td data-label="Closeout" data-testid="daily-closeout-closeout-state">
                      <StateBadge value={account.closeout_state} />
                    </td>
                    <td data-label="Settlement" data-testid="daily-closeout-settlement-state">
                      <StateBadge value={account.settlement_state} />
                    </td>
                    <td data-label="Equity" data-testid="daily-closeout-equity-continuity">
                      <StateBadge value={account.equity_continuity} />
                    </td>
                    <td data-label="Blockers" data-testid="daily-closeout-blocker">{account.blocker_count}</td>
                    <td data-label="Source" data-testid="daily-closeout-evidence-ref">
                      <code>{account.source_ref}</code>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty" data-testid="daily-closeout-empty-state">
              No account health rows for this fixture and filter set. Source: {fixture.context.source_ref}
            </div>
          )}
        </div>
      </div>

      <aside className="detail-drawer" data-testid="daily-closeout-detail-drawer">
        {selectedAccount ? (
          <AccountDetail account={selectedAccount} />
        ) : (
          <div className="empty" data-testid="daily-closeout-empty-state">
            No selected account. Source: {fixture.context.source_ref}
          </div>
        )}
      </aside>
    </section>
  );
}

function AccountDetail({ account }: { account: AccountHealthRow }) {
  return (
    <>
      <div className="drawer-section">
        <h3>{account.account_id}</h3>
        <dl className="detail-list">
          <div>
            <dt>Owner</dt>
            <dd>{account.owner}</dd>
          </div>
          <div>
            <dt>Last cursor</dt>
            <dd>{account.last_cursor}</dd>
          </div>
          <div>
            <dt>Checkpoint</dt>
            <dd>{account.last_checkpoint_ts}</dd>
          </div>
          <div>
            <dt>Checksum</dt>
            <dd>
              <CopyableCode label="checksum" value={account.checksum} />
            </dd>
          </div>
        </dl>
      </div>

      <div className="drawer-section">
        <h3>Blockers</h3>
        {account.blockers.length > 0 ? (
          <div className="blocker-list">
            {account.blockers.map((blocker) => (
              <article className="blocker-item" data-testid="daily-closeout-blocker" key={blocker.blocker_id}>
                <div className="blocker-head">
                  <StateBadge value={blocker.severity} />
                  <strong>{blocker.kind}</strong>
                </div>
                <dl className="detail-list">
                  <div>
                    <dt>Owner</dt>
                    <dd>{blocker.owner}</dd>
                  </div>
                  <div>
                    <dt>Next diagnostic</dt>
                    <dd>
                      <CopyableCode label="next diagnostic ref" value={blocker.next_diagnostic_ref} />
                    </dd>
                  </div>
                  <div>
                    <dt>Source</dt>
                    <dd>
                      <CopyableCode label="blocker source ref" value={blocker.source_ref} />
                    </dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">No blockers in the selected projection.</p>
        )}
      </div>

      <div className="drawer-section" data-testid="daily-closeout-evidence-drawer">
        <h3>Evidence</h3>
        <dl className="detail-list">
          <div>
            <dt>Closeout run</dt>
            <dd>
              <CopyableCode label="closeout run" value={account.closeout_run_id} />
            </dd>
          </div>
          <div>
            <dt>Settlement run</dt>
            <dd>
              <CopyableCode label="settlement run" value={account.settlement_run_id} />
            </dd>
          </div>
          <div>
            <dt>Equity artifact</dt>
            <dd>
              <CopyableCode label="equity artifact" value={account.equity_curve_artifact_id} />
            </dd>
          </div>
          <div>
            <dt>Source ref</dt>
            <dd data-testid="daily-closeout-evidence-ref">
              <CopyableCode label="source ref" value={account.source_ref} />
            </dd>
          </div>
        </dl>
      </div>
    </>
  );
}

function SelectFilter({
  label,
  onChange,
  options,
  value
}: {
  label: string;
  onChange: (value: string) => void;
  options: string[];
  value: string;
}) {
  return (
    <label>
      {label}
      <select onChange={(event) => onChange(event.target.value)} value={value}>
        <option value="all">all</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {formatLabel(option)}
          </option>
        ))}
      </select>
    </label>
  );
}

function CommandStatusPanel({
  status
}: {
  status: MirrorAccountProjection["command_status"] | null;
}) {
  const riskRefs = commandStatusRefs(status?.risk_decision_refs);
  const approvalRefs = commandStatusRefs(status?.approval_decision_refs);
  const gatewayRefs = commandStatusRefs(status?.gateway_event_refs);
  const readbackRefs = commandStatusRefs(status?.readback_refs);
  const blockers = Array.isArray(status?.blockers) ? status.blockers : [];
  const reconciliationRef = asText(status?.reconciliation_ref, "");
  const commandAuditRef = asText(status?.command_audit_ref, "");
  const hasReadback = readbackRefs.length > 0;
  const hasReconciliation = reconciliationRef.length > 0;
  const hasGatewayFinalClaim = status?.gateway_ack_is_final_state === true;
  const derivedBlockers = [
    ...blockers.map(commandStatusBlockerText),
    ...(status && !hasReadback ? ["missing readback refs"] : []),
    ...(status && !hasReconciliation ? ["missing reconciliation ref"] : []),
    ...(hasGatewayFinalClaim ? ["gateway ack is not final account state"] : [])
  ];
  const displayState = !status
    ? "empty"
    : derivedBlockers.length > 0
      ? "blocked"
      : asText(status.status, "unknown");

  return (
    <section className="terminal-panel" data-testid="account-command-status-panel">
      <div className="terminal-panel-header">
        <h3>Command Status</h3>
        <StateBadge value={displayState} />
      </div>
      {status ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item" data-testid="account-command-audit-ref">
            <strong>Audit</strong>
            {commandAuditRef ? (
              <CopyableCode label="command audit ref" value={commandAuditRef} />
            ) : (
              <span>missing audit ref</span>
            )}
          </div>
          {riskRefs.map((ref) => (
            <div className="evidence-item" data-testid="account-command-risk-ref" key={ref}>
              <strong>Risk</strong>
              <CopyableCode label="command risk ref" value={ref} />
            </div>
          ))}
          {approvalRefs.map((ref) => (
            <div className="evidence-item" data-testid="account-command-approval-ref" key={ref}>
              <strong>Approval</strong>
              <CopyableCode label="command approval ref" value={ref} />
            </div>
          ))}
          {gatewayRefs.map((ref) => (
            <div className="evidence-item" data-testid="account-command-gateway-ref" key={ref}>
              <strong>Gateway</strong>
              <CopyableCode label="command gateway ref" value={ref} />
            </div>
          ))}
          {readbackRefs.map((ref) => (
            <div className="evidence-item" data-testid="account-command-readback-ref" key={ref}>
              <strong>Readback</strong>
              <CopyableCode label="command readback ref" value={ref} />
            </div>
          ))}
          {hasReconciliation ? (
            <div className="evidence-item" data-testid="account-command-reconciliation-ref">
              <strong>Reconcile</strong>
              <CopyableCode label="command reconciliation ref" value={reconciliationRef} />
            </div>
          ) : null}
          <div className="evidence-item">
            <strong>Gateway final</strong>
            <span data-testid="account-command-gateway-final-state">
              {status.gateway_ack_is_final_state === true ? "invalid" : "false"}
            </span>
          </div>
        </div>
      ) : (
        <p className="muted">No command audit evidence in this read-only projection.</p>
      )}
      {derivedBlockers.length > 0 ? (
        <div className="blocker-list">
          {derivedBlockers.map((blocker) => (
            <article className="blocker-item" data-testid="account-command-blocker" key={blocker}>
              {blocker}
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}

function StateBadge({ value }: { value: string }) {
  return <span className={`state-badge ${stateTone(value)}`}>{formatLabel(value)}</span>;
}

function Ref({ label, value }: { label: string; value: string }) {
  return (
    <div className="ref-item">
      <span>{label}</span>
      <CopyableCode label={label} value={value} />
    </div>
  );
}

function CopyableCode({ label, value }: { label: string; value: string }) {
  function copyValue() {
    if (navigator.clipboard) {
      void navigator.clipboard.writeText(value);
    }
  }

  return (
    <span className="copyable-code">
      <code>{value}</code>
      <button aria-label={`Copy ${label}`} onClick={copyValue} title={`Copy ${label}`} type="button">
        <Clipboard size={13} />
      </button>
    </span>
  );
}

function Metric({ label, testId, value }: { label: string; testId?: string; value: string }) {
  return (
    <div className="metric" data-testid={testId}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
