# P024 UI Design / Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase4zc_remaining_acceptance_state_ui_projection_passed

## Design Intent

The Account Workbench adds compact guarded paper command controls only when API projection declares `capabilities.command.enabled=true`, `capabilities.command.mode=paper_armed`, allowed actions include `submit` and `cancel`, and command evidence refs are present.

No controls are reserved or visible in disabled mode.

## Data Test ID Map

| Data Test ID | Purpose |
| --- | --- |
| `account-paper-command-banner` | paper-only command warning |
| `account-command-mode` | command mode display |
| `account-command-preflight-ref` | preflight source ref |
| `account-submit-order-form` | guarded submit form |
| `account-submit-order-button` | submit action |
| `account-submit-idempotency-key` | idempotency preview |
| `account-cancel-order-button` | cancel action |
| `account-cancel-order-identity` | readback identity used for cancel |
| `account-order-identity` | stable order identity displayed in order row |
| `account-order-status` | order row lifecycle status |
| `account-order-submitted-quantity` | submitted quantity display |
| `account-order-filled-quantity` | filled quantity display |
| `account-order-remaining-quantity` | remaining quantity display |
| `account-order-cancelled-quantity` | cancelled quantity display |
| `account-order-partial-fill-row` | partial-fill row marker |
| `account-remaining-cancel-quantity` | cancel target derived from remaining quantity |
| `account-cancel-pending-ref` | command audit ref while cancel is pending |
| `account-fill-source-ref` | fill readback source ref |
| `account-fill-quantity` | fill row quantity |
| `account-fill-price` | fill row price |
| `account-command-status-panel` | command status display |
| `account-command-risk-ref` | risk decision ref |
| `account-command-approval-ref` | approval decision ref |
| `account-command-gateway-ref` | gateway event ref |
| `account-command-readback-ref` | readback ref |
| `account-command-reconciliation-ref` | reconciliation ref |
| `account-command-blocker` | fail-closed blocker |
| `account-runtime-closeout-panel` | read-only runtime closeout evidence panel |
| `account-runtime-closeout-run-id` | owner-backed runtime run id |
| `account-runtime-closeout-status` | runtime closeout reconciliation status |
| `account-runtime-closeout-manifest-checksum` | closeout manifest checksum |
| `account-runtime-closeout-gateway-send` | predecessor runtime gateway send observed flag |
| `account-runtime-closeout-web-trigger` | browser-triggered broker order flag; must remain false |
| `account-runtime-closeout-raw-secret` | raw secret evidence flag; must remain false |
| `account-runtime-closeout-gateway-final` | gateway ack final-state flag; must remain false |
| `account-runtime-closeout-artifact-count` | count of checksum-backed runtime artifacts |
| `account-runtime-closeout-non-claim` | explicit non-claims shown in UI |
| `account-runtime-handoff-panel` | blocked owner-runtime handoff request panel |
| `account-runtime-handoff-action` | submit or cancel handoff action |
| `account-runtime-handoff-status` | handoff status; must be `blocked_until_owner_runtime_invocation` |
| `account-runtime-handoff-entrypoint` | owner runtime script ref |
| `account-runtime-handoff-config-ref` | owner runtime config ref without raw endpoint values |
| `account-runtime-handoff-readback-ref` | cancel readback ref used for owner-runtime handoff |
| `account-runtime-handoff-invoked` | owner runtime invocation flag; must remain false |
| `account-runtime-handoff-web-trigger` | browser-triggered broker order flag; must remain false |
| `account-runtime-handoff-raw-secret` | raw secret evidence flag; must remain false |
| `account-runtime-handoff-blocker` | typed blocker for owner invocation, external write approval and post-run ingest |
| `account-runtime-handoff-non-claim` | explicit non-claims shown in UI |
| `account-runtime-readiness-panel` | owner-runtime readiness blocker projection panel |
| `account-runtime-readiness-status` | readiness status; must remain blocked until external owner-runtime approval and artifacts exist |
| `account-runtime-readiness-owner` | owner runtime ref |
| `account-runtime-readiness-owner-path` | owner repo path requiring external write approval |
| `account-runtime-readiness-config-ref` | owner config ref without raw endpoint or secret values |
| `account-runtime-readiness-config-raw` | raw config content read flag; must remain false |
| `account-runtime-readiness-approval-required` | external write approval required flag |
| `account-runtime-readiness-approval-obtained` | external write approval obtained flag; must remain false until approved |
| `account-runtime-readiness-invoked` | owner runtime invocation flag; must remain false |
| `account-runtime-readiness-owner-write` | owner repo write attempted flag; must remain false |
| `account-runtime-readiness-browser-trigger` | browser-triggered broker order flag; must remain false |
| `account-runtime-readiness-raw-secret` | raw secret evidence flag; must remain false |
| `account-runtime-readiness-entrypoint` | guarded submit/cancel owner runtime entrypoints and arm flags |
| `account-runtime-readiness-blocker` | typed external approval and owner artifact blockers |
| `account-runtime-readiness-non-claim` | explicit non-claims shown in UI |
| `account-runtime-approval-packet-panel` | owner-runtime execution approval packet projection panel |
| `account-runtime-approval-packet-status` | approval packet status; must remain packet-ready rather than executed |
| `account-runtime-approval-packet-owner-path` | owner repo path requiring explicit approval |
| `account-runtime-approval-packet-required` | operator approval required flag |
| `account-runtime-approval-packet-obtained` | operator approval obtained flag; must remain false until exact approval is supplied |
| `account-runtime-approval-packet-invoked` | owner runtime invocation flag; must remain false before approval |
| `account-runtime-approval-packet-owner-write` | owner repo write attempted flag; must remain false before approval |
| `account-runtime-approval-packet-broker-order` | broker order created flag; must remain false before approved runtime execution |
| `account-runtime-approval-packet-exact-text` | exact operator approval text required before owner-runtime execution |
| `account-runtime-approval-packet-entrypoint` | guarded submit/cancel owner runtime entrypoints and arm flags from the approval packet |
| `account-runtime-approval-packet-blocker` | typed approval and owner artifact blockers from the approval packet |
| `account-runtime-handoff-bundle-panel` | owner-runtime execution handoff bundle projection panel |
| `account-runtime-handoff-bundle-status` | handoff bundle status; must remain bundle-ready rather than executed |
| `account-runtime-handoff-bundle-execution-allowed` | execution allowed flag; must remain false before approval |
| `account-runtime-handoff-bundle-approval-obtained` | approval obtained flag; must remain false until exact approval is supplied |
| `account-runtime-handoff-bundle-invoked` | owner runtime invocation flag; must remain false before approval |
| `account-runtime-handoff-bundle-owner-write` | owner repo write attempted flag; must remain false before approval |
| `account-runtime-handoff-bundle-broker-order` | broker order created flag; must remain false before approved runtime execution |
| `account-runtime-handoff-bundle-input` | runtime input requirements that must be bound after approval |
| `account-runtime-handoff-bundle-step` | gated operator sequence for approved owner-runtime execution |
| `account-runtime-handoff-bundle-artifact-count` | required owner artifact count |
| `account-runtime-handoff-bundle-gate-count` | post-handoff gate count |
| `account-runtime-handoff-bundle-blocker` | typed approval/input/artifact blockers from the handoff bundle |
| `account-partial-fill-runtime-approval-packet-panel` | partial-fill runtime execution approval packet projection panel |
| `account-partial-fill-runtime-approval-packet-status` | partial-fill approval packet status; must remain packet-ready rather than executed |
| `account-partial-fill-runtime-approval-packet-owner-path` | owner repo path requiring explicit approval |
| `account-partial-fill-runtime-approval-packet-required` | partial-fill operator approval required flag |
| `account-partial-fill-runtime-approval-packet-obtained` | partial-fill operator approval obtained flag; must remain false before owner execution |
| `account-partial-fill-runtime-approval-packet-invoked` | owner runtime invocation flag; must remain false before approved execution |
| `account-partial-fill-runtime-approval-packet-owner-write` | owner repo write attempted flag; must remain false before approved execution |
| `account-partial-fill-runtime-approval-packet-new-order` | new order submitted flag; must remain false before approved execution |
| `account-partial-fill-runtime-approval-packet-cancel-sent` | cancel sent flag; must remain false before approved execution |
| `account-partial-fill-runtime-approval-packet-exact-text` | exact partial-fill operator approval text required before owner-runtime execution |
| `account-partial-fill-runtime-approval-packet-formula` | partial-fill and terminal cancel success formulas |
| `account-partial-fill-runtime-approval-packet-entrypoint` | guarded submit/cancel owner runtime entrypoints and arm flags from the approval packet |
| `account-partial-fill-runtime-approval-packet-blocker` | typed approval and partial-fill runtime blockers from the approval packet |
| `account-partial-fill-runtime-handoff-bundle-panel` | partial-fill runtime execution handoff bundle projection panel |
| `account-partial-fill-runtime-handoff-bundle-status` | partial-fill handoff bundle status; must remain bundle-ready rather than executed |
| `account-partial-fill-runtime-handoff-bundle-execution-allowed` | execution allowed flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-approval-obtained` | approval obtained flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-invoked` | owner runtime invocation flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-owner-write` | owner repo write attempted flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-new-order` | new order submitted flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-cancel-sent` | cancel sent flag; must remain false before approved owner execution |
| `account-partial-fill-runtime-handoff-bundle-input` | runtime input requirements for partial-fill then cancel acceptance |
| `account-partial-fill-runtime-handoff-bundle-step` | gated owner-runtime sequence for submit, classify, cancel, readback and ingest |
| `account-partial-fill-runtime-handoff-bundle-success` | non-UI and Web UI success criteria including quantity formulas |
| `account-partial-fill-runtime-handoff-bundle-fallback` | typed fallback classifications when real partial-fill does not occur |
| `account-runtime-execution-gap-panel` | final runtime execution gap audit projection panel |
| `account-runtime-execution-gap-status` | gap audit status; must remain Phase 4e blocker evidence until owner-runtime artifacts exist |
| `account-runtime-execution-gap-verdict` | gap audit verdict; must be blocked pending owner-runtime execution |
| `account-runtime-execution-gap-final-claimed` | final acceptance claimed flag; must remain false before A4 owner-runtime artifacts exist |
| `account-runtime-execution-gap-not-accepted` | A4 not-accepted scenario and required evidence shape |
| `account-runtime-execution-gap-approval-obtained` | external write approval obtained flag; must remain false until exact approval is supplied |
| `account-runtime-execution-gap-invoked` | runtime invocation flag; must remain false before approval |
| `account-runtime-execution-gap-owner-write` | owner repo write attempted flag; must remain false before approval |
| `account-runtime-execution-gap-broker-order` | broker order created flag; must remain false before approved runtime execution |
| `account-runtime-execution-gap-artifact-count` | required owner artifact count |
| `account-runtime-execution-gap-required` | concrete items required before all acceptance can be claimed |
| `account-runtime-execution-gap-blocker` | residual blockers preventing final runtime acceptance |
| `account-partial-fill-owner-repair-approval-packet-panel` | owner repair approval packet projection panel |
| `account-partial-fill-owner-repair-approval-packet-status` | repair approval packet status; must remain packet-ready rather than executed |
| `account-partial-fill-owner-repair-approval-packet-verdict` | repair approval packet verdict requiring owner repair approval before retry |
| `account-partial-fill-owner-repair-approval-packet-owner-path` | owner repo path requiring exact repair approval |
| `account-partial-fill-owner-repair-approval-packet-obtained` | owner repair approval obtained flag; must remain false until exact approval is supplied |
| `account-partial-fill-owner-repair-approval-packet-current-matches` | current scripts-only approval match flag; must remain false for repair-first next action |
| `account-partial-fill-owner-repair-approval-packet-runtime-retry` | runtime retry allowed flag; must remain false before owner repair evidence and fresh retry packet |
| `account-partial-fill-owner-repair-approval-packet-exact-text` | exact owner repair approval text required before owner source/test writes |
| `account-partial-fill-owner-repair-approval-packet-change` | expected owner-side repair changes after approval |
| `account-partial-fill-owner-repair-approval-packet-validator` | owner validator commands required before retry |
| `account-partial-fill-owner-repair-approval-packet-blocker` | residual owner repair and real partial-fill blockers |
| `account-partial-fill-owner-repair-approval-packet-owner-write` | owner write attempted flag; must remain false in this projection |
| `account-partial-fill-owner-repair-approval-packet-additional-order` | additional paper order authorization flag; must remain false in this projection |
| `account-partial-fill-owner-repair-approval-packet-partial-claimed` | partial-fill claim flag; must remain false until real owner runtime evidence exists |
| `account-partial-fill-owner-repair-approval-packet-full-claimed` | full acceptance claim flag; must remain false |
| `account-partial-fill-remaining-acceptance-panel` | remaining acceptance state projection panel |
| `account-partial-fill-remaining-acceptance-status` | remaining acceptance audit status |
| `account-partial-fill-remaining-acceptance-verdict` | not-fully-accepted verdict |
| `account-partial-fill-remaining-acceptance-full-claimed` | full acceptance claim flag; must remain false |
| `account-partial-fill-remaining-acceptance-owner-repair-allowed` | owner repair allowed flag; must remain false until exact approval |
| `account-partial-fill-remaining-acceptance-runtime-retry` | runtime retry allowed flag; must remain false until owner repair evidence and fresh retry approval |
| `account-partial-fill-remaining-acceptance-latest-attempt` | latest real partial-fill attempt classification |
| `account-partial-fill-remaining-acceptance-requirement` | each R1-R5 missing requirement row |
| `account-partial-fill-remaining-acceptance-evidence-group` | accepted evidence groups that do not complete full acceptance |
| `account-partial-fill-remaining-acceptance-real-partial-claimed` | real partial-fill claim flag; must remain false |
| `account-partial-fill-remaining-acceptance-web-ui-claimed` | Web UI real partial-fill claim flag; must remain false |

## Layout Rules

1. Controls live inside the existing Account Workbench right rail or a compact workbench command strip.
2. Submit controls require instrument, side, quantity, limit price, TIF and idempotency preview.
3. Cancel controls appear only on rows with readback identity and remaining quantity.
4. Command status remains separate from order/fill display.
5. Gateway acknowledgement is shown as a gateway event, never as final account state.
6. Partial-fill then cancel display keeps one row identity through working, partial, cancel pending and canceled stages.
7. After terminal cancel, the order row must preserve filled quantity, set remaining quantity to zero and show cancelled quantity equal to the cancelled remainder.
8. Runtime closeout projection is read-only and must show `browser_triggered_broker_order=false` beside predecessor runtime refs.
9. Runtime handoff requests are displayed as blocked owner-runtime preparation, not as browser-triggered broker execution.
10. Runtime readiness is displayed as a blocker projection: owner refs and config refs are visible, but raw config, endpoints, secrets, owner writes and runtime invocation remain false.
11. Partial-fill runtime approval and handoff panels are read-only: they show exact approval text, success formulas, fallback classifications and blockers, but never render a browser-side broker execution trigger.
12. Owner repair approval packet projection is read-only: it shows the exact owner repair approval text and why the current scripts-only approval is insufficient, while owner write, runtime retry, partial-fill claim and full acceptance remain false.
13. Remaining acceptance state projection is read-only: it shows R1-R5 missing requirements and accepted evidence groups, but does not turn blocker evidence into owner repair, runtime retry or full acceptance authority.

## Disabled Mode

When disabled, the view keeps the observation-only layout and renders no submit/cancel/replace affordance. Disabled mode may display status/evidence panels but no action controls.







