from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-15-p011-account-workbench-api-readback-browser-evidence.json"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "account-terminal-workbench.spec.ts"
ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-ui-readback-acceptance.md"
P079_ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-p079-stage2-simulated-001-account-console-acceptance.md"


class EvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def main() -> None:
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    p079_acceptance = P079_ACCEPTANCE.read_text(encoding="utf-8")

    require(payload["schema"] == "account-console.p011-account-workbench-api-readback-browser-evidence.v1", "schema drifted")
    require(payload["status"] == "implementation_browser_evidence", "status must be implementation_browser_evidence")
    require(payload["proposal_id"] == "p011-account-capability-contracts", "proposal_id mismatch")
    require(payload["verdict"] == "passed", "evidence verdict must be passed")

    for route in [
        "/accounts/acct.demo-19053",
        "/accounts/acct.ctp.paper.19053",
        "/accounts/acct.ctp.live.025292",
        "/accounts/simulated-001",
    ]:
        require(route in payload["routes_opened"], f"evidence missing route {route}")
        require(route in spec, f"Playwright spec missing route {route}")
    for route in ["/accounts/acct.ctp.paper.19053", "/accounts/acct.ctp.live.025292"]:
        require(route in acceptance, f"acceptance doc missing route {route}")
    require("/accounts/simulated-001" in p079_acceptance, "P079 acceptance doc missing simulated-001 route")

    require(payload["viewport_coverage"] == ["desktop", "tablet", "mobile"], "viewport coverage must be desktop/tablet/mobile")
    browser_evidence = payload["browser_evidence"]
    require(len(browser_evidence) == 12, "expected twelve browser screenshots for four routes across three viewports")
    expected_routes = {
        "/accounts/acct.demo-19053",
        "/accounts/acct.ctp.paper.19053",
        "/accounts/acct.ctp.live.025292",
        "/accounts/simulated-001",
    }
    expected_projects = {"desktop", "tablet", "mobile"}
    observed = {(item["route"], item["project"]) for item in browser_evidence}
    require(
        observed == {(route, project) for route in expected_routes for project in expected_projects},
        "browser evidence route/project matrix drifted",
    )
    for item in browser_evidence:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing browser evidence screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty browser evidence screenshot {item['screenshot']}")

    ctp19053 = payload["positive_assertions"]["ctp19053"]
    require(ctp19053["canonical_account_id_visible"] == "acct.ctp.paper.19053", "19053 canonical account drifted")
    require(ctp19053["display_alias_visible"] == "19053", "19053 alias drifted")
    require(ctp19053["readback_mode"] == "mirror API", "19053 must use mirror API readback")
    for expected in [
        "account-summary-cash",
        "No position rows in this fixture projection.",
        "No order rows in this fixture projection.",
        "source unavailable",
    ]:
        require(expected in spec, f"Playwright spec missing 19053 assertion {expected}")

    ctp025292 = payload["positive_assertions"]["ctp025292"]
    require(ctp025292["canonical_account_id_visible"] == "acct.ctp.live.025292", "025292 canonical account drifted")
    require(ctp025292["blocked_projection_visible"] is True, "025292 must remain blocked projection evidence")
    require(ctp025292["blocker_visible"] == "source unavailable", "025292 blocker text drifted")
    require(ctp025292["source_health_visible"] == "typed_blocker", "025292 source health must be typed blocker")
    require(ctp025292["execution_reports_empty"] is True, "025292 execution reports must remain empty while blocked")

    simulated001 = payload["positive_assertions"]["simulated001"]
    require(simulated001["canonical_account_id_visible"] == "simulated-001", "simulated-001 account id drifted")
    require(simulated001["account_uid_visible"] == "sandbox-paper.simulated-001", "simulated-001 account uid drifted")
    require(simulated001["market_visible"] == "CTP 025292 official market data only", "simulated-001 market boundary drifted")
    require(simulated001["execution_visible"] == "Nautilus Sandbox Paper", "simulated-001 execution boundary drifted")
    require(simulated001["orders_scope_visible"] == "simulated ledger only", "simulated-001 order scope drifted")
    require(simulated001["broker_submission_visible"] == "disabled", "simulated-001 broker submission drifted")
    for expected in [
        "simulated-001",
        "sandbox-paper.simulated-001",
        "CTP 025292 official market data only",
        "Nautilus Sandbox Paper",
        "simulated ledger only",
        "simulated_sandbox_ledger",
        "R1/P079 Stage 2",
    ]:
        require(expected in spec, f"Playwright spec missing simulated-001 assertion {expected}")

    forbidden = payload["negative_assertions"]
    for phrase in ["submit order text is absent", "cancel order text is absent", "replace order text is absent"]:
        require(phrase in forbidden, f"missing negative assertion {phrase}")
    for non_claim in [
        "does_not_prove_broker_truth",
        "does_not_prove_order_action_authority",
        "does_not_complete_ctp025292_real_account_consistency",
    ]:
        require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")

    print("P011_UI_READBACK_EVIDENCE_OK: routes=4 screenshots=12 verdict=passed")


if __name__ == "__main__":
    main()
