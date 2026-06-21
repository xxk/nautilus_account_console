from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-readiness-probe.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PREACCEPTANCE_COVERAGE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "pre-acceptance-coverage.md"


class TwsApiReadinessProbeError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TwsApiReadinessProbeError(message)


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
    payload = load(PROBE)
    acceptance = read(ACCEPTANCE)
    coverage = read(PREACCEPTANCE_COVERAGE)

    require(payload["schema"] == "account-console.p019-tws-api-readiness-probe.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "display alias mismatch")
    require(payload["probe_kind"] == "local_tws_api_readiness", "probe kind mismatch")
    require(payload["evidence_kind"] == "api_readiness_probe", "evidence kind mismatch")
    require(payload["ibapi_available"] is True, "worktree-local ibapi runtime must be available")
    require(payload["ibapi_runtime_ref"] == "output/runtime/python", "ibapi runtime ref drifted")
    require(payload["host_ref"] == "localhost_tws_api", "host must stay redacted ref")

    port_refs = payload["candidate_port_refs"]
    require(set(port_refs) == {"tws_live_default", "tws_paper_default", "gateway_live_default", "gateway_paper_default"}, "port refs drifted")
    for port_ref, result in port_refs.items():
        require(result["checked"] is True, f"{port_ref} must be checked")
        require(isinstance(result["open"], bool), f"{port_ref} open flag must be boolean")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw broker endpoint must not be recorded")
    require(boundaries["tws_api_account_query_sent"] is False, "readiness probe must not query account values")
    require(boundaries["funds_positions_values_recorded"] is False, "readiness probe must not record funds/positions")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "screenshots must not be used for funds/positions")
    require(boundaries["order_action_sent"] is False, "readiness probe must not send order actions")

    for non_claim in [
        "does_not_prove_account_truth",
        "does_not_prove_funds_truth",
        "does_not_prove_positions_truth",
        "does_not_accept_adr0005",
        "does_not_authorize_order_action",
    ]:
        require(non_claim in payload["explicit_non_claims"], f"missing non-claim {non_claim}")

    if payload["ready_for_tws_api_funds_positions_query"]:
        require(any(result["open"] for result in port_refs.values()), "ready probe requires at least one open local TWS API slot")
        require(payload["typed_blocker"] is None, "ready probe must not carry blocker")
    else:
        blocker = payload["typed_blocker"]
        require(blocker["blocker_id"] == "tws_api_readiness_missing", "blocker id mismatch")
        require(blocker["blocker_kind"] == "local_api_readiness_blocker", "blocker kind mismatch")
        require(blocker["reasons"], "blocked probe must include reasons")
        require(blocker["reasons"] == ["local_tws_api_socket_not_open"], "blocked probe must now only wait for local TWS API socket")

    forbidden_fragments = ["password=", "auth_code=", "api_key=", "secret=", "127.0.0.1:", "7496", "7497", "4001", "4002"]
    for value in walk_values(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in forbidden_fragments if fragment in lowered]
            require(not hits, f"probe recorded forbidden raw value fragment {hits} in {value!r}")

    for term in [
        "probe_p019_tws_api_readiness.py",
        "validate_p019_tws_api_readiness_probe.py",
        "P019_TWS_API_READINESS_PROBE_OK",
        "tws_api_readiness_missing",
    ]:
        require(term in acceptance, f"P019 acceptance missing term {term}")
    require(
        "Funds and positions closeout requires TWS API / owner runtime source data" in coverage,
        "coverage must keep TWS API funds/positions requirement",
    )

    status = "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked"
    print(f"P019_TWS_API_READINESS_PROBE_OK: status={status} account_query_sent=false")


if __name__ == "__main__":
    main()
