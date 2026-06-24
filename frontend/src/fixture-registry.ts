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
  AccountEvidenceFixtureState,
  AccountEvidencePanelReadModel,
  AccountHealthPanelFixtureState,
  AccountHealthPanelReadModel,
  AccountIncidentsFixtureState,
  AccountIncidentsPanelReadModel,
  AccountOrderDetailFixtureState,
  AccountOrderDetailPanelReadModel,
  AccountOrdersFixtureState,
  AccountOrdersPanelReadModel,
  AccountPositionsFixtureState,
  AccountPositionsPanelReadModel,
  AccountReconcileFixtureState,
  AccountReconcilePanelReadModel,
  AccountSettlementFixtureState,
  AccountSettlementPanelReadModel,
  AccountSummaryFixtureState,
  AccountSummaryPanelReadModel,
  IntradayMonitorFixtureState,
  IntradayMonitorPanelReadModel,
} from "./types";

export type AccountHealthFixtureId = AccountHealthPanelFixtureState | "adr0044_foundation";

export const healthFixtureMap: Record<AccountHealthFixtureId, AccountHealthPanelReadModel> = {
  happy_path: happyFixture as AccountHealthPanelReadModel,
  adr0044_foundation: adr0044Fixture as AccountHealthPanelReadModel,
  empty: emptyFixture as AccountHealthPanelReadModel,
  blocked: blockedFixture as AccountHealthPanelReadModel,
  stale: staleFixture as AccountHealthPanelReadModel,
  partial: partialFixture as AccountHealthPanelReadModel,
};

export const healthFixtureLabels: Record<AccountHealthFixtureId, string> = {
  happy_path: "happy path",
  adr0044_foundation: "ADR-0044 source-backed",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
};

export const accountSummaryFixtureMap: Record<AccountSummaryFixtureState, AccountSummaryPanelReadModel> = {
  happy_path: accountSummaryHappyFixture as AccountSummaryPanelReadModel,
  empty: accountSummaryEmptyFixture as AccountSummaryPanelReadModel,
  blocked: accountSummaryBlockedFixture as AccountSummaryPanelReadModel,
  stale: accountSummaryStaleFixture as AccountSummaryPanelReadModel,
  partial: accountSummaryPartialFixture as AccountSummaryPanelReadModel,
  r1_cta_core_001: accountSummaryR1CtaCoreFixture as AccountSummaryPanelReadModel,
};

export const accountSummaryFixtureLabels: Record<AccountSummaryFixtureState, string> = {
  happy_path: "happy path",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001",
};

export const accountOrdersFixtureMap: Record<AccountOrdersFixtureState, AccountOrdersPanelReadModel> = {
  current_orders: accountOrdersCurrentFixture as AccountOrdersPanelReadModel,
  empty: accountOrdersEmptyFixture as AccountOrdersPanelReadModel,
  blocked: accountOrdersBlockedFixture as AccountOrdersPanelReadModel,
  stale: accountOrdersStaleFixture as AccountOrdersPanelReadModel,
};

export const accountOrdersFixtureLabels: Record<AccountOrdersFixtureState, string> = {
  current_orders: "current orders",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
};

export const accountOrderDetailFixtureMap: Record<AccountOrderDetailFixtureState, AccountOrderDetailPanelReadModel> = {
  filled_lifecycle: accountOrderDetailFilledFixture as AccountOrderDetailPanelReadModel,
  blocked: accountOrderDetailBlockedFixture as AccountOrderDetailPanelReadModel,
  stale: accountOrderDetailBlockedFixture as AccountOrderDetailPanelReadModel,
};

export const accountOrderDetailFixtureLabels: Record<AccountOrderDetailFixtureState, string> = {
  filled_lifecycle: "filled lifecycle",
  blocked: "blocked",
  stale: "stale",
};

export const accountPositionsFixtureMap: Record<AccountPositionsFixtureState, AccountPositionsPanelReadModel> = {
  current_positions: accountPositionsCurrentFixture as AccountPositionsPanelReadModel,
  empty: accountPositionsEmptyFixture as AccountPositionsPanelReadModel,
  blocked: accountPositionsBlockedFixture as AccountPositionsPanelReadModel,
  stale: accountPositionsStaleFixture as AccountPositionsPanelReadModel,
  partial: accountPositionsPartialFixture as AccountPositionsPanelReadModel,
  r1_cta_core_001: accountPositionsR1CtaCoreFixture as AccountPositionsPanelReadModel,
};

export const accountPositionsFixtureLabels: Record<AccountPositionsFixtureState, string> = {
  current_positions: "current positions",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001",
};

export const accountSettlementFixtureMap: Record<AccountSettlementFixtureState, AccountSettlementPanelReadModel> = {
  current_settlement: accountSettlementCurrentFixture as AccountSettlementPanelReadModel,
  empty: accountSettlementEmptyFixture as AccountSettlementPanelReadModel,
  blocked: accountSettlementBlockedFixture as AccountSettlementPanelReadModel,
  stale: accountSettlementStaleFixture as AccountSettlementPanelReadModel,
  partial: accountSettlementPartialFixture as AccountSettlementPanelReadModel,
};

export const accountSettlementFixtureLabels: Record<AccountSettlementFixtureState, string> = {
  current_settlement: "current settlement",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
};

export const accountEquityFixtureMap: Record<AccountEquityFixtureState, AccountEquityPanelReadModel> = {
  current_equity: accountEquityCurrentFixture as AccountEquityPanelReadModel,
  empty: accountEquityEmptyFixture as AccountEquityPanelReadModel,
  blocked: accountEquityBlockedFixture as AccountEquityPanelReadModel,
  stale: accountEquityStaleFixture as AccountEquityPanelReadModel,
  partial: accountEquityPartialFixture as AccountEquityPanelReadModel,
};

export const accountEquityFixtureLabels: Record<AccountEquityFixtureState, string> = {
  current_equity: "current equity",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
};

export const accountReconcileFixtureMap: Record<AccountReconcileFixtureState, AccountReconcilePanelReadModel> = {
  matched: accountReconcileMatchedFixture as AccountReconcilePanelReadModel,
  empty: accountReconcileEmptyFixture as AccountReconcilePanelReadModel,
  mismatch: accountReconcileMismatchFixture as AccountReconcilePanelReadModel,
  stale: accountReconcileStaleFixture as AccountReconcilePanelReadModel,
  partial: accountReconcilePartialFixture as AccountReconcilePanelReadModel,
  r1_cta_core_001: accountReconcileR1CtaCoreFixture as AccountReconcilePanelReadModel,
};

export const accountReconcileFixtureLabels: Record<AccountReconcileFixtureState, string> = {
  matched: "matched",
  empty: "empty",
  mismatch: "mismatch",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001",
};

export const accountIncidentsFixtureMap: Record<AccountIncidentsFixtureState, AccountIncidentsPanelReadModel> = {
  active_incidents: accountIncidentsActiveFixture as AccountIncidentsPanelReadModel,
  empty: accountIncidentsEmptyFixture as AccountIncidentsPanelReadModel,
  blocked: accountIncidentsBlockedFixture as AccountIncidentsPanelReadModel,
  stale: accountIncidentsStaleFixture as AccountIncidentsPanelReadModel,
  partial: accountIncidentsPartialFixture as AccountIncidentsPanelReadModel,
};

export const accountIncidentsFixtureLabels: Record<AccountIncidentsFixtureState, string> = {
  active_incidents: "active incidents",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
};

export const accountEvidenceFixtureMap: Record<AccountEvidenceFixtureState, AccountEvidencePanelReadModel> = {
  current_evidence: accountEvidenceCurrentFixture as AccountEvidencePanelReadModel,
  empty: accountEvidenceEmptyFixture as AccountEvidencePanelReadModel,
  blocked: accountEvidenceBlockedFixture as AccountEvidencePanelReadModel,
  stale: accountEvidenceStaleFixture as AccountEvidencePanelReadModel,
  partial: accountEvidencePartialFixture as AccountEvidencePanelReadModel,
  r1_cta_core_001: accountEvidenceR1CtaCoreFixture as AccountEvidencePanelReadModel,
};

export const accountEvidenceFixtureLabels: Record<AccountEvidenceFixtureState, string> = {
  current_evidence: "current evidence",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
  r1_cta_core_001: "R1 CTA-CORE-001",
};

export const intradayMonitorFixtureMap: Record<IntradayMonitorFixtureState, IntradayMonitorPanelReadModel> = {
  current: intradayMonitorCurrentFixture as IntradayMonitorPanelReadModel,
  empty: intradayMonitorEmptyFixture as IntradayMonitorPanelReadModel,
  blocked: intradayMonitorBlockedFixture as IntradayMonitorPanelReadModel,
  stale: intradayMonitorStaleFixture as IntradayMonitorPanelReadModel,
  partial: intradayMonitorPartialFixture as IntradayMonitorPanelReadModel,
};

export const intradayMonitorFixtureLabels: Record<IntradayMonitorFixtureState, string> = {
  current: "current",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial",
};
