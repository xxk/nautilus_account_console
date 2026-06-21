# U3028269 TWS Login and API Knowledge / U3028269 TWS 登录与 API 知识卡

- Knowledge ID: `ib-tws-u3028269-login-api`
- Owner scope: Account Console broker observation knowledge
- Account slice: `acct.ib.live.u3028269`
- Status: login-success recorded
- Last updated: 2026-06-20

## Purpose

This knowledge card preserves the repeatable TWS login/API enablement workflow for U3028269 so future P019/ADR-0005 work does not rediscover the same local steps from scratch.

It records only non-secret process knowledge, sanitized config shape and verification commands.

## What This Card Must Never Store

```text
raw_tws_password=false
raw_2fa_or_auth_code=false
raw_broker_secret=false
raw_broker_endpoint=false
raw_tws_xml_contents=false
raw_account_secret=false
```

Do not paste passwords, 2FA values, auth codes, raw `tws.xml`, raw broker endpoints or account secrets into this card.

## Current Known Local Shape

| Item | Current non-secret shape |
| --- | --- |
| Canonical account | `acct.ib.live.u3028269` |
| Display alias | `U3028269` |
| TWS config owner | local TWS runtime under `local-file-ref://C:/Jts/.../tws.xml` |
| Latest sanitized API setting observed by P019 | runtime `handshake_ok=true`; latest static XML candidate may still report `socketClient=false`, `allowOnlyLocalhost=true`, `port=7497` |
| Required API access posture | socket clients enabled, localhost-only, no remote access policy unless explicitly owner-approved |
| Readiness proof | IB API `serverVersion` `handshake_ok`, not merely TCP connectable |
| Collection proof | read-only TWS API `reqAccountSummary`, `reqPositions` and `reqExecutions`/`ExecutionFilter` success |
| Projection proof | source package -> Account Mirror -> Account Workbench UI parity |
| Report/store non-claim | current real `reqExecutions` returned zero rows, so report parity and durable reload parity remain blocked |

## Repeatable Recovery Flow

1. Confirm TWS is running and logged into the intended `U3028269` session.
2. Open TWS Global Configuration.
3. Navigate to API settings.
4. Enable socket clients / TWS API socket.
5. Keep localhost-only access enabled unless a separate owner-approved remote policy exists.
6. Confirm the API port is the recorded expected port, currently `7497`.
7. Restart or reconnect TWS if the setting does not take effect in the running process.
8. Run the current-state closeout refresh:

```bash
python scripts/refresh_p019_u3028269_current_state_closeout.py --wait-timeout-seconds 120 --wait-interval-seconds 5
python scripts/validate_p019_u3028269_current_state_closeout_refresh.py
```

9. If ready, verify real closeout:

```bash
python scripts/validate_p019_u3028269_real_acceptance_closeout.py
python scripts/validate_p019_runtime_evidence_freshness.py
python scripts/validate_p019_broker_observation_foundation.py
```

## Required Evidence After Successful Login/API Enablement

The following current-state artifacts must exist and agree:

| Artifact | Required ready evidence |
| --- | --- |
| `output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json` | `ready_for_tws_api_funds_positions_query=true`, at least one `handshake_port_refs.*.status=handshake_ok` |
| `output/debug/p019-tws-api-readiness/tws-api-config-diagnostic.json` | `ready_for_tws_api_funds_positions_query=true`, connectable API port ref exists; static XML candidate is sanitized reference evidence and may lag runtime state |
| `output/account_capability/ib-live-u3028269/tws-api/account_summary.json` | `success=true`, `tws_api_login_confirmed=true` |
| `output/account_capability/ib-live-u3028269/tws-api/positions.json` | `success=true`, `tws_api_login_confirmed=true` |
| `output/account_capability/ib-live-u3028269/tws-api/executions.json` | `success=true`, `execution_report_rows=0`, `readonly_query.complete_history_claimed=false`, `readonly_query.order_action_sent=false` |
| `output/account_capability/ib-live-u3028269/source-package.json` | `source_health.state=ready`, `source_health.api_transport=ib_tws_api` |
| `output/account_capability/ib-live-u3028269/durable-store-reload.json` | `replay_state.state=partial`, `reload_proof.parity_status=blocked` while real execution rows are absent |
| `docs/proposals/p019-broker-observation-session-foundation/p019-completion-audit.json` | `overall_status=not_complete`, `completion_must_not_be_claimed=true` |
| `docs/acceptance/2026-06-20-p019-u3028269-real-ui-parity-evidence.json` | `verdict=pass` |
| `output/account_capability/ib-live-u3028269/real-acceptance-closeout.json` | `status=ready`, `blocker_id=null` |

## Failure Interpretation

| Failure | Meaning | Next action |
| --- | --- | --- |
| `local_tws_api_socket_not_open` | TWS API socket is not listening on known local refs. | Enable API socket in logged-in TWS and restart/reconnect if needed. |
| `local_tws_api_handshake_not_ok` | TCP may be open, but IB API `serverVersion` handshake failed. | Check Trusted IPs, localhost-only policy, API popup, wrong port or non-IB service mismatch. |
| `tws_api_socket_disabled_in_latest_config_candidate` | Latest sanitized config candidate still has `socketClient=false`. | Enable socket clients in TWS settings. |
| `tws_api_readiness_missing` | Readiness is not sufficient to query funds/positions. | Do not run or accept funds/positions collection as real evidence. |

## Safety Boundaries

```text
read_only_queries_only=true
placeOrder=false
cancelOrder=false
reqOpenOrders=false
reqAllOpenOrders=false
screenshot_used_for_funds_positions=false
direct_browser_tws_route=false
direct_backend_tws_route=false
raw_secret_values_recorded=false
raw_broker_endpoint_recorded=false
raw_config_file_contents_recorded=false
```

## Knowledge Update Rule

After a successful TWS login/API enablement and real closeout, update this card with:

1. The latest non-secret config shape, such as `socketClient=true`, `allowOnlyLocalhost=true`, and sanitized port ref.
2. The closeout artifact refs and timestamps.
3. Any non-secret operator step that was required, such as restart/reconnect or an API popup acknowledgement.
4. The exact verification commands that passed.

Do not record passwords, auth codes, raw endpoints, raw XML or funds/positions values in this card. Funds and positions stay in runtime artifacts and Account Mirror projections, not in the knowledge card.

## Success Backfill Template

When `output/account_capability/ib-live-u3028269/real-acceptance-closeout.json` reaches `status=ready`, append a dated entry under this section using only the fields below.

The draft can be prepared from current artifacts with:

```bash
python scripts/prepare_ib_tws_u3028269_login_api_knowledge_backfill.py
python scripts/validate_ib_tws_u3028269_login_api_knowledge_backfill.py
```

The draft artifact is `output/account_capability/ib-live-u3028269/knowledge-backfill-draft.json`. If closeout remains blocked, the draft status must remain `blocked_not_ready` and must not be appended as a success entry.

### 2026-06-20 Successful TWS API Login/API Enablement

- closeout_status: ready
- closeout_ref: output/account_capability/ib-live-u3028269/real-acceptance-closeout.json
- current_state_refresh_ref: output/account_capability/ib-live-u3028269/current-state-closeout-refresh.json
- socket_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json
- config_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-config-diagnostic.json
- account_summary_ref: output/account_capability/ib-live-u3028269/tws-api/account_summary.json
- positions_ref: output/account_capability/ib-live-u3028269/tws-api/positions.json
- executions_ref: output/account_capability/ib-live-u3028269/tws-api/executions.json
- source_package_ref: output/account_capability/ib-live-u3028269/source-package.json
- durable_store_reload_ref: output/account_capability/ib-live-u3028269/durable-store-reload.json
- completion_audit_ref: docs/proposals/p019-broker-observation-session-foundation/p019-completion-audit.json
- real_ui_parity_ref: docs/acceptance/2026-06-20-p019-u3028269-real-ui-parity-evidence.json
- sanitized_config_shape: runtime_handshake_ok=true, latest_static_socketClient=false, allowOnlyLocalhost=true, port_ref=7497
- readiness_shape: handshake_ok=true, account_summary_success=true, positions_success=true, source_package_state=ready, real_ui_parity_verdict=pass
- report_store_non_claims: executions_query_success=true, execution_report_rows=0, complete_history_claimed=false, durable_reload_state=partial, durable_reload_parity=blocked, completion_overall_status=not_complete
- non_secret_operator_steps_required: logged-in TWS API socket was enabled by local operator before collection; no external config write or reinstall was performed by this worktree
- verification_commands:
  - python scripts/validate_p019_u3028269_current_state_closeout_refresh.py
  - python scripts/validate_p019_u3028269_real_acceptance_closeout.py
  - python scripts/validate_p019_runtime_evidence_freshness.py
  - python scripts/validate_p019_broker_observation_foundation.py
- raw_secret_values_recorded=false
- raw_broker_endpoint_recorded=false
- raw_config_file_contents_recorded=false
- funds_positions_values_recorded_in_knowledge=false
- screenshot_used_for_funds_positions=false
- order_action_sent=false

```text
### YYYY-MM-DD Successful TWS API Login/API Enablement

- closeout_status: ready
- closeout_ref: output/account_capability/ib-live-u3028269/real-acceptance-closeout.json
- current_state_refresh_ref: output/account_capability/ib-live-u3028269/current-state-closeout-refresh.json
- socket_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-socket-diagnostic.json
- config_diagnostic_ref: output/debug/p019-tws-api-readiness/tws-api-config-diagnostic.json
- account_summary_ref: output/account_capability/ib-live-u3028269/tws-api/account_summary.json
- positions_ref: output/account_capability/ib-live-u3028269/tws-api/positions.json
- executions_ref: output/account_capability/ib-live-u3028269/tws-api/executions.json
- source_package_ref: output/account_capability/ib-live-u3028269/source-package.json
- durable_store_reload_ref: output/account_capability/ib-live-u3028269/durable-store-reload.json
- completion_audit_ref: docs/proposals/p019-broker-observation-session-foundation/p019-completion-audit.json
- real_ui_parity_ref: docs/acceptance/2026-06-20-p019-u3028269-real-ui-parity-evidence.json
- sanitized_config_shape: socketClient=true, allowOnlyLocalhost=true, port_ref=7497
- readiness_shape: handshake_ok=true, account_summary_success=true, positions_success=true
- report_store_non_claims: executions_query_success=<true|false>, execution_report_rows=<n>, complete_history_claimed=false, durable_reload_state=<partial|complete>, durable_reload_parity=<blocked|passed>, completion_overall_status=<not_complete|complete>
- non_secret_operator_steps_required: <for example restart/reconnect/API popup acknowledgement, or none>
- verification_commands:
  - python scripts/validate_p019_u3028269_current_state_closeout_refresh.py
  - python scripts/validate_p019_u3028269_real_acceptance_closeout.py
  - python scripts/validate_p019_runtime_evidence_freshness.py
  - python scripts/validate_p019_broker_observation_foundation.py
- raw_secret_values_recorded=false
- raw_broker_endpoint_recorded=false
- raw_config_file_contents_recorded=false
- funds_positions_values_recorded_in_knowledge=false
- screenshot_used_for_funds_positions=false
- order_action_sent=false
```

If closeout remains blocked, do not create a success entry. Keep the current blocker in P019 runtime artifacts instead.
