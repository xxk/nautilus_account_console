import type {
  AccountSnapshot,
  CancelIntentRequest,
  CommandPartialFillOwnerRepairApprovalPacket,
  CommandPartialFillRemainingAcceptanceCurrentState,
  CommandPartialFillOwnerRepairEvidenceIngestGate,
  CommandPartialFillOwnerRepairEvidenceIngestAudit,
  CommandPartialFillPostRepairRuntimeRetryApprovalPacket,
  CommandPartialFillPostRepairRuntimeAttemptAudit,
  CommandPartialFillOwnerRepairExecutionHandoffBundle,
  CommandPartialFillOwnerRepairImplementationPlan,
  CommandPartialFillOwnerRepairPatchPreview,
  CommandPartialFillOwnerRepairPreflightSourceAudit,
  CommandPartialFillRuntimeExecutionApprovalPacket,
  CommandPartialFillRuntimeExecutionHandoffBundle,
  CommandApiResult,
  CommandRuntimeCloseout,
  CommandRuntimeExecutionApprovalPacket,
  CommandRuntimeExecutionGapAudit,
  CommandRuntimeExecutionHandoffBundle,
  CommandRuntimeInvocationReadiness,
  CommandRuntimeRunRequest,
  MirrorAccountProjection,
  MirrorEvidenceResponse,
  MirrorListResponse,
  MirrorSourceHealthResponse,
  OrderIntentRequest,
  OrderEvent,
  OrderExecutionReports
} from "./types";

const API_BASE = "";

export async function fetchAccounts(): Promise<AccountSnapshot[]> {
  const response = await fetch(`${API_BASE}/api/accounts`);
  if (!response.ok) {
    throw new Error(`accounts request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchEvents(accountId: string, cursor = 0): Promise<OrderEvent[]> {
  const response = await fetch(`${API_BASE}/api/accounts/${accountId}/events?cursor=${cursor}`);
  if (!response.ok) {
    throw new Error(`events request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchOrderExecutionReports(
  accountId: string,
  clientOrderId: string
): Promise<OrderExecutionReports> {
  const response = await fetch(
    `${API_BASE}/api/accounts/${accountId}/orders/${clientOrderId}/execution-reports`
  );
  if (!response.ok) {
    throw new Error(`execution reports request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchMirrorAccounts(): Promise<MirrorListResponse> {
  const response = await fetch(`${API_BASE}/api/mirror/accounts`);
  if (!response.ok) {
    throw new Error(`mirror accounts request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchMirrorAccount(accountId: string): Promise<MirrorAccountProjection> {
  const response = await fetch(`${API_BASE}/api/mirror/accounts/${encodeURIComponent(accountId)}`);
  if (!response.ok) {
    throw new Error(`mirror account request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchMirrorSourceHealth(accountId: string): Promise<MirrorSourceHealthResponse> {
  const response = await fetch(`${API_BASE}/api/mirror/accounts/${encodeURIComponent(accountId)}/source-health`);
  if (!response.ok) {
    throw new Error(`mirror source health request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchMirrorEvidence(accountId: string): Promise<MirrorEvidenceResponse> {
  const response = await fetch(`${API_BASE}/api/mirror/accounts/${encodeURIComponent(accountId)}/evidence`);
  if (!response.ok) {
    throw new Error(`mirror evidence request failed: ${response.status}`);
  }
  return response.json();
}

export async function submitPaperOrderIntent(
  accountId: string,
  intent: OrderIntentRequest
): Promise<CommandApiResult> {
  const response = await fetch(`${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/submit-intents`, {
    body: JSON.stringify(intent),
    headers: { "Content-Type": "application/json" },
    method: "POST"
  });
  if (!response.ok) {
    throw new Error(`submit intent request failed: ${response.status}`);
  }
  return response.json();
}

export async function cancelPaperOrderIntent(
  accountId: string,
  intent: CancelIntentRequest
): Promise<CommandApiResult> {
  const response = await fetch(`${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/cancel-intents`, {
    body: JSON.stringify(intent),
    headers: { "Content-Type": "application/json" },
    method: "POST"
  });
  if (!response.ok) {
    throw new Error(`cancel intent request failed: ${response.status}`);
  }
  return response.json();
}

export async function prepareSubmitRuntimeRunRequest(
  accountId: string,
  intent: OrderIntentRequest
): Promise<CommandRuntimeRunRequest> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-run-requests/submit`,
    {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(intent)
    }
  );
  if (!response.ok) {
    throw new Error(`submit runtime handoff request failed: ${response.status}`);
  }
  return response.json();
}

export async function prepareCancelRuntimeRunRequest(
  accountId: string,
  intent: CancelIntentRequest
): Promise<CommandRuntimeRunRequest> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-run-requests/cancel`,
    {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(intent)
    }
  );
  if (!response.ok) {
    throw new Error(`cancel runtime handoff request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandRuntimeCloseout(
  accountId: string,
  runId = "p023-armed-20260621t0748z"
): Promise<CommandRuntimeCloseout> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-closeouts/${encodeURIComponent(runId)}`
  );
  if (!response.ok) {
    throw new Error(`runtime closeout request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandRuntimeInvocationReadiness(
  accountId: string
): Promise<CommandRuntimeInvocationReadiness> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-invocation-readiness`
  );
  if (!response.ok) {
    throw new Error(`runtime invocation readiness failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandRuntimeExecutionApprovalPacket(
  accountId: string
): Promise<CommandRuntimeExecutionApprovalPacket> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-execution-approval-packet`
  );
  if (!response.ok) {
    throw new Error(`runtime execution approval packet failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandRuntimeExecutionHandoffBundle(
  accountId: string
): Promise<CommandRuntimeExecutionHandoffBundle> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-execution-handoff-bundle`
  );
  if (!response.ok) {
    throw new Error(`runtime execution handoff bundle failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillRuntimeExecutionApprovalPacket(
  accountId: string
): Promise<CommandPartialFillRuntimeExecutionApprovalPacket> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-runtime-execution-approval-packet`
  );
  if (!response.ok) {
    throw new Error(`partial-fill runtime execution approval packet failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillRuntimeExecutionHandoffBundle(
  accountId: string
): Promise<CommandPartialFillRuntimeExecutionHandoffBundle> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-runtime-execution-handoff-bundle`
  );
  if (!response.ok) {
    throw new Error(`partial-fill runtime execution handoff bundle failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandRuntimeExecutionGapAudit(accountId: string): Promise<CommandRuntimeExecutionGapAudit> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-execution-gap-audit`
  );
  if (!response.ok) {
    throw new Error(`runtime execution gap audit failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairImplementationPlan(
  accountId: string
): Promise<CommandPartialFillOwnerRepairImplementationPlan> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-implementation-plan`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair implementation plan failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairApprovalPacket(
  accountId: string
): Promise<CommandPartialFillOwnerRepairApprovalPacket> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-approval-packet`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair approval packet failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillRemainingAcceptanceCurrentState(
  accountId: string
): Promise<CommandPartialFillRemainingAcceptanceCurrentState> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-remaining-acceptance-current-state`
  );
  if (!response.ok) {
    throw new Error(`partial-fill remaining acceptance current state failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairEvidenceIngestGate(
  accountId: string
): Promise<CommandPartialFillOwnerRepairEvidenceIngestGate> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-evidence-ingest-gate`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair evidence ingest gate failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairEvidenceIngestAudit(
  accountId: string
): Promise<CommandPartialFillOwnerRepairEvidenceIngestAudit> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-evidence-ingest-audit`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair evidence ingest audit failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillPostRepairRuntimeRetryApprovalPacket(
  accountId: string
): Promise<CommandPartialFillPostRepairRuntimeRetryApprovalPacket> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-post-repair-runtime-retry-approval-packet`
  );
  if (!response.ok) {
    throw new Error(`partial-fill post-repair runtime retry approval packet failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillPostRepairRuntimeAttemptAudit(
  accountId: string
): Promise<CommandPartialFillPostRepairRuntimeAttemptAudit> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-post-repair-runtime-attempt-audit`
  );
  if (!response.ok) {
    throw new Error(`partial-fill post-repair runtime attempt audit failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairPreflightSourceAudit(
  accountId: string
): Promise<CommandPartialFillOwnerRepairPreflightSourceAudit> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-preflight-source-audit`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair preflight source audit failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairPatchPreview(
  accountId: string
): Promise<CommandPartialFillOwnerRepairPatchPreview> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-patch-preview`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair patch preview failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchCommandPartialFillOwnerRepairExecutionHandoffBundle(
  accountId: string
): Promise<CommandPartialFillOwnerRepairExecutionHandoffBundle> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/partial-fill-owner-repair-execution-handoff-bundle`
  );
  if (!response.ok) {
    throw new Error(`partial-fill owner repair execution handoff bundle failed: ${response.status}`);
  }
  return response.json();
}

export function openEventStream(
  accountId: string,
  cursor: number,
  onEvent: (event: OrderEvent) => void,
  onStatus: (status: "live" | "stale") => void
): EventSource {
  const source = new EventSource(`${API_BASE}/api/accounts/${accountId}/events/stream?cursor=${cursor}`);
  source.addEventListener("open", () => onStatus("live"));
  source.addEventListener("error", () => onStatus("stale"));
  source.addEventListener("order_event", (message) => {
    onEvent(JSON.parse((message as MessageEvent).data) as OrderEvent);
  });
  return source;
}
