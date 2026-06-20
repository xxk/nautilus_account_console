# P019 TWS API Runtime Recovery Runbook / TWS API 运行恢复手册

- Proposal ID: `p019-broker-observation-session-foundation`
- Status: pre-acceptance runtime recovery guide
- Updated: 2026-06-20
- Account slice: `acct.ib.live.u3028269`
- ADR anchor: [ADR-0005](../../adr/0005-account-console-independent-broker-observation-sessions.md)

## 1. Purpose

This runbook is the operator-facing path from the current typed blocker to real read-only TWS API funds and positions collection.

Current blocker:

```text
tws_api_readiness_missing
local_tws_api_socket_not_open
tws_api_socket_disabled_in_latest_config_candidate
```

The recovery target is not a screenshot and not a browser readback. The target is a passing local TWS API readiness probe followed by read-only `reqAccountSummary` and `reqPositions` query artifacts, a source package built from those artifacts, and Account Mirror projection from that source package.

## 2. Boundaries

Allowed:

1. Confirm local TWS process/window state with diagnostics.
2. Inspect sanitized TWS API config refs and booleans.
3. Enable the logged-in TWS API socket in the TWS UI or owner-approved launcher/config path.
4. Run read-only TWS API readiness and collection commands.
5. Record refs, checksums, typed blockers and no-secret/no-command boundaries.

Forbidden:

1. Do not paste passwords, paste auth codes, paste 2FA values, account secrets, raw endpoints or client secret material into chat, docs, fixtures or evidence.
2. Do not copy raw `tws.xml` contents into this worktree.
3. Do not use screenshots as funds truth, positions truth, account truth, execution report truth or trading-readiness evidence.
4. Do not call or add `placeOrder`, `cancelOrder`, `reqOpenOrders`, `reqAllOpenOrders` or broker mutation APIs.
5. Do not bypass Account Mirror with direct browser/backend TWS routes.

## 3. Recovery Steps

1. Confirm current typed blocker and local state:

```bash
python scripts/diagnose_p019_tws_api_socket.py
python scripts/validate_p019_tws_api_socket_diagnostic.py
python scripts/diagnose_p019_windows_firewall_tws_api.py
python scripts/validate_p019_windows_firewall_tws_api_diagnostic.py
python scripts/diagnose_p019_tws_api_config.py
python scripts/validate_p019_tws_api_config_diagnostic.py
```

The socket diagnostic uses the historical IB API `serverVersion` handshake shape from `D:\Nautilus\nautilus_strategies\scripts\probe_tws_version.py` with version range `v100..155`: `handshake_ok` is required before funds/positions collection may start. TCP connectable without `serverVersion` remains blocked as `local_tws_api_handshake_not_ok`, because it may indicate Trusted IPs, localhost-only policy, API popup, wrong port or non-IB service mismatch.

2. Treat the current evidence as an API socket/config blocker, not an immediate reinstall signal. The current sanitized evidence says:

```text
tws_process.present=true
firewall_allow_rules=present
firewall_enabled_block_rules=absent
latest_config_candidate.api_socket_enabled=false
latest_config_candidate.socketClient=false
latest_config_candidate.port=7497
known_api_ports_connectable=false
```

3. Prepare the operator change request artifact before changing TWS settings:

```bash
python scripts/prepare_p019_tws_api_enable_change_request.py
python scripts/validate_p019_tws_api_enable_change_request.py
```

This artifact records the target config ref, current sanitized API settings, requested `socketClient=true` / localhost-only settings, expected impact and post-change verification commands. It does not modify `C:\Jts`, does not copy raw `tws.xml`, does not query account values and does not record secrets.

4. Enable the API socket in the already logged-in TWS session or through an owner-approved launcher/config path. The current sanitized config diagnostic expects this blocker to clear:

```text
latest_tws_config_candidate_socket_client_false
```

5. Re-run readiness without account queries:

```bash
python scripts/probe_p019_tws_api_readiness.py
python scripts/validate_p019_tws_api_readiness_probe.py
```

6. When readiness is true, run the guarded wait-and-collect entrypoint:

```bash
python scripts/wait_p019_tws_api_ready_and_collect.py --timeout-seconds 120 --interval-seconds 5
python scripts/validate_p019_tws_api_wait_collect.py
```

7. Validate the full pipeline and projection:

```bash
python scripts/validate_p019_ib_u3028269_tws_api_pipeline.py
python scripts/validate_p019_ib_u3028269_tws_api_queries.py
python scripts/validate_p019_ib_u3028269_source_package.py
python scripts/validate_account_mirror_api.py
python scripts/validate_p019_broker_observation_foundation.py
```

8. Validate that runtime evidence is fresh before using it for any closeout statement:

```bash
python scripts/validate_p019_runtime_evidence_freshness.py
```

This gate requires the reinstall decision and real closeout evidence to be newer than the latest socket/firewall/config diagnostics, requires the API enable change request to be newer than the config diagnostic it cites, and keeps stale pipeline summaries from being promoted to readiness while the current blocker remains `tws_api_readiness_missing`.

## 4. Reinstall Decision Gate

Do not reinstall TWS as the first remediation for the current blocker. Reinstall is outside this worktree and may modify `C:\Jts`, installed TWS versions, local settings, workspace layouts and logged-in session state. It requires explicit operator approval after recording the exact path, reason and expected impact.

Reinstall may be considered only after these preconditions are all recorded:

1. The API socket has been enabled in the logged-in TWS UI or owner-approved config/launcher path.
2. TWS has been restarted or relaunched after the API setting change.
3. `diagnose_p019_tws_api_config.py` no longer reports `latest_tws_config_candidate_socket_client_false`, or records that the setting cannot persist across restart.
4. `diagnose_p019_tws_api_socket.py` still reports no known TWS/Gateway API listener after the setting is enabled and TWS is restarted.
5. `diagnose_p019_windows_firewall_tws_api.py` still reports allow rules present and enabled block rules absent.
6. The reinstall target path, installer/source, version channel and expected impact have been approved by the operator.

Reinstall must not be used to bypass the evidence chain. After reinstall or repair, the same readiness, query, source-package, Account Mirror and UI parity validators still apply.

## 5. Ready Evidence Required

Ready closeout requires all of the following current-state evidence:

1. `output/debug/p019-tws-api-readiness/tws-api-readiness-probe.json` has `ready_for_tws_api_funds_positions_query=true`.
2. `output/account_capability/ib-live-u3028269/tws-api/account_summary.json` has `success=true` and `tws_api_login_confirmed=true`.
3. `output/account_capability/ib-live-u3028269/tws-api/positions.json` has `success=true` and `tws_api_login_confirmed=true`.
4. `output/account_capability/ib-live-u3028269/source-package.json` has `source_health.state=ready`, `source_health.api_transport=ib_tws_api`, `boundaries.screenshot_used_for_funds_positions=false` and `boundaries.order_action_sent=false`.
5. Account Mirror returns `acct.ib.live.u3028269` from `/api/mirror/accounts/acct.ib.live.u3028269` with command disabled and no broker/order truth claim.
6. Browser/UI parity remains a separate acceptance step and must compare rendered values against the same-slice TWS API/source package payload.

## 6. Blocked Evidence Required

If readiness remains blocked, the runbook closes only as a typed retry state. It must preserve:

```text
raw_secret_values_recorded=false
raw_broker_endpoint_recorded=false
tws_api_account_query_sent_before_readiness=false
funds_positions_values_recorded_before_readiness=false
screenshot_used_for_funds_positions=false
order_action_sent=false
```

The blocked state is not a pass for real funds or positions. It is evidence that the system failed closed.
