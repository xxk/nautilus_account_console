from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-socket-diagnostic.json"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"


class SocketDiagnosticError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SocketDiagnosticError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    payload = load(DIAGNOSTIC)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)

    require(payload["schema"] == "account-console.p019-tws-api-socket-diagnostic.v1", "schema drifted")
    require(payload["proposal_id"] == "p019-broker-observation-session-foundation", "proposal mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["display_alias"] == "U3028269", "alias mismatch")
    require(payload["diagnostic_kind"] == "local_tws_api_socket", "diagnostic kind mismatch")
    require(payload["ibapi_available"] is True, "ibapi runtime must remain available")
    require(payload["ibapi_runtime_ref"] == "output/runtime/python", "ibapi runtime ref mismatch")
    require(payload["host_ref"] == "localhost_tws_api", "host ref mismatch")

    tws_process = payload["tws_process"]
    tws_present = tws_process["present"] is True
    if tws_present:
        require(tws_process["window_title_ref"] == "U3028269_account_window", "TWS window title ref mismatch")
        require(tws_process["responding"] is True, "TWS process must be responding")
    else:
        require(payload["ready_for_tws_api_funds_positions_query"] is False, "absent TWS process cannot be ready")

    expected_refs = {"tws_live_default", "tws_paper_default", "gateway_live_default", "gateway_paper_default"}
    require(set(payload["listener_port_refs"]) == expected_refs, "listener port refs drifted")
    require(set(payload["connect_port_refs"]) == expected_refs, "connect port refs drifted")
    require(set(payload["handshake_port_refs"]) == expected_refs, "handshake port refs drifted")
    require(payload["handshake_version_range"] == "v100..155", "IB API handshake version range drifted")

    boundaries = payload["boundaries"]
    require(boundaries["raw_secret_values_recorded"] is False, "raw secrets must not be recorded")
    require(boundaries["raw_broker_endpoint_recorded"] is False, "raw endpoint must not be recorded")
    require(boundaries["tws_api_account_query_sent"] is False, "diagnostic must not query account")
    require(boundaries["funds_positions_values_recorded"] is False, "diagnostic must not record values")
    require(boundaries["screenshot_used_for_funds_positions"] is False, "diagnostic must not use screenshots for values")
    require(boundaries["order_action_sent"] is False, "diagnostic must not send order action")

    if payload["ready_for_tws_api_funds_positions_query"]:
        require(tws_present, "ready diagnostic must see TWS process")
        require(payload["typed_blocker"] is None, "ready diagnostic must not carry blocker")
        require(
            any(item["status"] == "handshake_ok" for item in payload["handshake_port_refs"].values()),
            "ready diagnostic must have IB API handshake_ok",
        )
    else:
        require(payload["typed_blocker"]["blocker_id"] == "tws_api_readiness_missing", "blocker id mismatch")
        require(
            payload["typed_blocker"]["reasons"] in [
                ["local_tws_api_socket_not_open"],
                ["local_tws_api_handshake_not_ok"],
            ],
            "socket blocker reason mismatch",
        )
        require(
            not any(item["status"] == "handshake_ok" for item in payload["handshake_port_refs"].values()),
            "blocked diagnostic must not have handshake_ok port refs",
        )

    for term in [
        "diagnose_p019_tws_api_socket.py",
        "validate_p019_tws_api_socket_diagnostic.py",
        "P019_TWS_API_SOCKET_DIAGNOSTIC_OK",
    ]:
        require(term in acceptance, f"acceptance missing diagnostic term {term}")
        require(term in phase_plan, f"phase plan missing diagnostic term {term}")

    status = "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked"
    handshake = "handshake_ok" if status == "ready" else "handshake_not_ok"
    process_label = "present" if tws_present else "absent"
    print(f"P019_TWS_API_SOCKET_DIAGNOSTIC_OK: status={status} tws_process={process_label} {handshake}")


if __name__ == "__main__":
    main()
