import {
  Clipboard,
  Database,
  FileSearch,
  Gauge,
  Landmark,
  Layers,
  Radio,
  ShieldAlert,
  Waypoints
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type {
  AccountEquityPanelReadModel,
  AccountHealthCloseoutState,
  AccountHealthSettlementState,
  AccountKind,
  AccountOrderDetailPanelReadModel,
  AccountSettlementPanelReadModel,
  IntradayMonitorExceptionRow,
  IntradayMonitorIncidentRow,
  IntradayMonitorPanelReadModel,
  IntradayMonitorStreamStateRow,
  MirrorAccountSummary
} from "./types";
import {
  portfolioOwnerConsoleUrl,
  workbenches,
} from "./app-shell-registry";
import {
  fetchMirrorAccount,
  fetchMirrorAccounts,
  fetchMirrorEvidence,
  fetchMirrorSourceHealth
} from "./api";
import { useCommandPlaneGovernance } from "./command-plane";
import {
  AccountEvidencePanel,
  AccountEquityPanel,
  AccountIncidentsPanel,
  AccountOrderDetailPanel,
  AccountOrdersPanel,
  AccountPositionsPanel,
  AccountReconcilePanel,
  AccountSettlementPanel,
  AccountSummaryPanel,
} from "./account-workbench-panels";
import { AccountWorkbenchTerminalPanel } from "./account-workbench-terminal";
import {
  asText,
  mirrorWorkbenchProjection,
  mirrorOrdersReadModel,
  mirrorPositionsReadModel,
  mirrorSummaryReadModel,
  type MirrorWorkbenchReadback
} from "./account-workbench-adapters";
import { AccountHealthPanel } from "./account-health-panels";
import { IntradayMonitorPanel } from "./intraday-monitor-panels";
import { classifyAppRoute, isMirrorWorkbenchEligibleRoute } from "./account-workbench-routing";
import { useFixtureSelection } from "./fixture-selection";
import { resolveMirrorRouteAccountId } from "./mirror-route-owner";
import { Ref } from "./panel-shared";
import { StateBadge, stateTone } from "./ui-primitives";

const workbenchIcons = {
  Gauge,
  Radio,
  Database,
  Layers,
  ShieldAlert,
  FileSearch,
  Waypoints,
} as const;

export function App() {
  const currentPath = window.location.pathname;
  const routeState = classifyAppRoute(currentPath);
  const { isIntradayMonitorRoute, isAccountWorkbenchRoute, routeAccountId } = routeState;
  const fixtures = useFixtureSelection();
  const workbenchFallback = fixtures.accountWorkbench;
  const [accountTypeFilter, setAccountTypeFilter] = useState<AccountKind | "all">("all");
  const [closeoutFilter, setCloseoutFilter] = useState<AccountHealthCloseoutState | "all">("all");
  const [settlementFilter, setSettlementFilter] = useState<AccountHealthSettlementState | "all">("all");
  const fixture = fixtures.health.fixture;
  const accountSummaryFixture = workbenchFallback.summary.fixture;
  const accountOrdersFixture = workbenchFallback.orders.fixture;
  const accountOrderDetailFixture = workbenchFallback.orderDetail.fixture;
  const accountPositionsFixture = workbenchFallback.positions.fixture;
  const accountSettlementFixture = workbenchFallback.settlement.fixture;
  const accountEquityFixture = workbenchFallback.equity.fixture;
  const accountReconcileFixture = workbenchFallback.reconcile.fixture;
  const accountIncidentsFixture = workbenchFallback.incidents.fixture;
  const accountEvidenceFixture = workbenchFallback.evidence.fixture;
  const intradayMonitorFixture = fixtures.intradayMonitor.fixture;
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
  const mirrorProjection = useMemo(
    () => (mirrorReadback ? mirrorWorkbenchProjection(mirrorReadback, routeState.routeOrderId) : null),
    [mirrorReadback, routeState.routeOrderId]
  );
  const showWorkbenchFixtureSelectors = !mirrorProjection;
  const terminalSummary = mirrorProjection?.summary ?? accountSummaryFixture;
  const terminalPositions = mirrorProjection?.positions ?? accountPositionsFixture;
  const terminalOrders = mirrorProjection?.orders ?? accountOrdersFixture;
  const summary = terminalSummary;
  const commandStatus = mirrorReadback?.selected.command_status ?? null;
  const commandPlaneGovernance = useCommandPlaneGovernance(summary.account.account_id);
  const isMirrorEligibleRoute = isMirrorWorkbenchEligibleRoute(routeState);

  useEffect(() => {
    if (!isMirrorEligibleRoute) {
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
  }, [isMirrorEligibleRoute, routeAccountId]);

  return (
    <main className="shell" data-testid="account-console">
      <aside className="primary-nav" aria-label="Primary workbenches">
        <div className="brand-lockup">
          <strong>Nautilus</strong>
          <span>Account Console</span>
        </div>
        <nav>
          {workbenches.map((item) => {
            const Icon = workbenchIcons[item.icon];
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
              fixtureState={fixtures.intradayMonitor.fixtureState}
              onFixtureState={fixtures.intradayMonitor.setFixtureState}
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

            {routeState.accountWorkbenchView === "order_detail" ? (
              <AccountOrderDetailPanel
                fixture={mirrorProjection?.orderDetail ?? accountOrderDetailFixture}
                fixtureState={workbenchFallback.orderDetail.fixtureState}
                onFixtureState={workbenchFallback.orderDetail.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "orders" ? (
              <AccountOrdersPanel
                fixture={mirrorProjection?.orders ?? accountOrdersFixture}
                fixtureState={workbenchFallback.orders.fixtureState}
                onFixtureState={workbenchFallback.orders.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "positions" ? (
              <AccountPositionsPanel
                fixture={mirrorProjection?.positions ?? accountPositionsFixture}
                fixtureState={workbenchFallback.positions.fixtureState}
                onFixtureState={workbenchFallback.positions.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "settlement" ? (
              <AccountSettlementPanel
                fixture={mirrorProjection?.settlement ?? accountSettlementFixture}
                fixtureState={workbenchFallback.settlement.fixtureState}
                onFixtureState={workbenchFallback.settlement.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "equity" ? (
              <AccountEquityPanel
                fixture={mirrorProjection?.equity ?? accountEquityFixture}
                fixtureState={workbenchFallback.equity.fixtureState}
                onFixtureState={workbenchFallback.equity.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "reconcile" ? (
              <AccountReconcilePanel
                fixture={mirrorProjection?.reconcile ?? accountReconcileFixture}
                fixtureState={workbenchFallback.reconcile.fixtureState}
                onFixtureState={workbenchFallback.reconcile.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "incidents" ? (
              <AccountIncidentsPanel
                fixture={mirrorProjection?.incidents ?? accountIncidentsFixture}
                fixtureState={workbenchFallback.incidents.fixtureState}
                onFixtureState={workbenchFallback.incidents.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
              />
            ) : routeState.accountWorkbenchView === "evidence" ? (
              <AccountEvidencePanel
                fixture={mirrorProjection?.evidence ?? accountEvidenceFixture}
                fixtureState={workbenchFallback.evidence.fixtureState}
                onFixtureState={workbenchFallback.evidence.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
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
                fixtureState={workbenchFallback.summary.fixtureState}
                onFixtureState={workbenchFallback.summary.setFixtureState}
                showFixtureSelector={showWorkbenchFixtureSelectors}
                governance={commandPlaneGovernance}
                commandStatus={commandStatus}
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
              fixtureState={fixtures.health.fixtureState}
              onAccountTypeFilter={setAccountTypeFilter}
              onCloseoutFilter={setCloseoutFilter}
              onFixtureState={fixtures.health.setFixtureState}
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


