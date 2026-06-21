# P023 UI Acceptance / OpenCTP 19053 Paper Command

- Proposal ID: `p023-openctp-19053-paper-command-capability`
- Status: paper_runtime_accepted

## Before Command Enabled

The UI must keep the current behavior:

1. `/accounts/acct.ctp.paper.19053` renders funds, positions, open orders and fills.
2. Command capability text says observation-only or disabled.
3. No submit, cancel, replace, broker action or live-ready controls render.
4. Existing挂单 rows may show status, but row buttons are hidden.

## After Paper Command Enabled

Command controls may appear only when `command.mode=paper_armed`.

Expected controls:

1. submit order form with instrument, side, quantity, limit price, TIF and idempotency preview
2. cancel button on eligible open-order rows
3. command status panel
4. risk/approval evidence panel
5. readback/reconciliation evidence panel

## UI Must Display

1. account id `acct.ctp.paper.19053`
2. command mode `paper_armed`
3. paper-only banner
4. risk decision
5. approval decision
6. gateway event id
7. post-submit/post-cancel readback refs
8. reconciliation result

## UI Must Not Display

1. live-ready claim
2. broker truth claim
3. gateway ack as final state
4. raw password/front/auth/token
5. cancel action without current readback identity
6. replace action before replace-specific proposal
