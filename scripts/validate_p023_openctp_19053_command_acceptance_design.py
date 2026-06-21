from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"
PROPOSAL = ROOT / "docs" / "proposals" / "p023-openctp-19053-paper-command-capability"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
CONTRACT_DIR = ROOT / "contracts" / "account_command"


class P023ValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P023ValidationError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_adr_link() -> None:
    text = read(ADR)
    for phrase in [
        "P023 OpenCTP 19053 Paper Command Capability Acceptance Design",
        "OpenCTP 19053 7x24 Paper",
        "The 7x24 property means the paper counter",
        "does not imply live readiness",
        "P023 may use small quantity",
    ]:
        require(phrase in text, f"ADR-0007 missing P023 landing phrase: {phrase}")


def validate_proposal_docs() -> None:
    required_files = [
        "README.md",
        "phase-plan.md",
        "acceptance.md",
        "ui-acceptance.md",
        "ui-design.md",
        "live-trading-scenarios.md",
        "non-ui-acceptance.md",
        "web-ui-acceptance.md",
    ]
    for filename in required_files:
        require((PROPOSAL / filename).exists(), f"P023 missing {filename}")

    readme = read(PROPOSAL / "README.md")
    for phrase in [
        "Proposal ID: `p023-openctp-19053-paper-command-capability`",
        "ADR carrier: yes",
        "Primary ADR: ADR-0007",
        "OpenCTP TTS 7x24 simulation",
        "This proposal does not enable Account Console web/API command controls.",
        "live-trading-scenarios.md",
        "Live Scenario Coverage",
        "validate_p023_account_command_contracts.py",
        "validate_p023_openctp19053_command_run.py",
        "Account Mirror as broker writer",
        "P023 paper runtime is accepted",
        "submit idempotency replay contract-lock evidence",
        "Phase 6 UI command status evidence",
        "validate_p023_ui_status_browser_evidence.py",
    ]:
        require(phrase in readme, f"P023 README missing {phrase}")

    phase_plan = read(PROPOSAL / "phase-plan.md")
    for phrase in [
        "Phase 4 | OpenCTP 19053 paper submit",
        "Phase 5 | OpenCTP 19053 paper cancel",
        "Phase 5b | OpenCTP 19053 partial-fill lifecycle",
        "completed_contract_gate",
        "completed_disabled_gate",
        "completed_dry_run",
        "completed_paper_submit",
        "completed_paper_cancel",
        "designed_runtime_blocker_until_partial_state",
        "ui_status_evidence_accepted_command_controls_disabled",
        "UI Command Status Evidence",
        "ui-status-evidence.json",
        "gateway-ack-only negative stage",
        "Submit Idempotency Replay Contract",
        "submit_idempotency_replay_valid.json",
        "runtime_duplicate_send_attempted=false",
        "ReqQryOrder",
        "Partial-Fill Runtime Sequence",
        "partial_fill_reconciliation_result.json",
        "ADR Decision Coverage Mapping",
        "Gateway ack is not final account state",
    ]:
        require(phrase in phase_plan, f"P023 phase plan missing {phrase}")

    acceptance = read(PROPOSAL / "acceptance.md")
    for phrase in [
        "P023_OPENCTP_19053_COMMAND_ACCEPTANCE_DESIGN_OK",
        "P023_ACCOUNT_COMMAND_CONTRACTS_OK",
        "P023_OPENCTP19053_COMMAND_RUN_OK",
        "P023_UI_STATUS_BROWSER_EVIDENCE_OK",
        "P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK",
        "validate_p023_ui_status_browser_evidence.py",
        "partial_cancel_display=pass",
        "validate_p023_account_command_contracts.py",
        "validate_p023_openctp19053_command_run.py",
        "validate_p023_partial_fill_browser_evidence.py",
        "contract_gate_ready",
        "runtime_accepted",
        "19053 7x24 paper preflight ready",
        "Paper submit accepted by gateway",
        "contract_lock_ready_runtime_duplicate_not_sent",
        "account_command.submit_idempotency_replay.v1",
        "runtime_duplicate_send_attempted=false",
        "same broker order identity",
        "Paper cancel uses readback identity",
        "Post-cancel readback reconciles",
        "browser_status_evidence_ready_command_controls_disabled",
        "account-console.p023.ui-status-evidence.v1",
        "gateway-ack-only state as blocked",
        "command_controls_enabled=false",
        "Partial fill then cancel",
        "designed_runtime_blocker_until_partial_state",
        "browser_order_display_contract_ready_runtime_blocked",
        "partial_cancel_display_verdict=pass",
        "Gateway ack treated as final order state",
        "Partial fill quantity or remaining quantity cannot be traced to broker readback",
        "Paper 7x24 evidence claims live readiness",
        "output/account_command/ctp-paper-19053/<run-id>/",
        "partial_fill_readback.json",
        "partial_fill_reconciliation_result.json",
        "gateway_ack_is_final_state=false",
        "partial_fill=true",
        "remaining_quantity_cancelled",
        "filled_quantity + remaining_quantity == submitted_quantity",
        "live-trading-scenarios.md",
        "LT-01",
        "LT-30",
        "non-ui-acceptance.md",
        "web-ui-acceptance.md",
    ]:
        require(phrase in acceptance, f"P023 acceptance missing {phrase}")

    live_scenarios = read(PROPOSAL / "live-trading-scenarios.md")
    for phrase in [
        "Scenario Groups",
        "Detailed Scenarios",
        "19053 Paper Acceptance Subset",
        "Live Blocked Until",
        "LT-01",
        "LT-08",
        "LT-11",
        "LT-14",
        "LT-14 Partial Fill Acceptance Detail",
        "partial_fill=true",
        "remaining_quantity_cancelled",
        "filled_quantity + remaining_quantity == submitted_quantity",
        "Duplicate trade rows",
        "LT-20",
        "LT-29",
        "LT-30",
        "7x24 paper lane",
        "live_armed",
        "raw password/front/auth/token",
        "gateway ack marked final",
        "duplicate broker orders appear",
        "Cancel open order",
        "Post-session closeout",
    ]:
        require(phrase in live_scenarios, f"P023 live scenario catalog missing {phrase}")

    non_ui = read(PROPOSAL / "non-ui-acceptance.md")
    for phrase in [
        "Non-UI Scenario Matrix",
        "Required Non-UI Artifact Family",
        "G1 Pre-trade readiness",
        "G2 Submit",
        "G3 Cancel",
        "G4 Fill lifecycle",
        "G5 Reject/block",
        "G6 Connectivity",
        "G7 Session conflict",
        "G8 Emergency controls",
        "G9 Audit/reconciliation",
        "G10 UI safety backend state",
        "NU-01",
        "NU-14",
        "NU-15",
        "Submit Idempotency Non-UI Acceptance",
        "validate_submit_idempotency_replay",
        "same_broker_order_identity=true",
        "duplicate_broker_order_created=false",
        "runtime_duplicate_send_attempted=false",
        "Partial Fill Non-UI Acceptance",
        "NUN-01",
        "NUN-12",
        "NUN-13",
        "NUN-15",
        "validate_partial_fill_then_cancel_reconciliation",
        "validate_command_audit_chain",
        "validate_command_redaction",
    ]:
        require(phrase in non_ui, f"P023 non-UI acceptance missing {phrase}")

    web_ui = read(PROPOSAL / "web-ui-acceptance.md")
    for phrase in [
        "Web UI Scenario Matrix",
        "Required Web UI Evidence",
        "Required Data Test IDs",
        "G1 Pre-trade readiness",
        "G2 Submit",
        "G3 Cancel",
        "G4 Fill lifecycle",
        "G5 Reject/block",
        "G6 Connectivity",
        "G7 Session conflict",
        "G8 Emergency controls",
        "G9 Audit/reconciliation",
        "G10 UI safety",
        "`account-submit-order-button`",
        "`account-cancel-order-button`",
        "`account-command-reconciliation-ref`",
        "ui-status-evidence.json",
        "command-status-reconciled.png",
        "command-status-blocked.png",
        "partial-fill-order-display.json",
        "`account-order-identity`",
        "`account-order-status`",
        "`account-order-submitted-quantity`",
        "`account-order-filled-quantity`",
        "`account-order-remaining-quantity`",
        "`account-order-cancelled-quantity`",
        "`account-order-partial-fill-row`",
        "`account-fill-source-ref`",
        "`account-fill-quantity`",
        "`account-fill-price`",
        "`account-remaining-cancel-quantity`",
        "`account-cancel-pending-ref`",
        "UI-01",
        "UI-12",
        "UI-13",
        "UI-09 Command Status Evidence",
        "account-command-gateway-final-state=invalid",
        "validate_p023_ui_status_browser_evidence.py",
        "Partial Fill Web UI Acceptance",
        "UI-13 Order Display Correctness",
        "partial_cancel_display_verdict=pass",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "fill_trade_identities_stable_after_cancel",
        "validate_p023_partial_fill_browser_evidence.py",
        "action-control part of UI-13 remains blocked",
        "`paper-armed-submit.png` is required only after Web UI action controls are enabled.",
        "S1 submitted/working",
        "S2 partially filled",
        "S3 cancel pending",
        "S4 remaining cancelled",
        "UIN-01",
        "UIN-10",
        "UIN-11",
        "UIN-12",
        "UIN-13",
        "UIN-15",
        "Screenshots alone are never sufficient.",
    ]:
        require(phrase in web_ui, f"P023 web UI acceptance missing {phrase}")

    ui_acceptance = read(PROPOSAL / "ui-acceptance.md")
    for phrase in [
        "Before Command Enabled",
        "After Paper Command Enabled",
        "command.mode=paper_armed",
        "No submit, cancel, replace",
        "gateway event id",
        "post-submit/post-cancel readback refs",
    ]:
        require(phrase in ui_acceptance, f"P023 UI acceptance missing {phrase}")

    ui_design = read(PROPOSAL / "ui-design.md")
    for phrase in [
        "`account-submit-order-button`",
        "`account-cancel-order-button`",
        "`account-command-reconciliation-ref`",
        "When disabled, the page should not reserve empty command controls.",
    ]:
        require(phrase in ui_design, f"P023 UI design missing {phrase}")


def validate_index() -> None:
    text = read(PROPOSAL_INDEX)
    require("Updated: 2026-06-21" in text, "proposal index date not updated")
    require("P023 OpenCTP 19053 Paper Command Capability" in text, "proposal index missing P023")
    require("ADR-0007 successor proposal" in text, "proposal index missing ADR-0007 relation")


def validate_contract_gate_landed() -> None:
    require((ROOT / "scripts" / "validate_p023_account_command_contracts.py").exists(), "missing P023 command contract validator")
    require((ROOT / "scripts" / "run_p023_openctp19053_command_acceptance.py").exists(), "missing P023 command runtime runner")
    require((ROOT / "scripts" / "validate_p023_openctp19053_command_run.py").exists(), "missing P023 command run validator")
    require((ROOT / "scripts" / "validate_p023_ui_status_browser_evidence.py").exists(), "missing P023 UI status validator")
    for filename in [
        "order_intent.schema.json",
        "cancel_intent.schema.json",
        "decision_and_event.schema.json",
    ]:
        require((CONTRACT_DIR / filename).exists(), f"missing command contract schema {filename}")
    fixture_dir = CONTRACT_DIR / "fixtures" / "openctp19053"
    for filename in [
        "order_intent_valid.json",
        "cancel_intent_valid.json",
        "command_audit_valid.json",
        "submit_idempotency_replay_valid.json",
        "invalid_order_intent_missing_idempotency.json",
        "invalid_order_intent_raw_secret_flag.json",
        "invalid_cancel_intent_missing_identity.json",
        "invalid_audit_ack_final_state.json",
        "invalid_submit_idempotency_replay_second_broker_order.json",
        "invalid_submit_idempotency_replay_missing_source_ref.json",
    ]:
        require((fixture_dir / filename).exists(), f"missing command contract fixture {filename}")


def validate_current_backend_still_read_only() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    forbidden_tokens = ["/submit", "/cancel", "/replace", "/commands"]
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        for token in forbidden_tokens:
            require(token not in path, f"backend exposes command route before P023 implementation: {path}")
        if path.startswith("/api/mirror/"):
            forbidden_methods = sorted(method for method in methods if method not in {"GET", "HEAD"})
            require(not forbidden_methods, f"mirror route exposes write method before P023 implementation: {path}")


def main() -> None:
    validate_adr_link()
    validate_proposal_docs()
    validate_index()
    validate_contract_gate_landed()
    validate_current_backend_still_read_only()
    print("P023_OPENCTP_19053_COMMAND_ACCEPTANCE_DESIGN_OK: status=paper_runtime_accepted current_command=disabled")


if __name__ == "__main__":
    main()
