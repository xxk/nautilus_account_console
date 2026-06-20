from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
ACCOUNT_SUMMARY = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "account_summary.json"
POSITIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "positions.json"
BUILDER = ROOT / "scripts" / "build_ib_u3028269_source_package_from_tws_api.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class IbSourcePackageError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IbSourcePackageError(message)


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


def main() -> None:
    payload = load(SOURCE_PACKAGE)
    account_summary = load(ACCOUNT_SUMMARY)
    positions = load(POSITIONS)
    builder = read(BUILDER)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema_version"] == "account_source_artifact.v1", "schema drifted")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "display alias mismatch")
    require(payload["source_owner"] == "account-console-broker-observation-session", "source owner mismatch")
    require(payload["source_kind"] == "ib_tws_observation", "source kind mismatch")
    require(payload["source_health"]["api_transport"] == "ib_tws_api", "API transport mismatch")
    require(payload["source_ref"] == "output/account_capability/ib-live-u3028269/source-package.json", "source ref mismatch")
    require(str(payload["source_checksum"]).startswith("sha256:"), "source checksum missing")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not back funds/positions")
    require(boundaries["tws_api_account_query_required"] is True, "TWS API account query must be required")
    require(boundaries["order_action_sent"] is False, "order action must not be sent")

    health = payload["source_health"]
    if health["state"] == "blocked":
        require(health["blocker_id"] == "tws_api_readiness_missing", "blocked package must carry readiness blocker")
        require(account_summary["blocker_id"] == "tws_api_readiness_missing", "blocked account query blocker mismatch")
        require(positions["blocker_id"] == "tws_api_readiness_missing", "blocked positions query blocker mismatch")
        require(account_summary["success"] is False and positions["success"] is False, "blocked source package must align with blocked query artifacts")
        require(payload["balances"] == [], "blocked package must not invent balances")
        require(payload["positions"] == [], "blocked package must not invent positions")
        require(payload["orders"] == [] and payload["fills"] == [], "blocked package must not invent reports")
        require(payload["source_inputs"]["account_summary_query"] is None, "blocked package must not claim account query input")
        require(payload["source_inputs"]["positions_query"] is None, "blocked package must not claim positions input")
    else:
        require(health["state"] == "ready", "source health must be ready or blocked")
        require(payload["source_mode"] == "live_observation", "ready package must be live_observation")
        require(payload["source_inputs"]["account_summary_query"], "ready package missing account summary query ref")
        require(payload["source_inputs"]["positions_query"], "ready package missing positions query ref")
        require(payload["balances"], "ready package must contain TWS API balances")

    forbidden_fragments = ["password=", "passwd=", "auth_code=", "api_key=", "secret=", "127.0.0.1:"]
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
            require(not hits, f"source package recorded forbidden fragment {hits} in {value!r}")

    for term in [
        "account-console.ib-tws-api-query.v1",
        "screenshot_used_for_values",
        "order_action_sent",
        "tws_api_readiness_missing",
    ]:
        require(term in builder, f"builder missing guard term {term}")
    for term in [
        "build_ib_u3028269_source_package_from_tws_api.py",
        "validate_p019_ib_u3028269_source_package.py",
        "P019_IB_U3028269_SOURCE_PACKAGE_OK",
    ]:
        require(term in acceptance, f"acceptance missing source-package term {term}")
        require(term in phase_plan, f"phase plan missing source-package term {term}")

    status = health["state"]
    print(f"P019_IB_U3028269_SOURCE_PACKAGE_OK: status={status} api_transport=ib_tws_api screenshot_values=false")


if __name__ == "__main__":
    main()
