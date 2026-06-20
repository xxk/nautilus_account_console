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
    "/submit",
    "/cancel",
    "/replace",
    "/commands",
]


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
        "landing_status: not_started",
        "Governed Account Command Capability",
        "Account Mirror never sends commands",
        "Gateway acknowledgement 不是最终账户状态",
        "`paper_armed`",
        "`live_armed`",
        "Phase 0: ADR/proposal/contract skeleton, no command implementation.",
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


def validate_backend_has_no_command_routes() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set()) or set()
        for token in FORBIDDEN_ROUTE_TOKENS:
            require(token not in path, f"backend exposes forbidden pre-ADR0007 command route: {path}")
        if path.startswith("/api/mirror/"):
            forbidden_methods = sorted(method for method in methods if method not in {"GET", "HEAD"})
            require(not forbidden_methods, f"mirror route {path} exposes write methods: {forbidden_methods}")


def main() -> None:
    validate_adr()
    validate_index()
    validate_existing_design_gate_still_closed()
    validate_capability_fixtures_still_disabled()
    validate_backend_has_no_command_routes()
    print("ADR0007_ACCOUNT_COMMAND_CAPABILITY_OK: status=proposed current_command=disabled")


if __name__ == "__main__":
    main()
