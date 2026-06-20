from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
FIXTURE_DIR = ROOT / "contracts" / "broker_observation" / "fixtures"
ACCOUNT_SUMMARY = FIXTURE_DIR / "ib_tws_u3028269_ready_query_account_summary.synthetic.json"
POSITIONS = FIXTURE_DIR / "ib_tws_u3028269_ready_query_positions.synthetic.json"
READINESS = FIXTURE_DIR / "ib_tws_u3028269_ready_readiness.synthetic.json"
BUILDER_PATH = ROOT / "scripts" / "build_ib_u3028269_source_package_from_tws_api.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class ReadySourceContractError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReadySourceContractError(message)


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


def import_builder():
    spec = importlib.util.spec_from_file_location("p019_ib_source_builder", BUILDER_PATH)
    require(spec is not None and spec.loader is not None, "builder module spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.source_bridge import source_artifact_to_capability_bundle

    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    readiness = load(READINESS)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)
    builder = import_builder()

    require(account_summary["success"] is True, "synthetic account summary must be ready")
    require(positions["success"] is True, "synthetic positions must be ready")
    require(readiness["ready_for_tws_api_funds_positions_query"] is True, "synthetic readiness must be ready")
    for payload in [account_summary, positions, readiness]:
        for value in walk_values(payload):
            if isinstance(value, str):
                lowered = value.lower()
                require("127.0.0.1:" not in lowered, "synthetic fixture must not contain raw endpoint")
                require("password=" not in lowered and "secret=" not in lowered, "synthetic fixture must not contain secrets")

    with tempfile.TemporaryDirectory(prefix="p019-ready-source-contract-") as tmp:
        tmp_dir = Path(tmp)
        output = tmp_dir / "source-package.json"
        executions = tmp_dir / "executions.json"
        executions.write_text(
            json.dumps(
                {
                    "schema": "account-console.ib-tws-api-query.v1",
                    "account_id": "acct.ib.live.u3028269",
                    "display_alias": "U3028269",
                    "query_kind": "executions",
                    "source_kind": "ib_tws_api",
                    "success": True,
                    "tws_api_login_confirmed": True,
                    "query_started_at": "2026-06-20T00:00:00Z",
                    "query_completed_at": "2026-06-20T00:00:00Z",
                    "raw_secret_values_recorded": False,
                    "raw_broker_endpoint_recorded": False,
                    "screenshot_used_for_values": False,
                    "order_action_sent": False,
                    "account_ref": "ib-account-ref://U3028269",
                    "executions": [],
                    "commissions": [],
                    "execution_report_rows": 0,
                    "readonly_query": {
                        "api_call": "reqExecutions",
                        "filter_type": "ExecutionFilter",
                        "filter_account_ref": "ib-account-ref://U3028269",
                        "filter_account_raw_value_recorded": False,
                        "query_scope": "synthetic_current_tws_session_matching_account_filter",
                        "request_id": "exec-readonly-synthetic",
                        "order_action_sent": False,
                        "complete_history_claimed": False,
                    },
                    "query_checksum": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        open_orders = tmp_dir / "open_orders.json"
        open_orders.write_text(
            json.dumps(
                {
                    "schema": "account-console.ib-tws-api-query.v1",
                    "account_id": "acct.ib.live.u3028269",
                    "display_alias": "U3028269",
                    "query_kind": "open_orders",
                    "source_kind": "ib_tws_api",
                    "success": True,
                    "tws_api_login_confirmed": True,
                    "query_started_at": "2026-06-20T00:00:00Z",
                    "query_completed_at": "2026-06-20T00:00:00Z",
                    "raw_secret_values_recorded": False,
                    "raw_broker_endpoint_recorded": False,
                    "screenshot_used_for_values": False,
                    "order_action_sent": False,
                    "cancel_order_sent": False,
                    "replace_order_sent": False,
                    "account_ref": "ib-account-ref://U3028269",
                    "open_orders": [],
                    "open_order_rows": 0,
                    "readonly_query": {
                        "api_call": "reqAllOpenOrders",
                        "callback_rows": ["openOrder", "orderStatus", "openOrderEnd"],
                        "query_scope": "synthetic_current_tws_session_open_orders_visible_to_api_client",
                        "order_action_sent": False,
                        "cancel_order_sent": False,
                        "replace_order_sent": False,
                        "complete_history_claimed": False,
                    },
                    "query_checksum": "sha256:abababababababababababababababababababababababababababababababab",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        package = builder.build_source_package(
            account_summary_path=ACCOUNT_SUMMARY,
            positions_path=POSITIONS,
            executions_query_path=executions,
            open_orders_query_path=open_orders,
            readiness_probe_path=READINESS,
            output_path=output,
            allow_blocked=False,
        )
        output.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    require(package["schema_version"] == "account_source_artifact.v1", "source package schema mismatch")
    require(package["account_id"] == "acct.ib.live.u3028269", "source package account mismatch")
    require(package["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(package["source_mode"] == "live_observation", "ready source mode mismatch")
    require(package["source_health"]["state"] == "ready", "ready package health mismatch")
    require(package["source_health"]["api_transport"] == "ib_tws_api", "ready package transport mismatch")
    require(package["source_health"]["raw_secret_values_recorded"] is False, "ready package recorded secrets")
    require(package["source_health"]["screenshot_used_for_values"] is False, "ready package used screenshot values")
    require(package["boundaries"]["screenshot_used_for_funds_positions"] is False, "ready package screenshot boundary drifted")
    require(package["boundaries"]["order_action_sent"] is False, "ready package order action drifted")
    require(package["blockers"] == [], "ready package must not carry blockers")
    require(len(package["balances"]) == 2, "ready package balances did not map from query fixture")
    require(len(package["positions"]) == 2, "ready package positions did not map from query fixture")
    require(package["balances"][0]["equity"] == 100000.0, "net liquidation should map to equity")
    require(package["balances"][0]["available_cash"] == 75000.0, "available funds should map to available_cash")
    positions_by_instrument = {row["instrument"]: row for row in package["positions"]}
    require(positions_by_instrument["AAPL"]["direction"] == "long", "positive position should map long")
    require(positions_by_instrument["MSFT"]["direction"] == "short", "negative position should map short")

    bundle = source_artifact_to_capability_bundle(package)
    require(bundle["account"]["account_id"] == "acct.ib.live.u3028269", "bundle account mismatch")
    require(bundle["capabilities"]["observation"]["mirror_state"] == "ready", "ready package must project ready mirror state")
    require(bundle["capabilities"]["command"]["enabled"] is False, "ready observation must not enable command")
    require(bundle["route_context"]["account_truth"] == "ib_tws_api_source_package", "ready route context truth mismatch")
    require(bundle["route_context"]["blocker_id"] is None, "ready route context must not carry blocker")
    require(bundle["boundaries"]["broker_truth"] is False, "ready mirror projection must not claim broker truth")
    require(bundle["boundaries"]["order_action"] is False, "ready mirror projection must not allow order action")
    require(len(bundle["observations"]["balances"]) == 2, "bundle balances missing")
    require(len(bundle["observations"]["positions"]) == 2, "bundle positions missing")

    for value in walk_values(package):
        if isinstance(value, str):
            lowered = value.lower()
            require("127.0.0.1:" not in lowered, "ready package must not record raw endpoint")
            require("password=" not in lowered and "secret=" not in lowered, "ready package must not record secrets")
    for term in [
        "validate_p019_ib_tws_ready_source_contract.py",
        "P019_IB_TWS_READY_SOURCE_CONTRACT_OK",
    ]:
        require(term in acceptance, f"acceptance missing ready source contract term {term}")
        require(term in phase_plan, f"phase plan missing ready source contract term {term}")

    print("P019_IB_TWS_READY_SOURCE_CONTRACT_OK: synthetic_ready_fixture=true mirror_state=ready command=false")


if __name__ == "__main__":
    main()
