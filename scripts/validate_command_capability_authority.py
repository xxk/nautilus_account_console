from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMAND_API = ROOT / "backend" / "src" / "nautilus_account_console" / "command_api.py"
SOURCE_BRIDGE = ROOT / "backend" / "src" / "nautilus_account_console" / "source_bridge.py"


class CommandCapabilityAuthorityError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CommandCapabilityAuthorityError(message)


def main() -> None:
    command_api = COMMAND_API.read_text(encoding="utf-8")
    source_bridge = SOURCE_BRIDGE.read_text(encoding="utf-8")

    require("def _require_command_capability(" in command_api, "command API authority gate missing")
    require("load_capability_bundles()" in command_api, "command API must read capability bundles")
    require(
        'command.get("enabled") is not True' in command_api,
        "command API must fail closed when command.enabled is not true",
    )
    require(
        'command.get("mode") != "paper_armed"' in command_api,
        "command API must require explicit paper_armed command capability",
    )
    require(
        'authority_ref != "owner-repo://nautilus_ctp_adapter"' in command_api,
        "command API must require owner repo authority",
    )
    for function_name in [
        "accept_submit_intent",
        "accept_cancel_intent",
        "prepare_submit_runtime_run_request",
        "prepare_cancel_runtime_run_request",
    ]:
        marker = f"def {function_name}"
        start = command_api.index(marker)
        end = command_api.find("\ndef ", start + len(marker))
        body = command_api[start:] if end == -1 else command_api[start:end]
        require("_require_command_capability(" in body, f"{function_name} must call capability authority")

    require(
        'owner_evidence.get("owner_repo_ref") != "owner-repo://nautilus_ctp_adapter"' in command_api,
        "runtime closeout must require owner runtime evidence",
    )
    require(
        'raise HTTPException(status_code=409, detail="runtime closeout missing owner runtime evidence")' in command_api,
        "runtime closeout must fail closed when owner evidence is missing",
    )
    require(
        '"enabled": False' in source_bridge and '"mode": "disabled"' in source_bridge and '"allowed_actions": []' in source_bridge,
        "source bridge default command capability must remain disabled",
    )

    print(
        "COMMAND_CAPABILITY_AUTHORITY_OK: "
        "command_api_uses_capability_bundles=true "
        "paper_scope_is_not_authority=true "
        "runtime_positive_claim_requires_owner_evidence=true "
        "source_bridge_default_command_disabled=true"
    )


if __name__ == "__main__":
    main()
