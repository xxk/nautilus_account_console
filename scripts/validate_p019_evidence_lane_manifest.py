from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "evidence-lane-manifest.json"
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


def main() -> None:
    payload = load(MANIFEST)
    require(payload["schema"] == "account-console.p019-evidence-lane-manifest.v1", "manifest schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "manifest proposal mismatch")
    require(payload["adr_id"] == "ADR-0005", "manifest ADR mismatch")
    require(payload["status"] == "accepted_with_lane_separation", "manifest status mismatch")
    require(payload["blocker_id"] is None, "ADR blocker should be retired")
    require(payload["raw_secret_values_recorded"] is False, "manifest must not record raw secrets")

    p018_lane = lane_by_id(payload, "p018-owner-source-package")
    p019_lane = lane_by_id(payload, "p019-adr0005-governed-observation-session")
    synthetic_lane = lane_by_id(payload, "p019-synthetic-contract-ready-path")

    require(p018_lane["lane_kind"] == "owner_source_package", "P018 lane kind mismatch")
    require(p018_lane["direct_session_allowed"] is False, "P018 lane cannot allow direct session")
    require(p018_lane["may_satisfy_p019_direct_observation_acceptance"] is False, "P018 cannot satisfy P019 direct observation acceptance")
    require(p018_lane["may_be_used_by_p019_with_explicit_mapping"] is True, "P018 mapping rule missing")

    require(p019_lane["lane_kind"] == "governed_observation_session", "P019 lane kind mismatch")
    require(p019_lane["authority_owner"] == "account-console-broker-observation-session", "P019 owner mismatch")
    require(p019_lane["direct_session_allowed"] is False, "P019 lane direct-session flag must stay false in manifest")
    require(p019_lane["may_satisfy_p018_owner_source_package_acceptance"] is False, "P019 lane cannot satisfy P018 source package acceptance")
    for allowed_work in [
        "schemas",
        "fixtures",
        "typed_blockers",
        "negative_tests",
        "blocked_ui_states",
        "owner_map_accepted_guard",
        "real_funds_positions_parity",
        "residual_runtime_blockers",
    ]:
        require(allowed_work in p019_lane["current_allowed_work"], f"P019 lane missing allowed work {allowed_work}")
    for root in [
        "docs/acceptance/2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
        "docs/acceptance/2026-06-20-adr0005-broker-observation-session-acceptance.json",
        "output/account_capability/ib-live-u3028269/",
    ]:
        require(root in p019_lane["allowed_evidence_roots"], f"P019 lane missing accepted root {root}")
    for forbidden_claim in [
        "Account Console owns broker runtime truth",
        "Account Console owns account/order/fill truth",
        "Account Console stores raw broker secrets",
        "observation session connectivity proves live readiness",
        "observation session connectivity permits submit/cancel/replace/modify",
        "zero real executions proves complete order/fill history",
    ]:
        require(forbidden_claim in p019_lane["forbidden_claims"], f"P019 lane missing forbidden claim {forbidden_claim}")

    require(synthetic_lane["lane_kind"] == "synthetic_contract_guard", "synthetic lane kind mismatch")
    require(synthetic_lane["direct_session_allowed"] is False, "synthetic lane cannot allow direct session")
    require(synthetic_lane["may_satisfy_real_funds_positions_parity"] is False, "synthetic lane cannot close real parity")
    require(synthetic_lane["may_satisfy_p018_owner_source_package_acceptance"] is False, "synthetic lane cannot satisfy P018")
    require(synthetic_lane["may_satisfy_p019_direct_observation_acceptance"] is False, "synthetic lane cannot satisfy direct observation")
    require(synthetic_lane["synthetic_contract_only"] is True, "synthetic lane must stay contract-only")

    rules = payload["cross_lane_rules"]
    require(rules["same_artifact_must_not_close_both_lanes_without_mapping"] is True, "cross-lane mapping rule missing")
    require(rules["p018_source_package_is_not_p019_direct_session_evidence"] is True, "P018/P019 separation missing")
    require(rules["p019_blocked_projection_is_not_p018_owner_source_package_evidence"] is True, "P019/P018 separation missing")
    require(rules["p019_synthetic_ready_contract_is_not_real_funds_positions_evidence"] is True, "synthetic real-parity separation missing")
    require(rules["p019_synthetic_ready_contract_is_not_p018_owner_source_package_evidence"] is True, "synthetic P018 separation missing")
    require(rules["screenshots_are_rendering_evidence_only"] is True, "screenshot boundary missing")
    require(rules["raw_secret_values_recorded"] is False, "cross-lane raw secret boundary missing")

    manifest_text = read(MANIFEST)
    for forbidden in [
        '"raw_secret_values_recorded": true',
        "raw_tws_endpoint",
        "raw_client_id",
        "broker_password",
        "auth_code",
        "placeOrder",
        "cancelOrder",
    ]:
        require(forbidden not in manifest_text, f"manifest must not contain {forbidden}")

    for path in [P019_PHASE_PLAN, P019_ACCEPTANCE]:
        text = read(path)
        require("validate_p019_evidence_lane_manifest.py" in text, f"{path} missing lane validator")
        require("P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true status=accepted" in text, f"{path} missing accepted lane pass signal")

    print("P019_EVIDENCE_LANE_MANIFEST_OK: lanes=3 p018_p019_synthetic_separated=true status=accepted")


if __name__ == "__main__":
    main()
