# Repeatable Codex Skill Installation Design

## Goal

Run Agent Readiness Eval through Codex without exposing evaluator-only materials to
the evaluated agent, and make each run reproducible from a known source revision and
installation configuration.

## Boundaries

- The repository remains the authoring source of truth.
- The Codex-installed skill is a generated, agent-visible projection of the source.
- Evaluator notes, design notes, reports, and prior answer directories are excluded
  from the installed projection.
- The package keeps its content-only boundary: no packaged runner or scorer is added.

## Installed Projection

Install to `~/.codex/skills/agent-readiness-eval/` with only:

```text
SKILL.md
skill.json
templates/run-metadata.json
tasks/task-*/task.md
tasks/task-*/inputs/**
tasks/task-*/output-requirements.md
```

The installed `SKILL.md` must not declare an empty tool allowlist. Codex needs its
normal local file read/write capability to complete a task.

## Repeatability Contract

Each evaluated run uses a fresh task-specific answer directory and records:

- task ID;
- exact Codex-selected model and provider when observable;
- source Git revision and installed-skill content revision in a run manifest;
- the original answer artifacts, without post-run edits.

The source projection is rebuilt before a comparison batch. A batch holds task,
Codex version, model selection, installed-skill revision, and environment policy
constant. Each model/task cell is repeated at least three times; results are reported
per task and distribution, not collapsed into an unsupported single ranking.

## Verification

The initial acceptance check runs Task 001 and asserts that the answer directory has
the four required files, valid JSON artifact and metadata, exact task ID, and
`UNAVAILABLE` for unavailable observability fields. It does not score answer quality
or access evaluator notes.

## Error Handling

If an installed copy already exists, save it to a timestamped backup before replacing
it. If a source task is incomplete or untracked, the build reports that condition and
does not silently claim the installed set is a repository-only release.
