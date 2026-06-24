from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-preflight-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-preflight-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024PartialFillOwnerRepairPreflightBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairPreflightBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-owner-repair-preflight-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    audit = payload["api_owner_repair_preflight"]
    require(
        audit["schema"] == "account-console.p024.partial-fill-owner-repair-preflight-source-audit.v1",
        "API schema mismatch",
    )
    require(audit["status"] == "phase4v_owner_repair_preflight_source_audited", "API status mismatch")
    require(audit["verdict"] == "owner_repair_still_required_before_runtime_retry", "API verdict mismatch")
    require(audit["source_check_count"] == 3, "source check count mismatch")
    require(audit["owner_repo_write_attempted"] is False, "owner write mismatch")
    require(audit["repair_approval_sufficient"] is False, "repair approval mismatch")
    require(audit["retry_approval_sufficient"] is False, "retry approval mismatch")
    require(audit["blind_script_retry_rejected"] is True, "blind retry mismatch")
    require(audit["runtime_invocation_attempted"] is False, "runtime invocation mismatch")
    require(audit["full_acceptance_claimed"] is False, "full claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "preflight_panel_visible",
        "source_checks_displayed",
        "owner_write_displayed_false",
        "repair_approval_displayed_false",
        "retry_approval_displayed_false",
        "blind_retry_displayed_true",
        "runtime_invoked_displayed_false",
        "full_acceptance_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-preflight-source-audit"
    require(all(getattr(item, "path", "") != route for item in app.routes), "preflight route should be retired")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-preflight-source-audit")
    require(response.status_code == 404, "preflight API retirement mismatch")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_BROWSER_EVIDENCE_OK: "
        "ui=archive_only_historical_evidence route=retired_404 blind_retry_rejected=true owner_write=false"
    )


if __name__ == "__main__":
    main()
