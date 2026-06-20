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
    "reqExecutions(",
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
        for fragment in FORBIDDEN_ROUTE_FRAGMENTS:
            require(fragment not in path, f"forbidden direct broker/command route {path}")
        if path.startswith("/api/"):
            lowered = path.lower()
            for action in FORBIDDEN_ROUTE_ACTION_WORDS:
                require(action not in lowered, f"forbidden action word {action!r} in route {path}")
            require(
                path.startswith("/api/mirror/")
                or path in ALLOWED_LEGACY_READ_ROUTES
                or path == "/api/accounts",
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
        require(projection["blockers"] == [], "ready U3028269 must not carry blockers")
        require(projection["balances"], "ready U3028269 should project TWS API balances")
        require(projection["positions"], "ready U3028269 should project TWS API positions")
    else:
        require(
            projection["source_health"]["blocker_id"] in {"adr0005_not_accepted", "tws_api_readiness_missing"},
            "U3028269 blocker drifted",
        )
        require(projection["source_health"]["api_transport"] == "ib_tws_api", "TWS API blocker must name API transport")
        require(projection["source_health"]["screenshot_used_for_values"] is False, "screenshots must not back funds/positions")
        require(projection["balances"] == [] and projection["positions"] == [], "blocked U3028269 must not invent balance/position rows")
    require(projection["capabilities"]["command"] == {"enabled": False, "mode": "disabled"}, "command capability drifted")
    require(projection["orders"] == [] and projection["fills"] == [], "U3028269 must not invent order/fill rows")
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
            "P019_API_BOUNDARY_OK: mirror_only=true command_routes=absent direct_broker_routes=absent",
        ],
    )
    require_terms(
        ACCEPTANCE,
        [
            "P019 API boundary validator",
            "validate_p019_api_boundary.py",
            "P019_API_BOUNDARY_OK: mirror_only=true command_routes=absent direct_broker_routes=absent",
        ],
    )

    print("P019_API_BOUNDARY_OK: mirror_only=true command_routes=absent direct_broker_routes=absent")


if __name__ == "__main__":
    main()
