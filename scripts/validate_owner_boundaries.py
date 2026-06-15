from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_MAP = ROOT / "docs" / "ownership" / "account-console-owner-map.md"
ROUTE_COVERAGE_MATRIX = ROOT / "docs" / "acceptance" / "2026-06-13-account-console-ui-route-coverage-matrix.md"
P001_README = ROOT / "docs" / "proposals" / "p001-daily-closeout-account-health-panel" / "README.md"
FRONTEND_TESTS_README = ROOT / "frontend" / "tests" / "README.md"
FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "daily_closeout"
P077_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "p077_paper_slice_panel.contract.json"
P077_FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "p077_paper_slice"
FRONTEND_SRC_DIR = ROOT / "frontend" / "src"
FRONTEND_E2E_DIR = ROOT / "frontend" / "tests" / "e2e"
P009_PROPOSAL_DIR = ROOT / "docs" / "proposals" / "p009-p077-paper-slice-evidence-panel"
ACCOUNT_SUMMARY_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_summary_panel.contract.json"
ACCOUNT_ORDERS_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_orders_panel.contract.json"
ACCOUNT_ORDER_DETAIL_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_order_detail_panel.contract.json"
ACCOUNT_POSITIONS_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_positions_panel.contract.json"
ACCOUNT_SETTLEMENT_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_settlement_panel.contract.json"
ACCOUNT_EQUITY_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_equity_panel.contract.json"
ACCOUNT_RECONCILE_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_reconcile_panel.contract.json"
ACCOUNT_INCIDENTS_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_incidents_panel.contract.json"
ACCOUNT_EVIDENCE_CONTRACT = ROOT / "contracts" / "ui" / "panels" / "account_evidence_panel.contract.json"
ACCOUNT_WORKBENCH_FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_workbench"
P077_UI_ROUTE_BLOCKER = ROOT / "docs" / "acceptance" / "2026-06-14-p077-e90-ui-route-acceptance-blocker.json"
P077_P009_DESIGN_GATE = ROOT / "docs" / "acceptance" / "2026-06-14-p077-p009-ui-slice-design-gate.json"
P077_P009_IMPLEMENTATION_EVIDENCE = (
    ROOT / "docs" / "acceptance" / "2026-06-14-p077-p009-ui-implementation-browser-evidence.json"
)
P077_P009_ROUTE_MATRIX_CLOSEOUT = (
    ROOT / "docs" / "acceptance" / "2026-06-14-p077-p009-route-matrix-governance-closeout.json"
)


REQUIRED_OWNER_MAP_TERMS = [
    "ASI-01 Canonical owner declared",
    "ASI-02 No alternate truth writer",
    "ASI-03 Rust hot path remains canonical",
    "ASI-04 Contract-first UI",
    "ASI-05 External owner blockers stay blockers",
    "account-console-browser-acceptance-tests",
    "P001 Owner Assignment",
    "Owner Boundary:",
]


def assert_contains(path: Path, terms: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    missing = [term for term in terms if term not in content]
    if missing:
        raise AssertionError(f"{path} missing terms: {missing}")


def assert_not_contains(path: Path, terms: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    present = [term for term in terms if term in content]
    if present:
        raise AssertionError(f"{path} contains forbidden owner-fork terms: {present}")


def validate_fixture_owner_boundary(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_health_panel.v1", path
    assert payload["route"] == "/closeout", path
    assert payload["context"]["source_ref"], path
    assert payload["context"]["checksum"].startswith("sha256:"), path
    for row in payload["accounts"]:
        assert row["source_ref"], (path, row["account_id"])
        assert row["checksum"].startswith("sha256:"), (path, row["account_id"])
        assert row["owner"], (path, row["account_id"])


def validate_p077_paper_slice_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "p077_paper_slice_panel.v1", path
    assert payload["route"] == "/orders/p077-paper-slice", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["context"]["producer_owner"], path
    assert payload["context"]["source_ref"], path
    assert payload["context"]["checksum"].startswith("sha256:"), path
    assert payload["context"]["rejection_rules"], path
    assert payload["slice"]["authorization_consumed"] is True, path
    assert payload["slice"]["active_authorization"] is False, path
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    for evidence in payload["evidence"]:
        assert evidence["source_ref"], (path, evidence["kind"])
        assert evidence["checksum"].startswith("sha256:"), (path, evidence["kind"])
        assert evidence["owner"], (path, evidence["kind"])
        assert evidence["authority"], (path, evidence["kind"])


def validate_account_summary_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_summary_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Summary Panel", path
    assert payload["route"] == "/accounts/{account_id}", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["context"]["source_authority"] in {
        "deterministic_fixture",
        "normalized_read_model",
        "typed_blocker",
    }, path
    assert payload["account"]["account_id"], path
    assert payload["account"]["account_alias"], path
    assert payload["source_refs"], path
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "action_controls",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    assert payload["boundaries"]["read_only_projection"] is True, path
    for source in payload["source_refs"]:
        assert source["source_ref"], (path, source["kind"])
        assert source["checksum"].startswith("sha256:"), (path, source["kind"])
        assert source["authority"], (path, source["kind"])
    for position in payload["positions"]:
        assert position["source_ref"], (path, position["instrument"])
        assert position["checksum"].startswith("sha256:"), (path, position["instrument"])
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path
    state = payload["fixture_state"]
    if state in {"blocked", "partial"}:
        assert payload["blockers"], path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path


def validate_order_boundaries(payload: dict, path: Path) -> None:
    assert payload["boundaries"]["read_only_projection"] is True, path
    for key in [
        "runtime_truth",
        "account_truth",
        "order_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "action_controls",
    ]:
        assert payload["boundaries"][key] is False, (path, key)


def validate_order_row(row: dict, path: Path) -> None:
    assert row["account_id"], path
    assert row["client_order_id"], path
    assert row["instrument"], path
    assert row["source_ref"], path
    assert row["checksum"].startswith("sha256:"), path
    if row["status"] == "filled":
        assert row["lifecycle_ref"], path
        assert row["report_provenance_ref"], path
        assert row["filled_quantity"] == row["quantity"], path


def validate_account_orders_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_orders_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Orders Panel", path
    assert payload["route"] == "/accounts/{account_id}/orders", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "current_orders":
        assert payload["orders"], path
    if state == "empty":
        assert not payload["orders"], path
    if state in {"blocked", "stale"}:
        assert payload["blockers"], path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
    for order in payload["orders"]:
        validate_order_row(order, path)
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path


def validate_account_order_detail_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_order_detail_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Order Detail Panel", path
    assert payload["route"] == "/accounts/{account_id}/orders/{client_order_id}", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    validate_order_row(payload["order"], path)
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "filled_lifecycle":
        assert len(payload["events"]) >= 2, path
        assert payload["report_provenance"], path
        assert [event["event_seq"] for event in payload["events"]] == [0, 1], path
    if state == "blocked":
        assert not payload["events"], path
        assert payload["blockers"], path
    for event in payload["events"]:
        assert event["event_id"], path
        assert event["source_ref"], path
        assert event["checksum"].startswith("sha256:"), path
        assert event["authority"], path


def validate_position_row(row: dict, path: Path) -> None:
    assert row["account_id"], path
    assert row["instrument"], path
    assert row["direction"] in {"LONG", "SHORT", "NET", "UNKNOWN"}, path
    assert row["source_ref"], path
    assert row["checksum"].startswith("sha256:"), path


def validate_account_positions_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_positions_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Positions Panel", path
    assert payload["route"] == "/accounts/{account_id}/positions", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["account"]["account_id"], path
    assert payload["account"]["account_alias"], path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "current_positions":
        assert payload["positions"], path
        for position in payload["positions"]:
            assert position["carryover_ref"], path
            assert position["settlement_ref"], path
    if state == "empty":
        assert not payload["positions"], path
        assert not payload["blockers"], path
    if state == "blocked":
        assert payload["blockers"], path
        assert any(position["carryover_ref"] is None for position in payload["positions"]), path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert any(position["settlement_ref"] is None for position in payload["positions"]), path
    for position in payload["positions"]:
        validate_position_row(position, path)
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_account_settlement_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_settlement_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Settlement Panel", path
    assert payload["route"] == "/accounts/{account_id}/settlement", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    settlement = payload["settlement"]
    assert settlement["source_ref"], path
    assert settlement["checksum"].startswith("sha256:"), path
    state = payload["fixture_state"]
    if state == "current_settlement":
        assert settlement["current_settlement_ref"], path
        assert settlement["position_carryover_ref"], path
    if state == "empty":
        assert settlement["settlement_state"] == "missing", path
        assert not payload["blockers"], path
    if state == "blocked":
        assert payload["blockers"], path
        assert settlement["current_settlement_ref"] is None, path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert settlement["position_carryover_ref"] is None, path
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_account_equity_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_equity_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Equity Panel", path
    assert payload["route"] == "/accounts/{account_id}/equity", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "current_equity":
        assert payload["equity_points"], path
        for point in payload["equity_points"]:
            assert point["ledger_ref"], path
            assert point["curve_ref"], path
    if state == "empty":
        assert not payload["equity_points"], path
        assert not payload["blockers"], path
    if state == "blocked":
        assert payload["blockers"], path
        assert any(point["ledger_ref"] is None for point in payload["equity_points"]), path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert any(point["curve_ref"] is None for point in payload["equity_points"]), path
    for point in payload["equity_points"]:
        assert point["source_ref"], path
        assert point["checksum"].startswith("sha256:"), path
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_account_reconcile_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_reconcile_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Reconcile Panel", path
    assert payload["route"] == "/accounts/{account_id}/reconcile", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "matched":
        assert payload["reconcile_items"], path
        assert all(item["status"] == "matched" for item in payload["reconcile_items"]), path
    if state == "empty":
        assert not payload["reconcile_items"], path
        assert not payload["blockers"], path
    if state == "mismatch":
        assert payload["blockers"], path
        assert any(item["status"] == "mismatch" and item["mismatch_ref"] for item in payload["reconcile_items"]), path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert any(item["tolerance_ref"] is None for item in payload["reconcile_items"]), path
    for item in payload["reconcile_items"]:
        assert item["item_id"], path
        assert item["owner"], path
        assert item["next_action"], path
        assert item["source_ref"], path
        assert item["checksum"].startswith("sha256:"), path
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_account_incidents_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_incidents_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Incidents Panel", path
    assert payload["route"] == "/accounts/{account_id}/incidents", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "active_incidents":
        assert payload["incidents"], path
    if state == "empty":
        assert not payload["incidents"], path
        assert not payload["blockers"], path
    if state == "blocked":
        assert payload["blockers"], path
        assert any(incident["repair_ref"] is None for incident in payload["incidents"]), path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert any(incident["repair_ref"] is None for incident in payload["incidents"]), path
    for incident in payload["incidents"]:
        assert incident["incident_id"], path
        assert incident["owner"], path
        assert incident["next_action"], path
        assert incident["source_ref"], path
        assert incident["checksum"].startswith("sha256:"), path
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_account_evidence_fixture(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "account_evidence_panel.v1", path
    assert payload["workbench"] == "Account Workbench", path
    assert payload["panel"] == "Account Evidence Panel", path
    assert payload["route"] == "/accounts/{account_id}/evidence", path
    assert payload["context"]["projection_owner"] == "account-console-contracts", path
    assert payload["source_refs"], path
    validate_order_boundaries(payload, path)
    state = payload["fixture_state"]
    if state == "current_evidence":
        assert payload["evidence_packages"], path
        assert all(package["status"] == "current" for package in payload["evidence_packages"]), path
    if state == "empty":
        assert not payload["evidence_packages"], path
        assert not payload["blockers"], path
    if state == "blocked":
        assert payload["blockers"], path
        assert any(package["schema_ref"] == "missing" for package in payload["evidence_packages"]), path
    if state == "stale":
        assert payload["context"]["stream_state"] == "stale", path
        assert payload["blockers"], path
    if state == "partial":
        assert payload["blockers"], path
        assert any(package["raw_payload_ref"] is None for package in payload["evidence_packages"]), path
    for package in payload["evidence_packages"]:
        assert package["package_id"], path
        assert package["owner"], path
        assert package["schema_ref"], path
        assert package["schema_version_ref"], path
        assert package["source_ref"], path
        assert package["next_action"], path
        assert package["checksum"].startswith("sha256:"), path
        if package["raw_payload_ref"]:
            assert package["normalized_ref"], path
    for source in payload["source_refs"]:
        assert source["source_ref"], path
        assert source["checksum"].startswith("sha256:"), path
        assert source["authority"], path
    for blocker in payload["blockers"]:
        assert blocker["blocker_id"], path
        assert blocker["owner"], path
        assert blocker["next_action"], path
        assert blocker["source_ref"], path
        assert blocker["checksum"].startswith("sha256:"), path


def validate_p077_account_evidence_owner_unified() -> None:
    forbidden_current_code_terms = [
        "isP077WorkbenchRoute",
        "P077PaperSlicePanel(",
        'data-testid="p077-paper-slice-panel"',
        'data-testid={`p077-paper-slice-panel`',
        "/accounts/19053/evidence",
        "/accounts/19053/orders",
    ]
    current_code_paths = [FRONTEND_SRC_DIR / "App.tsx"]
    current_code_paths.extend(sorted(FRONTEND_E2E_DIR.glob("*.ts")))
    for path in current_code_paths:
        assert_not_contains(path, forbidden_current_code_terms)

    assert_contains(
        P009_PROPOSAL_DIR / "acceptance.md",
        [
            "P009-NEG-01A",
            "P077-specific route branch",
            "Account Evidence Panel",
        ],
    )
    assert_contains(
        P009_PROPOSAL_DIR / "ui-acceptance.md",
        [
            "P009-UI-NEG-02A",
            "account-evidence-panel",
            "account-evidence-package-row",
        ],
    )

    evidence_fixture = ACCOUNT_WORKBENCH_FIXTURE_DIR / "account_evidence_current.json"
    payload = json.loads(evidence_fixture.read_text(encoding="utf-8"))
    packages = {package["package_id"]: package for package in payload["evidence_packages"]}
    p077_package = packages.get("evidence.p077.close-yesterday.e100-e102")
    assert p077_package is not None, evidence_fixture
    assert p077_package["owner"] == "nautilus_ctp_adapter", evidence_fixture
    assert p077_package["schema_ref"] == "contracts/ui/panels/p077_paper_slice_panel.contract.json", evidence_fixture
    assert p077_package["schema_version_ref"] == "p077_paper_slice_panel.v1", evidence_fixture
    assert p077_package["raw_payload_ref"] is None, evidence_fixture
    assert p077_package["normalized_ref"], evidence_fixture
    assert p077_package["checksum"].startswith("sha256:"), evidence_fixture
    source_kinds = {source["kind"]: source for source in payload["source_refs"]}
    p077_source = source_kinds.get("p077_owner_slice_projection")
    assert p077_source is not None, evidence_fixture
    assert p077_source["owner"] == "account-console-contracts", evidence_fixture
    assert "not runtime, order, account, ledger, readiness or retry authority" in p077_source["authority"], evidence_fixture
    assert any(
        "Reject P077 evidence package display as Paper readiness" in rule
        for rule in payload["rejection_rules"]
    ), evidence_fixture


def validate_p077_ui_route_blocker(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "account-console.p077-e90-ui-route-acceptance-blocker.v1", path
    assert payload["action_mode"] == "typed_blocker_no_ui_no_runtime_truth", path
    assert payload["blocker"]["blocker_id"] == "account-console.p077.e90.ui-route-acceptance-missing", path
    assert payload["route_review"]["ui_code_changed"] is False, path
    assert payload["route_review"]["browser_evidence_created"] is False, path
    assert payload["route_review"]["proposal_level_ui_design_present"] is False, path
    assert payload["route_review"]["proposal_level_ui_acceptance_present"] is False, path
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "paper_send_authorized",
        "paper_send_attempted",
        "native_send_attempted",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    assert payload["rejection_rules"], path


def validate_p077_p009_design_gate(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "account-console.p077-p009-ui-slice-design-gate.v1", path
    assert payload["action_mode"] == "design_gate_only_no_ui_no_runtime_truth", path
    assert payload["proposal"]["status"] == "design_gate_ready", path
    assert payload["route_mapping"]["top_level_route_allowed"] is False, path
    status = payload["e91_retry_condition_status"]
    assert status["proposal_level_ui_design_present"] is True, path
    assert status["proposal_level_ui_acceptance_present"] is True, path
    assert status["route_matrix_mapping_present"] is True, path
    assert status["browser_render_evidence_present"] is False, path
    assert status["frontend_implementation_started"] is False, path
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "paper_send_authorized",
        "paper_send_attempted",
        "native_send_attempted",
        "frontend_code_changed",
        "browser_evidence_claimed",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    assert payload["rejection_rules"], path


def validate_p077_p009_implementation_evidence(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "account-console.p077-p009-ui-implementation-browser-evidence.v1", path
    assert payload["action_mode"] == "read_only_ui_implementation_no_runtime_truth", path
    assert payload["proposal"]["proposal_id"] == "p009-p077-paper-slice-evidence-panel", path
    assert payload["proposal"]["status"] == "implementation_browser_evidence", path
    route = payload["route_mapping"]
    assert route["implemented_route"] == "/accounts/19053/evidence", path
    assert route["top_level_route_added"] is False, path
    assert route["primary_navigation_entry_added"] is False, path
    browser = payload["browser_evidence"]
    assert browser["status"] == "passed", path
    assert browser["viewports"] == ["desktop", "tablet", "mobile"], path
    assert len(browser["screenshots"]) == 3, path
    for screenshot in browser["screenshots"]:
        assert screenshot["path"], path
        assert screenshot["checksum"].startswith("sha256:"), path
    gates = {gate["name"]: gate["status"] for gate in payload["gates"]}
    for required in [
        "frontend fixture validation",
        "frontend build",
        "frontend e2e",
        "proposal docs",
        "owner boundary",
        "owner-side blocker adoption",
        "backend compileall",
        "hotpath rust tests",
    ]:
        assert gates.get(required) == "passed", (path, required)
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "paper_send_authorized",
        "paper_send_attempted",
        "native_send_attempted",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    assert payload["boundaries"]["frontend_code_changed"] is True, path
    assert payload["boundaries"]["browser_evidence_claimed"] is True, path
    assert payload["rejection_rules"], path


def validate_p077_p009_route_matrix_closeout(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "account-console.p077-p009-route-matrix-governance-closeout.v1", path
    assert payload["action_mode"] == "governance_route_matrix_closeout_no_runtime_truth", path
    assert payload["proposal"]["proposal_id"] == "p009-p077-paper-slice-evidence-panel", path
    assert payload["proposal"]["status"] == "governance_closeout", path
    assert payload["source_evidence"]["implementation_evidence_checksum"].startswith("sha256:"), path
    assert payload["route_mapping"]["route_matrix_status"] == "e93_browser_evidence_recorded", path
    assert payload["route_mapping"]["top_level_route_added"] is False, path
    assert payload["route_mapping"]["broader_account_workbench_accepted"] is False, path
    for key in [
        "runtime_truth",
        "ledger_truth",
        "ui_truth",
        "paper_ready",
        "live_ready",
        "broker_tradable",
        "admission_truth",
        "capital_truth",
        "paper_send_authorized",
        "paper_send_attempted",
        "native_send_attempted",
    ]:
        assert payload["boundaries"][key] is False, (path, key)
    assert payload["boundaries"]["governance_docs_changed"] is True, path
    assert payload["rejection_rules"], path


def main() -> None:
    assert OWNER_MAP.exists(), OWNER_MAP
    assert_contains(OWNER_MAP, REQUIRED_OWNER_MAP_TERMS)
    assert_contains(
        OWNER_MAP,
        ["P009 E93 implementation/browser evidence", "must not add a top-level `/orders/p077-paper-slice` route"],
    )
    assert_contains(
        FRONTEND_TESTS_README,
        [
            "account-console-browser-acceptance-tests",
            "No production code imports from `frontend/tests`",
            "Screenshots, traces, and Playwright state prove display behavior only",
        ],
    )
    assert_contains(
        ROUTE_COVERAGE_MATRIX,
        [
            "P009 E93 implementation/browser evidence exists for the P077 read-only panel only",
            "P001 and the P009 P077 slice now have completed proposal-level browser coverage",
        ],
    )
    assert_contains(P001_README, ["Owner Boundary", "account-console-contracts", "account-console-frontend"])
    for fixture in sorted(FIXTURE_DIR.glob("account_health_*.json")):
        validate_fixture_owner_boundary(fixture)
    assert ACCOUNT_SUMMARY_CONTRACT.exists(), ACCOUNT_SUMMARY_CONTRACT
    assert_contains(ACCOUNT_SUMMARY_CONTRACT, ["account_summary_panel.v1", "action_controls", "rejection_rules"])
    required_account_summary_fixtures = {
        "account_summary_happy_path.json",
        "account_summary_empty.json",
        "account_summary_blocked.json",
        "account_summary_stale_stream.json",
        "account_summary_partial_evidence.json",
    }
    actual_account_summary_fixtures = {path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_summary_*.json")}
    missing_account_summary = required_account_summary_fixtures - actual_account_summary_fixtures
    if missing_account_summary:
        raise AssertionError(f"missing account summary fixtures: {sorted(missing_account_summary)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_summary_*.json")):
        validate_account_summary_fixture(fixture)
    assert ACCOUNT_ORDERS_CONTRACT.exists(), ACCOUNT_ORDERS_CONTRACT
    assert_contains(ACCOUNT_ORDERS_CONTRACT, ["account_orders_panel.v1", "order_truth", "action_controls"])
    assert ACCOUNT_ORDER_DETAIL_CONTRACT.exists(), ACCOUNT_ORDER_DETAIL_CONTRACT
    assert_contains(ACCOUNT_ORDER_DETAIL_CONTRACT, ["account_order_detail_panel.v1", "lifecycle_event"])
    assert ACCOUNT_POSITIONS_CONTRACT.exists(), ACCOUNT_POSITIONS_CONTRACT
    assert_contains(
        ACCOUNT_POSITIONS_CONTRACT,
        ["account_positions_panel.v1", "carryover_ref", "settlement_ref", "action_controls"],
    )
    assert ACCOUNT_SETTLEMENT_CONTRACT.exists(), ACCOUNT_SETTLEMENT_CONTRACT
    assert_contains(
        ACCOUNT_SETTLEMENT_CONTRACT,
        ["account_settlement_panel.v1", "previous_settlement_ref", "current_settlement_ref", "position_carryover_ref", "action_controls"],
    )
    assert ACCOUNT_EQUITY_CONTRACT.exists(), ACCOUNT_EQUITY_CONTRACT
    assert_contains(
        ACCOUNT_EQUITY_CONTRACT,
        ["account_equity_panel.v1", "ledger_ref", "curve_ref", "action_controls"],
    )
    assert ACCOUNT_RECONCILE_CONTRACT.exists(), ACCOUNT_RECONCILE_CONTRACT
    assert_contains(
        ACCOUNT_RECONCILE_CONTRACT,
        ["account_reconcile_panel.v1", "mismatch_ref", "tolerance_ref", "next_action", "action_controls"],
    )
    assert ACCOUNT_INCIDENTS_CONTRACT.exists(), ACCOUNT_INCIDENTS_CONTRACT
    assert_contains(
        ACCOUNT_INCIDENTS_CONTRACT,
        ["account_incidents_panel.v1", "repair_ref", "next_action", "action_controls"],
    )
    assert ACCOUNT_EVIDENCE_CONTRACT.exists(), ACCOUNT_EVIDENCE_CONTRACT
    assert_contains(
        ACCOUNT_EVIDENCE_CONTRACT,
        ["account_evidence_panel.v1", "schema_ref", "checksum", "raw_payload_ref", "action_controls"],
    )
    required_account_order_fixtures = {
        "account_orders_current_e100.json",
        "account_orders_empty.json",
        "account_orders_blocked_missing_lifecycle.json",
        "account_orders_stale_stream.json",
        "account_order_detail_e100_filled_lifecycle.json",
        "account_order_detail_blocked_missing_events.json",
    }
    actual_account_order_fixtures = {
        path.name
        for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_order*.json")
    }
    missing_account_orders = required_account_order_fixtures - actual_account_order_fixtures
    if missing_account_orders:
        raise AssertionError(f"missing account order fixtures: {sorted(missing_account_orders)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_orders_*.json")):
        validate_account_orders_fixture(fixture)
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_order_detail_*.json")):
        validate_account_order_detail_fixture(fixture)
    required_account_positions_fixtures = {
        "account_positions_current_e100.json",
        "account_positions_empty.json",
        "account_positions_blocked_missing_carryover.json",
        "account_positions_stale_stream.json",
        "account_positions_partial_missing_settlement.json",
    }
    actual_account_positions_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_positions_*.json")
    }
    missing_account_positions = required_account_positions_fixtures - actual_account_positions_fixtures
    if missing_account_positions:
        raise AssertionError(f"missing account positions fixtures: {sorted(missing_account_positions)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_positions_*.json")):
        validate_account_positions_fixture(fixture)
    required_account_settlement_fixtures = {
        "account_settlement_current.json",
        "account_settlement_empty.json",
        "account_settlement_blocked_missing_current.json",
        "account_settlement_stale_stream.json",
        "account_settlement_partial_missing_carryover.json",
    }
    actual_account_settlement_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_settlement_*.json")
    }
    missing_account_settlement = required_account_settlement_fixtures - actual_account_settlement_fixtures
    if missing_account_settlement:
        raise AssertionError(f"missing account settlement fixtures: {sorted(missing_account_settlement)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_settlement_*.json")):
        validate_account_settlement_fixture(fixture)
    required_account_equity_fixtures = {
        "account_equity_current.json",
        "account_equity_empty.json",
        "account_equity_blocked_missing_ledger.json",
        "account_equity_stale_stream.json",
        "account_equity_partial_missing_curve.json",
    }
    actual_account_equity_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_equity_*.json")
    }
    missing_account_equity = required_account_equity_fixtures - actual_account_equity_fixtures
    if missing_account_equity:
        raise AssertionError(f"missing account equity fixtures: {sorted(missing_account_equity)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_equity_*.json")):
        validate_account_equity_fixture(fixture)
    required_account_reconcile_fixtures = {
        "account_reconcile_matched.json",
        "account_reconcile_empty.json",
        "account_reconcile_mismatch.json",
        "account_reconcile_stale_stream.json",
        "account_reconcile_partial_missing_tolerance.json",
    }
    actual_account_reconcile_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_reconcile_*.json")
    }
    missing_account_reconcile = required_account_reconcile_fixtures - actual_account_reconcile_fixtures
    if missing_account_reconcile:
        raise AssertionError(f"missing account reconcile fixtures: {sorted(missing_account_reconcile)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_reconcile_*.json")):
        validate_account_reconcile_fixture(fixture)
    required_account_incidents_fixtures = {
        "account_incidents_active.json",
        "account_incidents_empty.json",
        "account_incidents_blocked_source.json",
        "account_incidents_stale_stream.json",
        "account_incidents_partial_missing_repair.json",
    }
    actual_account_incidents_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_incidents_*.json")
    }
    missing_account_incidents = required_account_incidents_fixtures - actual_account_incidents_fixtures
    if missing_account_incidents:
        raise AssertionError(f"missing account incidents fixtures: {sorted(missing_account_incidents)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_incidents_*.json")):
        validate_account_incidents_fixture(fixture)
    required_account_evidence_fixtures = {
        "account_evidence_current.json",
        "account_evidence_empty.json",
        "account_evidence_blocked_missing_schema.json",
        "account_evidence_stale_stream.json",
        "account_evidence_partial_missing_raw_payload.json",
    }
    actual_account_evidence_fixtures = {
        path.name for path in ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_evidence_*.json")
    }
    missing_account_evidence = required_account_evidence_fixtures - actual_account_evidence_fixtures
    if missing_account_evidence:
        raise AssertionError(f"missing account evidence fixtures: {sorted(missing_account_evidence)}")
    for fixture in sorted(ACCOUNT_WORKBENCH_FIXTURE_DIR.glob("account_evidence_*.json")):
        validate_account_evidence_fixture(fixture)
    assert P077_CONTRACT.exists(), P077_CONTRACT
    assert_contains(P077_CONTRACT, ["p077_paper_slice_panel.v1", "rejection_rules"])
    for fixture in sorted(P077_FIXTURE_DIR.glob("*.json")):
        validate_p077_paper_slice_fixture(fixture)
    assert P077_UI_ROUTE_BLOCKER.exists(), P077_UI_ROUTE_BLOCKER
    validate_p077_ui_route_blocker(P077_UI_ROUTE_BLOCKER)
    assert P077_P009_DESIGN_GATE.exists(), P077_P009_DESIGN_GATE
    validate_p077_p009_design_gate(P077_P009_DESIGN_GATE)
    assert P077_P009_IMPLEMENTATION_EVIDENCE.exists(), P077_P009_IMPLEMENTATION_EVIDENCE
    validate_p077_p009_implementation_evidence(P077_P009_IMPLEMENTATION_EVIDENCE)
    assert P077_P009_ROUTE_MATRIX_CLOSEOUT.exists(), P077_P009_ROUTE_MATRIX_CLOSEOUT
    validate_p077_p009_route_matrix_closeout(P077_P009_ROUTE_MATRIX_CLOSEOUT)
    validate_p077_account_evidence_owner_unified()
    print("owner boundary validation passed")


if __name__ == "__main__":
    main()
