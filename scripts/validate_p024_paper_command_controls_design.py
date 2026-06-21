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

REQUIRED_DOCS = [
    "README.md",
    "phase-plan.md",
    "acceptance.md",
    "ui-design.md",
    "ui-acceptance.md",
    "partial-fill-cancel-ui-acceptance.md",
]

ALLOWED_COMMAND_ROUTES = {
    "/api/commands/accounts/{account_id}/submit-intents",
    "/api/commands/accounts/{account_id}/cancel-intents",
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

    adr = read(ADR)
    require("ADR-0007" in adr, "ADR-0007 missing")
    require("Second successor proposal: [P024 Account Console Paper Command Controls]" in adr, "ADR missing P024 successor")
    require("P024 Phase 1 backend command API" in adr, "ADR missing P024 next implementation work")


def validate_readme() -> None:
    text = read(PROPOSAL / "README.md")
    for phrase in [
        "Proposal ID: `p024-account-console-paper-command-controls`",
        "Status: phase1_backend_contract_gate_passed",
        "ADR carrier: yes",
        "Primary ADR: ADR-0007",
        "Predecessor: [P023 OpenCTP 19053 Paper Command Capability]",
        "paper-only controls proposal",
        "No `live_armed` mode.",
        "No Account Mirror broker writer.",
        "partial-fill then cancel order-display correctness scenario",
        "validate_p024_paper_command_controls_design.py",
        "validate_p024_paper_command_api.py",
    ]:
        require(phrase in text, f"P024 README missing phrase: {phrase}")


def validate_phase_plan() -> None:
    text = read(PROPOSAL / "phase-plan.md")
    for phrase in [
        "Artifact Trust Boundary",
        "output/account_command/ctp-paper-19053/",
        "phase_1_backend_command_api",
        "phase_2_frontend_guarded_controls",
        "phase_3_browser_paper_submit_cancel",
        "phase_3b_partial_fill_cancel_ui_display",
        "Partial-fill cancel display",
        "Phase 1 Backend command API",
        "completed_contract_gate",
        "validate_p024_paper_command_api.py",
        "Frontend submit/cancel controls are not implemented.",
        "Real partial-fill runtime remains blocked",
    ]:
        require(phrase in text, f"P024 phase plan missing phrase: {phrase}")


def validate_acceptance() -> None:
    text = read(PROPOSAL / "acceptance.md")
    for phrase in [
        "P024_PAPER_COMMAND_CONTROLS_DESIGN_OK",
        "P024_PAPER_COMMAND_API_OK",
        "Implementation/browser evidence is required before implementation closeout",
        "UI Anti-Drift Acceptance",
        "forbidden_actions",
        "forbidden_claims",
        "Account Mirror remains read-only",
        "gateway ack alone is final",
        "live mode exposed",
        "A10",
        "Partial fill then cancel Web UI order display correctness",
        "S1 submitted/working",
        "S2 partially filled",
        "S3 cancel pending",
        "S4 remaining cancelled",
        "filled_quantity + remaining_quantity == submitted_quantity",
        "filled_quantity + cancelled_quantity == submitted_quantity",
        "account-order-identity",
        "account-cancel-pending-ref",
        "validate_p023_partial_fill_browser_evidence.py",
        "P024 implementation must regenerate P024-scoped browser evidence",
        "Phase 1 Backend Command API Acceptance",
        "gateway_send_attempted=false",
        "accepted_for_risk",
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
    ]:
        require(phrase in ui_acceptance, f"P024 UI acceptance missing phrase: {phrase}")


def validate_partial_fill_cancel_doc() -> None:
    text = read(PROPOSAL / "partial-fill-cancel-ui-acceptance.md")
    for phrase in [
        "Proposal ID: `p024-account-console-paper-command-controls`",
        "Status: phase1_backend_contract_gate_passed",
        "acct.ctp.paper.19053",
        "not turn screenshots, browser text or TickTrader UI state into order truth",
        "account-console.p024.partial-fill-cancel-ui-acceptance.v1",
        "same_order_identity_across_stages",
        "s2_browser_fill_sum_equals_order_filled_quantity",
        "s2_cancel_target_equals_s2_remaining_quantity",
        "s3_quantities_unchanged_until_cancel_readback",
        "s4_cancelled_quantity_equals_s2_remaining_quantity",
        "s4_remaining_quantity_zero",
        "fill_trade_identities_stable_after_cancel",
        "account-command-readback-ref",
        "account-command-reconciliation-ref",
        "does_not_use_screenshot_as_order_truth",
        "gateway_ack_is_not_final_state",
        "raw_secret_values_recorded=false",
        "P023_PARTIAL_FILL_BROWSER_EVIDENCE_OK",
        "P024 must regenerate P024-scoped evidence",
    ]:
        require(phrase in text, f"P024 partial-fill cancel acceptance missing phrase: {phrase}")


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
    require(ALLOWED_COMMAND_ROUTES.issubset(route_paths), "P024 command API routes missing")
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        if path in ALLOWED_COMMAND_ROUTES:
            require(methods == {"POST"}, f"{path}: P024 command route must be POST-only")
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
    validate_p023_predecessor_evidence()
    validate_existing_command_boundary_still_closed()
    validate_backend_command_routes_are_p024_only()
    print(
        "P024_PAPER_COMMAND_CONTROLS_DESIGN_OK: "
        "status=phase1_backend_contract_gate_passed current_ui_command=disabled partial_fill_cancel_ui=designed"
    )


if __name__ == "__main__":
    main()
