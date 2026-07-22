# Agent Readiness Eval Core v4.0.0 PRD

## Goal

Provide a portable question pack that can be installed in VitaClaw, OpenClaw, Hermes, OpenCode, and Codex to compare native harness execution results with controller-captured trajectory evidence.

V4 releases task-001 through task-005. task-006 remains backlog-only and is not installable or distributable.

## Core Principle

Benchmark content is portable; execution remains native to each harness. Controller-captured trajectory events are the authoritative process record.

## Run Lifecycle

Every V4 run proceeds through six phases: package verification, preflight, answer directory creation (only if preflight `ready`), execution, controller evidence finalization, and status determination. Preflight blocked statuses (`adapter_blocked`, preflight `protocol_mismatch`) write only 2 controller files; runtime `protocol_mismatch` and all statuses where the agent started write all 5 controller files.

## Violation Dimensions

Violations are recorded with three orthogonal dimensions in `controller/protocol-violations.json`: `violation_type` (what happened), `enforcement_outcome` (blocked vs escaped vs executed), and `detection_timing` (runtime vs post_hoc). `evidence_fabrication` always maps to `enforcement_outcome: executed` and `detection_timing: post_hoc`.

## Profiles

Four named capability-authorization profiles: `static-eval` (canonical, shell blocked), `coding-eval` (project copy + restricted exec), `stateful-eval` (9 public tools), and `read_only_shell_fallback` (non-canonical, `shell.exec.read_only`, diagnostic-only). Profile bindings are in `contracts/uat-controller-contract.yaml`. Target-class precedence is in `contracts/trajectory-contract.yaml`.

## Scope

- `SKILL.md` with the V4 protocol including preflight, trajectory contract, and 50/50 scoring model.
- Five redesigned tasks under `tasks/` that fix V3 benchmark defects.
- Controller evidence templates under `templates/`.
- V4 contract tests that verify the protocol and task structure.
- V3 regression tests that verify V3 historical evidence is preserved.

## Non-Goals

- Packaged execution engine.
- Packaged grading engine.
- Child-agent control layer.
- Result packaging, integrity, or privacy-scrubbing pipeline.
- Token estimation.
- V3 backward-compatibility shims.

## Success Criteria

- The same package can be read by different harnesses without runtime dependencies.
- The harness runs a preflight probe before starting any scored task.
- The harness creates an answer directory with `answer/` and `controller/` subdirectories.
- Controller evidence is authoritative when agent claims conflict with observed actions.
- Offline reviewers can score Outcome (50 points) and Process (50 points) separately.
- Missing harness metadata is recorded as `UNAVAILABLE`, not guessed.
- V3 answer directories remain as historical evidence and are not rescored as V4.
