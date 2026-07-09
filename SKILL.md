---
name: agent-readiness-eval
description: Portable v3 question-pack skill for comparing agent harnesses by issuing tasks and collecting answer artifacts. Trigger with "评测".
category: evaluation
tags:
  - readiness
  - harness-eval
  - question-pack
  - vitaclaw
version: 3.0.0
allowed-tools: []
---

# Agent Readiness Eval v3

## Principle

Benchmark content is portable; execution remains native to each harness.

This Skill is a question pack, not an execution engine. It gives tasks and an answer format. The active harness must read the task, use its own tools, create answer artifacts, and stop.

## Trigger

When the user says `评测`, run the first task under `tasks/` unless the user names a specific task.

## Required Flow

1. Read `tasks/<task-id>/task.md`.
2. Read every file under `tasks/<task-id>/inputs/`.
3. Read `tasks/<task-id>/output-requirements.md`.
4. Create a new answer directory under `runs/` using this shape:

```text
runs/<task-id>-<harness-name>-<model-name>/
├── task-id.txt
├── final-answer.md
├── artifacts/
└── run-metadata.json
```

5. Fill `run-metadata.json` from `templates/run-metadata.json`. Use `UNAVAILABLE` for fields the harness cannot observe. Do not estimate token counts.
6. Write `final-answer.md` and required files under `artifacts/`.
7. Report the answer directory path to the user.

## Rules

- Do not call any packaged execution, grading, orchestration, or child-agent control code.
- Do not create fake tool logs, fake token counts, fake timings, or fake grading results.
- Do not request or record hidden chain of thought.
- Do not self-grade the answer.
- Do not use another agent to solve the task unless the current harness normally solves user tasks that way.
- If a metadata field is unavailable, write `UNAVAILABLE` exactly.

## Scoring

Scoring is offline and external to this Skill. Use `docs/OFFLINE-SCORING-GUIDE.md` for human review. The answer directory is the only artifact this Skill asks the harness to produce.
