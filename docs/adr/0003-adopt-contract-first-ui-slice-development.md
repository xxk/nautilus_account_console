---
status: accepted
owner: architecture
adr_id: "0003"
decision_status: accepted
landing_status: completed
---

# ADR-0003: Adopt Contract-First UI Slice Development / 采用契约优先的 UI 切片开发

- Date: 2026-06-13
- ADR type: UI delivery architecture decision
- Decision status: accepted
- Landing status: completed
- Scope: `nautilus_account_console` UI delivery decomposition principle
- Decision question: How should future Account Console UI features be decomposed so AI can implement them safely and verifiably?
- Decision: Use contract-first UI slices: `Workbench -> Panel -> Read Model Contract -> Fixture -> UI Slice -> Acceptance`.

---

## 1. Problem Frame / 问题框架

ADR-0002 adopts business workbench first navigation. That makes the product shape clear, but it does not by itself make implementation safe for AI-assisted development.

If AI implements UI directly from broad workbench descriptions, it may:

1. Add whole pages before read models are stable.
2. Invent fields not present in typed contracts.
3. Hide missing evidence behind visual placeholders.
4. Mix account truth, UI projection and request state.
5. Build untestable UI because no fixture or acceptance path exists.

The implementation unit must be smaller than a page and more concrete than a design paragraph.

## 2. Options Comparison / 方案对比

| Option | Core idea | Pros | Risks | AI suitability | Decision |
| --- | --- | --- | --- | --- | --- |
| A. Page-first development | Build one route/page at a time, then fill panels later | easy to demo, familiar for UI teams | encourages broad scope, weak fixture discipline, pages invent missing data | medium-low | rejected |
| B. Component-first development | Build reusable UI components first | good visual consistency, reusable primitives | can produce polished but domain-empty components; acceptance remains vague | medium | rejected as primary |
| C. Workbench-first only | Build each business workbench as a full feature | aligns with users and ADR-0002 | each workbench is still too large; AI may mix many data contracts | medium | accepted only as navigation/product layer |
| D. API/read-model-first only | Build backend/read models first, UI later | strong data discipline | UI ergonomics and visual acceptance may lag; hidden UX gaps | medium | rejected as sole approach |
| E. Contract-first UI slice | For each panel: contract, fixture, UI, test and acceptance | small, verifiable, AI-friendly, prevents invented data | requires more upfront contract files and fixture maintenance | high | accepted |
| F. Screenshot/mockup-first | Design screens visually before contracts | fast stakeholder review | weak truth boundary, hard to test, easy to drift from artifacts | low | rejected |

## 3. Decision / 决策

Future UI work must use this decomposition chain:

```text
Workbench
  -> Panel
  -> Read Model Contract
  -> Fixture
  -> UI Slice
  -> Acceptance
```

This ADR only records the architecture decision and option comparison. It does not own detailed implementation methods, slice queues, task plans or change acceptance templates.

Detailed implementation method belongs to:

1. Topic: [Contract-first UI slice development topic](../topics/contract-first-ui-slice-development.md)
2. Proposal: [P001 Daily Closeout Account Health Panel](../proposals/p001-daily-closeout-account-health-panel/README.md)
3. Shared UI acceptance: [Account Console capability UI acceptance](../acceptance/2026-06-13-account-console-capability-ui-acceptance.md)
4. Owner map: [Account Console owner map](../ownership/account-console-owner-map.md)

## 4. Binding Rules / 绑定规则

1. A future UI change must identify one workbench and one panel as the default implementation unit.
2. A UI panel must not invent fields outside its declared read model contract or fixture.
3. A page or workbench may compose several panels, but each panel still needs its own contract, fixture and acceptance mapping.
4. Account-management controls remain request/projection-only unless a typed request contract exists.
5. UI contracts cannot become account, runtime, broker, admission, approval or capital truth.
6. Forbidden readiness, admission, capital and tradability wording remains banned in implementation paths.
7. A UI slice must declare producer, verifier, projection, UI/report and approval owners before implementation.
8. Missing external source evidence must become a typed blocker; this project must not implement a substitute truth writer.

## 5. Relationship To ADR-0002 / 与 ADR-0002 的关系

ADR-0002 decides the product/navigation model: business workbenches first.

ADR-0003 decides the implementation decomposition principle: contract-first panel slices under those workbenches.

They are complementary:

```text
ADR-0002: what the user sees and how work is organized
ADR-0003: how each visible capability is decomposed for safe delivery
Topic/Proposal: how AI executes the concrete implementation steps
```

## 6. Consequences / 后果

Positive:

1. AI gets small, verifiable implementation units.
2. UI cannot invent data fields without a contract.
3. Fixtures make blocked, stale and empty states explicit.
4. Acceptance can be attached to individual panels and user paths.

Trade-offs:

1. More contract and fixture files are needed before visible UI accelerates.
2. Some quick demos will take longer because contract and fixture work comes first.
3. Contract versioning becomes important as read models mature.
