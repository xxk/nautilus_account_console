from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "acceptance" / "p024-account-console-paper-command-controls" / "partial-fill-post-repair-runtime-attempt-audit.json"


class P024PartialFillPostRepairRuntimeAttemptAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillPostRepairRuntimeAttemptAuditError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text() -> list[str]:
    fragments = ["password", "authcode", "auth_code", "tcp://", "trading.openctp", "frontaddress", "broker_secret", "account_secret"]
    text = AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.partial-fill-post-repair-runtime-attempt-audit.v1", "schema mismatch")
    require(payload["status"] == "phase4zf_post_repair_runtime_attempt_full_fill_blocker_recorded", "status mismatch")
    require(payload["verdict"] == "real_paper_order_filled_not_partial_fill_no_cancel_remainder", "verdict mismatch")
    attempt = payload["owner_runtime_attempt"]
    require(attempt["owner_runtime_artifacts_commit_ref"].startswith("ef17af2"), "owner runtime artifact commit mismatch")
    require(attempt["runtime_attempt_count_consumed"] == 1, "attempt count mismatch")
    require(attempt["additional_runtime_retry_authorized"] is False, "retry should not remain authorized")
    require(attempt["quantity"] == 1, "small order quantity mismatch")
    require(attempt["paper_send_armed"] is True, "paper send was not armed")
    artifacts = payload["owner_artifact_refs"]
    require(len(artifacts) == 3, "artifact count mismatch")
    for item in artifacts:
        require(str(item["ref"]).startswith("owner-repo://nautilus_ctp_adapter/output/account_command/ctp-paper-19053/"), "artifact ref mismatch")
        require(len(item["sha256"]) == 64, "artifact checksum mismatch")
    obs = payload["runtime_observation"]
    require(obs["submitted_quantity"] == 1, "submitted quantity mismatch")
    require(obs["filled_quantity"] == 1, "filled quantity mismatch")
    require(obs["remaining_quantity"] == 0, "remaining quantity mismatch")
    require(obs["partial_fill_formula_satisfied"] is False, "should not satisfy partial-fill formula")
    require(obs["cancel_attempted"] is False, "cancel should not be attempted after full fill")
    delta = payload["position_readback_delta"]
    require(delta["pre_position_qty"] == 3 and delta["post_position_qty"] == 2, "position delta mismatch")
    require(delta["exposure_reduction_observed"] is True, "exposure reduction not observed")
    decision = payload["acceptance_decision"]
    require(decision["real_paper_order_created"] is True, "real paper order not recorded")
    require(decision["real_paper_fill_observed"] is True, "real fill not recorded")
    require(decision["partial_fill_then_cancel_acceptance_satisfied"] is False, "partial-fill acceptance must remain false")
    negative = payload["negative_assertions"]
    for key in [
        "additional_runtime_retry_authorized",
        "cancel_sent",
        "real_partial_fill_claimed",
        "web_ui_real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate(load(AUDIT))
    print("P024_PARTIAL_FILL_POST_REPAIR_RUNTIME_ATTEMPT_AUDIT_OK: full_fill_not_partial retry_consumed=true")


if __name__ == "__main__":
    main()
