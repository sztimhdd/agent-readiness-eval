# UAT Diagnostic Report — Agent Readiness Eval Core v2.0

## Overview

| Field | Value |
|-------|-------|
| **Harness** | OpenCode |
| **Model** | deepseek-v4-pro (DeepSeek) |
| **Commit** | 2241e3a7f0ef59c08c17dd83a3aa8ce4c65670c6 |
| **Mode** | single_session_sequential |
| **Overall Status** | PASS |
| **Export Root** | `/Users/hai/agent-readiness-uat-controller/20260711T013426Z-2241e3a/opencode/export` |

## Task Results

| Task | Profile | Status | Defects |
|------|---------|--------|---------|
| task-001 — Baseline Delivery | default | completed | None |
| task-002 — Multi-Source Investigation | default | completed | None |
| task-003 — Policy-Constrained Decision | default | completed | None |
| task-004 — Coding & Repair | default | completed | None |
| task-005 — Stateful Tool Use | controlled_tool | completed | None |

## Defects by Category

### Harness Install/Activation Defects
- **Skill installation requires restart.** The agent-readiness-eval Skill was copied to `~/.config/opencode/skills/agent-readiness-eval-uat/` but could not be discovered by the `skill()` tool in the current session. The `direct_package_fallback` path was used — SKILL.md was read directly from `exam-workspace/skill/`. This is a known limitation of OpenCode's skill discovery mechanism. **Severity: Minor — fallback path available.**

### Observability Defects
- **Multiple metadata fields recorded as UNAVAILABLE.** OpenCode does not expose harness version, input/output token counts, total tokens, tool call counts, session IDs, or elapsed timing to the agent context. These are recorded as literal `UNAVAILABLE` per protocol. **Severity: Info — no impact on task execution, only on metadata completeness.**

### Distribution Defects
- None. All three distributions built successfully with no evaluator leaks detected.

### Source Contract Defects
- None. All 9 unittest tests passed (exit code 0).

### Agent Execution Defects
- None. All five tasks completed with all required files present and valid.

## Installation Details

- **Method:** Native file copy to `~/.config/opencode/skills/agent-readiness-eval-uat/`
- **Discovery:** Not verified (`skill("agent-readiness-eval-uat")` returned "not found")
- **Activation:** Restart required
- **Fallback:** Direct read of `exam-workspace/skill/SKILL.md`
- **Note:** Task execution was unaffected by the fallback; all tasks were completed following the Skill protocol directly.

## Evidence

| Artifact | Path |
|----------|------|
| Environment | `evidence/environment.txt` |
| Source Contract Tests | `evidence/source-contract-tests.txt` (9/9 passed) |
| Distribution Builds | `evidence/distribution-builds.txt` |
| Installation | `evidence/installation.txt` |
| Task-001 Answer | `answers/task-001-OpenCode-deepseek-v4-pro-uat-20260710T223730-311710d0/` |
| Task-002 Answer | `answers/task-002-OpenCode-deepseek-v4-pro-uat-20260710T223820-b835e309/` |
| Task-003 Answer | `answers/task-003-OpenCode-deepseek-v4-pro-uat-20260710T223958-cd3d0094/` |
| Task-004 Answer | `answers/task-004-OpenCode-deepseek-v4-pro-uat-20260710T224107-4256cdca/` |
| Task-005 Answer | `answers/task-005-OpenCode-deepseek-v4-pro-uat-20260710T224248-0a80460e/` |
