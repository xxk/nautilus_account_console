# P024 UI Design / Paper Command Controls

- Proposal ID: `p024-account-console-paper-command-controls`
- Status: phase1_backend_contract_gate_passed

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

## Layout Rules

1. Controls live inside the existing Account Workbench right rail or a compact workbench command strip.
2. Submit controls require instrument, side, quantity, limit price, TIF and idempotency preview.
3. Cancel controls appear only on rows with readback identity and remaining quantity.
4. Command status remains separate from order/fill display.
5. Gateway acknowledgement is shown as a gateway event, never as final account state.
6. Partial-fill then cancel display keeps one row identity through working, partial, cancel pending and canceled stages.
7. After terminal cancel, the order row must preserve filled quantity, set remaining quantity to zero and show cancelled quantity equal to the cancelled remainder.

## Disabled Mode

When disabled, the view keeps the observation-only layout and renders no submit/cancel/replace affordance. Disabled mode may display status/evidence panels but no action controls.
