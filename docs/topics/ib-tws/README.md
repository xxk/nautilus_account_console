# IB TWS Topic / IB TWS 专题入口

- Topic ID: `ib-tws`
- Status: active
- Updated: 2026-06-20
- Scope: non-secret IB TWS operational knowledge for Account Console observation work

## Purpose

This topic collects long-lived, non-secret IB TWS knowledge that should survive individual proposals and chat context.

It does not own broker truth, account truth, order truth, login secrets, raw TWS configuration or trading readiness.

## Knowledge Cards

| Card | Status | Purpose |
| --- | --- | --- |
| [U3028269 TWS login and API knowledge](./u3028269-tws-login-and-api-knowledge.md) | pre-login-success baseline | Repeatable non-secret workflow for U3028269 TWS login/API enablement, readiness checks, real closeout refs and safe success backfill. |

## Rules

1. Record repeatable process knowledge, sanitized config shape and verification commands only.
2. Do not record passwords, 2FA/auth codes, raw `tws.xml`, raw broker endpoints or account secrets.
3. Do not record funds/positions values in topic docs; keep those in runtime artifacts and Account Mirror projections.
4. Do not treat screenshots as funds/positions/account truth.
5. Do not authorize order actions from this topic.
6. Real acceptance remains with the active proposal/acceptance artifacts, currently P019/ADR-0005.
