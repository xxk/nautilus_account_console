from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-handoff-bundle-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-handoff-bundle-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-runtime-execution-handoff-bundle.spec.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024RuntimeHandoffBundleEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeHandoffBundleEvidenceError(message)


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
    require(payload["schema"] == "account-console.p024.runtime-handoff-bundle-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    bundle = payload["api_handoff_bundle"]
    require(
        bundle["schema"] == "account-console.p024.owner-runtime-execution-handoff-bundle.v1",
        "API handoff bundle schema mismatch",
    )
    require(
        bundle["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready",
        "API handoff bundle status mismatch",
    )
    require(bundle["verdict"] == "handoff_bundle_ready_runtime_not_invoked", "API verdict mismatch")
    require(bundle["execution_allowed"] is False, "execution allowed flag mismatch")
    require(bundle["approval_required"] is True, "approval required flag mismatch")
    require(bundle["approval_obtained"] is False, "approval obtained flag mismatch")
    require(bundle["runtime_input_count"] == 7, "runtime input count mismatch")
    require(bundle["operator_step_count"] == 7, "operator step count mismatch")
    require(bundle["required_owner_artifact_count"] == 14, "owner artifact count mismatch")
    require(bundle["post_handoff_gate_count"] == 6, "post handoff gate count mismatch")
    require(bundle["blocker_count"] == 3, "blocker count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "browser_triggered_broker_order",
        "gateway_send_attempted",
        "broker_order_created",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(bundle[key] is False, f"handoff bundle negative assertion mismatch: {key}")
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
        require(checks.get(check) is True, f"browser check missing: {check}")
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
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_backend_endpoint() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/runtime-execution-handoff-bundle"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "handoff bundle route must be GET-only")
    require(found, "handoff bundle route missing")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-execution-handoff-bundle")
    require(response.status_code == 200, "handoff bundle API does not return 200")
    payload = response.json()
    require(payload["status"] == "phase4c_owner_runtime_execution_handoff_bundle_ready", "API status mismatch")
    require(payload["execution_guard"]["execution_allowed"] is False, "API execution flag mismatch")
    require(payload["execution_guard"]["approval_obtained"] is False, "API approval flag mismatch")
    negative = payload["negative_assertions"]
    require(negative["runtime_invocation_attempted"] is False, "API invocation flag mismatch")
    require(negative["owner_repo_write_attempted"] is False, "API owner write flag mismatch")
    require(negative["broker_order_created"] is False, "API broker order flag mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeExecutionHandoffBundlePanel",
        "account-runtime-handoff-bundle-panel",
        "account-runtime-handoff-bundle-status",
        "account-runtime-handoff-bundle-execution-allowed",
        "account-runtime-handoff-bundle-input",
        "account-runtime-handoff-bundle-step",
        "account-runtime-handoff-bundle-artifact-count",
        "account-runtime-handoff-bundle-blocker",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["fetchCommandRuntimeExecutionHandoffBundle", "runtime-execution-handoff-bundle"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require(
        "interface CommandRuntimeExecutionHandoffBundle" in types_text,
        "frontend type missing handoff bundle interface",
    )
    for phrase in [
        "p024-runtime-handoff-bundle-ui.png",
        "runtime-handoff-bundle-ui.json",
        "does_not_guess_runtime_inputs",
        "does_not_close_real_runtime_execution",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime handoff bundle screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK: "
        "runtime_handoff_bundle_ui=pass execution_allowed=false runtime_invocation_attempted=false"
    )


if __name__ == "__main__":
    main()
