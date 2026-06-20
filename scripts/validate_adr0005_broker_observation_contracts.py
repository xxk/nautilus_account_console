from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "broker_observation"
FIXTURE_DIR = CONTRACT_DIR / "fixtures"
P019_AUDIT = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "pre-implementation-audit.md"
)
P019_UI_ACCEPTANCE = (
    ROOT
    / "docs"
    / "proposals"
    / "p019-broker-observation-session-foundation"
    / "tws-account-workbench-ui-acceptance.md"
)

CHECKSUM_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
ACCOUNT_ID_RE = re.compile(r"^acct\.[a-z0-9_.-]+$")
FORBIDDEN_COMMAND_ACTIONS = {"submit", "cancel", "replace", "modify", "placeOrder", "cancelOrder"}
FORBIDDEN_SECRET_FRAGMENTS = [
    "password=",
    "passwd=",
    "auth_code=",
    "front=tcp://",
    "host=",
    "port=",
    "client_id=",
    "api_key=",
    "secret=",
]


class ContractError(AssertionError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def require_checksum(value: str, field: str, path: Path) -> None:
    require(isinstance(value, str) and CHECKSUM_RE.match(value) is not None, f"{path}: invalid checksum {field}")


def walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk_values(item))
    return values


def assert_no_secret_material(payload: dict[str, Any], path: Path) -> None:
    require(payload.get("raw_secret_values_recorded") is False, f"{path}: raw_secret_values_recorded must be false")
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in FORBIDDEN_SECRET_FRAGMENTS if fragment in lowered]
            require(not hits, f"{path}: forbidden secret-like material {hits} in {value!r}")


def assert_command_disabled(command: dict[str, Any], path: Path) -> None:
    require(command["enabled"] is False, f"{path}: command.enabled must be false")
    require(command["allowed_actions"] == [], f"{path}: allowed_actions must be empty")
    action_hits = FORBIDDEN_COMMAND_ACTIONS.intersection(command.get("allowed_actions", []))
    require(not action_hits, f"{path}: forbidden command actions {sorted(action_hits)}")


def validate_docs_gates() -> None:
    audit = P019_AUDIT.read_text(encoding="utf-8")
    required_terms = [
        "AUD-01",
        "AUD-03",
        "PRE-G01",
        "PRE-G09",
        "adr0005_not_accepted",
        "P018 compatibility mode",
    ]
    missing = [term for term in required_terms if term not in audit]
    require(not missing, f"{P019_AUDIT}: missing audit gate terms {missing}")

    ui_acceptance = P019_UI_ACCEPTANCE.read_text(encoding="utf-8")
    for term in [
        "tws-multi-currency-funds-table",
        "tws-execution-reports-table",
        "execution_reports_persistence_parity",
    ]:
        require(term in ui_acceptance, f"{P019_UI_ACCEPTANCE}: missing UI acceptance term {term}")


def validate_schema_files() -> None:
    expected = {
        "broker_observation_profile.schema.json": "Broker Observation Profile",
        "session_conflict_policy.schema.json": "Broker Observation Session Conflict Policy",
        "nautilus_compatible_report_batch.schema.json": "Nautilus Compatible Broker Observation Report Batch",
        "report_mapping_matrix.schema.json": "Broker Observation Report Mapping Matrix",
        "freshness_sequence_checkpoint.schema.json": "Broker Observation Freshness Sequence Checkpoint",
        "durable_observation_store.schema.json": "Durable Broker Observation Store Snapshot",
        "cross_broker_extension_matrix.schema.json": "Broker Observation Cross Broker Extension Matrix",
    }
    for filename, title in expected.items():
        path = CONTRACT_DIR / filename
        payload = load_json(path)
        require(payload["title"] == title, f"{path}: title drifted")
        require("raw_secret_values_recorded" in payload["required"], f"{path}: must require raw_secret_values_recorded")


def validate_profile(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(payload["schema_version"] == "broker_observation_profile.v1", f"{path}: schema_version mismatch")
    require(ACCOUNT_ID_RE.match(payload["account_id"]) is not None, f"{path}: account_id must be canonical")
    require(payload["mode"] == "read_only_observation", f"{path}: mode must be read_only_observation")
    require(payload["projection_boundary"] == "account_mirror", f"{path}: projection_boundary must be Account Mirror")
    assert_command_disabled(payload["command"], path)

    adr_gate = payload["adr_gate"]
    require(adr_gate["adr_id"] == "ADR-0005", f"{path}: wrong ADR gate")
    if adr_gate["decision_status"] == "proposed":
        require(adr_gate["direct_session_allowed"] is False, f"{path}: proposed ADR cannot allow direct session")
        require(adr_gate["blocker_id"] == "adr0005_not_accepted", f"{path}: missing ADR blocker")

    conflict_policy = payload["conflict_policy"]
    require(conflict_policy["fail_closed"] is True, f"{path}: conflict policy must fail closed")
    require(conflict_policy["unknown_owner_policy"] == "blocked", f"{path}: unknown owner must block")
    for key in ["broker_username_ref", "client_id_ref", "nautilus_trading_session_ref"]:
        require(key in conflict_policy["conflict_keys"], f"{path}: missing conflict key {key}")


def validate_report_batch(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(payload["schema_version"] == "broker_observation_report_batch.v1", f"{path}: schema_version mismatch")
    require(ACCOUNT_ID_RE.match(payload["account_id"]) is not None, f"{path}: account_id must be canonical")
    assert_command_disabled(payload["command"], path)
    require(payload["reports"], f"{path}: report batch must contain normalized rows")

    seen_sequences: list[int] = []
    for idx, report in enumerate(payload["reports"]):
        field = f"reports[{idx}]"
        require(report["nautilus_report_type"] in {"OrderStatusReport", "FillReport"}, f"{path}: non-Nautilus report type")
        require(report["account_id"] == payload["account_id"], f"{path}: report account mismatch")
        require(report["report_id"], f"{path}: missing report_id")
        require(report["client_order_id"], f"{path}: missing client_order_id")
        require(report["venue_order_id"], f"{path}: missing venue_order_id")
        require(report["instrument_id"], f"{path}: missing instrument_id")
        require(report["event_timestamp"], f"{path}: missing event_timestamp")
        require(report["observed_timestamp"], f"{path}: missing observed_timestamp")
        require(report["received_timestamp"], f"{path}: missing received_timestamp")
        require(isinstance(report["sequence"], int), f"{path}: sequence must be integer")
        seen_sequences.append(report["sequence"])
        require_checksum(report["source_checksum"], f"{field}.source_checksum", path)
        require("raw_payload" not in report, f"{path}: raw_payload must not be canonical report truth")
        provenance = report["raw_payload_provenance"]
        require(provenance["payload_ref"], f"{path}: missing payload_ref")
        require_checksum(provenance["payload_checksum"], f"{field}.raw_payload_provenance.payload_checksum", path)
        require(provenance["excerpt_redacted"] is True, f"{path}: raw payload excerpt must be redacted")

        if report["nautilus_report_type"] == "OrderStatusReport":
            require(report["order_status"], f"{path}: OrderStatusReport missing order_status")
            require(report["quantity"] >= report["filled_quantity"], f"{path}: filled quantity exceeds quantity")
        if report["nautilus_report_type"] == "FillReport":
            require(report["trade_id"], f"{path}: FillReport missing trade_id")
            require(report["last_px"] is not None, f"{path}: FillReport missing last_px")
            require(report["last_qty"] is not None and report["last_qty"] > 0, f"{path}: FillReport missing last_qty")

    require(seen_sequences == sorted(seen_sequences), f"{path}: report sequence must be deterministic")


def validate_session_conflict_policy(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(
        payload["schema_version"] == "broker_observation_session_conflict_policy.v1",
        f"{path}: schema_version mismatch",
    )
    require(ACCOUNT_ID_RE.match(payload["account_id"]) is not None, f"{path}: account_id must be canonical")
    require(payload["fail_closed"] is True, f"{path}: conflict policy must fail closed")
    require(payload["unknown_owner_policy"] == "blocked", f"{path}: unknown owner must block")
    require(payload["direct_session_allowed"] is False, f"{path}: direct session must stay blocked")
    assert_command_disabled(payload["command"], path)

    conflict_keys = set(payload["conflict_keys"])
    for key in [
        "broker_username_ref",
        "host_port_ref",
        "client_id_ref",
        "session_owner",
        "nautilus_trading_session_ref",
        "broker_connection_slot_ref",
    ]:
        require(key in conflict_keys, f"{path}: missing conflict key {key}")

    required_cases = {
        "unknown_owner": "session_owner_unknown",
        "same_client_id_conflict": "broker_client_id_conflict",
        "active_nautilus_trading_session": "nautilus_trading_session_active",
        "broker_connection_slot_conflict": "broker_connection_slot_conflict",
    }
    evaluations = {case["case_id"]: case for case in payload["evaluations"]}
    for case_id, blocker_id in required_cases.items():
        require(case_id in evaluations, f"{path}: missing conflict case {case_id}")
        case = evaluations[case_id]
        require(case["decision"] == "blocked", f"{path}: {case_id} must be blocked")
        require(case["session_allowed"] is False, f"{path}: {case_id} must not allow session")
        require(case["blocker_id"] == blocker_id, f"{path}: {case_id} blocker mismatch")
        require(case["input_refs"], f"{path}: {case_id} missing input refs")
        require(case["next_action"], f"{path}: {case_id} missing next action")


def validate_store_snapshot(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(payload["schema_version"] == "broker_observation_store_snapshot.v1", f"{path}: schema_version mismatch")
    require(payload["store_semantics"] == "observation_evidence_projection_cache", f"{path}: wrong store semantics")
    for key, value in payload["truth_flags"].items():
        require(value is False, f"{path}: truth flag {key} must be false")
    for family in [
        "order_status_reports",
        "fill_reports",
        "funds_snapshots",
        "positions_snapshots",
        "session_health",
        "freshness_cursors",
    ]:
        require(family in payload["persisted_families"], f"{path}: missing persisted family {family}")
        require(family in payload["persisted_record_counts"], f"{path}: missing record count {family}")
        require(isinstance(payload["persisted_record_counts"][family], int), f"{path}: record count must be integer {family}")
    reload_proof = payload["reload_proof"]
    require(payload["reload_support"] is True, f"{path}: durable store must support reload")
    require_checksum(reload_proof["store_snapshot_checksum"], "reload_proof.store_snapshot_checksum", path)
    require_checksum(reload_proof["source_report_batch_checksum"], "reload_proof.source_report_batch_checksum", path)
    require(reload_proof["records_loaded_from_live_memory"] == 0, f"{path}: reload proof must not depend on live memory")
    persisted_reports = (
        payload["persisted_record_counts"]["order_status_reports"]
        + payload["persisted_record_counts"]["fill_reports"]
    )
    require(
        reload_proof["records_reloaded_from_store"] == persisted_reports,
        f"{path}: reloaded record count must match persisted report counts",
    )
    replay_state = payload["replay_state"]
    if replay_state["state"] in {"blocked", "partial"}:
        require(replay_state["blockers"], f"{path}: partial/blocked replay requires blockers")
        require(reload_proof["parity_status"] == "blocked", f"{path}: blocked replay must keep parity blocked")
    if replay_state["state"] == "complete":
        require(not replay_state["blockers"], f"{path}: complete replay must not carry blockers")
        require(reload_proof["parity_status"] == "passed", f"{path}: complete replay must pass parity")
        require(reload_proof["records_reloaded_from_store"] > 0, f"{path}: complete replay must reload records from store")
    for blocker in replay_state["blockers"]:
        require(blocker["blocker_id"], f"{path}: blocker missing id")
        require(blocker["next_action"], f"{path}: blocker missing next action")


def validate_freshness_sequence_checkpoint(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(
        payload["schema_version"] == "broker_observation_freshness_sequence_checkpoint.v1",
        f"{path}: schema_version mismatch",
    )
    require(ACCOUNT_ID_RE.match(payload["account_id"]) is not None, f"{path}: account_id must be canonical")
    assert_command_disabled(payload["command"], path)

    cursor = payload["cursor"]
    freshness = payload["freshness"]
    sequence_window = payload["sequence_window"]
    claim_guard = payload["claim_guard"]

    require(
        cursor["last_persisted_sequence"] <= cursor["last_observed_sequence"],
        f"{path}: persisted sequence cannot exceed observed sequence",
    )
    require(
        cursor["next_expected_sequence"] >= cursor["last_observed_sequence"],
        f"{path}: next expected sequence cannot precede observed sequence",
    )
    require(
        sequence_window["first_sequence"] <= sequence_window["last_sequence"],
        f"{path}: invalid sequence window",
    )
    require(
        sequence_window["record_count"] <= sequence_window["last_sequence"] - sequence_window["first_sequence"] + 1,
        f"{path}: record count exceeds sequence window",
    )
    require(freshness["max_observation_lag_ms"] >= 0, f"{path}: observation lag must be non-negative")
    require(freshness["max_persist_lag_ms"] >= 0, f"{path}: persist lag must be non-negative")
    require(claim_guard["may_claim_realtime"] is False, f"{path}: P019 pre-acceptance cannot claim realtime")
    require(
        claim_guard["may_claim_trading_readiness"] is False,
        f"{path}: observation freshness cannot claim trading readiness",
    )
    if payload["observation_mode"] in {"blocked", "snapshot", "replay"}:
        require(claim_guard["may_claim_realtime"] is False, f"{path}: {payload['observation_mode']} cannot claim realtime")
    if cursor["continuity"] in {"partial", "gap", "unknown"} or sequence_window["gap_count"] > 0:
        require(
            claim_guard["may_claim_complete_history"] is False,
            f"{path}: gapped/partial cursor cannot claim complete history",
        )
        require(claim_guard["blockers"], f"{path}: gapped/partial cursor requires blockers")
    for blocker in claim_guard["blockers"]:
        require(blocker["blocker_id"], f"{path}: freshness blocker missing id")
        require(blocker["next_action"], f"{path}: freshness blocker missing next action")


def validate_cross_broker_extension_matrix(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(
        payload["schema_version"] == "broker_observation_cross_broker_extension_matrix.v1",
        f"{path}: schema_version mismatch",
    )
    require(payload["adr_id"] == "ADR-0005", f"{path}: wrong ADR id")
    required_contracts = {
        "broker_observation_profile.v1",
        "broker_observation_session_conflict_policy.v1",
        "broker_observation_report_batch.v1",
        "broker_observation_freshness_sequence_checkpoint.v1",
        "broker_observation_store_snapshot.v1",
        "account_mirror_projection.v1",
    }
    require(set(payload["canonical_contracts"]) == required_contracts, f"{path}: canonical contract set drifted")

    expected_pairs = {
        "ib_tws": "ib_tws_observation",
        "ctp": "ctp_observation",
        "stock_broker": "stock_broker_observation",
        "cqg": "cqg_observation",
        "tt": "tt_observation",
    }
    rows = {row["broker_family"]: row for row in payload["broker_rows"]}
    require(set(rows) == set(expected_pairs), f"{path}: broker family set must cover {sorted(expected_pairs)}")
    for broker_family, source_kind in expected_pairs.items():
        row = rows[broker_family]
        require(row["source_kind"] == source_kind, f"{path}: {broker_family} source_kind mismatch")
        require(row["profile_contract"] == "broker_observation_profile.v1", f"{path}: {broker_family} profile forked")
        require(row["report_contract"] == "broker_observation_report_batch.v1", f"{path}: {broker_family} report forked")
        require(row["store_contract"] == "broker_observation_store_snapshot.v1", f"{path}: {broker_family} store forked")
        require(
            row["freshness_contract"] == "broker_observation_freshness_sequence_checkpoint.v1",
            f"{path}: {broker_family} freshness forked",
        )
        require(row["projection_boundary"] == "account_mirror", f"{path}: {broker_family} must project through Account Mirror")
        require(row["command_allowed"] is False, f"{path}: {broker_family} observation cannot allow command")
        require(row["raw_secret_values_recorded"] is False, f"{path}: {broker_family} must not record raw secrets")
        if row["status"] != "implemented":
            require(row["blocker_id"], f"{path}: blocked/not implemented {broker_family} requires blocker")
    rules = payload["extension_rules"]
    for rule_name in [
        "no_broker_specific_ui_truth",
        "no_command_from_observation",
        "no_raw_secret_material",
        "missing_adapter_blocks",
        "new_broker_must_extend_matrix",
    ]:
        require(rules[rule_name] is True, f"{path}: extension rule {rule_name} must be true")


def validate_report_mapping_matrix(path: Path) -> None:
    payload = load_json(path)
    assert_no_secret_material(payload, path)
    require(
        payload["schema_version"] == "broker_observation_report_mapping_matrix.v1",
        f"{path}: schema_version mismatch",
    )
    require(ACCOUNT_ID_RE.match(payload["account_id"]) is not None, f"{path}: account_id must be canonical")
    assert_command_disabled(payload["command"], path)
    raw_policy = payload["raw_payload_policy"]
    require(raw_policy["payload_ref_required"] is True, f"{path}: raw payload ref must be required")
    require(raw_policy["payload_checksum_required"] is True, f"{path}: raw payload checksum must be required")
    require(raw_policy["excerpt_must_be_redacted"] is True, f"{path}: raw payload excerpt must be redacted")
    require(raw_policy["browser_may_parse_raw_payload"] is False, f"{path}: browser must not parse raw payload")

    required_by_report_type = {
        "OrderStatusReport": {
            "report_id",
            "account_id",
            "instrument_id",
            "client_order_id",
            "venue_order_id",
            "order_status",
            "quantity",
            "filled_quantity",
            "remaining_quantity",
            "event_timestamp",
            "observed_timestamp",
            "received_timestamp",
            "sequence",
            "source_ref",
            "source_checksum",
            "raw_payload_provenance",
        },
        "FillReport": {
            "report_id",
            "account_id",
            "instrument_id",
            "client_order_id",
            "venue_order_id",
            "trade_id",
            "last_px",
            "last_qty",
            "event_timestamp",
            "observed_timestamp",
            "received_timestamp",
            "sequence",
            "source_ref",
            "source_checksum",
            "raw_payload_provenance",
        },
    }
    mappings_by_type: dict[str, list[dict[str, Any]]] = {"OrderStatusReport": [], "FillReport": []}
    for mapping in payload["mappings"]:
        report_type = mapping["target_report_type"]
        mappings_by_type[report_type].append(mapping)
        require(mapping["raw_payload_is_canonical"] is False, f"{path}: raw payload cannot be canonical")
        required_fields = set(mapping["required_target_fields"])
        missing_required = required_by_report_type[report_type] - required_fields
        require(not missing_required, f"{path}: {report_type} missing required fields {sorted(missing_required)}")
        mapped_targets = {item["target_field"] for item in mapping["field_map"]}
        require("raw_payload" not in mapped_targets, f"{path}: raw_payload cannot be a target field")
        if report_type == "OrderStatusReport":
            for field in ["venue_order_id", "order_status", "filled_quantity", "remaining_quantity", "sequence"]:
                require(field in mapped_targets, f"{path}: OrderStatusReport missing mapped target {field}")
        if report_type == "FillReport":
            for field in ["venue_order_id", "trade_id", "last_px", "last_qty", "sequence"]:
                require(field in mapped_targets, f"{path}: FillReport missing mapped target {field}")
        provenance_fields = set(mapping["provenance_fields"])
        for provenance in [
            "source_ref",
            "source_checksum",
            "raw_payload_provenance.payload_ref",
            "raw_payload_provenance.payload_checksum",
            "raw_payload_provenance.excerpt_redacted",
        ]:
            require(provenance in provenance_fields, f"{path}: missing provenance field {provenance}")
    for report_type, mappings in mappings_by_type.items():
        require(mappings, f"{path}: missing mapping for {report_type}")


def expect_failure(func, path: Path, reason: str) -> None:
    try:
        func(path)
    except ContractError:
        return
    raise AssertionError(f"{path} unexpectedly passed negative fixture validation: {reason}")


def main() -> None:
    validate_docs_gates()
    validate_schema_files()

    validate_profile(FIXTURE_DIR / "ib_tws_profile_blocked_adr0005_not_accepted.json")
    validate_session_conflict_policy(FIXTURE_DIR / "ib_tws_session_conflict_policy_blocked.json")
    validate_report_batch(FIXTURE_DIR / "ib_tws_report_batch_sample.json")
    validate_report_mapping_matrix(FIXTURE_DIR / "ib_tws_report_mapping_matrix.json")
    validate_freshness_sequence_checkpoint(FIXTURE_DIR / "ib_tws_freshness_sequence_blocked_gap.json")
    validate_store_snapshot(FIXTURE_DIR / "ib_tws_store_complete_reload.json")
    validate_store_snapshot(FIXTURE_DIR / "ib_tws_store_gap_blocker.json")
    validate_cross_broker_extension_matrix(FIXTURE_DIR / "cross_broker_extension_matrix_blocked.json")

    expect_failure(validate_profile, FIXTURE_DIR / "invalid_profile_raw_secret.json", "raw secrets must be rejected")
    expect_failure(
        validate_report_batch,
        FIXTURE_DIR / "invalid_report_command_enabled.json",
        "command actions must be rejected",
    )
    expect_failure(
        validate_report_batch,
        FIXTURE_DIR / "invalid_report_raw_payload_truth.json",
        "raw broker payload truth must be rejected",
    )
    expect_failure(
        validate_report_mapping_matrix,
        FIXTURE_DIR / "invalid_report_mapping_raw_payload_canonical.json",
        "raw broker payload cannot be canonical report mapping",
    )
    expect_failure(
        validate_report_mapping_matrix,
        FIXTURE_DIR / "invalid_report_mapping_missing_fill_fields.json",
        "FillReport mapping must include trade id, last price and last quantity",
    )
    expect_failure(
        validate_session_conflict_policy,
        FIXTURE_DIR / "invalid_session_conflict_fail_open.json",
        "session conflict policy must fail closed",
    )
    expect_failure(
        validate_session_conflict_policy,
        FIXTURE_DIR / "invalid_session_conflict_missing_nautilus_key.json",
        "session conflict policy must include Nautilus trading session key",
    )
    expect_failure(
        validate_freshness_sequence_checkpoint,
        FIXTURE_DIR / "invalid_freshness_snapshot_claims_realtime.json",
        "snapshot freshness cannot claim realtime",
    )
    expect_failure(
        validate_freshness_sequence_checkpoint,
        FIXTURE_DIR / "invalid_freshness_gap_claims_complete.json",
        "gapped freshness cursor cannot claim complete history",
    )
    expect_failure(
        validate_cross_broker_extension_matrix,
        FIXTURE_DIR / "invalid_cross_broker_missing_tt.json",
        "cross broker matrix must cover TT",
    )
    expect_failure(
        validate_cross_broker_extension_matrix,
        FIXTURE_DIR / "invalid_cross_broker_ctp_command_contract_fork.json",
        "cross broker matrix must reject command and contract forks",
    )
    expect_failure(
        validate_store_snapshot,
        FIXTURE_DIR / "invalid_store_claims_truth.json",
        "local store cannot claim broker/account/order truth",
    )
    expect_failure(
        validate_store_snapshot,
        FIXTURE_DIR / "invalid_store_memory_only_reload.json",
        "durable reload cannot pass from live memory only",
    )

    print("ADR0005_BROKER_OBSERVATION_CONTRACTS_OK: positive=8 negative=13 docs_gates=ok")


if __name__ == "__main__":
    main()
