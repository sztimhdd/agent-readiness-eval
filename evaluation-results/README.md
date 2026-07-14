# Evaluation results archive

This directory is a reviewable archive of answer artifacts and UAT reports, grouped by **harness / model**.  It intentionally contains no packaged source distribution, evaluator-only material, raw session logs, database/runtime state, or compressed UAT bundles.

## Current comparison sets

### Core v3 local UAT

The latest local V3 batch is [`v3-uat-20260714/`](v3-uat-20260714/). It preserves the Hermes and OpenCode full-suite answer directories and a CTO-facing comparison report.

| Harness | Model | Tasks completed | UAT result | Notes |
| --- | --- | ---: | --- | --- |
| Hermes | DeepSeek V4 Flash | 5 / 5 | PASS | Cleanest V3 run; benign shutdown warning after artifacts were written. |
| OpenCode | DeepSeek V4 Pro | 5 / 5 | PARTIAL PASS | task-003 judgment issue and task-004 missing pre-fix evidence capture. |

See [`v3-uat-20260714/uat-comparison-report.md`](v3-uat-20260714/uat-comparison-report.md) for CTO review.

### Core v2 cold-start UAT

The comparable batch is [`v2-uat-20260711/`](v2-uat-20260711/).  Each harness was asked to clone and pin commit `2241e3a7f0ef59c08c17dd83a3aa8ce4c65670c6`, install the Skill natively where possible, then complete task-001 through task-005 in one sequential session.  The raw, canonical answer directories and harness summaries are preserved below each model directory.

| Harness | Model | Tasks completed | Offline review score | Notes |
| --- | --- | ---: | ---: | --- |
| OpenCode | DeepSeek V4 Pro | 5 / 5 | 448 / 500 (89.6%) | Native discovery needed restart; direct package fallback used. |
| Hermes | DeepSeek V4 Flash | 5 / 5 | 495 / 500 (99.0%) | Native installation fetched only `SKILL.md`; direct package fallback used. |
| Codex | GPT-5.4 Mini | 5 / 5 | 443 / 500 (88.6%) | Native activation was not confirmed in session; direct package fallback used. |

Scores are a single-run diagnostic review, not a statistically valid model ranking.  They are documented here so reviewers can trace every judgement to the retained answer artifacts.  The test pack itself exposed two material design issues: task-003 rubric/summary inconsistency can trigger a veto despite correct structured output, and task-005's expected information field conflicts with the state machine.

### Execution constraints and non-results

- **Codex + GPT-5.6 Terra:** not executed; the shared quota was exhausted before the run.  No answer artifact is represented as a result.
- **VitaClaw:** blocked before task execution.  Its sandbox denied access to `github.com`, `raw.githubusercontent.com`, and `api.github.com`, and did not expose bare `bash`, `git`, or `python3`.  It needs GitHub egress or a pre-staged pinned repository, plus either basic execution tools or pre-built packages.  The original export was not available locally, so it is not fabricated in this archive.

## Directory guide

- [`v3-uat-20260714/`](v3-uat-20260714/) — latest V3 Hermes/OpenCode UAT report and answer directories.
- [`v2-uat-20260711/opencode/deepseek-v4-pro/`](v2-uat-20260711/opencode/deepseek-v4-pro/) — summary, source-contract evidence, and five canonical answer directories.
- [`v2-uat-20260711/hermes/deepseek-v4-flash/`](v2-uat-20260711/hermes/deepseek-v4-flash/) — summary, source-contract evidence, and five canonical answer directories.
- [`v2-uat-20260711/codex/gpt-5.4-mini/`](v2-uat-20260711/codex/gpt-5.4-mini/) — summary, source-contract evidence, and five canonical run directories.  The original flat `answers/` export is deliberately omitted because it lost per-run directory boundaries.
- [`historical/`](historical/) — local, incomplete V2 and legacy V1 OpenCode artifacts retained for traceability only; do not include them in the table above or compare them to the cold-start batch.

## Discovery note (2026-07-13)

The project worktree, ignored local `runs/`, `output/`, and the current remote `main` history were inspected before publishing.  No complete V3 UAT answer set was found.  This archive is therefore a V2 comparison baseline plus separately labelled historical material; V3 results should be added as a new dated batch when they exist.
