# Agent Readiness Eval v3 TDD

## Architecture

```text
SKILL.md
→ tasks/<task-id>/task.md
→ tasks/<task-id>/inputs/*
→ tasks/<task-id>/output-requirements.md
→ harness-native execution
→ runs/<task-id>-<harness>-<model>-<run-id>/ answer directory
→ offline human scoring
```

## Package Boundary

The package contains content and output contracts only. It has no executable control plane.

## Task Format

Each task directory contains:

```text
task.md
inputs/
output-requirements.md
```

There is no oracle solution, hidden grading script, or hidden expected-answer file.

## Answer Format

Each answer directory contains:

```text
task-id.txt
final-answer.md
artifacts/
run-metadata.json
```

`run-metadata.json` follows `templates/run-metadata.json` and uses `UNAVAILABLE` for unknown fields.

## Verification

Development verification is limited to package contract tests. Runtime scoring is offline and external.
