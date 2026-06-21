from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = (
    ROOT
    / "docs"
    / "acceptance"
    / "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json"
)
SPEC = ROOT / "frontend" / "tests" / "e2e" / "p019-ib-tws-synthetic-ready-projection.spec.ts"
MANIFEST = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "evidence-lane-manifest.json"
)
P019_ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"


class SyntheticReadyUiError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SyntheticReadyUiError(message)


def main() -> None:
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    acceptance = P019_ACCEPTANCE.read_text(encoding="utf-8")

    require(
        payload["schema"] == "account-console.p019-u3028269-synthetic-ready-ui-contract-evidence.v1",
        "schema mismatch",
    )
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "display alias mismatch")
    require(payload["route"] == "/accounts/acct.ib.live.u3028269", "route mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(payload["verdict"] == "synthetic_contract_only", "verdict must stay synthetic-only")
    require(payload["source_ref"].endswith(".synthetic.json"), "source ref must be synthetic")
    require(payload["source_checksum"].startswith("sha256:"), "source checksum missing")
    require(payload["projection_checksum"].startswith("sha256:"), "projection checksum missing")

    observed = payload["observed_contract_values"]
    require(observed["currency"] == "USD", "currency projection mismatch")
    require(observed["position_instrument"] == "AAPL", "position projection mismatch")
    require(observed["execution_report_types"] == ["OrderStatusReport", "FillReport"], "report type projection mismatch")
    require(observed["execution_report_sequences"] == [1, 2], "report sequence projection mismatch")
    require(
        observed["execution_report_source_refs"]
        == [
            "observation-ref://ib-tws/u3028269/reports/000001",
            "observation-ref://ib-tws/u3028269/reports/000002",
        ],
        "report source refs mismatch",
    )
    require(
        observed["store_reload_ref"] == "contracts/broker_observation/fixtures/ib_tws_store_complete_reload.json",
        "store reload ref mismatch",
    )
    require(
        observed["report_batch_ref"] == "contracts/broker_observation/fixtures/ib_tws_report_batch_sample.json",
        "report batch ref mismatch",
    )
    require(
        observed["reload_checkpoint_id"] == "broker-observation-store.reload.u3028269.complete.001",
        "reload checkpoint mismatch",
    )
    require(observed["records_reloaded_from_store"] == 2, "store reload count mismatch")
    require(observed["records_loaded_from_live_memory"] == 0, "live memory reload must stay zero")
    require(observed["reload_parity_status"] == "passed", "reload parity status mismatch")
    require(observed["command_enabled"] is False, "command must stay disabled")
    require(observed["mirror_state"] == "ready", "synthetic mirror state mismatch")

    for testid in [
        "tws-multi-currency-funds-table",
        "tws-base-currency-rollup",
        "account-positions-table",
        "account-position-projection-row",
        "tws-execution-reports-table",
        "tws-execution-report-row",
        "tws-execution-report-reload-ref",
        "account-command-capability-state",
        "account-evidence-rail",
    ]:
        require(testid in payload["ui_surfaces"].values(), f"evidence missing testid {testid}")
        require(testid in spec, f"Playwright spec missing testid {testid}")

    for non_claim in [
        "does_not_prove_real_u3028269_funds",
        "does_not_prove_real_u3028269_positions",
        "does_not_prove_real_u3028269_order_or_fill_callbacks",
        "does_not_close_real_ui_parity",
        "does_not_accept_adr0005",
        "does_not_satisfy_p018_owner_source_package_acceptance",
        "does_not_open_direct_tws_session",
        "does_not_enable_command_capability",
        "does_not_record_raw_secret_values",
    ]:
        require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")

    for required_step in [
        "local_tws_api_readiness_probe_pass",
        "readonly_tws_api_account_summary_success",
        "readonly_tws_api_positions_success",
        "source_package_built_from_real_query_artifacts",
        "account_mirror_projection_from_real_source_package",
        "ui_parity_against_same_slice_tws_api_source",
    ]:
        require(required_step in payload["required_real_closeout_chain"], f"missing real closeout step {required_step}")
        require(required_step in manifest, f"manifest missing real closeout step {required_step}")

    boundaries = payload["boundaries"]
    require(boundaries["synthetic_contract_only"] is True, "synthetic boundary missing")
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshot must not be funds/positions truth")
    require(boundaries["execution_reports_synthetic_contract_only"] is True, "report synthetic boundary missing")
    require(boundaries["durable_store_synthetic_contract_only"] is True, "store synthetic boundary missing")
    require(boundaries["broker_truth"] is False, "synthetic UI cannot be broker truth")
    require(boundaries["order_action"] is False, "synthetic UI cannot authorize order action")

    require(payload["browser_evidence"], "browser evidence missing")
    for item in payload["browser_evidence"]:
        screenshot = ROOT / item["screenshot"]
        require(screenshot.exists(), f"missing screenshot {item['screenshot']}")
        require(screenshot.stat().st_size > 0, f"empty screenshot {item['screenshot']}")

    forbidden_terms = [
        "placeOrder",
        "cancelOrder",
        "password=",
        "auth_code=",
        "front=tcp://",
        "api_key=",
        "raw_tws_endpoint",
    ]
    for term in forbidden_terms:
        require(term not in EVIDENCE.read_text(encoding="utf-8"), f"synthetic ready evidence must not contain {term}")
    for spec_term in ["password=", "auth_code=", "front=tcp", "api_key=", "secret="]:
        require(spec_term in spec, f"Playwright spec must keep negative assertion for {spec_term}")

    for term in [
        "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json",
        "validate_p019_u3028269_synthetic_ready_ui_contract.py",
        "P019_U3028269_SYNTHETIC_READY_UI_CONTRACT_OK",
    ]:
        require(term in acceptance, f"P019 acceptance missing {term}")

    print("P019_U3028269_SYNTHETIC_READY_UI_CONTRACT_OK: verdict=synthetic_contract_only surfaces=9 reports=2 reload=passed")


if __name__ == "__main__":
    main()
