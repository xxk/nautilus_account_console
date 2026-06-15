# Source Artifact Templates

These templates define the shape of source-owner artifacts that Account Console may read through Account Mirror. They are not runtime truth and must not be copied into UI fixtures as accepted account values.

## CTP Paper 19053

Template:

```text
contracts/source_artifacts/templates/ctp_paper_19053_source_package.template.json
```

Required output path for the real acceptance run:

```text
output/account_capability/ctp-paper-19053/source-package.json
```

The source owner should populate the package from one read-only CTP paper snapshot window:

```text
QryTradingAccount
QryInvestorPosition
QryOrder
QryTrade when fills exist or order fill state needs verification
```

Validation command:

```powershell
python scripts\validate_ctp19053_consistency.py --source-package output\account_capability\ctp-paper-19053\source-package.json
```

Boundary:

1. Do not include passwords, auth codes, tokens, secrets or session passwords.
2. Do not include a `command` object.
3. Keep `account_id` as `acct.ctp.paper.19053`; `19053` is only the display alias.
4. Keep `observation_mode=snapshot` and `event_stream=not_implemented` unless a successor polling/event-driven acceptance is approved.
5. Account Console must remain read-only and must not call CTP directly.

## CTP Live 025292

Template:

```text
contracts/source_artifacts/templates/ctp_live_025292_source_package.template.json
```

Required output path for the real acceptance run:

```text
output/account_capability/ctp-live-025292/source-package.json
```

The source owner should populate the package from one read-only CTP snapshot window:

```text
QryTradingAccount
QryInvestorPosition
QryOrder
QryTrade when fills exist or order fill state needs verification
```

Validation command:

```powershell
python scripts\validate_ctp025292_consistency.py --source-package output\account_capability\ctp-live-025292\source-package.json
```

Boundary:

1. Do not include passwords, auth codes, tokens, secrets or session passwords.
2. Do not include a `command` object.
3. Keep `account_id` as `acct.ctp.live.025292`; `025292` is only the display alias.
4. Keep `observation_mode=snapshot` and `event_stream=not_implemented` unless a successor polling/event-driven acceptance is approved.
5. Account Console must remain read-only and must not call CTP directly.
