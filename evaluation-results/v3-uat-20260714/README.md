# Core v3 UAT — 2026-07-14

**Source commit:** `2da43b965c393ae7983200e834129b88f88b6787`  
**Mode:** local full-suite UAT, task-001 through task-005  
**Purpose:** preserve V3 Hermes/OpenCode answer artifacts and CTO-facing evaluation notes.

Start here: [`uat-comparison-report.md`](uat-comparison-report.md)

## UAT matrix

| Harness / model | Tasks completed | UAT result | Notes |
| --- | ---: | --- | --- |
| Hermes / DeepSeek V4 Flash | 5 / 5 | PASS | Cleanest V3 run; benign shutdown warning after artifacts were written. |
| OpenCode / DeepSeek V4 Pro | 5 / 5 | PARTIAL PASS | task-003 judgment issue and task-004 empty `test-before.txt`; task execution completed. |

## Directory guide

- [`hermes/deepseek-v4-flash/answers/`](hermes/deepseek-v4-flash/answers/) — five Hermes answer directories from the V3 full-suite run.
- [`opencode/deepseek-v4-pro/answers/`](opencode/deepseek-v4-pro/answers/) — five OpenCode answer directories from the V3 full-suite run.

No raw session logs, compressed bundles, runtime-state databases, or evaluator-only assets are included here.
