from __future__ import annotations

import sys
from pathlib import Path

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.main import app  # noqa: E402


PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
SOURCE_ROOTS = [
    ROOT / "backend" / "src" / "nautilus_account_console",
    ROOT / "frontend" / "src",
]

FORBIDDEN_ROUTE_FRAGMENTS = [
    "/api/broker",
    "/api/brokers",
    "/api/tws",
    "/api/ib",
    "/api/ib-tws",
    "/api/broker-observation",
    "/api/orders/submit",
    "/api/orders/cancel",
    "/api/orders/replace",
    "/api/orders/modify",
]
FORBIDDEN_ROUTE_ACTION_WORDS = [
    "submit",
    "cancel",
    "replace",
    "modify",
    "place-order",
    "place_order",
]
FORBIDDEN_SOURCE_TERMS = [
    "import ibapi",
    "from ibapi",
    "EClient(",
    "EWrapper",
    "placeOrder(",
    "cancelOrder(",
    "reqAccountUpdates(",
    "reqPositions(",
    "/api/broker",
    "/api/tws",
    "/api/ib-tws",
    "/api/orders/submit",
    "/api/orders/cancel",
    "/api/orders/replace",
    "/api/orders/modify",
]
ALLOWED_LEGACY_READ_ROUTES = {
    "/api/accounts",
    "/api/accounts/{account_id}",
    "/api/accounts/{account_id}/events",
    "/api/accounts/{account_id}/events/stream",
    "/api/accounts/{account_id}/orders/{client_order_id}/execution-reports",
}
REQUIRED_MIRROR_ROUTES = {
    "/api/mirror/accounts",
    "/api/mirror/accounts/{account_id}",
    "/api/mirror/accounts/{account_id}/positions",
    "/api/mirror/accounts/{account_id}/orders",
    "/api/mirror/accounts/{account_id}/capabilities",
    "/api/mirror/accounts/{account_id}/source-health",
    "/api/mirror/accounts/{account_id}/evidence",
}
ALLOWED_GOVERNED_COMMAND_ROUTES = {
    "/api/commands/accounts/{account_id}/submit-intents": {"POST"},
    "/api/commands/accounts/{account_id}/cancel-intents": {"POST"},
    "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}": {"GET"},
}
PASS_SIGNAL = "P019_API_BOUNDARY_OK: mirror_only=true governed_command_routes=p024_only direct_broker_routes=absent"


class ApiBoundaryError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ApiBoundaryError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for root in SOURCE_ROOTS:
        for path in root.rglob("*"):
            if path.suffix in {".py", ".ts", ".tsx"}:
                files.append(path)
    return files


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    routes = [route for route in app.routes if isinstance(route, APIRoute)]
    route_paths = {route.path for route in routes}

    require(REQUIRED_MIRROR_ROUTES.issubset(route_paths), "required Account Mirror routes missing")
    for route in routes:
        path = route.path
        methods = route.methods or set()
        if path.startswith("/api/mirror/"):
            require(methods == {"GET"}, f"{path}: mirror route must be GET-only, got {sorted(methods)}")
        if path in ALLOWED_LEGACY_READ_ROUTES:
            require(methods == {"GET"}, f"{path}: legacy read route must be GET-only, got {sorted(methods)}")
        if path in ALLOWED_GOVERNED_COMMAND_ROUTES:
            require(
                methods == ALLOWED_GOVERNED_COMMAND_ROUTES[path],
                f"{path}: governed P024 command route has invalid methods {sorted(methods)}",
            )
        elif path.startswith("/api/commands"):
            require(False, f"{path}: command route is outside the P024 governed allowlist")
        for fragment in FORBIDDEN_ROUTE_FRAGMENTS:
            require(fragment not in path, f"forbidden direct broker/command route {path}")
        if path.startswith("/api/"):
            lowered = path.lower()
            if path not in ALLOWED_GOVERNED_COMMAND_ROUTES:
                for action in FORBIDDEN_ROUTE_ACTION_WORDS:
                    require(action not in lowered, f"forbidden action word {action!r} in route {path}")
            require(
                path.startswith("/api/mirror/")
                or path in ALLOWED_LEGACY_READ_ROUTES
                or path == "/api/accounts"
                or path in ALLOWED_GOVERNED_COMMAND_ROUTES,
                f"{path}: API route is outside accepted read-only families",
            )

    client = TestClient(app)
    projection_response = client.get("/api/mirror/accounts/acct.ib.live.u3028269")
    require(projection_response.status_code == 200, "U3028269 mirror projection missing")
    projection = projection_response.json()
    require(projection["source_kind"] == "ib_tws_observation", "U3028269 source kind drifted")
    require(projection["source_health"]["raw_secret_values_recorded"] is False, "raw secrets must stay false")
    require(projection["source_health"]["api_transport"] == "ib_tws_api", "TWS API transport drifted")
    require(projection["source_health"]["screenshot_used_for_values"] is False, "screenshots must not back funds/positions")
    if projection["capabilities"]["observation"]["mirror_state"] == "ready":
        require(projection["source_health"]["state"] == "ready", "ready U3028269 source health drifted")
        require(projection["source_health"].get("blocker_id") is None, "ready U3028269 must not carry blocker")
        readonly = projection["source_health"]["executions_readonly_query"]
        require(readonly["api_call"] == "reqExecutions", "mirror lost executions readonly API")
        require(readonly["filter_type"] == "ExecutionFilter", "mirror lost executions filter type")
        require(readonly["filter_account_raw_value_recorded"] is False, "mirror recorded raw executions filter")
        require(readonly["complete_history_claimed"] is False, "mirror must not claim complete execution history")
        require(readonly["order_action_sent"] is False, "mirror executions metadata must not send order action")
        require(projection["blockers"] == [], "ready U3028269 must not carry blockers")
        require(projection["balances"], "ready U3028269 should project TWS API balances")
        require(projection["positions"], "ready U3028269 should project TWS API positions")
        open_orders = projection["source_health"]["open_orders_readonly_query"]
        require(open_orders["api_call"] == "reqAllOpenOrders", "mirror lost open orders readonly API")
        require(open_orders["order_action_sent"] is False, "mirror open orders metadata must not send order action")
        require(open_orders["cancel_order_sent"] is False, "mirror open orders metadata must not send cancel")
        require(open_orders["replace_order_sent"] is False, "mirror open orders metadata must not send replace")
        require(projection["source_health"]["open_order_rows"] == len(projection["orders"]), "open order count drifted")
        for order in projection["orders"]:
            require(order.get("nautilus_report_type") == "OrderStatusReport", "open order must be normalized OrderStatusReport")
            require(
                str(order.get("source_ref", "")).startswith("output/account_capability/ib-live-u3028269/tws-api/open_orders.json#"),
                "open order source ref must point to open_orders artifact",
            )
            require(str(order.get("checksum", "")).startswith("sha256:"), "open order checksum missing")
    else:
        require(
            projection["source_health"]["blocker_id"] in {"adr0005_not_accepted", "tws_api_readiness_missing"},
            "U3028269 blocker drifted",
        )
        require(projection["source_health"]["api_transport"] == "ib_tws_api", "TWS API blocker must name API transport")
        require(projection["source_health"]["screenshot_used_for_values"] is False, "screenshots must not back funds/positions")
        require(projection["balances"] == [] and projection["positions"] == [], "blocked U3028269 must not invent balance/position rows")
        require(projection["orders"] == [], "blocked U3028269 must not invent order rows")
    require(projection["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}, "command capability drifted")
    if projection["fills"]:
        require(
            projection["source_health"].get("executions_query_success") is True,
            "U3028269 fills require successful read-only executions query",
        )
        for fill in projection["fills"]:
            require(fill.get("nautilus_report_type") == "FillReport", "U3028269 fills must be normalized FillReport rows")
    else:
        require(
            projection["source_health"].get("execution_report_state") in {None, "not_available_or_empty"},
            "empty fills must carry typed execution report state",
        )
    require(projection["boundaries"]["broker_truth"] is False, "U3028269 must not claim broker truth")
    require(projection["boundaries"]["order_action"] is False, "U3028269 must not allow order action")

    health = client.get("/api/mirror/accounts/acct.ib.live.u3028269/source-health")
    evidence = client.get("/api/mirror/accounts/acct.ib.live.u3028269/evidence")
    require(health.status_code == 200, "U3028269 source-health route missing")
    require(evidence.status_code == 200, "U3028269 evidence route missing")
    evidence_payload = evidence.json()
    require(evidence_payload["boundaries"]["broker_truth"] is False, "evidence must not claim broker truth")
    require(evidence_payload["boundaries"]["order_action"] is False, "evidence must not allow order action")
    expected_evidence = {"source_package", "mirror_projection"}
    if projection["capabilities"]["observation"]["mirror_state"] != "ready":
        expected_evidence.add("typed_blocker")
    require(
        {item["kind"] for item in evidence_payload["evidence"]} >= expected_evidence,
        "U3028269 evidence must include required source, mirror and blocker records",
    )

    for path in iter_source_files():
        text = read(path)
        rel = path.relative_to(ROOT)
        for term in FORBIDDEN_SOURCE_TERMS:
            require(term not in text, f"{rel}: forbidden direct broker/command term {term!r}")

    require_terms(
        PHASE_PLAN,
        [
            "validate_p019_api_boundary.py",
            PASS_SIGNAL,
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "P019 API boundary validator",
            "validate_p019_api_boundary.py",
            PASS_SIGNAL,
        ],
    )

    print(PASS_SIGNAL)


if __name__ == "__main__":
    main()
