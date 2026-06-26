from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-execution-handoff-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-execution-handoff-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024OwnerRepairExecutionHandoffBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRepairExecutionHandoffBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-owner-repair-execution-handoff-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    handoff = payload["api_owner_repair_execution_handoff"]
    require(handoff["schema"] == "account-console.p024.partial-fill-owner-repair-execution-handoff-bundle.v1", "API schema mismatch")
    require(handoff["status"] == "phase4z_owner_repair_execution_handoff_bundle_ready", "API status mismatch")
    require(handoff["step_count"] == 7, "step count mismatch")
    require(handoff["artifact_count"] == 7, "artifact count mismatch")
    require(handoff["execution_allowed"] is False, "execution flag mismatch")
    require(handoff["owner_repo_write_allowed"] is False, "owner write mismatch")
    require(handoff["runtime_retry_authorized"] is False, "runtime retry mismatch")
    require(handoff["exact_approval_required"] is True, "approval requirement mismatch")
    require(handoff["owner_patch_applied"] is False, "patch applied mismatch")
    require(handoff["full_acceptance_claimed"] is False, "full claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "handoff_panel_visible",
        "steps_displayed",
        "artifacts_displayed",
        "execution_displayed_false",
        "owner_write_displayed_false",
        "runtime_retry_displayed_false",
        "exact_approval_displayed_true",
        "patch_applied_displayed_false",
        "full_acceptance_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-execution-handoff-bundle"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "handoff route must be GET-only")
    require(found, "handoff route missing")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-execution-handoff-bundle")
    require(response.status_code == 200, "handoff API does not return 200")
    payload = response.json()
    require(payload["execution_guard"]["execution_allowed"] is False, "API execution flag mismatch")
    require(payload["negative_assertions"]["full_acceptance_claimed"] is False, "API full claim mismatch")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_EXECUTION_HANDOFF_BROWSER_EVIDENCE_OK: "
        "ui=pass execution=false runtime_retry=false"
    )


if __name__ == "__main__":
    main()
