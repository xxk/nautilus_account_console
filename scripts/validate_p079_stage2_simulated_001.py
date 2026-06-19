from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
UPSTREAM_CONTRACT = (
    ROOT.parent
    / "nautilus_strategies"
    / "docs"
    / "changes"
    / "20260615__paper__p079-stage2-025292-market-data-only-simulated-001-planning"
    / "evidence"
    / "stage2_environment_account_contract.json"
)
SOURCE_ARTIFACT = (
    ROOT
    / "contracts"
    / "source_artifacts"
    / "account_sources"
    / "nautilus_sandbox_paper_simulated_001_source.json"
)
SPEC = ROOT / "frontend" / "tests" / "e2e" / "account-terminal-workbench.spec.ts"
ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-p079-stage2-simulated-001-account-console-acceptance.md"
HANDOFF = ROOT / "docs" / "acceptance" / "2026-06-15-p079-stage2-simulated-001-handoff.json"

sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.main import app  # noqa: E402


class Stage2Error(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Stage2Error(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    upstream = load_json(UPSTREAM_CONTRACT)
    source = load_json(SOURCE_ARTIFACT)
    spec = SPEC.read_text(encoding="utf-8")
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    handoff = load_json(HANDOFF)

    sandbox = upstream["sandbox_paper_account"]
    market = upstream["market_source"]
    trading = upstream["trading_source"]

    require(source["account_id"] == sandbox["account_id"] == "simulated-001", "account_id mismatch")
    require(source["account_uid"] == sandbox["account_uid"] == "sandbox-paper.simulated-001", "account_uid mismatch")
    require(source["account_type"] == sandbox["account_type"] == "sandbox_paper", "account_type mismatch")
    require(source["ledger_type"] == "simulated_sandbox_ledger", "ledger_type mismatch")
    require(source["market_data_account_id"] == market["market_data_account_id"] == "025292", "market source mismatch")
    require(source["market_data_role"] == "market_data_only", "market data role mismatch")
    require(market["broker_order_submission_allowed"] is False, "025292 broker submission must be false")
    require(trading["trading_adapter"] == "disabled", "trading adapter must be disabled")
    require(trading["broker_order_submission_allowed"] is False, "trading broker submission must be false")
    require(source["broker_order_submission"] is False, "source broker_order_submission must be false")
    require(source["trading_adapter"] == "disabled", "source trading_adapter must be disabled")
    require(source["stage"] == "R1/P079 Stage 2", "stage mismatch")
    require(handoff["status"] == "ready_for_next_session", "handoff status mismatch")
    require(handoff["account_opening"]["account_id"] == "simulated-001", "handoff account_id mismatch")
    require(handoff["account_opening"]["ui_entry"] == "/accounts/simulated-001", "handoff UI entry mismatch")
    require(handoff["account_opening"]["api_entry"] == "/api/mirror/accounts/simulated-001", "handoff API entry mismatch")
    require(handoff["market_boundary"]["market_data_role"] == "market_data_only", "handoff market role mismatch")
    require(handoff["market_boundary"]["ctp_trading_front_order_submission"] is False, "handoff CTP trading submission must be false")
    require(handoff["execution_boundary"]["broker_order_submission"] is False, "handoff broker submission must be false")
    require(handoff["execution_boundary"]["trading_adapter"] == "disabled", "handoff trading adapter must be disabled")
    require(handoff["blocker"]["blocker_id"] == "simulated001_stage2_fixture_only", "handoff blocker mismatch")
    require(
        handoff["browser_evidence"]["viewport_coverage"] == ["desktop", "tablet", "mobile"],
        "handoff browser viewport coverage mismatch",
    )
    screenshots = handoff["browser_evidence"]["screenshots"]
    require(len(screenshots) == 3, "handoff must include three simulated-001 screenshots")
    for screenshot in screenshots:
        screenshot_path = ROOT / screenshot
        require(screenshot_path.exists(), f"missing simulated-001 browser evidence screenshot {screenshot}")
        require(screenshot_path.stat().st_size > 0, f"empty simulated-001 browser evidence screenshot {screenshot}")

    client = TestClient(app)
    list_response = client.get("/api/mirror/accounts")
    require(list_response.status_code == 200, "mirror list failed")
    account_ids = {row["account_id"] for row in list_response.json()["accounts"]}
    require("simulated-001" in account_ids, "simulated-001 missing from account list")

    detail = client.get("/api/mirror/accounts/simulated-001")
    require(detail.status_code == 200, "simulated-001 detail missing")
    payload = detail.json()
    require(payload["account_id"] == "simulated-001", "detail account_id mismatch")
    require(payload["account_domain"] == "sandbox", "simulated-001 must be sandbox domain")
    require(payload["source_kind"] == "nautilus_sandbox_paper", "simulated-001 source_kind mismatch")
    require(payload["capabilities"]["command"]["enabled"] is False, "command must be disabled")
    require(payload["boundaries"]["order_action"] is False, "Account Console must not own order action")
    require(payload["boundaries"]["account_truth"] is False, "Account Console must not own account truth")
    require(payload["boundaries"]["capital_truth"] is False, "Account Console must not own capital truth")
    require(any(row["instrument"] == "ag2612" and row["net_qty"] == 1 for row in payload["positions"]), "ag2612 long-one position missing")
    require(
        any(
            row["client_order_id"] == "simulated-001-ag2612-buy-1-001"
            and row["instrument"] == "ag2612"
            and row["status"] == "filled"
            for row in payload["orders"]
        ),
        "ag2612 buy-one filled order missing",
    )

    health = payload["source_health"]
    require(health["market_data_account_id"] == "025292", "025292 market data id missing from read-model")
    require(health["market_data_role"] == "market_data_only", "025292 must be market_data_only")
    require(health["execution_target"] == "Nautilus Sandbox Paper", "execution target mismatch")
    require(health["orders_scope"] == "simulated ledger only", "orders scope mismatch")
    require(health["broker_order_submission"] is False, "broker order submission must be false in read-model")
    require(health["trading_adapter"] == "disabled", "trading adapter must be disabled in read-model")
    require(health["account_console_writes_truth"] is False, "Account Console must not write truth")

    ctp025292 = client.get("/api/mirror/accounts/acct.ctp.live.025292").json()
    require(ctp025292["capabilities"]["command"]["enabled"] is False, "025292 command must remain disabled")
    require(ctp025292["boundaries"]["order_action"] is False, "025292 must not expose order action")
    require(ctp025292["source_health"]["state"] == "blocked", "025292 remains read-only blocked account projection")

    for phrase in [
        "simulated-001",
        "sandbox-paper.simulated-001",
        "CTP 025292 official market data only",
        "Nautilus Sandbox Paper",
        "simulated ledger only",
        "R1/P079 Stage 2",
    ]:
        require(phrase in spec, f"UI spec missing assertion phrase {phrase}")

    for scenario in [
        "S1 开户：simulated-001 registry/read-model exists",
        "S2 开户：025292 is market data only",
        "S3 开户：execution target is Nautilus Sandbox Paper",
        "S4 开户：Account Console is projection/operator surface only",
        "S5 开户：fixture-only blocker is explicit",
    ]:
        require(scenario in acceptance, f"acceptance missing scenario {scenario}")

    forbidden = [
        "submit_order_to_ctp_025292",
        "use_025292_trading_adapter",
        "paper_ready",
        "live_ready",
        "production_ready",
        "capital_allocated",
        "broker_tradable",
        "can_trade",
    ]
    combined = json.dumps(source, sort_keys=True).lower() + "\n" + spec.lower()
    for phrase in forbidden:
        require(phrase.lower() not in combined, f"forbidden claim present: {phrase}")
        require(phrase in handoff["forbidden_claims"], f"handoff missing forbidden claim {phrase}")

    for non_claim in [
        "no_order_sent_to_ctp_025292",
        "no_real_broker_account_created",
        "no_readiness_claim",
    ]:
        require(non_claim in handoff["explicit_non_claims"], f"handoff missing non-claim {non_claim}")

    print("P079_STAGE2_SIMULATED_001_OK: account=simulated-001 market_source=025292 role=market_data_only screenshots=3")


if __name__ == "__main__":
    main()
