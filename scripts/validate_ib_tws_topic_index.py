from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPICS_README = ROOT / "docs" / "topics" / "README.md"
REGISTRY = ROOT / "docs" / "topics" / "主题状态注册表_Topic State Registry.yaml"
IB_TWS_README = ROOT / "docs" / "topics" / "ib-tws" / "README.md"
KNOWLEDGE_CARD = ROOT / "docs" / "topics" / "ib-tws" / "u3028269-tws-login-and-api-knowledge.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class IbTwsTopicIndexError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IbTwsTopicIndexError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_terms(text: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in text]
    require(not missing, f"{label}: missing terms {missing}")


def main() -> None:
    topics_readme = read(TOPICS_README)
    registry = read(REGISTRY)
    ib_tws_readme = read(IB_TWS_README)
    card = read(KNOWLEDGE_CARD)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require_terms(
        topics_readme,
        [
            "[IB TWS](./ib-tws/README.md)",
            "Non-secret IB TWS operational knowledge",
            "U3028269 login/API enablement",
        ],
        "topics README",
    )
    require_terms(
        registry,
        [
            "ib-tws:",
            "canonical_status: active",
            "path: docs/topics/ib-tws/README.md",
            "docs/topics/ib-tws/u3028269-tws-login-and-api-knowledge.md",
        ],
        "topic registry",
    )
    require_terms(
        ib_tws_readme,
        [
            "Topic ID: `ib-tws`",
            "U3028269 TWS login and API knowledge",
            "./u3028269-tws-login-and-api-knowledge.md",
            "Do not record passwords",
            "Do not record funds/positions values",
            "Do not authorize order actions",
            "Real acceptance remains with the active proposal/acceptance artifacts",
        ],
        "IB TWS topic README",
    )
    require("ib-tws-u3028269-login-api" in card, "knowledge card missing expected ID")
    for forbidden in [
        "raw_secret_values_recorded=true",
        "raw_broker_endpoint_recorded=true",
        "funds_positions_values_recorded_in_knowledge=true",
        "screenshot_used_for_funds_positions=true",
        "order_action_sent=true",
        "can_trade=true",
        "broker_tradable=true",
    ]:
        require(forbidden not in ib_tws_readme, f"IB TWS topic must not claim {forbidden}")
        require(forbidden not in topics_readme, f"topics README must not claim {forbidden}")

    for term in [
        "validate_ib_tws_topic_index.py",
        "IB_TWS_TOPIC_INDEX_OK",
        "docs/topics/ib-tws/README.md",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print("IB_TWS_TOPIC_INDEX_OK: cards=1 status=active")


if __name__ == "__main__":
    main()
