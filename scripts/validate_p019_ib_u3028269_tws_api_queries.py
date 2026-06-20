from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUERY_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
ACCOUNT_SUMMARY = QUERY_DIR / "account_summary.json"
POSITIONS = QUERY_DIR / "positions.json"
COLLECTOR = ROOT / "scripts" / "collect_ib_u3028269_tws_api_snapshot.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class TwsApiQueryError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TwsApiQueryError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk_values(item))
    return values


def validate_common(payload: dict[str, Any], kind: str) -> None:
    require(payload["schema"] == "account-console.ib-tws-api-query.v1", f"{kind}: schema drifted")
    require(payload["account_id"] == "acct.ib.live.u3028269", f"{kind}: account mismatch")
    require(payload["display_alias"] == "U3028269", f"{kind}: alias mismatch")
    require(payload["query_kind"] == kind, f"{kind}: query kind mismatch")
    require(payload["source_kind"] == "ib_tws_api", f"{kind}: source kind mismatch")
    require(payload["raw_secret_values_recorded"] is False, f"{kind}: raw secrets recorded")
    require(payload["raw_broker_endpoint_recorded"] is False, f"{kind}: raw endpoint recorded")
    require(payload["screenshot_used_for_values"] is False, f"{kind}: screenshot used for values")
    require(payload["order_action_sent"] is False, f"{kind}: order action sent")
    require(str(payload["query_checksum"]).startswith("sha256:"), f"{kind}: checksum missing")


def main() -> None:
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    collector = read(COLLECTOR)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    validate_common(account_summary, "account_summary")
    validate_common(positions, "positions")

    if account_summary["success"] is False or positions["success"] is False:
        require(account_summary["success"] is False and positions["success"] is False, "blocked query pair must both be blocked")
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "account summary blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "positions blocker mismatch")
        require(account_summary["tws_api_login_confirmed"] is False, "blocked account query must not claim login")
        require(positions["tws_api_login_confirmed"] is False, "blocked positions query must not claim login")
        require(account_summary["balances"] == [], "blocked account query must not invent balances")
        require(positions["positions"] == [], "blocked positions query must not invent positions")
    else:
        require(account_summary["success"] is True and positions["success"] is True, "ready query pair must both pass")
        require(account_summary["tws_api_login_confirmed"] is True, "account query must confirm TWS API login")
        require(positions["tws_api_login_confirmed"] is True, "positions query must confirm TWS API login")
        require(isinstance(account_summary["balances"], list), "ready account query balances must be list")
        require(isinstance(positions["positions"], list), "ready positions query positions must be list")

    forbidden_fragments = ["password=", "passwd=", "auth_code=", "api_key=", "secret=", "127.0.0.1:"]
    for label, payload in [("account_summary", account_summary), ("positions", positions)]:
        for value in walk_values(payload):
            if isinstance(value, str):
                lowered = value.lower()
                hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
                require(not hits, f"{label}: forbidden fragment {hits} in {value!r}")

    for term in [
        "reqAccountSummary",
        "reqPositions",
        "cancelAccountSummary",
        "cancelPositions",
        "order_action_sent",
        "raw_broker_endpoint_recorded",
    ]:
        require(term in collector, f"collector missing guard/readonly term {term}")
    for forbidden in ["placeOrder", "cancelOrder", "reqOpenOrders", "reqAllOpenOrders"]:
        require(forbidden not in collector, f"collector must not contain order/action API {forbidden}")

    for term in [
        "collect_ib_u3028269_tws_api_snapshot.py",
        "validate_p019_ib_u3028269_tws_api_queries.py",
        "P019_IB_U3028269_TWS_API_QUERIES_OK",
    ]:
        require(term in acceptance, f"acceptance missing query term {term}")
        require(term in phase_plan, f"phase plan missing query term {term}")

    status = "ready" if account_summary["success"] and positions["success"] else "blocked"
    print(f"P019_IB_U3028269_TWS_API_QUERIES_OK: status={status} order_action_sent=false screenshot_values=false")


if __name__ == "__main__":
    main()
