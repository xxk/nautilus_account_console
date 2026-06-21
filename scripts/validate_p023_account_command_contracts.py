from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "account_command"
FIXTURE_DIR = CONTRACT_DIR / "fixtures" / "openctp19053"

ACCOUNT_ID = "acct.ctp.paper.19053"
CHECKSUM_RE = re.compile(r"^sha256:[a-f0-9]{64}$")


class P023CommandContractError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P023CommandContractError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_local_ref(ref: str, *, path: Path) -> Path | None:
    if "://" in ref:
        return None
    target = (ROOT / ref).resolve()
    root = ROOT.resolve()
    require(target == root or root in target.parents, f"{path}: ref escapes worktree: {ref}")
    require(target.exists(), f"{path}: referenced artifact missing: {ref}")
    return target


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def validate_ref_checksum(payload: dict[str, Any], *, ref_key: str, checksum_key: str, path: Path) -> dict[str, Any] | None:
    ref = str(payload.get(ref_key) or "").strip()
    checksum = str(payload.get(checksum_key) or "").strip()
    require(ref, f"{path}: {ref_key} missing")
    require(CHECKSUM_RE.match(checksum) is not None, f"{path}: {checksum_key} invalid")
    target = resolve_local_ref(ref, path=path)
    if target is None:
        return None
    require(sha256_file(target) == checksum, f"{path}: checksum mismatch for {ref_key}")
    return load(target)


def validate_schema_files() -> None:
    expected = [
        "order_intent.schema.json",
        "cancel_intent.schema.json",
        "decision_and_event.schema.json",
    ]
    for name in expected:
        path = CONTRACT_DIR / name
        require(path.exists(), f"missing schema {name}")
        payload = load(path)
        require(payload.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{name}: schema draft mismatch")
        require(payload.get("title"), f"{name}: title missing")


def validate_order_intent(payload: dict[str, Any], *, path: Path) -> None:
    required = [
        "schema_version",
        "intent_id",
        "account_id",
        "mode",
        "action",
        "instrument",
        "exchange",
        "side",
        "quantity",
        "order_type",
        "limit_price",
        "time_in_force",
        "offset",
        "idempotency_key",
        "operator_ref",
        "preflight_ref",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]
    for key in required:
        require(key in payload, f"{path}: missing {key}")
    require(payload["schema_version"] == "account_command.order_intent.v1", f"{path}: schema mismatch")
    require(payload["account_id"] == ACCOUNT_ID, f"{path}: account mismatch")
    require(payload["mode"] == "paper_armed", f"{path}: first landing must be paper_armed")
    require(payload["action"] == "submit", f"{path}: action mismatch")
    require(payload["side"] in {"BUY", "SELL"}, f"{path}: side mismatch")
    require(isinstance(payload["quantity"], int) and payload["quantity"] > 0, f"{path}: quantity invalid")
    require(payload["order_type"] == "LIMIT", f"{path}: order_type invalid")
    require(float(payload["limit_price"]) > 0, f"{path}: limit_price invalid")
    require(payload["time_in_force"] in {"GFD", "IOC", "FAK", "FOK"}, f"{path}: time_in_force invalid")
    require(payload["offset"] in {"OPEN", "CLOSE", "CLOSETODAY", "CLOSEYESTERDAY"}, f"{path}: offset invalid")
    require(len(str(payload["idempotency_key"])) >= 12, f"{path}: idempotency key too short")
    assert_redacted(payload, path)


def validate_cancel_intent(payload: dict[str, Any], *, path: Path) -> None:
    required = [
        "schema_version",
        "intent_id",
        "account_id",
        "mode",
        "action",
        "instrument",
        "exchange",
        "client_order_id",
        "venue_order_id",
        "order_ref",
        "front_id",
        "session_id",
        "idempotency_key",
        "operator_ref",
        "readback_ref",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]
    for key in required:
        require(key in payload, f"{path}: missing {key}")
    require(payload["schema_version"] == "account_command.cancel_intent.v1", f"{path}: schema mismatch")
    require(payload["account_id"] == ACCOUNT_ID, f"{path}: account mismatch")
    require(payload["mode"] == "paper_armed", f"{path}: first landing must be paper_armed")
    require(payload["action"] == "cancel", f"{path}: action mismatch")
    for key in ["client_order_id", "venue_order_id", "order_ref", "readback_ref", "idempotency_key"]:
        require(str(payload.get(key) or "").strip(), f"{path}: {key} missing")
    require(isinstance(payload["front_id"], int), f"{path}: front_id invalid")
    require(isinstance(payload["session_id"], int), f"{path}: session_id invalid")
    assert_redacted(payload, path)


def validate_audit(payload: dict[str, Any], *, path: Path) -> None:
    require(payload["schema_version"] == "account_command.command_audit_record.v1", f"{path}: schema mismatch")
    require(payload["account_id"] == ACCOUNT_ID, f"{path}: account mismatch")
    require(payload["status"] in {"reconciled", "blocked", "mismatch", "timeout"}, f"{path}: status invalid")
    require(CHECKSUM_RE.match(str(payload["checksum"])) is not None, f"{path}: checksum invalid")
    require(payload.get("gateway_ack_is_final_state") is False, f"{path}: gateway ack must not be final")
    for key in ["intent_refs", "risk_decision_refs", "approval_decision_refs", "gateway_event_refs", "readback_refs"]:
        require(isinstance(payload.get(key), list) and payload[key], f"{path}: {key} missing")
    require(payload.get("reconciliation_ref"), f"{path}: reconciliation ref missing")
    assert_redacted(payload, path)


def validate_broker_order_identity(identity: Any, *, path: Path, label: str) -> dict[str, Any]:
    require(isinstance(identity, dict), f"{path}: {label} must be an object")
    for key in ["client_order_id", "order_ref", "front_id", "session_id"]:
        require(key in identity, f"{path}: {label}.{key} missing")
    require(str(identity["client_order_id"]).strip(), f"{path}: {label}.client_order_id missing")
    require(str(identity["order_ref"]).strip(), f"{path}: {label}.order_ref missing")
    require(isinstance(identity["front_id"], int), f"{path}: {label}.front_id invalid")
    require(isinstance(identity["session_id"], int), f"{path}: {label}.session_id invalid")
    return identity


def validate_submit_idempotency_replay(payload: dict[str, Any], *, path: Path) -> None:
    required = [
        "schema_version",
        "evidence_level",
        "account_id",
        "mode",
        "action",
        "idempotency_key",
        "original_intent_ref",
        "original_intent_checksum",
        "retry_intent_ref",
        "retry_intent_checksum",
        "command_result_ref",
        "command_result_checksum",
        "gateway_event_ref",
        "gateway_event_checksum",
        "readback_ref",
        "readback_checksum",
        "original_broker_order_identity",
        "retry_broker_order_identity",
        "same_command_result",
        "same_broker_order_identity",
        "duplicate_broker_order_created",
        "gateway_send_replayed",
        "runtime_duplicate_send_attempted",
        "gateway_ack_is_final_state",
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
    ]
    for key in required:
        require(key in payload, f"{path}: missing {key}")
    require(payload["schema_version"] == "account_command.submit_idempotency_replay.v1", f"{path}: schema mismatch")
    require(payload["evidence_level"] == "contract_lock", f"{path}: evidence level mismatch")
    require(payload["account_id"] == ACCOUNT_ID, f"{path}: account mismatch")
    require(payload["mode"] == "paper_armed", f"{path}: mode mismatch")
    require(payload["action"] == "submit", f"{path}: action mismatch")
    require(len(str(payload["idempotency_key"])) >= 12, f"{path}: idempotency key too short")
    original_intent = validate_ref_checksum(
        payload, ref_key="original_intent_ref", checksum_key="original_intent_checksum", path=path
    )
    retry_intent = validate_ref_checksum(payload, ref_key="retry_intent_ref", checksum_key="retry_intent_checksum", path=path)
    command_result = validate_ref_checksum(
        payload, ref_key="command_result_ref", checksum_key="command_result_checksum", path=path
    )
    gateway_event = validate_ref_checksum(payload, ref_key="gateway_event_ref", checksum_key="gateway_event_checksum", path=path)
    validate_ref_checksum(payload, ref_key="readback_ref", checksum_key="readback_checksum", path=path)
    if original_intent is not None:
        validate_order_intent(original_intent, path=Path(str(payload["original_intent_ref"])))
        require(original_intent["idempotency_key"] == payload["idempotency_key"], f"{path}: original idempotency mismatch")
    if retry_intent is not None:
        validate_order_intent(retry_intent, path=Path(str(payload["retry_intent_ref"])))
        require(retry_intent["idempotency_key"] == payload["idempotency_key"], f"{path}: retry idempotency mismatch")
    if command_result is not None:
        validate_audit(command_result, path=Path(str(payload["command_result_ref"])))
    original_identity = validate_broker_order_identity(
        payload["original_broker_order_identity"], path=path, label="original_broker_order_identity"
    )
    retry_identity = validate_broker_order_identity(
        payload["retry_broker_order_identity"], path=path, label="retry_broker_order_identity"
    )
    if gateway_event is not None:
        require(gateway_event.get("schema_version") == "account_command.execution_event.v1", f"{path}: event schema mismatch")
        require(gateway_event.get("status") == "accepted", f"{path}: gateway event status mismatch")
        require(gateway_event.get("gateway_ack_is_final_state") is False, f"{path}: gateway ack must not be final")
        for key in ["client_order_id", "order_ref", "front_id", "session_id"]:
            require(str(gateway_event.get(key)) == str(original_identity[key]), f"{path}: gateway identity {key} mismatch")
    require(payload["original_intent_checksum"] == payload["retry_intent_checksum"], f"{path}: retry must replay same intent")
    require(payload["same_command_result"] is True, f"{path}: retry must map to same command result")
    require(payload["same_broker_order_identity"] is True, f"{path}: retry must map to same broker order identity")
    require(original_identity == retry_identity, f"{path}: broker order identity changed")
    require(payload["duplicate_broker_order_created"] is False, f"{path}: duplicate broker order created")
    require(payload["gateway_send_replayed"] is False, f"{path}: gateway send replayed")
    require(payload["runtime_duplicate_send_attempted"] is False, f"{path}: runtime duplicate send attempted")
    require(payload["gateway_ack_is_final_state"] is False, f"{path}: gateway ack must not be final")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_send_duplicate_broker_order",
        "does_not_claim_runtime_duplicate_submit_pass",
        "does_not_enable_web_command_controls",
    ]:
        require(claim in non_claims, f"{path}: missing non-claim {claim}")
    assert_redacted(payload, path)


def iter_string_values(payload: Any):
    if isinstance(payload, dict):
        for value in payload.values():
            yield from iter_string_values(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from iter_string_values(item)
    elif isinstance(payload, str):
        yield payload


def assert_redacted(payload: Any, path: Path) -> None:
    for value in iter_string_values(payload):
        lowered = value.lower()
        for fragment in ["password", "auth_code", "authcode", "tcp://", "front=", "token=", "api_key", "secret="]:
            require(fragment not in lowered, f"{path}: forbidden sensitive value fragment {fragment}")
    if isinstance(payload, dict):
        if "raw_secret_values_recorded" in payload:
            require(payload["raw_secret_values_recorded"] is False, f"{path}: raw secrets recorded")
        if "raw_broker_endpoint_recorded" in payload:
            require(payload["raw_broker_endpoint_recorded"] is False, f"{path}: raw endpoint recorded")


def expect_rejected(path: Path, validator) -> None:
    try:
        validator(load(path), path=path)
    except P023CommandContractError:
        return
    raise AssertionError(f"{path} unexpectedly passed")


def main() -> None:
    validate_schema_files()
    validate_order_intent(load(FIXTURE_DIR / "order_intent_valid.json"), path=FIXTURE_DIR / "order_intent_valid.json")
    validate_cancel_intent(load(FIXTURE_DIR / "cancel_intent_valid.json"), path=FIXTURE_DIR / "cancel_intent_valid.json")
    validate_audit(load(FIXTURE_DIR / "command_audit_valid.json"), path=FIXTURE_DIR / "command_audit_valid.json")
    validate_submit_idempotency_replay(
        load(FIXTURE_DIR / "submit_idempotency_replay_valid.json"),
        path=FIXTURE_DIR / "submit_idempotency_replay_valid.json",
    )
    expect_rejected(FIXTURE_DIR / "invalid_order_intent_missing_idempotency.json", validate_order_intent)
    expect_rejected(FIXTURE_DIR / "invalid_order_intent_raw_secret_flag.json", validate_order_intent)
    expect_rejected(FIXTURE_DIR / "invalid_cancel_intent_missing_identity.json", validate_cancel_intent)
    expect_rejected(FIXTURE_DIR / "invalid_audit_ack_final_state.json", validate_audit)
    expect_rejected(
        FIXTURE_DIR / "invalid_submit_idempotency_replay_second_broker_order.json",
        validate_submit_idempotency_replay,
    )
    expect_rejected(
        FIXTURE_DIR / "invalid_submit_idempotency_replay_missing_source_ref.json",
        validate_submit_idempotency_replay,
    )
    print("P023_ACCOUNT_COMMAND_CONTRACTS_OK: positive=4 negative=6")


if __name__ == "__main__":
    main()
