---
name: agent-readiness-eval
description: Agent Readiness Eval Core v3.0 — portable evaluation suite for comparing agent harnesses. V3 releases task-001 through task-005; task-006 is backlog-only. Trigger with "评测".
category: evaluation
tags:
  - readiness
  - harness-eval
  - agent-evaluation
  - vitaclaw
version: 3.0.0
---

# Agent Readiness Eval Core v3.0

## Principle

Evaluation content is portable. Execution is native to each harness.

This Skill issues tasks and defines answer formats. It does not execute, grade, sanitize, package, or certify results. The harness reads the task, uses its own tools, creates answer artifacts, and stops.

## Harness-Native Execution

### VitaClaw

- Activate this Skill with `activate_skill("agent-readiness-eval")`.
- Read Skill resources with `read_skill_file(skill_id="agent-readiness-eval", path="tasks/<task-id>/task.md")`, then the matching `inputs/`, `output-requirements.md`, and capability or environment contracts.
- Never use `exec`, `cat`, `find`, `list_dir`, or guessed filesystem paths to read Skill files.
- Skill directory is a read-only mount; answers go under the workspace root, not inside the Skill directory; writing answers into the Skill directory will fail silently or corrupt the projection.

### OpenCode

- OpenCode uses the native `Read` tool pointed at the workspace directory containing the local clone or unpacked bundle.
- After installing or updating the Skill, restart OpenCode or start a fresh session before running `评测`.

### Codex

- Codex uses workspace file tools pointed at the projection directory.
- Run a fresh-session activation probe before evaluation.
- The workspace-read fallback is a non-canonical install mode and must be recorded as fallback evidence by the external controller.

### Hermes

- Hermes uses workspace tools after install to read the pre-staged Skill bundle.
- Hermes `file://` limitation requires a pre-staged bundle; do not require live `file://` acquisition during a run.

## Trigger

| Trigger | Behavior |
|---------|----------|
| `评测` | Run task-001 (default) |
| `评测 task-001` | Run task-001 |
| `评测 task-002` | Run task-002 |
| `评测 task-003` | Run task-003 |
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
<!-- task-006 — Web Research — backlog-only; not installable or distributable in V3 -->

## Required Flow

1. Read `tasks/<task-id>/task.md`.
2. For static tasks: read every file under `tasks/<task-id>/inputs/`.
3. For environment tasks (task-004 and task-005): read `tasks/<task-id>/environment-contract.yaml` and any public contracts under `tasks/<task-id>/environment/public/` or `tasks/<task-id>/profiles/<profile>/public/`.
4. Read `tasks/<task-id>/output-requirements.md`.
5. Read `tasks/<task-id>/capability-contract.yaml` to understand what is being measured.
6. Create a new answer directory using this shape:

```text
<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/
├── task-id.txt
├── final-answer.md
├── artifacts/
└── run-metadata.json
```

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root. If you cannot determine the workspace root, stop and report preflight failure.

The `run-id` MUST be unique per evaluation run. Use a timestamp or UUID.

7. Fill `run-metadata.json` from `templates/run-metadata.json`. Set `run_status` to:
   - `"completed"` — all required artifacts produced
   - `"partial"` — some artifacts produced, some missing
   - `"aborted"` — directory created, no artifacts produced

   Use `UNAVAILABLE` for fields the harness cannot observe. Do not estimate tokens, timings, or tool calls.

8. Write `final-answer.md` and required files under `artifacts/`.
9. Report the answer directory path to the user.

## Completion Gate

Before setting `run_status` to `completed`:

1. Re-read the task's `output-requirements.md` using the harness-native read tool.
2. Verify every required filename exists under the run directory.
3. Verify every required Markdown heading exists literally (exact match, including punctuation).
4. Verify every JSON file parses without error.
5. Verify every required JSON key and value type exactly matches the declared schema.
6. Verify `run-metadata.json` contains every key from `templates/run-metadata.json`.
7. Verify `task-id.txt` contains exactly the correct task ID.
8. Set `run_status` to `partial` when any required item is missing or invalid.
9. Only report completion after all checks pass.

## Error Handling

| Condition | Action |
|-----------|--------|
| Skill directory is read-only | Write answers under workspace root, never inside the Skill directory |
| Workspace root is unknown | Stop and report preflight failure; do not guess paths |
| Output directory already exists | Append a new unique `run-id` |
| A required artifact cannot be created | Set `run_status` to `partial`, document missing artifacts in `run-metadata.json` |
| JSON output does not parse | Fix before attempting to mark completion |
| Required Markdown heading is missing | Fix before attempting to mark completion |
| Task 004 tests do not pass 5/5 after source repair | Re-examine the repair; do not mark completed with failing tests |
| Task 005 tool invocation returns an error | Re-read the tool contract and retry; log the error in the action log |
| Static task (001, 002, 003) attempted via `exec` or shell command | Stop; static tasks must use file tools only. Restart with correct tool profile. |

## Tool Authorization

This Skill does not declare `allowed-tools`. Tool authorization varies by task and harness:

| Task | Required Capabilities | VitaClaw Profile | Notes |
|------|----------------------|------------------|-------|
| 001 — Baseline Delivery | `read_skill_file`, `write_file` | static-eval | No `exec` |
| 002 — Multi-Source Investigation | `read_skill_file`, `write_file` | static-eval | No `exec` |
| 003 — Policy-Constrained Decision | `read_skill_file`, `write_file` | static-eval | No `exec` |
| 004 — Coding & Repair | file tools + code edit + restricted `exec` | coding-eval | `exec` restricted to `python3 -m unittest` and `python3 -m src.reconcile` |
| 005 — Stateful Tool Use | file tools + `skill_run`/`run_skill_script` | stateful-eval | VitaClaw: controller sets `AGENT_EVAL_TASK005_TOOL_API`, then use `skill_run` on `scripts/task005_tool.py`. Other harnesses: use canonical tool names per `environment/public/tool-contract.yaml`. |

The external UAT controller binds the correct Profile per task per harness. Do not use `exec` to invoke Task 005 tools. Do not use `exec` for static tasks.

## Rules

- Do not call any packaged execution, grading, orchestration, or child-agent control code.
- Do not create fake tool logs, fake token counts, fake timings, or fake grading results.
- Do not request or record hidden chain of thought.
- Do not self-grade the answer.
- Do not modify files under `tasks/<task-id>/evaluator-notes/` or `tasks/<task-id>/evaluator-private/`.
- For environment tasks (004-005): do not modify base project files in-place. Copy to `artifacts/project/` first.
- For stateful tasks (005): do not access the SQLite database directly. Use only the canonical tool interface.
- Task 006 is backlog-only and is not installable or distributable in V3.
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
