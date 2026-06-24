---
status: proposed
owner: architecture
adr_id: "0007"
decision_status: proposed
landing_status: p024_governed_capability_authority_gate
---

# ADR-0007: Governed Account Command Capability / 受治理的账户下单与撤单能力

- 日期：`2026-06-21`
- ADR 类型：standard
- 决策状态：proposed
- 落地状态：p024_governed_capability_authority_gate
- 适用范围：`nautilus_account_console` Account Capability Fabric, Account Workbench, future Command Gateway, CTP / IB TWS / future broker command paths
- 决策问题：Account Console 是否可以实现账户下单、撤单能力；如果可以，命令 authority、risk/approval、broker session、readback reconciliation 与 UI 安全边界应该如何分层？
- 当前倾向：proposed；接受一个受治理的 command capability，但不得由 Account Mirror 或 UI 直接写 broker。命令必须通过 `OrderIntent -> RiskDecision -> ApprovalDecision -> ExecutionGateway -> ExecutionEvent -> AccountMirrorReadback -> ReconciliationResult`。
- 最终决策：pending；P024 backend command routes now fail closed unless an explicit command capability bundle grants authority. P024 runtime closeout no longer treats repo-local `output/` as broker/runtime truth unless owner-runtime evidence from `owner-repo://nautilus_ctp_adapter` is present. Existing P024 UI/runtime packet routes remain blocker/handoff/readiness projections; real Web UI risk/approval/gateway runtime send/live evidence are not complete and Account Mirror remains read-only.
- Required predecessor: ADR-0004 command boundary and ADR-0005 read-only broker observation boundary.
- First successor proposal: [P023 OpenCTP 19053 Paper Command Capability Acceptance Design](../proposals/p023-openctp-19053-paper-command-capability/README.md)
- Second successor proposal: [P024 Account Console Paper Command Controls](../proposals/p024-account-console-paper-command-controls/README.md)
- Executable design gate: `python scripts\validate_adr0007_account_command_capability.py`
- Required document order: ADR-0007 -> successor proposal -> command contracts -> gateway implementation -> paper acceptance -> live guarded acceptance

---

## 1. Problem Frame / 问题框架

Account Console 已经能通过 Account Mirror 显示账户资金、持仓、挂单和成交。下一步用户需要在账户工作台里完成下单和撤单，尤其是对 OpenCTP / TWS 等账户做 paper 或受控 live 操作。

现有 ADR 的边界仍然有效：

1. ADR-0004 接受 Account Capability Fabric，但只把 command 落到 design gate。
2. ADR-0005 接受独立 broker observation session，但明确禁止 observation session 发单、撤单、改单。
3. Account Mirror 是 readback/projection owner，不是 broker writer。

所以本 ADR 的核心问题不是“UI 上放一个买卖按钮”，而是如何增加 command capability，同时不把 Account Console 变成第二个无治理 broker runtime。

### 1.1 Hard Constraints / 硬约束

1. Account Mirror 不得发送、撤销、改单或批准订单；它只能做 readback、projection、reconciliation 和 typed blocker。
2. UI 不得直接调用 CTP、IB TWS、stock、CQG、TT 或 Nautilus runtime mutation APIs。
3. Command capability 不得从 account domain、source kind、paper/live 字样、OpenCTP 登录成功或 UI 显示挂单推断。
4. 每个 command 必须有 namespace-qualified `account_id`、`command_id`、`intent_id`、operator/session identity ref、source/ref/checksum 和 idempotency key。
5. 下单必须先生成 `OrderIntent`，再经过 risk check 和 approval/admission；缺任何一项都 fail closed。
6. 撤单必须绑定已知 `venue_order_id` / `client_order_id` / `order_ref` 及最新 readback 版本；不能按 UI 文本或截图撤单。
7. Gateway acknowledgement 不是最终账户状态；最终状态必须来自 Account Mirror readback 与 reconciliation。
8. Paper command 与 live command 必须分开 capability mode、owner ref、risk policy、approval policy、evidence path 和 UI affordance。
9. Live command 必须额外要求 capital/risk/admission owner refs、operator arm、session conflict check、market-hours/trading-window check 和 post-command readback。
10. Raw passwords、auth codes、front addresses、2FA、API keys、broker secrets 和 account secrets 不得写入本 worktree。
11. Any command implementation must record negative assertions: `raw_secret_values_recorded=false`, `order_action_authorized=true/false`, `gateway_ack_is_final_state=false`.
12. Repeated command submissions must be idempotent; duplicate clicks, network retries and browser refreshes must not produce duplicate broker orders.

### 1.2 Explicit Non-Goals / 明确不做

1. 本 ADR 不直接实现发单/撤单 UI 或 broker gateway。
2. 本 ADR 不授权 Account Mirror 写 broker。
3. 本 ADR 不授权 live trading readiness、capital approval 或 production admission。
4. 本 ADR 不把 OpenCTP/TWS 登录成功等同于可交易。
5. 本 ADR 不允许截图、browser text、debug/latest path 或人工口头确认作为 command pass evidence。

---

## 2. Relationship To Existing Decisions / 与既有 ADR 的关系

1. ADR-0004 remains valid: command is separated from observation and must reconcile through mirror readback.
2. ADR-0005 remains valid: broker observation sessions stay read-only. ADR-0007 introduces a separate command gateway owner, not an upgraded observation session.
3. ADR-0007 reopens only the future command lane reserved by ADR-0004; it does not weaken read-only observation evidence rules.
4. Existing source packages, including OpenCTP 19053 orders/fills, remain observation evidence only until a command capability package is accepted.

---

## 3. Options Comparison / 方案对比

| Option | Core idea | Pros | Risks | Decision |
| --- | --- | --- | --- | --- |
| A. Keep command disabled forever | Account Console remains observation-only | Lowest risk; matches current gates | Does not satisfy operator workflow | rejected as long-term target |
| B. UI directly calls broker order API | React/FastAPI calls CTP/TWS mutation methods | Fast demo | Creates second execution owner; no risk/readback boundary | rejected |
| C. Account Mirror sends orders | Mirror writes broker and reads broker | Fewer concepts | Read model becomes writer; truth boundary collapses | rejected |
| D. Governed Command Gateway | UI submits `OrderIntent`; gateway owns mutation after risk/approval; Mirror performs readback reconciliation | Keeps authority split; auditable; supports paper/live lanes | More contracts and gates | proposed accepted direction |
| E. External execution gateway only | Account Console never owns gateway, only talks to an external service | Strong owner separation | Requires external platform owner before first paper loop | future extension |

ADR-0007 chooses Option D as the proposed direction, with Option E allowed later if a shared execution gateway owner emerges.

---

## 4. Decision / 决策

### 4.1 Decision Summary / 决策摘要

Account Console may implement account submit and cancel capability only through a governed command path:

```text
Account Workbench UI
  -> OrderIntent
  -> RiskDecision
  -> ApprovalDecision
  -> ExecutionCommand
  -> Command Gateway
  -> Broker mutation API
  -> ExecutionEvent
  -> Account Mirror Readback
  -> ReconciliationResult
  -> UI command status evidence
```

The command path is separate from Account Mirror. Account Mirror never sends commands; it reads back broker/account state after the gateway attempt and produces reconciliation evidence.

### 4.2 Command Modes / 命令模式

| Mode | Meaning | Allowed actions | Required evidence | UI state |
| --- | --- | --- | --- | --- |
| `disabled` | No command authority | none | capability blocker | no submit/cancel controls |
| `paper_armed` | Paper account command loop allowed | submit, cancel | paper risk policy, paper gateway ref, readback pass | guarded controls |
| `live_dry_run` | Live command path validates without broker mutation | validate_intent only | live risk/approval refs, dry-run event | no broker mutation controls |
| `live_armed` | Live broker mutation allowed | submit, cancel, optionally replace | live risk/admission/capital/operator-arm/session/readback evidence | guarded controls with explicit armed state |

`replace` remains future unless a successor proposal accepts replace-specific risk and broker mapping. ADR-0007 covers submit/cancel first.

### 4.3 Required Contracts / 必需契约

1. `OrderIntent`: account, instrument, side, quantity, order type, limit/stop price, time-in-force, reduce/open/close intent, idempotency key.
2. `CancelIntent`: account, client/venue order identity, latest readback version, cancel reason, idempotency key.
3. `RiskDecision`: pass/block, policy refs, limits, exposure delta, reason codes.
4. `ApprovalDecision`: approver/admission refs, scope, expiry, mode.
5. `ExecutionCommand`: immutable command payload sent to gateway, with checksum and authority ref.
6. `ExecutionEvent`: accepted/rejected/submitted/cancel-requested/cancelled/failed, with gateway timestamp and broker ids where available.
7. `MirrorReadback`: post-command funds/positions/orders/fills snapshot or event cursor.
8. `ReconciliationResult`: matched/mismatched/timeout/blocked, with source refs and retry policy.
9. `CommandAuditRecord`: append-only evidence for intent, decisions, gateway event, readback and UI status.

### 4.4 Required Owner Map / 必需 owner 分层

| Concern | Owner |
| --- | --- |
| UI intent capture | Account Console UI |
| Intent validation shape | Account Console contracts |
| Risk policy decision | risk owner, not UI |
| Approval/admission | approval owner, not UI |
| Broker mutation | Command Gateway / execution owner |
| Broker credentials | owner repo/runtime, never Account Console docs/evidence |
| Broker/account truth | broker/runtime/source owner |
| Readback projection | Account Mirror |
| Command status display | Account Console UI from command evidence plus readback |

---

## 5. Acceptance Shape / 验收形态

ADR-0007 cannot be accepted by text alone. A successor proposal must provide these machine-checkable gates:

| ID | Scenario | Verification shape | Must fail if |
| --- | --- | --- | --- |
| A1 | ADR and contracts present | ADR validator + schema tests | command UI/API appears before contracts |
| A2 | Command disabled remains default | API/fixture tests | account kind or OpenCTP login implies command |
| A3 | Paper submit path | unit/contract/integration test with paper gateway | duplicate click creates duplicate order |
| A4 | Paper cancel path | integration test using real readback identity | cancel uses UI text/screenshot/latest path |
| A5 | Gateway ack not final | reconciliation test | UI marks command final without Mirror readback |
| A6 | Risk/approval fail closed | negative tests | missing risk/approval still sends broker command |
| A7 | Secret boundary | artifact redaction validator | raw password/front/auth/token recorded |
| A8 | Live mode blocked by default | live-arm validator | live mutation possible without arm/admission/capital refs |
| A9 | Real paper closeout | browser + API + source evidence | browser text alone is treated as pass |

### 5.1 Landing Phases / 落地阶段

1. Phase 0: ADR/proposal/contract skeleton, no command implementation.
2. Phase 1: command capability schema and disabled/default negative gates.
3. Phase 2: paper command gateway with simulated broker adapter only.
4. Phase 3: OpenCTP paper submit/cancel with real readback reconciliation.
5. Phase 4: TWS paper submit/cancel with real readback reconciliation.
6. Phase 5: live dry-run, no broker mutation.
7. Phase 6: guarded live command, only after external risk/approval/capital/admission acceptance.

### 5.2 First Landing Target: OpenCTP 19053 7x24 Paper / 首个落地目标

The first implementation target is `acct.ctp.paper.19053`, the OpenCTP TTS 7x24 simulation account. The 7x24 property means the paper counter can be used as a reproducible command acceptance lane outside normal exchange hours. It does not imply live readiness, capital approval, broker truth ownership or unrestricted mutation.

P023 must prove submit and cancel through real OpenCTP paper evidence:

1. Preflight readback: current funds, positions, orders and fills are read by owner-backed OpenCTP query evidence.
2. Paper submit: a guarded order intent is accepted by risk/approval policy and sent through the command gateway, not Account Mirror.
3. Immediate readback: `ReqQryOrder` observes the new order by venue identity and records a source ref/checksum.
4. Paper cancel: a cancel intent uses the readback order identity, not UI text or screenshot coordinates.
5. Cancel readback: `ReqQryOrder` observes cancelled/withdrawn terminal state, or a typed timeout/blocker is preserved.
6. UI evidence: Account Console shows command status from command audit + mirror readback, not gateway ack alone.
7. Negative evidence: duplicate submit idempotency, missing risk, missing approval, stale order identity and missing readback all fail closed.

P023 may use small quantity, approved instrument, limit price away from market, and explicit paper-only guardrails. It must not claim live trading readiness.

---

## 6. Non-Negotiable Negative Acceptance / 不可降级负向验收

1. `POST /api/mirror/.../orders` is forbidden.
2. Any route named submit/cancel/replace must be absent until successor command API contracts are accepted.
3. Browser controls must not appear while `command.mode=disabled`.
4. Command gateway response alone must not set final order state.
5. OpenCTP `ReqQryOrder/ReqQryTrade` readback cannot be reused as authorization to cancel unless paired with a `CancelIntent`, risk decision, approval decision and current readback version.
6. Missing risk/approval/session/authority/readback must create typed blocker, not hidden success.
7. Live command must remain impossible without explicit `live_armed` evidence.

---

## 7. Status / 当前状态

ADR-0007 is proposed only. Current repository behavior remains observation-only:

1. Account Mirror command capability stays disabled.
2. Existing OpenCTP 19053 UI shows orders/fills by read-only query only.
3. No submit/cancel/replace UI controls are accepted by this ADR draft.
4. P024 governed capability authority gate supersedes the earlier Phase 1 intent-acceptance shape: backend `submit-intents`, `cancel-intents` and owner-runtime run-request routes must fail closed with `command_capability_not_mounted` unless the selected account bundle declares `command.enabled=true`, `command.mode=paper_armed`, action membership, `authority_ref=owner-repo://nautilus_ctp_adapter` and a checksum.
5. P024 browser controls remain projection-only and must not be treated as authority. A UI state or mocked `paper_armed` projection cannot authorize backend intent acceptance unless the backend capability authority gate passes.
6. P024 runtime closeout projection is accepted only when positive runtime claims are backed by owner-runtime evidence. Repo-local `output/account_command/...` artifacts without `owner_runtime_evidence.owner_repo_ref=owner-repo://nautilus_ctp_adapter` must produce a typed blocker and must not return `runtime_gateway_send_observed=true` or `broker_order_created=true`.
7. P024 Phase 3b partial-fill cancel UI display is accepted as browser display-contract evidence only: S1 working, S2 partial, S3 cancel pending and S4 remaining cancelled keep stable order/fill identities and correct quantity formulas while preserving a typed runtime partial-fill blocker.
8. P024 Phase 3c owner-runtime handoff request is accepted as browser handoff evidence only: submit/cancel controls prepare typed run requests for `ctp_guarded_paper_order_loop.py` and `ctp_guarded_paper_cancel_loop.py`, while `runtime_invocation_attempted=false`, `browser_triggered_broker_order=false` and `gateway_send_attempted=false` remain required.
9. P024 Phase 3d owner-runtime invocation readiness is accepted as a readiness gate only: owner repo path, guarded entrypoint checksums, external write approval scope and post-run artifact requirements are frozen while real owner-runtime invocation remains blocked pending explicit approval.
10. P024 Phase 3e runtime readiness UI projection is accepted as browser blocker evidence only: the Web UI renders owner refs, entrypoints, approval state, blockers and non-claims while `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `browser_triggered_broker_order=false` remain required.
11. P024 Phase 4 residual blocker audit is accepted as closeout evidence only: A1-A16, required gates, non-accepted runtime scope and residual owner-runtime blockers are machine-checked while `full_runtime_acceptance_claimed=false`.
12. P024 Phase 4a owner-runtime execution approval packet is accepted as an approval-packet gate only: `owner-runtime-execution-approval-packet.json` freezes the exact operator approval text `I approve writes to D:/Nautilus/nautilus_ctp_adapter ...`, owner path, reason, expected impact, command templates and post-run artifact requirements while `approval_obtained=false`, `runtime_invocation_attempted=false` and `owner_repo_write_attempted=false`.
13. P024 Phase 4b runtime approval packet UI projection is accepted as browser blocker evidence only: the Web UI renders the exact approval text, owner path, entrypoints, blockers and false execution flags while `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.
14. P024 Phase 4c owner-runtime execution handoff bundle is accepted as a handoff gate only: the post-approval sequence, runtime input requirements, required owner artifacts and post-handoff gates are machine-checked while `execution_allowed=false`, `approval_obtained=false` and `runtime_invocation_attempted=false`.
15. P024 Phase 4d runtime handoff bundle UI projection is accepted as browser blocker evidence only: the Web UI renders the execution guard, runtime input requirements, operator sequence, artifact counts, post-handoff gates and blockers while `execution_allowed=false`, `approval_obtained=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.
16. P024 Phase 4e runtime execution gap audit is accepted as final blocker evidence only: the artifact/API/Web UI identify A4 as not accepted, require owner-runtime artifacts and preserve `final_acceptance_claimed=false`, `runtime_invocation_attempted=false`, `owner_repo_write_attempted=false` and `broker_order_created=false`.
17. P024 is the current successor proposal for guarded Web/API paper controls, runtime closeout projection, partial-fill then cancel Web UI display correctness, owner-runtime handoff request preparation, owner-runtime invocation readiness, runtime readiness UI projection, residual blocker closeout audit, owner-runtime execution approval packet, runtime approval packet UI projection, owner-runtime execution handoff bundle, runtime handoff bundle UI projection and runtime execution gap audit.
18. Next implementation work is real Web UI submit/cancel runtime evidence through risk/approval/gateway/readback/reconciliation; broker gateway send remains blocked until external owner-runtime approval and artifacts are present.
