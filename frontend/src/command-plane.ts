import { useEffect, useMemo, useState } from "react";

import {
  fetchCommandPlaneProjection,
  fetchLegacyCommandReadSuite,
  type LegacyCommandReadSuite,
} from "./api";
import type {
  CommandPlaneProjection,
  CommandRuntimeCloseout,
  CommandRuntimeExecutionApprovalPacket,
  CommandRuntimeExecutionGapAudit,
  CommandRuntimeExecutionHandoffBundle,
  CommandRuntimeInvocationReadiness,
} from "./types";

export interface CommandPlaneProjectionSummary {
  retainBlockerCount: number;
  retiredWithPanelsCount: number;
  panelMappingsPreview: string;
  firstBatchSummary: string;
}

export interface CommandPlaneGovernanceState {
  commandPlaneProjection: CommandPlaneProjection | null;
  commandPlaneProjectionError: string | null;
  legacyCommandPanels: LegacyCommandReadSuite | null;
  runtimeCloseout: CommandRuntimeCloseout | null;
  runtimeCloseoutError: string | null;
  runtimeReadiness: CommandRuntimeInvocationReadiness | null;
  runtimeReadinessError: string | null;
  runtimeApprovalPacket: CommandRuntimeExecutionApprovalPacket | null;
  runtimeApprovalPacketError: string | null;
  runtimeHandoffBundle: CommandRuntimeExecutionHandoffBundle | null;
  runtimeHandoffBundleError: string | null;
  runtimeExecutionGapAudit: CommandRuntimeExecutionGapAudit | null;
  runtimeExecutionGapAuditError: string | null;
  projectionSummary: CommandPlaneProjectionSummary | null;
}

export function summarizeCommandPlaneProjection(
  projection: CommandPlaneProjection | null
): CommandPlaneProjectionSummary | null {
  if (!projection) {
    return null;
  }
  return {
    retainBlockerCount: projection.retirement_slices.filter(
      (slice) =>
        slice.category === "retain_blocker_projection" &&
        slice.execution_state === "active_blocker_projection"
    ).length,
    retiredWithPanelsCount: projection.retirement_slices.filter(
      (slice) =>
        slice.category === "retire_when_panels_removed" &&
        slice.execution_state === "retired_archive_only"
    ).length,
    panelMappingsPreview: projection.retired_archive_surfaces
      .slice(0, 3)
      .map((surface) => `${surface.panel_ids[0]} -> ${surface.route}`)
      .join("; "),
    firstBatchSummary: projection.retirement_batches[0]
      ? `${projection.retirement_batches[0].batch_id} [${projection.retirement_batches[0].execution_state}] (${projection.retirement_batches[0].route_count} routes / ${projection.retirement_batches[0].panel_count} panels)`
      : "none",
  };
}

export function useCommandPlaneGovernance(accountId: string): CommandPlaneGovernanceState {
  const [commandPlaneProjection, setCommandPlaneProjection] = useState<CommandPlaneProjection | null>(null);
  const [commandPlaneProjectionError, setCommandPlaneProjectionError] = useState<string | null>(null);
  const [legacyCommandPanels, setLegacyCommandPanels] = useState<LegacyCommandReadSuite | null>(null);

  useEffect(() => {
    if (accountId !== "acct.ctp.paper.19053") {
      setCommandPlaneProjection(null);
      setCommandPlaneProjectionError(null);
      setLegacyCommandPanels(null);
      return;
    }
    let active = true;
    async function loadRuntimeEvidence() {
      try {
        const commandPlaneProjectionResult = await fetchCommandPlaneProjection(accountId);
        const legacySuite = await fetchLegacyCommandReadSuite(accountId, commandPlaneProjectionResult);
        if (!active) {
          return;
        }
        setCommandPlaneProjection(commandPlaneProjectionResult);
        setCommandPlaneProjectionError(null);
        setLegacyCommandPanels(legacySuite);
      } catch (error) {
        if (!active) {
          return;
        }
        setCommandPlaneProjection(null);
        setLegacyCommandPanels(null);
        setCommandPlaneProjectionError(
          error instanceof Error ? error.message : "command-plane governance read failed"
        );
      }
    }
    void loadRuntimeEvidence();
    return () => {
      active = false;
    };
  }, [accountId]);

  const projectionSummary = useMemo(
    () => summarizeCommandPlaneProjection(commandPlaneProjection),
    [commandPlaneProjection]
  );

  return {
    commandPlaneProjection,
    commandPlaneProjectionError,
    legacyCommandPanels,
    runtimeCloseout: legacyCommandPanels?.runtimeCloseout?.data ?? null,
    runtimeCloseoutError: legacyCommandPanels?.runtimeCloseout?.error ?? null,
    runtimeReadiness: legacyCommandPanels?.runtimeReadiness?.data ?? null,
    runtimeReadinessError: legacyCommandPanels?.runtimeReadiness?.error ?? null,
    runtimeApprovalPacket: legacyCommandPanels?.runtimeApprovalPacket?.data ?? null,
    runtimeApprovalPacketError: legacyCommandPanels?.runtimeApprovalPacket?.error ?? null,
    runtimeHandoffBundle: legacyCommandPanels?.runtimeHandoffBundle?.data ?? null,
    runtimeHandoffBundleError: legacyCommandPanels?.runtimeHandoffBundle?.error ?? null,
    runtimeExecutionGapAudit: legacyCommandPanels?.runtimeExecutionGapAudit?.data ?? null,
    runtimeExecutionGapAuditError: legacyCommandPanels?.runtimeExecutionGapAudit?.error ?? null,
    projectionSummary,
  };
}
