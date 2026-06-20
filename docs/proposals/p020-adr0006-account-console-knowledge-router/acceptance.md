# P020 ADR-0006 Account Console Knowledge Router Acceptance / 验收

- Proposal ID: `p020-adr0006-account-console-knowledge-router`
- Status: implementation_gate_passed
- Created: 2026-06-20
- Updated: 2026-06-20
- Linked proposal: [README.md](README.md)
- Linked phase plan: [phase-plan.md](phase-plan.md)
- ADR anchor: [ADR-0006](../../adr/0006-adopt-project-local-and-shared-knowledge-base.md)

## Acceptance Scope / 验收范围

This proposal accepts only the governance landing of ADR-0006:

1. A project-local knowledge skeleton for Account Console.
2. A blocker/symptom-to-card Knowledge Router.
3. A Prevention Gate that rejects structural drift, route drift, truth-source drift and obvious secret/runtime leakage.
4. Anti-drift rules that keep shared knowledge, project facts and current acceptance truth separated.

This proposal does not accept:

1. Runtime, broker, account, admission, approval, capital or trading-readiness truth.
2. Any ADR-0005/P019 broker observation completion.
3. Any Obsidian/plugin/local UI state as formal governance truth.
4. Any knowledge card as a substitute for current proposal/change acceptance.

## ADR Carrier Acceptance Matrix

| ID | ADR decision item | Positive path | Must fail if | Authority / boundary | Minimal evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Shared vs project-local split | `docs/knowledge/README.md` links to `D:\Nautilus\global_docs\knowledge-common` and states project facts stay local | Project owner facts, local commands or bug evidence are copied into shared knowledge as global truth | shared knowledge owns patterns only; project knowledge owns facts | README plus gate check | passed |
| A2 | Knowledge as non-truth-source | knowledge docs explicitly forbid current status, readiness, acceptance verdicts and account/broker/runtime truth | a card claims current pass/fail, readiness, broker truth, capital/admission truth or acceptance completion | proposal/change/acceptance remain truth source | forbidden-content gate | passed |
| A3 | Knowledge Router | `blocker-routing.json` maps symptoms to matched local cards and optional shared patterns | router output declares verdict, acceptance, readiness, owner transfer or blocker closure | router is advisory reading scope only | route target validation | passed |
| A4 | Prevention Gate | `scripts/check_knowledge_docs.py` checks required files, required card fields, route targets and forbidden content | gate is missing, positive-only, or ignores dangling route targets / forbidden truth-source wording | gate prevents repeat drift but does not close proposal acceptance alone | command pass signal | passed |
| A5 | Repeat-bug memory | bug cards include source_ref, correct_action, wrong_action and prevention_gate | bug card is prose-only, lacks source ref, or has no prevention/gate routing | bug ledger is reusable failure memory, not issue tracking | seed bug cards and template | passed |
| A6 | AI minimal-read discipline | docs say AI reads current task truth first, then router, then matched cards only | AGENTS/README tells AI to read full shared/project knowledge by default | current task truth wins over knowledge | README/router wording plus gate | passed |
| A7 | Cross-project learning | adoption note says other projects copy structure and rewrite local facts/routes | other projects are instructed to copy Account Console owner facts or bug cards verbatim | structure is reusable; facts are not | adoption note | passed |
| A8 | Obsidian boundary | docs allow Obsidian only as read-only projection over Git Markdown | `.obsidian`, Canvas, plugin state or local workspace state becomes truth source | Git Markdown is source | README wording | passed |
| A9 | Secret/runtime boundary | gate rejects obvious raw secret/runtime fields and docs require secret refs only | card contains raw password/auth/front/API key/account secret or owner runtime material | secret-bearing material stays outside knowledge cards | forbidden-content gate | passed |

## Anti-Drift Matrix / 防跑偏验收

| ID | Drift type | Must fail if | Rejection signal | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| N1 | current-state leakage | any knowledge card records active proposal status, acceptance pass/fail, live readiness or blocker closure as knowledge truth | `knowledge_truth_source_drift` | `check_knowledge_docs.py` | planned |
| N2 | shared/project mixing | Account Console owner map, local commands, P019/P020 evidence or local bug details are copied into `knowledge-common` as shared truth | `shared_project_fact_leak` | source review / gate if local refs appear in shared-pattern refs | planned |
| N3 | acceptance substitution | a knowledge card or route rule is cited as the only evidence for proposal/change completion | `knowledge_not_acceptance_evidence` | acceptance review | planned |
| N4 | context flooding | default AI instructions require reading all `knowledge-common` or all `docs/knowledge` before every task | `full_library_read_default_forbidden` | README/router text scan | planned |
| N5 | route drift | `blocker-routing.json` points to missing files, unapproved shared paths or route rules without `must_not` boundaries | `route_target_missing_or_unbounded` | route target validation | planned |
| N6 | cross-project copy drift | adoption note tells other projects to copy Account Console owner facts, paths or bug cards without rewriting them | `project_fact_copy_forbidden` | adoption note review | planned |
| N7 | secret/runtime leakage | docs/knowledge contains raw password/auth code/front/API key/account secret, raw config body, raw endpoint value, funds/positions truth value or order action instruction | `knowledge_secret_or_runtime_leak` | forbidden-content gate | planned |
| N8 | gate-as-acceptance drift | `check_knowledge_docs.py` pass is written as formal proposal closeout without skeleton/card/router evidence | `gate_pass_not_closeout` | acceptance review | planned |

## Initial Route Families / 初始路由族

| Route family | Trigger examples | Required local cards | Optional shared pattern | Must not |
| --- | --- | --- | --- | --- |
| readiness-wording | `Paper ready`, `Live ready`, `can trade`, `admitted` | `ui-projection-boundary.md`, readiness bug card | shared fake-acceptance/readiness pattern if available | claim readiness from UI or knowledge |
| raw-report-truth | raw callback, raw report, broker payload, screenshot truth | `account-console-read-model-boundary.md`, raw-report bug card | shared truth-source pattern if available | parse raw payload as account/order truth |
| secret-runtime-material | password, auth code, front, API key, raw config | `runtime-secret-boundary.md` | shared secret-leak pattern if available | copy raw secrets into docs/chat/evidence |
| owner-boundary-confusion | command, broker session, mirror, runtime owner | `owner-boundaries.md`, `project-playbook.md` | owner-boundary shared pattern if available | create second runtime or owner |

## Scenario Matrix / 验收场景矩阵

Every positive scenario below has a paired anti-drift scenario. A future implementation cannot close P020 by passing only happy-path structure checks.

| ID | Type | Scenario | Verification | Pass signal | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | success | Knowledge skeleton exists with README, dashboard, project playbook, boundary docs, bug ledger and template | `python scripts/check_knowledge_docs.py --root .` | `KNOWLEDGE_DOCS_OK` with required files present | planned |
| D1 | drift | A required file is missing, or the dashboard contains progress/readiness/pass-fail status | same gate | `knowledge_required_file_missing` or `knowledge_dashboard_status_drift` | planned |
| S2 | success | Shared/project split is explicit: shared knowledge links are references, project facts remain local | gate plus source review | `shared_project_split_ok` | planned |
| D2 | drift | Account Console owner facts, local commands, evidence, P019/P020 details or local bug narratives are promoted into shared knowledge as global truth | gate/source review | `shared_project_fact_leak` | planned |
| S3 | success | `blocker-routing.json` maps each initial route family to existing local cards and optional approved shared patterns | route target validation | `knowledge_routes_ok` | planned |
| D3 | drift | A route points to a missing file, an unapproved external/shared path, or lacks `must_not` boundaries | route target validation | `route_target_missing_or_unbounded` | planned |
| S4 | success | Router output is advisory reading scope only: matched cards, optional gates and must-not boundaries | route schema validation | `router_advisory_only=true` | planned |
| D4 | drift | Router rule declares readiness, acceptance, owner transfer, blocker closure, or pass/fail verdict | route schema validation | `router_verdict_forbidden` | planned |
| S5 | success | AI reading order is current task truth -> router -> matched cards only | README/playbook scan | `minimal_read_policy_ok` | planned |
| D5 | drift | README, playbook or AGENTS-facing text instructs AI to read all shared/project knowledge by default | text scan | `full_library_read_default_forbidden` | planned |
| S6 | success | Bug cards include frontmatter plus symptom, trigger, root_cause, correct_action, wrong_action, prevention_gate and source_ref | card validation | `bug_cards_ok` | planned |
| D6 | drift | Bug card is prose-only, has no source ref, has no prevention gate, or records open task state as bug memory | card validation | `bug_card_contract_violation` | planned |
| S7 | success | Prevention Gate rejects obvious secret/runtime fields and truth-source claims | negative fixture or temp file check | `forbidden_content_rejected` | planned |
| D7 | drift | Knowledge docs contain raw password/auth/front/API key/account secret, raw endpoint/config body, funds/positions truth value, order action instruction, or trading-readiness claim | negative fixture or temp file check | `knowledge_secret_or_runtime_leak` | planned |
| S8 | success | Gate pass is recorded as guard evidence only; proposal closeout also requires skeleton, route and card evidence | acceptance review | `gate_pass_not_closeout_boundary_ok` | planned |
| D8 | drift | `check_knowledge_docs.py` pass alone is used as formal proposal closeout while required files/cards/routes are absent | acceptance review | `gate_pass_not_closeout` | planned |
| S9 | success | Cross-project adoption note tells other projects to copy structure, then rewrite local owner boundaries, route rules and bug cards | adoption note review | `cross_project_adoption_boundary_ok` | planned |
| D9 | drift | Adoption note tells other projects to copy Account Console facts, paths, P019/P020 evidence or bug cards verbatim | adoption note review | `project_fact_copy_forbidden` | planned |
| S10 | success | Obsidian is documented as read-only projection over Git Markdown | README/adoption note review | `obsidian_projection_only_ok` | planned |
| D10 | drift | `.obsidian`, Canvas, plugin state or local workspace state is described as governance truth or route authority | README/adoption note review | `obsidian_truth_source_forbidden` | planned |
| S11 | success | Route schema requires each rule to declare `id`, `when`, `read`, `must_not`, `gate` and `owner_boundary` | route schema validation | `route_schema_ok` | planned |
| D11 | drift | A route rule has broad trigger text but no owner boundary, no must-not list, or no verification gate | route schema validation | `route_rule_underconstrained` | planned |
| S12 | success | Route matching can return both local cards and shared patterns, but shared paths are explicit and project-independent | route target validation | `shared_pattern_refs_ok` | planned |
| D12 | drift | Route sends AI to whole `D:\Nautilus\global_docs\knowledge-common` or whole `docs/knowledge` instead of specific files | route target validation | `route_directory_target_forbidden` | planned |
| S13 | success | Promotion loop is documented: evidence first in proposal/change acceptance, stable lesson second in bug card, generic pattern third in shared knowledge, machine-checkable rule fourth in gate | README/playbook scan | `promotion_loop_ok` | planned |
| D13 | drift | Stable lesson is written straight to shared knowledge or bug ledger before current evidence/source_ref exists | README/playbook/gate review | `promotion_without_source_ref_forbidden` | planned |
| S14 | success | Negative fixtures or temp fixtures exist for each anti-drift family and are rejected by `check_knowledge_docs.py` | gate fixture review | `knowledge_negative_fixtures_ok` | planned |
| D14 | drift | Gate only checks positive structure and has no negative fixture coverage for route drift, truth-source drift, secret leakage or full-library read defaults | gate fixture review | `knowledge_gate_positive_only_forbidden` | planned |
| S15 | success | Knowledge card frontmatter uses stable fields: `id`, `type`, `scope`, `area`, `status`, `source_ref`, `prevention_gate`, `shared_pattern_ref` | card validation | `knowledge_frontmatter_ok` | planned |
| D15 | drift | Card frontmatter includes current proposal state fields such as `current_task`, `acceptance_status`, `ready`, `admitted`, `can_trade`, `capital_status` or live blocker closure | card validation | `knowledge_frontmatter_state_leak` | planned |
| S16 | success | Account Console-specific route families do not become mandatory shared route families for other projects | adoption note review | `project_route_locality_ok` | planned |
| D16 | drift | Adoption note or shared template requires every project to inherit Account Console route ids, owner names, broker examples or UI labels | adoption note review | `project_route_template_overreach` | planned |
| S17 | success | Gate error messages are typed and actionable enough for AI repair: missing path, forbidden claim, dangling route, secret leak, state leak, directory target | gate behavior review | `typed_repair_signals_ok` | planned |
| D17 | drift | Gate only emits generic failure text that does not identify route id, file path, field or forbidden pattern | gate behavior review | `generic_gate_error_forbidden` | planned |
| S18 | success | AGENTS/README integration states knowledge lookup is conditional and subordinate to current task truth | README/AGENTS review | `agent_knowledge_precedence_ok` | planned |
| D18 | drift | AGENTS/README integration puts knowledge lookup before current proposal/change/acceptance or lets knowledge override task constraints | README/AGENTS review | `agent_precedence_inversion` | planned |
| S19 | success | Router smoke returns the readiness boundary card and readiness bug card for a readiness-like input | `python scripts/route_knowledge.py --root . --query "can trade"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2` | passed |
| D19 | drift | Router smoke returns the whole knowledge directory, whole shared knowledge base, or no cards for a known readiness trigger | router smoke | `route_smoke_target_drift` | planned |
| S20 | success | Router smoke returns raw-report boundary and raw-report bug card for raw payload/screenshot truth input | `python scripts/route_knowledge.py --root . --query "raw broker payload screenshot truth"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2` | passed |
| D20 | drift | Raw-report query routes to readiness, secret or owner cards instead of read-model boundary cards | router smoke | `route_smoke_family_mismatch` | planned |
| S21 | success | Router smoke returns only advisory reading scope and `must_not` boundaries, never verdict or acceptance fields | route JSON and smoke output review | `route_smoke_advisory_only_ok` | passed |
| D21 | drift | Router smoke output includes `verdict`, `acceptance`, readiness, owner transfer, blocker closure or pass/fail conclusion | router smoke | `route_smoke_verdict_forbidden` | planned |
| S22 | success | No-match input returns a typed no-match signal and tells AI to continue from current task truth, not to read the full library | `python scripts/route_knowledge.py --root . --query "unrelated styling typo"` | `ROUTE_KNOWLEDGE_NO_MATCH` | passed |
| D22 | drift | No-match input falls back to full `knowledge-common` or full `docs/knowledge` scan | router smoke | `route_smoke_full_library_fallback_forbidden` | planned |

## Positive-to-Negative Coverage Map

| Positive scenario | Required anti-drift rows | Coverage rule |
| --- | --- | --- |
| S1 Knowledge skeleton | D1 | Skeleton cannot pass if required files are missing or dashboard carries status truth. |
| S2 Shared/project split | D2 | Split cannot pass if project facts leak into shared knowledge. |
| S3 Route target validity | D3 | Route validation cannot pass with dangling or unbounded route targets. |
| S4 Router advisory-only | D4 | Router cannot pass if it declares verdicts or current task conclusions. |
| S5 Minimal-read discipline | D5 | AI routing cannot pass if full-library reading is the default. |
| S6 Bug card contract | D6 | Bug ledger cannot pass with prose-only cards or open-task state. |
| S7 Secret/runtime boundary | D7 | Knowledge gate cannot pass if secret/runtime/trading truth appears in cards. |
| S8 Gate boundary | D8 | Prevention gate cannot be the only closeout evidence. |
| S9 Cross-project adoption | D9 | Adoption cannot pass if it tells projects to copy local facts. |
| S10 Obsidian boundary | D10 | Obsidian support cannot pass if local UI/plugin state becomes truth. |
| S11 Route schema | D11 | Route schema cannot pass with underconstrained broad matching rules. |
| S12 Specific route targets | D12 | Route targets cannot be whole directories or whole knowledge bases. |
| S13 Promotion loop | D13 | Lessons cannot be promoted without source evidence first. |
| S14 Negative fixtures | D14 | Prevention gate cannot be positive-only. |
| S15 Card frontmatter | D15 | Knowledge card metadata cannot carry live state or readiness fields. |
| S16 Project route locality | D16 | Account Console route facts cannot become mandatory shared template facts. |
| S17 Typed repair signals | D17 | Gate failures must be actionable enough for AI repair. |
| S18 Agent precedence | D18 | Knowledge lookup cannot outrank current task truth. |
| S19 Readiness router smoke | D19 | Known readiness-like inputs must route to exact local cards, not whole libraries. |
| S20 Raw-report router smoke | D20 | Known raw-report inputs must route to read-model boundary cards. |
| S21 Advisory-only smoke | D21 | Router output cannot contain verdict or acceptance conclusions. |
| S22 No-match smoke | D22 | Unknown inputs cannot trigger full-library fallback. |

## Route Schema Contract / 路由 Schema 契约

The first implementation of `docs/knowledge/blocker-routing.json` must be small but explicit. This proposal accepts the following minimum shape:

```json
{
  "version": 1,
  "scope": "project-local",
  "extends": "D:/Nautilus/global_docs/knowledge-common/router-base.json",
  "rules": [
    {
      "id": "account-console-readiness-wording",
      "when": ["paper ready", "live ready", "can trade", "admitted"],
      "read": [
        "docs/knowledge/ui-projection-boundary.md",
        "docs/knowledge/bug-ledger/KB-BUG-0001__readiness-claim-leaked-into-readonly-console.md"
      ],
      "shared_patterns": [],
      "must_not": [
        "claim readiness from UI",
        "write admission, capital, broker or trading truth"
      ],
      "owner_boundary": "account-console-read-only-projection",
      "gate": "python scripts/check_knowledge_docs.py --root ."
    }
  ]
}
```

Route schema anti-drift:

1. `read` and `shared_patterns` must point to files, not directories.
2. `shared_patterns` may reference only project-independent shared patterns.
3. `must_not` must not be empty.
4. `owner_boundary` must not be empty.
5. `gate` must not be empty for any rule that maps a repeatable failure pattern.
6. A route rule must not contain `verdict`, `acceptance`, `ready`, `admitted`, `can_trade`, `pass`, `closeout` or equivalent current-state authority fields.

## Negative Fixture Requirements / 负向 Fixture 要求

The successor implementation should include repo-local negative fixtures or temporary fixture generation for at least:

| Fixture ID | Drift represented | Expected rejection |
| --- | --- | --- |
| NF1 | route target points to `docs/knowledge/` directory | `route_directory_target_forbidden` |
| NF2 | route rule declares `verdict: pass` | `router_verdict_forbidden` |
| NF3 | card frontmatter has `acceptance_status: passed` | `knowledge_frontmatter_state_leak` |
| NF4 | card body contains raw secret placeholder wording or raw endpoint field | `knowledge_secret_or_runtime_leak` |
| NF5 | dashboard contains `Paper ready` or `Live ready` as current status | `knowledge_dashboard_status_drift` |
| NF6 | bug card has no `source_ref` or `prevention_gate` | `bug_card_contract_violation` |
| NF7 | README tells AI to read all `knowledge-common` before every task | `full_library_read_default_forbidden` |
| NF8 | adoption note tells projects to copy Account Console bug cards verbatim | `project_fact_copy_forbidden` |

## Required Before Implementation Closeout

1. `docs/knowledge/README.md` exists and states precedence, no-truth-source boundary and shared knowledge link.
2. `docs/knowledge/00-dashboard.md` exists and is navigation-only.
3. `docs/knowledge/blocker-routing.json` exists and covers the four initial route families.
4. `docs/knowledge/project-playbook.md`, `owner-boundaries.md`, `account-console-read-model-boundary.md`, `ui-projection-boundary.md` and `runtime-secret-boundary.md` exist.
5. `docs/knowledge/bug-ledger/README.md` and at least two seed bug cards exist.
6. `docs/knowledge/templates/bug-card.md` exists and requires source_ref, correct_action, wrong_action and prevention_gate.
7. `scripts/check_knowledge_docs.py --root .` passes and rejects the anti-drift cases above.
8. `scripts/route_knowledge.py --root . --query "can trade"` returns the readiness route and exact local cards.
9. `scripts/route_knowledge.py --root . --query "raw broker payload screenshot truth"` returns the raw-report route and exact local cards.
10. `scripts/route_knowledge.py --root . --query "unrelated styling typo"` returns a typed no-match without full-library fallback.
11. `python scripts/check_proposal_docs.py --root . --proposal-id p020-adr0006-account-console-knowledge-router` passes.

## Phase 0 Evidence

| Evidence | Command / path | Result |
| --- | --- | --- |
| P020 acceptance-first proposal | `docs/proposals/p020-adr0006-account-console-knowledge-router/` | proposal docs created; implementation gate passed |
| Knowledge docs gate | `python scripts/check_knowledge_docs.py --root .` | `KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2` |
| Knowledge docs negative fixture selftest | `python scripts/check_knowledge_docs.py --root . --selftest` | `KNOWLEDGE_DOCS_OK: files=13 routes=4 bug_cards=2 negative_fixtures=8` |
| Readiness router smoke | `python scripts/route_knowledge.py --root . --query "can trade"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2`; reads `ui-projection-boundary.md` and `KB-BUG-0001` |
| Raw-report router smoke | `python scripts/route_knowledge.py --root . --query "raw broker payload screenshot truth"` | `ROUTE_KNOWLEDGE_OK: matches=1 cards=2`; reads `account-console-read-model-boundary.md` and `KB-BUG-0002` |
| No-match router smoke | `python scripts/route_knowledge.py --root . --query "unrelated styling typo"` | `ROUTE_KNOWLEDGE_NO_MATCH: read=0 action=current_task_truth` |
| Proposal docs gate | `python scripts/check_proposal_docs.py --root .` | `PROPOSAL_DOCS_OK: proposals=10` |
