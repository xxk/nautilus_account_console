from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_DIR = ROOT / "docs" / "topics" / "ib-tws"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class IbTwsKnowledgeRedactionError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IbTwsKnowledgeRedactionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    docs = sorted(TOPIC_DIR.glob("*.md"))
    require(docs, "IB TWS topic docs missing")

    forbidden_fragments = [
        "raw_tws_password=true",
        "raw_2fa_or_auth_code=true",
        "raw_broker_secret=true",
        "raw_broker_endpoint=true",
        "raw_tws_xml_contents=true",
        "raw_account_secret=true",
        "raw_secret_values_recorded=true",
        "raw_broker_endpoint_recorded=true",
        "raw_config_file_contents_recorded=true",
        "funds_positions_values_recorded_in_knowledge=true",
        "screenshot_used_for_funds_positions=true",
        "placeOrder=true",
        "cancelOrder=true",
        "order_action_sent=true",
        "can_trade=true",
        "broker_tradable=true",
        "<TWS",
        "<tws",
        "password: ",
        "auth_code: ",
        "api_key: ",
        "secret: ",
        "\"password\"",
        "\"auth_code\"",
        "\"api_key\"",
    ]
    required_boundaries = [
        "Do not record passwords",
        "Do not record funds/positions values",
        "raw_secret_values_recorded=false",
        "raw_broker_endpoint_recorded=false",
        "raw_config_file_contents_recorded=false",
        "screenshot_used_for_funds_positions=false",
        "order_action_sent=false",
    ]

    combined = "\n".join(read(path) for path in docs)
    lowered = combined.lower()
    for fragment in forbidden_fragments:
        require(fragment.lower() not in lowered, f"IB TWS knowledge contains forbidden fragment {fragment}")
    for boundary in required_boundaries:
        require(boundary in combined, f"IB TWS knowledge missing boundary {boundary}")

    require("U3028269" in combined, "IB TWS knowledge missing U3028269")
    require("handshake_ok" in combined, "IB TWS knowledge missing handshake_ok")
    require("reqAccountSummary" in combined, "IB TWS knowledge missing reqAccountSummary")
    require("reqPositions" in combined, "IB TWS knowledge missing reqPositions")

    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)
    for term in [
        "validate_ib_tws_knowledge_redaction.py",
        "IB_TWS_KNOWLEDGE_REDACTION_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print(f"IB_TWS_KNOWLEDGE_REDACTION_OK: docs={len(docs)}")


if __name__ == "__main__":
    main()
