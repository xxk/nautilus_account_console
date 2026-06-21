from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
PROPOSAL = ROOT / "docs" / "proposals" / "p024-account-console-paper-command-controls"
DESIGN_GATE = ROOT / "contracts" / "account_capability" / "command_capability_design_gate.json"
FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_capability"
P023_PARTIAL_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p023-openctp-19053-command"
    / "partial-fill-order-display.json"
)
P024_PARTIAL_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-cancel-order-display.json"
)
P024_RUNTIME_CLOSEOUT_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-closeout-ui.json"
)
P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-feasibility-audit.json"
)
P024_RUNTIME_HANDOFF_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-handoff-ui.json"
)
P024_RUNTIME_READINESS_UI_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-readiness-ui.json"
)
P024_RUNTIME_APPROVAL_PACKET_UI_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-approval-packet-ui.json"
)
P024_RUNTIME_HANDOFF_BUNDLE_UI_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-handoff-bundle-ui.json"
)
P024_RUNTIME_EXECUTION_GAP_UI_EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "runtime-execution-gap-audit-ui.json"
)
P024_OWNER_RUNTIME_READINESS = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-invocation-readiness.json"
)
P024_FULL_ACCEPTANCE_CLOSEOUT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "full-acceptance-closeout.json"
)
P024_OWNER_RUNTIME_APPROVAL_PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-approval-packet.json"
)
P024_OWNER_RUNTIME_HANDOFF_BUNDLE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-handoff-bundle.json"
)
P024_RUNTIME_EXECUTION_GAP_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "runtime-execution-gap-audit.json"
)
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"

REQUIRED_DOCS = [
    "README.md",
    "phase-plan.md",
    "acceptance.md",
    "ui-design.md",
    "ui-acceptance.md",
    "partial-fill-cancel-ui-acceptance.md",
    "runtime-invocation-readiness.md",
]

ALLOWED_COMMAND_ROUTES = {
    "/api/commands/accounts/{account_id}/submit-intents": {"POST"},
    "/api/commands/accounts/{account_id}/cancel-intents": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-run-requests/submit": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-run-requests/cancel": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-invocation-readiness": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-approval-packet": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle": {"GET"},
    "/api/commands/accounts/{account_id}/runtime-execution-gap-audit": {"GET"},
}


class P024ValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024ValidationError(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing json file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_docs_exist() -> None:
    for filename in REQUIRED_DOCS:
        require((PROPOSAL / filename).exists(), f"P024 missing {filename}")


def validate_proposal_index_and_adr() -> None:
    index = read(PROPOSAL_INDEX)
    require("P024 Account Console Paper Command Controls" in index, "proposal index missing P024")
    require("partial-fill then cancel Web UI display correctness" in index, "proposal index missing P024 partial-fill scope")
    require("owner-backed runtime closeout projection" in index, "proposal index missing P024 runtime closeout scope")
    require("owner-runtime handoff request evidence" in index, "proposal index missing P024 runtime handoff scope")
    require("owner-runtime invocation readiness" in index, "proposal index missing P024 runtime readiness scope")
    require("runtime readiness UI projection" in index, "proposal index missing P024 runtime readiness UI scope")
    require("residual blocker closeout audit" in index, "proposal index missing P024 closeout audit scope")
    require("owner-runtime execution approval packet" in index, "proposal index missing P024 approval packet scope")
    require("runtime approval packet UI projection" in index, "proposal index missing P024 approval packet UI scope")
    require("owner-runtime execution handoff bundle" in index, "proposal index missing P024 handoff bundle scope")
    require("runtime handoff bundle UI projection" in index, "proposal index missing P024 handoff bundle UI scope")
    require("runtime execution gap audit" in index, "proposal index missing P024 runtime execution gap scope")
    require(
        "real partial-fill runtime feasibility audit" in index,
        "proposal index missing P024 partial-fill feasibility scope",
    )

    adr = read(ADR)
    require("ADR-0007" in adr, "ADR-0007 missing")
    require("Second successor proposal: [P024 Account Console Paper Command Controls]" in adr, "ADR missing P024 successor")
    require("P024 Phase 1 backend command API" in adr, "ADR missing P024 next implementation work")
    require(
        "P024 Phase 3a runtime closeout projection is accepted as read-only Web UI evidence" in adr,
        "ADR missing P024 runtime closeout landing",
    )
    require(
        "P024 Phase 3c owner-runtime handoff request is accepted as browser handoff evidence only" in adr,
        "ADR missing P024 runtime handoff landing",
    )
    require(
        "P024 Phase 3d owner-runtime invocation readiness is accepted as a readiness gate only" in adr,
        "ADR missing P024 runtime readiness landing",
    )
    require(
        "P024 Phase 3e runtime readiness UI projection is accepted as browser blocker evidence only" in adr,
        "ADR missing P024 runtime readiness UI landing",
    )
    require(
        "P024 Phase 4 residual blocker audit is accepted as closeout evidence only" in adr,
        "ADR missing P024 full closeout audit landing",
    )
    require(
        "P024 Phase 4a owner-runtime execution approval packet is accepted as an approval-packet gate only" in adr,
        "ADR missing P024 approval packet landing",
    )
    require(
        "P024 Phase 4b runtime approval packet UI projection is accepted as browser blocker evidence only" in adr,
        "ADR missing P024 approval packet UI landing",
    )
    require(
        "P024 Phase 4c owner-runtime execution handoff bundle is accepted as a handoff gate only" in adr,
        "ADR missing P024 handoff bundle landing",
    )
    require(
        "P024 Phase 4d runtime handoff bundle UI projection is accepted as browser blocker evidence only" in adr,
        "ADR missing P024 handoff bundle UI landing",
    )
    require(
        "P024 Phase 4e runtime execution gap audit is accepted as final blocker evidence only" in adr,
        "ADR missing P024 runtime execution gap landing",
    )


def validate_readme() -> None:
    text = read(PROPOSAL / "README.md")
    for phrase in [
        "Proposal ID: `p024-account-console-paper-command-controls`",
        "Status: phase4h_real_partial_fill_runtime_feasibility_blocked",
        "ADR carrier: yes",
        "Primary ADR: ADR-0007",
        "Predecessor: [P023 OpenCTP 19053 Paper Command Capability]",
        "paper-only controls proposal",
        "No `live_armed` mode.",
        "No Account Mirror broker writer.",
        "partial-fill then cancel order-display correctness scenario",
        "validate_p024_paper_command_controls_design.py",
        "validate_p024_paper_command_api.py",
        "validate_p024_ui_command_controls_browser_evidence.py",
        "validate_p024_runtime_closeout_browser_evidence.py",
        "validate_p024_partial_fill_cancel_browser_evidence.py",
        "validate_p024_runtime_handoff_browser_evidence.py",
        "validate_p024_owner_runtime_invocation_readiness.py",
        "validate_p024_runtime_readiness_browser_evidence.py",
        "validate_p024_full_acceptance_closeout.py",
        "validate_p024_owner_runtime_execution_approval_packet.py",
        "validate_p024_runtime_approval_packet_browser_evidence.py",
        "validate_p024_owner_runtime_execution_handoff_bundle.py",
        "validate_p024_runtime_handoff_bundle_browser_evidence.py",
        "validate_p024_runtime_execution_gap_audit.py",
        "validate_p024_runtime_execution_gap_browser_evidence.py",
        "validate_p024_partial_fill_runtime_feasibility_audit.py",
        "browser_triggered_broker_order=false",
        "runtime_invocation_attempted=false",
        "owner-runtime invocation readiness",
        "runtime readiness UI projection",
        "full residual blocker closeout audit",
        "owner-runtime execution approval packet",
        "runtime approval packet UI projection",
        "owner-runtime execution handoff bundle",
        "runtime handoff bundle UI projection",
        "runtime execution gap audit",
        "real partial-fill runtime feasibility",
    ]:
        require(phrase in text, f"P024 README missing phrase: {phrase}")


def validate_phase_plan() -> None:
    text = read(PROPOSAL / "phase-plan.md")
    for phrase in [
        "Artifact Trust Boundary",
        "output/account_command/ctp-paper-19053/",
        "phase_1_backend_command_api",
        "phase_2_frontend_guarded_controls",
        "completed_browser_contract_gate",
        "phase_3_browser_paper_submit_cancel",
        "phase_3a_runtime_closeout_projection",
        "completed_browser_runtime_projection_gate",
        "phase_3b_partial_fill_cancel_ui_display",
        "completed_browser_display_gate",
        "phase_3c_owner_runtime_handoff_request",
        "completed_browser_handoff_gate",
        "phase_3d_owner_runtime_invocation_readiness",
        "completed_readiness_gate_blocked_by_external_approval",
        "phase_3e_runtime_readiness_ui_projection",
        "completed_browser_readiness_projection_gate",
        "phase_4_closeout",
        "completed_residual_blocker_audit",
        "phase_4a_owner_runtime_execution_approval_packet",
        "completed_approval_packet_gate_runtime_not_invoked",
        "phase_4b_runtime_approval_packet_ui_projection",
        "completed_browser_approval_packet_projection_gate",
        "phase_4c_owner_runtime_execution_handoff_bundle",
        "completed_handoff_bundle_gate_runtime_not_invoked",
        "phase_4d_runtime_handoff_bundle_ui_projection",
        "completed_browser_handoff_bundle_projection_gate",
        "phase_4e_runtime_execution_gap_audit",
        "completed_final_gap_audit_gate_blocked_by_owner_runtime_execution",
        "phase_4h_real_partial_fill_runtime_feasibility",
        "blocked_until_owner_runtime_partial_fill_state_available",
        "Runtime closeout projection",
        "Partial-fill cancel display",
        "Owner-runtime handoff request",
        "Owner-runtime invocation readiness",
        "Runtime readiness UI projection",
        "Phase 4 Closeout",
        "Phase 4h Real partial-fill runtime feasibility",
        "Phase 1 Backend command API",
        "completed_contract_gate",
        "validate_p024_paper_command_api.py",
        "validate_p024_runtime_closeout_browser_evidence.py",
        "validate_p024_partial_fill_cancel_browser_evidence.py",
        "validate_p024_runtime_handoff_browser_evidence.py",
        "validate_p024_owner_runtime_invocation_readiness.py",
        "validate_p024_runtime_readiness_browser_evidence.py",
        "validate_p024_full_acceptance_closeout.py",
        "validate_p024_owner_runtime_execution_approval_packet.py",
        "validate_p024_runtime_approval_packet_browser_evidence.py",
        "validate_p024_owner_runtime_execution_handoff_bundle.py",
        "validate_p024_runtime_handoff_bundle_browser_evidence.py",
        "validate_p024_partial_fill_runtime_feasibility_audit.py",
        "validate_p024_runtime_execution_gap_audit.py",
        "validate_p024_runtime_execution_gap_browser_evidence.py",
        "Browser controls are implemented only for `paper_armed` projection",
        "browser_triggered_broker_order=false",
        "Real partial-fill runtime remains blocked",
        "Web UI owner-runtime handoff requests are accepted only as typed requests",
        "Phase 3e readiness UI projection is complete",
        "Phase 4 residual blocker audit is complete",
        "Phase 4a owner-runtime execution approval packet is complete",
        "Phase 4b runtime approval packet UI projection is complete",
        "Phase 4c owner-runtime execution handoff bundle is complete",
        "Phase 4d runtime handoff bundle UI projection is complete",
        "Phase 4e runtime execution gap audit is complete",
        "external write approval",
    ]:
        require(phrase in text, f"P024 phase plan missing phrase: {phrase}")


def validate_acceptance() -> None:
    text = read(PROPOSAL / "acceptance.md")
    for phrase in [
        "P024_PAPER_COMMAND_CONTROLS_DESIGN_OK",
        "P024_PAPER_COMMAND_API_OK",
        "P024_UI_COMMAND_CONTROLS_BROWSER_EVIDENCE_OK",
        "P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK",
        "P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK",
        "P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK",
        "P024_OWNER_RUNTIME_INVOCATION_READINESS_OK",
        "P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK",
        "P024_FULL_ACCEPTANCE_CLOSEOUT_OK",
        "P024_OWNER_RUNTIME_EXECUTION_APPROVAL_PACKET_OK",
        "P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK",
        "P024_OWNER_RUNTIME_EXECUTION_HANDOFF_BUNDLE_OK",
        "P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK",
        "P024_RUNTIME_EXECUTION_GAP_AUDIT_OK",
        "P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK",
        "P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT_OK",
        "Implementation/browser evidence is required before implementation closeout",
        "UI Anti-Drift Acceptance",
        "forbidden_actions",
        "forbidden_claims",
        "Account Mirror remains read-only",
        "gateway ack alone is final",
        "live mode exposed",
        "A10",
        "Partial fill then cancel Web UI order display correctness",
        "Runtime closeout evidence appears in Web UI without browser-trigger claim",
        "Web UI prepares owner-runtime submit/cancel handoff without invoking broker runtime",
        "Owner-runtime invocation readiness and external approval scope are frozen",
        "Runtime readiness blocker appears in Web UI without broker execution claims",
        "S1 submitted/working",
        "S2 partially filled",
        "S3 cancel pending",
        "S4 remaining cancelled",
        "filled_quantity + remaining_quantity == submitted_quantity",
        "filled_quantity + cancelled_quantity == submitted_quantity",
        "account-order-identity",
        "account-cancel-pending-ref",
        "validate_p024_partial_fill_cancel_browser_evidence.py",
        "validate_p024_runtime_closeout_browser_evidence.py",
        "does not claim real partial-fill runtime",
        "browser_triggered_broker_order=false",
        "runtime_invocation_attempted=false",
        "blocked_until_owner_runtime_invocation",
        "owner_repo_write_attempted=false",
        "external owner-runtime approval",
        "Phase 3e Runtime Readiness UI Projection Acceptance",
        "Phase 4 Full Acceptance Closeout Audit",
        "phase4_residual_blocker_audit_passed",
        "accepted_with_residual_owner_runtime_blockers",
        "Phase 4a Owner Runtime Execution Approval Packet",
        "approval_packet_ready_runtime_not_invoked",
        "owner-runtime-execution-approval-packet.json",
        "Phase 4b Runtime Approval Packet UI Projection",
        "account-runtime-approval-packet-panel",
        "account-runtime-approval-packet-exact-text",
        "Phase 4c Owner Runtime Execution Handoff Bundle",
        "handoff_bundle_ready_runtime_not_invoked",
        "owner-runtime-execution-handoff-bundle.json",
        "Phase 4d Runtime Handoff Bundle UI Projection",
        "account-runtime-handoff-bundle-panel",
        "account-runtime-handoff-bundle-execution-allowed",
        "Phase 4e Runtime Execution Gap Audit",
        "Phase 4h Real Partial-Fill Runtime Feasibility Audit",
        "runtime-execution-gap-audit.json",
        "account-runtime-execution-gap-panel",
        "account-runtime-execution-gap-final-claimed",
        "account-runtime-readiness-panel",
        "account-runtime-readiness-invoked",
        "owner_repo_write_attempted=false",
        "Phase 1 Backend Command API Acceptance",
        "gateway_send_attempted=false",
        "accepted_for_risk",
        "Phase 2 Frontend Guarded Controls Acceptance",
        "paper_armed_controls_visible",
        "blocked_until_owner_runtime_partial_fill_state_available",
    ]:
        require(phrase in text, f"P024 acceptance missing phrase: {phrase}")


def validate_ui_docs() -> None:
    design = read(PROPOSAL / "ui-design.md")
    for phrase in [
        "Data Test ID",
        "account-submit-order-button",
        "account-cancel-order-button",
        "account-order-identity",
        "account-order-filled-quantity",
        "account-order-remaining-quantity",
        "account-order-cancelled-quantity",
        "account-order-partial-fill-row",
        "account-remaining-cancel-quantity",
        "account-cancel-pending-ref",
        "account-fill-source-ref",
        "account-command-reconciliation-ref",
        "account-runtime-closeout-panel",
        "account-runtime-closeout-web-trigger",
        "account-runtime-closeout-non-claim",
        "account-runtime-handoff-panel",
        "account-runtime-handoff-entrypoint",
        "account-runtime-handoff-invoked",
        "account-runtime-handoff-web-trigger",
        "account-runtime-readiness-panel",
        "account-runtime-readiness-status",
        "account-runtime-readiness-owner-path",
        "account-runtime-readiness-approval-obtained",
        "account-runtime-readiness-invoked",
        "account-runtime-readiness-owner-write",
        "account-runtime-readiness-browser-trigger",
        "account-runtime-readiness-blocker",
        "account-runtime-approval-packet-panel",
        "account-runtime-approval-packet-status",
        "account-runtime-approval-packet-owner-path",
        "account-runtime-approval-packet-obtained",
        "account-runtime-approval-packet-invoked",
        "account-runtime-approval-packet-owner-write",
        "account-runtime-approval-packet-broker-order",
        "account-runtime-approval-packet-exact-text",
        "account-runtime-approval-packet-entrypoint",
        "account-runtime-approval-packet-blocker",
        "account-runtime-handoff-bundle-panel",
        "account-runtime-handoff-bundle-status",
        "account-runtime-handoff-bundle-execution-allowed",
        "account-runtime-handoff-bundle-approval-obtained",
        "account-runtime-handoff-bundle-invoked",
        "account-runtime-handoff-bundle-owner-write",
        "account-runtime-handoff-bundle-broker-order",
        "account-runtime-handoff-bundle-input",
        "account-runtime-handoff-bundle-step",
        "account-runtime-handoff-bundle-artifact-count",
        "account-runtime-handoff-bundle-gate-count",
        "account-runtime-handoff-bundle-blocker",
        "account-runtime-execution-gap-panel",
        "account-runtime-execution-gap-status",
        "account-runtime-execution-gap-verdict",
        "account-runtime-execution-gap-final-claimed",
        "account-runtime-execution-gap-not-accepted",
        "account-runtime-execution-gap-approval-obtained",
        "account-runtime-execution-gap-invoked",
        "account-runtime-execution-gap-owner-write",
        "account-runtime-execution-gap-broker-order",
        "account-runtime-execution-gap-artifact-count",
        "account-runtime-execution-gap-required",
        "account-runtime-execution-gap-blocker",
        "After terminal cancel",
    ]:
        require(phrase in design, f"P024 UI design missing phrase: {phrase}")

    ui_acceptance = read(PROPOSAL / "ui-acceptance.md")
    for phrase in [
        "Browser Acceptance",
        "Negative UI Acceptance",
        "Blocker",
        "UI-09",
        "partial fill then cancel display correctness",
        "Same `account-order-identity`",
        "S4 cancelled quantity equals S2 remaining quantity",
        "Screenshots alone are not sufficient",
        "NUI-09",
        "UI-10",
        "runtime closeout projection",
        "account-runtime-closeout-panel",
        "account-runtime-closeout-web-trigger",
        "P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK",
        "phase3e_runtime_readiness_ui_projection_passed",
        "UI-11",
        "owner-runtime handoff request",
        "account-runtime-handoff-panel",
        "P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK",
        "UI-12",
        "runtime readiness blocker projection",
        "account-runtime-readiness-panel",
        "P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK",
        "UI-13",
        "runtime approval packet projection",
        "account-runtime-approval-packet-panel",
        "P024_RUNTIME_APPROVAL_PACKET_BROWSER_EVIDENCE_OK",
        "UI-14",
        "runtime handoff bundle projection",
        "account-runtime-handoff-bundle-panel",
        "P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK",
        "UI-15",
        "runtime execution gap audit projection",
        "account-runtime-execution-gap-panel",
        "P024_RUNTIME_EXECUTION_GAP_BROWSER_EVIDENCE_OK",
        "NUI-13",
        "NUI-14",
        "NUI-15",
    ]:
        require(phrase in ui_acceptance, f"P024 UI acceptance missing phrase: {phrase}")


def validate_partial_fill_cancel_doc() -> None:
    text = read(PROPOSAL / "partial-fill-cancel-ui-acceptance.md")
    for phrase in [
        "Proposal ID: `p024-account-console-paper-command-controls`",
        "Status: phase3b_partial_fill_cancel_ui_display_passed",
        "acct.ctp.paper.19053",
        "not turn screenshots, browser text or TickTrader UI state into order truth",
        "account-console.p024.partial-fill-cancel-ui-acceptance.v1",
        "same_order_identity_across_stages",
        "s2_browser_fill_sum_equals_order_filled_quantity",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "s3_quantities_unchanged_until_cancel_readback",
        "s3_cancel_pending_is_not_terminal",
        "s4_cancelled_quantity_equals_s2_remaining_quantity",
        "s4_remaining_quantity_zero",
        "fill_trade_identities_stable_after_cancel",
        "account-command-readback-ref",
        "account-command-reconciliation-ref",
        "does_not_use_screenshot_as_order_truth",
        "gateway_ack_is_not_final_state",
        "raw_secret_values_recorded=false",
        "P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK",
        "P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK",
        "typed_blocker_until_real_or_owner_approved_partial_fill_state",
    ]:
        require(phrase in text, f"P024 partial-fill cancel acceptance missing phrase: {phrase}")


def validate_p024_partial_fill_evidence() -> None:
    payload = load_json(P024_PARTIAL_EVIDENCE)
    require(
        payload["schema"] == "account-console.p024.partial-fill-cancel-ui-acceptance.v1",
        "P024 partial-fill schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 partial proposal mismatch")
    require(payload["partial_cancel_display_verdict"] == "pass", "P024 partial display verdict mismatch")
    require(
        payload["runtime_partial_fill_verdict"]
        == "typed_blocker_until_real_or_owner_approved_partial_fill_state",
        "P024 runtime partial-fill blocker missing",
    )
    checks = payload.get("partial_cancel_display_checks") or {}
    for check in [
        "same_order_identity_across_stages",
        "s2_browser_fill_sum_equals_order_filled_quantity",
        "s2_trade_refs_match_api_projection",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "s3_quantities_unchanged_until_cancel_readback",
        "s3_no_remaining_cancel_quantity_visible",
        "s3_cancel_pending_is_not_terminal",
        "s4_filled_quantity_preserved_after_cancel",
        "s4_cancelled_quantity_equals_s2_remaining_quantity",
        "s4_remaining_quantity_zero",
        "s4_no_remaining_cancel_quantity_visible",
        "fill_trade_identities_stable_after_cancel",
    ]:
        require(checks.get(check) is True, f"P024 partial display check missing: {check}")
    cancel = payload.get("cancel_request") or {}
    require(cancel.get("mode") == "paper_armed", "P024 partial cancel mode mismatch")
    require(cancel.get("venue_order_id") == "ctp19053-p024-partial-order-001", "P024 partial cancel identity mismatch")
    artifacts = payload.get("command_artifacts") or {}
    require(artifacts.get("gateway_ack_is_final_state") is False, "P024 partial gateway final flag mismatch")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_prove_real_openctp_partial_fill_runtime",
        "does_not_use_screenshot_as_order_truth",
        "does_not_claim_live_readiness",
        "gateway_ack_is_not_final_state",
    ]:
        require(claim in non_claims, f"P024 partial non-claim missing: {claim}")


def validate_p024_runtime_closeout_evidence() -> None:
    payload = load_json(P024_RUNTIME_CLOSEOUT_EVIDENCE)
    require(payload["schema"] == "account-console.p024.runtime-closeout-ui.v1", "P024 runtime schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 runtime proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 runtime account mismatch")
    require(payload["run_id"] == "p023-armed-20260621t0748z", "P024 runtime run id mismatch")
    require(payload["verdict"] == "pass", "P024 runtime verdict mismatch")
    require(payload["api_schema"] == "account_command.runtime_closeout.v1", "P024 runtime API schema mismatch")
    require(payload["api_status"] == "reconciled", "P024 runtime API status mismatch")
    require(payload["api_mode"] == "paper_armed", "P024 runtime API mode mismatch")
    require(payload["runtime_gateway_send_observed"] is True, "P024 runtime gateway send evidence missing")
    require(payload["broker_order_created"] is True, "P024 runtime broker order evidence missing")
    require(payload["browser_triggered_broker_order"] is False, "P024 runtime browser trigger non-claim missing")
    require(payload["gateway_ack_is_final_state"] is False, "P024 runtime gateway final flag mismatch")
    require(payload["raw_secret_values_recorded"] is False, "P024 runtime raw secret flag mismatch")
    require(payload["raw_broker_endpoint_recorded"] is False, "P024 runtime raw endpoint flag mismatch")
    require(payload["artifact_checksum_count"] >= 13, "P024 runtime artifact checksum count too low")
    checks = payload.get("browser_checks") or {}
    for check in [
        "runtime_panel_visible",
        "command_status_refs_visible",
        "browser_trigger_displayed_false",
        "gateway_final_displayed_false",
        "live_ready_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 runtime browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_send_broker_order_from_browser_read",
        "does_not_store_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_make_gateway_ack_final_state",
        "web_ui_trigger_of_new_runtime_order_still_pending",
    ]:
        require(claim in non_claims, f"P024 runtime non-claim missing: {claim}")


def validate_p024_runtime_handoff_evidence() -> None:
    payload = load_json(P024_RUNTIME_HANDOFF_EVIDENCE)
    require(payload["schema"] == "account-console.p024.runtime-handoff-ui.v1", "P024 handoff schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 handoff proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 handoff account mismatch")
    require(payload["verdict"] == "pass", "P024 handoff verdict mismatch")
    checks = payload.get("browser_checks") or {}
    for check in [
        "handoff_panel_visible",
        "submit_handoff_displayed",
        "cancel_handoff_displayed",
        "runtime_invocation_displayed_false",
        "browser_trigger_displayed_false",
        "live_ready_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 handoff browser check missing: {check}")
    for key, action, entrypoint in [
        ("submit_handoff", "submit", "ctp_guarded_paper_order_loop.py"),
        ("cancel_handoff", "cancel", "ctp_guarded_paper_cancel_loop.py"),
    ]:
        handoff = payload.get(key) or {}
        require(handoff.get("schema_version") == "account_command.owner_runtime_run_request.v1", f"{key}: schema mismatch")
        require(handoff.get("action") == action, f"{key}: action mismatch")
        require(handoff.get("status") == "blocked_until_owner_runtime_invocation", f"{key}: status mismatch")
        require(str(handoff.get("owner_runtime_entrypoint_ref")).endswith(entrypoint), f"{key}: entrypoint mismatch")
        require(handoff.get("runtime_invocation_attempted") is False, f"{key}: runtime invocation flag mismatch")
        require(handoff.get("browser_triggered_broker_order") is False, f"{key}: browser trigger flag mismatch")
        require(handoff.get("gateway_send_attempted") is False, f"{key}: gateway send flag mismatch")
        require(handoff.get("broker_order_created") is False, f"{key}: broker order flag mismatch")
        require(handoff.get("raw_secret_values_recorded") is False, f"{key}: raw secret flag mismatch")
        require(handoff.get("raw_broker_endpoint_recorded") is False, f"{key}: raw endpoint flag mismatch")
        require(len(handoff.get("blockers") or []) == 3, f"{key}: blocker count mismatch")
        non_claims = set(handoff.get("explicit_non_claims") or [])
        for claim in [
            "does_not_invoke_owner_runtime",
            "does_not_send_broker_order_from_browser",
            "does_not_store_raw_ctp_secret_or_endpoint",
            "does_not_claim_live_readiness",
            "does_not_make_gateway_ack_final_state",
        ]:
            require(claim in non_claims, f"{key}: missing non-claim {claim}")


def validate_p024_owner_runtime_readiness() -> None:
    payload = load_json(P024_OWNER_RUNTIME_READINESS)
    require(
        payload["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1",
        "P024 runtime readiness schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 readiness proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 readiness account mismatch")
    require(
        payload["status"] == "blocked_waiting_for_external_owner_runtime_write_approval",
        "P024 readiness status mismatch",
    )
    require(payload["verdict"] == "readiness_package_passed_runtime_not_invoked", "P024 readiness verdict mismatch")
    owner = payload["owner_runtime"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "P024 readiness owner mismatch")
    require(owner["config_raw_content_read"] is False, "P024 readiness config read flag mismatch")
    require(owner["raw_secret_values_recorded"] is False, "P024 readiness raw secret flag mismatch")
    require(owner["raw_broker_endpoint_recorded"] is False, "P024 readiness raw endpoint flag mismatch")
    entrypoints = {entry["action"]: entry for entry in payload["entrypoints"]}
    require(set(entrypoints) == {"submit", "cancel"}, "P024 readiness entrypoint action mismatch")
    require(entrypoints["submit"]["armed_flag"] == "--arm-paper-send", "P024 readiness submit arm flag mismatch")
    require(entrypoints["cancel"]["armed_flag"] == "--arm-cancel-send", "P024 readiness cancel arm flag mismatch")
    approval = payload["external_write_approval_request"]
    require(approval["required"] is True, "P024 readiness approval required mismatch")
    require(approval["obtained"] is False, "P024 readiness approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "P024 readiness approval path mismatch")
    negative = payload["negative_assertions"]
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
        require(negative[key] is False, f"P024 readiness negative assertion mismatch: {key}")
    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_send_broker_order_from_browser",
        "does_not_write_owner_repo",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_phase_3_runtime_execution",
    ]:
        require(claim in non_claims, f"P024 readiness missing non-claim: {claim}")


def validate_p024_runtime_readiness_ui_evidence() -> None:
    payload = load_json(P024_RUNTIME_READINESS_UI_EVIDENCE)
    require(payload["schema"] == "account-console.p024.runtime-readiness-ui.v1", "P024 readiness UI schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 readiness UI proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 readiness UI account mismatch")
    require(payload["verdict"] == "pass", "P024 readiness UI verdict mismatch")
    readiness = payload["api_readiness"]
    require(
        readiness["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1",
        "P024 readiness UI API schema mismatch",
    )
    require(
        readiness["status"] == "blocked_waiting_for_external_owner_runtime_write_approval",
        "P024 readiness UI status mismatch",
    )
    require(readiness["owner_ref"] == "owner://nautilus_ctp_adapter", "P024 readiness UI owner mismatch")
    require(readiness["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "P024 readiness UI path mismatch")
    require(readiness["config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", "P024 readiness UI config mismatch")
    require(readiness["config_raw_content_read"] is False, "P024 readiness UI raw config read flag mismatch")
    require(readiness["approval_required"] is True, "P024 readiness UI approval required mismatch")
    require(readiness["approval_obtained"] is False, "P024 readiness UI approval obtained mismatch")
    require(readiness["entrypoint_count"] == 2, "P024 readiness UI entrypoint count mismatch")
    require(readiness["blocker_count"] == 2, "P024 readiness UI blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(readiness[key] is False, f"P024 readiness UI negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "readiness_panel_visible",
        "owner_ref_displayed",
        "owner_path_displayed",
        "config_ref_displayed_without_raw_endpoint",
        "approval_required_displayed_true",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "browser_trigger_displayed_false",
        "raw_secret_displayed_false",
        "entrypoints_displayed",
        "blockers_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 readiness UI browser check missing: {check}")
    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_send_broker_order_from_browser",
        "does_not_write_owner_repo",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_phase_3_runtime_execution",
    ]:
        require(claim in non_claims, f"P024 readiness UI missing non-claim: {claim}")


def validate_p024_runtime_approval_packet_ui_evidence() -> None:
    payload = load_json(P024_RUNTIME_APPROVAL_PACKET_UI_EVIDENCE)
    require(
        payload["schema"] == "account-console.p024.runtime-approval-packet-ui.v1",
        "P024 approval packet UI schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 approval UI proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 approval UI account mismatch")
    require(payload["verdict"] == "pass", "P024 approval UI verdict mismatch")
    packet = payload["api_approval_packet"]
    require(
        packet["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1",
        "P024 approval UI API schema mismatch",
    )
    require(
        packet["status"] == "phase4a_owner_runtime_execution_approval_packet_ready",
        "P024 approval UI status mismatch",
    )
    require(packet["verdict"] == "approval_packet_ready_runtime_not_invoked", "P024 approval UI verdict mismatch")
    require(packet["approval_required"] is True, "P024 approval UI required mismatch")
    require(packet["approval_obtained"] is False, "P024 approval UI obtained mismatch")
    require(packet["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "P024 approval UI path mismatch")
    require(packet["exact_approval_text_present"] is True, "P024 approval UI exact text missing")
    require(packet["entrypoint_count"] == 2, "P024 approval UI entrypoint count mismatch")
    require(packet["blocker_count"] == 2, "P024 approval UI blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(packet[key] is False, f"P024 approval UI negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "approval_packet_panel_visible",
        "owner_path_displayed",
        "exact_approval_text_displayed",
        "approval_required_displayed_true",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "broker_order_displayed_false",
        "entrypoints_displayed",
        "blockers_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 approval UI browser check missing: {check}")


def validate_p024_runtime_handoff_bundle_ui_evidence() -> None:
    payload = load_json(P024_RUNTIME_HANDOFF_BUNDLE_UI_EVIDENCE)
    require(
        payload["schema"] == "account-console.p024.runtime-handoff-bundle-ui.v1",
        "P024 handoff bundle UI schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 handoff UI proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 handoff UI account mismatch")
    require(payload["verdict"] == "pass", "P024 handoff UI verdict mismatch")
    bundle = payload["api_handoff_bundle"]
    require(
        bundle["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1",
        "P024 handoff UI API schema mismatch",
    )
    require(
        bundle["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready",
        "P024 handoff UI API status mismatch",
    )
    require(bundle["verdict"] == "handoff_bundle_ready_runtime_not_invoked", "P024 handoff UI API verdict mismatch")
    require(bundle["execution_allowed"] is False, "P024 handoff UI execution allowed mismatch")
    require(bundle["approval_required"] is True, "P024 handoff UI approval required mismatch")
    require(bundle["approval_obtained"] is False, "P024 handoff UI approval obtained mismatch")
    require(bundle["runtime_input_count"] == 7, "P024 handoff UI input count mismatch")
    require(bundle["operator_step_count"] == 7, "P024 handoff UI step count mismatch")
    require(bundle["required_owner_artifact_count"] == 14, "P024 handoff UI artifact count mismatch")
    require(bundle["post_handoff_gate_count"] == 6, "P024 handoff UI gate count mismatch")
    require(bundle["blocker_count"] == 3, "P024 handoff UI blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(bundle[key] is False, f"P024 handoff UI negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "handoff_bundle_panel_visible",
        "execution_allowed_displayed_false",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "broker_order_displayed_false",
        "runtime_inputs_displayed",
        "operator_sequence_displayed",
        "required_artifact_count_displayed",
        "post_handoff_gate_count_displayed",
        "blockers_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 handoff UI browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_create_broker_order",
        "does_not_guess_runtime_inputs",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_real_runtime_execution",
    ]:
        require(claim in non_claims, f"P024 handoff UI missing non-claim: {claim}")


def validate_p024_runtime_execution_gap_audit() -> None:
    payload = load_json(P024_RUNTIME_EXECUTION_GAP_AUDIT)
    require(
        payload["schema"] == "account-console.p024.runtime-execution-gap-audit.v1",
        "P024 execution gap schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 execution gap proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 execution gap account mismatch")
    require(payload["status"] == "phase4e_final_runtime_execution_gap_audited", "P024 execution gap status mismatch")
    require(payload["verdict"] == "blocked_pending_owner_runtime_execution", "P024 execution gap verdict mismatch")
    require(set(payload["accepted_scenarios"]) == {f"A{index}" for index in range(1, 17)} - {"A4", "A16"}, "P024 execution gap accepted scenario mismatch")
    not_accepted = {item["id"]: item for item in payload["not_accepted_scenarios"]}
    require(set(not_accepted) == {"A4"}, "P024 execution gap not accepted scenario mismatch")
    require(not_accepted["A4"]["current_status"] == "blocked_pending_owner_runtime_execution", "P024 execution gap A4 status mismatch")
    approval = payload["external_write_approval"]
    require(approval["required"] is True, "P024 execution gap approval required mismatch")
    require(approval["obtained"] is False, "P024 execution gap approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "P024 execution gap approval path mismatch")
    require(len(payload["required_before_goal_complete"]) == 8, "P024 execution gap required-before count mismatch")
    require(len(payload["required_owner_artifacts"]) == 14, "P024 execution gap artifact count mismatch")
    blockers = {blocker["blocker_id"] for blocker in payload["residual_blockers"]}
    require(
        blockers
        == {
            "p024_external_owner_runtime_write_approval_required",
            "p024_owner_runtime_artifacts_missing",
            "p024_real_partial_fill_runtime_missing",
        },
        "P024 execution gap blocker mismatch",
    )
    negative = payload["negative_assertions"]
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
        require(negative[key] is False, f"P024 execution gap negative assertion mismatch: {key}")


def validate_p024_runtime_execution_gap_ui_evidence() -> None:
    payload = load_json(P024_RUNTIME_EXECUTION_GAP_UI_EVIDENCE)
    require(
        payload["schema"] == "account-console.p024.runtime-execution-gap-audit-ui.v1",
        "P024 execution gap UI schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 execution gap UI proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 execution gap UI account mismatch")
    require(payload["verdict"] == "pass", "P024 execution gap UI verdict mismatch")
    audit = payload["api_gap_audit"]
    require(audit["schema"] == "account-console.p024.runtime-execution-gap-audit.v1", "P024 execution gap UI API schema mismatch")
    require(audit["status"] == "phase4e_final_runtime_execution_gap_audited", "P024 execution gap UI API status mismatch")
    require(audit["verdict"] == "blocked_pending_owner_runtime_execution", "P024 execution gap UI API verdict mismatch")
    require(audit["accepted_scenario_count"] == 14, "P024 execution gap UI accepted count mismatch")
    require(audit["not_accepted_scenario_count"] == 1, "P024 execution gap UI not accepted count mismatch")
    require(audit["required_before_goal_complete_count"] == 8, "P024 execution gap UI required-before count mismatch")
    require(audit["required_owner_artifact_count"] == 14, "P024 execution gap UI artifact count mismatch")
    require(audit["blocker_count"] == 3, "P024 execution gap UI blocker count mismatch")
    for key in [
        "final_acceptance_claimed",
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(audit[key] is False, f"P024 execution gap UI negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "gap_panel_visible",
        "verdict_displayed_blocked",
        "final_acceptance_claimed_displayed_false",
        "a4_not_accepted_displayed",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "broker_order_displayed_false",
        "required_items_displayed",
        "blocker_items_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"P024 execution gap UI browser check missing: {check}")


def validate_p024_full_acceptance_closeout() -> None:
    payload = load_json(P024_FULL_ACCEPTANCE_CLOSEOUT)
    require(payload["schema"] == "account-console.p024.full-acceptance-closeout.v1", "P024 closeout schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 closeout proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 closeout account mismatch")
    require(payload["status"] == "phase4_residual_blocker_audit_passed", "P024 closeout status mismatch")
    require(
        payload["verdict"] == "accepted_with_residual_owner_runtime_blockers",
        "P024 closeout verdict mismatch",
    )
    scenarios = {item["id"]: item for item in payload["scenario_matrix"]}
    require(set(scenarios) == {f"A{index}" for index in range(1, 17)}, "P024 closeout scenario set mismatch")
    require(
        scenarios["A4"]["status"] == "blocked_pending_owner_runtime_execution",
        "P024 closeout A4 must remain blocked",
    )
    require(
        scenarios["A13"]["status"] == "passed_blocked_by_external_approval",
        "P024 closeout A13 status mismatch",
    )
    require(scenarios["A15"]["status"] == "passed", "P024 closeout A15 status mismatch")
    require(
        scenarios["A16"]["status"] == "passed_blocked_by_owner_runtime_execution",
        "P024 closeout A16 status mismatch",
    )
    blockers = {blocker["blocker_id"]: blocker for blocker in payload["residual_blockers"]}
    require(
        set(blockers)
        == {
            "p024_external_owner_runtime_write_approval_required",
            "p024_owner_runtime_artifacts_missing",
            "p024_real_partial_fill_runtime_missing",
        },
        "P024 closeout residual blockers mismatch",
    )
    negative = payload["negative_assertions"]
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted_from_browser",
        "broker_order_created_from_browser",
        "live_armed",
        "account_mirror_write_authority",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "full_runtime_acceptance_claimed",
    ]:
        require(negative[key] is False, f"P024 closeout negative assertion mismatch: {key}")


def validate_p024_partial_fill_runtime_feasibility_audit() -> None:
    payload = load_json(P024_PARTIAL_FILL_RUNTIME_FEASIBILITY_AUDIT)
    require(
        payload["schema"] == "account-console.p024.partial-fill-runtime-feasibility-audit.v1",
        "P024 partial-fill feasibility schema mismatch",
    )
    require(
        payload["proposal_id"] == "p024-account-console-paper-command-controls",
        "P024 partial-fill feasibility proposal mismatch",
    )
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 partial-fill feasibility account mismatch")
    require(
        payload["status"] == "phase4h_real_partial_fill_runtime_feasibility_blocked",
        "P024 partial-fill feasibility status mismatch",
    )
    require(
        payload["verdict"] == "blocked_until_owner_runtime_partial_fill_state_available",
        "P024 partial-fill feasibility verdict mismatch",
    )
    approval = payload["operator_approval_scope"]
    require(approval["approved_for_one_submit_cancel_attempt"] is True, "P024 partial-fill approval scope mismatch")
    require(approval["additional_partial_fill_order_authorized"] is False, "P024 partial-fill extra order mismatch")
    evidence = payload["current_real_runtime_evidence"]
    require(evidence["observed_trade_fill"] is False, "P024 partial-fill trade fill claim mismatch")
    require(evidence["observed_partial_fill"] is False, "P024 partial-fill runtime claim mismatch")
    scan = payload["owner_capability_scan"]
    require(scan["can_record_trade_callbacks_if_emitted"] is True, "P024 partial-fill callback capability missing")
    require(
        scan["deterministic_partial_fill_generator_present"] is False,
        "P024 partial-fill generator claim mismatch",
    )
    require(
        payload["non_ui_acceptance_shape"]["status"] == "blocked",
        "P024 partial-fill non-UI acceptance status mismatch",
    )
    require(
        payload["web_ui_acceptance_shape"]["status"] == "blocked",
        "P024 partial-fill Web UI acceptance status mismatch",
    )
    require(
        payload["residual_blocker"]["blocker_id"] == "p024_real_partial_fill_runtime_missing",
        "P024 partial-fill blocker mismatch",
    )
    negative = payload["negative_assertions"]
    for key in [
        "new_partial_fill_order_submitted_by_this_audit",
        "final_acceptance_claimed",
        "real_partial_fill_runtime_claimed",
        "browser_fixture_promoted_to_runtime_truth",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"P024 partial-fill negative assertion mismatch: {key}")


def validate_p024_owner_runtime_approval_packet() -> None:
    payload = load_json(P024_OWNER_RUNTIME_APPROVAL_PACKET)
    require(
        payload["schema"] == "account-console.p024.owner-runtime-execution-approval-packet.v1",
        "P024 approval packet schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 approval proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 approval account mismatch")
    require(
        payload["status"] == "phase4a_owner_runtime_execution_approval_packet_ready",
        "P024 approval packet status mismatch",
    )
    require(
        payload["verdict"] == "approval_packet_ready_runtime_not_invoked",
        "P024 approval packet verdict mismatch",
    )
    approval = payload["required_operator_approval"]
    require(approval["required"] is True, "P024 approval required flag mismatch")
    require(approval["obtained"] is False, "P024 approval obtained flag mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "P024 approval path mismatch")
    require(
        "I approve writes to D:/Nautilus/nautilus_ctp_adapter" in approval["exact_approval_text"],
        "P024 exact approval text missing path",
    )
    entrypoints = {entry["action"]: entry for entry in payload["entrypoints"]}
    require(set(entrypoints) == {"submit", "cancel"}, "P024 approval entrypoint action mismatch")
    require(entrypoints["submit"]["armed_flag"] == "--arm-paper-send", "P024 approval submit arm flag mismatch")
    require(entrypoints["cancel"]["armed_flag"] == "--arm-cancel-send", "P024 approval cancel arm flag mismatch")
    commands = {command["action"]: command for command in payload["command_templates"]}
    require("--arm-paper-send" in commands["submit"]["template"], "P024 approval submit command missing arm flag")
    require("--arm-cancel-send" in commands["cancel"]["template"], "P024 approval cancel command missing arm flag")
    artifacts = set(payload["required_post_run_artifacts"])
    for artifact in [
        "submit_intent.json",
        "submit_gateway_event.json",
        "post_submit_readback.json",
        "cancel_intent.json",
        "cancel_gateway_event.json",
        "post_cancel_readback.json",
        "reconciliation_result.json",
        "redaction_report.json",
        "command_audit.json",
        "closeout_manifest.json",
    ]:
        require(artifact in artifacts, f"P024 approval packet missing artifact: {artifact}")
    negative = payload["negative_assertions"]
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
        require(negative[key] is False, f"P024 approval packet negative assertion mismatch: {key}")


def validate_p024_owner_runtime_handoff_bundle() -> None:
    payload = load_json(P024_OWNER_RUNTIME_HANDOFF_BUNDLE)
    require(
        payload["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1",
        "P024 handoff bundle schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "P024 handoff bundle proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "P024 handoff bundle account mismatch")
    require(
        payload["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready",
        "P024 handoff bundle status mismatch",
    )
    require(
        payload["verdict"] == "handoff_bundle_ready_runtime_not_invoked",
        "P024 handoff bundle verdict mismatch",
    )
    guard = payload["execution_guard"]
    require(guard["execution_allowed"] is False, "P024 handoff bundle execution allowed mismatch")
    require(guard["approval_required"] is True, "P024 handoff bundle approval required mismatch")
    require(guard["approval_obtained"] is False, "P024 handoff bundle approval obtained mismatch")
    required_inputs = {item["field"] for item in payload["runtime_input_requirements"]}
    for field in [
        "owner_pre_snapshot_ref",
        "owner_post_snapshot_ref",
        "instrument",
        "side",
        "qty",
        "price",
        "readback_order_identity",
    ]:
        require(field in required_inputs, f"P024 handoff bundle missing runtime input: {field}")
    steps = [item["step"] for item in payload["operator_sequence"]]
    for step in [
        "pre_approval_gate",
        "owner_repo_context",
        "submit_runtime",
        "submit_readback",
        "cancel_runtime",
        "post_run_ingest",
        "browser_closeout",
    ]:
        require(step in steps, f"P024 handoff bundle missing operator step: {step}")
    blockers = {blocker["type"] for blocker in payload["blockers"]}
    require(
        blockers == {"external_write_approval_required", "runtime_inputs_required", "owner_runtime_artifacts_missing"},
        "P024 handoff bundle blockers mismatch",
    )
    negative = payload["negative_assertions"]
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
        require(negative[key] is False, f"P024 handoff bundle negative assertion mismatch: {key}")


def validate_owner_map_backfill() -> None:
    owner_map = read(OWNER_MAP)
    for phrase in [
        "P024 paper command controls",
        "owner://nautilus_ctp_adapter",
        "external approval blocker",
        "claim browser-triggered broker order",
        "Account Mirror a command writer",
    ]:
        require(phrase in owner_map, f"P024 owner map missing phrase: {phrase}")


def validate_p023_predecessor_evidence() -> None:
    payload = load_json(P023_PARTIAL_EVIDENCE)
    require(payload["schema"] == "account-console.p023.partial-fill-order-display.v1", "P023 evidence schema mismatch")
    require(payload["partial_cancel_display_verdict"] == "pass", "P023 partial cancel display verdict mismatch")
    require(
        payload["runtime_partial_fill_verdict"]
        == "typed_blocker_until_real_or_owner_approved_partial_fill_state",
        "P023 runtime partial-fill blocker missing",
    )
    checks = payload.get("partial_cancel_display_checks") or {}
    for check in [
        "same_order_identity_across_stages",
        "s2_browser_fill_sum_equals_order_filled_quantity",
        "s2_trade_refs_match_api_projection",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "s3_quantities_unchanged_until_cancel_readback",
        "s3_no_remaining_cancel_quantity_visible",
        "s4_filled_quantity_preserved_after_cancel",
        "s4_cancelled_quantity_equals_s2_remaining_quantity",
        "s4_remaining_quantity_zero",
        "s4_no_remaining_cancel_quantity_visible",
        "fill_trade_identities_stable_after_cancel",
    ]:
        require(checks.get(check) is True, f"P023 predecessor check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_submit_orders",
        "does_not_cancel_orders",
        "does_not_prove_real_openctp_partial_fill_runtime",
        "does_not_use_screenshot_as_order_truth",
        "does_not_enable_command_capability",
    ]:
        require(claim in non_claims, f"P023 predecessor non-claim missing: {claim}")


def validate_existing_command_boundary_still_closed() -> None:
    design_gate = load_json(DESIGN_GATE)
    require(design_gate["status"] == "design_gate_only", "existing command design gate must remain design_gate_only")
    current = design_gate["current_phase"]
    for key in [
        "command_implementation_accepted",
        "ui_command_controls_accepted",
        "account_mirror_write_authority",
        "broker_gateway_implementation_accepted",
    ]:
        require(current[key] is False, f"{key} must remain false in P024 design gate")

    for path in sorted(FIXTURE_DIR.glob("acct_*_capability.json")):
        payload = load_json(path)
        command = payload["capabilities"]["command"]
        require(command["enabled"] is False, f"{path}: command must stay disabled")
        require(command["mode"] == "disabled", f"{path}: command mode must stay disabled")
        require(command["allowed_actions"] == [], f"{path}: command allowed_actions must stay empty")
        require(payload["boundaries"]["order_action"] is False, f"{path}: order_action boundary must stay false")


def validate_backend_command_routes_are_p024_only() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route_paths = {getattr(route, "path", "") for route in app.routes}
    require(set(ALLOWED_COMMAND_ROUTES).issubset(route_paths), "P024 command API routes missing")
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        if path in ALLOWED_COMMAND_ROUTES:
            require(methods == ALLOWED_COMMAND_ROUTES[path], f"{path}: P024 command route methods mismatch")
        elif path.startswith("/api/commands"):
            require(False, f"unexpected command route outside P024 allowlist: {path}")
        require("/replace" not in path, f"replace route remains forbidden in P024: {path}")
        if path.startswith("/api/mirror/"):
            forbidden_methods = sorted(method for method in methods if method not in {"GET", "HEAD"})
            require(not forbidden_methods, f"mirror route {path} exposes write methods: {forbidden_methods}")


def main() -> None:
    validate_docs_exist()
    validate_proposal_index_and_adr()
    validate_readme()
    validate_phase_plan()
    validate_acceptance()
    validate_ui_docs()
    validate_partial_fill_cancel_doc()
    validate_p024_partial_fill_evidence()
    validate_p024_runtime_closeout_evidence()
    validate_p024_runtime_handoff_evidence()
    validate_p024_owner_runtime_readiness()
    validate_p024_runtime_readiness_ui_evidence()
    validate_p024_runtime_approval_packet_ui_evidence()
    validate_p024_runtime_handoff_bundle_ui_evidence()
    validate_p024_runtime_execution_gap_audit()
    validate_p024_runtime_execution_gap_ui_evidence()
    validate_p024_full_acceptance_closeout()
    validate_p024_partial_fill_runtime_feasibility_audit()
    validate_p024_owner_runtime_approval_packet()
    validate_p024_owner_runtime_handoff_bundle()
    validate_owner_map_backfill()
    validate_p023_predecessor_evidence()
    validate_existing_command_boundary_still_closed()
    validate_backend_command_routes_are_p024_only()
    print(
        "P024_PAPER_COMMAND_CONTROLS_DESIGN_OK: "
        "status=phase4h_real_partial_fill_runtime_feasibility_blocked current_ui_command=guarded runtime_closeout=browser_projection_passed partial_fill_cancel_ui=browser_contract_passed runtime_handoff=browser_handoff_passed runtime_invocation_readiness=blocked_by_external_approval runtime_readiness_ui=browser_projection_passed full_closeout=residual_blocker_audit_passed approval_packet=ready_runtime_not_invoked runtime_approval_packet_ui=browser_projection_passed handoff_bundle=ready_runtime_not_invoked runtime_handoff_bundle_ui=browser_projection_passed runtime_execution_gap=blocked_final_claim_false partial_fill_runtime=blocked_until_owner_runtime_partial_fill_state_available"
    )


if __name__ == "__main__":
    main()
