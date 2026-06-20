from __future__ import annotations

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
    expect_rejected(FIXTURE_DIR / "invalid_order_intent_missing_idempotency.json", validate_order_intent)
    expect_rejected(FIXTURE_DIR / "invalid_order_intent_raw_secret_flag.json", validate_order_intent)
    expect_rejected(FIXTURE_DIR / "invalid_cancel_intent_missing_identity.json", validate_cancel_intent)
    expect_rejected(FIXTURE_DIR / "invalid_audit_ack_final_state.json", validate_audit)
    print("P023_ACCOUNT_COMMAND_CONTRACTS_OK: positive=3 negative=4")


if __name__ == "__main__":
    main()
