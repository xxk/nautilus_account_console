# P019 Workspace/Home Runbook Intake / workspace 与 home runbook 采纳记录

- Proposal ID: `p019-broker-observation-session-foundation`
- Account slice: `acct.ib.live.u3028269`
- Date: 2026-06-20
- Status: pre-acceptance intake evidence

## Purpose

This intake records which local workspace/home runbooks were inspected for the P019 TWS API runtime recovery path and which stable operating rules were adopted.

It is not real funds/positions evidence, not a TWS login proof and not ADR-0005 acceptance.

## Search Scope

Read-only search covered:

1. `D:\Nautilus` workspace runbooks and TWS-related docs.
2. `C:\Users\Administrator` home runbooks.
3. Local project docs under `D:\Nautilus\nautilus_account_console`.

No writes were made outside `D:\Nautilus\_worktrees\r1-hb-contract`.

## Adopted References

| Reference | Why adopted | Stable rule used by P019 |
| --- | --- | --- |
| `D:\Nautilus\nautilus_strategies\scripts\probe_tws_version.py` | Existing IB API probe separates TCP connect from IB `serverVersion` handshake. | P019 socket readiness must require IB API `handshake_ok` using version range `v100..155`; TCP connectable alone is not enough for funds/positions collection. |
| `D:\Nautilus\nautilus_strategies\tests\scripts\test_probe_tws_version.py` | Existing tests lock the framed IB API handshake and JSON status taxonomy. | P019 diagnostic records `connect_timeout`, `connect_refused`, `handshake_timeout`, `handshake_invalid` and `handshake_ok` as distinct states. |
| `D:\Nautilus\nautilus_strategies\tests\scripts\test_run_issue19_unblock_sequence.py` | Existing unblock sequence fails closed when the TWS probe is not handshake OK. | P019 current-state closeout must stop before account query/source-package success when the socket handshake is not OK. |
| `D:\Nautilus\global_docs\network\20_3proxy上游拓扑与接入方案_3proxy Upstream Topology and Access Plan.md` | Local network topology notes say direct TWS startup should be checked via TWS/Java/2FA/API/GUI before blaming OpenWrt/PassWall/3proxy. | Current P019 blocker remains a local TWS API socket/config blocker, not a network-proxy blocker. |
| `D:\Nautilus\global_docs\network\93_本机Windows防火墙分析与最小启用方案_Local Windows Firewall Analysis and Enable Plan.md` | Firewall runbook distinguishes profile/default-action checks from broad rule mutation. | P019 firewall diagnostic remains read-only and records allow/block rule state; it does not mutate firewall rules. |

## Excluded References

| Reference class | Why excluded |
| --- | --- |
| `C:\Users\Administrator\.codex\.tmp\plugins\plugins\zoom\...\RUNBOOK.md` | Home runbooks found there are Zoom plugin SDK runbooks, unrelated to TWS/P019 broker observation. |
| Backup copies under `D:\Nautilus\_backups\...` | Duplicated historical docs are lower authority than current workspace roots. |
| Raw TWS XML/config contents | Sensitive/runtime-owned material; P019 records config refs and sanitized booleans only. |

## Adopted P019 Changes

1. `scripts/diagnose_p019_tws_api_socket.py` now performs the IB API `serverVersion` handshake probe.
2. `scripts/validate_p019_tws_api_socket_diagnostic.py` requires `handshake_ok` for readiness.
3. `scripts/validate_p019_runtime_evidence_freshness.py` treats TCP-connectable but not handshake-OK as blocked.
4. `docs/proposals/p019-broker-observation-session-foundation/tws-api-runtime-recovery-runbook.md` records the runbook-derived handshake recovery rule.

## Boundaries

```text
raw_secret_values_recorded=false
raw_broker_endpoint_recorded=false
raw_config_file_contents_recorded=false
external_runbook_copied_as_truth=false
home_zoom_runbooks_adopted=false
tws_config_modified=false
tws_reinstall_performed=false
tws_api_account_query_sent_by_intake=false
funds_positions_values_recorded_by_intake=false
screenshot_used_for_funds_positions=false
order_action_sent=false
```

## Current Result

The current local TWS process/window is present for U3028269, but P019 socket diagnostic records all known TWS/Gateway API refs as handshake-not-OK, currently `connect_timeout`. Therefore the current blocker remains:

```text
tws_api_readiness_missing
local_tws_api_socket_not_open
tws_api_socket_disabled_in_latest_config_candidate
```

Ready closeout still requires real TWS API `handshake_ok`, account summary success, positions success, ready source package and real UI parity pass.
