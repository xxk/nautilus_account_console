from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

PROPOSAL = ROOT / "docs" / "proposals" / "p022-openctp-19053-account-console-readback"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ctp-paper-19053" / "source-package.json"
EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-real-login-ui-acceptance-evidence.json"


class P022ValidationError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P022ValidationError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk(item))
    return values


def validate_docs() -> None:
    required = {
        "README.md": [
            "Proposal ID: `p022-openctp-19053-account-console-readback`",
            "ADR-0005",
            "Owner Boundary:",
            "forbidden",
            "second_implementation_rejected",
        ],
        "acceptance.md": [
            "P022_OPENCTP_19053_READBACK_OK",
            "UI Anti-Drift Acceptance",
            "forbidden_actions",
            "forbidden_claims",
            "Implementation/browser evidence",
        ],
        "ui-design.md": ["Data Test ID", "tws-open-orders-table", "tws-fills-table"],
        "ui-acceptance.md": ["Negative UI Acceptance", "Browser Acceptance", "Blocker"],
        "phase-plan.md": ["Proposal ID", "Status", "Phase"],
    }
    for filename, terms in required.items():
        text = (PROPOSAL / filename).read_text(encoding="utf-8")
        for term in terms:
            require(term in text, f"{filename} missing {term}")


def validate_source_package(payload: dict[str, Any]) -> None:
    require(payload["schema_version"] == "account_source_artifact.v1", "source package schema mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["display_alias"] == "19053", "alias mismatch")
    require(payload["source_owner"] == "nautilus_ctp_adapter", "source owner mismatch")
    require(payload["source_kind"] == "ctp_trader_api", "source kind mismatch")
    require(payload["source_mode"] == "paper_observation", "source mode mismatch")
    require(payload["source_ref"] == "output/account_capability/ctp-paper-19053/source-package.json", "source ref mismatch")
    require(str(payload["source_checksum"]).startswith("sha256:"), "source checksum missing")
    require(payload["source_inputs"]["account_query"].startswith("owner://nautilus_ctp_adapter/"), "account owner ref missing")
    require(
        payload["source_inputs"]["paper_readonly_snapshot"].startswith("owner://nautilus_ctp_adapter/"),
        "snapshot owner ref missing",
    )
    require(
        payload["source_inputs"]["td_order_truth"].startswith("output/account_capability/ctp-paper-19053/current-openctp-login/"),
        "current TD order truth ref missing",
    )
    require(
        payload["source_inputs"]["order_trade_query"].startswith("output/account_capability/ctp-paper-19053/current-openctp-login/"),
        "current order/trade query ref missing",
    )
    require(payload["balances"], "funds balance row missing")
    balance = payload["balances"][0]
    require(balance["currency"] == "CNY", "balance currency mismatch")
    for field in ["equity", "available_cash", "margin_used"]:
        require(isinstance(balance.get(field), (int, float)), f"balance {field} missing")
    require(len(payload["positions"]) > 0, "positions missing")
    for position in payload["positions"]:
        require(position["instrument"], "position instrument missing")
        require(position["direction"] in {"long", "short"}, "position direction mismatch")
        require(isinstance(position["net_qty"], int), "position net_qty missing")
    health = payload["source_health"]
    require(health["state"] == "ready", "source health must be ready")
    require(health["api_transport"] == "ctp_trader_api", "api transport mismatch")
    require(health["open_orders_state"] in {"empty", "available"}, "open orders state mismatch")
    require(health["open_order_rows"] == len(payload["orders"]), "open order row count mismatch")
    require(health["fills_state"] in {"empty", "available"}, "fills state mismatch")
    require(health["fill_rows"] == len(payload["fills"]), "fill row count mismatch")
    require(health["order_trade_query_success"] is True, "order/trade query proof missing")
    require(health["order_trade_query_login_success"] is True, "order/trade query login missing")
    require(health["order_trade_query_ready"] is True, "order/trade query ready missing")
    require(health["order_trade_query_open_order_rows"] == len(payload["orders"]), "order/trade open order count mismatch")
    require(health["order_trade_query_trade_rows"] == len(payload["fills"]), "order/trade fill count mismatch")
    require("ReqQryOrder" in health["readonly_api_calls"], "order query API call missing")
    require("ReqQryTrade" in health["readonly_api_calls"], "trade query API call missing")
    require(health["complete_trade_history_claimed"] is False, "complete trade history claimed")
    require(health["td_order_truth_login_success"] is True, "current TD order truth login missing")
    require(health["td_order_truth_ready"] is True, "current TD order truth ready missing")
    require(health["td_order_truth_observed_order_event_count"] == 0, "callback order truth must not be used as query rows")
    require(health["td_order_truth_observed_trade_event_count"] == 0, "callback trade truth must not be used as query rows")
    require(health["order_action_sent"] is False, "order action sent")
    require(health["cancel_order_sent"] is False, "cancel order sent")
    require(health["replace_order_sent"] is False, "replace order sent")
    require(health["raw_secret_values_recorded"] is False, "raw secrets recorded")
    require(health["raw_broker_endpoint_recorded"] is False, "raw endpoint recorded")
    require(payload["boundaries"]["order_action_sent"] is False, "boundary order action drifted")
    forbidden_fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "OrderInsert", "OrderAction"]
    for value in walk(payload):
        if isinstance(value, str):
            lowered = value.lower()
            for fragment in forbidden_fragments:
                require(fragment.lower() not in lowered, f"forbidden fragment {fragment} in source package")


def validate_mirror() -> None:
    from fastapi.testclient import TestClient
    from nautilus_account_console.main import app

    client = TestClient(app)
    response = client.get("/api/mirror/accounts/acct.ctp.paper.19053")
    require(response.status_code == 200, "mirror route missing")
    payload = response.json()
    require(payload["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}, "command capability drifted")
    require(payload["boundaries"]["order_action"] is False, "mirror order action drifted")
    require(payload["source_health"]["api_transport"] == "ctp_trader_api", "mirror transport mismatch")
    require(payload["source_health"]["td_order_truth_login_success"] is True, "mirror current login proof missing")
    require(payload["source_health"]["order_trade_query_success"] is True, "mirror order/trade query proof missing")
    require(payload["source_health"]["open_order_rows"] == len(payload["orders"]), "mirror open order count mismatch")
    require(payload["source_health"]["fill_rows"] == len(payload["fills"]), "mirror fill count mismatch")
    require(payload["balances"], "mirror balances missing")
    require(payload["positions"], "mirror positions missing")


def validate_evidence_if_present() -> None:
    if not EVIDENCE.exists():
        return
    payload = load(EVIDENCE)
    if payload.get("account_id") != "acct.ctp.paper.19053":
        return
    require(payload["verdict"] in {"passed", "blocked"}, "evidence verdict mismatch")
    if payload["verdict"] == "passed":
        require(payload.get("rendered_open_order_count") == payload.get("order_count"), "rendered order count mismatch")
        require(payload.get("funds_parity") == "pass", "funds parity missing")
        require(payload.get("positions_parity") == "pass", "positions parity missing")
        require(payload.get("open_orders_parity") == "pass", "open orders parity missing")
        require(payload.get("fills_parity") == "pass", "fills parity missing")
        require(payload.get("rendered_fill_count") == payload.get("fill_count"), "rendered fill count mismatch")
        require(payload.get("td_order_truth_login_success") is True, "evidence current login proof missing")
        require(
            payload.get("td_order_truth_observed_order_event_count") == 0,
            "evidence callback order truth must stay separate from query rows",
        )
        require(
            payload.get("td_order_truth_observed_trade_event_count") == 0,
            "evidence callback trade truth must stay separate from query rows",
        )


def main() -> None:
    validate_docs()
    source_package = load(SOURCE_PACKAGE)
    validate_source_package(source_package)
    validate_mirror()
    validate_evidence_if_present()
    print(
        "P022_OPENCTP_19053_READBACK_OK: "
        f"balances={len(source_package['balances'])} positions={len(source_package['positions'])} "
        f"open_orders={len(source_package['orders'])} fills={len(source_package['fills'])} command=false"
    )


if __name__ == "__main__":
    main()
