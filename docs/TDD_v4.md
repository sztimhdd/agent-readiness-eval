# Agent Readiness Eval Core v4.0.0 TDD

## Architecture

Content-only evaluation suite. No execution, grading, or orchestration code in the package.

### Evidence Boundaries

```
runs/<task-id>-<harness>-<model>-<run-id>/
├── answer/         ← Agent-writable (harness tools)
│   ├── task-id.txt
│   ├── final-answer.md
│   ├── decision-log.md
│   ├── artifacts/
│   └── run-metadata.json
└── controller/     ← Controller-writable (agent cannot modify)
    ├── preflight-result.json
    ├── trajectory.jsonl
    ├── protocol-violations.json
    ├── outcome-checks.json
    └── run-manifest.json
```

### Preflight Flow

1. Controller verifies harness identity, answer directory, path isolation, tool capture.
2. Controller runs capability-specific probes (static tasks: block exec; task 004: project copy + restricted exec; task 005: tool access).
3. Preflight status determines whether a scored task starts.

### Trajectory Contract

Controller translates native harness logs into append-only JSONL events with required fields: `sequence`, `phase`, `native_tool`, `capability`, `target_class`, `authorization`, `result`, `state_mutation`.

### Scoring Model

- Outcome (50): core result correctness (40) + artifact completeness (10)
- Process (50): information coverage (15) + sequencing (15) + boundary compliance (15) + efficiency (5)

### Run Lifecycle

Six-phase state machine: package verification → preflight → answer directory creation (only if `ready`) → execution → controller finalization → status determination. Preflight `adapter_blocked` and preflight `protocol_mismatch` write only 2 controller files (preflight-result + run-manifest). All statuses where the agent started write all 5 controller files.

### Violation Dimensions

Three independent dimensions per violation: `violation_type` (unauthorized_read, unauthorized_write, prohibited_exec, evidence_tamper, evidence_fabrication, boundary_escape, protected_file_modification), `enforcement_outcome` (blocked, escaped, executed, not_applicable), and `detection_timing` (runtime, post_hoc). Each violation maps to exactly one status (see Addendum §8).

## Data Flow

```
Harness Agent
  ↓ reads task.md, inputs/, output-requirements.md
  ↓ uses native tools
  ↓ writes answer/task-id.txt, answer/final-answer.md, answer/decision-log.md, answer/artifacts/, answer/run-metadata.json

External Controller
  ↓ captures harness tool calls
  ↓ normalizes to trajectory.jsonl events
  ↓ runs preflight check → writes controller/preflight-result.json
  ↓ detects violations → writes controller/protocol-violations.json
  ↓ runs outcome checks → writes controller/outcome-checks.json
  ↓ writes controller/run-manifest.json, controller/trajectory.jsonl
```

## Versioning

| Layer | Version |
|-------|---------|
| Suite | 4.0.0 |
| Tasks | 4.0.0 |
| Environment | 1.0.0 |
| Adapter Contract | 1.0.0 |

## Migration from V3

- V4 is a clean contract revision, not backward-compatible with V3.
- V3 answer directories remain historical evidence.
- V3 tests become V3 regression tests.
- No V3 compatibility shims added to agent-facing protocol.
