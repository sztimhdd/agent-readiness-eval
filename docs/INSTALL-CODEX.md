# Install in Codex

Install a generated agent-visible copy of this question pack. Do not install the
authoring repository directly: it contains evaluator-only materials that must not be
available to the evaluated agent.

## Build an agent-visible projection

From a clean, committed checkout of this repository, run the following commands. They
copy only the files the agent needs; in particular, they do not copy
`evaluator-notes/`, design notes, reports, or previous runs.
The default installed destination is `~/.codex/skills/agent-readiness-eval`.

```bash
SOURCE="$(pwd -P)"
STAGING="$(mktemp -d "${TMPDIR:-/tmp}/agent-readiness-eval.XXXXXX")"
INSTALL_DIR="$HOME/.codex/skills/agent-readiness-eval"

cp "$SOURCE/SKILL.md" "$STAGING/"
cp "$SOURCE/skill.json" "$STAGING/"
mkdir -p "$STAGING/templates" "$STAGING/tasks"
cp "$SOURCE/templates/run-metadata.json" "$STAGING/templates/"

for task_dir in "$SOURCE"/tasks/task-*; do
  task_name="$(basename "$task_dir")"
  mkdir -p "$STAGING/tasks/$task_name"
  cp "$task_dir/task.md" "$STAGING/tasks/$task_name/"
  cp "$task_dir/output-requirements.md" "$STAGING/tasks/$task_name/"
  cp -R "$task_dir/inputs" "$STAGING/tasks/$task_name/"
done

find "$STAGING" -path '*/evaluator-notes/*' -print
```

The final command must print nothing. If it prints a path, remove the staging copy
and correct the projection before installing it.

## Replace the installed Skill

Only replace the installation after the staging check is clean. This keeps a known
working Skill available if the projection process fails.

```bash
if [ -e "$INSTALL_DIR" ]; then
  backup="$INSTALL_DIR.backup-$(date +%Y%m%d%H%M%S)"
  mv "$INSTALL_DIR" "$backup"
fi

mkdir -p "$(dirname "$INSTALL_DIR")"
mv "$STAGING" "$INSTALL_DIR"
find "$INSTALL_DIR" -path '*/evaluator-notes/*' -print
```

Again, the final command must produce no output. Restart Codex or begin a new Codex
task so it discovers the new local Skill.

## Run a task

In a fresh Codex task, send an explicit task identifier:

```text
评测 task-001
```

The agent should create a new answer directory under the installed Skill's `runs/`
directory. Never reuse or edit an answer directory after its run; use a new run ID
for every attempt.

## Repeatable comparison protocol

Before each batch, rebuild the installed projection from a clean Git revision. Keep a
run ledger outside the installed Skill with one row per run containing:

| Field | Record |
|---|---|
| Source revision | `git rev-parse HEAD` from the source checkout |
| Projection timestamp | UTC installation time |
| Codex version | exact client version |
| Model and provider | exact selected values, or `UNAVAILABLE` |
| Task and run ID | for example `task-001`, `r01` |
| Tool and sandbox policy | exact Codex settings |
| Answer directory | immutable output path |

Hold the source revision, Codex version, model/provider, tool policy, task, and
prompt constant within a comparison cell. Run each model/task cell at least three
independent times. Compare per-task distributions and reviewer scores; do not infer a
single overall model ranking from six static tasks.

## Release check

Before rebuilding a comparison batch, run:

```bash
git status --short
python3 -m unittest discover tests
```

Use a clean source revision and a passing contract suite. Uncommitted task changes
make a batch non-reproducible and must be recorded explicitly if they are intentional.
