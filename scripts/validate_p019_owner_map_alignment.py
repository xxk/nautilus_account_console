from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
ADR = ROOT / "docs" / "adr" / "0005-account-console-independent-broker-observation-sessions.md"
PROPOSAL = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "README.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"


class OwnerMapAlignmentError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise OwnerMapAlignmentError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    owner_map = read(OWNER_MAP)
    adr = read(ADR)
    proposal = read(PROPOSAL)

    require("decision_status: proposed" in adr, "ADR-0005 must remain proposed for this alignment gate")
    require("landing_status: not_started" in adr, "ADR-0005 landing must remain not_started")
    require("- Status: proposed" in proposal, "P019 proposal must remain proposed")

    require_terms(
        OWNER_MAP,
        [
            "ADR-0005 independent broker observation sessions",
            "Pending broker observation session capability",
            "`account-console-broker-observation-session` pending ADR-0005 acceptance",
            "P019 Broker Observation Session Foundation Pending Assignment",
            "P019 and ADR-0005 are currently `proposed`",
            "pending capability owner, not an accepted runtime or broker owner",
            "contracts/broker_observation/**",
            "docs/proposals/p019-broker-observation-session-foundation/",
            "scripts/validate_adr0005_broker_observation_contracts.py",
            "acct.ib.live.u3028269",
            "`adr0005_not_accepted`",
            "`direct_session_allowed=false`",
            "`raw_secret_values_recorded=false`",
            "no rows, no command and no broker truth",
            "does not authorize Account Console to open a direct TWS/CTP/stock/CQG/TT session",
            "own broker live state",
            "own account/order/fill truth",
            "store raw secrets",
            "infer trading readiness",
            "expose submit/cancel/replace/modify controls",
            "typed blocker such as `adr0005_not_accepted`",
        ],
    )

    forbidden_owner_claims = [
        "`account-console-broker-observation-session` accepted",
        "accepted broker observation session capability",
        "Account Console owns broker live state",
        "Account Console owns account/order/fill truth",
        "direct_session_allowed=true",
        "raw_secret_values_recorded=true",
        "broker_truth=true",
        "order_action=true",
        "live_ready=true",
        "can_trade=true",
    ]
    for forbidden in forbidden_owner_claims:
        require(forbidden not in owner_map, f"owner map must not claim {forbidden}")

    require_terms(
        PHASE_PLAN,
        [
            "validate_p019_owner_map_alignment.py",
            "pending owner-map guard",
            "P019_OWNER_MAP_ALIGNMENT_OK: pending_owner=guarded adr0005=proposed",
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "P019 owner-map alignment validator",
            "validate_p019_owner_map_alignment.py",
            "P019_OWNER_MAP_ALIGNMENT_OK: pending_owner=guarded adr0005=proposed",
            "pending owner-map assignment",
        ],
    )

    print("P019_OWNER_MAP_ALIGNMENT_OK: pending_owner=guarded adr0005=proposed")


if __name__ == "__main__":
    main()
