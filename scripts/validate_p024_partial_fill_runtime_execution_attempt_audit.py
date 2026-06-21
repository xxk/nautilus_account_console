from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-runtime-execution-attempt-audit.json"
)


class P024PartialFillRuntimeExecutionAttemptAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillRuntimeExecutionAttemptAuditError(message)


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
    text = AUDIT.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-runtime-execution-attempt-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(
        payload["status"] == "phase4n_partial_fill_runtime_attempt_rejected_blocker_recorded",
        "status mismatch",
    )
    require(
        payload["verdict"] == "real_owner_runtime_attempt_did_not_produce_partial_fill",
        "verdict mismatch",
    )

    approval = payload["operator_approval_basis"]
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require(approval["raw_secret_values_recorded"] is False, "approval raw secret flag mismatch")
    require(approval["raw_broker_endpoint_recorded"] is False, "approval raw endpoint flag mismatch")

    owner = payload["owner_runtime_refs"]
    require(owner["owner_ref"] == "owner://nautilus_ctp_adapter", "owner ref mismatch")
    require(
        "p024-partial-fill-runtime-20260621T174616p0800" in owner["run_dir_ref"],
        "owner run dir mismatch",
    )
    require(owner["config_raw_content_recorded"] is False, "config raw flag mismatch")

    artifacts = {artifact["artifact_id"]: artifact for artifact in payload["owner_artifacts"]}
    require(
        set(artifacts)
        == {
            "pre_snapshot_with_reducible_position",
            "submit_owner_runtime_dry_run",
            "submit_owner_runtime_result",
            "post_submit_readback",
            "md_login_tick_blocker",
        },
        "artifact set mismatch",
    )
    for artifact in artifacts.values():
        require(artifact["ref"].startswith("owner-repo://nautilus_ctp_adapter/"), "artifact ref owner mismatch")
        require(len(artifact["sha256"]) == 64, f"artifact checksum mismatch: {artifact['artifact_id']}")

    attempt = payload["attempt"]
    require(attempt["instrument"] == "rb2610", "instrument mismatch")
    require(attempt["side"] == "SELL", "side mismatch")
    require(attempt["quantity"] == 3, "quantity mismatch")
    require(attempt["position_effect"] == "CLOSEYESTERDAY", "position effect mismatch")
    require(attempt["paper_send_armed"] is True, "paper send armed mismatch")
    require(attempt["close_intent_accepted"] is True, "close intent mismatch")
    require(attempt["verified_exposure_reduction"] is True, "exposure reduction mismatch")
    require(attempt["projected_net_position"] == 0, "projected net mismatch")
    require(attempt["session_send_budget"] == 1, "send budget mismatch")

    observed = payload["observed_owner_runtime_result"]
    require(observed["submit_status"] == "blocked", "submit status mismatch")
    require(observed["submit_success"] is False, "submit success mismatch")
    require(observed["matched_exec_count"] == 1, "matched exec count mismatch")
    require(observed["callback_source"] == "OnRspOrderInsert", "callback source mismatch")
    require(observed["response_error_id"] == 1009, "response error mismatch")
    require(
        observed["broker_rejection_disposition"]
        == "source_bearing_order_insert_insufficient_position_close_rejection",
        "broker rejection mismatch",
    )
    require(observed["filled_quantity"] == 0, "filled quantity mismatch")
    require(observed["partial_fill_observed"] is False, "partial fill flag mismatch")
    require(observed["cancel_identity_available"] is False, "cancel identity mismatch")
    require(observed["cancel_sent"] is False, "cancel sent mismatch")

    readback = payload["post_attempt_readback"]
    require(readback["rb2610_long_position_qty_before"] == 3, "pre position mismatch")
    require(readback["rb2610_long_position_qty_after"] == 3, "post position mismatch")
    require(readback["position_changed"] is False, "position changed mismatch")
    require(readback["observed_order_event_count"] == 0, "readback order event mismatch")
    require(readback["observed_trade_event_count"] == 0, "readback trade event mismatch")

    classification = payload["classification"]
    require(
        classification["classification_id"] == "rejected_before_partial_fill_not_partial_fill",
        "classification mismatch",
    )
    require(classification["non_ui_partial_fill_runtime_acceptance"] == "blocked", "non-ui status mismatch")
    require(classification["web_ui_real_partial_fill_runtime_acceptance"] == "blocked", "web-ui status mismatch")
    require(classification["full_acceptance_claimed"] is False, "full acceptance claim mismatch")

    negative = payload["negative_assertions"]
    for key in [
        "partial_fill_claimed",
        "cancel_sent",
        "browser_fixture_promoted_to_runtime_truth",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(AUDIT))
    print(
        "P024_PARTIAL_FILL_RUNTIME_EXECUTION_ATTEMPT_AUDIT_OK: "
        "owner_attempt=paper_send_rejected partial_fill_observed=false cancel_sent=false"
    )


if __name__ == "__main__":
    main()
