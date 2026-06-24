import type {
  CommandApiResult,
  CommandRuntimeRunRequest,
  MirrorAccountProjection,
} from "./types";
import { CopyableCode, StateBadge } from "./ui-primitives";

function commandStatusRefs(value: unknown): string[] {
  return Array.isArray(value)
    ? value.map((item) => (typeof item === "string" && item.length > 0 ? item : "unknown")).filter((item) => item !== "unknown")
    : [];
}

function commandStatusBlockerText(blocker: Record<string, unknown>) {
  const asText = (value: unknown, fallback = "unknown") =>
    typeof value === "string" && value.length > 0 ? value : fallback;
  return [
    asText(blocker.type, asText(blocker.stage, "command_status")),
    asText(blocker.reason, asText(blocker.kind, "missing evidence")),
    asText(blocker.source_ref, "missing source ref"),
  ].join(" | ");
}

export function CommandRuntimeRunRequestPanel({
  request,
  error,
}: {
  request: CommandRuntimeRunRequest | null;
  error: string | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-runtime-handoff-panel">
      <div className="terminal-panel-header">
        <h3>Runtime Handoff</h3>
        <StateBadge value={request ? "blocked" : error ? "blocked" : "empty"} />
      </div>
      {request ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Action</strong>
            <span data-testid="account-runtime-handoff-action">{request.action}</span>
          </div>
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-handoff-status">{request.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Entrypoint</strong>
            <span data-testid="account-runtime-handoff-entrypoint">{request.owner_runtime_entrypoint_ref}</span>
          </div>
          <div className="evidence-item">
            <strong>Config</strong>
            <span data-testid="account-runtime-handoff-config-ref">{request.owner_runtime_config_ref}</span>
          </div>
          <div className="evidence-item">
            <strong>Preflight</strong>
            <CopyableCode label="runtime handoff preflight" value={request.source_preflight_ref} />
          </div>
          {request.readback_ref ? (
            <div className="evidence-item">
              <strong>Readback</strong>
              <span data-testid="account-runtime-handoff-readback-ref">{request.readback_ref}</span>
            </div>
          ) : null}
          <div className="evidence-item">
            <strong>Checksum</strong>
            <span data-testid="account-runtime-handoff-checksum">{request.run_request_checksum}</span>
          </div>
          <div className="evidence-item">
            <strong>Runtime invoked</strong>
            <span data-testid="account-runtime-handoff-invoked">{String(request.runtime_invocation_attempted)}</span>
          </div>
          <div className="evidence-item">
            <strong>Browser trigger</strong>
            <span data-testid="account-runtime-handoff-web-trigger">
              {String(request.browser_triggered_broker_order)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Raw secrets</strong>
            <span data-testid="account-runtime-handoff-raw-secret">
              {String(request.raw_secret_values_recorded)}
            </span>
          </div>
          {request.blockers.map((blocker) => (
            <div className="evidence-item" data-testid="account-runtime-handoff-blocker" key={blocker.blocker_id}>
              <strong>{blocker.type}</strong>
              <span>{blocker.next_action}</span>
            </div>
          ))}
          {request.explicit_non_claims.map((claim) => (
            <div className="evidence-item" data-testid="account-runtime-handoff-non-claim" key={claim}>
              <strong>Non-claim</strong>
              <span>{claim}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-handoff-error">
          {error}
        </div>
      ) : (
        <p className="muted">No owner-runtime handoff request has been prepared from this browser session.</p>
      )}
    </section>
  );
}

export function CommandIntentReceiptPanel({
  result,
}: {
  result: CommandApiResult | null;
}) {
  const blockers = result?.blockers ?? [];
  return (
    <section className="terminal-panel" data-testid="account-command-intent-receipt-panel">
      <div className="terminal-panel-header">
        <h3>Intent Receipt</h3>
        <StateBadge value={result ? "partial" : "empty"} />
      </div>
      {result ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item" data-testid="account-command-intent-ref">
            <strong>Intent</strong>
            <CopyableCode label="command intent ref" value={result.intent_ref} />
          </div>
          <div className="evidence-item">
            <strong>Action</strong>
            <span data-testid="account-command-intent-action">{result.action}</span>
          </div>
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-command-intent-status">{result.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Next</strong>
            <span data-testid="account-command-intent-next-stage">{result.next_required_stage}</span>
          </div>
          <div className="evidence-item">
            <strong>Idempotency</strong>
            <span data-testid="account-command-intent-idempotency">{result.idempotency_key}</span>
          </div>
          <div className="evidence-item">
            <strong>Gateway final</strong>
            <span data-testid="account-command-intent-gateway-final-state">
              {result.gateway_ack_is_final_state ? "invalid" : "false"}
            </span>
          </div>
          {blockers.map((blocker) => (
            <article
              className="blocker-item"
              data-testid="account-command-intent-blocker"
              key={`${String(blocker.blocker_id)}-${String(blocker.stage)}`}
            >
              {commandStatusBlockerText(blocker as unknown as Record<string, unknown>)}
            </article>
          ))}
        </div>
      ) : (
        <p className="muted">No intent receipt is mounted for this read-only projection.</p>
      )}
    </section>
  );
}

export function CommandStatusPanel({
  status,
}: {
  status: MirrorAccountProjection["command_status"] | null;
}) {
  const riskRefs = commandStatusRefs(status?.risk_decision_refs);
  const approvalRefs = commandStatusRefs(status?.approval_decision_refs);
  const gatewayRefs = commandStatusRefs(status?.gateway_event_refs);
  const readbackRefs = commandStatusRefs(status?.readback_refs);
  const blockers = Array.isArray(status?.blockers) ? status.blockers : [];
  const reconciliationRef =
    typeof status?.reconciliation_ref === "string" && status.reconciliation_ref.length > 0
      ? status.reconciliation_ref
      : "";
  const commandAuditRef =
    typeof status?.command_audit_ref === "string" && status.command_audit_ref.length > 0
      ? status.command_audit_ref
      : "";
  const hasReadback = readbackRefs.length > 0;
  const hasReconciliation = reconciliationRef.length > 0;
  const hasGatewayFinalClaim = status?.gateway_ack_is_final_state === true;
  const derivedBlockers = [
    ...blockers.map(commandStatusBlockerText),
    ...(status && !hasReadback ? ["missing readback refs"] : []),
    ...(status && !hasReconciliation ? ["missing reconciliation ref"] : []),
    ...(hasGatewayFinalClaim ? ["gateway ack is not final account state"] : []),
  ];
  const displayState = !status ? "empty" : derivedBlockers.length > 0 ? "blocked" : typeof status.status === "string" ? status.status : "unknown";

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
