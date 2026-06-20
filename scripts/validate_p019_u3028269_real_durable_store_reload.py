from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
BUILDER = ROOT / "scripts" / "build_p019_u3028269_real_durable_store_reload.py"
ACCEPTANCE = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "acceptance.md"
PHASE_PLAN = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "phase-plan.md"
AUDIT = ROOT / "docs" / "proposals" / "p019-broker-observation-session-foundation" / "p019-completion-audit.json"


class RealDurableReloadError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RealDurableReloadError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def walk(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(walk(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(walk(item))
    return values


def import_builder():
    spec = importlib.util.spec_from_file_location("p019_real_durable_reload_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "builder module spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_synthetic_complete_reload_path(builder_module: Any) -> None:
    source_package = {
        "account_id": "acct.ib.live.u3028269",
        "source_checksum": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
        "source_health": {"state": "ready"},
        "balances": [{"currency": "USD"}],
        "positions": [{"instrument": "MSFT"}],
        "fills": [
            {
                "nautilus_report_type": "FillReport",
                "trade_id": "SYNTH-EXEC-0001",
                "source_checksum": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
            }
        ],
    }
    executions = {
        "account_id": "acct.ib.live.u3028269",
        "success": True,
        "query_checksum": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
        "execution_report_rows": 1,
        "executions": [{"exec_id": "SYNTH-EXEC-0001"}],
    }
    payload = builder_module.build_durable_reload(
        source_package=source_package,
        executions=executions,
        source_package_ref="synthetic/source-package.json",
        executions_ref="synthetic/executions.json",
        output_ref="synthetic/durable-store-reload.json",
    )
    require(payload["replay_state"]["state"] == "complete", "synthetic non-empty reload should be complete")
    require(payload["reload_proof"]["parity_status"] == "passed", "synthetic non-empty reload should pass parity")
    require(payload["persisted_record_counts"]["fill_reports"] == 1, "synthetic fill report count mismatch")
    require(payload["reload_proof"]["records_loaded_from_live_memory"] == 0, "synthetic reload used live memory")
    require(payload["boundaries"]["synthetic_evidence_used"] is False, "builder must not mark synthetic as real evidence")


def main() -> None:
    payload = load(ARTIFACT)
    source_package = load(SOURCE_PACKAGE)
    executions = load(EXECUTIONS)
    builder = read(BUILDER)
    acceptance = read(ACCEPTANCE)
    phase_plan = read(PHASE_PLAN)
    audit = load(AUDIT)
    builder_module = import_builder()

    require(payload["schema_version"] == "broker_observation_store_snapshot.v1", "schema mismatch")
    require(payload["account_id"] == "acct.ib.live.u3028269", "account mismatch")
    require(payload["store_semantics"] == "observation_evidence_projection_cache", "store semantics mismatch")
    require(payload["raw_secret_values_recorded"] is False, "raw secrets recorded")
    for key, value in payload["truth_flags"].items():
        require(value is False, f"truth flag {key} must remain false")
    boundaries = payload["boundaries"]
    for key in [
        "raw_secret_values_recorded",
        "raw_broker_endpoint_recorded",
        "screenshot_used_for_funds_positions",
        "order_action_sent",
        "synthetic_evidence_used",
    ]:
        require(boundaries[key] is False, f"boundary {key} must remain false")
    require(boundaries["records_loaded_from_live_memory"] == 0, "reload must not use live memory")

    reload_proof = payload["reload_proof"]
    require(reload_proof["records_loaded_from_live_memory"] == 0, "reload proof used live memory")
    require(reload_proof["store_snapshot_ref"] == "output/account_capability/ib-live-u3028269/durable-store-reload.json", "store snapshot ref mismatch")
    require(reload_proof["source_report_batch_ref"] == "output/account_capability/ib-live-u3028269/tws-api/executions.json", "source report ref mismatch")
    require(reload_proof["source_report_batch_checksum"] == executions["query_checksum"], "executions checksum mismatch")
    require(str(reload_proof["store_snapshot_checksum"]).startswith("sha256:"), "store checksum missing")

    counts = payload["persisted_record_counts"]
    require(counts["funds_snapshots"] == len(source_package["balances"]), "funds snapshot count mismatch")
    require(counts["positions_snapshots"] == len(source_package["positions"]), "positions snapshot count mismatch")
    require(counts["fill_reports"] == len(source_package["fills"]), "fill report count mismatch")
    require(counts["order_status_reports"] == 0, "real U3028269 has no order status rows in current slice")
    require(counts["session_health"] == 1, "session health count mismatch")
    require(counts["freshness_cursors"] == 1, "freshness cursor count mismatch")
    require(reload_proof["records_reloaded_from_store"] == sum(counts.values()), "reload count mismatch")

    require(source_package["source_health"]["executions_query_success"] is True, "source package missing executions success")
    require(executions["success"] is True, "executions query must succeed")
    require(executions["execution_report_rows"] == len(executions["executions"]), "execution row count mismatch")
    if executions["execution_report_rows"] == 0:
        require(payload["replay_state"]["state"] == "partial", "zero executions must keep replay partial")
        require(reload_proof["parity_status"] == "blocked", "zero executions must keep report parity blocked")
        require(payload["replay_state"]["blockers"], "zero executions must carry blocker")
        require(payload["replay_state"]["blockers"][0]["blocker_id"] == "real_order_fill_callbacks_not_available", "blocker mismatch")
    else:
        require(payload["replay_state"]["state"] == "complete", "non-empty executions should be complete")
        require(reload_proof["parity_status"] == "passed", "non-empty executions should pass reload parity")

    refs = payload["real_source_refs"]
    require(refs["source_package"] == "output/account_capability/ib-live-u3028269/source-package.json", "source package ref mismatch")
    require(refs["executions_query"] == "output/account_capability/ib-live-u3028269/tws-api/executions.json", "executions ref mismatch")
    require(refs["source_package_checksum"] == source_package["source_checksum"], "source package checksum mismatch")
    require(refs["executions_query_checksum"] == executions["query_checksum"], "executions query checksum mismatch")

    forbidden_fragments = ["password=", "auth_code=", "api_key=", "secret=", "placeOrder", "cancelOrder", "127.0.0.1:"]
    for value in walk(payload):
        if isinstance(value, str):
            lowered = value.lower()
            hits = [fragment for fragment in forbidden_fragments if fragment.lower() in lowered]
            require(not hits, f"forbidden fragment {hits} in durable reload artifact")

    for term in [
        "records_loaded_from_live_memory",
        "synthetic_evidence_used",
        "build_durable_reload",
    ]:
        require(term in builder, f"builder missing guard term {term}")
    for term in [
        "validate_p019_u3028269_real_durable_store_reload.py",
        "P019_U3028269_REAL_DURABLE_STORE_RELOAD_OK",
    ]:
        require(term in acceptance, f"acceptance missing {term}")
        require(term in phase_plan, f"phase plan missing {term}")

    blockers = {item["blocker_id"]: item for item in audit["blocking_conditions"]}
    require("real_durable_store_reload_not_implemented" not in blockers, "audit still claims real durable reload is not implemented")
    require("real_durable_store_reload_partial_empty_executions" in blockers, "audit missing real durable reload partial blocker")
    require_synthetic_complete_reload_path(builder_module)

    print(
        "P019_U3028269_REAL_DURABLE_STORE_RELOAD_OK: "
        f"state={payload['replay_state']['state']} parity={reload_proof['parity_status']} "
        f"records={reload_proof['records_reloaded_from_store']} synthetic_complete=pass"
    )


if __name__ == "__main__":
    main()
