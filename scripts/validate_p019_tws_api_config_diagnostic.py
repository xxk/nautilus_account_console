from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class ConfigDiagnosticError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigDiagnosticError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(DIAGNOSTIC)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-tws-api-config-diagnostic.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["diagnostic_kind"] == "tws_api_config", "diagnostic kind mismatch")
    require(payload["tws_process"]["present"] is True, "TWS process must be present")
    require(payload["tws_process"]["window_title_ref"] == "U3028269_account_window", "TWS account window ref mismatch")
    require(payload["candidate_config_count"] >= 1, "expected at least one TWS config candidate")

    latest = payload["latest_config_candidate"]
    require(latest is not None, "latest config candidate missing")
    require(latest["config_ref"].startswith("local-file-ref://"), "latest config must be a local ref")
    require(latest["api_settings"]["socketClient"] in {"true", "false"}, "latest socketClient setting missing")
    require(latest["api_settings"]["port"] in {"7496", "7497"}, "latest TWS API port should be an IB TWS default")
    require(
        any(candidate["api_settings"]["socketClient"] == "true" for candidate in payload["config_candidates"]),
        "historical enabled TWS API config candidate should be visible",
    )
    require(
        any(candidate["api_settings"]["socketClient"] == "false" for candidate in payload["config_candidates"]),
        "disabled current TWS API config candidate should be visible",
    )

    expected_refs = {"tws_live_default", "tws_paper_default", "gateway_live_default", "gateway_paper_default"}
    require(set(payload["connect_port_refs"]) == expected_refs, "connect port refs drifted")

    boundaries = payload["boundaries"]
    require(boundaries["raw_config_file_contents_recorded"] is False, "raw config contents must not be recorded")
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["tws_api_account_query_sent"] is False, "diagnostic must not query account")
    require(boundaries["funds_positions_values_recorded"] is False, "diagnostic must not record values")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "diagnostic must not use screenshots")
    require(boundaries["order_action_sent"] is False, "diagnostic must not send order action")

    if payload["ready_for_tws_api_funds_positions_query"]:
        require(payload["typed_blocker"] is None, "ready config diagnostic must not carry blocker")
    else:
        blocker = payload["typed_blocker"]
        require(blocker["blocker_id"] == "tws_api_readiness_missing", "blocker id mismatch")
        require(
            blocker["primary_blocker"] == "tws_api_socket_disabled_in_latest_config_candidate",
            "primary blocker should point at latest config socketClient=false",
        )
        require("local_tws_api_socket_not_open" in blocker["reasons"], "missing socket blocker reason")
        require(
            "latest_tws_config_candidate_socket_client_false" in blocker["reasons"],
            "missing latest config blocker reason",
        )
        require(
            not any(item["connectable"] for item in payload["connect_port_refs"].values()),
            "blocked diagnostic must not have connectable TWS API refs",
        )

    for term in [
        "diagnose_p019_tws_api_config.py",
        "validate_p019_tws_api_config_diagnostic.py",
        "P019_TWS_API_CONFIG_DIAGNOSTIC_OK",
    ]:
        require(term in acceptance, f"acceptance missing config diagnostic term {term}")
        require(term in phase_plan, f"phase plan missing config diagnostic term {term}")

    status = "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked"
    primary = "none" if status == "ready" else "latest_config_socket_disabled"
    latest_socket_client = latest["api_settings"]["socketClient"]
    print(
        "P019_TWS_API_CONFIG_DIAGNOSTIC_OK: "
        f"status={status} latest_socket_client={latest_socket_client} primary_blocker={primary}"
    )


if __name__ == "__main__":
    main()
