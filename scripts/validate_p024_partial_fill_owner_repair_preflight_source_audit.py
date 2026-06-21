from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = Path("D:/Nautilus/nautilus_ctp_adapter")
AUDIT = (
    ROOT
    / "docs"
    / "acceptance"
    / "p024-account-console-paper-command-controls"
    / "partial-fill-owner-repair-preflight-source-audit.json"
)


class P024OwnerRepairPreflightSourceAuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024OwnerRepairPreflightSourceAuditError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    payload = load_json(AUDIT)
    require(
        payload["schema"] == "account-console.p024.partial-fill-owner-repair-preflight-source-audit.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["status"] == "phase4v_owner_repair_preflight_source_audited", "status mismatch")
    require(payload["verdict"] == "owner_repair_still_required_before_runtime_retry", "verdict mismatch")
    owner = payload["owner_repo"]
    require(owner["owner_repo_path"] == "D:/Nautilus/nautilus_ctp_adapter", "owner path mismatch")
    require(owner["write_attempted_by_audit"] is False, "audit must be read-only")

    checks = {item["path"]: item for item in payload["source_checks"]}
    require(
        set(checks)
        == {
            "scripts/ctp_guarded_paper_order_loop.py",
            "tests/test_guarded_paper_order_loop.py",
            "tests/test_nautilus_integration.py",
        },
        "source check set mismatch",
    )
    for rel_path, item in checks.items():
        path = OWNER_ROOT / rel_path
        require(path.exists(), f"owner source missing: {rel_path}")
        require(item["sha256"] == sha256(path), f"owner source checksum mismatch: {rel_path}")
        require(item["required_symbol_present"] is True, f"required symbol flag mismatch: {rel_path}")

    order_loop = (OWNER_ROOT / "scripts" / "ctp_guarded_paper_order_loop.py").read_text(encoding="utf-8")
    tests = (OWNER_ROOT / "tests" / "test_guarded_paper_order_loop.py").read_text(encoding="utf-8")
    require("def build_close_offset_owner_rule_semantics" in order_loop, "owner rule function missing")
    require('position_effect == "CLOSETODAY"' in order_loop, "current CLOSETODAY diagnostic gate missing")
    require('expected_offset == "3"' in order_loop, "current offset 3 diagnostic gate missing")
    require("close_yesterday_submit_observed" not in order_loop, "owner source already has unrecorded close-yesterday repair")
    require(
        'expected_submit_offset_from_position_effect"] == "4"' not in tests,
        "focused close-yesterday offset 4 assertion already present but not ingested",
    )

    approval = payload["operator_approval_delta"]
    require(approval["sufficient_for_owner_code_repair"] is False, "approval delta repair flag mismatch")
    require(approval["sufficient_for_post_repair_runtime_retry"] is False, "approval delta retry flag mismatch")
    require("repair owner close-offset semantics" in approval["required_exact_approval_before_owner_write_or_retry"], "exact approval text missing repair scope")
    next_action = payload["next_required_action"]
    require(next_action["owner_code_repair_allowed_by_current_audit"] is False, "owner repair allowed unexpectedly")
    require(next_action["owner_runtime_retry_allowed_by_current_audit"] is False, "runtime retry allowed unexpectedly")
    require(next_action["blind_script_retry_rejected"] is True, "blind retry rejection missing")
    negative = payload["negative_assertions"]
    for key in [
        "owner_repo_write_attempted",
        "owner_code_repair_claimed",
        "owner_validator_pass_claimed",
        "owner_runtime_invocation_attempted",
        "post_repair_runtime_retry_authorized",
        "real_partial_fill_claimed",
        "full_acceptance_claimed",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "config_raw_content_recorded",
    ]:
        require(negative[key] is False, f"negative assertion mismatch: {key}")
    print(
        "P024_PARTIAL_FILL_OWNER_REPAIR_PREFLIGHT_SOURCE_AUDIT_OK: "
        "owner_repair_required=true blind_retry_rejected=true owner_write=false"
    )


if __name__ == "__main__":
    main()
