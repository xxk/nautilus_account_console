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
import accountEvidenceStaleFixture from "../../contracts/ui/fixtures/account_workbench/account_evidence_stale_stream.json";
import accountReconcileEmptyFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_empty.json";
import accountReconcileMatchedFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_matched.json";
import accountReconcileMismatchFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_mismatch.json";
import accountReconcilePartialFixture from "../../contracts/ui/fixtures/account_workbench/account_reconcile_partial_missing_tolerance.json";
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
  AccountOrdersFixtureState,
  AccountOrdersPanelReadModel,
  AccountOrderRow,
  AccountPositionRow,
  AccountPositionsFixtureState,
  AccountPositionsPanelReadModel,
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
  IntradayMonitorStreamStateRow
} from "./types";

type AccountHealthFixtureId = AccountHealthPanelFixtureState | "adr0044_foundation";

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
  partial: accountSummaryPartialFixture as AccountSummaryPanelReadModel
};

const accountSummaryFixtureLabels: Record<AccountSummaryFixtureState, string> = {
  happy_path: "happy path",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
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
  partial: accountPositionsPartialFixture as AccountPositionsPanelReadModel
};

const accountPositionsFixtureLabels: Record<AccountPositionsFixtureState, string> = {
  current_positions: "current positions",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
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
  partial: accountReconcilePartialFixture as AccountReconcilePanelReadModel
};

const accountReconcileFixtureLabels: Record<AccountReconcileFixtureState, string> = {
  matched: "matched",
  empty: "empty",
  mismatch: "mismatch",
  stale: "stale",
  partial: "partial"
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
  partial: accountEvidencePartialFixture as AccountEvidencePanelReadModel
};

const accountEvidenceFixtureLabels: Record<AccountEvidenceFixtureState, string> = {
  current_evidence: "current evidence",
  empty: "empty",
  blocked: "blocked",
  stale: "stale",
  partial: "partial"
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
                  {accountSummaryFixture.context.trading_day} ·{" "}
                  {accountSummaryFixture.account.account_id} · {accountSummaryFixture.context.run_id}
                </p>
              </div>
              <div
                className={`stream-pill ${stateTone(accountSummaryFixture.context.stream_state)}`}
                data-testid="account-workbench-stream-state"
              >
                <Landmark size={16} />
                {accountSummaryFixture.context.stream_state}
              </div>
            </header>

            <section className="checkpoint-strip" aria-label="Account source checkpoint">
              <Ref label="Reducer checkpoint" value={accountSummaryFixture.context.reducer_checkpoint_id} />
              <Ref label="Checkpoint time" value={accountSummaryFixture.context.reducer_checkpoint_ts} />
              <Ref label="Projection" value={accountSummaryFixture.context.projection_owner} />
              <Ref label="Authority" value={accountSummaryFixture.context.source_authority} />
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
              <AccountSummaryPanel
                fixture={accountSummaryFixture}
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
                  <article className="position-item" key={position.checksum}>
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
            {fixture.source_refs.map((source) => (
              <article className="evidence-item" data-testid="account-summary-source-ref" key={source.checksum}>
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
                <OrderRowCard order={order} key={order.checksum} />
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
                <PositionRowCard position={position} key={position.checksum} />
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
                <ReconcileItemCard item={item} key={item.checksum} />
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
          <strong>{order.client_order_id}</strong>
          <span>
            {order.instrument} · {order.side} · {order.offset}
          </span>
        </div>
        <StateBadge value={order.status} />
      </div>
      <dl className="detail-list two-column">
        <div>
          <dt>Type</dt>
          <dd>{order.order_type}</dd>
        </div>
        <div>
          <dt>Limit</dt>
          <dd>{order.limit_price ?? "missing"}</dd>
        </div>
        <div>
          <dt>Quantity</dt>
          <dd>{order.quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>Filled</dt>
          <dd>{order.filled_quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>Remaining</dt>
          <dd>{order.remaining_quantity ?? "missing"}</dd>
        </div>
        <div>
          <dt>Lifecycle ref</dt>
          <dd>{order.lifecycle_ref ? <CopyableCode label="lifecycle ref" value={order.lifecycle_ref} /> : "missing"}</dd>
        </div>
      </dl>
      <CopyableCode label="order source ref" value={order.source_ref} />
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

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
