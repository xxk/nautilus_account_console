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
    / "partial-fill-close-offset-owner-rule-gap-audit.json"
)


class P024PartialFillCloseOffsetOwnerRuleGapAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024PartialFillCloseOffsetOwnerRuleGapAuditError(message)


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
        payload["schema"] == "account-console.p024.partial-fill-close-offset-owner-rule-gap-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4o_close_yesterday_owner_rule_gap_audited", "status mismatch")
    require(
        payload["verdict"] == "blocked_pending_owner_close_offset_semantics_repair_or_primary_rule_source",
        "verdict mismatch",
    )

    depends = payload["depends_on"]
    require(
        depends["attempt_audit_ref"]
        == "docs/acceptance/p024-account-console-paper-command-controls/partial-fill-runtime-execution-attempt-audit.json",
        "attempt dependency mismatch",
    )
    require(len(depends["owner_attempt_result_sha256"]) == 64, "attempt checksum mismatch")

    observed = payload["observed_runtime_semantics"]
    require(observed["position_effect"] == "CLOSEYESTERDAY", "position effect mismatch")
    require(observed["submit_native_comb_offset"] == "4", "submit offset mismatch")
    require(observed["native_submit_boundary_offset_flags"] == ["4"], "submit boundary mismatch")
    require(observed["native_submit_boundary_matches_command_payload"] is True, "submit boundary flag mismatch")
    require(observed["callback_source"] == "OnRspOrderInsert", "callback source mismatch")
    require(observed["callback_offset_flags"] == ["1"], "callback offset mismatch")
    require(observed["callback_offset_authority"] == "front_response_diagnostic", "callback authority mismatch")
    require(observed["callback_offset_rewrites_submit_truth"] is False, "callback rewrite flag mismatch")
    require(observed["order_insert_response_offset_mismatch"] is True, "offset mismatch flag mismatch")
    require(observed["response_error_id"] == 1009, "response error mismatch")
    require(observed["filled_quantity"] == 0, "filled quantity mismatch")
    require(observed["partial_fill_observed"] is False, "partial fill flag mismatch")

    source_refs = {item["source_id"]: item for item in payload["owner_source_refs"]}
    require(
        set(source_refs) == {"guarded_order_loop", "execution_client", "guarded_order_loop_tests"},
        "source ref set mismatch",
    )
    for item in source_refs.values():
        require(item["ref"].startswith("owner-repo://nautilus_ctp_adapter/"), "source owner ref mismatch")
        require(len(item["sha256"]) == 64, f"source checksum mismatch: {item['source_id']}")
    require("CLOSEYESTERDAY" in source_refs["guarded_order_loop"]["observed_gap"], "guarded loop gap mismatch")
    require("CLOSEYESTERDAY -> 4" in source_refs["execution_client"]["observed_gap"], "execution mapping gap mismatch")

    repair = payload["repair_acceptance_shape"]
    require(repair["owner_repo_write_required"] is True, "owner write requirement mismatch")
    require(repair["approval_required_before_owner_write"] is True, "approval requirement mismatch")
    require(len(repair["expected_owner_changes"]) == 3, "owner change count mismatch")
    require(
        "python -m pytest tests/test_guarded_paper_order_loop.py -q" in repair["required_owner_validators"],
        "guarded loop validator missing",
    )

    retry = payload["retry_policy"]
    require(retry["additional_partial_fill_order_authorized"] is False, "retry authorization mismatch")
    require("at most one additional guarded OpenCTP paper partial-fill attempt" in retry["required_exact_approval_before_retry"], "retry approval text mismatch")

    blockers = {blocker["blocker_id"]: blocker for blocker in payload["residual_blockers"]}
    require(
        set(blockers) == {"p024_close_yesterday_owner_rule_gap", "p024_real_partial_fill_runtime_missing"},
        "residual blocker set mismatch",
    )

    negative = payload["negative_assertions"]
    for key in [
        "owner_repo_write_attempted_by_this_audit",
        "additional_order_authorized",
        "partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")


def main() -> None:
    leaks = scan_forbidden_text()
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(AUDIT))
    print(
        "P024_PARTIAL_FILL_CLOSE_OFFSET_OWNER_RULE_GAP_AUDIT_OK: "
        "close_yesterday_offset_gap=blocked retry_authorized=false"
    )


if __name__ == "__main__":
    main()
