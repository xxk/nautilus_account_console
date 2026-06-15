# DSLresearch Template Reference Mirror / DSLresearch 模板参考镜像

- Source root: `D:\Nautilus\DSLresearch`
- Copied on: 2026-06-13
- Selection rule: files whose path matches `template`, `_template`, `templates` or `模板`
- File count at copy time: 61

This directory is a reference mirror. It preserves source-relative paths so future work can compare, copy and trim known DSLresearch documentation and Gate/report template patterns without treating them as local runtime entries.

## Included Groups

| Source-relative group | Notes |
| --- | --- |
| `docs/adr/` | ADR template reference. |
| `docs/changes/_template/` | Change plan/design/constraints/acceptance templates. |
| `docs/codex/_template/` | Codex prompt/status templates. |
| `docs/findings/` | Review snapshot template. |
| `docs/proposals/_template/` | Proposal base, fragments, profiles and template metadata. |
| `docs/runbooks/_template/` | Runbook template reference. |
| `dslresearch/**/templates/` | Jinja/report surface templates for UI/report structure reference. |
| Other `*模板*` files | Historical or proposal-local template examples copied as references. |

## Adaptation Rules

1. Keep these files reference-only until a local account-console template is intentionally created.
2. Do not copy DSLresearch research, admission, approval, capital, factor-board or runtime ownership semantics into local truth paths.
3. Any local Gate/check adapted from these templates must declare its verdict scope and local evidence command.
4. Any UI/report template adapted from these files must keep `nautilus_account_console` read-only and avoid forbidden readiness/tradability wording.
