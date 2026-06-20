from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TWS_API_DIR = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api"
ACCOUNT_SUMMARY = TWS_API_DIR / "account_summary.json"
POSITIONS = TWS_API_DIR / "positions.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
FIXTURE_DIR = ROOT / "contracts" / "broker_observation" / "fixtures"
SYNTHETIC_ACCOUNT_SUMMARY = FIXTURE_DIR / "ib_tws_u3028269_ready_query_account_summary.synthetic.json"
SYNTHETIC_POSITIONS = FIXTURE_DIR / "ib_tws_u3028269_ready_query_positions.synthetic.json"
SYNTHETIC_READINESS = FIXTURE_DIR / "ib_tws_u3028269_ready_readiness.synthetic.json"
BUILDER_PATH = ROOT / "scripts" / "build_ib_u3028269_source_package_from_tws_api.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class QuerySourceParityError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QuerySourceParityError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def import_builder():
    spec = importlib.util.spec_from_file_location("p019_ib_source_builder", BUILDER_PATH)
    require(spec is not None and spec.loader is not None, "builder module spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_boundaries(payload: dict[str, Any], label: str) -> None:
    require(payload["raw_secret_values_recorded"] is False, f"{label}: raw secrets recorded")
    require(payload["raw_broker_endpoint_recorded"] is False, f"{label}: raw endpoint recorded")
    require(payload["screenshot_used_for_values"] is False, f"{label}: screenshot used for values")
    require(payload["order_action_sent"] is False, f"{label}: order action sent")


def assert_ready_query_to_source_parity(account_summary: dict[str, Any], positions: dict[str, Any], package: dict[str, Any]) -> None:
    require(account_summary["success"] is True, "ready account summary query must succeed")
    require(positions["success"] is True, "ready positions query must succeed")
    require(package["source_health"]["state"] == "ready", "package must be ready")
    require(package["source_inputs"]["account_summary_query"], "package missing account summary ref")
    require(package["source_inputs"]["positions_query"], "package missing positions ref")

    query_balances = account_summary["balances"]
    package_balances = package["balances"]
    require(len(package_balances) == len(query_balances), "balance row count mismatch")
    for query_row, package_row in zip(query_balances, package_balances):
        require(package_row["currency"] == query_row["currency"], "balance currency mismatch")
        require(package_row["equity"] == float(query_row["net_liquidation"]), "net liquidation did not map to equity")
        require(package_row["available_cash"] == float(query_row["available_funds"]), "available funds mismatch")
        require(package_row["margin_used"] == float(query_row.get("margin_used") or 0.0), "margin used mismatch")
        require(package_row["unrealized_pnl"] == float(query_row.get("unrealized_pnl") or 0.0), "unrealized pnl mismatch")

    query_positions = positions["positions"]
    package_positions = package["positions"]
    require(len(package_positions) == len(query_positions), "position row count mismatch")
    for query_row, package_row in zip(query_positions, package_positions):
        net_qty = float(query_row.get("net_qty") or 0.0)
        require(package_row["instrument"] == query_row["instrument"], "position instrument mismatch")
        require(package_row["exchange"] == query_row.get("exchange"), "position exchange mismatch")
        require(package_row["direction"] == ("long" if net_qty >= 0 else "short"), "position direction mismatch")
        require(package_row["net_qty"] == net_qty, "position net qty mismatch")
        require(package_row["available_qty"] == net_qty, "position available qty mismatch")
        expected_avg = None if query_row.get("avg_cost") is None else float(query_row["avg_cost"])
        require(package_row["avg_price"] == expected_avg, "position avg price mismatch")
        expected_pnl = None if query_row.get("unrealized_pnl") is None else float(query_row["unrealized_pnl"])
        require(package_row["unrealized_pnl"] == expected_pnl, "position unrealized pnl mismatch")


def main() -> None:
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    source_package = load(SOURCE_PACKAGE)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(account_summary["schema"] == "account-console.ib-tws-api-query.v1", "account summary schema mismatch")
    require(positions["schema"] == "account-console.ib-tws-api-query.v1", "positions schema mismatch")
    require(source_package["schema_version"] == "account_source_artifact.v1", "source package schema mismatch")
    assert_boundaries(account_summary, "account_summary")
    assert_boundaries(positions, "positions")
    require(source_package["boundaries"]["raw_secret_values_recorded"] is False, "source package recorded secrets")
    require(
        source_package["boundaries"]["screenshot_used_for_funds_positions"] is False,
        "source package used screenshot values",
    )
    require(source_package["boundaries"]["order_action_sent"] is False, "source package sent order action")

    if source_package["source_health"]["state"] == "blocked":
        require(account_summary["success"] is False, "blocked package cannot pair with successful account summary")
        require(positions["success"] is False, "blocked package cannot pair with successful positions")
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "account summary blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "positions blocker mismatch")
        require(source_package["source_health"]["blocker_id"] == "tws_api_readiness_missing", "source blocker mismatch")
        require(source_package["balances"] == [], "blocked package must not invent balances")
        require(source_package["positions"] == [], "blocked package must not invent positions")
        current_status = "blocked"
    else:
        assert_ready_query_to_source_parity(account_summary, positions, source_package)
        current_status = "ready"

    builder = import_builder()
    synthetic_account_summary = load(SYNTHETIC_ACCOUNT_SUMMARY)
    synthetic_positions = load(SYNTHETIC_POSITIONS)
    with tempfile.TemporaryDirectory(prefix="p019-query-source-parity-") as tmp:
        output = Path(tmp) / "source-package.json"
        synthetic_package = builder.build_source_package(
            account_summary_path=SYNTHETIC_ACCOUNT_SUMMARY,
            positions_path=SYNTHETIC_POSITIONS,
            readiness_probe_path=SYNTHETIC_READINESS,
            output_path=output,
            allow_blocked=False,
        )
    assert_ready_query_to_source_parity(synthetic_account_summary, synthetic_positions, synthetic_package)

    for term in [
        "validate_p019_ib_u3028269_query_source_parity.py",
        "P019_IB_U3028269_QUERY_SOURCE_PARITY_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print(f"P019_IB_U3028269_QUERY_SOURCE_PARITY_OK: current={current_status} synthetic_ready=pass")


if __name__ == "__main__":
    main()
