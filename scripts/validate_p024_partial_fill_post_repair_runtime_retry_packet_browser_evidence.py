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
    / "partial-fill-post-repair-runtime-retry-packet-ui.json"
)


class P024PartialFillPostRepairRuntimeRetryPacketBrowserEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillPostRepairRuntimeRetryPacketBrowserEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-post-repair-runtime-retry-packet-ui.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["verdict"] == "pass", "browser verdict mismatch")
    api = payload["api_post_repair_runtime_retry_packet"]
    require(api["status"] == "phase4ze_post_repair_runtime_retry_approval_packet_ready", "api status mismatch")
    require(api["runtime_retry_authorized_by_packet"] is True, "retry authorization not displayed")
    require(api["maximum_attempts"] == 1, "attempt cap mismatch")
    require(api["exposure_reduction_only"] is True, "exposure reduction guard mismatch")
    require(api["required_runtime_evidence_count"] == 7, "runtime requirement count mismatch")
    require(api["owner_runtime_invocation_attempted_by_packet"] is False, "packet must not claim invocation")
    require(api["real_partial_fill_claimed"] is False, "packet must not claim real partial fill")
    checks = payload["browser_checks"]
    for key in [
        "retry_packet_panel_visible",
        "authorized_displayed_true",
        "max_attempts_displayed_one",
        "exposure_reduction_displayed_true",
        "runtime_requirements_displayed",
        "runtime_invoked_displayed_false",
        "real_partial_fill_displayed_false",
        "sensitive_endpoint_wording_absent",
    ]:
        require(checks[key] is True, f"browser check failed: {key}")
    screenshot = ROOT / payload["browser_evidence"][0]["screenshot"]
    require(screenshot.exists(), f"missing screenshot: {screenshot}")


def main() -> None:
    validate(load(EVIDENCE))
    print("P024_PARTIAL_FILL_POST_REPAIR_RUNTIME_RETRY_PACKET_BROWSER_EVIDENCE_OK: verdict=pass")


if __name__ == "__main__":
    main()
