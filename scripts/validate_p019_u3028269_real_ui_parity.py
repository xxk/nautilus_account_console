from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json"
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-real-ui-parity.spec.ts"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
UI_ACCEPTANCE = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "tws-account-workbench-ui-acceptance.md"
)


class RealUiParityError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RealUiParityError(message)


def main() -> None:
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")
    ui_acceptance = UI_ACCEPTANCE.read_text(encoding="utf-8")

    require(payload["schema"] == "account-console.p019-u3028269-real-ui-parity-evidence.v1", "schema mismatch")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["route"] == "/accounts/acct.ib.live.u3028269", "route mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(payload["source_checksum"].startswith("sha256:"), "source checksum missing")
    require(payload["projection_checksum"].startswith("sha256:"), "projection checksum missing")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshot must not be funds/positions truth")
    require(boundaries["broker_truth"] is False, "UI parity must not claim broker truth")
    require(boundaries["order_action"] is False, "UI parity must not enable order action")

    for item in payload["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty screenshot {item['screenshot']}")

    parity = payload["parity"]
    if payload["verdict"] == "blocked":
        require(payload["status"] == "blocked_waiting_for_real_tws_api_source_package", "blocked status mismatch")
        require(payload["blocker_id"] == "tws_api_readiness_missing", "blocked evidence must name TWS API readiness blocker")
        require(parity["funds_parity"] == "blocked", "blocked evidence cannot pass funds parity")
        require(parity["positions_parity"] == "blocked", "blocked evidence cannot pass positions parity")
        for non_claim in [
            "does_not_prove_real_u3028269_funds",
            "does_not_prove_real_u3028269_positions",
            "does_not_close_real_ui_parity",
            "does_not_use_screenshot_for_funds_positions",
            "does_not_enable_command_capability",
        ]:
            require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")
    else:
        require(payload["verdict"] == "pass", "verdict must be blocked or pass")
        require(
            payload["status"] == "ready_real_tws_api_source_package_ui_parity_checked",
            "pass status mismatch",
        )
        require(parity["funds_parity"] == "pass", "ready evidence must pass funds parity")
        require(parity["positions_parity"] == "pass", "ready evidence must pass positions parity")
        require(payload["compared_against"]["api_route"] == "/api/mirror/accounts/acct.ib.live.u3028269", "API route mismatch")
        require(payload["compared_against"]["balance_count"] > 0, "ready parity must include balance rows")
        require(payload["compared_against"]["position_count"] >= 0, "position count missing")

    for term in [
        "/api/mirror/accounts/",
        "tws-multi-currency-funds-table",
        "account-position-projection-row",
        "formatMoney",
        "screenshot_used_for_funds_positions: false",
    ]:
        require(term in spec, f"spec missing {term}")

    for term in [
        "2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
        "validate_p019_u3028269_real_ui_parity.py",
        "P019_U3028269_REAL_UI_PARITY_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    for term in [
        "UI-TWS-13",
        "UI-TWS-14",
        "machine-readable parity evidence compares Web UI rendered values against TWS API/source package values",
    ]:
        require(term in ui_acceptance, f"UI acceptance missing {term}")

    print(f"P019_U3028269_REAL_UI_PARITY_OK: verdict={payload['verdict']}")


if __name__ == "__main__":
    main()
