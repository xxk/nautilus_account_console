import { AlertTriangle, ListFilter } from "lucide-react";

import type {
  AccountEvidenceFixtureState,
  AccountEvidencePackage,
  AccountEvidencePanelReadModel,
  AccountEquityFixtureState,
  AccountEquityPanelReadModel,
  AccountIncidentRow,
  AccountIncidentsFixtureState,
  AccountIncidentsPanelReadModel,
  AccountOrderDetailFixtureState,
  AccountOrderDetailPanelReadModel,
  AccountOrderRow,
  AccountOrdersFixtureState,
  AccountOrdersPanelReadModel,
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
  AccountEquityPoint,
} from "./types";
import {
  accountEvidenceFixtureLabels,
  accountEquityFixtureLabels,
  accountIncidentsFixtureLabels,
  accountOrderDetailFixtureLabels,
  accountOrdersFixtureLabels,
  accountPositionsFixtureLabels,
  accountReconcileFixtureLabels,
  accountSettlementFixtureLabels,
  accountSummaryFixtureLabels,
} from "./app-registry";
import {
  BlockerList,
  Metric,
  Ref,
  RejectionRuleList,
  SourceRefsList,
  accountBoundaryRows,
} from "./panel-shared";
import { CopyableCode, StateBadge, formatLabel } from "./ui-primitives";

function formatMoney(value: number | null, currency = "CNY"): string {
  if (value === null) {
    return "missing";
  }
  return `${currency} ${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
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
          <dd>{evidencePackage.normalized_ref ? <CopyableCode label="normalized ref" value={evidencePackage.normalized_ref} /> : "missing"}</dd>
        </div>
        <div>
          <dt>Raw payload ref</dt>
          <dd>{evidencePackage.raw_payload_ref ? <CopyableCode label="raw payload ref" value={evidencePackage.raw_payload_ref} /> : "missing"}</dd>
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

export function AccountOrdersPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountOrdersPanelReadModel;
  fixtureState: AccountOrdersFixtureState;
  onFixtureState: (value: AccountOrdersFixtureState) => void;
  showFixtureSelector?: boolean;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Account authority", fixture.boundaries.account_truth],
    ["Order authority", fixture.boundaries.order_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Broker action flag", fixture.boundaries.broker_tradable],
    ["Action controls", fixture.boundaries.action_controls],
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

        {showFixtureSelector ? (
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
        ) : null}

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-orders-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale order checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
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

export function AccountPositionsPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountPositionsPanelReadModel;
  fixtureState: AccountPositionsFixtureState;
  onFixtureState: (value: AccountPositionsFixtureState) => void;
  showFixtureSelector?: boolean;
}) {
  const boundaryRows = accountBoundaryRows(fixture.boundaries, "Position authority");

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

        {showFixtureSelector ? (
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
        ) : null}

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-positions-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale position checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
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
        <RejectionRuleList rules={fixture.rejection_rules} testId="account-positions-rejection-rule" />
      </aside>
    </section>
  );
}

export function AccountSettlementPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountSettlementPanelReadModel;
  fixtureState: AccountSettlementFixtureState;
  onFixtureState: (value: AccountSettlementFixtureState) => void;
  showFixtureSelector?: boolean;
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

        {showFixtureSelector ? (
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
        ) : null}

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-settlement-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale settlement checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
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

export function AccountEquityPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountEquityPanelReadModel;
  fixtureState: AccountEquityFixtureState;
  onFixtureState: (value: AccountEquityFixtureState) => void;
  showFixtureSelector?: boolean;
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

        {showFixtureSelector ? (
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
        ) : null}

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-equity-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale equity checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
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

export function AccountReconcilePanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountReconcilePanelReadModel;
  fixtureState: AccountReconcileFixtureState;
  onFixtureState: (value: AccountReconcileFixtureState) => void;
  showFixtureSelector?: boolean;
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

        {showFixtureSelector ? (
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
        ) : null}

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

export function AccountIncidentsPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountIncidentsPanelReadModel;
  fixtureState: AccountIncidentsFixtureState;
  onFixtureState: (value: AccountIncidentsFixtureState) => void;
  showFixtureSelector?: boolean;
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

        {showFixtureSelector ? (
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
        ) : null}

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

export function AccountEvidencePanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountEvidencePanelReadModel;
  fixtureState: AccountEvidenceFixtureState;
  onFixtureState: (value: AccountEvidenceFixtureState) => void;
  showFixtureSelector?: boolean;
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

        {showFixtureSelector ? (
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
        ) : null}

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

export function AccountOrderDetailPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountOrderDetailPanelReadModel;
  fixtureState: AccountOrderDetailFixtureState;
  onFixtureState: (value: AccountOrderDetailFixtureState) => void;
  showFixtureSelector?: boolean;
}) {
  const boundaryRows: Array<[string, boolean]> = [
    ["Read-only projection", fixture.boundaries.read_only_projection],
    ["Runtime authority", fixture.boundaries.runtime_truth],
    ["Account authority", fixture.boundaries.account_truth],
    ["Order authority", fixture.boundaries.order_truth],
    ["Ledger authority", fixture.boundaries.ledger_truth],
    ["UI authority", fixture.boundaries.ui_truth],
    ["Action controls", fixture.boundaries.action_controls],
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

        {showFixtureSelector ? (
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
        ) : null}

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

export function AccountSummaryPanel({
  fixture,
  fixtureState,
  onFixtureState,
  showFixtureSelector = true,
}: {
  fixture: AccountSummaryPanelReadModel;
  fixtureState: AccountSummaryFixtureState;
  onFixtureState: (value: AccountSummaryFixtureState) => void;
  showFixtureSelector?: boolean;
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
    ["Action controls", fixture.boundaries.action_controls],
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

        {showFixtureSelector ? (
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
        ) : null}

        {fixture.fixture_state === "stale" ? (
          <div className="state-callout stale" data-testid="account-summary-stale-state">
            <AlertTriangle size={16} />
            <span>
              Stale checkpoint {fixture.context.reducer_checkpoint_id} at {fixture.context.reducer_checkpoint_ts}
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
        <SourceRefsList refs={fixture.source_refs} testId="account-summary-source-ref" />
        <BlockerList blockers={fixture.blockers} testId="account-summary-blocker" />
      </aside>
    </section>
  );
}
