from __future__ import annotations

import argparse
import importlib.util
import json
import socket
import struct
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-socket-diagnostic.json"
DEFAULT_IBAPI_RUNTIME = ROOT / "output" / "runtime" / "python"
PORT_REFS = {
    "tws_live_default": 7496,
    "tws_paper_default": 7497,
    "gateway_live_default": 4001,
    "gateway_paper_default": 4002,
}
HANDSHAKE_VERSION_RANGE = "v100..155"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _add_runtime(path: Path) -> str | None:
    if path.exists():
        sys.path.insert(0, str(path))
        return _source_ref(path)
    return None


def _tcp_connectable(port: int, timeout: float) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def _build_ib_handshake() -> bytes:
    payload = HANDSHAKE_VERSION_RANGE.encode("ascii")
    return b"API\x00" + struct.pack(">I", len(payload)) + payload


def _recv_ib_frame(sock: socket.socket, timeout: float) -> bytes:
    deadline = time.monotonic() + timeout
    buffer = b""
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("timed out waiting for IB API serverVersion")
        sock.settimeout(remaining)
        chunk = sock.recv(4096)
        if not chunk:
            return buffer
        buffer += chunk
        if len(buffer) >= 4:
            payload_length = struct.unpack(">I", buffer[:4])[0]
            if len(buffer) >= 4 + payload_length:
                return buffer[: 4 + payload_length]


def _parse_server_version(frame: bytes) -> tuple[int, str | None]:
    if len(frame) < 4:
        raise ValueError("response frame too short")
    payload_length = struct.unpack(">I", frame[:4])[0]
    if len(frame) < 4 + payload_length:
        raise ValueError("response frame incomplete")
    payload = frame[4 : 4 + payload_length].decode("ascii", errors="replace")
    parts = payload.split("\x00")
    if not parts or not parts[0].strip().isdigit():
        raise ValueError("unexpected serverVersion payload")
    return int(parts[0].strip()), parts[1].strip() if len(parts) > 1 and parts[1].strip() else None


def _handshake_probe(port: int, timeout: float) -> dict[str, Any]:
    try:
        sock = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    except TimeoutError:
        return {
            "status": "connect_timeout",
            "tcp_connected": False,
            "bytes_received": 0,
            "server_version": None,
            "connect_time": None,
        }
    except ConnectionRefusedError:
        return {
            "status": "connect_refused",
            "tcp_connected": False,
            "bytes_received": 0,
            "server_version": None,
            "connect_time": None,
        }
    except OSError:
        return {
            "status": "connect_error",
            "tcp_connected": False,
            "bytes_received": 0,
            "server_version": None,
            "connect_time": None,
        }
    with sock:
        try:
            sock.sendall(_build_ib_handshake())
            frame = _recv_ib_frame(sock, timeout)
        except TimeoutError:
            return {
                "status": "handshake_timeout",
                "tcp_connected": True,
                "bytes_received": 0,
                "server_version": None,
                "connect_time": None,
            }
        except OSError:
            return {
                "status": "handshake_error",
                "tcp_connected": True,
                "bytes_received": 0,
                "server_version": None,
                "connect_time": None,
            }
    if not frame:
        return {
            "status": "handshake_no_response",
            "tcp_connected": True,
            "bytes_received": 0,
            "server_version": None,
            "connect_time": None,
        }
    try:
        server_version, connect_time = _parse_server_version(frame)
    except ValueError:
        return {
            "status": "handshake_invalid",
            "tcp_connected": True,
            "bytes_received": len(frame),
            "server_version": None,
            "connect_time": None,
        }
    return {
        "status": "handshake_ok",
        "tcp_connected": True,
        "bytes_received": len(frame),
        "server_version": server_version,
        "connect_time": connect_time,
    }


def _listening_port_refs() -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {
        ref: {"listening": False, "owning_process": None}
        for ref in PORT_REFS
    }
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "$items=@(); foreach($p in 7496,7497,4001,4002){"
        "$items += @(Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | "
        "Select-Object LocalPort,OwningProcess)"
        "}; $items | ConvertTo-Json -Compress",
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, check=False, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return results
    if completed.returncode != 0 or not completed.stdout.strip():
        return results
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return results
    rows = parsed if isinstance(parsed, list) else [parsed]
    port_to_ref = {port: ref for ref, port in PORT_REFS.items()}
    for row in rows:
        ref = port_to_ref.get(int(row.get("LocalPort", 0)))
        if ref:
            results[ref] = {"listening": True, "owning_process": row.get("OwningProcess")}
    return results


def _tws_process() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-Process -Name tws -ErrorAction SilentlyContinue | "
        "Select-Object -First 1 Id,MainWindowTitle,Responding | ConvertTo-Json -Compress",
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False, timeout=5)
    if completed.returncode != 0 or not completed.stdout.strip():
        return {"present": False}
    try:
        row = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"present": False}
    return {
        "present": True,
        "process_name": "tws",
        "process_id": row.get("Id"),
        "window_title_ref": "U3028269_account_window" if "U3028269" in str(row.get("MainWindowTitle", "")) else "unmatched_tws_window",
        "responding": bool(row.get("Responding")),
    }


def build_payload(timeout: float, ibapi_runtime: Path) -> dict[str, Any]:
    runtime_ref = _add_runtime(ibapi_runtime)
    ibapi_available = importlib.util.find_spec("ibapi") is not None
    listener_results = _listening_port_refs()
    connect_results = {
        ref: {"connectable": _tcp_connectable(port, timeout)}
        for ref, port in PORT_REFS.items()
    }
    handshake_results = {
        ref: _handshake_probe(port, timeout)
        for ref, port in PORT_REFS.items()
    }
    any_socket_ready = any(item["status"] == "handshake_ok" for item in handshake_results.values())
    blocker_reasons = []
    if not ibapi_available:
        blocker_reasons.append("python_ibapi_module_missing")
    if not any_socket_ready:
        if any(item["tcp_connected"] for item in handshake_results.values()):
            blocker_reasons.append("local_tws_api_handshake_not_ok")
        else:
            blocker_reasons.append("local_tws_api_socket_not_open")
    return {
        "schema": "account-console.p019-tws-api-socket-diagnostic.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "observed_at": _now(),
        "diagnostic_kind": "local_tws_api_socket",
        "tws_process": _tws_process(),
        "ibapi_available": ibapi_available,
        "ibapi_runtime_ref": runtime_ref,
        "host_ref": "localhost_tws_api",
        "listener_port_refs": listener_results,
        "connect_port_refs": connect_results,
        "handshake_port_refs": handshake_results,
        "handshake_version_range": HANDSHAKE_VERSION_RANGE,
        "ready_for_tws_api_funds_positions_query": ibapi_available and any_socket_ready,
        "typed_blocker": None
        if ibapi_available and any_socket_ready
        else {
            "blocker_id": "tws_api_readiness_missing",
            "blocker_kind": "local_api_socket_blocker",
            "reasons": blocker_reasons,
            "retry_condition": "enable the already logged-in TWS/Gateway API socket, then rerun the P019 pipeline.",
        },
        "boundaries": {
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "tws_api_account_query_sent": False,
            "funds_positions_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose local TWS API socket readiness without account queries.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=0.75)
    parser.add_argument("--ibapi-runtime", type=Path, default=DEFAULT_IBAPI_RUNTIME)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    payload = build_payload(args.timeout, args.ibapi_runtime)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked", "output": str(output)}, ensure_ascii=False))
    return 0 if payload["ready_for_tws_api_funds_positions_query"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
