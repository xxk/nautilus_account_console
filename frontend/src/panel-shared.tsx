import { AlertTriangle } from "lucide-react";

import { CopyableCode, StateBadge, formatLabel } from "./ui-primitives";

export function SourceRefsList({
  refs,
  testId,
  title = "Source Refs",
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

export function RejectionRuleList({ rules, testId }: { rules: string[]; testId: string }) {
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

export function accountBoundaryRows(
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
    ["Action controls", boundaries.action_controls],
  ];
}

export function BlockerList({
  blockers,
  testId,
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

export function Ref({ label, value }: { label: string; value: string }) {
  return (
    <div className="ref-item">
      <span>{label}</span>
      <CopyableCode label={label} value={value} />
    </div>
  );
}

export function Metric({ label, testId, value }: { label: string; testId?: string; value: string }) {
  return (
    <div className="metric" data-testid={testId}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
