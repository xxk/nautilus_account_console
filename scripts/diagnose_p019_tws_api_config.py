from __future__ import annotations

import argparse
import json
import socket
import subprocess
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "tws-api-config-diagnostic.json"
DEFAULT_JTS_ROOT = Path("C:/Jts")
PORT_REFS = {
    "tws_live_default": 7496,
    "tws_paper_default": 7497,
    "gateway_live_default": 4001,
    "gateway_paper_default": 4002,
}
API_ATTRS = {"socketClient", "allowOnlyLocalhost", "port"}


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _file_ref(path: Path) -> str:
    return f"local-file-ref://{path.as_posix()}"


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
    title = str(row.get("MainWindowTitle", ""))
    return {
        "present": True,
        "process_name": "tws",
        "process_id": row.get("Id"),
        "window_title_ref": "U3028269_account_window" if "U3028269" in title else "unmatched_tws_window",
        "responding": bool(row.get("Responding")),
    }


def _tcp_connectable(port: int, timeout: float) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def _connect_port_refs(timeout: float) -> dict[str, dict[str, Any]]:
    return {ref: {"connectable": _tcp_connectable(port, timeout)} for ref, port in PORT_REFS.items()}


def _api_attrs(path: Path) -> dict[str, str | None]:
    attrs: dict[str, str | None] = {attr: None for attr in API_ATTRS}
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return attrs
    for element in root.iter():
        for name in API_ATTRS:
            if attrs[name] is None and name in element.attrib:
                attrs[name] = element.attrib[name]
        if all(value is not None for value in attrs.values()):
            break
    return attrs


def _candidate(path: Path) -> dict[str, Any]:
    stat = path.stat()
    attrs = _api_attrs(path)
    return {
        "config_ref": _file_ref(path),
        "last_write_time": datetime.fromtimestamp(stat.st_mtime, UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "length_bytes": stat.st_size,
        "api_settings": {
            "socketClient": attrs["socketClient"],
            "allowOnlyLocalhost": attrs["allowOnlyLocalhost"],
            "port": attrs["port"],
        },
        "api_socket_enabled": str(attrs["socketClient"]).lower() == "true",
    }


def build_payload(jts_root: Path, timeout: float) -> dict[str, Any]:
    paths = sorted(jts_root.rglob("tws.xml")) if jts_root.exists() else []
    candidates = [_candidate(path) for path in paths]
    candidates.sort(key=lambda item: item["last_write_time"], reverse=True)
    latest = candidates[0] if candidates else None
    connect_refs = _connect_port_refs(timeout)
    any_connectable = any(item["connectable"] for item in connect_refs.values())

    reasons: list[str] = []
    primary_blocker = None
    if not any_connectable:
        reasons.append("local_tws_api_socket_not_open")
    if latest and latest["api_settings"]["socketClient"] == "false":
        reasons.append("latest_tws_config_candidate_socket_client_false")
        primary_blocker = "tws_api_socket_disabled_in_latest_config_candidate"
    elif not candidates:
        reasons.append("tws_config_candidates_missing")
        primary_blocker = "tws_api_config_not_found"
    elif not any_connectable:
        primary_blocker = "local_tws_api_socket_not_open"

    return {
        "schema": "account-console.p019-tws-api-config-diagnostic.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "observed_at": _now(),
        "diagnostic_kind": "tws_api_config",
        "tws_process": _tws_process(),
        "config_search_ref": _file_ref(jts_root),
        "candidate_config_count": len(candidates),
        "latest_config_candidate": latest,
        "config_candidates": candidates,
        "connect_port_refs": connect_refs,
        "ready_for_tws_api_funds_positions_query": any_connectable,
        "typed_blocker": None
        if any_connectable
        else {
            "blocker_id": "tws_api_readiness_missing",
            "blocker_kind": "tws_api_config_or_socket_blocker",
            "primary_blocker": primary_blocker,
            "reasons": reasons,
            "retry_condition": "enable the logged-in TWS API socket in Global Configuration, confirm the API port, then rerun the P019 TWS API pipeline.",
        },
        "boundaries": {
            "raw_config_file_contents_recorded": False,
            "raw_secret_values_recorded": False,
            "raw_broker_endpoint_recorded": False,
            "tws_api_account_query_sent": False,
            "funds_positions_values_recorded": False,
            "screenshot_used_for_funds_positions": False,
            "order_action_sent": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose sanitized TWS API config readiness without account queries.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--jts-root", type=Path, default=DEFAULT_JTS_ROOT)
    parser.add_argument("--timeout", type=float, default=0.75)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    payload = build_payload(args.jts_root, args.timeout)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ready" if payload["ready_for_tws_api_funds_positions_query"] else "blocked",
                "primary_blocker": None
                if payload["typed_blocker"] is None
                else payload["typed_blocker"]["primary_blocker"],
                "output": str(output),
            },
            ensure_ascii=False,
        )
    )
    return 0 if payload["ready_for_tws_api_funds_positions_query"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
