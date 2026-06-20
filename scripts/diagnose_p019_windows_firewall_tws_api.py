from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "debug" / "p019-tws-api-readiness" / "windows-firewall-tws-api-diagnostic.json"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _powershell(script: str) -> Any:
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        text=True,
        capture_output=True,
        check=False,
        timeout=20,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        return []
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return []


def build_payload() -> dict[str, Any]:
    profiles = _powershell(
        "Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction | ConvertTo-Json -Compress"
    )
    allow_rules = _powershell(
        "$out=@(); "
        "$rules=Get-NetFirewallRule -ErrorAction SilentlyContinue | "
        "Where-Object { $_.DisplayName -match 'TWS|Trader|Interactive|IB|Java|OpenJDK|JDK|JRE|7496|7497|4001|4002' }; "
        "foreach($r in $rules){ "
        "$ports=$r | Get-NetFirewallPortFilter; $addr=$r | Get-NetFirewallAddressFilter; "
        "$out += [pscustomobject]@{DisplayName=$r.DisplayName; Enabled=$r.Enabled.ToString(); "
        "Direction=$r.Direction.ToString(); Action=$r.Action.ToString(); Profile=$r.Profile.ToString(); "
        "Program=$r.Program; Protocol=$ports.Protocol; LocalPort=$ports.LocalPort; "
        "RemoteAddress=$addr.RemoteAddress; LocalAddress=$addr.LocalAddress} }; "
        "$out | ConvertTo-Json -Compress -Depth 4"
    )
    block_rules = _powershell(
        "Get-NetFirewallRule -Direction Inbound -Action Block -Enabled True -ErrorAction SilentlyContinue | "
        "Where-Object { $_.DisplayName -match 'TWS|Trader|Interactive|IB|Java|OpenJDK|JDK|JRE|7496|7497|4001|4002' -or $_.Program -match 'tws|java|ib' } | "
        "Select-Object DisplayName,Enabled,Direction,Action,Profile,Program | ConvertTo-Json -Compress -Depth 3"
    )
    listen_rows = _powershell(
        "$items=@(); foreach($p in 7496,7497,4001,4002){ "
        "$items += @(Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | "
        "Select-Object LocalAddress,LocalPort,State,OwningProcess) }; "
        "$items | ConvertTo-Json -Compress"
    )
    tws_rows = _powershell(
        "Get-Process -Name tws -ErrorAction SilentlyContinue | "
        "Select-Object -First 1 Id,MainWindowTitle,Responding | ConvertTo-Json -Compress"
    )
    if isinstance(allow_rules, dict):
        allow_rules = [allow_rules]
    if isinstance(block_rules, dict):
        block_rules = [block_rules]
    if isinstance(listen_rows, dict):
        listen_rows = [listen_rows]
    has_allow = any(str(row.get("Action")) == "Allow" and str(row.get("Enabled")) == "True" for row in allow_rules)
    has_block = bool(block_rules)
    has_listen = bool(listen_rows)
    return {
        "schema": "account-console.p019-windows-firewall-tws-api-diagnostic.v1",
        "proposal_id": "p019-broker-observation-session-foundation",
        "account_id": "acct.ib.live.u3028269",
        "display_alias": "U3028269",
        "observed_at": _now(),
        "diagnostic_kind": "windows_firewall_tws_api",
        "tws_process": {
            "present": bool(tws_rows),
            "window_title_ref": "U3028269_account_window" if "U3028269" in json.dumps(tws_rows, ensure_ascii=False) else "unmatched_or_absent",
            "responding": bool(tws_rows.get("Responding")) if isinstance(tws_rows, dict) else None,
        },
        "firewall_profiles": profiles,
        "matching_allow_rules": allow_rules,
        "matching_block_rules": block_rules,
        "known_api_listeners": listen_rows,
        "diagnosis": {
            "matching_allow_rules_present": has_allow,
            "matching_block_rules_present": has_block,
            "known_tws_api_ports_listening": has_listen,
            "firewall_is_primary_blocker": False if not has_listen else None,
            "primary_blocker": "local_tws_api_socket_not_open" if not has_listen else "unknown",
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
    parser = argparse.ArgumentParser(description="Diagnose Windows firewall posture for local TWS API readiness.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    payload = build_payload()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "written", "primary_blocker": payload["diagnosis"]["primary_blocker"], "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
