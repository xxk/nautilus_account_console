from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "account_capability" / "account_capability_bundle.schema.json"
FIXTURE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_capability"

POSITIVE_FIXTURES = [
    "acct_nautilus_paper_demo_capability.json",
    "acct_ctp_paper_19053_capability.json",
    "acct_ctp_live_025292_capability.json",
]

NEGATIVE_FIXTURES = {
    "invalid_bare_alias_canonical.json": "canonical account_id must be namespace-qualified",
    "invalid_missing_provenance.json": "observation values must carry source_ref and checksum",
    "invalid_command_inferred_live.json": "command capability must not be inferred from live account kind",
}

ACCOUNT_ID_RE = re.compile(r"^acct\.[a-z0-9_.-]+$")
CHECKSUM_RE = re.compile(r"^sha256:[a-f0-9]{64}$")


class ContractError(AssertionError):
    pass


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def require_checksum(value: str, path: Path, field: str) -> None:
    require(isinstance(value, str) and CHECKSUM_RE.match(value) is not None, f"{path}: invalid checksum at {field}")


def require_source_ref(payload: dict, path: Path, field: str) -> None:
    require(payload.get("source_ref"), f"{path}: missing source_ref at {field}")
    require_checksum(payload.get("checksum", ""), path, f"{field}.checksum")
    require(payload.get("observed_at"), f"{path}: missing observed_at at {field}")


def validate_schema_shape() -> None:
    schema = load_json(SCHEMA)
    require(schema["title"] == "Account Capability Bundle", "schema title drifted")
    required = set(schema["required"])
    for key in {"schema_version", "account", "capabilities", "observations", "boundaries", "rejection_rules"}:
        require(key in required, f"schema missing required key {key}")
    defs = schema["$defs"]
    for key in {"account_identity", "capabilities", "observations", "blocker", "boundaries"}:
        require(key in defs, f"schema missing $defs.{key}")


def validate_bundle(payload: dict, path: Path) -> None:
    require(payload["schema_version"] == "account_capability_bundle.v1", f"{path}: schema_version mismatch")

    account = payload["account"]
    account_id = account["account_id"]
    require(ACCOUNT_ID_RE.match(account_id) is not None, f"{path}: account_id is not canonical")
    require(account["display_alias"], f"{path}: missing display_alias")
    require(account["display_alias"] != account_id, f"{path}: display_alias should not duplicate canonical account_id")

    capabilities = payload["capabilities"]
    command = capabilities["command"]
    require(command["enabled"] is False, f"{path}: P011 Phase 1 fixtures must keep command disabled")
    require(command["mode"] == "disabled", f"{path}: P011 Phase 1 command mode must be disabled")
    require(command["gateway_kind"] is None, f"{path}: disabled command must not name gateway_kind")
    require(command["allowed_actions"] == [], f"{path}: disabled command must have no allowed actions")
    require(command["requires_risk_check"] is True, f"{path}: command must fail closed on risk")
    require(command["requires_approval"] is True, f"{path}: command must fail closed on approval")
    require(command["authority_ref"] is None, f"{path}: disabled command must not claim authority_ref")
    require_checksum(command["capability_checksum"], path, "capabilities.command.capability_checksum")

    observation = capabilities["observation"]
    require(observation["enabled"] is True, f"{path}: observation capability must be enabled")
    require_source_ref(observation["source_ref"], path, "capabilities.observation.source_ref")

    reconciliation = capabilities["reconciliation"]
    require(reconciliation["readback_required"] is True, f"{path}: reconciliation readback must be required")

    evidence = capabilities["evidence"]
    require(evidence["required"] is True, f"{path}: evidence must be required")
    require(evidence["source_refs_required"] is True, f"{path}: source refs must be required")
    require(evidence["checksums_required"] is True, f"{path}: checksums must be required")

    observations = payload["observations"]
    require_source_ref(observations["source_health"], path, "observations.source_health")
    for bucket in ["balances", "positions", "orders", "fills"]:
        for idx, row in enumerate(observations[bucket]):
            require_source_ref(row, path, f"observations.{bucket}[{idx}]")
    for idx, blocker in enumerate(observations["blockers"]):
        require(blocker["blocker_id"], f"{path}: blocker missing id")
        require(blocker["owner"], f"{path}: blocker missing owner")
        require(blocker["next_action"], f"{path}: blocker missing next_action")
        require(blocker["source_ref"], f"{path}: blocker missing source_ref")
        require_checksum(blocker["checksum"], path, f"observations.blockers[{idx}].checksum")

    boundaries = payload["boundaries"]
    require(boundaries["read_only_projection"] is True, f"{path}: read_only_projection must be true")
    for key in [
        "broker_truth",
        "runtime_truth",
        "account_truth",
        "order_action",
        "approval_truth",
        "capital_truth",
        "trading_readiness_truth",
    ]:
        require(boundaries[key] is False, f"{path}: boundary {key} must be false")

    require(payload["rejection_rules"], f"{path}: rejection_rules required")


def main() -> None:
    validate_schema_shape()

    for name in POSITIVE_FIXTURES:
        validate_bundle(load_json(FIXTURE_DIR / name), FIXTURE_DIR / name)

    for name, reason in NEGATIVE_FIXTURES.items():
        path = FIXTURE_DIR / name
        try:
            validate_bundle(load_json(path), path)
        except ContractError:
            continue
        raise AssertionError(f"{path} unexpectedly passed negative fixture validation: {reason}")

    print(
        "ACCOUNT_CAPABILITY_CONTRACTS_OK: "
        f"positive={len(POSITIVE_FIXTURES)} negative={len(NEGATIVE_FIXTURES)}"
    )


if __name__ == "__main__":
    main()
