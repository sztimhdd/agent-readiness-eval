# Agent Readiness Eval Core v2.0

`agent-readiness-eval` is a portable agent evaluation suite. Six tasks across four capability tracks. It defines task content and answer formats; execution, scoring, and packaging belong to each harness or a separate offline review layer.

## Package Shape

```text
agent-readiness-eval/
├── SKILL.md
├── README.md
├── skill.json
├── contracts/
│   └── distribution-contract.yaml
├── scripts/
│   └── build-distribution.py
├── tasks/
│   ├── task-001/          # Baseline Delivery (static)
│   ├── task-002/          # Multi-Source Investigation (static)
│   ├── task-003/          # Policy-Constrained Decision (static)
│   ├── task-004/          # Coding & Repair (runnable project)
│   ├── task-005/          # Stateful Tool Use (stateful service)
│   └── task-006/          # Web Research (web profiles)
├── adapters/
│   ├── vitaclaw/
│   ├── openclaw/
│   └── hermes/
├── templates/
│   ├── run-metadata.json
│   └── completion-summary.md
├── docs/
│   ├── PRD_core_v2.md
│   ├── TDD_core_v2.md
│   ├── INSTALL-*.md
│   └── OFFLINE-SCORING-GUIDE.md
├── tests/
│   └── test_core_v2_contract.py
└── archive/
    └── v1-question-pack/   # v1.0 historical (read-only)
```

## How to Run

Install this Skill in a compatible harness. Send one message:

```text
评测
```

The harness reads `tasks/task-001/`, solves it using its own native tools, and writes an answer directory under `runs/`.

For specific tasks or profiles:

```text
评测 task-004
评测 task-005 controlled_tool
评测 task-006 controlled_web
```

For a leakage-free, repeatable installation procedure, see `docs/INSTALL-CODEX.md`.

## Task Catalog

| Task | Track | Environment | Difficulty | Key Capability |
|------|-------|-------------|------------|----------------|
| 001 — Baseline Delivery | reading_and_delivery | static_files | basic | Single-source extraction, instruction following, edge case handling |
| 002 — Multi-Source Investigation | investigation_and_judgment | static_files | intermediate | Multi-file correlation, evidence evaluation, distractor exclusion |
| 003 — Policy-Constrained Decision | rules_and_safety | static_files | intermediate | Rule application, exception scoping, escalation boundary detection |
| 004 — Coding & Repair | coding_and_execution | runnable_project | advanced | Code execution, bug diagnosis, repair, result verification |
| 005 — Stateful Tool Use | stateful_tool_use | stateful_service | advanced | State reading, policy lookup, sequential operation, safety stop |
| 006 — Web Research | web_research | web_research | advanced | Proactive search, source verification, citation accuracy |

## Answer Directory

```text
runs/<task-id>-<harness-name>-<model-name>-<run-id>/
├── task-id.txt
├── final-answer.md
├── artifacts/
└── run-metadata.json
```

## Run Status

Every `run-metadata.json` records a `run_status`:

| Status | Meaning |
|--------|---------|
| `completed` | All required artifacts produced |
| `partial` | Some artifacts present, some missing — flagged for reviewer judgment |
| `aborted` | Directory created, no artifacts — never scored |

Use `UNAVAILABLE` for metadata the harness cannot observe. Do not estimate token usage.

## Distribution

Three distribution views are enforced by `contracts/distribution-contract.yaml`:

| Package | Contains | Consumer |
|---------|----------|----------|
| **Agent** | task.md, inputs/, output-requirements, capability contracts, public tool contracts | Agent at runtime |
| **Runtime** | base-project (004), databases (005), corpora (006) | Environment service |
| **Evaluator** | reference analysis, scoring rubrics, expected final state, replacement data | Human reviewer |

Build packages with `scripts/build-distribution.py`.

## Architecture

Four-layer separation:
- **Agent-Visible Task Content**: what the agent reads and produces
- **Controlled Runtime Environment**: code projects, state systems, search corpora
- **Harness Adapter**: protocol conversion only — no business decisions
- **Evaluator-Only Assets**: reference analysis, scoring rubrics, expected final states

## What This Package Does Not Include

This package has no execution engine, grading engine, child-agent control layer, result packaging pipeline, privacy scrubber, or answer key. Those concerns belong to each harness or to a separate offline review layer.

## Versioning

| Layer | Version |
|-------|---------|
| Suite | 2.0.0 |
| Tasks | 2.0.0 |
| Environment | 1.0.0 |
| Adapter Contract | 1.0.0 |
