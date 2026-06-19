# CTP Source Owner Package Handoff

- Date: 2026-06-15
- Status: blocked_waiting_for_source_owner_packages
- Owner expected: `nautilus_ctp_adapter`
- Consumer: Account Console Account Mirror
- Scope: pinned read-only CTP source packages for ADR-0004 / ADR-0047 / T001 / P011 real readback acceptance

## Purpose

Account Console can already render API-backed Account Mirror projections and fail closed when source packages are missing. To verify broker-current CTP paper/live funds, positions and orders, the source owner must publish pinned read-only source packages.

These packages must be produced by the source owner. Account Console must not call CTP directly and must not fabricate broker truth.

ADR-0047 also requires route/context separation. A source package proves only the read-only source snapshot for one account/query window. It does not create `AccountRuntimeContext`, route resolver, runtime builder, order truth, account ledger truth or readiness truth. Account Console consumes the package as projection input and must still show or block route/context fields before UI consistency can close.

## Required Packages

| Account | Domain | Required package path | Template | Current blocker | Validation |
| --- | --- | --- | --- | --- | --- |
| `acct.ctp.paper.19053` | CTP paper | `output/account_capability/ctp-paper-19053/source-package.json` | `contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json` | `docs/acceptance/2026-06-15-ctp19053-real-readback-blocker.json` | `python scripts\validate_ctp19053_consistency.py --source-package output\account_capability\ctp-paper-19053\source-package.json` |
| `acct.ctp.live.025292` | CTP live | `output/account_capability/ctp-live-025292/source-package.json` | `contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json` | `docs/acceptance/2026-06-15-ctp025292-real-account-consistency-blocker.json` | `python scripts\validate_ctp025292_consistency.py --source-package output\account_capability\ctp-live-025292\source-package.json` |

## Snapshot Input Contract

Each package must represent one read-only query window:

```text
QryTradingAccount
QryInvestorPosition
QryOrder
QryTrade when fills exist or order fill state needs verification
```

Required snapshot metadata:

```text
trading_day
query_window_id
query_started_at
query_completed_at
observed_at
source_ref
source_checksum
observation_mode=snapshot
event_stream=not_implemented
```

Required ADR-0047 routing metadata, either in the source package or in a companion route/context artifact referenced by checksum:

```text
route_id
account_alias
market_data_source
execution_adapter
account_truth
risk_domain
evidence_partition
```

If the route/context artifact is missing, Account Console must render a typed blocker rather than claim real-account UI consistency.

## Safety Boundary

The source package must not include:

```text
password
auth_code
authcode
token
secret
session_password
command
```

The source package must not claim:

```text
Paper ready
Live ready
production ready
capital allocated
broker tradable
can trade
```

## Acceptance Commands

Default fail-closed blocker refresh:

```powershell
python scripts\validate_ctp19053_consistency.py --write-blocker
python scripts\validate_ctp025292_consistency.py --write-blocker
```

Sample harness checks, which prove comparison logic only:

```powershell
python scripts\validate_ctp19053_consistency.py --source-package contracts\source_artifacts\samples\ctp_paper_19053_sample_source.json
python scripts\validate_ctp025292_consistency.py --source-package contracts\source_artifacts\samples\ctp_live_025292_sample_source.json
```

After source owner publishes real packages, run:

```powershell
python scripts\validate_ctp19053_consistency.py --source-package output\account_capability\ctp-paper-19053\source-package.json
python scripts\validate_ctp025292_consistency.py --source-package output\account_capability\ctp-live-025292\source-package.json
python scripts\validate_adr004_p011_landing_consistency.py
```

## Current State

Current manual UI entry remains:

```text
http://127.0.0.1:5175/accounts/acct.demo-19053
```

The broker-current CTP Paper account route is:

```text
http://127.0.0.1:5175/accounts/acct.ctp.paper.19053
```

The legacy `acct.demo-19053` route is a compatibility/manual-entry route and must not be treated as broker-current truth. Historical checked-in/sample evidence proves UI comparison mechanics only.

Both real-source acceptances remain blocked until source-owner packages exist at the required output paths. The blockers are accepted fail-closed evidence, not passed real account consistency.
