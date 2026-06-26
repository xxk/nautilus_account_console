import type {
  AccountSnapshot,
  CancelIntentRequest,
  CommandApiResult,
  CommandPlaneProjection,
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

export async function fetchCommandPlaneProjection(accountId: string): Promise<CommandPlaneProjection> {
  const response = await fetch(`${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/projection`);
  if (!response.ok) {
    throw new Error(`command plane projection request failed: ${response.status}`);
  }
  return response.json();
}

export const LEGACY_COMMAND_READ_DESCRIPTOR = {
  owner: "account-console-backend.command-plane-retirement-registry",
  state: "legacy_read_only_until_mirror_convergence",
  retirementGuardrails: [
    "use_canonical_command_plane_projection_for_owner_decisions",
    "consume_projection_registered_legacy_reads_through_one_loader_only",
    "retire_legacy_command_reads_by_backend_owned_slice_registry_without_new_frontend_call_sites"
  ]
} as const;

type LegacyCommandPanelResult<T> = {
  data: T | null;
  error: string | null;
};

export type LegacyCommandReadSuite = {
  descriptor: typeof LEGACY_COMMAND_READ_DESCRIPTOR;
  routesLoaded: string[];
  runtimeCloseout?: LegacyCommandPanelResult<CommandRuntimeCloseout>;
  runtimeReadiness?: LegacyCommandPanelResult<CommandRuntimeInvocationReadiness>;
  runtimeApprovalPacket?: LegacyCommandPanelResult<CommandRuntimeExecutionApprovalPacket>;
  runtimeHandoffBundle?: LegacyCommandPanelResult<CommandRuntimeExecutionHandoffBundle>;
  runtimeExecutionGapAudit?: LegacyCommandPanelResult<CommandRuntimeExecutionGapAudit>;
};

const LEGACY_COMMAND_READ_REGISTRY = {
  "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}": {
    slot: "runtimeCloseout",
    load: fetchCommandRuntimeCloseout
  },
  "/api/commands/accounts/{account_id}/runtime-invocation-readiness": {
    slot: "runtimeReadiness",
    load: fetchCommandRuntimeInvocationReadiness
  },
  "/api/commands/accounts/{account_id}/runtime-execution-approval-packet": {
    slot: "runtimeApprovalPacket",
    load: fetchCommandRuntimeExecutionApprovalPacket
  },
  "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle": {
    slot: "runtimeHandoffBundle",
    load: fetchCommandRuntimeExecutionHandoffBundle
  },
  "/api/commands/accounts/{account_id}/runtime-execution-gap-audit": {
    slot: "runtimeExecutionGapAudit",
    load: fetchCommandRuntimeExecutionGapAudit
  },
} as const;

function toLegacyCommandPanelResult<T>(
  settled: PromiseSettledResult<T> | undefined,
  unavailableMessage: string
): LegacyCommandPanelResult<T> {
  if (!settled) {
    return {
      data: null,
      error: unavailableMessage
    };
  }
  if (settled.status === "fulfilled") {
    return {
      data: settled.value,
      error: null
    };
  }
  return {
    data: null,
    error: settled.reason instanceof Error ? settled.reason.message : unavailableMessage
  };
}

function getScheduledResult(
  settledBySlot: ReadonlyMap<string, PromiseSettledResult<unknown>>,
  slot: string
): PromiseSettledResult<unknown> | undefined {
  return settledBySlot.get(slot);
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

export async function fetchCommandRuntimeExecutionGapAudit(accountId: string): Promise<CommandRuntimeExecutionGapAudit> {
  const response = await fetch(
    `${API_BASE}/api/commands/accounts/${encodeURIComponent(accountId)}/runtime-execution-gap-audit`
  );
  if (!response.ok) {
    throw new Error(`runtime execution gap audit failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchLegacyCommandReadSuite(
  accountId: string,
  projection: CommandPlaneProjection
): Promise<LegacyCommandReadSuite> {
  const scheduledLoads = projection.retirement_slices
    .map((slice) => {
      const registration = LEGACY_COMMAND_READ_REGISTRY[slice.route as keyof typeof LEGACY_COMMAND_READ_REGISTRY];
      if (!registration) {
        return null;
      }
      return {
        route: slice.route,
        slot: registration.slot,
        request: registration.load(accountId)
      };
    })
    .filter((item): item is NonNullable<typeof item> => item !== null);

  const settled = await Promise.allSettled(scheduledLoads.map((item) => item.request));
  const suite: LegacyCommandReadSuite = {
    descriptor: LEGACY_COMMAND_READ_DESCRIPTOR,
    routesLoaded: scheduledLoads.map((item) => item.route)
  };

  const settledBySlot = new Map(
    scheduledLoads.map((item, index) => [item.slot, settled[index]] as const)
  );

  suite.runtimeCloseout = toLegacyCommandPanelResult(
    getScheduledResult(settledBySlot, "runtimeCloseout") as PromiseSettledResult<CommandRuntimeCloseout> | undefined,
    "runtime closeout not scheduled by command-plane retirement registry"
  );
  suite.runtimeReadiness = toLegacyCommandPanelResult(
    getScheduledResult(settledBySlot, "runtimeReadiness") as
      | PromiseSettledResult<CommandRuntimeInvocationReadiness>
      | undefined,
    "runtime readiness not scheduled by command-plane retirement registry"
  );
  suite.runtimeApprovalPacket = toLegacyCommandPanelResult(
    getScheduledResult(settledBySlot, "runtimeApprovalPacket") as
      | PromiseSettledResult<CommandRuntimeExecutionApprovalPacket>
      | undefined,
    "runtime approval packet not scheduled by command-plane retirement registry"
  );
  suite.runtimeHandoffBundle = toLegacyCommandPanelResult(
    getScheduledResult(settledBySlot, "runtimeHandoffBundle") as
      | PromiseSettledResult<CommandRuntimeExecutionHandoffBundle>
      | undefined,
    "runtime handoff bundle not scheduled by command-plane retirement registry"
  );
  suite.runtimeExecutionGapAudit = toLegacyCommandPanelResult(
    getScheduledResult(settledBySlot, "runtimeExecutionGapAudit") as
      | PromiseSettledResult<CommandRuntimeExecutionGapAudit>
      | undefined,
    "runtime execution gap audit not scheduled by command-plane retirement registry"
  );
  return suite;
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
