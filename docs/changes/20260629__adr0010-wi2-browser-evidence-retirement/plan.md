---
change-id: 20260629__adr0010-wi2-browser-evidence-retirement
status: completed
topic-id: adr0010-wi2
---

# ADR-0010 WI-2 Browser Evidence Retirement - nautilus_account_console

> Completed. Historical browser evidence JSON and pytest scratch artifacts are
> retired from the source layer; the guard in
> `backend/tests/test_adr0010_wi2_generated_artifact_retirement.py` prevents
> tracked `output/**`, `.pytest_tmp/**`, and browser/acceptance evidence JSON
> from returning.

## Scope

- Retire tracked historical browser-evidence images and proposal demo HTML from source control.
- Add ignore rules so generated UI evidence does not return to the source layer.
- Do not change frontend runtime, API code, or WI-7 codegen drift work.

## Acceptance

See `acceptance.md`.

## Rollback Boundary

This change is limited to `.gitignore`, this change bundle, and index retirement of historical UI evidence artifacts.
It is independent from WI-7.
