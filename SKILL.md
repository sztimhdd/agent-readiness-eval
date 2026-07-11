---
name: agent-readiness-eval
description: Agent Readiness Eval Core v2.0 — portable evaluation suite for comparing agent harnesses. Five tasks across four capability tracks (task-006 planned for future release). Trigger with "评测".
category: evaluation
tags:
  - readiness
  - harness-eval
  - agent-evaluation
  - vitaclaw
version: 2.0.0
---

# Agent Readiness Eval Core v2.0

## Principle

Evaluation content is portable. Execution is native to each harness.

This Skill issues tasks and defines answer formats. It does not execute, grade, sanitize, package, or certify results. The harness reads the task, uses its own tools, creates answer artifacts, and stops.

## Trigger

| Trigger | Behavior |
|---------|----------|
| `评测` | Run task-001 (default) |
| `评测 task-001` | Run task-001 |
| `评测 task-002` | Run task-002 |
| `评测 task-004` | Run task-004 (requires environment setup) |
| `评测 task-005 controlled_tool` | Run task-005 with controlled tool profile |

## Task Catalog

| Task | Track | Environment | Difficulty | Profiles |
|------|-------|-------------|------------|----------|
| task-001 — Baseline Delivery | reading_and_delivery | static_files | basic | — |
| task-002 — Multi-Source Investigation | investigation_and_judgment | static_files | intermediate | — |
| task-003 — Policy-Constrained Decision | rules_and_safety | static_files | intermediate | — |
| task-004 — Coding & Repair | coding_and_execution | runnable_project | advanced | — |
| task-005 — Stateful Tool Use | stateful_tool_use | stateful_service | advanced | controlled_tool, native_adapter |
<!-- task-006 — Web Research — planned for future release -->

## Required Flow

1. Read `tasks/<task-id>/task.md`.
2. For static tasks: read every file under `tasks/<task-id>/inputs/`.
3. For environment tasks: read `tasks/<task-id>/environment-contract.yaml` and any public contracts under `tasks/<task-id>/environment/public/` or `tasks/<task-id>/profiles/<profile>/public/`.
4. Read `tasks/<task-id>/output-requirements.md`.
5. Read `tasks/<task-id>/capability-contract.yaml` to understand what is being measured.
6. Create a new answer directory under `runs/` using this shape:

```text
runs/<task-id>-<harness-name>-<model-name>-<run-id>/
├── task-id.txt
├── final-answer.md
├── artifacts/
└── run-metadata.json
```

The `run-id` MUST be unique per evaluation run. Use a timestamp or UUID.

7. Fill `run-metadata.json` from `templates/run-metadata.json`. Set `run_status` to:
   - `"completed"` — all required artifacts produced
   - `"partial"` — some artifacts produced, some missing
   - `"aborted"` — directory created, no artifacts produced

   Use `UNAVAILABLE` for fields the harness cannot observe. Do not estimate tokens, timings, or tool calls.

8. Write `final-answer.md` and required files under `artifacts/`.
9. Report the answer directory path to the user.

## Rules

- Do not call any packaged execution, grading, orchestration, or child-agent control code.
- Do not create fake tool logs, fake token counts, fake timings, or fake grading results.
- Do not request or record hidden chain of thought.
- Do not self-grade the answer.
- Do not modify files under `tasks/<task-id>/evaluator-notes/` or `tasks/<task-id>/evaluator-private/`.
- For environment tasks (004-006): do not modify base project files in-place. Copy to `artifacts/project/` first.
- For stateful tasks (005): do not access the SQLite database directly. Use only the canonical tool interface.
- For web tasks (006): do not read the private corpus directory directly. Use only `search_corpus` and `fetch_document`.
- If a metadata field is unavailable, write `UNAVAILABLE` exactly.
- Aborted runs are never scored. Partial runs are flagged for reviewer judgment.

## Environment Notes

**Task 004 (Coding & Repair):**
- Copy `tasks/task-004/environment/base-project/` → `artifacts/project/`
- Run `python3 -m unittest discover -s tests -v` to see failures
- Fix bugs in `src/` only. Do not modify `tests/`, `data/`, or `expected-output-format.md`.

**Task 005 (Stateful Tool Use):**
- The environment service exposes tools via `tasks/task-005/environment/public/tool-contract.yaml`
- Use the canonical tool names exactly as declared
- State operations are recorded in an audit log — you do not need to create one

## Scoring

Scoring is offline and external to this Skill. Use `docs/OFFLINE-SCORING-GUIDE.md` for human review. The answer directory is the only artifact this Skill asks the harness to produce.
