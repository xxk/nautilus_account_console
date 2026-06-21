from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-readiness-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-readiness-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-runtime-invocation-readiness.spec.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024RuntimeReadinessEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeReadinessEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "trading.openctp", "live_armed=true"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.runtime-readiness-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    readiness = payload["api_readiness"]
    require(
        readiness["schema"] == "account-console.p024.owner-runtime-invocation-readiness.v1",
        "API readiness schema mismatch",
    )
    require(
        readiness["status"] == "blocked_waiting_for_external_owner_runtime_write_approval",
        "API readiness status mismatch",
    )
    require(readiness["verdict"] == "readiness_package_passed_runtime_not_invoked", "API readiness verdict mismatch")
    require(readiness["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(readiness["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(readiness["config_ref"] == "cfgs/local/ctp.openctp.tts.7x24.local.json", "config ref mismatch")
    require(readiness["config_raw_content_read"] is False, "raw config read flag mismatch")
    require(readiness["approval_required"] is True, "approval required flag mismatch")
    require(readiness["approval_obtained"] is False, "approval obtained flag mismatch")
    require(readiness["entrypoint_count"] == 2, "entrypoint count mismatch")
    require(readiness["blocker_count"] == 2, "blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(readiness[key] is False, f"readiness negative assertion mismatch: {key}")
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
        require(checks.get(check) is True, f"browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_invoke_owner_runtime",
        "does_not_send_broker_order_from_browser",
        "does_not_write_owner_repo",
        "does_not_read_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_close_phase_3_runtime_execution",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_backend_endpoint() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/runtime-invocation-readiness"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "runtime readiness route must be GET-only")
    require(found, "runtime readiness route missing")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-invocation-readiness")
    require(response.status_code == 200, "runtime readiness API does not return 200")
    payload = response.json()
    require(payload["status"] == "blocked_waiting_for_external_owner_runtime_write_approval", "API status mismatch")
    require(payload["owner_runtime"]["owner_ref"] == "owner://nautilus_ctp_adapter", "API owner mismatch")
    require(payload["owner_runtime"]["config_raw_content_read"] is False, "API config raw read mismatch")
    require(payload["external_write_approval_request"]["required"] is True, "API approval required mismatch")
    require(payload["external_write_approval_request"]["obtained"] is False, "API approval obtained mismatch")
    negative = payload["negative_assertions"]
    require(negative["runtime_invocation_attempted"] is False, "API invocation flag mismatch")
    require(negative["owner_repo_write_attempted"] is False, "API owner write flag mismatch")
    require(negative["browser_triggered_broker_order"] is False, "API browser trigger flag mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeInvocationReadinessPanel",
        "account-runtime-readiness-panel",
        "account-runtime-readiness-status",
        "account-runtime-readiness-owner-path",
        "account-runtime-readiness-approval-obtained",
        "account-runtime-readiness-invoked",
        "account-runtime-readiness-browser-trigger",
        "account-runtime-readiness-blocker",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["fetchCommandRuntimeInvocationReadiness", "runtime-invocation-readiness"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require("interface CommandRuntimeInvocationReadiness" in types_text, "frontend type missing readiness interface")
    for phrase in [
        "p024-runtime-readiness-ui.png",
        "runtime-readiness-ui.json",
        "sensitive_endpoint_wording_absent",
        "does_not_close_phase_3_runtime_execution",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime readiness screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_READINESS_BROWSER_EVIDENCE_OK: "
        "runtime_readiness_ui=pass runtime_invocation_attempted=false external_write_approval=blocked"
    )


if __name__ == "__main__":
    main()
