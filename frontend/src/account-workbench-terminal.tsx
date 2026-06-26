import { AlertTriangle, CircleX, Landmark, ListFilter, Send } from "lucide-react";
import { useState } from "react";

import {
  cancelPaperOrderIntent,
  prepareCancelRuntimeRunRequest,
  prepareSubmitRuntimeRunRequest,
  submitPaperOrderIntent
} from "./api";
import {
  accountKindFromDomain,
  asText,
  cancelIntentForOrder,
  defaultSubmitIntent,
  isP024PaperArmed,
  mirrorExecutionReportRows,
  type MirrorWorkbenchReadback
} from "./account-workbench-adapters";
import { accountSummaryFixtureLabels, accountSummaryFixtureMap } from "./app-registry";
import {
  CommandPlaneOwnerPanel,
  CommandRuntimeCloseoutPanel,
  CommandRuntimeExecutionApprovalPacketPanel,
  CommandRuntimeExecutionGapAuditPanel,
  CommandRuntimeExecutionHandoffBundlePanel,
  CommandRuntimeInvocationReadinessPanel
} from "./command-plane-panels";
import {
  CommandIntentReceiptPanel,
  CommandRuntimeRunRequestPanel,
  CommandStatusPanel
} from "./command-surface-panels";
import { Metric } from "./panel-shared";
import { CopyableCode, StateBadge, formatLabel, stateTone } from "./ui-primitives";
import type { CommandPlaneGovernanceState } from "./command-plane";
import type {
  AccountOrdersPanelReadModel,
  AccountOrderRow,
  AccountPositionsPanelReadModel,
  AccountSummaryBlocker,
  AccountSummaryFixtureState,
  AccountSummaryPanelReadModel,
  MirrorCommandStatusProjection,
  CommandApiResult,
  CommandRuntimeRunRequest
} from "./types";

function formatMoney(value: number | null, currency = "CNY"): string {
  if (value === null) {
    return "missing";
  }
  return `${currency} ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

function numberTone(value: number | null): string {
  if (value === null || value === 0) {
    return "neutral";
  }
  return value > 0 ? "positive" : "negative";
}

interface AccountWorkbenchTerminalPanelProps {
  mirrorAccounts: MirrorWorkbenchReadback["accounts"] | null;
  mirrorReadback: MirrorWorkbenchReadback | null;
  mirrorReadbackError: string | null;
  sourceHealthDetails: Record<string, unknown> | null;
  summary: AccountSummaryPanelReadModel;
  positions: AccountPositionsPanelReadModel;
  orders: AccountOrdersPanelReadModel;
  fixtureState: AccountSummaryFixtureState;
  onFixtureState: (value: AccountSummaryFixtureState) => void;
  showFixtureSelector?: boolean;
  governance: CommandPlaneGovernanceState;
  commandStatus: MirrorCommandStatusProjection | null;
}

export function AccountWorkbenchTerminalPanel({
  mirrorAccounts,
  mirrorReadback,
  mirrorReadbackError,
  sourceHealthDetails,
  summary,
  positions,
  orders,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
  governance,
  commandStatus
}: AccountWorkbenchTerminalPanelProps) {
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
  const [commandResult, setCommandResult] = useState<CommandApiResult | null>(null);
  const [commandError, setCommandError] = useState<string | null>(null);
  const [runtimeRunRequest, setRuntimeRunRequest] = useState<CommandRuntimeRunRequest | null>(null);
  const [runtimeRunRequestError, setRuntimeRunRequestError] = useState<string | null>(null);
  const paperArmed = isP024PaperArmed(mirrorReadback);
  const submitIntent = mirrorReadback && paperArmed ? defaultSubmitIntent(mirrorReadback) : null;
  const cancelEligibleOrder = paperArmed
    ? visibleOrders.find((order) => {
        const remaining = order.remaining_quantity ?? 0;
        return remaining > 0 && Boolean(order.lifecycle_ref) && order.status !== "cancel_pending";
      })
    : null;
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

  async function handleSubmitIntent() {
    if (!mirrorReadback || !submitIntent) {
      return;
    }
    try {
      setCommandError(null);
      setRuntimeRunRequestError(null);
      const result = await submitPaperOrderIntent(mirrorReadback.selected.account_id, submitIntent);
      setCommandResult(result);
      const handoff = await prepareSubmitRuntimeRunRequest(mirrorReadback.selected.account_id, submitIntent);
      setRuntimeRunRequest(handoff);
    } catch (error) {
      setCommandError(error instanceof Error ? error.message : "submit intent request failed");
      setRuntimeRunRequestError(error instanceof Error ? error.message : "submit runtime handoff unavailable");
    }
  }

  async function handleCancelIntent(order: AccountOrderRow) {
    if (!mirrorReadback) {
      return;
    }
    try {
      setCommandError(null);
      setRuntimeRunRequestError(null);
      const cancelIntent = cancelIntentForOrder(mirrorReadback, order);
      const result = await cancelPaperOrderIntent(mirrorReadback.selected.account_id, cancelIntent);
      setCommandResult(result);
      const handoff = await prepareCancelRuntimeRunRequest(mirrorReadback.selected.account_id, cancelIntent);
      setRuntimeRunRequest(handoff);
    } catch (error) {
      setCommandError(error instanceof Error ? error.message : "cancel intent request failed");
      setRuntimeRunRequestError(error instanceof Error ? error.message : "cancel runtime handoff unavailable");
    }
  }

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

          <CommandPlaneOwnerPanel
            commandPlaneProjection={governance.commandPlaneProjection}
            commandPlaneProjectionError={governance.commandPlaneProjectionError}
            projectionSummary={governance.projectionSummary}
          />
        </aside>

        <main className="terminal-center">
          {showFixtureSelector ? (
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
          ) : null}

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
              <Metric label="Cash" testId="account-summary-cash" value={formatMoney(summary.balances.cash, baseCurrency)} />
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
                          <td className="numeric-cell" data-label="Cash">{formatMoney(balance.cash, balance.currency)}</td>
                          <td className="numeric-cell" data-label="Available">
                            {formatMoney(balance.available_cash, balance.currency)}
                          </td>
                          <td className="numeric-cell" data-label="Buying power">
                            {formatMoney(balance.buying_power, balance.currency)}
                          </td>
                          <td className="numeric-cell" data-label="Margin">{formatMoney(balance.margin_used, balance.currency)}</td>
                          <td className="numeric-cell" data-label="Equity/net liq">{formatMoney(balance.equity, balance.currency)}</td>
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
                        <td className="numeric-cell" data-label="Cash">{formatMoney(summary.balances.cash, baseCurrency)}</td>
                        <td className="numeric-cell" data-label="Available">
                          {formatMoney(summary.balances.available_cash, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Buying power">
                          {formatMoney(summary.balances.buying_power, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Margin">
                          {formatMoney(summary.margin.initial_margin, baseCurrency)}
                        </td>
                        <td className="numeric-cell" data-label="Equity/net liq">{formatMoney(summary.balances.cash, baseCurrency)}</td>
                        <td className={`numeric-cell ${numberTone(summary.pnl.unrealized)}`} data-label="Unrealized PnL">
                          {formatMoney(summary.pnl.unrealized, baseCurrency)}
                        </td>
                        <td data-label="FX/provenance" data-testid="tws-fx-provenance">source currency</td>
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
                        <td data-label="Direction"><StateBadge value={position.direction} /></td>
                        <td className="numeric-cell" data-label="Net">{position.net_qty ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Today">{position.today_qty ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Available">{position.available_qty ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Avg">{position.average_price ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Last">{position.market_price ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Value">{formatMoney(position.market_value, baseCurrency)}</td>
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
                        <td data-label="Side" data-testid="tws-open-order-side"><StateBadge value={order.side} /></td>
                        <td data-label="Status" data-testid="tws-open-order-status">
                          <span data-testid="account-order-status"><StateBadge value={order.status} /></span>
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
                          <td data-label="Client order" data-testid="tws-fill-client-order-id">{report.client_order_id}</td>
                          <td data-label="Venue order" data-testid="tws-fill-venue-order-id">{report.venue_order_id ?? "missing"}</td>
                          <td data-label="Instrument" data-testid="tws-fill-instrument">{report.instrument}</td>
                          <td data-label="Side" data-testid="tws-fill-side"><StateBadge value={report.side} /></td>
                          <td data-label="Trade/status" data-testid="tws-fill-status-or-trade">{report.status_or_trade}</td>
                          <td className="numeric-cell" data-label="Filled" data-testid="tws-fill-filled-quantity">
                            <span data-testid="account-fill-quantity">{report.filled_quantity ?? "missing"}</span>
                          </td>
                          <td className="numeric-cell" data-label="Last price" data-testid="tws-fill-last-price">
                            <span data-testid="account-fill-price">{report.limit_or_last_price ?? "missing"}</span>
                          </td>
                          <td data-label="Sequence" data-testid="tws-fill-sequence">{report.sequence ?? "missing"}</td>
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
                    executionReportRows.map((report) => (
                      <tr data-testid="tws-execution-report-row" key={`${report.report_id}-${report.source_ref}`}>
                        <td data-label="Report type" data-testid="tws-execution-report-type">{report.report_type}</td>
                        <td data-label="Client order" data-testid="tws-execution-report-client-order-id">{report.client_order_id}</td>
                        <td data-label="Venue order" data-testid="tws-execution-report-venue-order-id">{report.venue_order_id ?? "missing"}</td>
                        <td data-label="Instrument">{report.instrument}</td>
                        <td data-label="Side"><StateBadge value={report.side} /></td>
                        <td data-label="Status/trade">{report.status_or_trade}</td>
                        <td className="numeric-cell" data-label="Quantity">{report.quantity ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Filled">{report.filled_quantity ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Remaining">{report.remaining_quantity ?? "missing"}</td>
                        <td className="numeric-cell" data-label="Limit/last">{report.limit_or_last_price ?? "missing"}</td>
                        <td data-label="Sequence" data-testid="tws-execution-report-sequence">{report.sequence ?? "missing"}</td>
                        <td data-label="Source" data-testid="tws-execution-report-source-ref">
                          <CopyableCode label="report provenance ref" value={report.source_ref} />
                          {report.reload_checkpoint_id ? (
                            <small data-testid="tws-execution-report-reload-ref">{report.reload_checkpoint_id}</small>
                          ) : null}
                        </td>
                      </tr>
                    ))
                  ) : allBlockers.length > 0 ? (
                    allBlockers.map((blocker) => (
                      <tr data-testid="tws-execution-report-blocker" key={`execution-report-${blocker.blocker_id}`}>
                        <td data-label="Report type">blocked</td>
                        <td data-label="Client order" colSpan={2}>{blocker.blocker_id}</td>
                        <td data-label="Instrument">missing</td>
                        <td data-label="Side">missing</td>
                        <td data-label="Status/trade">{formatLabel(blocker.kind)}</td>
                        <td className="numeric-cell" data-label="Quantity">missing</td>
                        <td className="numeric-cell" data-label="Filled">missing</td>
                        <td className="numeric-cell" data-label="Remaining">missing</td>
                        <td className="numeric-cell" data-label="Limit/last">missing</td>
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
              <StateBadge value={paperArmed ? "partial" : summary.boundaries.action_controls ? "warning" : "empty"} />
            </div>
            <dl className="detail-list">
              <div>
                <dt>Mode</dt>
                <dd data-testid="account-command-mode">{paperArmed ? "paper_armed" : "observation only"}</dd>
              </div>
              <div>
                <dt>Controls</dt>
                <dd data-testid="account-command-controls-state">{paperArmed ? "mounted" : "none mounted"}</dd>
              </div>
              <div>
                <dt>Broker adapter</dt>
                <dd>{paperArmed ? "P024 API gate" : "not bound in this view"}</dd>
              </div>
            </dl>
            {paperArmed && submitIntent ? (
              <div className="command-control-stack" data-testid="account-paper-command-banner">
                <div className="command-preflight-row">
                  <span data-testid="account-command-preflight-ref">{submitIntent.preflight_ref}</span>
                </div>
                <form
                  className="command-form"
                  data-testid="account-submit-order-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    void handleSubmitIntent();
                  }}
                >
                  <label>
                    Instrument
                    <input readOnly value={submitIntent.instrument} />
                  </label>
                  <label>
                    Qty
                    <input readOnly value={submitIntent.quantity} />
                  </label>
                  <label>
                    Limit
                    <input readOnly value={submitIntent.limit_price} />
                  </label>
                  <span className="command-idempotency" data-testid="account-submit-idempotency-key">
                    {submitIntent.idempotency_key}
                  </span>
                  <button data-testid="account-submit-order-button" type="submit">
                    <Send size={14} />
                    Submit
                  </button>
                </form>
                {cancelEligibleOrder ? (
                  <div className="command-cancel-row">
                    <span data-testid="account-cancel-order-identity">
                      {cancelEligibleOrder.lifecycle_ref ?? cancelEligibleOrder.client_order_id}
                    </span>
                    <button
                      data-testid="account-cancel-order-button"
                      onClick={() => void handleCancelIntent(cancelEligibleOrder)}
                      type="button"
                    >
                      <CircleX size={14} />
                      Cancel
                    </button>
                  </div>
                ) : null}
                {commandError ? (
                  <div className="state-callout stale" data-testid="account-command-control-blocker">
                    {commandError}
                  </div>
                ) : null}
              </div>
            ) : null}
          </section>

          <CommandRuntimeRunRequestPanel request={runtimeRunRequest} error={runtimeRunRequestError} />
          <CommandRuntimeInvocationReadinessPanel readiness={governance.runtimeReadiness} error={governance.runtimeReadinessError} />
          <CommandRuntimeExecutionApprovalPacketPanel
            error={governance.runtimeApprovalPacketError}
            packet={governance.runtimeApprovalPacket}
          />
          <CommandRuntimeExecutionHandoffBundlePanel
            bundle={governance.runtimeHandoffBundle}
            error={governance.runtimeHandoffBundleError}
          />
          <CommandRuntimeExecutionGapAuditPanel
            audit={governance.runtimeExecutionGapAudit}
            error={governance.runtimeExecutionGapAuditError}
          />
          <CommandIntentReceiptPanel result={commandResult} />
          <CommandRuntimeCloseoutPanel closeout={governance.runtimeCloseout} error={governance.runtimeCloseoutError} />
          <CommandStatusPanel status={commandStatus} />

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
