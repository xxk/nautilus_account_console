import type {
  CommandPlaneProjection,
  CommandRuntimeCloseout,
  CommandRuntimeExecutionApprovalPacket,
  CommandRuntimeExecutionGapAudit,
  CommandRuntimeExecutionHandoffBundle,
  CommandRuntimeInvocationReadiness,
} from "./types";
import { CopyableCode, StateBadge } from "./ui-primitives";

export function CommandPlaneOwnerPanel({
  commandPlaneProjection,
  commandPlaneProjectionError,
  projectionSummary,
}: {
  commandPlaneProjection: CommandPlaneProjection | null;
  commandPlaneProjectionError: string | null;
  projectionSummary: {
    retainBlockerCount: number;
    retiredWithPanelsCount: number;
    panelMappingsPreview: string;
    firstBatchSummary: string;
  } | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-command-plane-owner-panel">
      <div className="terminal-panel-header">
        <h3>Command Plane Owner</h3>
        <StateBadge value={commandPlaneProjection ? "healthy" : commandPlaneProjectionError ? "warning" : "stale"} />
      </div>
      {commandPlaneProjection ? (
        <dl className="detail-list">
          <div>
            <dt>Canonical source</dt>
            <dd data-testid="account-command-plane-canonical-source">{commandPlaneProjection.canonical_source}</dd>
          </div>
          <div>
            <dt>Projection owner</dt>
            <dd data-testid="account-command-plane-owner">{commandPlaneProjection.projection_owner}</dd>
          </div>
          <div>
            <dt>Legacy read state</dt>
            <dd data-testid="account-command-plane-legacy-state">{commandPlaneProjection.legacy_read_surface_state}</dd>
          </div>
          <div>
            <dt>Legacy reads</dt>
            <dd data-testid="account-command-plane-legacy-count">{commandPlaneProjection.legacy_read_surfaces.length}</dd>
          </div>
          <div>
            <dt>Retired archive surfaces</dt>
            <dd data-testid="account-command-plane-archive-count">
              {commandPlaneProjection.retired_archive_surfaces.length}
            </dd>
          </div>
          <div>
            <dt>Guardrails</dt>
            <dd data-testid="account-command-plane-guardrails">{commandPlaneProjection.retirement_guardrails.join(", ")}</dd>
          </div>
          <div>
            <dt>Retain blockers</dt>
            <dd data-testid="account-command-plane-retain-count">{projectionSummary?.retainBlockerCount ?? 0}</dd>
          </div>
          <div>
            <dt>Retire with panels</dt>
            <dd data-testid="account-command-plane-retire-count">{projectionSummary?.retiredWithPanelsCount ?? 0}</dd>
          </div>
          <div>
            <dt>Panel mappings</dt>
            <dd data-testid="account-command-plane-panel-mappings">{projectionSummary?.panelMappingsPreview ?? ""}</dd>
          </div>
          <div>
            <dt>First batch</dt>
            <dd data-testid="account-command-plane-first-batch">{projectionSummary?.firstBatchSummary ?? "none"}</dd>
          </div>
        </dl>
      ) : commandPlaneProjectionError ? (
        <p className="terminal-muted-text">{commandPlaneProjectionError}</p>
      ) : (
        <p className="terminal-muted-text">Loading canonical command-plane owner projection...</p>
      )}
    </section>
  );
}

export function CommandRuntimeInvocationReadinessPanel({
  readiness,
  error,
}: {
  readiness: CommandRuntimeInvocationReadiness | null;
  error: string | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-runtime-readiness-panel">
      <div className="terminal-panel-header">
        <h3>Runtime Readiness</h3>
        <StateBadge value={readiness ? "blocked" : error ? "blocked" : "empty"} />
      </div>
      {readiness ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-readiness-status">{readiness.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Owner</strong>
            <span data-testid="account-runtime-readiness-owner">{readiness.owner_runtime.owner_ref}</span>
          </div>
          <div className="evidence-item">
            <strong>Owner path</strong>
            <span data-testid="account-runtime-readiness-owner-path">{readiness.owner_runtime.owner_repo_path}</span>
          </div>
          <div className="evidence-item">
            <strong>Config</strong>
            <span data-testid="account-runtime-readiness-config-ref">{readiness.owner_runtime.config_ref}</span>
          </div>
          <div className="evidence-item">
            <strong>Approval required</strong>
            <span data-testid="account-runtime-readiness-approval-required">
              {String(readiness.external_write_approval_request.required)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval obtained</strong>
            <span data-testid="account-runtime-readiness-approval-obtained">
              {String(readiness.external_write_approval_request.obtained)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Runtime invoked</strong>
            <span data-testid="account-runtime-readiness-invoked">
              {String(readiness.negative_assertions.runtime_invocation_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Owner write</strong>
            <span data-testid="account-runtime-readiness-owner-write">
              {String(readiness.negative_assertions.owner_repo_write_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Browser trigger</strong>
            <span data-testid="account-runtime-readiness-browser-trigger">
              {String(readiness.negative_assertions.browser_triggered_broker_order)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Raw secrets</strong>
            <span data-testid="account-runtime-readiness-raw-secret">
              {String(readiness.negative_assertions.raw_secret_values_recorded)}
            </span>
          </div>
          {readiness.entrypoints.map((entrypoint) => (
            <div className="evidence-item" data-testid="account-runtime-readiness-entrypoint" key={entrypoint.action}>
              <strong>{entrypoint.action}</strong>
              <span>
                {entrypoint.entrypoint_ref} / {entrypoint.armed_flag}
              </span>
            </div>
          ))}
          {readiness.blockers.map((blocker) => (
            <div className="evidence-item" data-testid="account-runtime-readiness-blocker" key={blocker.blocker_id}>
              <strong>{blocker.type}</strong>
              <span>{blocker.next_action}</span>
            </div>
          ))}
          {readiness.explicit_non_claims.map((claim) => (
            <div className="evidence-item" data-testid="account-runtime-readiness-non-claim" key={claim}>
              <strong>Non-claim</strong>
              <span>{claim}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-readiness-error">
          {error}
        </div>
      ) : (
        <p className="muted">No owner-runtime invocation readiness evidence is mounted for this account.</p>
      )}
    </section>
  );
}

export function CommandRuntimeExecutionApprovalPacketPanel({
  packet,
  error,
}: {
  packet: CommandRuntimeExecutionApprovalPacket | null;
  error: string | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-runtime-approval-packet-panel">
      <div className="terminal-panel-header">
        <h3>Runtime Approval</h3>
        <StateBadge value={packet ? "blocked" : error ? "blocked" : "empty"} />
      </div>
      {packet ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-approval-packet-status">{packet.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Verdict</strong>
            <span data-testid="account-runtime-approval-packet-verdict">{packet.verdict}</span>
          </div>
          <div className="evidence-item">
            <strong>Owner path</strong>
            <span data-testid="account-runtime-approval-packet-owner-path">
              {packet.required_operator_approval.approval_path}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval required</strong>
            <span data-testid="account-runtime-approval-packet-required">
              {String(packet.required_operator_approval.required)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval obtained</strong>
            <span data-testid="account-runtime-approval-packet-obtained">
              {String(packet.required_operator_approval.obtained)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Runtime invoked</strong>
            <span data-testid="account-runtime-approval-packet-invoked">
              {String(packet.negative_assertions.runtime_invocation_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Owner write</strong>
            <span data-testid="account-runtime-approval-packet-owner-write">
              {String(packet.negative_assertions.owner_repo_write_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Broker order</strong>
            <span data-testid="account-runtime-approval-packet-broker-order">
              {String(packet.negative_assertions.broker_order_created)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval text</strong>
            <span data-testid="account-runtime-approval-packet-exact-text">
              {packet.required_operator_approval.exact_approval_text}
            </span>
          </div>
          {packet.entrypoints.map((entrypoint) => (
            <div className="evidence-item" data-testid="account-runtime-approval-packet-entrypoint" key={entrypoint.action}>
              <strong>{entrypoint.action}</strong>
              <span>
                {entrypoint.entrypoint_ref} / {entrypoint.armed_flag}
              </span>
            </div>
          ))}
          {packet.blockers.map((blocker) => (
            <div className="evidence-item" data-testid="account-runtime-approval-packet-blocker" key={blocker.blocker_id}>
              <strong>{blocker.type}</strong>
              <span>{blocker.next_action}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-approval-packet-error">
          {error}
        </div>
      ) : (
        <p className="muted">No owner-runtime execution approval packet is mounted for this account.</p>
      )}
    </section>
  );
}

export function CommandRuntimeExecutionHandoffBundlePanel({
  bundle,
  error,
}: {
  bundle: CommandRuntimeExecutionHandoffBundle | null;
  error: string | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-runtime-handoff-bundle-panel">
      <div className="terminal-panel-header">
        <h3>Runtime Bundle</h3>
        <StateBadge value={bundle ? "blocked" : error ? "blocked" : "empty"} />
      </div>
      {bundle ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-handoff-bundle-status">{bundle.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Verdict</strong>
            <span data-testid="account-runtime-handoff-bundle-verdict">{bundle.verdict}</span>
          </div>
          <div className="evidence-item">
            <strong>Execution allowed</strong>
            <span data-testid="account-runtime-handoff-bundle-execution-allowed">
              {String(bundle.execution_guard.execution_allowed)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval obtained</strong>
            <span data-testid="account-runtime-handoff-bundle-approval-obtained">
              {String(bundle.execution_guard.approval_obtained)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Runtime invoked</strong>
            <span data-testid="account-runtime-handoff-bundle-invoked">
              {String(bundle.negative_assertions.runtime_invocation_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Owner write</strong>
            <span data-testid="account-runtime-handoff-bundle-owner-write">
              {String(bundle.negative_assertions.owner_repo_write_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Broker order</strong>
            <span data-testid="account-runtime-handoff-bundle-broker-order">
              {String(bundle.negative_assertions.broker_order_created)}
            </span>
          </div>
          {bundle.runtime_input_requirements.map((item) => (
            <div className="evidence-item" data-testid="account-runtime-handoff-bundle-input" key={item.field}>
              <strong>{item.field}</strong>
              <span>{item.reason}</span>
            </div>
          ))}
          {bundle.operator_sequence.map((item) => (
            <div className="evidence-item" data-testid="account-runtime-handoff-bundle-step" key={item.step}>
              <strong>{item.step}</strong>
              <span>
                {item.action}
                {item.armed_flag ? ` / ${item.armed_flag}` : ""}
              </span>
            </div>
          ))}
          <div className="evidence-item">
            <strong>Artifacts</strong>
            <span data-testid="account-runtime-handoff-bundle-artifact-count">
              {bundle.required_owner_artifacts.length}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Gates</strong>
            <span data-testid="account-runtime-handoff-bundle-gate-count">{bundle.post_handoff_gates.length}</span>
          </div>
          {bundle.blockers.map((blocker) => (
            <div className="evidence-item" data-testid="account-runtime-handoff-bundle-blocker" key={blocker.blocker_id}>
              <strong>{blocker.type}</strong>
              <span>{blocker.next_action}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-handoff-bundle-error">
          {error}
        </div>
      ) : (
        <p className="muted">No owner-runtime execution handoff bundle is mounted for this account.</p>
      )}
    </section>
  );
}

export function CommandRuntimeExecutionGapAuditPanel({
  audit,
  error,
}: {
  audit: CommandRuntimeExecutionGapAudit | null;
  error: string | null;
}) {
  const a4 = audit?.not_accepted_scenarios.find((scenario) => scenario.id === "A4");
  return (
    <section className="terminal-panel" data-testid="account-runtime-execution-gap-panel">
      <div className="terminal-panel-header">
        <h3>Acceptance Gap</h3>
        <StateBadge value={audit ? "blocked" : error ? "blocked" : "empty"} />
      </div>
      {audit ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-execution-gap-status">{audit.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Verdict</strong>
            <span data-testid="account-runtime-execution-gap-verdict">{audit.verdict}</span>
          </div>
          <div className="evidence-item">
            <strong>Final claimed</strong>
            <span data-testid="account-runtime-execution-gap-final-claimed">
              {String(audit.negative_assertions.final_acceptance_claimed)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Accepted scenarios</strong>
            <span data-testid="account-runtime-execution-gap-accepted-count">{audit.accepted_scenarios.length}</span>
          </div>
          {a4 ? (
            <div className="evidence-item" data-testid="account-runtime-execution-gap-not-accepted">
              <strong>{a4.id}</strong>
              <span>
                {a4.current_status} / {a4.required_evidence_shape}
              </span>
            </div>
          ) : null}
          <div className="evidence-item">
            <strong>Approval obtained</strong>
            <span data-testid="account-runtime-execution-gap-approval-obtained">
              {String(audit.external_write_approval.obtained)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Approval path</strong>
            <span data-testid="account-runtime-execution-gap-approval-path">
              {audit.external_write_approval.approval_path}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Runtime invoked</strong>
            <span data-testid="account-runtime-execution-gap-invoked">
              {String(audit.negative_assertions.runtime_invocation_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Owner write</strong>
            <span data-testid="account-runtime-execution-gap-owner-write">
              {String(audit.negative_assertions.owner_repo_write_attempted)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Broker order</strong>
            <span data-testid="account-runtime-execution-gap-broker-order">
              {String(audit.negative_assertions.broker_order_created)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Artifacts</strong>
            <span data-testid="account-runtime-execution-gap-artifact-count">
              {audit.required_owner_artifacts.length}
            </span>
          </div>
          {audit.required_before_goal_complete.map((item) => (
            <div className="evidence-item" data-testid="account-runtime-execution-gap-required" key={item}>
              <strong>{item}</strong>
              <span>required before all acceptance</span>
            </div>
          ))}
          {audit.residual_blockers.map((blocker) => (
            <div className="evidence-item" data-testid="account-runtime-execution-gap-blocker" key={blocker.blocker_id}>
              <strong>{blocker.type}</strong>
              <span>{blocker.next_action}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-execution-gap-error">
          {error}
        </div>
      ) : (
        <p className="muted">No runtime execution gap audit is mounted for this account.</p>
      )}
    </section>
  );
}

export function CommandRuntimeCloseoutPanel({
  closeout,
  error,
}: {
  closeout: CommandRuntimeCloseout | null;
  error: string | null;
}) {
  return (
    <section className="terminal-panel" data-testid="account-runtime-closeout-panel">
      <div className="terminal-panel-header">
        <h3>Runtime Closeout</h3>
        <StateBadge value={closeout ? closeout.status : error ? "blocked" : "empty"} />
      </div>
      {closeout ? (
        <div className="evidence-stack compact-evidence-stack">
          <div className="evidence-item">
            <strong>Run</strong>
            <span data-testid="account-runtime-closeout-run-id">{closeout.run_id}</span>
          </div>
          <div className="evidence-item">
            <strong>Status</strong>
            <span data-testid="account-runtime-closeout-status">{closeout.status}</span>
          </div>
          <div className="evidence-item">
            <strong>Manifest</strong>
            <CopyableCode label="runtime closeout manifest" value={closeout.closeout_manifest_ref} />
          </div>
          <div className="evidence-item">
            <strong>Checksum</strong>
            <span data-testid="account-runtime-closeout-manifest-checksum">{closeout.closeout_manifest_checksum}</span>
          </div>
          <div className="evidence-item">
            <strong>Gateway send</strong>
            <span data-testid="account-runtime-closeout-gateway-send">
              {String(closeout.runtime_gateway_send_observed)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Browser trigger</strong>
            <span data-testid="account-runtime-closeout-web-trigger">
              {String(closeout.browser_triggered_broker_order)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Raw secrets</strong>
            <span data-testid="account-runtime-closeout-raw-secret">
              {String(closeout.raw_secret_values_recorded)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Gateway final</strong>
            <span data-testid="account-runtime-closeout-gateway-final">
              {String(closeout.gateway_ack_is_final_state)}
            </span>
          </div>
          <div className="evidence-item">
            <strong>Artifacts</strong>
            <span data-testid="account-runtime-closeout-artifact-count">
              {Object.keys(closeout.artifact_checksums).length}
            </span>
          </div>
          {closeout.explicit_non_claims.map((claim) => (
            <div className="evidence-item" data-testid="account-runtime-closeout-non-claim" key={claim}>
              <strong>Non-claim</strong>
              <span>{claim}</span>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="state-callout blocked" data-testid="account-runtime-closeout-error">
          {error}
        </div>
      ) : (
        <p className="muted">No runtime command closeout evidence is mounted for this account.</p>
      )}
    </section>
  );
}
