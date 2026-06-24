from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "acceptance" / "browser-evidence" / "p024-account-console-paper-command-controls"
EVIDENCE = EVIDENCE_DIR / "command-controls-ui.json"
REQUIRED_SCREENSHOTS = [
    "command-controls-disabled.png",
    "paper-armed-controls.png",
    "submit-accepted-for-risk.png",
    "cancel-accepted-for-risk.png",
]
APP = ROOT / "frontend" / "src" / "App.tsx"
API = ROOT / "frontend" / "src" / "api.ts"


class P024UiCommandEvidenceError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise P024UiCommandEvidenceError(message)


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
    require(payload["schema"] == "account-console.p024.command-controls-ui.v1", "schema mismatch")
    require(payload["proposal_id"] == "p024-account-console-paper-command-controls", "proposal mismatch")
    require(payload["account_id"] == "acct.ctp.paper.19053", "account mismatch")
    require(payload["verdict"] == "pass", "verdict mismatch")
    require(payload["disabled_controls_absent"] is True, "disabled controls must be absent")
    require(payload["paper_armed_controls_visible"] is False, "paper_armed controls must not be visible without capability")
    require(payload["submit_result_status"] == "command_capability_not_mounted", "submit blocker mismatch")
    require(payload["cancel_result_status"] == "command_capability_not_mounted", "cancel blocker mismatch")
    require(payload["gateway_send_attempted"] is False, "gateway send must stay false")
    require(payload["broker_order_created"] is False, "broker order must stay false")
    require(payload["gateway_ack_is_final_state"] is False, "gateway ack final flag must stay false")
    require(payload["cancel_uses_readback_identity"] is False, "cancel readback identity must not be used when blocked")

    submit = payload["submitted_request"]
    cancel = payload["cancel_request"]
    require(submit is None, "submit request must not be emitted when blocked")
    require(cancel is None, "cancel request must not be emitted when blocked")

    non_claims = set(payload.get("explicit_non_claims") or [])
    for claim in [
        "does_not_send_broker_order_from_browser_test",
        "does_not_claim_real_openctp_runtime_command_from_ui",
        "does_not_enable_live_armed",
        "does_not_use_screenshot_as_command_truth",
        "does_not_treat_paper_armed_ui_projection_as_authority",
    ]:
        require(claim in non_claims, f"missing non-claim: {claim}")


def validate_frontend_hooks() -> None:
    app_text = APP.read_text(encoding="utf-8")
    api_text = API.read_text(encoding="utf-8")
    for phrase in [
        "account-submit-order-form",
        "account-submit-order-button",
        "account-submit-idempotency-key",
        "account-cancel-order-button",
        "account-cancel-order-identity",
        "isP024PaperArmed",
        "gateway_ack_is_final_state",
    ]:
        require(phrase in app_text, f"frontend app missing {phrase}")
    for phrase in [
        "submitPaperOrderIntent",
        "cancelPaperOrderIntent",
        "/api/commands/accounts/",
        "submit-intents",
        "cancel-intents",
    ]:
        require(phrase in api_text, f"frontend API missing {phrase}")


def main() -> None:
    for screenshot in REQUIRED_SCREENSHOTS:
        require((EVIDENCE_DIR / screenshot).exists(), f"missing browser screenshot: {screenshot}")
    leaks = scan_forbidden_text(EVIDENCE_DIR)
    require(not leaks, f"forbidden sensitive fragments found: {leaks}")
    validate_payload(load(EVIDENCE))
    validate_frontend_hooks()
    print(
        "P024_UI_COMMAND_CONTROLS_BROWSER_EVIDENCE_OK: "
        "disabled_absent=true command_capability_not_mounted=true gateway_send_attempted=false"
    )


if __name__ == "__main__":
    main()
