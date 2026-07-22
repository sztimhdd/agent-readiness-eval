# Agent Readiness Eval Core v4.0.0

`agent-readiness-eval` is a portable agent evaluation suite. The V4 release includes task-001 through task-005 across five capability tracks. task-006 is retained on disk as backlog-only material and is not installable or distributable. The suite defines task content and answer formats; execution, scoring, and packaging belong to each harness or a separate offline review layer. V4 adds controller/evidence write boundary, harness preflight, normalized trajectory contract, and 50/50 outcome/process scoring.

## Package Shape

```text
agent-readiness-eval/
├── SKILL.md
├── README.md
├── skill.json
├── contracts/
│   ├── controller-evidence-contract.yaml
│   ├── distribution-contract.yaml
│   ├── preflight-contract.yaml
│   ├── trajectory-contract.yaml
│   └── uat-controller-contract.yaml
├── scripts/
│   └── build-distribution.py
├── tasks/
│   ├── task-001/          # Reading and Delivery (static)
│   ├── task-002/          # Multi-Source Investigation (static)
│   ├── task-003/          # Policy-Constrained Decision (static)
│   ├── task-004/          # Coding & Repair (runnable project)
│   ├── task-005/          # Stateful Tool Use (stateful service)
│   └── task-006/          # Web Research (backlog-only)
├── templates/
│   ├── run-metadata.json
│   ├── preflight-result.json
│   ├── run-manifest.json
│   └── trajectory-event.json
├── docs/
│   ├── PRD_v4.md
│   ├── TDD_v4.md
│   ├── INSTALL-*.md
│   └── OFFLINE-SCORING-GUIDE.md
├── tests/
│   ├── test_core_v2_contract.py
│   ├── test_v4_contract.py
│   └── test_v3_regression.py
└── archive/
    └── v1-question-pack/   # v1.0 historical (read-only)
```

## How to Run

Install this Skill in a compatible harness. Send one message:

```text
评测
```

The harness runs a preflight capability probe, then reads `tasks/task-001/`, solves it using its own native tools, and writes an answer directory under `<workspace-root>/runs/`.

For specific tasks or profiles:

```text
评测 task-004
评测 task-005 controlled_tool
```

## Task Catalog

| Task | Track | Environment | Difficulty | Key Capability |
|------|-------|-------------|------------|----------------|
| 001 — Reading and Delivery | reading_and_delivery | static_files | basic | Source-authority resolution, severity triage, stale-label detection |
| 002 — Multi-Source Investigation | investigation_and_judgment | static_files | intermediate | Conflict disambiguation, distractor rejection, causal-chain construction |
| 003 — Policy-Constrained Decision | rules_and_safety | static_files | intermediate | Deterministic policy application, exception scoping, escalation boundary detection |
| 004 — Coding & Repair | coding_and_execution | runnable_project | advanced | Causal debugging, cross-module repair, invariant-based fixes |
| 005 — Stateful Tool Use | stateful_tool_use | stateful_service | advanced | Policy-before-action ordering, recovery from tool failures, boundary compliance |
<!-- | 006 — Web Research | web_research | web_research | advanced | Backlog-only; not installable or distributable | -->

## Answer Directory

```text
<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/
├── answer/
│   ├── task-id.txt
│   ├── final-answer.md
│   ├── decision-log.md
│   ├── artifacts/
│   └── run-metadata.json
└── controller/
    ├── preflight-result.json
    ├── trajectory.jsonl
    ├── protocol-violations.json
    ├── outcome-checks.json
    └── run-manifest.json
```

## Run Status

The controller records `run_status` in `controller/run-manifest.json`:

| Status | Meaning |
|--------|---------|
| `scored` | Valid task with Outcome and Process scores |
| `partial` | Some artifacts present, some missing — flagged for reviewer judgment |
| `adapter_blocked` | Legal required capability unavailable |
| `protocol_mismatch` | Controller cannot enforce or observe the profile |
| `task_invalid` | Task-level gate fired |
| `run_invalid` | Run-level tampering or evidence fabrication |

Use `UNAVAILABLE` for metadata the harness cannot observe. Do not estimate token usage. Controller evidence is authoritative when agent claims conflict with observed actions.

## Material Trajectory Loss

Zero trajectory events = `protocol_mismatch`. A complete `decision-log.md` does not substitute for missing trajectory. Partial-but-sufficient trajectory receives deductions, not `protocol_mismatch`. See SKILL.md for the four required trajectory determinations.

## Harness Preflight

No scored task starts until the harness passes a task-specific capability probe. Common checks include canonical identity, writable answer directory, readable agent-visible paths, isolated controller/evaluator paths, and capturable tool events. Static tasks (001-003) must block shell execution. Task 004 must support project copy and restricted exec. Task 005 must expose only public contract tools.

Preflight statuses: `ready` (task may start), `adapter_blocked` (no model score), `protocol_mismatch` (no official task starts).

## V4 Profiles

| Profile | Capabilities | Tasks | Notes |
|---------|-------------|-------|-------|
| `static-eval` | file read + write | 001, 002, 003 | Shell blocked |
| `coding-eval` | file tools + code edit + restricted exec | 004 | `exec` restricted to declared entry points |
| `stateful-eval` | file tools + 9 public stateful tools | 005 | Admin tools on separate interface |
| `read_only_shell_fallback` | `shell.exec.read_only` | Any static task | Non-canonical, diagnostic-only |

Canonical task-to-profile bindings are in `contracts/uat-controller-contract.yaml`. `read_only_shell_fallback` is for harnesses that can only read files via shell; fallback results are not ranked with canonical runs.

## Distribution

Three distribution views are enforced by `contracts/distribution-contract.yaml`:

| Package | Contains | Consumer |
|---------|----------|----------|
| **Agent** | task.md, inputs/, output-requirements, capability contracts, public tool contracts | Agent at runtime |
| **Runtime** | base-project (004), databases (005) | Environment service |
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

## V3 Historical Evidence

V3 answer directories under `runs/`, `evaluation-results/`, and `_eval-repo/` remain historical evidence. V3 content is preserved unchanged. V4 is a clean contract revision, not a backward-compatible extension of V3.

## Versioning

| Layer | Version |
|-------|---------|
| Suite | 4.0.0 |
| Tasks | 4.0.0 |
| Environment | 1.0.0 |
| Adapter Contract | 1.0.0 |
