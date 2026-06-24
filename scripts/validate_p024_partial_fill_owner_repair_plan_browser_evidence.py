from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
)
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-plan-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-plan-ui.png"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p024-partial-fill-owner-repair-plan.spec.ts"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
HISTORICAL_TYPES = ROOT / "frontend" / "src" / "types-historical-p024.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024PartialFillOwnerRepairPlanBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairPlanBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def validate_evidence(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-plan-ui.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    plan = payload["api_owner_repair_plan"]
    require(
        plan["schema"] == "account-console.p024.partial-fill-owner-repair-implementation-plan.v1",
        "API schema mismatch",
    )
    require(
        plan["status"] == "phase4r_owner_close_offset_repair_implementation_plan_ready",
        "API status mismatch",
    )
    require(plan["verdict"] == "owner_repair_plan_ready_no_owner_write_attempted", "API verdict mismatch")
    require(plan["source_ref_count"] == 3, "source ref count mismatch")
    require(plan["planned_change_count"] == 3, "planned change count mismatch")
    require(plan["validator_count"] == 4, "validator count mismatch")
    require(plan["forbidden_shape_count"] == 5, "forbidden shape count mismatch")
    require(plan["owner_repo_write_attempted"] is False, "owner write flag mismatch")
    require(plan["runtime_attempt_allowed"] is False, "runtime retry flag mismatch")
    require(plan["fresh_approval_required"] is True, "fresh approval flag mismatch")
    require(plan["partial_fill_claimed"] is False, "partial fill claim mismatch")
    require(plan["full_acceptance_claimed"] is False, "full acceptance claim mismatch")
    require(plan["raw_secret_values_recorded"] is False, "raw secret flag mismatch")
    require(plan["raw_broker_endpoint_recorded"] is False, "raw endpoint flag mismatch")
    checks = payload["browser_checks"]
    for key in [
        "repair_plan_panel_visible",
        "status_displayed",
        "owner_path_displayed",
        "owner_write_displayed_false",
        "runtime_retry_displayed_false",
        "fresh_approval_displayed_true",
        "close_yesterday_source_displayed",
        "planned_changes_displayed",
        "validators_displayed",
        "forbidden_shapes_displayed",
        "partial_fill_claimed_displayed_false",
        "full_acceptance_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route_and_frontend() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-implementation-plan"
    require(all(getattr(item, "path", "") != route for item in app.routes), "owner repair plan route should be retired")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-implementation-plan")
    require(response.status_code == 404, "owner repair plan API retirement mismatch")

    app_text = read(APP)
    api_text = read(API)
    types_text = read(HISTORICAL_TYPES)
    spec_text = read(SPEC)
    for phrase in [
        "CommandPartialFillOwnerRepairImplementationPlan",
        "partial-fill-owner-repair-implementation-plan",
        ]:
        require(phrase in app_text or phrase in api_text or phrase in types_text or phrase in spec_text, f"frontend phrase missing: {phrase}")
    require("fetchCommandPartialFillOwnerRepairImplementationPlan" not in api_text, "retired frontend API fetch should be removed")
    require("account-partial-fill-owner-repair-plan-panel" not in app_text, "retired frontend panel should be removed")
    for phrase in [
        "partial-fill-owner-repair-implementation-plan",
        "partial-fill-owner-repair-plan-ui.json",
        "p024-partial-fill-owner-repair-plan-ui.png",
        "CLOSEYESTERDAY expected/submit offset 4",
        "runtime retry authorized",
    ]:
        require(phrase in spec_text, f"spec phrase missing: {phrase}")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route_and_frontend()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_PLAN_BROWSER_EVIDENCE_OK: "
        "ui=archive_only_historical_evidence route=retired_404 owner_write=false runtime_retry=false"
    )


if __name__ == "__main__":
    main()
