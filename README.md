# Agent Readiness Eval v3

`agent-readiness-eval` is a portable question-pack Skill. It issues tasks and defines the answer format. It does not execute, grade, sanitize, package, or certify results.

The design follows the useful split from SecPriv Skill, Harbor, Terminal-Bench, and Meta-Harness:

- Skill content is portable.
- Harness execution remains native.
- Dataset/task, harness, model, and scoring are separate variables.
- Offline reviewers score answer artifacts after the run.

## Package Shape

```text
agent-readiness-eval/
├── SKILL.md
├── README.md
├── skill.json
├── tasks/
│   └── task-001/
│       ├── task.md
│       ├── inputs/
│       │   └── data.json
│       └── output-requirements.md
├── templates/
│   ├── run-metadata.json
│   └── completion-summary.md
├── docs/
│   ├── PRD_v3.md
│   ├── TDD_v3.md
│   ├── INSTALL-VITACLAW.md
│   ├── INSTALL-OPENCLAW.md
│   ├── INSTALL-HERMES.md
│   └── OFFLINE-SCORING-GUIDE.md
└── tests/
    └── test_v3_contract.py
```

## How to Run

Install this Skill in a compatible harness. Send one message:

```text
评测
```

The harness should read `tasks/task-001/`, solve it using its own native tools, and write an answer directory under `runs/`.

## Answer Directory

```text
runs/<task-id>-<harness-name>-<model-name>/
├── task-id.txt
├── final-answer.md
├── artifacts/
└── run-metadata.json
```

Use `UNAVAILABLE` for metadata the harness cannot observe. Do not estimate token usage.

## What This Package Does Not Include

This package has no packaged execution engine, grading engine, child-agent control layer, result packaging pipeline, privacy scrubber, integrity manifest, or answer key.

Those concerns belong to each harness or to a separate offline review layer.
