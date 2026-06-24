import { AlertTriangle, ListFilter } from "lucide-react";

import type {
  AccountHealthCloseoutState,
  AccountHealthPanelReadModel,
  AccountHealthRow,
  AccountHealthSettlementState,
  AccountKind,
} from "./types";
import { healthFixtureLabels, type AccountHealthFixtureId } from "./app-registry";
import { Metric } from "./panel-shared";
import { CopyableCode, StateBadge, formatLabel, stateTone } from "./ui-primitives";

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
  value,
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

export function AccountHealthPanel({
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
  visibleRows,
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
          <span className={`state-badge ${stateTone(fixture.fixture_state)}`}>{healthFixtureLabels[fixtureState]}</span>
        </div>

        <div className="filter-toolbar" data-testid="daily-closeout-filter-toolbar">
          <label>
            <ListFilter size={14} />
            Fixture
            <select
              onChange={(event) => onFixtureState(event.target.value as AccountHealthFixtureId)}
              value={fixtureState}
            >
              {Object.entries(healthFixtureLabels).map(([value, label]) => (
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
                    <td data-label="Blockers" data-testid="daily-closeout-blocker">
                      {account.blocker_count}
                    </td>
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
