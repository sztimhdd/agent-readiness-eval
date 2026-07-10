# Agent Readiness Eval v3 PRD

## Goal

Provide a portable question pack that can be installed in VitaClaw, OpenClaw, Hermes, and OpenCode to compare native harness execution results.

## Core Principle

Benchmark content is portable; execution remains native to each harness.

## Scope

- `SKILL.md` with the task-taking protocol.
- Static tasks under `tasks/`.
- Output templates under `templates/`.
- Harness install notes and offline scoring guide under `docs/`.
- Contract tests that ensure no packaged execution architecture returns.

## Non-Goals

- Packaged execution engine.
- Packaged grading engine.
- Child-agent control layer.
- Result packaging, integrity, or privacy-scrubbing pipeline.
- Token estimation.

## Success Criteria

- The same package can be read by different harnesses without runtime dependencies.
- The harness creates an answer directory with `final-answer.md`, `artifacts/`, `run-metadata.json`, and `task-id.txt`.
- Offline reviewers can compare answers with the scoring guide.
- Missing harness metadata is recorded as `UNAVAILABLE`, not guessed.
