from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATHS = [
    ROOT / "output" / "debug" / "p019-tws-api-readiness",
    ROOT / "output" / "account_capability" / "ib-live-u3028269",
    ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-blocked-ui-parity-evidence.json",
    ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-real-ui-parity-evidence.json",
    ROOT / "docs" / "acceptance" / "2026-06-20-p019-u3028269-synthetic-ready-ui-contract-evidence.json",
]
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class RuntimeArtifactRedactionError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeArtifactRedactionError(message)


def iter_json_files() -> list[Path]:
    files: list[Path] = []
    for path in RUNTIME_PATHS:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.json")))
        elif path.exists():
            files.append(path)
    return files


def walk(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk(item))
    return values


def main() -> None:
    files = iter_json_files()
    require(files, "P019 runtime artifacts missing")
    forbidden_fragments = [
        "password=",
        "auth_code=",
        "api_key=",
        "secret=",
        "<TWS",
        "<tws",
        "placeOrder",
        "cancelOrder",
        "reqOpenOrders",
        "reqAllOpenOrders",
        "screenshot proves funds",
        "screenshot proves positions",
        "can_trade=true",
        "broker_tradable=true",
    ]
    false_boundary_keys = {
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "raw_config_file_contents_recorded",
        "screenshot_used_for_funds_positions",
        "screenshot_used_for_values",
        "order_action_sent",
        "tws_reinstall_performed",
        "tws_config_modified_by_this_script",
        "writes_outside_worktree",
        "synthetic_evidence_used_for_real_closeout",
        "funds_positions_values_recorded_in_knowledge",
    }
    checked = 0
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        checked += 1
        for value in walk(payload):
            if isinstance(value, str):
                for fragment in forbidden_fragments:
                    require(fragment.lower() not in value.lower(), f"{path}: forbidden fragment {fragment}")
        for value in walk(payload):
            if isinstance(value, dict):
                for key in false_boundary_keys & set(value):
                    require(value[key] is False, f"{path}: boundary {key} drifted to {value[key]!r}")

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")
    for term in [
        "validate_p019_runtime_artifact_redaction.py",
        "P019_RUNTIME_ARTIFACT_REDACTION_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    print(f"P019_RUNTIME_ARTIFACT_REDACTION_OK: files={checked}")


if __name__ == "__main__":
    main()
