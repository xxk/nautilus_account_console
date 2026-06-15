# P002 P0 Conflict Analysis / P0 冲突分析

- Proposal ID: `p002-adr0044-adr0045-loop-heartbeat`
- Status: p0_conflict_analysis
- Updated: 2026-06-13

## 1. P0 Summary / P0 总结

P0 conclusion:

```text
conditional_go
```

There is no irreconcilable architecture conflict between ADR-0044, ADR-0045 and Account Console ADR-0003, but a new heartbeat must be constrained. The main risk is not technical incompatibility; the main risk is ownership drift:

1. A second scheduler competing with P077.
2. UI work starting before ADR-0044 foundation/read-model artifacts exist.
3. Account Console becoming runtime/account/order truth.
4. P077/P078 evidence being overclaimed as ADR-0045 or Account Console completion.
5. The 26-route Account Console capability map being treated as 26 equal implementation pages.

## 2. Owner Map / Owner 边界图

| Layer | Canonical owner | What it may own | Must not own |
| --- | --- | --- | --- |
| ADR-0044 | `nautilus_strategies` ADR/topic/P078 child changes | Real-Feed Sandbox Paper route, official-first matching baseline, account/order/fill/settlement artifact contracts | Account Console UI, readiness/admission/capital truth |
| ADR-0045 | `nautilus_strategies` ADR + independent `nautilus_account_console` project | event-driven universal read-only Account Console architecture | runtime/account/order/fill truth |
| ADR-0003 | `nautilus_account_console` local ADR | contract-first UI slice decomposition decision | implementation queue, runtime truth, scheduler truth |
| P077 | `nautilus_strategies` proposal | timed loop workflow, checkpoint, lock, one-slice dispatch, waiting/blocker projection | ADR-0044/P078/P076/ADR-0045 evidence truth |
| P078 | `nautilus_strategies` proposal | ADR-0044 A0-A3 foundation delivery lane | Account Console UI, A4+ market profiles, readiness/capital |
| P001 | `nautilus_account_console` proposal | first `/closeout` Account Health Panel UI slice design/acceptance | ADR-0044 runtime artifacts |
| P002 | `nautilus_account_console` proposal | P0 conflict analysis and heartbeat coordination guardrails | scheduler, runtime/account/UI truth, owner closeout |

## 3. Conflict Matrix / 冲突矩阵

| ID | Potential conflict | Severity | Current status | Resolution |
| --- | --- | --- | --- | --- |
| P0-C1 | New heartbeat duplicates P077 scheduler/lock/checkpoint semantics | P0 blocking if implemented | present risk | P002 must not implement scheduler. It may read P077 state and recommend next owner lane only. |
| P0-C2 | Account Console UI starts before ADR-0044 A0-A3 artifacts/read models exist | P0 blocking for data-dependent panels | present risk | UI shell/design may proceed; truthful account/order/settlement panels require typed artifacts, fixtures or typed blockers. |
| P0-C3 | P077 requires ADR-0045 UI opened before runtime slices, while P078 says Account Console successor opens after ledger/read model package | P0 design conflict if interpreted literally | present | Split "operator UI shell/gate" from "truthful artifact-backed account panels". UI shell can open; artifact-backed panels wait for P078/ADR0044 source refs. |
| P0-C4 | P078 excludes Account Console, but heartbeat wants ADR0045 landing | P1 sequencing risk | expected | P078 A0-A3 remains foundation only. ADR0045/account-console work is a successor lane, not P078 scope. |
| P0-C5 | ADR-0045 legacy route model `/accounts` differs from account_console workbench route model `/closeout`, `/monitor`, etc. | P1 UI taxonomy risk | present | Treat `/accounts` and `/accounts/{account_id}` as Account Workbench/deep-link compatibility. Account Console local route coverage matrix governs product navigation. |
| P0-C6 | P077 `19054` UI visibility case could be mistaken for broker-paper account truth | P0 evidence risk | present | Keep Nautilus sandbox Paper alias `19054` separate from CTP/broker-paper aliases; UI visibility must cite typed sandbox runtime/order refs/checksums. |
| P0-C7 | Heartbeat claims "全部落地" from proposal docs or screenshots | P0 blocking | present risk | Heartbeat can only report owner state: `not_started`, `blocked`, `proposal_ready`, `verified_by_owner`. Completion needs child acceptance and typed evidence. |
| P0-C8 | Account Console route coverage says P001 `/closeout` covered-proposal, but ADR-0045 original routes only named `/accounts` | low | resolved by local design | ADR-0045 provides architecture; account_console local ADR-0002/0003 and design docs refine product navigation. |
| P0-C9 | P002 becomes another long-term topic/proposal queue parallel to P077/P078 | medium | prevent now | P002 is P0 guardrail only unless a later proposal explicitly promotes it to a coordination lane with no scheduler/runtime truth. |

## 4. P0 Blocking Rules / P0 阻断规则

The heartbeat must stop and split if any of these appear:

1. Need for a new recurring scheduler, daemon, database or lock file outside P077.
2. Need to emit runtime/account/order/fill/settlement artifacts.
3. Need to call CTP/IB/broker endpoints or submit/cancel/replace orders.
4. Need to declare Paper ready, Live ready, admission, PM approval, production readiness, capital allocation or tradability.
5. Need to accept UI screenshot, UI text, DB row, latest/debug path, stdout or report HTML as owner truth.
6. Need to bypass P078 A0-A3 for real-feed/high-fidelity Paper claims.
7. Need to bypass Account Console contract/fixture/UI acceptance for visible UI claims.

## 5. Recommended P1 Heartbeat Shape / 推荐 P1 心跳形态

If P0 exits `conditional_go`, P1 may define a read-only heartbeat row:

```text
Loop Heartbeat Row:
  heartbeat_id:
  source_state_refs:
    - P077 phase/status
    - P078 phase/status
    - account_console proposal/status
  selected_next_owner_lane:
  entry_condition:
  exit_signal:
  typed_blockers:
  forbidden_truth_sources:
  stop_and_split_conditions:
```

P1 must select exactly one lane per heartbeat:

1. `p078_a0_a3_foundation`
2. `account_console_contract_fixture_ui_slice`
3. `p077_owner_blocker_repair`
4. `wait_external_owner`

It must not run multiple owner lanes in one wakeup.

## 6. P0 Verdict / P0 结论

The heartbeat is useful only if it is a thin cross-owner coordination check.

It is unsafe if it becomes:

1. A second P077 scheduler.
2. A second ADR-0044 delivery lane.
3. A second ADR-0045/account-console truth owner.
4. A shortcut around P078 foundation acceptance.
5. A shortcut around Account Console route/UI/anti-drift acceptance.

Therefore P0 is:

```text
conditional_go:
  proceed_to_p1_only_after_acceptance_review
  no_scheduler
  no_runtime_truth
  no_ui_truth
  no_completion_claim
```
