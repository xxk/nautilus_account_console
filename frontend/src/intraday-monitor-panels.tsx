import { AlertTriangle, ListFilter } from "lucide-react";

import type {
  IntradayMonitorExceptionRow,
  IntradayMonitorFixtureState,
  IntradayMonitorIncidentRow,
  IntradayMonitorPanelReadModel,
  IntradayMonitorStreamStateRow,
} from "./types";
import { intradayMonitorFixtureLabels } from "./app-registry";
import {
  BlockerList,
  Metric,
  RejectionRuleList,
  SourceRefsList,
  accountBoundaryRows,
} from "./panel-shared";
import { CopyableCode, StateBadge, formatLabel } from "./ui-primitives";

function formatLag(value: number | null): string {
  if (value === null) {
    return "missing";
  }
  if (value >= 1000) {
    return `${(value / 1000).toLocaleString(undefined, { maximumFractionDigits: 1 })}s`;
  }
  return `${value.toLocaleString()}ms`;
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

export function IntradayMonitorPanel({
  fixture,
  fixtureState,
  onFixtureState,
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
              Stale monitor checkpoint {fixture.context.monitor_checkpoint_id} at {fixture.context.monitor_checkpoint_ts}
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
