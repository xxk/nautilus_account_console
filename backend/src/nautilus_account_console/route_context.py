from __future__ import annotations

from typing import Any


IB_U3028269_ACCOUNT_ID = "acct.ib.live.u3028269"


class RouteContextError(ValueError):
    pass


def route_context_from_source_artifact(payload: dict[str, Any]) -> dict[str, Any]:
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


def route_context_from_capability_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    account = payload["account"]
    source_ref = payload["capabilities"]["observation"]["source_ref"]
    source_payload = {
        "account_id": account["account_id"],
        "display_alias": account["display_alias"],
        "source_kind": account["source_kind"],
        "source_mode": account["source_mode"],
        "source_owner": source_ref["owner"],
        "source_ref": source_ref["source_ref"],
        "source_checksum": source_ref["checksum"],
        "account_domain": account["account_domain"],
    }
    return route_context_from_source_artifact(source_payload)


def blocked_route_context(
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
        raise RouteContextError(f"{account_id}: route_context missing fields {missing}")
    if route_context["state"] not in {"projected", "blocked"}:
        raise RouteContextError(f"{account_id}: route_context.state must be projected or blocked")
    for key in required - {"blocker_id"}:
        if not route_context[key]:
            raise RouteContextError(f"{account_id}: route_context.{key} is required")
    checksum = str(route_context["context_checksum"])
    if not checksum.startswith("sha256:"):
        raise RouteContextError(f"{account_id}: route_context.context_checksum must be sha256")

    market_data_source = str(route_context["market_data_source"]).lower()
    execution_adapter = str(route_context["execution_adapter"]).lower()
    account_truth = str(route_context["account_truth"]).lower()
    if "ctp_md.025292" in market_data_source:
        if "ctp_td.025292" in execution_adapter:
            raise RouteContextError(f"{account_id}: ctp_md.025292 must not imply ctp_td.025292 execution")
        if account_truth in {"broker_ctp", "ctp_broker_account", "ctp_td.025292"}:
            raise RouteContextError(f"{account_id}: ctp_md.025292 must not become broker account truth")
    if any(claim in account_truth for claim in ["paper_ready", "live_ready", "can_trade", "broker_tradable"]):
        raise RouteContextError(f"{account_id}: route_context.account_truth must not carry readiness claims")
    if account_id == IB_U3028269_ACCOUNT_ID:
        if route_context["state"] == "projected" and "ib_tws_api_source_package" not in account_truth:
            raise RouteContextError(f"{account_id}: ready IB projection must come from TWS API source package")
