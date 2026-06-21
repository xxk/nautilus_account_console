from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-patch-preview-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-patch-preview-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024PartialFillOwnerRepairPatchPreviewBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairPatchPreviewBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-owner-repair-patch-preview-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    preview = payload["api_owner_repair_patch_preview"]
    require(preview["schema"] == "account-console.p024.partial-fill-owner-repair-patch-preview.v1", "API schema mismatch")
    require(preview["status"] == "phase4x_owner_repair_patch_preview_ready", "API status mismatch")
    require(preview["verdict"] == "patch_preview_ready_owner_write_not_authorized", "API verdict mismatch")
    require(preview["baseline_file_count"] == 2, "baseline count mismatch")
    require(preview["patch_count"] == 3, "patch count mismatch")
    require(preview["validator_count"] == 3, "validator count mismatch")
    require(preview["owner_repo_write_attempted"] is False, "owner write mismatch")
    require(preview["runtime_retry_authorized"] is False, "runtime retry mismatch")
    require(preview["fresh_retry_approval_required"] is True, "fresh approval mismatch")
    require(preview["owner_patch_applied"] is False, "patch applied mismatch")
    require(preview["full_acceptance_claimed"] is False, "full claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "patch_preview_panel_visible",
        "baseline_files_displayed",
        "patches_displayed",
        "validators_displayed",
        "owner_write_displayed_false",
        "runtime_retry_displayed_false",
        "fresh_approval_displayed_true",
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

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-patch-preview"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "patch preview route must be GET-only")
    require(found, "patch preview route missing")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-patch-preview")
    require(response.status_code == 200, "patch preview API does not return 200")
    payload = response.json()
    require(payload["post_patch_runtime_gate"]["runtime_retry_authorized_by_preview"] is False, "API retry flag mismatch")
    require(payload["negative_assertions"]["owner_patch_applied"] is False, "API patch flag mismatch")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_PATCH_PREVIEW_BROWSER_EVIDENCE_OK: "
        "ui=pass owner_write=false runtime_retry=false"
    )


if __name__ == "__main__":
    main()
