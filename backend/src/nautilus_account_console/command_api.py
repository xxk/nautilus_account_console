from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException

from .command_actions import (
    accept_cancel_intent,
    accept_submit_intent,
    prepare_cancel_runtime_run_request,
    prepare_submit_runtime_run_request,
)
from .schemas import (
    CommandPlaneProjection,
    CommandReadRetirementBatch,
    CommandRetiredArchiveSurface,
    CommandReadRetirementSlice,
    CommandPartialFillOwnerRepairApprovalPacket,
    CommandPartialFillRuntimeExecutionApprovalPacket,
    CommandPartialFillRuntimeExecutionHandoffBundle,
    CommandPartialFillOwnerRepairImplementationPlan,
    CommandPartialFillOwnerRepairEvidenceIngestGate,
    CommandPartialFillOwnerRepairEvidenceIngestAudit,
    CommandPartialFillPostRepairRuntimeRetryApprovalPacket,
    CommandPartialFillPostRepairRuntimeAttemptAudit,
    CommandPartialFillOwnerRepairPreflightSourceAudit,
    CommandPartialFillOwnerRepairPatchPreview,
    CommandPartialFillOwnerRepairExecutionHandoffBundle,
    CommandPartialFillRemainingAcceptanceCurrentState,
    CommandRuntimeExecutionApprovalPacket,
    CommandRuntimeExecutionGapAudit,
    CommandRuntimeExecutionHandoffBundle,
    CommandRuntimeInvocationReadiness,
    CommandRuntimeCloseout,
)
from .account_mirror import AccountMirrorStore
from .source_bridge import load_capability_bundles


PAPER_ACCOUNT_ID = "acct.ctp.paper.19053"
PROPOSAL_ID = "p024-account-console-paper-command-controls"
ROOT = Path(__file__).resolve().parents[3]
COMMAND_RUN_ROOT = ROOT / "output" / "account_command" / "ctp-paper-19053"
RUNTIME_INVOCATION_READINESS = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-invocation-readiness.json"
)
RUNTIME_EXECUTION_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-approval-packet.json"
)
RUNTIME_EXECUTION_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-handoff-bundle.json"
)
RUNTIME_EXECUTION_GAP_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "runtime-execution-gap-audit.json"
)
PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-approval-packet.json"
)
PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-handoff-bundle.json"
)
PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-implementation-plan.json"
)
PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-approval-packet.json"
)
PARTIAL_FILL_REMAINING_ACCEPTANCE_CURRENT_STATE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-remaining-acceptance-current-state.json"
)
PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_GATE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-evidence-ingest-gate.json"
)
PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-evidence-ingest-audit.json"
)
PARTIAL_FILL_POST_REPAIR_RUNTIME_RETRY_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-post-repair-runtime-retry-approval-packet.json"
)
PARTIAL_FILL_POST_REPAIR_RUNTIME_ATTEMPT_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-post-repair-runtime-attempt-audit.json"
)
PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_SOURCE_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-preflight-source-audit.json"
)
PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-patch-preview.json"
)
PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-execution-handoff-bundle.json"
)
DEFAULT_RUNTIME_RUN_ID = "p023-armed-20260621t0748z"
REQUIRED_RUNTIME_FILES = [
    "submit_intent.json",
    "submit_risk_decision.json",
    "submit_approval_decision.json",
    "submit_gateway_event.json",
    "post_submit_readback.json",
    "cancel_intent.json",
    "cancel_risk_decision.json",
    "cancel_approval_decision.json",
    "cancel_gateway_event.json",
    "post_cancel_readback.json",
    "reconciliation_result.json",
    "command_audit.json",
    "redaction_report.json",
    "closeout_manifest.json",
]
SENSITIVE_RUNTIME_FRAGMENTS = ["tcp://", "trading.openctp", "Password", "AuthCode", "BrokerID", "UserID"]

LEGACY_COMMAND_READ_SURFACES = [
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}",
    "/api/commands/accounts/{account_id}/runtime-invocation-readiness",
    "/api/commands/accounts/{account_id}/runtime-execution-approval-packet",
    "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle",
    "/api/commands/accounts/{account_id}/runtime-execution-gap-audit",
]
RETIRED_ARCHIVE_COMMAND_SURFACES = [
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-runtime-approval-packet-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-runtime-approval-packet-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-runtime-handoff-bundle-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-runtime-handoff-bundle-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-approval-packet",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-approval-packet-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-approval-packet-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-remaining-acceptance-current-state",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-remaining-acceptance-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-remaining-acceptance-state-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-plan-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-plan-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-ingest-gate-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-ingest-gate-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-audit",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-ingest-audit-panel"],
        historical_contract_ref="docs/acceptance/p024-account-console-paper-command-controls/partial-fill-owner-repair-evidence-ingest-audit.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-retry-approval-packet",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-post-repair-runtime-retry-packet-panel"],
        historical_contract_ref="docs/acceptance/p024-account-console-paper-command-controls/partial-fill-post-repair-runtime-retry-approval-packet.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-attempt-audit",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-post-repair-runtime-attempt-panel"],
        historical_contract_ref="docs/acceptance/p024-account-console-paper-command-controls/partial-fill-post-repair-runtime-attempt-audit.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-preflight-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-preflight-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-patch-preview-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-patch-preview-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
    CommandRetiredArchiveSurface(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle",
        archive_evidence_only=True,
        panel_ids=["account-partial-fill-owner-repair-execution-handoff-panel"],
        historical_contract_ref="docs/acceptance/browser-evidence/p024-account-console-paper-command-controls/partial-fill-owner-repair-execution-handoff-ui.json",
        retirement_assertion="live_route_and_panel_retired_archive_evidence_only",
    ),
]
ACTION_COMMAND_SURFACES = [
    "/api/commands/accounts/{account_id}/submit-intents",
    "/api/commands/accounts/{account_id}/cancel-intents",
    "/api/commands/accounts/{account_id}/runtime-run-requests/submit",
    "/api/commands/accounts/{account_id}/runtime-run-requests/cancel",
]
LEGACY_COMMAND_RETIREMENT_SLICES = [
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}",
        category="retain_blocker_projection",
        execution_state="active_blocker_projection",
        panel_ids=["account-runtime-closeout-panel"],
        rationale="owner-runtime artifact closeout stays useful as a typed blocker/read-only audit surface",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/runtime-invocation-readiness",
        category="retain_blocker_projection",
        execution_state="active_blocker_projection",
        panel_ids=["account-runtime-readiness-panel"],
        rationale="external approval and owner-runtime readiness remain blocker-only governance surfaces",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/runtime-execution-approval-packet",
        category="retain_blocker_projection",
        execution_state="active_blocker_projection",
        panel_ids=["account-runtime-approval-packet-panel"],
        rationale="exact approval packet is a governance blocker packet, not durable command truth",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle",
        category="retain_blocker_projection",
        execution_state="active_blocker_projection",
        panel_ids=["account-runtime-handoff-bundle-panel"],
        rationale="handoff sequence remains a read-only blocker packet until owner-runtime execution is out of band",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/runtime-execution-gap-audit",
        category="retain_blocker_projection",
        execution_state="active_blocker_projection",
        panel_ids=["account-runtime-execution-gap-panel"],
        rationale="gap audit is explicit non-acceptance evidence and should stay separate from mirror command status",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-runtime-approval-packet-panel"],
        rationale="partial-fill attempt packet is panel-specific governance state, not durable command truth",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-runtime-handoff-bundle-panel"],
        rationale="partial-fill handoff is panel-specific governance flow and is now retired as archive-only historical evidence",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-approval-packet",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-approval-packet-panel"],
        rationale="owner repair approval packet is a temporary governance lane for partial-fill recovery only",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-remaining-acceptance-current-state",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-remaining-acceptance-panel"],
        rationale="remaining-acceptance audit tracked temporary acceptance debt and is now retired as archive-only historical evidence",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-plan-panel"],
        rationale="owner repair implementation plan is a temporary remediation document surface",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-ingest-gate-panel"],
        rationale="ingest gate is a temporary evidence-governance surface for repair closeout",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-audit",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-ingest-audit-panel"],
        rationale="ingest audit exists only to bridge owner repair evidence into this proposal lane",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-retry-approval-packet",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-post-repair-runtime-retry-packet-panel"],
        rationale="post-repair retry packet is a one-off governance surface for a consumed retry lane",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-attempt-audit",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-post-repair-runtime-attempt-panel"],
        rationale="post-repair attempt audit is specific to the temporary recovery/validation lane",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-preflight-panel"],
        rationale="preflight source audit is temporary recovery governance state",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-patch-preview-panel"],
        rationale="patch preview is temporary remediation planning state",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
    CommandReadRetirementSlice(
        route="/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle",
        category="retire_when_panels_removed",
        execution_state="retired_archive_only",
        panel_ids=["account-partial-fill-owner-repair-execution-handoff-panel"],
        rationale="repair execution handoff is a temporary repair-governance surface",
        successor_surface="/api/commands/accounts/{account_id}/projection",
    ),
]
LEGACY_COMMAND_RETIREMENT_BATCHES = [
    CommandReadRetirementBatch(
        batch_id="batch.partial_fill_post_repair_closeout_panels",
        execution_state="completed_safe_retirement",
        route_count=3,
        panel_count=3,
        routes=[
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-audit",
            "/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-retry-approval-packet",
            "/api/commands/accounts/{account_id}/partial-fill-post-repair-runtime-attempt-audit",
        ],
        panel_ids=[
            "account-partial-fill-owner-repair-ingest-audit-panel",
            "account-partial-fill-post-repair-runtime-retry-packet-panel",
            "account-partial-fill-post-repair-runtime-attempt-panel",
        ],
        preconditions=[
            "canonical_projection_retirement_slicing_present",
            "frontend_legacy_suite_loader_is_single_entrypoint",
            "p024_acceptance_docs_migrate_batch_to_archive_or_remove_panel_lane",
        ],
        rationale="These post-repair closeout panels describe a consumed temporary recovery lane and are the safest first grouped retirement target.",
    ),
    CommandReadRetirementBatch(
        batch_id="batch.partial_fill_pre_repair_attempt_planning_panels",
        execution_state="completed_safe_retirement",
        route_count=2,
        panel_count=2,
        routes=[
            "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-approval-packet",
            "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle",
        ],
        panel_ids=[
            "account-partial-fill-runtime-approval-packet-panel",
            "account-partial-fill-runtime-handoff-bundle-panel",
        ],
        preconditions=[
            "owner_repair_lane_is_canonical_next_step",
            "archive_only_artifact_validators_remain",
            "p024_acceptance_docs_migrate_phase4l_and_phase4m_ui_projection_to_archive_only",
        ],
        rationale="These panels described the superseded pre-repair attempt planning lane and are now retired from the active runtime UI as archive-only historical evidence.",
    ),
    CommandReadRetirementBatch(
        batch_id="batch.partial_fill_owner_repair_planning_panels",
        execution_state="completed_safe_retirement",
        route_count=3,
        panel_count=3,
        routes=[
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-approval-packet",
            "/api/commands/accounts/{account_id}/partial-fill-remaining-acceptance-current-state",
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan",
        ],
        panel_ids=[
            "account-partial-fill-owner-repair-approval-packet-panel",
            "account-partial-fill-remaining-acceptance-panel",
            "account-partial-fill-owner-repair-plan-panel",
        ],
        preconditions=[
            "archive_only_acceptance_rows_present_for_phase4p_phase4q_phase4r",
            "owner_repair_ingest_gate_is_canonical_active_follow_on_lane",
            "frontend_runtime_ui_no_longer_mounts_owner_repair_planning_panels",
        ],
        rationale="These planning and approval panels described a superseded temporary owner-repair governance lane and are now retired as archive-only historical evidence.",
    ),
    CommandReadRetirementBatch(
        batch_id="batch.partial_fill_owner_repair_execution_lane_panels",
        execution_state="completed_safe_retirement",
        route_count=4,
        panel_count=4,
        routes=[
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate",
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit",
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview",
            "/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle",
        ],
        panel_ids=[
            "account-partial-fill-owner-repair-ingest-gate-panel",
            "account-partial-fill-owner-repair-preflight-panel",
            "account-partial-fill-owner-repair-patch-preview-panel",
            "account-partial-fill-owner-repair-execution-handoff-panel",
        ],
        preconditions=[
            "archive_only_acceptance_rows_present_for_phase4u_phase4w_phase4y_phase4za",
            "owner_repair_ingest_audit_and_retry_artifacts_are_machine_checked",
            "frontend_runtime_ui_no_longer_mounts_owner_repair_execution_lane_panels",
        ],
        rationale="These execution-lane panels described a completed temporary repair governance sequence and are now retired as archive-only historical evidence.",
    ),
]


def _file_checksum(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _runtime_ref(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _scan_runtime_fragments(run_dir: Path) -> list[str]:
    matches: list[str] = []
    for path in sorted(run_dir.rglob("*.json")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
            matches.append(_runtime_ref(path))
    return matches


def _runtime_run_dir(run_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise HTTPException(status_code=400, detail="invalid runtime run_id")
    run_dir = (COMMAND_RUN_ROOT / run_id).resolve()
    root = COMMAND_RUN_ROOT.resolve()
    if not str(run_dir).startswith(str(root)):
        raise HTTPException(status_code=400, detail="runtime run_id escaped command evidence root")
    return run_dir


def load_command_plane_projection(account_id: str) -> CommandPlaneProjection:
    bundles = load_capability_bundles()
    projections = AccountMirrorStore().list_projections_from_bundles(bundles)
    projection = next((item for item in projections if item.account_id == account_id), None)
    if projection is None:
        raise HTTPException(status_code=404, detail="command plane projection not found")

    return CommandPlaneProjection(
        schema_version="account_command.command_plane_projection.v1",
        proposal_id=PROPOSAL_ID,
        account_id=projection.account_id,
        projection_owner="account-console-backend.mirror_projection",
        canonical_source="/api/mirror/accounts/{account_id}",
        legacy_read_surface_state="legacy_read_only_until_mirror_convergence",
        legacy_read_surfaces=list(LEGACY_COMMAND_READ_SURFACES),
        retired_archive_surfaces=list(RETIRED_ARCHIVE_COMMAND_SURFACES),
        action_surfaces=list(ACTION_COMMAND_SURFACES),
        retirement_guardrails=[
            "legacy_read_surfaces_are_projection_only",
            "legacy_read_surfaces_must_not_become_canonical_command_truth",
            "retired_archive_surfaces_must_not_be_treated_as_live_routes",
            "retire_legacy_reads_by_migrating_consumers_to_mirror_owned_projection",
        ],
        retirement_slices=list(LEGACY_COMMAND_RETIREMENT_SLICES),
        retirement_batches=list(LEGACY_COMMAND_RETIREMENT_BATCHES),
        source_ref=projection.source_ref,
        source_checksum=projection.source_checksum,
        projection_checkpoint_id=projection.projection_checkpoint_id,
        projection_checksum=projection.projection_checksum,
        blockers=list(projection.blockers),
        boundaries=dict(projection.boundaries),
        explicit_non_claims=[
            "does_not_promote_command_api_receipts_to_canonical_command_status",
            "does_not_make_legacy_command_reads_canonical_command_truth",
            "does_not_grant_account_console_broker_write_authority",
        ],
    )


def register_legacy_command_read_routes(app: FastAPI) -> None:
    for route in LEGACY_COMMAND_READ_ROUTE_REGISTRY:
        loader = route["loader"]
        path = str(route["path"])
        if path.endswith("/{run_id}"):
            app.add_api_route(
                path,
                cast(Callable[..., CommandRuntimeCloseout], loader),
                methods=["GET"],
                response_model=cast(type[CommandRuntimeCloseout], route["response_model"]),
                response_model_exclude_none=True,
            )
            continue
        app.add_api_route(
            path,
            cast(Callable[..., object], loader),
            methods=["GET"],
            response_model=route["response_model"],
            response_model_exclude_none=True,
        )


def load_runtime_closeout(account_id: str, run_id: str = DEFAULT_RUNTIME_RUN_ID) -> CommandRuntimeCloseout:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime closeout is scoped to acct.ctp.paper.19053 only")
    run_dir = _runtime_run_dir(run_id)
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="runtime closeout run not found")
    missing = [filename for filename in REQUIRED_RUNTIME_FILES if not (run_dir / filename).exists()]
    if missing:
        raise HTTPException(status_code=409, detail=f"runtime closeout missing artifacts: {missing}")
    leaks = _scan_runtime_fragments(run_dir)
    if leaks:
        raise HTTPException(status_code=409, detail=f"runtime closeout contains forbidden sensitive fragments: {leaks}")

    manifest_path = run_dir / "closeout_manifest.json"
    manifest = _read_json(manifest_path)
    audit_path = run_dir / "command_audit.json"
    audit = _read_json(audit_path)
    redaction = _read_json(run_dir / "redaction_report.json")
    reconciliation = _read_json(run_dir / "reconciliation_result.json")
    submit_gateway = _read_json(run_dir / "submit_gateway_event.json")
    cancel_gateway = _read_json(run_dir / "cancel_gateway_event.json")

    if manifest.get("account_id") != PAPER_ACCOUNT_ID or audit.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime closeout account_id mismatch")
    if manifest.get("status") != "reconciled" or audit.get("status") != "reconciled":
        raise HTTPException(status_code=409, detail="runtime closeout is not reconciled")
    if manifest.get("mode") != "paper_armed" or audit.get("mode") != "paper_armed":
        raise HTTPException(status_code=409, detail="runtime closeout is not paper_armed")
    if redaction.get("status") != "passed":
        raise HTTPException(status_code=409, detail="runtime closeout redaction did not pass")
    if reconciliation.get("status") != "reconciled":
        raise HTTPException(status_code=409, detail="runtime closeout reconciliation did not pass")
    if manifest.get("gateway_ack_is_final_state") is not False or audit.get("gateway_ack_is_final_state") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout marked gateway ack as final state")
    if manifest.get("raw_secret_values_recorded") is not False or audit.get("raw_secret_values_recorded") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout recorded raw secret values")
    if manifest.get("raw_broker_endpoint_recorded") is not False or audit.get("raw_broker_endpoint_recorded") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout recorded raw broker endpoint")
    if submit_gateway.get("paper_send_armed") is not True or cancel_gateway.get("cancel_send_armed") is not True:
        raise HTTPException(status_code=409, detail="runtime closeout gateway send evidence is not armed paper runtime")
    owner_evidence = manifest.get("owner_runtime_evidence") or audit.get("owner_runtime_evidence") or {}
    if owner_evidence.get("owner_repo_ref") != "owner-repo://nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="runtime closeout missing owner runtime evidence")
    if owner_evidence.get("raw_secret_values_recorded") is not False:
        raise HTTPException(status_code=409, detail="runtime closeout owner evidence recorded raw secrets")
    owner_artifacts = owner_evidence.get("artifact_refs")
    if not isinstance(owner_artifacts, list) or not owner_artifacts:
        raise HTTPException(status_code=409, detail="runtime closeout owner artifact refs missing")
    for item in owner_artifacts:
        if not isinstance(item, dict):
            raise HTTPException(status_code=409, detail="runtime closeout owner artifact ref invalid")
        if item.get("owner_repo_ref") != "owner-repo://nautilus_ctp_adapter":
            raise HTTPException(status_code=409, detail="runtime closeout owner artifact ref mismatch")
        if not str(item.get("checksum") or "").startswith("sha256:"):
            raise HTTPException(status_code=409, detail="runtime closeout owner artifact checksum missing")

    artifact_refs = manifest.get("artifact_refs")
    if not isinstance(artifact_refs, dict) or not artifact_refs:
        raise HTTPException(status_code=409, detail="runtime closeout manifest artifact_refs missing")
    artifact_checksums: dict[str, str] = {}
    for filename, item in artifact_refs.items():
        artifact_path = run_dir / filename
        if not artifact_path.exists():
            raise HTTPException(status_code=409, detail=f"manifest references missing artifact: {filename}")
        checksum = _file_checksum(artifact_path)
        if item.get("checksum") != checksum:
            raise HTTPException(status_code=409, detail=f"manifest checksum mismatch: {filename}")
        artifact_checksums[_runtime_ref(artifact_path)] = checksum

    return CommandRuntimeCloseout(
        schema_version="account_command.runtime_closeout.v1",
        proposal_id=PROPOSAL_ID,
        account_id=PAPER_ACCOUNT_ID,
        run_id=run_id,
        mode="paper_armed",
        status="reconciled",
        closeout_manifest_ref=_runtime_ref(manifest_path),
        closeout_manifest_checksum=_file_checksum(manifest_path),
        command_audit_ref=_runtime_ref(audit_path),
        command_audit_checksum=_file_checksum(audit_path),
        intent_refs=list(audit.get("intent_refs") or []),
        risk_decision_refs=list(audit.get("risk_decision_refs") or []),
        approval_decision_refs=list(audit.get("approval_decision_refs") or []),
        gateway_event_refs=list(audit.get("gateway_event_refs") or []),
        readback_refs=list(audit.get("readback_refs") or []),
        reconciliation_ref=str(audit.get("reconciliation_ref") or ""),
        artifact_checksums=artifact_checksums,
        runtime_gateway_send_observed=True,
        broker_order_created=True,
        browser_triggered_broker_order=False,
        gateway_ack_is_final_state=False,
        raw_secret_values_recorded=False,
        raw_broker_endpoint_recorded=False,
        runtime_duplicate_send_attempted=False,
        source_owner_ref="output/account_command/ctp-paper-19053",
        explicit_non_claims=[
            "does_not_send_broker_order_from_browser_read",
            "does_not_store_raw_ctp_secret_or_endpoint",
            "does_not_claim_live_readiness",
            "does_not_make_gateway_ack_final_state",
            "web_ui_trigger_of_new_runtime_order_still_pending",
        ],
    )


def load_runtime_invocation_readiness(account_id: str) -> CommandRuntimeInvocationReadiness:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime readiness is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_INVOCATION_READINESS.exists():
        raise HTTPException(status_code=404, detail="runtime invocation readiness evidence not found")
    text = RUNTIME_INVOCATION_READINESS.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime invocation readiness contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime invocation readiness account_id mismatch")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime invocation readiness negative assertion failed: {key}")
    owner = payload.get("owner_runtime") or {}
    if owner.get("config_raw_content_read") is not False:
        raise HTTPException(status_code=409, detail="runtime invocation readiness read raw config content")
    approval = payload.get("external_write_approval_request") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime invocation readiness approval boundary drifted")
    return CommandRuntimeInvocationReadiness(**payload)


def load_runtime_execution_approval_packet(account_id: str) -> CommandRuntimeExecutionApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime approval packet is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="runtime execution approval packet evidence not found")
    text = RUNTIME_EXECUTION_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution approval packet account_id mismatch")
    approval = payload.get("required_operator_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution approval packet approval boundary drifted")
    if approval.get("approval_path") != "D:/Nautilus/nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="runtime execution approval packet owner path drifted")
    planned = payload.get("planned_execution") or {}
    if planned.get("runtime_invocation_attempted") is not False or planned.get("owner_repo_write_attempted") is not False:
        raise HTTPException(status_code=409, detail="runtime execution approval packet planned execution flags drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
        "full_runtime_acceptance_claimed",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution approval packet negative assertion failed: {key}")
    return CommandRuntimeExecutionApprovalPacket(**payload)


def load_runtime_execution_handoff_bundle(account_id: str) -> CommandRuntimeExecutionHandoffBundle:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime handoff bundle is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_HANDOFF_BUNDLE.exists():
        raise HTTPException(status_code=404, detail="runtime execution handoff bundle evidence not found")
    text = RUNTIME_EXECUTION_HANDOFF_BUNDLE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle account_id mismatch")
    guard = payload.get("execution_guard") or {}
    if guard.get("execution_allowed") is not False:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle allowed execution before approval")
    if guard.get("approval_required") is not True or guard.get("approval_obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution handoff bundle approval boundary drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "execution_allowed",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
        "full_runtime_acceptance_claimed",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution handoff bundle negative assertion failed: {key}")
    return CommandRuntimeExecutionHandoffBundle(**payload)


def load_partial_fill_runtime_execution_approval_packet(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 partial-fill approval packet is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="partial-fill runtime execution approval packet evidence not found")
    text = PARTIAL_FILL_RUNTIME_EXECUTION_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval packet account_id mismatch")
    approval = payload.get("required_operator_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution approval boundary drifted")
    planned = payload.get("planned_execution") or {}
    for key in ["runtime_invocation_attempted", "owner_repo_write_attempted", "new_order_submitted", "cancel_sent"]:
        if planned.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill planned execution flag drifted: {key}")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "approval_obtained",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "new_order_submitted",
        "cancel_sent",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
        "full_acceptance_claimed",
        "browser_fixture_promoted_to_runtime_truth",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill approval packet negative assertion failed: {key}")
    return CommandPartialFillRuntimeExecutionApprovalPacket(**payload)


def load_partial_fill_runtime_execution_handoff_bundle(
    account_id: str,
) -> CommandPartialFillRuntimeExecutionHandoffBundle:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 partial-fill handoff bundle is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE.exists():
        raise HTTPException(status_code=404, detail="partial-fill runtime execution handoff bundle evidence not found")
    text = PARTIAL_FILL_RUNTIME_EXECUTION_HANDOFF_BUNDLE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff bundle contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff bundle account_id mismatch")
    guard = payload.get("execution_guard") or {}
    if guard.get("execution_allowed") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff allowed execution before approval")
    if guard.get("approval_required") is not True or guard.get("approval_obtained") is not False:
        raise HTTPException(status_code=409, detail="partial-fill runtime execution handoff approval boundary drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "execution_allowed",
        "approval_obtained",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "new_order_submitted",
        "cancel_sent",
        "full_acceptance_claimed",
        "browser_fixture_promoted_to_runtime_truth",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill handoff bundle negative assertion failed: {key}")
    return CommandPartialFillRuntimeExecutionHandoffBundle(**payload)


def load_runtime_execution_gap_audit(account_id: str) -> CommandRuntimeExecutionGapAudit:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 runtime execution gap audit is scoped to acct.ctp.paper.19053 only")
    if not RUNTIME_EXECUTION_GAP_AUDIT.exists():
        raise HTTPException(status_code=404, detail="runtime execution gap audit evidence not found")
    text = RUNTIME_EXECUTION_GAP_AUDIT.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="runtime execution gap audit contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="runtime execution gap audit account_id mismatch")
    approval = payload.get("external_write_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="runtime execution gap audit approval boundary drifted")
    not_accepted = {item.get("id"): item for item in payload.get("not_accepted_scenarios") or []}
    if not_accepted.get("A4", {}).get("current_status") != "blocked_pending_owner_runtime_execution":
        raise HTTPException(status_code=409, detail="runtime execution gap audit A4 status drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "final_acceptance_claimed",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_read",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"runtime execution gap audit negative assertion failed: {key}")
    return CommandRuntimeExecutionGapAudit(**payload)


def load_partial_fill_owner_repair_implementation_plan(
    account_id: str,
) -> CommandPartialFillOwnerRepairImplementationPlan:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair plan is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair implementation plan evidence not found")
    text = PARTIAL_FILL_OWNER_REPAIR_IMPLEMENTATION_PLAN.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan account_id mismatch")
    context = payload.get("owner_read_context") or {}
    if context.get("owner_repo_path") != "D:/Nautilus/nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan owner path drifted")
    if context.get("owner_repo_write_attempted") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan attempted owner write")
    runtime = payload.get("post_repair_runtime_attempt_gate") or {}
    if runtime.get("runtime_attempt_allowed_by_this_plan") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan allowed runtime retry")
    if runtime.get("fresh_approval_required") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair implementation plan lost fresh approval gate")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_repo_write_attempted_by_this_plan",
        "owner_runtime_invocation_attempted",
        "owner_repair_claimed_complete",
        "runtime_retry_authorized",
        "partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair implementation plan negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairImplementationPlan(**payload)


def load_partial_fill_owner_repair_approval_packet(
    account_id: str,
) -> CommandPartialFillOwnerRepairApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair approval packet is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair approval packet evidence not found")
    text = PARTIAL_FILL_OWNER_REPAIR_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet account_id mismatch")
    assessment = payload.get("current_thread_approval_assessment") or {}
    if assessment.get("matches_current_next_action") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet assessment drifted")
    approval = payload.get("required_owner_repair_approval") or {}
    if approval.get("required") is not True or approval.get("obtained") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet approval boundary drifted")
    if approval.get("approval_path") != "D:/Nautilus/nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet owner path drifted")
    if "repair owner close-offset semantics for P024" not in str(approval.get("exact_approval_text_required") or ""):
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet exact text drifted")
    retry_gate = payload.get("retry_gate") or {}
    for key in [
        "additional_partial_fill_order_authorized",
        "runtime_invocation_allowed",
    ]:
        if retry_gate.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair approval packet retry gate failed: {key}")
    if retry_gate.get("owner_repair_required_first") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair approval packet lost owner repair prerequisite")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_repo_write_attempted_by_this_packet",
        "owner_runtime_invocation_attempted",
        "owner_code_repair_authorized_by_current_thread_text",
        "additional_order_authorized",
        "partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair approval packet negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairApprovalPacket(**payload)


def load_partial_fill_remaining_acceptance_current_state(
    account_id: str,
) -> CommandPartialFillRemainingAcceptanceCurrentState:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 remaining acceptance state is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_REMAINING_ACCEPTANCE_CURRENT_STATE.exists():
        raise HTTPException(status_code=404, detail="partial-fill remaining acceptance current state evidence not found")
    text = PARTIAL_FILL_REMAINING_ACCEPTANCE_CURRENT_STATE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance current state contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance current state account_id mismatch")
    current = payload.get("current_authoritative_state") or {}
    if current.get("full_acceptance_claimed") is not False:
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance state claimed full acceptance")
    requirements = {item.get("requirement_id"): item for item in payload.get("remaining_acceptance_requirements") or []}
    expected = {
        "R1_owner_repair_approval",
        "R2_owner_close_offset_repair",
        "R3_owner_validators",
        "R4_post_repair_partial_fill_runtime",
        "R5_web_ui_real_partial_fill_projection",
    }
    if set(requirements) != expected:
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance state requirement set drifted")
    if any(item.get("current_status") != "missing" for item in requirements.values()):
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance state accepted missing evidence")
    next_action = payload.get("next_authorized_action") or {}
    if next_action.get("owner_code_repair_allowed") is not False or next_action.get("owner_runtime_retry_allowed") is not False:
        raise HTTPException(status_code=409, detail="partial-fill remaining acceptance state allowed owner action too early")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "full_acceptance_claimed",
        "owner_repair_claimed",
        "post_repair_runtime_retry_claimed",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill remaining acceptance state negative assertion failed: {key}")
    return CommandPartialFillRemainingAcceptanceCurrentState(**payload)


def load_partial_fill_owner_repair_evidence_ingest_gate(
    account_id: str,
) -> CommandPartialFillOwnerRepairEvidenceIngestGate:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair ingest gate is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_GATE.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair evidence ingest gate not found")
    text = PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_GATE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest gate contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest gate account_id mismatch")
    scope = payload.get("ingest_scope") or {}
    if scope.get("runtime_retry_allowed_by_ingest_gate") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest gate allowed runtime retry")
    if scope.get("accepts_owner_runtime_partial_fill_evidence") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest gate accepted runtime evidence too early")
    evidence = payload.get("required_owner_repair_evidence") or []
    if len(evidence) != 6 or any(item.get("current_status") != "missing" for item in evidence):
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest gate evidence state drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_repair_evidence_recorded",
        "owner_repo_write_attempted_by_this_gate",
        "owner_runtime_invocation_attempted",
        "runtime_retry_authorized",
        "partial_fill_runtime_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair evidence ingest gate negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairEvidenceIngestGate(**payload)


def load_partial_fill_owner_repair_evidence_ingest_audit(
    account_id: str,
) -> CommandPartialFillOwnerRepairEvidenceIngestAudit:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair ingest audit is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_AUDIT.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair evidence ingest audit not found")
    text = PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_AUDIT.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest audit contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest audit account_id mismatch")
    owner = payload.get("owner_repair_evidence") or {}
    if owner.get("owner_repo_ref") != "owner-repo://nautilus_ctp_adapter":
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest audit owner ref mismatch")
    if owner.get("owner_runtime_invocation_attempted") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence ingest audit invoked runtime")
    decision = payload.get("ingest_decision") or {}
    if decision.get("owner_repair_evidence_recorded") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair evidence not recorded")
    if decision.get("owner_validators_passed") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner validators not passed")
    if decision.get("runtime_retry_authorized") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair ingest audit authorized runtime retry")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_runtime_invocation_attempted",
        "post_repair_runtime_retry_claimed",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair ingest audit negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairEvidenceIngestAudit(**payload)


def load_partial_fill_post_repair_runtime_retry_approval_packet(
    account_id: str,
) -> CommandPartialFillPostRepairRuntimeRetryApprovalPacket:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 post-repair runtime retry packet is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_POST_REPAIR_RUNTIME_RETRY_APPROVAL_PACKET.exists():
        raise HTTPException(status_code=404, detail="partial-fill post-repair runtime retry approval packet not found")
    text = PARTIAL_FILL_POST_REPAIR_RUNTIME_RETRY_APPROVAL_PACKET.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime retry approval packet contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime retry approval packet account_id mismatch")
    guard = payload.get("runtime_retry_guard") or {}
    if guard.get("runtime_retry_authorized_by_packet") is not True:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime retry not authorized")
    if guard.get("maximum_attempts") != 1:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime retry attempt cap drifted")
    if guard.get("exposure_reduction_only") is not True or guard.get("small_order_only") is not True:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime retry risk guard drifted")
    negative = payload.get("negative_assertions_before_runtime") or {}
    for key in [
        "owner_runtime_invocation_attempted_by_packet",
        "paper_order_created_by_packet",
        "paper_cancel_sent_by_packet",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill post-repair runtime retry packet negative assertion failed: {key}")
    return CommandPartialFillPostRepairRuntimeRetryApprovalPacket(**payload)


def load_partial_fill_post_repair_runtime_attempt_audit(
    account_id: str,
) -> CommandPartialFillPostRepairRuntimeAttemptAudit:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 post-repair runtime attempt audit is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_POST_REPAIR_RUNTIME_ATTEMPT_AUDIT.exists():
        raise HTTPException(status_code=404, detail="partial-fill post-repair runtime attempt audit not found")
    text = PARTIAL_FILL_POST_REPAIR_RUNTIME_ATTEMPT_AUDIT.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime attempt audit contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime attempt audit account_id mismatch")
    obs = payload.get("runtime_observation") or {}
    if obs.get("partial_fill_formula_satisfied") is not False:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime attempt audit claimed partial fill")
    decision = payload.get("acceptance_decision") or {}
    if decision.get("partial_fill_then_cancel_acceptance_satisfied") is not False:
        raise HTTPException(status_code=409, detail="partial-fill post-repair runtime attempt audit claimed acceptance")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "additional_runtime_retry_authorized",
        "cancel_sent",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill post-repair runtime attempt audit negative assertion failed: {key}")
    return CommandPartialFillPostRepairRuntimeAttemptAudit(**payload)


def load_partial_fill_owner_repair_preflight_source_audit(
    account_id: str,
) -> CommandPartialFillOwnerRepairPreflightSourceAudit:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair preflight audit is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_SOURCE_AUDIT.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair preflight source audit not found")
    text = PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_SOURCE_AUDIT.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit account_id mismatch")
    owner = payload.get("owner_repo") or {}
    if owner.get("write_attempted_by_audit") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit attempted owner write")
    checks = payload.get("source_checks") or []
    if len(checks) != 3 or any(not item.get("sha256") or item.get("required_symbol_present") is not True for item in checks):
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit source checks drifted")
    approval = payload.get("operator_approval_delta") or {}
    if approval.get("sufficient_for_owner_code_repair") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit allowed owner repair")
    if approval.get("sufficient_for_post_repair_runtime_retry") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit allowed runtime retry")
    next_action = payload.get("next_required_action") or {}
    if next_action.get("blind_script_retry_rejected") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair preflight source audit did not reject blind retry")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_repo_write_attempted",
        "owner_code_repair_claimed",
        "owner_validator_pass_claimed",
        "owner_runtime_invocation_attempted",
        "post_repair_runtime_retry_authorized",
        "real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair preflight source audit negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairPreflightSourceAudit(**payload)


def load_partial_fill_owner_repair_patch_preview(
    account_id: str,
) -> CommandPartialFillOwnerRepairPatchPreview:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair patch preview is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair patch preview not found")
    text = PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview account_id mismatch")
    baseline = payload.get("owner_baseline") or {}
    if baseline.get("owner_repo_write_attempted_by_preview") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview attempted owner write")
    patches = payload.get("previewed_owner_patch") or []
    if len(patches) != 3 or not any(item.get("patch_id") == "add_close_yesterday_focused_test" for item in patches):
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview patch set drifted")
    gate = payload.get("post_patch_runtime_gate") or {}
    if gate.get("runtime_retry_authorized_by_preview") is not False:
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview authorized runtime retry")
    if gate.get("fresh_runtime_retry_approval_required_after_patch") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair patch preview missing fresh retry approval gate")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "owner_repo_write_attempted",
        "owner_patch_applied",
        "owner_validator_run_claimed",
        "owner_runtime_invocation_attempted",
        "runtime_retry_authorized",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair patch preview negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairPatchPreview(**payload)


def load_partial_fill_owner_repair_execution_handoff_bundle(
    account_id: str,
) -> CommandPartialFillOwnerRepairExecutionHandoffBundle:
    if account_id != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="P024 owner repair execution handoff is scoped to acct.ctp.paper.19053 only")
    if not PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BUNDLE.exists():
        raise HTTPException(status_code=404, detail="partial-fill owner repair execution handoff bundle not found")
    text = PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BUNDLE.read_text(encoding="utf-8")
    if any(fragment.lower() in text.lower() for fragment in SENSITIVE_RUNTIME_FRAGMENTS):
        raise HTTPException(status_code=409, detail="partial-fill owner repair execution handoff contains forbidden sensitive fragments")
    payload = json.loads(text)
    if payload.get("account_id") != PAPER_ACCOUNT_ID:
        raise HTTPException(status_code=409, detail="partial-fill owner repair execution handoff account_id mismatch")
    guard = payload.get("execution_guard") or {}
    for key in [
        "execution_allowed",
        "owner_repo_write_allowed_by_this_bundle",
        "owner_runtime_invocation_allowed_by_this_bundle",
        "runtime_retry_authorized_by_this_bundle",
    ]:
        if guard.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair execution handoff guard failed: {key}")
    if guard.get("requires_exact_owner_repair_approval") is not True:
        raise HTTPException(status_code=409, detail="partial-fill owner repair execution handoff missing approval requirement")
    steps = payload.get("operator_sequence_after_exact_approval") or []
    if len(steps) != 7 or any(item.get("execution_allowed_before_approval") is not False for item in steps):
        raise HTTPException(status_code=409, detail="partial-fill owner repair execution handoff sequence drifted")
    negative = payload.get("negative_assertions") or {}
    for key in [
        "execution_allowed",
        "owner_repo_write_attempted",
        "owner_patch_applied",
        "owner_validator_run_claimed",
        "owner_runtime_invocation_attempted",
        "runtime_retry_authorized",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        if negative.get(key) is not False:
            raise HTTPException(status_code=409, detail=f"partial-fill owner repair execution handoff negative assertion failed: {key}")
    return CommandPartialFillOwnerRepairExecutionHandoffBundle(**payload)


def register_legacy_command_read_routes(app: FastAPI) -> None:
    for path, response_model, loader in [
        (
            "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}",
            CommandRuntimeCloseout,
            load_runtime_closeout,
        ),
        (
            "/api/commands/accounts/{account_id}/runtime-invocation-readiness",
            CommandRuntimeInvocationReadiness,
            load_runtime_invocation_readiness,
        ),
        (
            "/api/commands/accounts/{account_id}/runtime-execution-approval-packet",
            CommandRuntimeExecutionApprovalPacket,
            load_runtime_execution_approval_packet,
        ),
        (
            "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle",
            CommandRuntimeExecutionHandoffBundle,
            load_runtime_execution_handoff_bundle,
        ),
        (
            "/api/commands/accounts/{account_id}/runtime-execution-gap-audit",
            CommandRuntimeExecutionGapAudit,
            load_runtime_execution_gap_audit,
        ),
    ]:
        app.add_api_route(
            path,
            loader,
            methods=["GET"],
            response_model=response_model,
            response_model_exclude_none=True,
        )
