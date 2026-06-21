---
id: KB-BUG-0002
type: bug
scope: project-local
area: read-model
status: active
source_ref: docs/adr/0004-adopt-account-mirror-observation-and-command-plane.md
prevention_gate: python scripts/check_knowledge_docs.py --root .
shared_pattern_ref: D:/Nautilus/global_docs/knowledge-common/validation-playbook.md
---

# Raw Report Treated As Account Truth

## Symptom

Raw broker payloads, screenshots or debug provenance are treated as canonical account, order, fill, funds or position truth.

## Trigger

AI sees raw callback/report wording and skips the normalized read-model or Account Mirror boundary.

## Root Cause

Debug provenance is mistaken for the projection contract.

## Correct Action

Map observed payloads into typed read models or Account Mirror projections, then use those projections for UI and acceptance.

## Wrong Action

Do not parse raw broker payloads in the browser as truth. Do not use screenshots or raw report blobs as formal account/order truth.

## Prevention Gate

`python scripts/check_knowledge_docs.py --root .`

## Source Ref

ADR-0004 Account Mirror boundary and ADR-0006 knowledge anti-drift rules.

