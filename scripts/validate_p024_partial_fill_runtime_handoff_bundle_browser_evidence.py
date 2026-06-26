from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-runtime-handoff-bundle-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-runtime-handoff-bundle-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
HISTORICAL_TYPES = ROOT / "frontend" / "src" / "types-historical-p024.ts"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-partial-fill-runtime-execution-handoff-bundle.spec.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024PartialFillRuntimeHandoffBundleEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRuntimeHandoffBundleEvidenceError(message)


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
    require(payload["schema"] == "account-console.p024.partial-fill-runtime-handoff-bundle-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    bundle = payload["api_handoff_bundle"]
    require(
        bundle["schema"] == "account-console.p024.partial-fill-runtime-execution-handoff-bundle.v1",
        "API handoff bundle schema mismatch",
    )
    require(
        bundle["status"] == "phase4k_partial_fill_runtime_execution_handoff_bundle_ready",
        "API handoff bundle status mismatch",
    )
    require(bundle["verdict"] == "handoff_bundle_ready_runtime_not_invoked", "API verdict mismatch")
    require(bundle["execution_allowed"] is False, "execution allowed flag mismatch")
    require(bundle["approval_required"] is True, "approval required flag mismatch")
    require(bundle["approval_obtained"] is False, "approval obtained flag mismatch")
    require(bundle["runtime_input_count"] == 4, "runtime input count mismatch")
    require(bundle["operator_step_count"] == 7, "operator step count mismatch")
    require(bundle["non_ui_success_count"] == 5, "non-ui success count mismatch")
    require(bundle["web_ui_success_count"] == 4, "web-ui success count mismatch")
    require(bundle["fallback_count"] == 4, "fallback count mismatch")
    for key in [
        "runtime_invocation_attempted",
        "owner_repo_write_attempted",
        "new_order_submitted",
        "cancel_sent",
        "full_acceptance_claimed",
        "browser_fixture_promoted_to_runtime_truth",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(bundle[key] is False, f"partial-fill handoff bundle negative assertion mismatch: {key}")
    checks = payload.get("browser_checks") or {}
    for check in [
        "handoff_bundle_panel_visible",
        "execution_allowed_displayed_false",
        "approval_obtained_displayed_false",
        "runtime_invocation_displayed_false",
        "owner_write_displayed_false",
        "new_order_displayed_false",
        "cancel_sent_displayed_false",
        "runtime_inputs_displayed",
        "operator_sequence_displayed",
        "success_criteria_displayed",
        "fallback_classifications_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks.get(check) is True, f"browser check missing: {check}")


def validate_backend_endpoint() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-runtime-execution-handoff-bundle"
    require(all(getattr(item, "path", "") != route for item in app.routes), "partial-fill handoff bundle route should be retired")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-runtime-execution-handoff-bundle")
    require(response.status_code == 404, "partial-fill handoff bundle API retirement mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = HISTORICAL_TYPES.read_text(encoding="utf-8")
    spec_text = SPEC.read_text(encoding="utf-8")
    require("account-partial-fill-runtime-handoff-bundle-panel" not in app_text, "retired frontend panel should be removed")
    require(
        "fetchCommandPartialFillRuntimeExecutionHandoffBundle" not in api_text,
        "retired frontend API fetch should be removed",
    )
    require(
        "interface CommandPartialFillRuntimeExecutionHandoffBundle" in types_text,
        "frontend type missing partial-fill handoff bundle interface",
    )
    for phrase in [
        "p024-partial-fill-runtime-handoff-bundle-ui.png",
        "partial-fill-runtime-handoff-bundle-ui.json",
        "fully_filled_not_partial_fill_then_cancel",
        "0 < filled_quantity < submitted_quantity",
    ]:
        require(phrase in spec_text, f"Playwright spec missing {phrase}")


def main() -> None:
    require(SCREENSHOT.exists(), "missing partial-fill runtime handoff bundle screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_PARTIAL_FILL_RUNTIME_HANDOFF_BUNDLE_BROWSER_EVIDENCE_OK: "
        "partial_fill_runtime_handoff_bundle_ui=archive_only_historical_evidence route=retired_404 execution_allowed=false new_order_submitted=false cancel_sent=false"
    )


if __name__ == "__main__":
    main()
