# <Topic Title> / <主题标题>

- topic-id: `<topic-id>`
- domain: `account-console`
- status: planned
- owner: architecture
- last_updated: `YYYY-MM-DD`
- source pattern: `D:\Nautilus\DSLresearch\docs\topics`

## 1. Intent / 意图

Describe the long-running account-console workstream in one or two paragraphs.

This topic must stay within the read-only account observation boundary. It may organize proposals, changes and evidence, but it must not write or infer runtime truth, broker truth, admission truth, approval truth, capital truth or tradability truth.

## 2. Scope / 范围

In scope:

1. Account-console documentation, contracts, read models, UI projections, benchmarks or governance artifacts relevant to this topic.

Out of scope:

1. Runtime trading state writes.
2. Broker state writes.
3. Admission, approval, capital allocation or tradability decisions.
4. Treating raw report messages, screenshots, report HTML or debug payloads as account truth.

## 3. Frontier / 当前前线

| Field | Value |
| --- | --- |
| current proposal | none |
| current change | none |
| current blocker | none |
| next action | define first proposal or close as docs-only |

## 4. Proposal Queue / Proposal 队列

| Order | Proposal | Goal | Status |
| --- | --- | --- | --- |
| 1 | TBD | TBD | planned |

## 5. Evidence Expectations / 证据期望

Evidence should be local to `nautilus_account_console` and may include:

1. docs checks;
2. contract tests;
3. `python -m compileall backend/src`;
4. `cargo test --manifest-path hotpath-rs/Cargo.toml`;
5. frontend build and rendering checks when Node/npm is available;
6. typed benchmark artifacts for HFT-related claims.

## 6. Closeout Rule / 收口规则

This topic can be marked completed only when:

1. planned proposals/changes are completed or explicitly retired;
2. local evidence is recorded in proposal/change acceptance docs;
3. stable decisions are distilled into ADR, architecture or README docs;
4. the topic registry status is updated.
