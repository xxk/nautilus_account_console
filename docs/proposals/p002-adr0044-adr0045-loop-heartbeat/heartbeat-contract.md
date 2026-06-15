# P002 Heartbeat Contract / 心跳合同

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p1_contract_landed
- Updated: 2026-06-13

## 1. Contract Purpose / 合同目的

This heartbeat contract defines the smallest safe coordination unit for pushing ADR-0044, ADR-0045 and Account Console ADR-0003 toward implementation.

It is a read-only governance heartbeat. It does not create a scheduler, does not replace P077, does not write runtime/account/order/UI truth and does not close owner work.

## 2. Heartbeat Row / 心跳行

Every heartbeat must be represented as one row:

```text
Loop Heartbeat Row:
  heartbeat_id:
  observed_at:
  observed_by:
  source_state_refs:
    p077:
      proposal_ref:
      phase_status:
      active_blocker:
      latest_owner_evidence_ref:
    p078:
      proposal_ref:
      phase_status:
      active_child_change:
      latest_owner_evidence_ref:
    account_console:
      proposal_refs:
      route_coverage_ref:
      ui_acceptance_ref:
      latest_owner_evidence_ref:
  selected_next_owner_lane:
  selection_reason:
  entry_condition:
  exit_signal:
  blocker_handling:
  typed_blockers:
  forbidden_truth_sources:
  stop_and_split_conditions:
  loop_termination_signal:
  next_allowed_action:
```

## 3. Allowed Owner Lanes / 允许选择的 owner lane

Exactly one lane may be selected per heartbeat:

| Lane | Owner | Allowed action | Must not do |
| --- | --- | --- | --- |
| `p078_a0_a3_foundation` | `nautilus_strategies` P078 child changes | open or continue ADR-0044 A0-A3 foundation work | implement UI, CN S2/HFT, real-feed runtime or readiness |
| `account_console_contract_fixture_ui_slice` | `nautilus_account_console` proposal/change | open or continue contract-backed UI slice work | invent account/order fields or use UI as truth |
| `p077_owner_blocker_repair` | `nautilus_strategies` P077/P076 owner path | repair scheduler/blocker handoff or typed owner blocker | replace runtime evidence |
| `ctp_market_owner_blocker_repair` | `nautilus_ctp_adapter` CTP market owner path | repair or re-run MD-only freshness owner artifact/blocker path | call TD/order, create another market runtime or turn stale tick into pass |
| `wait_external_owner` | unavailable external owner/resource | record typed blocker and retry condition | turn waiting into pass or stop the loop |

## 4. Lane Selection Rule / Lane 选择规则

The heartbeat must select the first eligible lane in this order:

1. If P078 A0-A3 foundation is not complete, select `p078_a0_a3_foundation`.
2. If P078 A0-A3 has typed artifacts or typed blockers sufficient for a UI fixture, select `account_console_contract_fixture_ui_slice`.
3. If P077 has an active workflow/blocker repair need, select `p077_owner_blocker_repair`.
4. If a blocker points to an available sibling owner repo, select that owner-side repair lane, such as `ctp_market_owner_blocker_repair`.
5. If no lane is eligible because the blocker is an unavailable external resource, select `wait_external_owner`.

The heartbeat must not select multiple lanes. If two lanes look eligible, select the lower dependency first and record the other as `deferred_candidate`.

## 4.1 Blocker Handling Rule / 阻塞处理规则

Blocked is work input, not a loop termination signal. For each typed blocker:

1. If the blocker names an available owner repo, the heartbeat should enter that repo and make the smallest safe owner-side repair.
2. The repair must run the owner repo's lightweight gates and return either a typed pass artifact or a typed blocker with source ref and checksum.
3. If the blocker is an unavailable market window, credential, endpoint permission, broker approval, capital/admission approval or unsafe order action, record the typed blocker and retry condition, then keep the loop active.
4. A blocker may pause a single owner lane, but it must not terminate the overall ADR0044/ADR0045 landing loop.

## 4.2 Loop Termination Rule / Loop 终止规则

The loop terminates only when all scoped work is formally complete:

1. ADR0044/P078 scoped foundation and any selected successors have owner acceptance evidence.
2. ADR0045/Account Console scoped UI slices selected by the loop have contract/fixture/UI acceptance evidence.
3. P077/P076 or sibling owner lanes selected by the loop have typed pass artifacts or accepted closeout blockers.
4. No active typed blocker remains without retry/closeout decision.
5. No required sibling repo handoff remains open.

The loop must not terminate from coordination evidence, chat agreement, clean logs, screenshots, UI state, route config or an unresolved blocker.

## 5. Forbidden Truth Sources / 禁止真源

Heartbeat evidence must reject:

1. chat memory
2. terminal scrollback
3. stdout/log excerpts
4. screenshots as truth
5. browser state
6. DB row as runtime/order truth
7. latest/debug folders
8. report HTML or tearsheet
9. UI labels
10. proposal README as child implementation evidence

## 6. Stop And Split Conditions / 停止并拆分

Stop and split if the heartbeat needs:

1. a new recurring scheduler, daemon, lock file or checkpoint system
2. runtime/account/order/fill/position/settlement artifact writing
3. broker, CTP, IB or live endpoint calls
4. order submit/cancel/replace actions
5. Paper/Live/admission/capital/tradability claims
6. P078 A4+ market profile work
7. Account Console UI implementation without contract, fixture and UI acceptance
8. acceptance closeout for another owner

## 7. First Landed Heartbeat Row / 首个已落心跳行

```text
Loop Heartbeat Row:
  heartbeat_id: p002-hb-0001
  observed_at: 2026-06-13
  observed_by: Codex
  source_state_refs:
    p077:
      proposal_ref: D:/Nautilus/nautilus_strategies/docs/proposals/p077-p076-timed-paper-loop-workflow/
      phase_status: phase_6_real_paper_node_capability_runway_blocked
      active_blocker: p077-t6-ctp-market-freshness-stale-owner-artifact
      latest_owner_evidence_ref: P077 acceptance current evidence table
    p078:
      proposal_ref: D:/Nautilus/nautilus_strategies/docs/proposals/p078-ADR0044-real-feed-sandbox-paper-foundation/
      phase_status: A0-A3 not_started
      active_child_change: none
      latest_owner_evidence_ref: P078 proposal scaffold only
    account_console:
      proposal_refs:
        - docs/proposals/p001-daily-closeout-account-health-panel/
        - docs/proposals/p002-adr0044-adr0045-loop-heartbeat/
      route_coverage_ref: docs/acceptance/2026-06-13-account-console-ui-route-coverage-matrix.md
      ui_acceptance_ref: docs/proposals/p001-daily-closeout-account-health-panel/ui-acceptance.md
      latest_owner_evidence_ref: P001 design/acceptance only; no runtime-backed account read model claim
  selected_next_owner_lane: p078_a0_a3_foundation
  selection_reason: P078 A0 official matching baseline is the lowest unfinished dependency before truthful account/order/settlement UI panels.
  entry_condition: open P078 A0 child change in nautilus_strategies
  exit_signal: A0 child acceptance has official source mapping, official fixture or typed blocker, and official gap register
  typed_blockers:
    - no P078 A0 child evidence exists yet
  forbidden_truth_sources:
    - proposal docs as implementation pass
    - UI screenshots as account/order truth
    - latest/debug/report/stdout truth
  stop_and_split_conditions:
    - any scheduler implementation in P002
    - any runtime/order truth writing in account_console
    - any Account Console data panel requiring missing P078 artifacts
  next_allowed_action: prepare or open P078 A0 official matching baseline child change under nautilus_strategies
```
