from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ATTEMPT_AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "owner-runtime-execution-attempt-audit.json"
)


class P024OwnerRuntimeExecutionAttemptAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRuntimeExecutionAttemptAuditError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text() -> list[str]:
    fragments = [
        "password",
        "authcode",
        "auth_code",
        "tcp://",
        "trading.openctp",
        "frontaddress",
        "broker_secret",
        "account_secret",
    ]
    payload = ATTEMPT_AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in payload]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.owner-runtime-execution-attempt-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4f_owner_runtime_execution_attempted_readback_blocked",
        "status mismatch",
    )
    require(payload["verdict"] == "blocked_pending_order_readback_identity", "verdict mismatch")

    approval = payload["operator_approval"]
    require(approval["required"] is True, "approval required mismatch")
    require(approval["obtained"] is True, "approval obtained mismatch")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")

    owner = payload["owner_runtime_refs"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(owner["config_raw_content_recorded"] is False, "config raw content flag mismatch")
    require(owner["submit_entrypoint_ref"] == "scripts/ctp_guarded_paper_order_loop.py", "submit entrypoint mismatch")
    require(owner["cancel_entrypoint_ref"] == "scripts/ctp_guarded_paper_cancel_loop.py", "cancel entrypoint mismatch")

    attempt = payload["runtime_attempt"]
    require(attempt["instrument"] == "rb2610", "instrument mismatch")
    require(attempt["risk_shape"] == "exposure_reduction_only", "risk shape mismatch")
    require(attempt["paper_send_attempted"] is True, "paper send attempt mismatch")
    require(attempt["paper_cancel_attempted"] is True, "paper cancel attempt mismatch")
    require(attempt["browser_triggered_broker_order"] is False, "browser trigger mismatch")

    artifacts = {artifact["kind"]: artifact for artifact in payload["owner_artifacts"]}
    require(
        set(artifacts)
        == {
            "submit_dry_run",
            "submit_armed_send",
            "cancel_armed_send_initial_guard_block",
            "cancel_armed_send",
            "post_cancel_readonly_snapshot",
            "td_order_truth_after_cancel",
            "query_adapter_order_readback_after_cancel",
        },
        "artifact kind set mismatch",
    )
    for artifact in artifacts.values():
        require(artifact["owner_path"].startswith("output/account-console-ctp19053-readback/"), "owner path mismatch")
        require(len(artifact["sha256"]) == 64, f"sha256 length mismatch: {artifact['kind']}")
    require(artifacts["submit_armed_send"]["status"] == "passed", "submit send status mismatch")
    require(artifacts["submit_armed_send"]["observed"]["native_order_ref_present"] is True, "submit order ref missing")
    require(artifacts["submit_armed_send"]["observed"]["leaves_qty"] == 1, "submit leaves qty mismatch")
    require(artifacts["cancel_armed_send"]["status"] == "passed", "cancel send status mismatch")
    require(artifacts["cancel_armed_send"]["observed"]["native_code"] == 0, "cancel native code mismatch")
    require(
        artifacts["post_cancel_readonly_snapshot"]["observed"]["observed_order_event_count"] == 0,
        "post cancel readonly order count must document the blocker",
    )
    require(
        artifacts["td_order_truth_after_cancel"]["observed"]["observed_order_event_count"] == 0,
        "order truth count must document the blocker",
    )
    require(
        artifacts["query_adapter_order_readback_after_cancel"]["observed"][
            "order_truth_observed_order_event_count"
        ]
        == 0,
        "query adapter order truth count must document the blocker",
    )

    result = payload["a4_acceptance_result"]
    require(result["submit_runtime_executed"] is True, "A4 submit runtime mismatch")
    require(result["cancel_runtime_executed"] is True, "A4 cancel runtime mismatch")
    require(result["post_submit_readback_identity_observed"] is True, "A4 submit readback mismatch")
    require(result["post_cancel_readback_identity_observed"] is False, "A4 cancel readback blocker mismatch")
    require(result["can_claim_web_ui_order_display_correctness"] is False, "UI correctness claim mismatch")
    require(result["can_claim_all_acceptance_complete"] is False, "all acceptance claim mismatch")

    blockers = {blocker["blocker_id"] for blocker in payload["residual_blockers"]}
    require(
        blockers
        == {
            "p024_post_cancel_order_readback_identity_missing",
            "p024_real_partial_fill_runtime_missing",
        },
        "residual blocker mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "final_acceptance_claimed",
        "browser_triggered_broker_order",
        "account_mirror_write_authority",
        "live_armed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
        "web_ui_order_display_correctness_claimed",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(ATTEMPT_AUDIT))
    print(
        "P024_OWNER_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK: "
        "verdict=blocked_pending_order_readback_identity submit=true cancel=true final_acceptance=false"
    )


if __name__ == "__main__":
    main()
