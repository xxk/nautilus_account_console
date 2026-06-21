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
    / "partial-fill-owner-repair-evidence-ingest-audit.json"
)


class P024PartialFillOwnerRepairEvidenceIngestAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillOwnerRepairEvidenceIngestAuditError(message)


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
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-evidence-ingest-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4zd_owner_repair_evidence_ingested", "status mismatch")
    require(
        payload["verdict"] == "owner_repair_evidence_recorded_runtime_retry_packet_required",
        "verdict mismatch",
    )

    owner = payload["owner_repair_evidence"]
    require(owner["owner_repo_ref"] == "owner-repo://nautilus_ctp_adapter", "owner repo ref mismatch")
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(len(owner["owner_repair_commit_ref"]) == 40, "owner commit ref shape mismatch")
    require(owner["owner_repair_commit_ref"].startswith("01db0f8"), "owner repair commit mismatch")
    require(owner["owner_repo_write_attempted"] is True, "owner write should be recorded")
    require(owner["owner_runtime_invocation_attempted"] is False, "runtime should not be invoked by repair audit")
    for key in ["raw_secret_values_recorded", "raw_broker_endpoint_recorded", "config_raw_content_recorded"]:
        require(owner[key] is False, f"owner sensitive negative assertion mismatch: {key}")

    checks = {item["path"]: item for item in payload["post_repair_source_checksums"]}
    require(len(checks) == 3, "source checksum count mismatch")
    require(
        checks["owner-repo://nautilus_ctp_adapter/scripts/ctp_guarded_paper_order_loop.py"]["sha256"]
        == "DBF9CCE8663B207C1BDE53BA0EEB320483C9E61F04443494059E5822555EE2BD",
        "guarded order loop checksum mismatch",
    )
    require(
        checks["owner-repo://nautilus_ctp_adapter/tests/test_guarded_paper_order_loop.py"]["required_symbol"]
        == "test_close_yesterday_owner_rule_blocks_callback_offset_as_submit_truth",
        "focused close-yesterday test missing",
    )
    require(
        "CLOSEYESTERDAY submit-boundary offset 4"
        in checks["owner-repo://nautilus_ctp_adapter/scripts/ctp_guarded_paper_order_loop.py"]["repair_assertion"],
        "close-yesterday repair assertion missing",
    )

    validators = {item["evidence_id"]: item for item in payload["owner_validator_refs"]}
    require(set(validators) == {"owner_focus_validator_result", "owner_integration_validator_result"}, "validator set mismatch")
    require(validators["owner_focus_validator_result"]["exit_code"] == 0, "focus validator failed")
    require("57 passed" in validators["owner_focus_validator_result"]["stdout_tail"], "focus validator output mismatch")
    require(validators["owner_integration_validator_result"]["exit_code"] == 0, "integration validator failed")
    require("88 passed" in validators["owner_integration_validator_result"]["stdout_tail"], "integration output mismatch")
    for item in validators.values():
        require(str(item["validator_run_sha256"]).startswith("sha256:"), "validator checksum missing")

    decision = payload["ingest_decision"]
    require(decision["owner_repair_evidence_recorded"] is True, "repair evidence not recorded")
    require(decision["owner_validators_passed"] is True, "validators not recorded as passed")
    require(decision["runtime_retry_authorized"] is False, "audit must not authorize runtime retry")
    require(decision["requires_post_repair_runtime_retry_packet"] is True, "retry packet requirement missing")
    require(decision["maximum_runtime_attempts_after_repair"] == 1, "runtime attempt cap mismatch")

    negative = payload["negative_assertions"]
    for key in [
        "owner_runtime_invocation_attempted",
        "post_repair_runtime_retry_claimed",
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
    validate_payload(load(AUDIT))
    print("P024_PARTIAL_FILL_OWNER_REPAIR_EVIDENCE_INGEST_AUDIT_OK: owner_repair_evidence=recorded runtime_retry=false")


if __name__ == "__main__":
    main()
