from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "browser-evidence"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-ingest-audit-ui.json"
)


class P024PartialFillOwnerRepairIngestAuditBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairIngestAuditBrowserEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-ingest-audit-ui.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["verdict"] == "pass", "browser verdict mismatch")
    api = payload["api_owner_repair_ingest_audit"]
    require(api["status"] == "phase4zd_owner_repair_evidence_ingested", "api status mismatch")
    require(api["owner_repair_commit_ref"].startswith("01db0f8"), "commit ref mismatch")
    require(api["source_checksum_count"] == 3, "checksum count mismatch")
    require(api["validator_count"] == 2, "validator count mismatch")
    require(api["owner_repair_evidence_recorded"] is True, "repair evidence not displayed as recorded")
    require(api["runtime_retry_authorized"] is False, "audit UI must show retry false")
    require(api["real_partial_fill_claimed"] is False, "audit UI must not claim partial fill")
    checks = payload["browser_checks"]
    for key in [
        "ingest_audit_panel_visible",
        "commit_ref_displayed",
        "checksums_displayed",
        "validators_displayed",
        "owner_repair_evidence_recorded_displayed_true",
        "runtime_retry_displayed_false",
        "real_partial_fill_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check failed: {key}")
    screenshot = ROOT / payload["browser_evidence"][0]["screenshot"]
    require(screenshot.exists(), f"missing screenshot: {screenshot}")


def main() -> None:
    validate(load(EVIDENCE))
    print("P024_PARTIAL_FILL_OWNER_REPAIR_INGEST_AUDIT_BROWSER_EVIDENCE_OK: verdict=pass")


if __name__ == "__main__":
    main()
