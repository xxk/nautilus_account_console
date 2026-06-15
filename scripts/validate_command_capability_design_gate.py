from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN_GATE = ROOT / "contracts" / "account_capability" / "command_capability_design_gate.json"
DESIGN_DOC = ROOT / "docs" / "design" / "account-command-capability-design-gate.md"
FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_capability"
BACKEND_SRC = ROOT / "backend" / "src"

REQUIRED_FLOW = [
    "order_intent",
    "risk_check",
    "approval_admission",
    "execution_gateway",
    "execution_event",
    "account_mirror_readback",
    "reconciliation_projection",
    "ui_status_evidence",
]

REQUIRED_CONTRACTS = {
    "OrderIntent",
    "RiskDecision",
    "ApprovalDecision",
    "ExecutionCommand",
    "ExecutionEvent",
    "MirrorReadback",
    "ReconciliationResult",
}

FORBIDDEN_COMMAND_ROUTE_TOKENS = [
    "/commands",
    "/submit",
    "/cancel",
    "/replace",
]


class DesignGateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DesignGateError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_design_gate() -> None:
    payload = load_json(DESIGN_GATE)
    require(payload["schema_version"] == "account_command_capability_design_gate.v1", "schema_version drifted")
    require(payload["status"] == "design_gate_only", "command design gate must remain design_gate_only")
    require(payload["proposal_phase"] == "p011.phase_7", "proposal phase mismatch")
    require(payload["primary_adr"] == "ADR-0004", "primary ADR mismatch")
    current = payload["current_phase"]
    for key in [
        "command_implementation_accepted",
        "ui_command_controls_accepted",
        "account_mirror_write_authority",
        "broker_gateway_implementation_accepted",
    ]:
        require(current[key] is False, f"{key} must be false in P011 Phase 7")

    require(payload["required_flow"] == REQUIRED_FLOW, "required command flow changed")
    require(set(payload["required_future_contracts"]) == REQUIRED_CONTRACTS, "required future contract set changed")

    boundaries = payload["authority_boundaries"]
    for key in [
        "account_console_ui_command_authority",
        "account_console_backend_broker_writer",
        "account_mirror_command_authority",
    ]:
        require(boundaries[key] is False, f"{key} must be false")
    for key in [
        "risk_owner_required",
        "approval_owner_required",
        "gateway_owner_required",
        "readback_reconciliation_required",
    ]:
        require(boundaries[key] is True, f"{key} must be true")


def validate_design_doc() -> None:
    text = DESIGN_DOC.read_text(encoding="utf-8")
    for phrase in [
        "design_gate_only",
        "P011 Phase 7 does not implement submit, cancel or replace",
        "Order Intent",
        "Risk Check",
        "Approval / Admission",
        "Execution Gateway",
        "Account Mirror Readback",
        "Reconciliation Projection",
        "The gateway response is not final account state",
    ]:
        require(phrase in text, f"design doc missing phrase: {phrase}")


def validate_existing_account_fixtures_remain_read_only() -> None:
    for path in sorted(FIXTURE_DIR.glob("acct_*_capability.json")):
        payload = load_json(path)
        command = payload["capabilities"]["command"]
        boundaries = payload["boundaries"]
        require(command["enabled"] is False, f"{path}: command.enabled must remain false")
        require(command["mode"] == "disabled", f"{path}: command.mode must remain disabled")
        require(command["allowed_actions"] == [], f"{path}: allowed_actions must remain empty")
        require(command["gateway_kind"] is None, f"{path}: gateway_kind must remain null")
        require(command["authority_ref"] is None, f"{path}: authority_ref must remain null")
        require(boundaries["order_action"] is False, f"{path}: order_action boundary must remain false")


def validate_backend_has_no_command_routes() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        for token in FORBIDDEN_COMMAND_ROUTE_TOKENS:
            require(token not in path, f"backend exposes forbidden command route: {path}")
        if path.startswith("/api/mirror/"):
            forbidden_methods = sorted(method for method in methods if method not in {"GET", "HEAD"})
            require(not forbidden_methods, f"mirror route {path} exposes non-read methods: {forbidden_methods}")


def main() -> None:
    validate_design_gate()
    validate_design_doc()
    validate_existing_account_fixtures_remain_read_only()
    validate_backend_has_no_command_routes()
    print("COMMAND_CAPABILITY_DESIGN_GATE_OK: phase=p011.phase_7 status=design_gate_only")


if __name__ == "__main__":
    main()
