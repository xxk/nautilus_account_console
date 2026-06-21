from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls" / "partial-fill-post-repair-runtime-attempt-ui.json"


class P024PartialFillPostRepairRuntimeAttemptBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillPostRepairRuntimeAttemptBrowserEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-post-repair-runtime-attempt-ui.v1", "schema mismatch")
    require(payload["verdict"] == "pass", "browser verdict mismatch")
    api = payload["api_post_repair_runtime_attempt"]
    require(api["status"] == "phase4zf_post_repair_runtime_attempt_full_fill_blocker_recorded", "status mismatch")
    require(api["filled_quantity"] == 1, "filled quantity mismatch")
    require(api["remaining_quantity"] == 0, "remaining quantity mismatch")
    require(api["partial_fill_formula_satisfied"] is False, "partial-fill formula must be false")
    require(api["real_paper_order_created"] is True, "real paper order not shown")
    require(api["partial_fill_then_cancel_acceptance_satisfied"] is False, "partial-fill acceptance must remain false")
    require(api["additional_runtime_retry_authorized"] is False, "retry should be false")
    checks = payload["browser_checks"]
    for key in [
        "attempt_panel_visible",
        "full_fill_displayed",
        "partial_fill_displayed_false",
        "retry_displayed_false",
        "position_delta_displayed",
        "artifacts_displayed",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check failed: {key}")
    screenshot = ROOT / payload["browser_evidence"][0]["screenshot"]
    require(screenshot.exists(), f"missing screenshot: {screenshot}")


def main() -> None:
    validate(load(EVIDENCE))
    print("P024_PARTIAL_FILL_POST_REPAIR_RUNTIME_ATTEMPT_BROWSER_EVIDENCE_OK: full_fill_not_partial retry=false")


if __name__ == "__main__":
    main()
