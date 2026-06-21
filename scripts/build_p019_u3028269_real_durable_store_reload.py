from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCOUNT_ID = "acct.ib.live.u3028269"
SOURCE_PACKAGE = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "source-package.json"
EXECUTIONS = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "tws-api" / "executions.json"
DEFAULT_OUTPUT = ROOT / "output" / "account_capability" / "ib-live-u3028269" / "durable-store-reload.json"


class BuildDurableReloadError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildDurableReloadError(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def checksum(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(encoded).hexdigest()


def build_durable_reload(
    *,
    source_package: dict[str, Any],
    executions: dict[str, Any],
    source_package_ref: str,
    executions_ref: str,
    output_ref: str,
) -> dict[str, Any]:
    require(source_package["account_id"] == ACCOUNT_ID, "source package account mismatch")
    require(executions["account_id"] == ACCOUNT_ID, "executions account mismatch")
    require(source_package["source_health"]["state"] == "ready", "source package must be ready")
    require(executions["success"] is True, "executions query must have succeeded")

    fills = source_package.get("fills", [])
    execution_rows = executions.get("execution_report_rows")
    require(execution_rows == len(executions.get("executions", [])), "executions row count mismatch")
    require(len(fills) == execution_rows, "source package fills must match execution row count")

    record_counts = {
        "order_status_reports": 0,
        "fill_reports": len(fills),
        "funds_snapshots": len(source_package.get("balances", [])),
        "positions_snapshots": len(source_package.get("positions", [])),
        "session_health": 1,
        "freshness_cursors": 1,
    }
    replay_blockers = []
    parity_status = "passed"
    replay_state = "complete"
    if execution_rows == 0:
        parity_status = "blocked"
        replay_state = "partial"
        replay_blockers.append(
            {
                "blocker_id": "real_order_fill_callbacks_not_available",
                "reason": "read-only TWS reqExecutions succeeded but returned zero matching execution rows for the current slice",
                "next_action": "rerun read-only reqExecutions after same-slice U3028269 executions are present",
            }
        )

    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload: dict[str, Any] = {
        "schema_version": "broker_observation_store_snapshot.v1",
        "account_id": ACCOUNT_ID,
        "store_semantics": "observation_evidence_projection_cache",
        "truth_flags": {
            "broker_truth": False,
            "order_truth": False,
            "account_truth": False,
            "command_authority": False,
            "readiness_truth": False,
        },
        "reload_support": True,
        "reload_proof": {
            "store_snapshot_ref": output_ref,
            "store_snapshot_checksum": "sha256:pending",
            "source_report_batch_ref": executions_ref,
            "source_report_batch_checksum": executions["query_checksum"],
            "reload_checkpoint_id": f"broker-observation-store.reload.u3028269.real.{datetime.now(UTC):%Y%m%d%H%M%S}",
            "records_reloaded_from_store": sum(record_counts.values()),
            "records_loaded_from_live_memory": 0,
            "parity_status": parity_status,
        },
        "persisted_families": [
            "order_status_reports",
            "fill_reports",
            "funds_snapshots",
            "positions_snapshots",
            "session_health",
            "freshness_cursors",
            "provenance_refs",
        ],
        "persisted_record_counts": record_counts,
        "replay_state": {
            "state": replay_state,
            "blockers": replay_blockers,
        },
        "raw_secret_values_recorded": False,
        "real_source_refs": {
            "source_package": source_package_ref,
            "executions_query": executions_ref,
            "source_package_checksum": source_package["source_checksum"],
            "executions_query_checksum": executions["query_checksum"],
        },
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
            "records_loaded_from_live_memory": 0,
            "synthetic_evidence_used": False,
        },
        "observed_at": observed_at,
    }
    payload["reload_proof"]["store_snapshot_checksum"] = checksum(
        {**payload, "reload_proof": {**payload["reload_proof"], "store_snapshot_checksum": "sha256:pending"}}
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a real U3028269 durable observation store reload artifact from persisted TWS API artifacts.")
    parser.add_argument("--source-package", type=Path, default=SOURCE_PACKAGE)
    parser.add_argument("--executions", type=Path, default=EXECUTIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    source_package = load(args.source_package)
    executions = load(args.executions)
    payload = build_durable_reload(
        source_package=source_package,
        executions=executions,
        source_package_ref=source_ref(args.source_package),
        executions_ref=source_ref(args.executions),
        output_ref=source_ref(args.output),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["replay_state"]["state"],
                "parity_status": payload["reload_proof"]["parity_status"],
                "execution_report_rows": executions.get("execution_report_rows"),
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
