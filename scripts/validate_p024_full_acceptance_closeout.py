from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "docs" / "acceptance" / "p024-account-console-paper-command-controls" / "full-acceptance-closeout.json"
OWNER_READINESS = (
    ROOT / "docs" / "acceptance" / "p024-account-console-paper-command-controls" / "owner-runtime-invocation-readiness.json"
)
P024_EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
PROPOSAL = ROOT / "docs" / "proposals" / "p024-account-console-paper-command-controls"
PROPOSAL_INDEX = ROOT / "docs" / "proposals" / "README.md"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"


class P024FullAcceptanceCloseoutError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024FullAcceptanceCloseoutError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def scan_forbidden_text() -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    matches: list[str] = []
    for path in [CLOSEOUT, OWNER_READINESS]:
        payload = path.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in payload for fragment in fragments):
            matches.append(str(path))
    return matches


def validate_required_gates(payload: dict[str, Any]) -> None:
    gates = {gate["id"]: gate for gate in payload["required_gates"]}
    expected = {
        "p024_backend_command_api": "P024_PAPER_COMMAND_API_OK",
        "p024_ui_command_controls": "P024_UI_COMMAND_CONTROLS_BROWSER_EVIDENCE_OK",
        "p024_runtime_closeout_projection": "P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK",
        "p024_partial_fill_cancel_display": "P024_PARTIAL_FILL_CANCEL_BROWSER_EVIDENCE_OK",
        "p024_runtime_handoff_request": "P024_RUNTIME_HANDOFF_BROWSER_EVIDENCE_OK",
        "p024_owner_runtime_invocation_readiness": "P024_OWNER_RUNTIME_INVOCATION_READINESS_OK",
        "p024_runtime_readiness_ui_projection": "P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK",
        "p024_design_and_adr": "P024_PAPER_COMMAND_CONTROLS_DESIGN_OK",
        "p019_boundary": "P019_API_BOUNDARY_OK",
        "proposal_docs": "PROPOSAL_DOCS_OK",
    }
    require(set(expected).issubset(gates), "required gate set incomplete")
    for gate_id, signal in expected.items():
        gate = gates[gate_id]
        require(gate["status"] == "passed", f"{gate_id}: gate must be passed")
        require(signal in gate["pass_signal"], f"{gate_id}: pass signal mismatch")
        require(gate["command"], f"{gate_id}: command missing")


def validate_scenarios(payload: dict[str, Any]) -> None:
    scenarios = {item["id"]: item for item in payload["scenario_matrix"]}
    require(set(scenarios) == {f"A{index}" for index in range(1, 15)}, "scenario matrix must contain A1-A14 only")
    passed = {"A1", "A2", "A3", "A5", "A7", "A9", "A10", "A11", "A12", "A14"}
    for scenario_id in passed:
        require(scenarios[scenario_id]["status"] == "passed", f"{scenario_id}: expected passed")
        require(scenarios[scenario_id].get("evidence_refs"), f"{scenario_id}: evidence refs missing")
    require(
        scenarios["A4"]["status"] == "blocked_pending_owner_runtime_execution",
        "A4 must remain blocked until owner runtime execution",
    )
    require(
        set(scenarios["A4"]["blocker_refs"])
        == {"p024_external_owner_runtime_write_approval_required", "p024_owner_runtime_artifacts_missing"},
        "A4 blocker refs mismatch",
    )
    require(scenarios["A6"]["status"] == "passed_pre_gateway_contract_gate", "A6 status mismatch")
    require(
        scenarios["A8"]["status"] == "passed_display_contract_real_runtime_blocked",
        "A8 status mismatch",
    )
    require(
        scenarios["A13"]["status"] == "passed_blocked_by_external_approval",
        "A13 status mismatch",
    )


def validate_residual_blockers(payload: dict[str, Any]) -> None:
    blockers = {blocker["blocker_id"]: blocker for blocker in payload["residual_blockers"]}
    expected = {
        "p024_external_owner_runtime_write_approval_required",
        "p024_owner_runtime_artifacts_missing",
        "p024_real_partial_fill_runtime_missing",
    }
    require(set(blockers) == expected, "residual blocker set mismatch")
    approval = blockers["p024_external_owner_runtime_write_approval_required"]
    require(approval["type"] == "external_write_approval_required", "approval blocker type mismatch")
    require(approval["owner_ref"] == "owner://nautilus_ctp_adapter", "approval owner mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    artifacts = blockers["p024_owner_runtime_artifacts_missing"]["required_artifacts"]
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
        require(artifact in artifacts, f"missing required owner artifact: {artifact}")


def validate_negative_assertions(payload: dict[str, Any]) -> None:
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
        require(negative[key] is False, f"negative assertion mismatch: {key}")
    non_claims = set(payload["explicit_non_claims"])
    for claim in [
        "does_not_claim_new_browser_triggered_owner_runtime_execution",
        "does_not_claim_live_readiness",
        "does_not_write_owner_repo",
        "does_not_send_broker_order_from_browser",
        "does_not_close_real_runtime_execution_until_owner_artifacts_exist",
        "does_not_use_screenshot_as_order_or_runtime_truth",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_evidence_files() -> None:
    for path in [
        OWNER_READINESS,
        P024_EVIDENCE_DIR / "command-controls-ui.json",
        P024_EVIDENCE_DIR / "runtime-closeout-ui.json",
        P024_EVIDENCE_DIR / "partial-fill-cancel-order-display.json",
        P024_EVIDENCE_DIR / "runtime-handoff-ui.json",
        P024_EVIDENCE_DIR / "runtime-readiness-ui.json",
        ROOT / "frontend" / "tests" / "e2e" / "p024-runtime-invocation-readiness.spec.ts",
        ROOT / "scripts" / "validate_p024_runtime_readiness_browser_evidence.py",
    ]:
        require(path.exists(), f"missing referenced evidence path: {path}")


def validate_docs() -> None:
    readme = text(PROPOSAL / "README.md")
    acceptance = text(PROPOSAL / "acceptance.md")
    phase_plan = text(PROPOSAL / "phase-plan.md")
    index = text(PROPOSAL_INDEX)
    adr = text(ADR)
    owner_map = text(OWNER_MAP)
    for phrase in [
        "phase4_residual_blocker_audit_passed",
        "validate_p024_full_acceptance_closeout.py",
        "accepted_with_residual_owner_runtime_blockers",
    ]:
        require(phrase in readme or phrase in acceptance or phrase in phase_plan, f"proposal docs missing {phrase}")
    require("Phase 4 Closeout" in phase_plan, "phase plan missing Phase 4")
    require("Full P024 gate set and residual blocker mapping" in phase_plan, "phase plan missing closeout scope")
    require("runtime readiness UI projection" in index, "proposal index missing P024 runtime readiness UI text")
    require("P024 Phase 3e runtime readiness UI projection" in adr, "ADR missing Phase 3e status")
    require("P024 paper command controls" in owner_map, "owner map missing P024 command owner boundary")
    require("owner://nautilus_ctp_adapter" in owner_map, "owner map missing P024 external runtime owner")
    require("Account Mirror a command writer" in owner_map, "owner map missing P024 mirror writer rejection")
    require("Account Mirror never sends commands" in adr, "ADR missing mirror command boundary")


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.full-acceptance-closeout.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4_residual_blocker_audit_passed", "status mismatch")
    require(payload["verdict"] == "accepted_with_residual_owner_runtime_blockers", "verdict mismatch")
    accepted = set(payload["accepted_scope"])
    for item in [
        "backend_paper_command_api_contract_gate",
        "frontend_guarded_command_controls",
        "runtime_closeout_readonly_projection",
        "partial_fill_then_cancel_ui_display_contract",
        "owner_runtime_handoff_request_projection",
        "owner_runtime_invocation_readiness",
        "runtime_readiness_ui_projection",
        "proposal_docs_and_adr_boundary",
    ]:
        require(item in accepted, f"accepted scope missing: {item}")
    not_accepted = set(payload["not_accepted_scope"])
    for item in [
        "new_browser_triggered_owner_runtime_submit_cancel_execution",
        "new_p024_gateway_send_from_web_ui",
        "new_p024_broker_order_created_from_web_ui",
        "real_p024_partial_fill_runtime",
        "live_armed_mode",
        "account_mirror_write_authority",
        "replace_or_modify_order",
    ]:
        require(item in not_accepted, f"not accepted scope missing: {item}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    payload = load(CLOSEOUT)
    validate_payload(payload)
    validate_required_gates(payload)
    validate_scenarios(payload)
    validate_residual_blockers(payload)
    validate_negative_assertions(payload)
    validate_evidence_files()
    validate_docs()
    print(
        "P024_FULL_ACCEPTANCE_CLOSEOUT_OK: "
        "status=phase4_residual_blocker_audit_passed verdict=accepted_with_residual_owner_runtime_blockers"
    )


if __name__ == "__main__":
    main()
