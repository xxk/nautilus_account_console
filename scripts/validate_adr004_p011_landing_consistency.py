from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"

ADR = ROOT / "docs" / "adr" / "0004-adopt-account-mirror-observation-and-command-plane.md"
ADR_ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-adr0004-account-capability-fabric-acceptance.md"
ACCEPTANCE_INDEX = ROOT / "docs" / "acceptance" / "README.md"
CTP19053_ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-ui-readback-acceptance.md"
CTP19053_FUNDS_POSITIONS_EVIDENCE = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-funds-positions-ui-readback-evidence.json"
)
CTP19053_REAL_LOGIN_UI_EVIDENCE = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-real-login-ui-acceptance-evidence.json"
)
CTP19053_REAL_LOGIN_BLOCKER = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-real-login-ui-readback-blocker.json"
)
CTP19053_TEMPLATE = (
    ROOT / "contracts" / "source_artifacts" / "templates" / "ctp_paper_19053_source_package.template.json"
)
CTP19053_BLOCKER = ROOT / "docs" / "acceptance" / "2026-06-15-ctp19053-real-readback-blocker.json"
CTP025292_ACCEPTANCE = ROOT / "docs" / "acceptance" / "2026-06-15-ctp025292-real-account-consistency-acceptance.md"
CTP_SOURCE_OWNER_HANDOFF = ROOT / "docs" / "acceptance" / "2026-06-15-ctp-source-owner-package-handoff.md"
CTP_SOURCE_OWNER_HANDOFF_JSON = ROOT / "docs" / "acceptance" / "2026-06-15-ctp-source-owner-package-handoff.json"
CTP025292_TEMPLATE = (
    ROOT / "contracts" / "source_artifacts" / "templates" / "ctp_live_025292_source_package.template.json"
)
VSCODE_TASKS = ROOT / ".vscode" / "tasks.json"
TOPIC = ROOT / "docs" / "topics" / "T001-account-mirror-observation-plane.md"
P011_README = ROOT / "docs" / "proposals" / "p011-account-capability-contracts" / "README.md"
P011_PHASE_PLAN = ROOT / "docs" / "proposals" / "p011-account-capability-contracts" / "phase-plan.md"
P011_ACCEPTANCE = ROOT / "docs" / "proposals" / "p011-account-capability-contracts" / "acceptance.md"
P011_BROWSER_EVIDENCE = (
    ROOT / "docs" / "acceptance" / "2026-06-15-p011-account-workbench-api-readback-browser-evidence.json"
)
P079_ACCEPTANCE = (
    ROOT / "docs" / "acceptance" / "2026-06-15-p079-stage2-simulated-001-account-console-acceptance.md"
)
P079_HANDOFF = ROOT / "docs" / "acceptance" / "2026-06-15-p079-stage2-simulated-001-handoff.json"
CTP025292_BLOCKER = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp025292-real-account-consistency-blocker.json"
)
CTP025292_REAL_LOGIN_UI_EVIDENCE = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp025292-real-login-ui-acceptance-evidence.json"
)
CTP025292_REAL_LOGIN_BLOCKER = (
    ROOT / "docs" / "acceptance" / "2026-06-15-ctp025292-real-login-ui-readback-blocker.json"
)
COMMAND_GATE = ROOT / "contracts" / "account_capability" / "command_capability_design_gate.json"


sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.main import app  # noqa: E402


class LandingConsistencyError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LandingConsistencyError(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def require_all(text: str, phrases: list[str], owner: str) -> None:
    for phrase in phrases:
        require(phrase in text, f"{owner} missing phrase: {phrase}")


def main() -> None:
    adr = read_text(ADR)
    adr_acceptance = read_text(ADR_ACCEPTANCE)
    acceptance_index = read_text(ACCEPTANCE_INDEX)
    ctp19053_acceptance = read_text(CTP19053_ACCEPTANCE)
    ctp19053_funds_positions_evidence = read_json(CTP19053_FUNDS_POSITIONS_EVIDENCE)
    ctp19053_real_login_ui_evidence = read_json(CTP19053_REAL_LOGIN_UI_EVIDENCE)
    ctp19053_real_login_blocker = read_json(CTP19053_REAL_LOGIN_BLOCKER)
    ctp19053_template = read_json(CTP19053_TEMPLATE)
    ctp19053_blocker = read_json(CTP19053_BLOCKER)
    ctp025292_acceptance = read_text(CTP025292_ACCEPTANCE)
    ctp_source_owner_handoff = read_text(CTP_SOURCE_OWNER_HANDOFF)
    ctp_source_owner_handoff_json = read_json(CTP_SOURCE_OWNER_HANDOFF_JSON)
    ctp025292_template = read_json(CTP025292_TEMPLATE)
    vscode_tasks = read_json(VSCODE_TASKS)
    topic = read_text(TOPIC)
    p011_readme = read_text(P011_README)
    p011_phase_plan = read_text(P011_PHASE_PLAN)
    p011_acceptance = read_text(P011_ACCEPTANCE)
    p011_browser = read_json(P011_BROWSER_EVIDENCE)
    p079_acceptance = read_text(P079_ACCEPTANCE)
    p079_handoff = read_json(P079_HANDOFF)
    ctp025292_blocker = read_json(CTP025292_BLOCKER)
    ctp025292_real_login_ui_evidence = read_json(CTP025292_REAL_LOGIN_UI_EVIDENCE)
    ctp025292_real_login_blocker = read_json(CTP025292_REAL_LOGIN_BLOCKER)
    command_gate = read_json(COMMAND_GATE)

    require("landing_status: observation_only_in_progress" in adr, "ADR landing status drifted")
    require("observation-only in progress via T001/P011" in adr, "ADR summary must name T001/P011")
    require("CTP `025292` real-account consistency remains blocked" in adr, "ADR must keep 025292 blocker visible")
    require("passed_design_gate_only" in adr, "ADR must keep command as design gate only")

    require_all(
        adr_acceptance,
        [
            "API-backed Account Workbench browser acceptance",
            "npx playwright test tests/e2e/account-terminal-workbench.spec.ts",
            "docs/acceptance/2026-06-15-p011-account-workbench-api-readback-browser-evidence.json",
            "CTP `025292` real-account consistency remains blocked",
        ],
        "ADR acceptance",
    )
    require_all(
        acceptance_index,
        [
            "CTP 19053 UI readback acceptance](./2026-06-15-ctp19053-ui-readback-acceptance.md) | blocked_waiting_for_real_login_source_package",
            "CTP 19053 real-login UI evidence](./2026-06-15-ctp19053-real-login-ui-acceptance-evidence.json) | blocked_waiting_for_real_login_source_package",
            "CTP 025292 real-login UI evidence](./2026-06-15-ctp025292-real-login-ui-acceptance-evidence.json) | blocked_waiting_for_real_login_source_package",
            "CTP 19053 real source readback harness | blocked_waiting_for_source_package",
            "validate_ctp19053_consistency.py --write-blocker",
            "CTP 025292 real account consistency acceptance](./2026-06-15-ctp025292-real-account-consistency-acceptance.md) | blocked_waiting_for_real_login_source_package",
            "CTP source owner package handoff](./2026-06-15-ctp-source-owner-package-handoff.md) | blocked_waiting_for_source_owner_packages",
            "CTP source owner package handoff JSON](./2026-06-15-ctp-source-owner-package-handoff.json) | machine_readable_handoff",
            "ADR004/P011 landing consistency gate",
            "Current worktree management UI",
            "http://127.0.0.1:5175/accounts/acct.demo-19053",
            "four mirror accounts",
            "four UI routes including legacy `/accounts/acct.demo-19053`",
            "twelve screenshots",
        ],
        "acceptance index",
    )
    require_all(
        ctp19053_acceptance,
        [
            "- Status: implementation browser evidence available",
            "npx playwright test tests/e2e/account-terminal-workbench.spec.ts",
            "npx playwright test tests/e2e/ctp19053-ui-funds-positions.spec.ts --project=desktop",
            "/accounts/simulated-001",
            "desktop/tablet/mobile",
            "docs/acceptance/browser-evidence/p011-account-workbench-api-readback/",
            "contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json",
            "python scripts\\validate_ctp19053_consistency.py --write-blocker",
            "blocker_id: ctp19053_real_login_source_unavailable",
        ],
        "CTP 19053 acceptance",
    )
    require(ctp19053_template["account_id"] == "acct.ctp.paper.19053", "19053 template account id drifted")
    require(ctp19053_template["display_alias"] == "19053", "19053 template display alias drifted")
    require(ctp19053_template["source_owner"] == "nautilus_ctp_adapter", "19053 template source owner drifted")
    require(ctp19053_template["observation_mode"] == "snapshot", "19053 template observation mode drifted")
    require(ctp19053_template["event_stream"] == "not_implemented", "19053 template event stream drifted")
    require("command" not in ctp19053_template, "19053 template must not carry command capability")
    require(ctp19053_blocker["blocker_id"] == "ctp19053_source_unavailable", "19053 blocker id drifted")
    require(ctp19053_blocker["verdict"] == "blocked", "19053 blocker verdict drifted")
    require(
        ctp19053_blocker.get("template_ref")
        == "contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json",
        "19053 blocker template ref drifted",
    )
    require("desktop/tablet/mobile" in ctp19053_acceptance, "CTP 19053 aggregate acceptance must keep viewport coverage")
    require(
        ctp19053_funds_positions_evidence["verdict"] == "passed_for_ui_readback_against_pinned_projection",
        "historical CTP 19053 sample projection evidence drifted",
    )
    require(
        "does_not_prove_current_broker_truth" in ctp19053_funds_positions_evidence["explicit_non_claims"],
        "historical CTP 19053 sample evidence must not claim broker truth",
    )
    require(ctp19053_real_login_ui_evidence["verdict"] == "blocked", "CTP 19053 real-login UI evidence must be blocked")
    require(
        ctp19053_real_login_ui_evidence["status"] == "blocked_waiting_for_real_login_source_package",
        "CTP 19053 real-login UI status drifted",
    )
    require(
        ctp19053_real_login_ui_evidence["source_ref"]
        == "output/account_capability/ctp-paper-19053/source-package.json",
        "CTP 19053 real-login source ref drifted",
    )
    require(
        "does_not_display_repo_local_sample_as_real_account"
        in ctp19053_real_login_ui_evidence["explicit_non_claims"],
        "CTP 19053 real-login evidence missing sample non-claim",
    )
    require(
        ctp19053_real_login_blocker["blocker_id"] == "ctp19053_real_login_td_bridge_unavailable",
        "CTP 19053 real-login blocker drifted",
    )
    ctp19053_screenshot = ROOT / ctp19053_real_login_ui_evidence["browser_evidence"][0]["screenshot"]
    require(ctp19053_screenshot.exists(), "CTP 19053 funds/positions screenshot missing")
    require(ctp19053_screenshot.stat().st_size > 0, "CTP 19053 funds/positions screenshot empty")
    require_all(
        ctp025292_acceptance,
        [
            "- Status: blocked_waiting_for_real_login_source_package",
            "Current blocker record",
            "python scripts\\validate_ctp025292_consistency.py --write-blocker",
            "npx playwright test tests/e2e/ctp025292-ui-funds-positions.spec.ts --project=desktop",
            "blocker_id: ctp025292_source_unavailable",
            "blocker_id: ctp025292_real_login_td_bridge_unavailable",
            "contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json",
            "The sample harness proves the comparison logic only; it does not prove real account consistency",
        ],
        "CTP 025292 acceptance",
    )
    require_all(
        ctp_source_owner_handoff,
        [
            "- Status: blocked_waiting_for_source_owner_packages",
            "output/account_capability/ctp-paper-19053/source-package.json",
            "output/account_capability/ctp-live-025292/source-package.json",
            "contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json",
            "contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json",
            "python scripts\\validate_ctp19053_consistency.py --write-blocker",
            "python scripts\\validate_ctp025292_consistency.py --write-blocker",
            "password",
            "command",
            "Both real-source acceptances remain blocked until source-owner packages exist",
        ],
        "CTP source owner handoff",
    )
    require(
        ctp_source_owner_handoff_json["schema"] == "account-console.ctp-source-owner-package-handoff.v1",
        "CTP source owner handoff schema drifted",
    )
    require(
        ctp_source_owner_handoff_json["status"] == "blocked_waiting_for_source_owner_packages",
        "CTP source owner handoff status drifted",
    )
    package_by_account = {package["account_id"]: package for package in ctp_source_owner_handoff_json["packages"]}
    require(set(package_by_account) == {"acct.ctp.paper.19053", "acct.ctp.live.025292"}, "CTP handoff account set drifted")
    require(
        package_by_account["acct.ctp.paper.19053"]["required_package_path"]
        == "output/account_capability/ctp-paper-19053/source-package.json",
        "19053 handoff package path drifted",
    )
    require(
        package_by_account["acct.ctp.live.025292"]["required_package_path"]
        == "output/account_capability/ctp-live-025292/source-package.json",
        "025292 handoff package path drifted",
    )
    for field in ["password", "auth_code", "token", "secret", "session_password", "command"]:
        require(field in ctp_source_owner_handoff_json["forbidden_fields"], f"CTP handoff missing forbidden field {field}")
    for claim in ["Paper ready", "Live ready", "broker tradable", "can trade"]:
        require(claim in ctp_source_owner_handoff_json["forbidden_claims"], f"CTP handoff missing forbidden claim {claim}")
    for command in [
        "python scripts\\validate_ctp19053_consistency.py --source-package output\\account_capability\\ctp-paper-19053\\source-package.json",
        "python scripts\\validate_ctp025292_consistency.py --source-package output\\account_capability\\ctp-live-025292\\source-package.json",
        "python scripts\\validate_adr004_p011_landing_consistency.py",
    ]:
        require(command in ctp_source_owner_handoff_json["acceptance_commands_after_real_packages"], f"CTP handoff missing command {command}")
    require(ctp025292_template["account_id"] == "acct.ctp.live.025292", "025292 template account id drifted")
    require(ctp025292_template["display_alias"] == "025292", "025292 template display alias drifted")
    require(ctp025292_template["source_owner"] == "nautilus_ctp_adapter", "025292 template source owner drifted")
    require(ctp025292_template["observation_mode"] == "snapshot", "025292 template observation mode drifted")
    require(ctp025292_template["event_stream"] == "not_implemented", "025292 template event stream drifted")
    require("command" not in ctp025292_template, "025292 template must not carry command capability")
    require("T001-GATE-CAPABILITY-REGISTRY" in topic, "T001 capability registry gate missing")
    require("Until then, Account Console must not show submit, cancel, replace or broker action controls." in topic, "T001 command freeze drifted")

    require_all(
        p011_readme,
        [
            "P011 is the single landing proposal for ADR-0004",
            "P012-P017 are not separate proposals",
            "Phase 1 through Phase 5 are accepted",
            "Phase 6 is blocked",
            "ADR-0047",
            "AccountRuntimeContext",
            "market_data_source",
            "execution_adapter",
            "account_truth",
            "Phase 7 is accepted as a design gate only",
            "simulated-001",
        ],
        "P011 README",
    )
    require_all(
        p011_phase_plan,
        [
            "ACCOUNT_SOURCE_BRIDGES_OK: bundles=4 projections=4",
            "ACCOUNT_MIRROR_API_OK: accounts=4",
            "desktop/tablet/mobile UI readback",
            "simulated-001",
            "Phase 6a ADR-0047 route/context alignment",
            "market_data_source",
            "execution_adapter",
            "account_truth",
            "evidence_partition",
            "blocked",
        ],
        "P011 phase plan",
    )
    require_all(
        p011_acceptance,
        [
            "ACCOUNT_SOURCE_BRIDGES_OK: bundles=4 projections=4",
            "ACCOUNT_MIRROR_API_OK: accounts=4",
            "P011_UI_READBACK_EVIDENCE_OK: routes=4 screenshots=12 verdict=passed",
            "P079_STAGE2_SIMULATED_001_OK: account=simulated-001 market_source=025292 role=market_data_only screenshots=3",
            "COMMAND_CAPABILITY_DESIGN_GATE_OK: phase=p011.phase_7 status=design_gate_only",
            "blocked_waiting_for_source_owner_packages",
            "ADR-0047 route/context alignment gate",
            "market_data_source",
            "execution_adapter",
            "account_truth",
            "evidence_partition",
            "19 passed",
        ],
        "P011 acceptance",
    )

    require(p011_browser["verdict"] == "passed", "P011 browser evidence verdict drifted")
    manual_ui_entry = p011_browser["manual_ui_entry"]
    require(
        manual_ui_entry["url"] == "http://127.0.0.1:5175/accounts/acct.demo-19053",
        "manual UI entry URL drifted",
    )
    require(manual_ui_entry["backend_url"] == "http://127.0.0.1:8775", "manual UI backend URL drifted")
    require(manual_ui_entry["required_readback"] == "mirror API", "manual UI readback requirement drifted")
    require(manual_ui_entry["required_account_visible"] == "simulated-001", "manual UI account requirement drifted")
    task_text = json.dumps(vscode_tasks, sort_keys=True)
    for expected_task in manual_ui_entry["vscode_tasks"]:
        require(expected_task in task_text, f"missing VS Code task {expected_task}")
    require("8775" in task_text and "5175" in task_text, "VS Code tasks must include 8775 backend and 5175 UI")
    require(p011_browser["viewport_coverage"] == ["desktop", "tablet", "mobile"], "P011 viewport coverage drifted")
    require(len(p011_browser["browser_evidence"]) == 12, "P011 browser screenshot count drifted")
    for item in p011_browser["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty screenshot {item['screenshot']}")
    require("/accounts/acct.demo-19053" in p011_browser["routes_opened"], "P011 evidence missing legacy acct.demo-19053 route")
    require("/accounts/simulated-001" in p011_browser["routes_opened"], "P011 evidence missing simulated-001 route")

    require("S5 开户：fixture-only blocker is explicit" in p079_acceptance, "P079 fixture-only blocker scenario missing")
    require(p079_handoff["status"] == "ready_for_next_session", "P079 handoff status drifted")
    require(p079_handoff["account_opening"]["account_id"] == "simulated-001", "P079 account id drifted")
    require(p079_handoff["market_boundary"]["market_data_role"] == "market_data_only", "P079 market role drifted")
    require(p079_handoff["execution_boundary"]["broker_order_submission"] is False, "P079 broker submission drifted")
    require(p079_handoff["execution_boundary"]["trading_adapter"] == "disabled", "P079 trading adapter drifted")
    require(
        p079_handoff["browser_evidence"]["viewport_coverage"] == ["desktop", "tablet", "mobile"],
        "P079 browser evidence coverage drifted",
    )

    require(ctp025292_blocker["blocker_id"] == "ctp025292_source_unavailable", "025292 blocker id drifted")
    require(ctp025292_blocker["verdict"] == "blocked", "025292 blocker verdict drifted")
    require(
        ctp025292_blocker.get("template_ref")
        == "contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json",
        "025292 blocker template ref drifted",
    )
    require("pinned read-only CTP 025292 source package" in ctp025292_blocker["next_action"], "025292 next action drifted")
    require(ctp025292_real_login_ui_evidence["verdict"] == "blocked", "CTP 025292 real-login UI evidence must be blocked")
    require(
        ctp025292_real_login_ui_evidence["status"] == "blocked_waiting_for_real_login_source_package",
        "CTP 025292 real-login UI status drifted",
    )
    require(
        ctp025292_real_login_ui_evidence["source_ref"]
        == "output/account_capability/ctp-live-025292/source-package.json",
        "CTP 025292 real-login source ref drifted",
    )
    require(
        ctp025292_real_login_blocker["blocker_id"] == "ctp025292_real_login_td_bridge_unavailable",
        "CTP 025292 real-login blocker drifted",
    )

    require(command_gate["status"] == "design_gate_only", "command gate status drifted")
    command_gate_text = json.dumps(command_gate, sort_keys=True).lower()
    for forbidden in ["submit_order_implemented", "cancel_order_implemented", "replace_order_implemented"]:
        require(forbidden not in command_gate_text, f"command gate contains forbidden implementation claim {forbidden}")

    client = TestClient(app)
    accounts_response = client.get("/api/mirror/accounts")
    require(accounts_response.status_code == 200, "mirror account list failed")
    account_ids = {row["account_id"] for row in accounts_response.json()["accounts"]}
    require(
        account_ids
        == {
            "acct.nautilus.paper.demo",
            "acct.ctp.paper.19053",
            "acct.ctp.live.025292",
            "simulated-001",
        },
        f"mirror account list drifted: {sorted(account_ids)}",
    )
    for account_id in account_ids:
        detail = client.get(f"/api/mirror/accounts/{account_id}")
        require(detail.status_code == 200, f"account detail failed for {account_id}")
        payload = detail.json()
        require(payload["capabilities"]["command"]["enabled"] is False, f"command enabled for {account_id}")
        require(payload["boundaries"]["order_action"] is False, f"order action boundary true for {account_id}")

    blocked = client.get("/api/mirror/accounts/acct.ctp.live.025292").json()
    require(blocked["source_health"]["state"] == "blocked", "025292 source health must remain blocked")
    require(blocked["positions"] == [], "025292 blocked projection must not invent positions")
    require(blocked["orders"] == [], "025292 blocked projection must not invent orders")

    simulated = client.get("/api/mirror/accounts/simulated-001").json()
    health = simulated["source_health"]
    require(health["account_uid"] == "sandbox-paper.simulated-001", "simulated-001 uid drifted")
    require(health["market_data_account_id"] == "025292", "simulated-001 market data id drifted")
    require(health["market_data_role"] == "market_data_only", "simulated-001 market role drifted")
    require(health["execution_target"] == "Nautilus Sandbox Paper", "simulated-001 execution target drifted")
    require(health["orders_scope"] == "simulated ledger only", "simulated-001 orders scope drifted")
    require(health["broker_order_submission"] is False, "simulated-001 broker submission drifted")

    require(
        "UI declares Paper ready, Live ready, production ready, capital allocated, broker tradable or can trade."
        in p079_acceptance,
        "P079 negative readiness acceptance drifted",
    )
    for forbidden_claim in [
        "live_ready",
        "paper_ready",
        "production_ready",
        "capital_allocated",
        "broker_tradable",
        "can_trade",
    ]:
        require(forbidden_claim in p079_handoff["forbidden_claims"], f"P079 handoff missing forbidden claim {forbidden_claim}")
    combined_json = "\n".join(
        [
            json.dumps(p011_browser, sort_keys=True),
            json.dumps(p079_handoff, sort_keys=True),
            json.dumps(command_gate, sort_keys=True),
        ]
    ).lower()
    require('"command": {"enabled": true' not in combined_json, "command enabled machine claim present")

    print(
        "ADR004_P011_LANDING_CONSISTENCY_OK: accounts=4 routes=4 screenshots=12 "
        "blockers=ctp19053_source_unavailable,ctp025292_source_unavailable"
    )


if __name__ == "__main__":
    main()
