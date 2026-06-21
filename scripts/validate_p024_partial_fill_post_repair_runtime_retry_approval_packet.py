from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-post-repair-runtime-retry-approval-packet.json"
)


class P024PartialFillPostRepairRuntimeRetryApprovalPacketError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillPostRepairRuntimeRetryApprovalPacketError(message)


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
    text = PACKET.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-post-repair-runtime-retry-approval-packet.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4ze_post_repair_runtime_retry_approval_packet_ready", "status mismatch")
    require(payload["verdict"] == "one_guarded_post_repair_paper_attempt_authorized", "verdict mismatch")

    depends = payload["depends_on"]
    require(
        depends["owner_repair_evidence_ingest_audit_status"] == "phase4zd_owner_repair_evidence_ingested",
        "repair ingest dependency mismatch",
    )
    require(depends["owner_repair_commit_ref"].startswith("01db0f8"), "owner repair commit dependency mismatch")
    require(depends["owner_focus_validator_exit_code"] == 0, "focus validator dependency mismatch")
    require(depends["owner_integration_validator_exit_code"] == 0, "integration validator dependency mismatch")
    require(depends["approval_packets_updated"] is True, "approval packet update flag mismatch")

    approval = payload["operator_approval"]
    require(approval["approval_obtained"] is True, "operator approval not recorded")
    require(approval["approval_path"] == "D:/Nautilus/nautilus_ctp_adapter", "approval path mismatch")
    require("at most one" in approval["scope"], "approval scope must cap attempts")

    guard = payload["runtime_retry_guard"]
    require(guard["runtime_retry_authorized_by_packet"] is True, "runtime retry should be authorized by packet")
    require(guard["maximum_attempts"] == 1, "maximum attempts mismatch")
    require(guard["account_id"] == "acct.ctp.paper.19053", "guard account mismatch")
    require(guard["simulation_user"] == "19053", "simulation user mismatch")
    require(guard["mode"] == "paper_armed", "mode mismatch")
    require(guard["exposure_reduction_only"] is True, "exposure reduction guard missing")
    require(guard["small_order_only"] is True, "small order guard missing")
    require(guard["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(guard["submit_entrypoint_ref"].endswith("scripts/ctp_guarded_paper_order_loop.py"), "submit entrypoint mismatch")
    require(guard["cancel_entrypoint_ref"].endswith("scripts/ctp_guarded_paper_cancel_loop.py"), "cancel entrypoint mismatch")
    for key in ["raw_secret_values_recorded", "raw_broker_endpoint_recorded", "config_raw_content_recorded"]:
        require(guard[key] is False, f"guard sensitive negative assertion mismatch: {key}")

    evidence = payload["required_runtime_evidence"]
    for phrase in [
        "pre_snapshot_with_reducible_position.json",
        "submit_owner_runtime_result.json",
        "post_submit_readback.json",
        "reconciliation artifact",
    ]:
        require(any(phrase in item for item in evidence), f"runtime evidence requirement missing: {phrase}")

    formula = payload["success_formula"]
    require(formula["partial_fill"] == "0 < filled_quantity < submitted_quantity", "partial-fill formula mismatch")
    require("remaining_quantity == 0" in formula["terminal_cancel"], "terminal cancel formula mismatch")

    fallback = payload["fallback_if_not_partial"]
    require(fallback["claim_full_acceptance"] is False, "fallback must not claim full acceptance")
    require(fallback["record_typed_blocker"] is True, "fallback blocker missing")

    negative = payload["negative_assertions_before_runtime"]
    for key in [
        "owner_runtime_invocation_attempted_by_packet",
        "paper_order_created_by_packet",
        "paper_cancel_sent_by_packet",
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
    validate_payload(load(PACKET))
    print("P024_PARTIAL_FILL_POST_REPAIR_RUNTIME_RETRY_APPROVAL_PACKET_OK: authorized_attempts=1 pre_runtime_claims=false")


if __name__ == "__main__":
    main()
