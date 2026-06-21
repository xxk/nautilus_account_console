---
id: KB-BUG-0001
type: bug
scope: project-local
area: ui-projection
status: active
source_ref: docs/adr/0006-adopt-project-local-and-shared-knowledge-base.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/validation-playbook.md
---

# Readiness Claim Leaked Into Read-Only Console

## Symptom

UI or docs imply that an account observation surface grants operational readiness or trading ability.

## Trigger

The UI has source health, readback, account identity or broker observation data, and AI tries to summarize it as ready.

## Root Cause

Observation and projection are confused with admission, capital, approval or command authority.

## Correct Action

Use typed blocker/readback wording and keep command disabled unless a separate accepted command authority exists.

## Wrong Action

Do not claim readiness, admission, capital approval, broker tradability or ability to trade from Account Console UI or knowledge cards.

## Prevention Gate

`python scripts/check_knowledge_docs.py --root .`

## Source Ref

ADR-0006 and Account Console AGENTS read-only boundary.

