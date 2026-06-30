# Acceptance

## Guard-First Evidence

| Scenario | Command | Expected |
| --- | --- | --- |
| red | `git ls-files | ? { $_ -match '^(docs/acceptance/browser-evidence/|docs/proposals/).+\.(png|jpg|jpeg|gif|html|jsonl|pdf)$' } | Measure-Object | % Count` | nonzero before retirement; observed `112` |
| red-follow-up | `python -m pytest backend\tests\test_adr0010_wi2_generated_artifact_retirement.py -q` | failed before retirement on tracked `.pytest_tmp/**`, `*browser-evidence.json`, and `*acceptance-evidence.json` |
| green | repeat red command | `0` after retirement |
| green-guard | `python -m pytest backend\tests\test_adr0010_wi2_generated_artifact_retirement.py -q` | passed; tracked `output/**`, `.pytest_tmp/**`, browser evidence, and acceptance evidence are zero |
| fresh-clone | repeat green command after clean checkout | `0` |

## Risk-Control Scenarios

- RC-2 WI-2 inventory classification: browser evidence artifacts classified in Batch 0 carrier.
- RC-3 WI-2 post-retirement guard: tracked browser evidence must be zero and ignore rules must match representative evidence paths.
- RC-6 Evidence replay: commands above are the replay surface.

## Compatibility

Historical browser screenshots may remain in an existing local checkout but are no longer source-of-truth acceptance evidence.
Current UI acceptance must be regenerated from tests, code, and proposal acceptance criteria.
