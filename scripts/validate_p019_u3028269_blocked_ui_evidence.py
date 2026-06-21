from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-blocked-projection.spec.ts"
P019_ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"


class EvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def main() -> None:
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    acceptance = P019_ACCEPTANCE.read_text(encoding="utf-8")

    require(
        payload["schema"] == "account-console.p019-u3028269-blocked-ui-parity-evidence.v1",
        "schema drifted",
    )
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal_id mismatch")
    require(payload["status"] == "blocked_waiting_for_tws_api_readiness_and_real_source_package", "status drifted")
    require(payload["verdict"] == "blocked", "verdict must stay blocked")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account_id mismatch")
    require(payload["display_alias"] == "U3028269", "display alias mismatch")
    require(payload["route"] == "/accounts/acct.ib.live.u3028269", "route mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source_kind mismatch")
    require(payload["blocker_id"] == "tws_api_readiness_missing", "blocker mismatch")
    require(payload["blocker_kind"] == "source_unavailable", "blocker kind mismatch")
    require(payload["projection_checksum"].startswith("sha256:"), "projection checksum missing")
    require(payload["source_checksum"].startswith("sha256:"), "source checksum missing")

    for key in [
        "funds_parity",
        "positions_parity",
        "orders_fills_parity",
        "execution_reports_table_parity",
        "execution_reports_persistence_parity",
    ]:
        require(payload["parity"][key] == "blocked", f"{key} must be blocked")

    for testid in [
        "tws-multi-currency-funds-table",
        "tws-funds-blocker",
        "tws-fx-provenance",
        "account-positions-table",
        "account-bottom-tape",
        "tws-execution-reports-table",
        "tws-execution-report-blocker",
    ]:
        require(testid in payload["ui_surfaces"].values(), f"evidence missing testid {testid}")
        require(testid in spec, f"Playwright spec missing testid {testid}")

    require(payload["browser_evidence"], "browser evidence missing")
    for item in payload["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty screenshot {item['screenshot']}")

    for non_claim in [
        "does_not_accept_adr0005",
        "does_not_open_direct_tws_session",
        "does_not_prove_tws_api_funds_parity",
        "does_not_prove_tws_api_positions_parity",
        "does_not_prove_order_or_fill_truth",
        "does_not_enable_command_capability",
        "does_not_record_raw_secret_values",
    ]:
        require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["direct_session_allowed"] is False, "direct TWS session must stay blocked")
    require(boundaries["broker_truth"] is False, "broker truth must stay false")
    require(boundaries["order_action"] is False, "order action must stay false")

    for term in [
        "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json",
        "funds_parity",
        "execution_reports_table_parity",
    ]:
        require(term in acceptance, f"P019 acceptance missing evidence term {term}")

    print("P019_U3028269_BLOCKED_UI_EVIDENCE_OK: verdict=blocked surfaces=7")


if __name__ == "__main__":
    main()
