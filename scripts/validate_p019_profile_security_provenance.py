from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_profile_blocked_adr0005_not_accepted.json"
REPORT_BATCH = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_report_batch_sample.json"
REPORT_MAPPING = ROOT / "contracts" / "broker_observation" / "fixtures" / "ib_tws_report_mapping_matrix.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"

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
FORBIDDEN_ACTIONS = {"submit", "cancel", "replace", "modify", "placeOrder", "cancelOrder"}


class ProfileSecurityProvenanceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProfileSecurityProvenanceError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk_values(item))
    return values


def assert_no_secret_material(payload: dict[str, Any], label: str) -> None:
    require(payload.get("raw_secret_values_recorded") is False, f"{label}: raw_secret_values_recorded must be false")
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in FORBIDDEN_SECRET_FRAGMENTS if fragment in lowered]
            require(not hits, f"{label}: forbidden secret-like material {hits} in {value!r}")


def assert_command_disabled(command: dict[str, Any], label: str) -> None:
    require(command["enabled"] is False, f"{label}: command must be disabled")
    require(command["allowed_actions"] == [], f"{label}: allowed actions must be empty")
    require(not FORBIDDEN_ACTIONS.intersection(command["allowed_actions"]), f"{label}: forbidden action present")


def require_terms(path: Path, terms: list[str]) -> None:
    text = read(path)
    missing = [term for term in terms if term not in text]
    require(not missing, f"{path}: missing terms {missing}")


def main() -> None:
    profile = load(PROFILE)
    report_batch = load(REPORT_BATCH)
    report_mapping = load(REPORT_MAPPING)

    assert_no_secret_material(profile, "profile")
    require(profile["mode"] == "read_only_observation", "profile must be read-only observation")
    require(profile["adr_gate"]["adr_id"] == "ADR-0005", "profile must carry ADR-0005 gate")
    require(profile["adr_gate"]["decision_status"] == "proposed", "profile must remain pre-acceptance")
    require(profile["adr_gate"]["direct_session_allowed"] is False, "profile must block direct session")
    require(profile["adr_gate"]["blocker_id"] == "adr0005_not_accepted", "profile must carry ADR blocker")
    require(profile["config_ref"].startswith("owner-config-ref://"), "profile config must be owner ref only")
    require(profile["secret_ref"].startswith("owner-secret-ref://"), "profile secret must be owner ref only")
    assert_command_disabled(profile["command"], "profile")
    require(profile["projection_boundary"] == "account_mirror", "profile must project through Account Mirror")

    assert_no_secret_material(report_batch, "report_batch")
    assert_command_disabled(report_batch["command"], "report_batch")
    for report in report_batch["reports"]:
        require("raw_payload" not in report, "report batch must not store raw payload as canonical truth")
        provenance = report["raw_payload_provenance"]
        require(provenance["payload_ref"], "report must carry raw payload ref")
        require(provenance["payload_checksum"].startswith("sha256:"), "report must carry raw payload checksum")
        require(provenance["excerpt_redacted"] is True, "report raw payload excerpt must be redacted")

    assert_no_secret_material(report_mapping, "report_mapping")
    assert_command_disabled(report_mapping["command"], "report_mapping")
    raw_policy = report_mapping["raw_payload_policy"]
    require(raw_policy["payload_ref_required"] is True, "raw payload ref must be required")
    require(raw_policy["payload_checksum_required"] is True, "raw payload checksum must be required")
    require(raw_policy["excerpt_must_be_redacted"] is True, "raw payload excerpt must be redacted")
    require(raw_policy["browser_may_parse_raw_payload"] is False, "browser must not parse raw payload")
    for mapping in report_mapping["mappings"]:
        require(mapping["raw_payload_is_canonical"] is False, "mapping must not make raw payload canonical")
        mapped_targets = {item["target_field"] for item in mapping["field_map"]}
        require("raw_payload" not in mapped_targets, "mapping must not target raw_payload")

    require_terms(
        ACCEPTANCE,
        [
            "P019 profile/security/provenance validator",
            "validate_p019_profile_security_provenance.py",
            "P019_PROFILE_SECURITY_PROVENANCE_OK: observation_only=true raw_secret_refs_only=true raw_payload_provenance_only=true",
        ],
    )
    require_terms(
        PHASE_PLAN,
        [
            "validate_p019_profile_security_provenance.py",
            "P019_PROFILE_SECURITY_PROVENANCE_OK: observation_only=true raw_secret_refs_only=true raw_payload_provenance_only=true",
        ],
    )

    print("P019_PROFILE_SECURITY_PROVENANCE_OK: observation_only=true raw_secret_refs_only=true raw_payload_provenance_only=true")


if __name__ == "__main__":
    main()
