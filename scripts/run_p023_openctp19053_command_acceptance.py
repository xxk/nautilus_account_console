from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKTREE_ROOT = ROOT.parent
WORKTREE_ADAPTER = WORKTREE_ROOT / "nautilus_ctp_adapter"
OWNER_ADAPTER = Path("D:/Nautilus/nautilus_ctp_adapter")
OWNER_SRC = OWNER_ADAPTER / "src"
OWNER_CONFIG = OWNER_ADAPTER / "cfgs" / "local" / "ctp.openctp.tts.7x24.local.json"
QUERY_SCRIPT = WORKTREE_ADAPTER / "scripts" / "ctp_order_trade_query_smoke.py"
NATIVE_DLL = WORKTREE_ADAPTER / "rust" / "target" / "release" / "ctp_native.dll"
VENDOR_BIN = OWNER_ADAPTER / "vendor" / "ctp" / "bin"
ACCOUNT_ID = "acct.ctp.paper.19053"
OPERATOR_REF = "operator-ref://local-codex/p023"


if str(OWNER_SRC) not in sys.path:
    sys.path.insert(0, str(OWNER_SRC))

from nautilus_ctp_adapter.adapters.ctp.config import CtpAdapterConfig
from nautilus_ctp_adapter.adapters.ctp.factory import build_ctp_stack
from nautilus_ctp_adapter.native.pyo3_runtime import create_td_live_session


class P023RuntimeError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_id() -> str:
    return ("p023-openctp19053-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")).lower()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_checksum(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def file_checksum(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload.setdefault("checksum", payload_checksum({k: v for k, v in payload.items() if k != "checksum"}))
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return file_checksum(path)


def source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def fingerprint(value: str | None) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def sensitive_matches(path: Path) -> list[str]:
    fragments = ["tcp://", "trading.openctp", "Password", "AuthCode", "BrokerID", "UserID"]
    matches: list[str] = []
    for file in sorted(path.rglob("*")):
        if not file.is_file():
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        if any(fragment.lower() in text.lower() for fragment in fragments):
            matches.append(source_ref(file))
    return matches


def require_worktree_path(path: Path) -> None:
    resolved = path.resolve()
    root = WORKTREE_ROOT.resolve()
    if not str(resolved).lower().startswith(str(root).lower()):
        raise P023RuntimeError(f"refusing to write outside worktree: {resolved}")


def validate_preflight(preflight: dict[str, Any], *, instrument: str, direction: str, quantity: int) -> dict[str, Any]:
    issues: list[str] = []
    if preflight.get("baseline") != "ctp-paper-readonly-snapshot-v1":
        issues.append("preflight_baseline_mismatch")
    if preflight.get("success") is not True:
        issues.append("preflight_not_success")
    schema = preflight.get("schema") or {}
    if schema.get("account_profile") != "openctp-tts-7x24-simulation":
        issues.append("preflight_account_profile_mismatch")
    if schema.get("reconciliation_role") != "pre_or_post_order_snapshot":
        issues.append("preflight_reconciliation_role_mismatch")
    records = ((preflight.get("positions") or {}).get("records") or [])
    matching = [
        row
        for row in records
        if str(row.get("venue_symbol") or "").strip() == instrument
        and str(row.get("direction") or "").strip().upper() == direction.upper()
    ]
    qty = sum(max(int(row.get("position_qty") or 0), 0) for row in matching)
    yd_qty = sum(max(int(row.get("yd_position_qty") or 0), 0) for row in matching)
    if qty < quantity:
        issues.append("insufficient_position_qty")
    if yd_qty < quantity:
        issues.append("insufficient_yesterday_position_qty")
    exchange = next((row.get("exchange_id") for row in matching if row.get("exchange_id")), None)
    return {
        "accepted": not issues,
        "issues": issues,
        "instrument": instrument,
        "direction": direction.upper(),
        "position_qty": qty,
        "yd_position_qty": yd_qty,
        "exchange": exchange,
        "preflight_run_id": schema.get("run_id"),
    }


def guardrail_shape(config: CtpAdapterConfig) -> dict[str, Any]:
    guardrails = config.execution_guardrails
    return {
        "config_ref": "owner://nautilus_ctp_adapter/cfgs/local/ctp.openctp.tts.7x24.local.json",
        "user_id_fingerprint": fingerprint(config.user_id),
        "allowed_instruments": list(guardrails.allowed_instruments),
        "guardrails_enabled": guardrails.enabled,
        "allow_live_order_smoke": guardrails.allow_live_order_smoke,
        "allow_exposure_reduction_order_smoke": guardrails.allow_exposure_reduction_order_smoke,
        "max_order_qty": guardrails.max_order_qty,
        "max_net_position": guardrails.max_net_position,
        "max_submit_per_minute": guardrails.max_submit_per_minute,
        "price_mode": guardrails.price_mode,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }


def build_risk_decision(
    *,
    status: str,
    intent_ref: str,
    preflight_verdict: dict[str, Any],
    guardrails: dict[str, Any],
    projected_net_position: int,
) -> dict[str, Any]:
    return {
        "schema_version": "account_command.risk_decision.v1",
        "account_id": ACCOUNT_ID,
        "status": status,
        "source_ref": intent_ref,
        "mode": "paper_armed",
        "preflight": preflight_verdict,
        "guardrails": guardrails,
        "projected_net_position": projected_net_position,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "gateway_ack_is_final_state": False,
    }


def build_approval_decision(*, status: str, risk_ref: str) -> dict[str, Any]:
    return {
        "schema_version": "account_command.approval_decision.v1",
        "account_id": ACCOUNT_ID,
        "status": status,
        "source_ref": risk_ref,
        "mode": "paper_armed",
        "approval_scope": "OpenCTP 19053 paper exposure-reduction command smoke",
        "operator_ref": OPERATOR_REF,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "gateway_ack_is_final_state": False,
    }


def serialize_matched_exec(item: Any) -> dict[str, Any]:
    fields = [
        "python_client_order_id",
        "native_order_id",
        "native_order_ref",
        "venue_symbol",
        "front_id",
        "session_id",
        "status",
        "is_trade",
        "trade_volume",
        "leaves_qty",
        "match_reason",
    ]
    return {field: getattr(item, field, None) for field in fields}


def run_readback_query(*, config_path: Path, flow_path: Path, output_json: Path) -> dict[str, Any]:
    require_worktree_path(flow_path)
    require_worktree_path(output_json)
    command = [
        sys.executable,
        str(QUERY_SCRIPT),
        "--config",
        str(config_path),
        "--native-dll",
        str(NATIVE_DLL),
        "--vendor-bin",
        str(VENDOR_BIN),
        "--flow-path",
        str(flow_path),
        "--output-json",
        str(output_json),
        "--timeout-seconds",
        "30",
        "--query-timeout-seconds",
        "12",
        "--quiet-seconds",
        "1",
    ]
    result = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, timeout=60)
    if output_json.exists():
        payload = read_json(output_json)
    else:
        payload = {
            "schema": "account-console.openctp-order-trade-query.v1",
            "success": False,
            "failure_reason": "query_output_missing",
        }
    payload["p023_query_invocation"] = {
        "returncode": result.returncode,
        "script_ref": source_ref(QUERY_SCRIPT),
        "stdout_json_used_as_truth": False,
    }
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def find_order(readback: dict[str, Any], *, instrument: str, order_ref: str) -> dict[str, Any] | None:
    for row in readback.get("orders") or []:
        if str(row.get("symbol") or "") != instrument:
            continue
        if str(row.get("order_ref") or row.get("order_id") or "") == str(order_ref):
            return row
    return None


def order_is_cancelled(row: dict[str, Any] | None) -> bool:
    if row is None:
        return False
    status = str(row.get("status") or "")
    text = str(row.get("error_msg") or "")
    return status == "5" or "撤" in text or text.lower() in {"cancelled", "canceled"}


def order_is_working(row: dict[str, Any] | None) -> bool:
    if row is None:
        return False
    leaves = int(row.get("leaves_qty") or 0)
    return leaves > 0 and not order_is_cancelled(row)


def run_native_cancel(
    *,
    config: CtpAdapterConfig,
    instrument: str,
    exchange: str,
    order_ref: int,
    front_id: int,
    session_id: int,
    flow_path: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    require_worktree_path(flow_path)
    flow_path.mkdir(parents=True, exist_ok=True)
    state: dict[str, Any] = {"login": None, "disconnects": [], "events": []}
    session = create_td_live_session(flow_path)
    try:
        session.set_login_callback(lambda resp: state.__setitem__("login", resp))
        session.set_front_disconnected_callback(lambda reason: state["disconnects"].append(int(reason)))
        session.set_exec_callback(lambda event: state["events"].append(event))
        init_code = session.init(config.td_front)
        auth_code = session.authenticate(config.app_id, config.auth_code, config.product_info)
        login_code = session.login(config.broker_id, config.user_id, config.password)
        deadline = time.time() + timeout_seconds
        while time.time() < deadline and state["login"] is None:
            time.sleep(0.1)
        login = state["login"]
        if login is None or not getattr(login, "success", False):
            return {
                "accepted": False,
                "failure_reason": "cancel_login_failed",
                "init_code": init_code,
                "authenticate_code": auth_code,
                "login_code": login_code,
                "login_error_id": None if login is None else getattr(login, "error_id", None),
                "raw_secret_values_recorded": False,
                "raw_broker_endpoint_recorded": False,
            }
        settlement_code = session.confirm_settlement()
        if settlement_code != 0:
            return {
                "accepted": False,
                "failure_reason": "cancel_settlement_failed",
                "settlement_code": settlement_code,
                "raw_secret_values_recorded": False,
                "raw_broker_endpoint_recorded": False,
            }
        native_code = session.order_action(
            config.broker_id,
            config.user_id,
            instrument,
            str(order_ref),
            front_id,
            session_id,
            exchange,
            "",
            0,
        )
        time.sleep(2.0)
        return {
            "accepted": native_code == 0,
            "failure_reason": None if native_code == 0 else "native_cancel_action_failed",
            "native_code": native_code,
            "disconnect_count": len(state["disconnects"]),
            "observed_event_count": len(state["events"]),
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
        }
    finally:
        session.dispose()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run P023 OpenCTP 19053 paper command acceptance.")
    parser.add_argument("--config", type=Path, default=OWNER_CONFIG)
    parser.add_argument("--preflight-readback", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--instrument", default="rb2610")
    parser.add_argument("--exchange", default="SHFE")
    parser.add_argument("--side", default="SELL")
    parser.add_argument("--quantity", type=int, default=1)
    parser.add_argument("--limit-price", type=float, required=True)
    parser.add_argument("--position-effect", default="CLOSEYESTERDAY")
    parser.add_argument("--time-in-force", default="GFD")
    parser.add_argument("--client-order-id", default=None)
    parser.add_argument("--arm-paper-send", action="store_true")
    parser.add_argument("--arm-cancel-send", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=25)
    args = parser.parse_args(argv)

    effective_run_id = run_id()
    output_dir = args.output_dir or (ROOT / "output" / "account_command" / "ctp-paper-19053" / effective_run_id)
    require_worktree_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    client_order_id = args.client_order_id or f"{effective_run_id}-close-001"
    preflight_path = args.preflight_readback.resolve()
    preflight = read_json(preflight_path)
    preflight_verdict = validate_preflight(
        preflight,
        instrument=args.instrument,
        direction="LONG" if args.side.upper() == "SELL" else "SHORT",
        quantity=args.quantity,
    )
    config = CtpAdapterConfig.from_json_file(args.config)
    guardrails = guardrail_shape(config)
    projected_net_position = int(preflight_verdict.get("position_qty") or 0) - args.quantity
    mode = "paper_armed" if args.arm_paper_send and args.arm_cancel_send else "live_dry_run"

    submit_intent = {
        "schema_version": "account_command.order_intent.v1",
        "intent_id": f"intent.ctp19053.{client_order_id}.submit",
        "account_id": ACCOUNT_ID,
        "mode": mode,
        "action": "submit",
        "instrument": args.instrument,
        "exchange": args.exchange,
        "side": args.side.upper(),
        "quantity": args.quantity,
        "order_type": "LIMIT",
        "limit_price": args.limit_price,
        "time_in_force": args.time_in_force.upper(),
        "offset": args.position_effect.upper(),
        "idempotency_key": client_order_id,
        "operator_ref": OPERATOR_REF,
        "preflight_ref": source_ref(preflight_path),
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    submit_intent_checksum = write_json(output_dir / "submit_intent.json", submit_intent)

    risk_status = "approved" if preflight_verdict["accepted"] else "blocked"
    submit_risk = build_risk_decision(
        status=risk_status,
        intent_ref=source_ref(output_dir / "submit_intent.json"),
        preflight_verdict=preflight_verdict,
        guardrails=guardrails,
        projected_net_position=projected_net_position,
    )
    write_json(output_dir / "submit_risk_decision.json", submit_risk)
    submit_approval = build_approval_decision(
        status="approved" if risk_status == "approved" else "blocked",
        risk_ref=source_ref(output_dir / "submit_risk_decision.json"),
    )
    write_json(output_dir / "submit_approval_decision.json", submit_approval)

    submit_gateway: dict[str, Any] = {
        "schema_version": "account_command.execution_event.v1",
        "account_id": ACCOUNT_ID,
        "status": "blocked",
        "source_ref": source_ref(output_dir / "submit_intent.json"),
        "mode": mode,
        "paper_send_armed": args.arm_paper_send,
        "gateway_ack_is_final_state": False,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    mapped_order_ref: int | None = None
    mapped_front_id: int | None = None
    mapped_session_id: int | None = None
    try:
        if submit_approval["status"] != "approved":
            raise P023RuntimeError("submit approval blocked")
        stack = build_ctp_stack(config)
        execution_client = stack["execution_client"]
        runtime_bridge = stack["runtime_bridge"]
        result = execution_client.run_order_lifecycle_smoke_baseline(
            instrument_id=args.instrument,
            side=args.side.upper(),
            quantity=args.quantity,
            limit_price=args.limit_price,
            position_effect=args.position_effect.upper(),
            client_order_id=client_order_id,
            timeout_seconds=args.timeout_seconds,
            flow_path=output_dir / "submit_flow",
            dry_run=not args.arm_paper_send,
            time_in_force=args.time_in_force.upper(),
            order_type="LIMIT",
            verified_exposure_reduction=True,
        )
        commands = runtime_bridge.drain_submitted_commands()
        events = runtime_bridge.drain_events()
        mapped_order_ref = result.mapped_submit.order_ref
        mapped_front_id = result.mapped_submit.front_id
        mapped_session_id = result.mapped_submit.session_id
        submit_gateway.update(
            {
                "status": "accepted" if result.mapped_submit.error is None else "blocked",
                "live_send_armed": result.live_send_armed,
                "bootstrap_ready": result.bootstrap.ready,
                "mapped_submit_error": None
                if result.mapped_submit.error is None
                else {
                    "error_id": result.mapped_submit.error.error_id,
                    "error_message": result.mapped_submit.error.error_message,
                },
                "client_order_id": client_order_id,
                "order_ref": mapped_order_ref,
                "front_id": mapped_front_id,
                "session_id": mapped_session_id,
                "command_kinds": [command.kind.value for command in commands],
                "event_kinds": [event.kind.value for event in events],
                "matched_execs": [serialize_matched_exec(item) for item in (result.matched_execs or [])],
            }
        )
    except Exception as exc:
        submit_gateway.update(
            {
                "status": "blocked",
                "failure_reason": "submit_gateway_exception",
                "exception": {"type": type(exc).__name__, "message": str(exc)},
            }
        )
    write_json(output_dir / "submit_gateway_event.json", submit_gateway)

    post_submit = run_readback_query(
        config_path=args.config,
        flow_path=output_dir / "post_submit_query_flow",
        output_json=output_dir / "post_submit_readback.json",
    )
    submit_readback_order = None
    if mapped_order_ref is not None:
        submit_readback_order = find_order(post_submit, instrument=args.instrument, order_ref=str(mapped_order_ref))

    cancel_status = "blocked"
    cancel_intent: dict[str, Any] = {
        "schema_version": "account_command.cancel_intent.v1",
        "intent_id": f"intent.ctp19053.{client_order_id}.cancel",
        "account_id": ACCOUNT_ID,
        "mode": mode,
        "action": "cancel",
        "instrument": args.instrument,
        "exchange": args.exchange,
        "client_order_id": client_order_id,
        "venue_order_id": str((submit_readback_order or {}).get("order_id") or mapped_order_ref or ""),
        "order_ref": str(mapped_order_ref or ""),
        "front_id": int(mapped_front_id or 0),
        "session_id": int(mapped_session_id or 0),
        "idempotency_key": f"{client_order_id}-cancel",
        "operator_ref": OPERATOR_REF,
        "readback_ref": source_ref(output_dir / "post_submit_readback.json"),
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    write_json(output_dir / "cancel_intent.json", cancel_intent)
    cancel_risk = build_risk_decision(
        status="approved" if order_is_working(submit_readback_order) or not args.arm_paper_send else "blocked",
        intent_ref=source_ref(output_dir / "cancel_intent.json"),
        preflight_verdict={
            "accepted": order_is_working(submit_readback_order) or not args.arm_paper_send,
            "submit_order_seen": submit_readback_order is not None,
            "submit_order_working": order_is_working(submit_readback_order),
        },
        guardrails=guardrails,
        projected_net_position=projected_net_position,
    )
    write_json(output_dir / "cancel_risk_decision.json", cancel_risk)
    cancel_approval = build_approval_decision(
        status="approved" if cancel_risk["status"] == "approved" else "blocked",
        risk_ref=source_ref(output_dir / "cancel_risk_decision.json"),
    )
    write_json(output_dir / "cancel_approval_decision.json", cancel_approval)

    cancel_gateway: dict[str, Any] = {
        "schema_version": "account_command.execution_event.v1",
        "account_id": ACCOUNT_ID,
        "status": "blocked",
        "source_ref": source_ref(output_dir / "cancel_intent.json"),
        "mode": mode,
        "cancel_send_armed": args.arm_cancel_send,
        "gateway_ack_is_final_state": False,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    if not args.arm_cancel_send:
        cancel_gateway.update({"status": "dry_run", "failure_reason": None})
    elif cancel_approval["status"] != "approved":
        cancel_gateway.update({"failure_reason": "cancel_approval_blocked"})
    else:
        cancel_result = run_native_cancel(
            config=config,
            instrument=args.instrument,
            exchange=args.exchange,
            order_ref=int(mapped_order_ref or 0),
            front_id=int(mapped_front_id or 0),
            session_id=int(mapped_session_id or 0),
            flow_path=output_dir / "cancel_flow",
            timeout_seconds=args.timeout_seconds,
        )
        cancel_gateway.update(cancel_result)
        cancel_gateway["status"] = "accepted" if cancel_result.get("accepted") else "blocked"
        cancel_status = cancel_gateway["status"]
    write_json(output_dir / "cancel_gateway_event.json", cancel_gateway)

    post_cancel = run_readback_query(
        config_path=args.config,
        flow_path=output_dir / "post_cancel_query_flow",
        output_json=output_dir / "post_cancel_readback.json",
    )
    post_cancel_order = None
    if mapped_order_ref is not None:
        post_cancel_order = find_order(post_cancel, instrument=args.instrument, order_ref=str(mapped_order_ref))

    if args.arm_paper_send and args.arm_cancel_send:
        reconciled = (
            submit_gateway.get("status") == "accepted"
            and submit_readback_order is not None
            and cancel_status == "accepted"
            and order_is_cancelled(post_cancel_order)
        )
    else:
        reconciled = submit_gateway.get("status") == "accepted" and cancel_gateway.get("status") == "dry_run"
    reconciliation = {
        "schema_version": "account_command.reconciliation_result.v1",
        "account_id": ACCOUNT_ID,
        "status": "reconciled" if reconciled else "blocked",
        "source_ref": source_ref(output_dir / "post_cancel_readback.json"),
        "mode": mode,
        "submit_readback_order_seen": submit_readback_order is not None,
        "submit_readback_order_working": order_is_working(submit_readback_order),
        "post_cancel_order_seen": post_cancel_order is not None,
        "post_cancel_order_cancelled": order_is_cancelled(post_cancel_order),
        "gateway_ack_is_final_state": False,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    write_json(output_dir / "reconciliation_result.json", reconciliation)

    audit_status = "reconciled" if reconciliation["status"] == "reconciled" else "blocked"
    command_audit = {
        "schema_version": "account_command.command_audit_record.v1",
        "account_id": ACCOUNT_ID,
        "status": audit_status,
        "source_ref": source_ref(output_dir / "command_audit.json"),
        "mode": mode,
        "intent_refs": [source_ref(output_dir / "submit_intent.json"), source_ref(output_dir / "cancel_intent.json")],
        "risk_decision_refs": [
            source_ref(output_dir / "submit_risk_decision.json"),
            source_ref(output_dir / "cancel_risk_decision.json"),
        ],
        "approval_decision_refs": [
            source_ref(output_dir / "submit_approval_decision.json"),
            source_ref(output_dir / "cancel_approval_decision.json"),
        ],
        "gateway_event_refs": [
            source_ref(output_dir / "submit_gateway_event.json"),
            source_ref(output_dir / "cancel_gateway_event.json"),
        ],
        "readback_refs": [
            source_ref(output_dir / "post_submit_readback.json"),
            source_ref(output_dir / "post_cancel_readback.json"),
        ],
        "reconciliation_ref": source_ref(output_dir / "reconciliation_result.json"),
        "submit_intent_checksum": submit_intent_checksum,
        "gateway_ack_is_final_state": False,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
    }
    write_json(output_dir / "command_audit.json", command_audit)

    leaks = sensitive_matches(output_dir)
    redaction = {
        "schema_version": "account_command.redaction_report.v1",
        "account_id": ACCOUNT_ID,
        "status": "passed" if not leaks else "blocked",
        "source_ref": source_ref(output_dir),
        "mode": mode,
        "sensitive_match_files": leaks,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "gateway_ack_is_final_state": False,
    }
    write_json(output_dir / "redaction_report.json", redaction)

    manifest_refs = {}
    for artifact in sorted(output_dir.glob("*.json")):
        manifest_refs[artifact.name] = {
            "ref": source_ref(artifact),
            "checksum": file_checksum(artifact),
        }
    closeout = {
        "schema_version": "account_command.closeout_manifest.v1",
        "account_id": ACCOUNT_ID,
        "status": audit_status if redaction["status"] == "passed" else "blocked",
        "run_id": output_dir.name,
        "captured_at_utc": utc_now(),
        "mode": mode,
        "artifact_refs": manifest_refs,
        "raw_secret_values_recorded": False,
        "raw_broker_endpoint_recorded": False,
        "gateway_ack_is_final_state": False,
    }
    write_json(output_dir / "closeout_manifest.json", closeout)

    print(
        json.dumps(
            {
                "status": closeout["status"],
                "mode": mode,
                "run_dir": str(output_dir),
                "submit_status": submit_gateway.get("status"),
                "cancel_status": cancel_gateway.get("status"),
                "reconciliation_status": reconciliation["status"],
                "redaction_status": redaction["status"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if closeout["status"] == "reconciled" else 1


if __name__ == "__main__":
    raise SystemExit(main())
