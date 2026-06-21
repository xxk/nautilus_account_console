from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATE = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-evidence-ingest-gate.json"
)


class P024PartialFillOwnerRepairEvidenceIngestGateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairEvidenceIngestGateError(message)


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
    text = GATE.read_text(encoding="utf-8", errors="ignore").lower()
    return [fragment for fragment in fragments if fragment in text]


def validate_payload(payload: dict[str, Any]) -> None:
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-evidence-ingest-gate.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4t_owner_repair_evidence_ingest_gate_ready", "status mismatch")
    require(
        payload["verdict"] == "ingest_gate_ready_owner_repair_evidence_missing",
        "verdict mismatch",
    )

    depends = payload["depends_on"]
    require(
        depends["owner_repair_plan_status"] == "phase4r_owner_close_offset_repair_implementation_plan_ready",
        "repair plan dependency mismatch",
    )
    require(depends["owner_repair_plan_ui_verdict"] == "pass", "repair plan UI dependency mismatch")

    scope = payload["ingest_scope"]
    require(scope["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(scope["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner repo path mismatch")
    require(scope["raw_secret_values_allowed"] is False, "raw secret allowance mismatch")
    require(scope["raw_broker_endpoint_allowed"] is False, "raw endpoint allowance mismatch")
    require(scope["config_raw_content_allowed"] is False, "raw config allowance mismatch")
    require(scope["runtime_retry_allowed_by_ingest_gate"] is False, "runtime retry allowance mismatch")
    require(scope["accepts_owner_code_repair_evidence"] is True, "owner code evidence allowance mismatch")
    require(scope["accepts_owner_runtime_partial_fill_evidence"] is False, "runtime evidence allowance mismatch")

    evidence = {item["evidence_id"]: item for item in payload["required_owner_repair_evidence"]}
    require(
        set(evidence)
        == {
            "owner_repair_commit",
            "guarded_order_loop_source_checksum",
            "focused_owner_tests_checksum",
            "owner_focus_validator_result",
            "owner_integration_validator_result",
            "account_console_ingest_audit",
        },
        "required evidence set mismatch",
    )
    for item in evidence.values():
        require(item["current_status"] == "missing", f"evidence should still be missing: {item['evidence_id']}")
        require(item["must_include"], f"must_include missing for: {item['evidence_id']}")
    require(
        "build_close_offset_owner_rule_semantics" in evidence["guarded_order_loop_source_checksum"]["must_include"],
        "owner rule symbol requirement missing",
    )
    require(
        "expected_submit_offset_from_position_effect == 4"
        in evidence["focused_owner_tests_checksum"]["must_include"],
        "CLOSEYESTERDAY focused assertion missing",
    )
    require(
        "exit_code=0" in evidence["owner_focus_validator_result"]["must_include"],
        "focus validator pass requirement missing",
    )
    require(
        "runtime_retry_authorized=false" in evidence["account_console_ingest_audit"]["must_include"],
        "console ingest no-retry requirement missing",
    )

    updates = payload["post_ingest_required_account_console_updates"]
    for phrase in [
        "update partial-fill remaining acceptance current-state audit",
        "update partial-fill runtime approval packet and handoff bundle",
        "validate_p024_partial_fill_owner_repair_evidence_ingest_gate.py",
        "validate_p024_paper_command_controls_design.py",
        "keep runtime retry disallowed",
    ]:
        require(any(phrase in item for item in updates), f"post-ingest update missing: {phrase}")

    rejects = payload["reject_evidence_if"]
    for phrase in [
        "owner commit/ref is missing",
        "CLOSEYESTERDAY offset 4",
        "owner validator command is missing",
        "raw secrets",
        "runtime retry",
    ]:
        require(any(phrase in item for item in rejects), f"reject rule missing: {phrase}")

    negative = payload["negative_assertions"]
    for key in [
        "owner_repair_evidence_recorded",
        "owner_repo_write_attempted_by_this_gate",
        "owner_runtime_invocation_attempted",
        "runtime_retry_authorized",
        "partial_fill_runtime_claimed",
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
    validate_payload(load(GATE))
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_GATE_OK: "
        "owner_repair_evidence=missing runtime_retry=false"
    )


if __name__ == "__main__":
    main()
