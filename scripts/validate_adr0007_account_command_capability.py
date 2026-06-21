from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
ADR = ROOT / "docs" / "adr" / "0007-adopt-governed-account-command-capability.md"
ADR_INDEX = ROOT / "docs" / "adr" / "README.md"
DESIGN_GATE = ROOT / "contracts" / "account_capability" / "command_capability_design_gate.json"
FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_capability"

REQUIRED_FLOW = [
    "OrderIntent",
    "RiskDecision",
    "ApprovalDecision",
    "ExecutionCommand",
    "Command Gateway",
    "ExecutionEvent",
    "Account Mirror Readback",
    "ReconciliationResult",
]

FORBIDDEN_ROUTE_TOKENS = [
    "/replace",
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


class Adr0007ValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Adr0007ValidationError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_adr() -> None:
    text = ADR.read_text(encoding="utf-8")
    for phrase in [
        'adr_id: "0007"',
        "decision_status: proposed",
        "landing_status: p024_phase4e_runtime_execution_gap_audit_gate",
        "Governed Account Command Capability",
        "Account Mirror never sends commands",
        "Gateway acknowledgement 不是最终账户状态",
        "`paper_armed`",
        "`live_armed`",
        "Phase 0: ADR/proposal/contract skeleton, no command implementation.",
        "P024 Phase 1 backend command API is accepted as a contract gate only",
        "P024 Phase 2 frontend guarded controls are accepted as browser contract evidence only",
        "P024 Phase 3a runtime closeout projection is accepted as read-only Web UI evidence",
        "P024 Phase 3b partial-fill cancel UI display is accepted as browser display-contract evidence only",
        "P024 Phase 3c owner-runtime handoff request is accepted as browser handoff evidence only",
        "P024 Phase 3d owner-runtime invocation readiness is accepted as a readiness gate only",
        "P024 Phase 3e runtime readiness UI projection is accepted as browser blocker evidence only",
        "P024 Phase 4 residual blocker audit is accepted as closeout evidence only",
        "P024 Phase 4a owner-runtime execution approval packet is accepted as an approval-packet gate only",
        "P024 Phase 4b runtime approval packet UI projection is accepted as browser blocker evidence only",
        "P024 Phase 4c owner-runtime execution handoff bundle is accepted as a handoff gate only",
        "P024 Phase 4d runtime handoff bundle UI projection is accepted as browser blocker evidence only",
        "P024 Phase 4e runtime execution gap audit is accepted as final blocker evidence only",
        "browser_triggered_broker_order=false",
        "gateway_send_attempted=false",
        "runtime_invocation_attempted=false",
        "owner_repo_write_attempted=false",
        "full_runtime_acceptance_claimed=false",
    ]:
        require(phrase in text, f"ADR-0007 missing phrase: {phrase}")
    for phrase in REQUIRED_FLOW:
        require(phrase in text, f"ADR-0007 missing required flow term: {phrase}")
    require("POST /api/mirror/.../orders` is forbidden" in text, "ADR-0007 must forbid mirror POST")


def validate_index() -> None:
    text = ADR_INDEX.read_text(encoding="utf-8")
    require("Updated: 2026-06-21" in text, "ADR index date not updated")
    require("ADR-0007" in text, "ADR index missing ADR-0007")
    require("Governed Account Command Capability" in text, "ADR index missing ADR-0007 title")


def validate_existing_design_gate_still_closed() -> None:
    payload = load_json(DESIGN_GATE)
    require(payload["status"] == "design_gate_only", "command design gate must remain design_gate_only")
    current = payload["current_phase"]
    for key in [
        "command_implementation_accepted",
        "ui_command_controls_accepted",
        "account_mirror_write_authority",
        "broker_gateway_implementation_accepted",
    ]:
        require(current[key] is False, f"{key} must remain false until ADR-0007 successor lands")


def validate_capability_fixtures_still_disabled() -> None:
    for path in sorted(FIXTURE_DIR.glob("acct_*_capability.json")):
        payload = load_json(path)
        command = payload["capabilities"]["command"]
        require(command["enabled"] is False, f"{path}: command must stay disabled")
        require(command["mode"] == "disabled", f"{path}: command mode must stay disabled")
        require(command["allowed_actions"] == [], f"{path}: command allowed_actions must stay empty")
        require(payload["boundaries"]["order_action"] is False, f"{path}: order_action boundary must stay false")


def validate_backend_has_only_p024_command_routes() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route_paths = {getattr(route, "path", "") for route in app.routes}
    require(set(ALLOWED_COMMAND_ROUTES).issubset(route_paths), "ADR-0007 P024 command routes missing")
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        if path in ALLOWED_COMMAND_ROUTES:
            require(methods == ALLOWED_COMMAND_ROUTES[path], f"{path}: P024 command route methods mismatch")
        elif path.startswith("/api/commands"):
            require(False, f"unexpected command route outside P024 allowlist: {path}")
        for token in FORBIDDEN_ROUTE_TOKENS:
            require(token not in path, f"backend exposes forbidden ADR-0007 command route: {path}")
        if path.startswith("/api/mirror/"):
            forbidden_methods = sorted(method for method in methods if method not in {"GET", "HEAD"})
            require(not forbidden_methods, f"mirror route {path} exposes write methods: {forbidden_methods}")


def main() -> None:
    validate_adr()
    validate_index()
    validate_existing_design_gate_still_closed()
    validate_capability_fixtures_still_disabled()
    validate_backend_has_only_p024_command_routes()
    print(
        "ADR0007_ACCOUNT_COMMAND_CAPABILITY_OK: "
        "status=proposed landing=p024_phase4e_runtime_execution_gap_audit_gate"
    )


if __name__ == "__main__":
    main()
