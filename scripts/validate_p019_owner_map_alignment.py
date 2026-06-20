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

    require("decision_status: accepted" in adr, "ADR-0005 must be accepted for this alignment gate")
    require("landing_status: foundation_accepted" in adr, "ADR-0005 landing mismatch")
    require("- Status: accepted_with_residual_runtime_blockers" in proposal, "P019 proposal must be accepted")

    require_terms(
        OWNER_MAP,
        [
            "ADR-0005 independent broker observation sessions",
            "Broker observation session capability",
            "`account-console-broker-observation-session` accepted by ADR-0005",
            "P019 Broker Observation Session Foundation Accepted Assignment",
            "accepted guarded capability owner for read-only observation contracts",
            "not a broker runtime owner, account/order truth owner, command owner, approval owner, capital owner or trading-readiness owner",
            "contracts/broker_observation/**",
            "output/account_capability/ib-live-u3028269/durable-store-reload.json",
            "acct.ib.live.u3028269",
            "`raw_secret_values_recorded=false`",
            "no broker truth",
            "no order action",
            "typed residual blockers for zero execution rows",
            "real_order_fill_callbacks_not_available",
            "does not authorize Account Console to own broker live state",
            "own account/order/fill truth",
            "store raw secrets",
            "infer trading readiness",
            "expose submit/cancel/replace/modify controls",
        ],
    )

    forbidden_owner_claims = [
        "Account Console owns broker live state",
        "Account Console owns account/order/fill truth",
        "direct_session_allowed=true",
        "raw_secret_values_recorded=true",
        "broker_truth=true",
        "order_action=true",
        "live_ready=true",
        "can_trade=true",
        "complete_history_claimed=true",
    ]
    for forbidden in forbidden_owner_claims:
        require(forbidden not in owner_map, f"owner map must not claim {forbidden}")

    require_terms(
        PHASE_PLAN,
        [
            "validate_p019_owner_map_alignment.py",
            "accepted read-only `account-console-broker-observation-session`",
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "P019 owner-map alignment validator",
            "validate_p019_owner_map_alignment.py",
            "P019_OWNER_MAP_ALIGNMENT_OK: owner=accepted_guarded adr0005=accepted",
        ],
    )

    print("P019_OWNER_MAP_ALIGNMENT_OK: owner=accepted_guarded adr0005=accepted")


if __name__ == "__main__":
    main()
