from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "evidence-lane-manifest.json"
)
P018_README = ROOT / "docs" / "proposals" / "p018-ib-tws-readonly-account-console" / "README.md"
P018_ACCEPTANCE = ROOT / "docs" / "proposals" / "p018-ib-tws-readonly-account-console" / "acceptance.md"
P019_README = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "README.md"
P019_AUDIT = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "pre-implementation-audit.md"
)
P019_PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
P019_ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"


class EvidenceLaneError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceLaneError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def lane_by_id(payload: dict[str, Any], lane_id: str) -> dict[str, Any]:
    for lane in payload["lanes"]:
        if lane["lane_id"] == lane_id:
            return lane
    raise EvidenceLaneError(f"missing lane {lane_id}")


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    payload = load(MANIFEST)
    require(payload["schema"] == "account-console.p019-evidence-lane-manifest.v1", "manifest schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "manifest proposal mismatch")
    require(payload["adr_id"] == "ADR-0005", "manifest ADR mismatch")
    require(payload["status"] == "pre_acceptance_blocked", "manifest status must remain blocked")
    require(payload["blocker_id"] == "adr0005_not_accepted", "manifest blocker mismatch")
    require(payload["raw_secret_values_recorded"] is False, "manifest must not record raw secrets")

    p018_lane = lane_by_id(payload, "p018-owner-source-package")
    p019_lane = lane_by_id(payload, "p019-adr0005-governed-observation-session")
    synthetic_lane = lane_by_id(payload, "p019-synthetic-contract-ready-path")

    require(p018_lane["lane_kind"] == "owner_source_package", "P018 lane kind mismatch")
    require(p018_lane["authority_owner"] == "nautilus_strategies", "P018 owner mismatch")
    require(p018_lane["direct_session_allowed"] is False, "P018 lane cannot allow direct session")
    require(p018_lane["may_satisfy_p019_direct_observation_acceptance"] is False, "P018 cannot satisfy P019 direct observation acceptance")
    require(p018_lane["may_be_used_by_p019_with_explicit_mapping"] is True, "P018 mapping rule missing")
    for field in [
        "source_package_ref",
        "source_package_checksum",
        "source_package_collected_at",
        "mapped_to_contract",
        "mapping_owner",
        "raw_secret_values_recorded",
    ]:
        require(field in p018_lane["required_mapping_fields"], f"P018 mapping missing {field}")
    for root in [
        "owner-source-ref://p018/ib-tws/u3028269/",
        "docs/proposals/p018-ib-tws-readonly-account-console/",
    ]:
        require(root in p018_lane["allowed_evidence_roots"], f"P018 lane missing root {root}")

    require(p019_lane["lane_kind"] == "governed_observation_session", "P019 lane kind mismatch")
    require(p019_lane["authority_owner"] == "account-console-broker-observation-session", "P019 owner mismatch")
    require(p019_lane["direct_session_allowed"] is False, "P019 lane cannot allow direct session while ADR-0005 is proposed")
    require(p019_lane["may_satisfy_p018_owner_source_package_acceptance"] is False, "P019 blocked projection cannot satisfy P018 source package acceptance")
    for allowed_work in [
        "schemas",
        "fixtures",
        "typed_blockers",
        "negative_tests",
        "blocked_ui_states",
        "owner_map_pending_guard",
    ]:
        require(allowed_work in p019_lane["current_allowed_work"], f"P019 lane missing allowed work {allowed_work}")
    for root in [
        "contracts/broker_observation/",
        "docs/proposals/p019-broker-observation-session-foundation/",
        "docs/acceptance/2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json",
        "output/debug/p019-tws-local-window-confirmation/",
    ]:
        require(root in p019_lane["allowed_evidence_roots"], f"P019 lane missing root {root}")

    require(synthetic_lane["lane_kind"] == "synthetic_contract_guard", "synthetic lane kind mismatch")
    require(
        synthetic_lane["authority_owner"] == "account-console-broker-observation-session",
        "synthetic lane owner mismatch",
    )
    require(synthetic_lane["direct_session_allowed"] is False, "synthetic lane cannot allow direct session")
    require(synthetic_lane["may_satisfy_real_funds_positions_parity"] is False, "synthetic lane cannot close real parity")
    require(
        synthetic_lane["may_satisfy_p018_owner_source_package_acceptance"] is False,
        "synthetic lane cannot satisfy P018 owner source package",
    )
    require(
        synthetic_lane["may_satisfy_p019_direct_observation_acceptance"] is False,
        "synthetic lane cannot satisfy P019 direct observation acceptance",
    )
    require(synthetic_lane["synthetic_contract_only"] is True, "synthetic lane must be contract-only")
    for root in [
        "contracts/broker_observation/fixtures/ib_tws_u3028269_ready_*.synthetic.json",
        "scripts/validate_p019_ib_tws_ready_source_contract.py",
        "backend/tests/test_source_bridge.py::test_ib_tws_ready_source_package_projects_ready_without_command",
        "frontend/tests/e2e/p019-ib-tws-synthetic-ready-projection.spec.ts",
        "docs/acceptance/2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json",
        "scripts/validate_p019_u3028269_synthetic_ready_ui_contract.py",
    ]:
        require(root in synthetic_lane["allowed_evidence_roots"], f"synthetic lane missing root {root}")
    for forbidden_claim in [
        "synthetic ready fixture proves real U3028269 funds",
        "synthetic ready fixture proves real U3028269 positions",
        "synthetic ready fixture closes UI funds/positions parity",
        "synthetic ready fixture satisfies P018 owner source-package acceptance",
        "synthetic ready fixture accepts ADR-0005",
        "synthetic ready fixture authorizes direct broker session",
        "synthetic ready fixture authorizes order action",
    ]:
        require(forbidden_claim in synthetic_lane["forbidden_claims"], f"synthetic lane missing forbidden claim {forbidden_claim}")
    for required_step in [
        "local_tws_api_readiness_probe_pass",
        "readonly_tws_api_account_summary_success",
        "readonly_tws_api_positions_success",
        "source_package_built_from_real_query_artifacts",
        "account_mirror_projection_from_real_source_package",
        "ui_parity_against_same_slice_tws_api_source",
    ]:
        require(required_step in synthetic_lane["required_real_closeout_chain"], f"synthetic lane missing real closeout step {required_step}")

    rules = payload["cross_lane_rules"]
    require(rules["same_artifact_must_not_close_both_lanes_without_mapping"] is True, "cross-lane mapping rule missing")
    require(rules["p018_source_package_is_not_p019_direct_session_evidence"] is True, "P018/P019 separation missing")
    require(rules["p019_blocked_projection_is_not_p018_owner_source_package_evidence"] is True, "P019/P018 separation missing")
    require(
        rules["p019_synthetic_ready_contract_is_not_real_funds_positions_evidence"] is True,
        "synthetic real-parity separation missing",
    )
    require(
        rules["p019_synthetic_ready_contract_is_not_p018_owner_source_package_evidence"] is True,
        "synthetic P018 separation missing",
    )
    require(rules["screenshots_are_rendering_evidence_only"] is True, "screenshot boundary missing")
    require(rules["raw_secret_values_recorded"] is False, "cross-lane raw secret boundary missing")
    require(rules["required_blocker_when_mapping_missing"] == "p018_p019_lane_mapping_missing", "mapping blocker mismatch")

    forbidden_manifest_terms = [
        '"direct_session_allowed": true',
        '"raw_secret_values_recorded": true',
        "raw_tws_endpoint",
        "raw_client_id",
        "broker_password",
        "auth_code",
        "placeOrder",
        "cancelOrder",
    ]
    manifest_text = read(MANIFEST)
    for forbidden in forbidden_manifest_terms:
        require(forbidden not in manifest_text, f"manifest must not contain {forbidden}")

    require_terms(
        P018_README,
        [
            "Account Console direct connection to TWS / IB Gateway",
            "TWS / IB Gateway session ownership",
            "source package",
        ],
    )
    require_terms(
        P018_ACCEPTANCE,
        [
            "This proposal accepts only the read-only IB TWS observation path from owner-produced source package",
            "Account Console opens a TWS socket",
            "No same-slice owner connectivity evidence exists",
        ],
    )
    require_terms(
        P019_README,
        [
            "Related proposal: [P018 IB TWS Read-Only Account Console Landing]",
            "Replacing P018 same-slice IB source-package work",
            "P019 defines the broker-generic foundation",
        ],
    )
    require_terms(
        P019_AUDIT,
        [
            "PRE-G03 P018/P019 lane separation",
            "Evidence must not be reused across lanes without explicit mapping",
            "P018 compatibility mode",
        ],
    )
    require_terms(
        P019_PHASE_PLAN,
        [
            "evidence-lane-manifest.json",
            "validate_p019_evidence_lane_manifest.py",
            "P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true",
            "validate_p019_u3028269_synthetic_ready_ui_contract.py",
            "P019_U3028269_SYNTHETIC_READY_UI_CONTRACT_OK: verdict=synthetic_contract_only surfaces=9 reports=2 reload=passed",
        ],
    )
    require_terms(
        P019_ACCEPTANCE,
        [
            "P019 evidence lane manifest validator",
            "validate_p019_evidence_lane_manifest.py",
            "P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true",
        ],
    )

    print("P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true")


if __name__ == "__main__":
    main()
