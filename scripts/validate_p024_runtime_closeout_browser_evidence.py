from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "runtime-closeout-ui.json"
SCREENSHOT = EVIDENCE_DIR / "p024-runtime-closeout-ui.png"
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"
TYPES = ROOT / "frontend" / "src" / "types.ts"
ACCOUNT_ID = "acct.ctp.paper.19053"
RUN_ID = "p023-armed-20260621t0748z"


class P024RuntimeCloseoutEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024RuntimeCloseoutEvidenceError(message)


def load(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scan_forbidden_text(path: Path) -> list[str]:
    fragments = ["password=", "auth_code=", "api_key=", "secret=", "tcp://", "live_armed=true"]
    matches: list[str] = []
    for item in path.rglob("*.json"):
        text = item.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment.lower() in text for fragment in fragments):
            matches.append(str(item))
    return matches


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "account-console.p024.runtime-closeout-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == ACCOUNT_ID, "account mismatch")
    require(payload["run_id"] == RUN_ID, "run mismatch")
    require(payload["verdict"] == "blocked_pending_owner_runtime_evidence", "verdict mismatch")
    require(payload["api_status_code"] == 409, "API status code mismatch")
    require(payload["api_blocker"] == "runtime closeout missing owner runtime evidence", "API blocker mismatch")
    require(payload["runtime_gateway_send_observed"] is False, "runtime gateway send must not be claimed")
    require(payload["broker_order_created"] is False, "broker order must not be claimed")
    require(payload["browser_triggered_broker_order"] is False, "browser trigger flag mismatch")
    require(payload["gateway_ack_is_final_state"] is False, "gateway final flag mismatch")
    require(payload["raw_secret_values_recorded"] is False, "raw secret flag mismatch")
    require(payload["raw_broker_endpoint_recorded"] is False, "raw endpoint flag mismatch")
    checks = payload.get("browser_checks") or {}
    for check in [
        "runtime_panel_visible",
        "owner_evidence_blocker_visible",
        "browser_trigger_displayed_false",
        "gateway_final_displayed_false",
        "live_ready_wording_absent",
    ]:
        require(checks.get(check) is True, f"browser check missing: {check}")
    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_send_broker_order_from_browser_read",
        "does_not_store_raw_ctp_secret_or_endpoint",
        "does_not_claim_live_readiness",
        "does_not_make_gateway_ack_final_state",
        "does_not_promote_repo_local_output_to_runtime_truth",
        "owner_runtime_evidence_required_before_positive_claim",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_backend_endpoint() -> None:
    import sys

    sys.path.insert(0, str(BACKEND_SRC))
    from nautilus_account_console.main import app

    route = "/api/commands/accounts/{account_id}/runtime-closeouts/{run_id}"
    found = False
    for item in app.routes:
        if getattr(item, "path", "") == route:
            found = True
            require(getattr(item, "methods", set()) == {"GET"}, "runtime closeout route must be GET-only")
    require(found, "runtime closeout route missing")

    client = TestClient(app)
    response = client.get(f"/api/commands/accounts/{ACCOUNT_ID}/runtime-closeouts/{RUN_ID}")
    require(response.status_code == 409, "runtime closeout API must fail closed without owner evidence")
    payload = response.json()
    require(payload["detail"] == "runtime closeout missing owner runtime evidence", "runtime closeout blocker mismatch")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    types_text = TYPES.read_text(encoding="utf-8")
    for phrase in [
        "CommandRuntimeCloseoutPanel",
        "account-runtime-closeout-panel",
        "account-runtime-closeout-error",
        "account-runtime-closeout-web-trigger",
        "const commandStatus = mirrorReadback?.selected.command_status ?? null;",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in ["fetchCommandRuntimeCloseout", "runtime-closeouts"]:
        require(phrase in api_text, f"frontend API missing {phrase}")
    require("interface CommandRuntimeCloseout" in types_text, "frontend type missing CommandRuntimeCloseout")


def main() -> None:
    require(SCREENSHOT.exists(), "missing runtime closeout screenshot")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_backend_endpoint()
    validate_frontend_hooks()
    print(
        "P024_RUNTIME_CLOSEOUT_BROWSER_EVIDENCE_OK: "
        "runtime_closeout=blocked_pending_owner_runtime_evidence browser_triggered_broker_order=false gateway_ack_final=false"
    )


if __name__ == "__main__":
    main()
