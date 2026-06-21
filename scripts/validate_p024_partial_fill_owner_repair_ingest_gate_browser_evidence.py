from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "partial-fill-owner-repair-ingest-gate-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-partial-fill-owner-repair-ingest-gate-ui.png"
ACCOUNT_ID = "acct.ctp.paper.19053"


class P024PartialFillOwnerRepairIngestGateBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairIngestGateBrowserEvidenceError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-owner-repair-ingest-gate-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    gate = payload["api_owner_repair_ingest_gate"]
    require(gate["schema"] == "account-console.p024.partial-fill-owner-repair-evidence-ingest-gate.v1", "API schema mismatch")
    require(gate["status"] == "phase4t_owner_repair_evidence_ingest_gate_ready", "API status mismatch")
    require(gate["required_evidence_count"] == 6, "required evidence count mismatch")
    require(gate["update_count"] == 5, "update count mismatch")
    require(gate["reject_rule_count"] == 6, "reject count mismatch")
    require(gate["runtime_retry_allowed"] is False, "runtime retry mismatch")
    require(gate["runtime_evidence_allowed"] is False, "runtime evidence mismatch")
    require(gate["owner_repair_evidence_recorded"] is False, "repair evidence flag mismatch")
    require(gate["full_acceptance_claimed"] is False, "full claim mismatch")
    checks = payload["browser_checks"]
    for key in [
        "ingest_gate_panel_visible",
        "runtime_retry_displayed_false",
        "runtime_evidence_displayed_false",
        "required_evidence_displayed",
        "update_items_displayed",
        "reject_rules_displayed",
        "owner_repair_evidence_recorded_displayed_false",
        "full_acceptance_claimed_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check mismatch: {key}")
    require(SCREENSHOT.exists(), "missing screenshot")


def validate_route() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/partial-fill-owner-repair-evidence-ingest-gate"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "ingest gate route must be GET-only")
    require(found, "ingest gate route missing")
    response = TestClient(app).get(f"/api/commands/accounts/{ACCOUNT_ID}/partial-fill-owner-repair-evidence-ingest-gate")
    require(response.status_code == 200, "ingest gate API does not return 200")
    payload = response.json()
    require(payload["ingest_scope"]["runtime_retry_allowed_by_ingest_gate"] is False, "API retry flag mismatch")
    require(payload["negative_assertions"]["owner_repair_evidence_recorded"] is False, "API evidence flag mismatch")


def main() -> None:
    validate_evidence(load_json(EVIDENCE))
    validate_route()
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_INGEST_GATE_BROWSER_EVIDENCE_OK: "
        "ui=pass evidence_missing=true runtime_retry=false"
    )


if __name__ == "__main__":
    main()
