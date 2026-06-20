from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ARTIFACT_DIR = ROOT / "contracts" / "source_artifacts" / "account_sources"
CTP19053_REAL_SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ctp-paper-19053" / "source-package.json"
CTP19053_ACCOUNT_ID = "acct.ctp.paper.19053"
CTP025292_REAL_SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ctp-live-025292" / "source-package.json"
CTP025292_ACCOUNT_ID = "acct.ctp.live.025292"
IB_U3028269_SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
IB_U3028269_ACCOUNT_ID = "acct.ib.live.u3028269"


class SourceBridgeError(ValueError):
    pass


def _fallback_route_context(payload: dict[str, Any]) -> dict[str, Any]:
    account_id = str(payload["account_id"])
    if account_id == "simulated-001":
        return {
            "state": "projected",
            "route_id": "route.p079.stage2.simulated-001",
            "account_alias": str(payload.get("account_uid", "sandbox-paper.simulated-001")),
            "market_data_source": "ctp_md.025292",
            "execution_adapter": "nautilus_sandbox_paper_simulated_runtime",
            "account_truth": "nautilus_sandbox_paper_simulated_ledger",
            "risk_domain": "sandbox",
            "evidence_partition": "p079.stage2/simulated-001/025292-md-only",
            "context_ref": str(payload.get("upstream_contract_ref", payload["source_ref"])),
            "context_checksum": payload["source_checksum"],
            "blocker_id": "simulated001_stage2_fixture_only",
        }
    if account_id == "acct.ctp.paper.19053":
        return {
            "state": "projected",
            "route_id": "route.ctp.paper.19053.account-readonly",
            "account_alias": "19053",
            "market_data_source": "not_in_scope_for_account_readback",
            "execution_adapter": "ctp_td.19053.readonly_projection",
            "account_truth": "nautilus_ctp_adapter_source_package",
            "risk_domain": "paper",
            "evidence_partition": "account/acct.ctp.paper.19053/source-package",
            "context_ref": payload["source_ref"],
            "context_checksum": payload["source_checksum"],
            "blocker_id": None,
        }
    if account_id == "acct.ctp.live.025292":
        return {
            "state": "projected",
            "route_id": "route.ctp.live.025292.account-readonly",
            "account_alias": "025292",
            "market_data_source": "not_in_scope_for_account_readback",
            "execution_adapter": "ctp_td.025292.readonly_projection",
            "account_truth": "nautilus_ctp_adapter_source_package",
            "risk_domain": "live",
            "evidence_partition": "account/acct.ctp.live.025292/source-package",
            "context_ref": payload["source_ref"],
            "context_checksum": payload["source_checksum"],
            "blocker_id": None,
        }
    if account_id == IB_U3028269_ACCOUNT_ID:
        is_blocked = str(payload.get("source_mode")) == "live_observation_blocked"
        return {
            "state": "blocked" if is_blocked else "projected",
            "route_id": "route.ib.live.u3028269.account-readonly",
            "account_alias": "U3028269",
            "market_data_source": "not_in_scope_for_account_readback",
            "execution_adapter": "ib_tws_api.readonly_observation" if not is_blocked else "ib_tws_api.blocked_until_readiness",
            "account_truth": "ib_tws_api_source_package" if not is_blocked else "blocked_until_tws_api_source_package",
            "risk_domain": "live",
            "evidence_partition": "account/acct.ib.live.u3028269/source-package",
            "context_ref": payload["source_ref"],
            "context_checksum": payload["source_checksum"],
            "blocker_id": "tws_api_readiness_missing" if is_blocked else None,
        }
    return {
        "state": "projected",
        "route_id": f"route.{account_id.removeprefix('acct.')}.readonly",
        "account_alias": str(payload["display_alias"]),
        "market_data_source": "not_in_scope_for_account_readback",
        "execution_adapter": str(payload["source_kind"]),
        "account_truth": str(payload["source_owner"]),
        "risk_domain": str(payload["account_domain"]),
        "evidence_partition": f"account/{account_id}/source-package",
        "context_ref": payload["source_ref"],
        "context_checksum": payload["source_checksum"],
        "blocker_id": None,
    }


def _blocked_route_context(
    *,
    account_id: str,
    display_alias: str,
    source_ref: str,
    checksum: str,
    blocker_id: str,
    risk_domain: str,
) -> dict[str, Any]:
    return {
        "state": "blocked",
        "route_id": f"route.{account_id.removeprefix('acct.')}.account-readonly",
        "account_alias": display_alias,
        "market_data_source": "not_in_scope_for_account_readback",
        "execution_adapter": f"ctp_td.{display_alias}.blocked_until_source_package",
        "account_truth": "blocked_until_pinned_source_package",
        "risk_domain": risk_domain,
        "evidence_partition": f"account/{account_id}/blocked-source-package",
        "context_ref": source_ref,
        "context_checksum": checksum,
        "blocker_id": blocker_id,
    }


def validate_route_context(route_context: dict[str, Any], account_id: str) -> None:
    required = {
        "state",
        "route_id",
        "account_alias",
        "market_data_source",
        "execution_adapter",
        "account_truth",
        "risk_domain",
        "evidence_partition",
        "context_ref",
        "context_checksum",
        "blocker_id",
    }
    missing = sorted(required - set(route_context))
    if missing:
        raise SourceBridgeError(f"{account_id}: route_context missing fields {missing}")
    if route_context["state"] not in {"projected", "blocked"}:
        raise SourceBridgeError(f"{account_id}: route_context.state must be projected or blocked")
    for key in required - {"blocker_id"}:
        if not route_context[key]:
            raise SourceBridgeError(f"{account_id}: route_context.{key} is required")
    checksum = str(route_context["context_checksum"])
    if not checksum.startswith("sha256:"):
        raise SourceBridgeError(f"{account_id}: route_context.context_checksum must be sha256")

    market_data_source = str(route_context["market_data_source"]).lower()
    execution_adapter = str(route_context["execution_adapter"]).lower()
    account_truth = str(route_context["account_truth"]).lower()
    if "ctp_md.025292" in market_data_source:
        if "ctp_td.025292" in execution_adapter:
            raise SourceBridgeError(f"{account_id}: ctp_md.025292 must not imply ctp_td.025292 execution")
        if account_truth in {"broker_ctp", "ctp_broker_account", "ctp_td.025292"}:
            raise SourceBridgeError(f"{account_id}: ctp_md.025292 must not become broker account truth")
    if any(claim in account_truth for claim in ["paper_ready", "live_ready", "can_trade", "broker_tradable"]):
        raise SourceBridgeError(f"{account_id}: route_context.account_truth must not carry readiness claims")
    if account_id == IB_U3028269_ACCOUNT_ID:
        if route_context["state"] == "projected" and "ib_tws_api_source_package" not in account_truth:
            raise SourceBridgeError(f"{account_id}: ready IB projection must come from TWS API source package")


def load_source_artifact(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "command" in payload:
        raise SourceBridgeError(f"{path}: source artifact must not carry command capability")
    account_id = str(payload.get("account_id", ""))
    is_stage2_simulated = account_id == "simulated-001" and payload.get("account_uid") == "sandbox-paper.simulated-001"
    if not account_id.startswith("acct.") and not is_stage2_simulated:
        raise SourceBridgeError(f"{path}: account_id must be namespace-qualified")
    if is_stage2_simulated:
        if payload.get("stage") != "R1/P079 Stage 2":
            raise SourceBridgeError(f"{path}: simulated-001 must be scoped to R1/P079 Stage 2")
        if payload.get("market_data_role") != "market_data_only":
            raise SourceBridgeError(f"{path}: CTP 025292 must remain market_data_only")
        if payload.get("broker_order_submission") is not False:
            raise SourceBridgeError(f"{path}: broker_order_submission must be false")
        if payload.get("trading_adapter") != "disabled":
            raise SourceBridgeError(f"{path}: trading_adapter must be disabled")
        if payload.get("ledger_type") != "simulated_sandbox_ledger":
            raise SourceBridgeError(f"{path}: ledger_type must be simulated_sandbox_ledger")
    if not payload.get("source_ref") or not str(payload.get("source_checksum", "")).startswith("sha256:"):
        raise SourceBridgeError(f"{path}: source_ref and source_checksum are required")
    if account_id == IB_U3028269_ACCOUNT_ID:
        if payload.get("source_kind") != "ib_tws_observation":
            raise SourceBridgeError(f"{path}: IB U3028269 source_kind must be ib_tws_observation")
        if payload.get("source_health", {}).get("api_transport") != "ib_tws_api":
            raise SourceBridgeError(f"{path}: IB U3028269 source package must be backed by TWS API transport")
        if payload.get("boundaries", {}).get("screenshot_used_for_funds_positions") is not False:
            raise SourceBridgeError(f"{path}: screenshots must not be used for IB funds/positions")
        if payload.get("boundaries", {}).get("raw_secret_values_recorded") is not False:
            raise SourceBridgeError(f"{path}: raw secrets must not be recorded")
        if payload.get("boundaries", {}).get("order_action_sent") is not False:
            raise SourceBridgeError(f"{path}: order action must not be sent by observation source")
    route_context = payload.get("route_context") or _fallback_route_context(payload)
    validate_route_context(route_context, account_id)
    payload["route_context"] = route_context
    return payload


def source_artifact_to_capability_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    route_context = payload.get("route_context") or _fallback_route_context(payload)
    validate_route_context(route_context, str(payload["account_id"]))
    mirror_state = "blocked" if route_context["state"] == "blocked" or payload["source_health"].get("state") == "blocked" else "ready"
    source_ref = {
        "owner": payload["source_owner"],
        "source_ref": payload["source_ref"],
        "checksum": payload["source_checksum"],
        "observed_at": payload["observed_at"],
    }
    return {
        "schema_version": "account_capability_bundle.v1",
        "account": {
            "account_id": payload["account_id"],
            "display_alias": payload["display_alias"],
            "source_kind": payload["source_kind"],
            "source_mode": payload["source_mode"],
            "account_domain": payload["account_domain"],
        },
        "capabilities": {
            "observation": {
                "enabled": True,
                "mirror_state": mirror_state,
                "source_ref": source_ref,
            },
            "command": {
                "enabled": False,
                "mode": "disabled",
                "gateway_kind": None,
                "allowed_actions": [],
                "requires_risk_check": True,
                "requires_approval": True,
                "authority_ref": None,
                "capability_checksum": payload["source_checksum"],
            },
            "reconciliation": {
                "enabled": True,
                "readback_required": True,
            },
            "evidence": {
                "required": True,
                "source_refs_required": True,
                "checksums_required": True,
            },
        },
        "observations": {
            "balances": [_with_provenance(row, payload) for row in payload.get("balances", [])],
            "positions": [_with_provenance(row, payload) for row in payload.get("positions", [])],
            "orders": [_with_provenance(row, payload) for row in payload.get("orders", [])],
            "fills": [_with_provenance(row, payload) for row in payload.get("fills", [])],
            "source_health": _with_provenance(dict(payload["source_health"]), payload),
            "blockers": list(payload.get("blockers", [])),
        },
        "route_context": dict(route_context),
        "boundaries": {
            "read_only_projection": True,
            "broker_truth": False,
            "runtime_truth": False,
            "account_truth": False,
            "order_action": False,
            "approval_truth": False,
            "capital_truth": False,
            "trading_readiness_truth": False,
        },
        "rejection_rules": [
            "Source artifacts are read-only inputs and must not grant command capability.",
            "Account Console backend/UI must not call broker APIs directly.",
            "Mirror projections are not broker, runtime, account, capital or readiness truth.",
        ],
    }


def load_capability_bundles(artifact_dir: Path = DEFAULT_ARTIFACT_DIR) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    for path in sorted(artifact_dir.glob("*.json")):
        if path.name.startswith("invalid_"):
            continue
        if path.name == "ctp_paper_19053_source.json":
            continue
        bundles.append(source_artifact_to_capability_bundle(load_source_artifact(path)))
    bundles.append(load_ctp19053_real_login_bundle())
    bundles.append(load_ctp025292_real_login_bundle())
    bundles.append(load_ib_u3028269_real_login_bundle())
    return bundles


def _with_provenance(row: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(row)
    enriched["source_ref"] = payload["source_ref"]
    enriched["checksum"] = payload["source_checksum"]
    enriched["observed_at"] = payload["observed_at"]
    return enriched


def load_ctp19053_real_login_bundle(source_package: Path = CTP19053_REAL_SOURCE_PACKAGE) -> dict[str, Any]:
    if source_package.exists():
        return source_artifact_to_capability_bundle(load_source_artifact(source_package))

    checksum = "sha256:2222222222222222222222222222222222222222222222222222222222222222"
    source_ref = str(source_package.relative_to(ROOT)).replace("\\", "/")
    route_context = _blocked_route_context(
        account_id=CTP19053_ACCOUNT_ID,
        display_alias="19053",
        source_ref=source_ref,
        checksum=checksum,
        blocker_id="ctp19053_real_login_source_unavailable",
        risk_domain="paper",
    )
    return {
        "schema_version": "account_capability_bundle.v1",
        "account": {
            "account_id": CTP19053_ACCOUNT_ID,
            "display_alias": "19053",
            "source_kind": "ctp_trader_api",
            "source_mode": "paper_observation",
            "account_domain": "paper",
        },
        "capabilities": {
            "observation": {
                "enabled": True,
                "mirror_state": "blocked",
                "source_ref": {
                    "owner": "nautilus_ctp_adapter",
                    "source_ref": source_ref,
                    "checksum": checksum,
                    "observed_at": "2026-06-15T00:00:00Z",
                },
            },
            "command": {
                "enabled": False,
                "mode": "disabled",
                "gateway_kind": None,
                "allowed_actions": [],
                "requires_risk_check": True,
                "requires_approval": True,
                "authority_ref": None,
                "capability_checksum": checksum,
            },
            "reconciliation": {
                "enabled": True,
                "readback_required": True,
            },
            "evidence": {
                "required": True,
                "source_refs_required": True,
                "checksums_required": True,
            },
        },
        "observations": {
            "balances": [],
            "positions": [],
            "orders": [],
            "fills": [],
            "source_health": {
                "state": "blocked",
                "blocker_id": "ctp19053_real_login_source_unavailable",
                "source_ref": source_ref,
                "checksum": checksum,
                "observed_at": "2026-06-15T00:00:00Z",
            },
            "blockers": [
                {
                    "blocker_id": "ctp19053_real_login_source_unavailable",
                    "type": "source_unavailable",
                    "owner": "nautilus_ctp_adapter",
                    "next_action": (
                        "Run read-only real-login CTP 19053 account and position queries, then build "
                        "output/account_capability/ctp-paper-19053/source-package.json."
                    ),
                    "source_ref": source_ref,
                    "checksum": checksum,
                }
            ],
        },
        "route_context": route_context,
        "boundaries": {
            "read_only_projection": True,
            "broker_truth": False,
            "runtime_truth": False,
            "account_truth": False,
            "order_action": False,
            "approval_truth": False,
            "capital_truth": False,
            "trading_readiness_truth": False,
        },
        "rejection_rules": [
            "Do not display CTP 19053 funds or positions from repo-local sample data.",
            "Do not pass UI readback until a real-login source package is present.",
            "Do not infer command capability from CTP paper account domain.",
        ],
    }


def load_ctp025292_real_login_bundle(source_package: Path = CTP025292_REAL_SOURCE_PACKAGE) -> dict[str, Any]:
    if source_package.exists():
        try:
            payload = load_source_artifact(source_package)
            if payload.get("source_kind") != "ctp_trader_api":
                raise SourceBridgeError(f"{source_package}: source_kind must be ctp_trader_api for account readback")
            if payload.get("source_mode") != "live_observation":
                raise SourceBridgeError(f"{source_package}: source_mode must be live_observation for account readback")
            return source_artifact_to_capability_bundle(payload)
        except SourceBridgeError as exc:
            return _blocked_ctp025292_bundle(source_package, package_error=str(exc))

    return _blocked_ctp025292_bundle(source_package)


def _blocked_ctp025292_bundle(source_package: Path, package_error: str | None = None) -> dict[str, Any]:
    checksum = "sha256:3333333333333333333333333333333333333333333333333333333333333333"
    source_ref = str(source_package.relative_to(ROOT)).replace("\\", "/")
    route_context = _blocked_route_context(
        account_id=CTP025292_ACCOUNT_ID,
        display_alias="025292",
        source_ref=source_ref,
        checksum=checksum,
        blocker_id="ctp025292_real_login_source_unavailable",
        risk_domain="live",
    )
    next_action = (
        "Run read-only real-login CTP 025292 account, position and order queries, then build "
        "output/account_capability/ctp-live-025292/source-package.json."
    )
    if package_error:
        next_action = f"Replace invalid 025292 account readback package. {next_action}"
    return {
        "schema_version": "account_capability_bundle.v1",
        "account": {
            "account_id": CTP025292_ACCOUNT_ID,
            "display_alias": "025292",
            "source_kind": "ctp_trader_api",
            "source_mode": "live_observation",
            "account_domain": "live",
        },
        "capabilities": {
            "observation": {
                "enabled": True,
                "mirror_state": "blocked",
                "source_ref": {
                    "owner": "nautilus_ctp_adapter",
                    "source_ref": source_ref,
                    "checksum": checksum,
                    "observed_at": "2026-06-15T00:00:00Z",
                },
            },
            "command": {
                "enabled": False,
                "mode": "disabled",
                "gateway_kind": None,
                "allowed_actions": [],
                "requires_risk_check": True,
                "requires_approval": True,
                "authority_ref": None,
                "capability_checksum": checksum,
            },
            "reconciliation": {
                "enabled": True,
                "readback_required": True,
            },
            "evidence": {
                "required": True,
                "source_refs_required": True,
                "checksums_required": True,
            },
        },
        "observations": {
            "balances": [],
            "positions": [],
            "orders": [],
            "fills": [],
            "source_health": {
                "state": "blocked",
                "blocker_id": "ctp025292_real_login_source_unavailable",
                "source_ref": source_ref,
                "checksum": checksum,
                "observed_at": "2026-06-15T00:00:00Z",
                **({"package_error": package_error} if package_error else {}),
            },
            "blockers": [
                {
                    "blocker_id": "ctp025292_real_login_source_unavailable",
                    "type": "source_unavailable",
                    "owner": "nautilus_ctp_adapter",
                    "next_action": next_action,
                    "source_ref": source_ref,
                    "checksum": checksum,
                    **({"package_error": package_error} if package_error else {}),
                }
            ],
        },
        "route_context": route_context,
        "boundaries": {
            "read_only_projection": True,
            "broker_truth": False,
            "runtime_truth": False,
            "account_truth": False,
            "order_action": False,
            "approval_truth": False,
            "capital_truth": False,
            "trading_readiness_truth": False,
        },
        "rejection_rules": [
            "Do not display CTP 025292 funds or positions from repo-local sample data.",
            "Do not pass UI readback until a real-login source package is present.",
            "Do not infer command capability from CTP live account domain.",
        ],
    }


def load_ib_u3028269_observation_blocker_bundle() -> dict[str, Any]:
    checksum = "sha256:4444444444444444444444444444444444444444444444444444444444444444"
    source_ref = "contracts/broker_observation/fixtures/ib_tws_profile_blocked_adr0005_not_accepted.json"
    route_context = {
        "state": "blocked",
        "route_id": "route.ib.live.u3028269.account-readonly",
        "account_alias": "U3028269",
        "market_data_source": "not_in_scope_for_account_readback",
        "execution_adapter": "ib_tws_observation.blocked_until_adr0005_accepted",
        "account_truth": "blocked_until_adr0005_accepted_and_owner_source_package",
        "risk_domain": "live",
        "evidence_partition": "account/acct.ib.live.u3028269/broker-observation-blocked",
        "context_ref": source_ref,
        "context_checksum": checksum,
        "blocker_id": "adr0005_not_accepted",
    }
    return {
        "schema_version": "account_capability_bundle.v1",
        "account": {
            "account_id": IB_U3028269_ACCOUNT_ID,
            "display_alias": "U3028269",
            "source_kind": "ib_tws_observation",
            "source_mode": "live_observation_blocked",
            "account_domain": "live",
        },
        "capabilities": {
            "observation": {
                "enabled": True,
                "mirror_state": "blocked",
                "source_ref": {
                    "owner": "account-console-broker-observation-session",
                    "source_ref": source_ref,
                    "checksum": checksum,
                    "observed_at": "2026-06-20T00:00:00Z",
                },
            },
            "command": {
                "enabled": False,
                "mode": "disabled",
                "gateway_kind": None,
                "allowed_actions": [],
                "requires_risk_check": True,
                "requires_approval": True,
                "authority_ref": None,
                "capability_checksum": checksum,
            },
            "reconciliation": {
                "enabled": True,
                "readback_required": True,
            },
            "evidence": {
                "required": True,
                "source_refs_required": True,
                "checksums_required": True,
            },
        },
        "observations": {
            "balances": [],
            "positions": [],
            "orders": [],
            "fills": [],
            "source_health": {
                "state": "blocked",
                "blocker_id": "adr0005_not_accepted",
                "source_ref": source_ref,
                "checksum": checksum,
                "observed_at": "2026-06-20T00:00:00Z",
                "account_id": IB_U3028269_ACCOUNT_ID,
                "source_kind": "ib_tws_observation",
                "projection_boundary": "account_mirror",
                "direct_session_allowed": False,
                "raw_secret_values_recorded": False,
            },
            "blockers": [
                {
                    "blocker_id": "adr0005_not_accepted",
                    "type": "architecture_gate",
                    "owner": "architecture",
                    "next_action": (
                        "Accept ADR-0005 and provide owner-produced IB TWS observation source refs before "
                        "opening a direct read-only broker observation session."
                    ),
                    "source_ref": source_ref,
                    "checksum": checksum,
                }
            ],
        },
        "route_context": route_context,
        "boundaries": {
            "read_only_projection": True,
            "broker_truth": False,
            "runtime_truth": False,
            "account_truth": False,
            "order_action": False,
            "approval_truth": False,
            "capital_truth": False,
            "trading_readiness_truth": False,
        },
        "rejection_rules": [
            "Do not open a direct IB TWS observation session while ADR-0005 is proposed.",
            "Do not infer broker truth, readiness or command capability from the blocked Account Mirror projection.",
            "Do not store raw IB username, password, 2FA, host, port, client id or account secrets in this repo.",
        ],
    }


def load_ib_u3028269_real_login_bundle(source_package: Path = IB_U3028269_SOURCE_PACKAGE) -> dict[str, Any]:
    if source_package.exists():
        try:
            payload = load_source_artifact(source_package)
            if payload.get("source_kind") != "ib_tws_observation":
                raise SourceBridgeError(f"{source_package}: source_kind must be ib_tws_observation")
            if payload.get("source_mode") not in {"live_observation", "live_observation_blocked"}:
                raise SourceBridgeError(f"{source_package}: invalid source_mode for IB observation")
            return source_artifact_to_capability_bundle(payload)
        except SourceBridgeError as exc:
            return _blocked_ib_u3028269_bundle(source_package, package_error=str(exc))
    return load_ib_u3028269_observation_blocker_bundle()


def _blocked_ib_u3028269_bundle(source_package: Path, package_error: str | None = None) -> dict[str, Any]:
    bundle = load_ib_u3028269_observation_blocker_bundle()
    source_ref = str(source_package.relative_to(ROOT)).replace("\\", "/")
    checksum = "sha256:5555555555555555555555555555555555555555555555555555555555555555"
    bundle["capabilities"]["observation"]["source_ref"]["source_ref"] = source_ref
    bundle["capabilities"]["observation"]["source_ref"]["checksum"] = checksum
    bundle["capabilities"]["command"]["capability_checksum"] = checksum
    bundle["observations"]["source_health"]["source_ref"] = source_ref
    bundle["observations"]["source_health"]["checksum"] = checksum
    bundle["observations"]["source_health"]["blocker_id"] = "ib_u3028269_tws_api_source_package_invalid"
    bundle["observations"]["source_health"]["package_error"] = package_error
    bundle["observations"]["blockers"][0]["blocker_id"] = "ib_u3028269_tws_api_source_package_invalid"
    bundle["observations"]["blockers"][0]["type"] = "source_invalid"
    bundle["observations"]["blockers"][0]["source_ref"] = source_ref
    bundle["observations"]["blockers"][0]["checksum"] = checksum
    bundle["observations"]["blockers"][0]["package_error"] = package_error
    bundle["observations"]["blockers"][0]["next_action"] = (
        "Regenerate output/account_capability/ib-live-u3028269/source-package.json from read-only TWS API "
        "account_summary.json and positions.json; screenshots cannot satisfy this package."
    )
    bundle["route_context"]["context_ref"] = source_ref
    bundle["route_context"]["context_checksum"] = checksum
    bundle["route_context"]["blocker_id"] = "ib_u3028269_tws_api_source_package_invalid"
    return bundle
