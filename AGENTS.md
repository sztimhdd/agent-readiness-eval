# PROJECT KNOWLEDGE BASE

**Generated:** 2026-07-09
**Commit:** c1360ea
**Branch:** main

## OVERVIEW

Portable question-pack Skill for comparing agent harnesses. Pure content: tasks, templates, docs, and contract tests only; execution stays native to each harness.

## STRUCTURE

```text
agent-readiness-eval/
├── SKILL.md                 # harness-facing protocol; trigger: 评测
├── skill.json               # manifest; currently lists task-001 only
├── tasks/                   # static task packs
│   ├── task-001/            # customer ticket triage; canonical simple task
│   └── task-002/            # incident investigation; includes evaluator-only notes
├── templates/               # answer metadata/completion templates
├── docs/                    # PRD/TDD/install/scoring + task-002 design docs
└── tests/                   # stdlib unittest contract tests
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Skill protocol | `SKILL.md` | Read first before changing runtime-visible behavior |
| Manifest/tasks list | `skill.json` | `task-002` exists on disk but is not listed yet |
| Architecture boundary | `docs/PRD_v3.md`, `docs/TDD_v3.md` | Content-only package; no control plane |
| Human scoring | `docs/OFFLINE-SCORING-GUIDE.md`, `tasks/task-002/evaluator-notes/` | Evaluator material is not agent-visible during a run |
| Task authoring pattern | `tasks/task-001/` | Canonical shape: `task.md`, `inputs/`, `output-requirements.md` |
| Task 002 design rationale | `docs/task-002-*.md`, `tasks/task-002/task-design-note.md` | Development context for the new harder task |
| Contract tests | `tests/test_v3_contract.py` | Run after changes |

## CODE MAP

No application code. Only one executable development file:

| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| `V3ContractTests` | unittest class | `tests/test_v3_contract.py` | unmeasured | Guards package shape and v3 boundary |
| `FORBIDDEN_PATHS` | constant | `tests/test_v3_contract.py` | local | Blocks legacy execution/scoring artifacts |
| `FORBIDDEN_TERMS` | constant | `tests/test_v3_contract.py` | local | Blocks legacy architecture language in active docs |

## CONVENTIONS

- Task IDs use `task-NNN` (`task-001`, `task-002`).
- Answer dirs are runtime output under `runs/<task-id>-<harness-name>-<model-name>/`; `runs/` is gitignored.
- Required answer files: `task-id.txt`, `final-answer.md`, `artifacts/<task-specific>.json`, `run-metadata.json`.
- Metadata uses literal string `UNAVAILABLE` for fields a harness cannot observe. Never estimate tokens, timings, or tool calls.
- `tasks/<task-id>/inputs/` is agent-visible. `tasks/<task-id>/evaluator-notes/` is evaluator-only.
- Contract tests are structural only; runtime scoring remains offline and external.

## ANTI-PATTERNS

- Do not add packaged execution, grading, orchestration, child-agent control, result packaging, privacy scrubbers, or token estimation.
- Do not add hidden answer/grading files inside task directories.
- Do not add top-level execution-support directories; keep the denylist centralized in `tests/test_v3_contract.py`.
- Do not fabricate tool logs, token counts, timings, or grading results.
- Do not self-grade task answers; offline reviewers score only answer-directory artifacts.
- Do not make tasks depend on external network, APIs, GUI/browser, code execution, Docker, or harness-specific tools unless the PRD changes.

## UNIQUE STYLES

- This repo is intentionally not a normal app/library. Missing build files and dependency manifests are expected.
- Tests obfuscate forbidden strings with concatenation to avoid self-matching; keep that style when extending lists.
- Task 002 intentionally has design/evaluator material; keep it separate from `inputs/` and never treat it as agent-visible input.
- `templates/completion-summary.md` exists but is not currently referenced by `SKILL.md`.

## COMMANDS

```bash
python3 -m unittest discover tests
```

No build command. No runtime dependencies beyond the active harness reading/writing files.

## NOTES

- Discovery found 29 tracked/untracked content files and no existing `AGENTS.md`.
- Current drift to resolve separately: `skill.json` and `README.md` describe only `task-001` while `tasks/task-002/` exists.
- If registering Task 002, update `skill.json`, README package shape, and likely generalize the task-shape contract test to cover all `tasks/task-*` directories.
