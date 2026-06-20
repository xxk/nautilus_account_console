from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SOURCE_DIR = ROOT / "contracts" / "ui" / "fixtures" / "account_capability"


def _checksum(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(encoded).hexdigest()


def _fallback_route_context_for_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    account = payload["account"]
    account_id = str(account["account_id"])
    source_ref = payload["capabilities"]["observation"]["source_ref"]
    if account_id == "acct.ctp.paper.19053":
        return {
            "state": "blocked",
            "route_id": "route.ctp.paper.19053.account-readonly",
            "account_alias": "19053",
            "market_data_source": "not_in_scope_for_account_readback",
            "execution_adapter": "ctp_td.19053.blocked_until_source_package",
            "account_truth": "blocked_until_pinned_source_package",
            "risk_domain": "paper",
            "evidence_partition": "account/acct.ctp.paper.19053/blocked-source-package",
            "context_ref": source_ref["source_ref"],
            "context_checksum": source_ref["checksum"],
            "blocker_id": "ctp19053_source_package_pending",
        }
    if account_id == "acct.ctp.live.025292":
        return {
            "state": "blocked",
            "route_id": "route.ctp.live.025292.account-readonly",
            "account_alias": "025292",
            "market_data_source": "not_in_scope_for_account_readback",
            "execution_adapter": "ctp_td.025292.blocked_until_source_package",
            "account_truth": "blocked_until_pinned_source_package",
            "risk_domain": "live",
            "evidence_partition": "account/acct.ctp.live.025292/blocked-source-package",
            "context_ref": source_ref["source_ref"],
            "context_checksum": source_ref["checksum"],
            "blocker_id": "ctp025292_source_package_pending",
        }
    return {
        "state": "projected",
        "route_id": f"route.{account_id.removeprefix('acct.')}.readonly",
        "account_alias": str(account["display_alias"]),
        "market_data_source": "not_in_scope_for_account_readback",
        "execution_adapter": str(account["source_kind"]),
        "account_truth": str(source_ref["owner"]),
        "risk_domain": str(account["account_domain"]),
        "evidence_partition": f"account/{account_id}/source-package",
        "context_ref": source_ref["source_ref"],
        "context_checksum": source_ref["checksum"],
        "blocker_id": None,
    }


@dataclass(frozen=True)
class MirrorProjection:
    account_id: str
    display_alias: str
    source_kind: str
    source_mode: str
    account_domain: str
    observation_enabled: bool
    command_enabled: bool
    command_mode: str
    mirror_state: str
    balances: list[dict[str, Any]]
    positions: list[dict[str, Any]]
    orders: list[dict[str, Any]]
    fills: list[dict[str, Any]]
    source_health: dict[str, Any]
    blockers: list[dict[str, Any]]
    projection_checkpoint_id: str
    projection_checksum: str
    source_ref: str
    source_checksum: str
    route_context: dict[str, Any]
    boundaries: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "account_mirror_projection.v1",
            "account_id": self.account_id,
            "display_alias": self.display_alias,
            "source_kind": self.source_kind,
            "source_mode": self.source_mode,
            "account_domain": self.account_domain,
            "capabilities": {
                "observation": {
                    "enabled": self.observation_enabled,
                    "mirror_state": self.mirror_state,
                },
                "command": {
                    "enabled": self.command_enabled,
                    "mode": self.command_mode,
                },
            },
            "balances": self.balances,
            "positions": self.positions,
            "orders": self.orders,
            "fills": self.fills,
            "source_health": self.source_health,
            "blockers": self.blockers,
            "projection_checkpoint_id": self.projection_checkpoint_id,
            "projection_checksum": self.projection_checksum,
            "source_ref": self.source_ref,
            "source_checksum": self.source_checksum,
            "route_context": self.route_context,
            "boundaries": self.boundaries,
        }


class AccountMirrorStore:
    def __init__(self, source_dir: Path = DEFAULT_SOURCE_DIR) -> None:
        self.source_dir = source_dir

    def list_source_paths(self) -> list[Path]:
        return sorted(
            path
            for path in self.source_dir.glob("*.json")
            if not path.name.startswith("invalid_")
        )

    def list_projections(self) -> list[MirrorProjection]:
        return [self.project_source(path) for path in self.list_source_paths()]

    def list_projections_from_bundles(self, bundles: list[dict[str, Any]]) -> list[MirrorProjection]:
        return [self.project_bundle(bundle, f"bundle://{idx}") for idx, bundle in enumerate(bundles)]

    def get_projection(self, account_id: str) -> MirrorProjection | None:
        for projection in self.list_projections():
            if projection.account_id == account_id:
                return projection
        return None

    def project_source(self, path: Path) -> MirrorProjection:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return self.project_bundle(payload, path.as_posix())

    def project_bundle(self, payload: dict[str, Any], source_path: str) -> MirrorProjection:
        account = payload["account"]
        capabilities = payload["capabilities"]
        observations = payload["observations"]
        source_ref = capabilities["observation"]["source_ref"]
        route_context = payload.get("route_context") or _fallback_route_context_for_bundle(payload)
        checkpoint_seed = {
            "account": account,
            "capabilities": capabilities,
            "observations": observations,
            "route_context": route_context,
            "source_path": source_path,
        }
        checkpoint_id = _checksum({"checkpoint": checkpoint_seed})
        projection_payload = {
            "schema_version": "account_mirror_projection.v1",
            "account_id": account["account_id"],
            "source_checksum": source_ref["checksum"],
            "checkpoint_id": checkpoint_id,
            "observations": observations,
            "route_context": route_context,
            "boundaries": payload["boundaries"],
        }
        projection_checksum = _checksum(projection_payload)
        return MirrorProjection(
            account_id=account["account_id"],
            display_alias=account["display_alias"],
            source_kind=account["source_kind"],
            source_mode=account["source_mode"],
            account_domain=account["account_domain"],
            observation_enabled=capabilities["observation"]["enabled"],
            command_enabled=capabilities["command"]["enabled"],
            command_mode=capabilities["command"]["mode"],
            mirror_state=capabilities["observation"]["mirror_state"],
            balances=list(observations["balances"]),
            positions=list(observations["positions"]),
            orders=list(observations["orders"]),
            fills=list(observations["fills"]),
            source_health=dict(observations["source_health"]),
            blockers=list(observations["blockers"]),
            projection_checkpoint_id=checkpoint_id,
            projection_checksum=projection_checksum,
            source_ref=source_ref["source_ref"],
            source_checksum=source_ref["checksum"],
            route_context=dict(route_context),
            boundaries=dict(payload["boundaries"]),
        )
