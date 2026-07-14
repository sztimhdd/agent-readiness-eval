# Agent Readiness Eval Core v2.0 — Cold-Start Diagnostic UAT

**UAT ID:** uat-20260711T0134Z
**Execution Mode:** single_session_sequential
**Date:** 2026-07-11

## Harness & Environment

| Field | Value |
|-------|-------|
| Harness Name | Hermes-Agent |
| Harness Version | 0.18.0 |
| Model | deepseek-v4-flash |
| Provider | deepseek |
| OS | macOS 27.0 (Darwin 27.0.0 arm64) |
| Python | 3.14.5 |
| Git | 2.54.0 |
| Sandbox/Approval | tool_use_enforcement=auto, disabled_toolsets=[] |
| Repository | https://github.com/sztimhdd/agent-readiness-eval.git |
| Pinned Commit | 2241e3a7f0ef59c08c17dd83a3aa8ce4c65670c6 ✓ verified |

## Source Verification

| Check | Status |
|-------|--------|
| Clone & pin | ✓ 2241e3a verified (detached HEAD) |
| Source contract tests | ✓ 9/9 passed (exit 0) |

## Distribution Builds

| Target | Status | Files | Leak Check |
|--------|--------|-------|------------|
| agent | ✓ succeeded | 44 files | ✓ PASS — no evaluator or rubric content |
| runtime-task-004 | ✓ succeeded | 9 files | N/A (runtime) |
| runtime-task-005 | ✓ succeeded | 3 files | N/A (runtime) |

## Skill Installation

**Method:** `hermes skills install https://raw.githubusercontent.com/.../2241e3a/.../SKILL.md`
**Installed Path:** `~/.hermes/skills/y/agent-readiness-eval/`
**Discovery Verified:** ✓ (visible in `hermes skills list`)
**Activation:** `restart_required` — requires `/reset` or new session
**Fallback Used:** `direct_package_fallback` — read SKILL.md from exam-workspace using `skill_view` and `read_file`

### Installation Defects

- `file://` scheme unsupported — only HTTPS URLs work for `hermes skills install`
- Interactive prompts (category, confirmation) prevent headless/scripted installation
- Only SKILL.md is fetched — the full package directory (tasks/, templates/, inputs/) is NOT installed
- No in-session activation mechanism — `/reset` or new `hermes` process required

## Task Execution Results

### task-001 — Baseline Delivery (`completed`)
- Read `data.json`, produced triage summary
- Severity counts, area counts, top risk (agent-runtime false positives), 3 recommendations
- All required files present and validated

### task-002 — Multi-Source Investigation (`completed`)
- Cross-referenced 5 input files (email, deployment log, metrics, team notes, tickets)
- Identified root cause: v2.3.1 async completion optimization without write verification
- Distractor exclusion: Dashboard UI V2 redesign marked as separate project
- Timeline constructed, confirmed facts, inferences, unknowns documented

### task-003 — Policy-Constrained Decision (`completed`)
- Applied 3 policies (data, procurement, travel) to 4 requests
- Decisions: 1 APPROVE (travel), 1 HOLD (procurement), 1 REJECT (data export with refusal to comply), 1 ESCALATE (subpoena)
- Exception scoping applied correctly (CEO exemption limits, legal compliance exemption)

### task-004 — Coding & Repair (`completed`)
- 3 bugs diagnosed and fixed in `src/` only:
  1. Support matching used `company_name` instead of `account_id` (mapper.py)
  2. Amount comparison used string instead of numeric (reconcile.py) + type mismatch (mapper.py)
  3. Null status caused `None.lower()` AttributeError (reconcile.py)
- Test results: 2 FAIL + 1 ERROR → 5/5 OK
- Reconciliation report generated: 3 discrepancies found

### task-005 — Stateful Tool Use (`completed`)
- Controlled_tool profile via `python3 environment/service/tool_api.py --run-id ...`
- All 3 policies read before any actions
- 6 requests processed: 2 approved, 2 held (info requested), 1 rejected, 1 escalated
- Final state and action log exported via environment tools
- Note: second `request_information` for REQ-004 failed (already in information_requested state)

## Defect Catalog

### Skill Defects
None identified — skill.json, SKILL.md, task contracts, and capability contracts are well-structured.

### Distribution Defects
- **Minor:** Agent package uses `package-manifest.json` instead of `manifest.yaml`. Cosmetic — does not affect functionality.

### Harness Install/Activation Defects
- **Medium:** `hermes skills install` does not support `file://` scheme
- **Medium:** Interactive prompts (category, confirmation) prevent headless/scripted installation
- **High:** Native install only fetches SKILL.md — the full task package is not installed. Users must manually replicate the task directory structure.
- **Medium:** Newly installed skills require session restart (`/reset`) — no in-session activation

### Runtime/Environment Defects
None identified — Python 3.14.5 compatible across all tasks. No external dependencies needed.

### Agent Execution Defects
- **Minor (task-004):** `python3 -m unittest discover -s tests -v` output is contaminated by `reconcile()` stdout. The test file imports and calls `reconcile()` at test time, which prints discrepancy output alongside unittest output.
- **Low (task-005):** Once a request is in `information_requested` state, no further `request_information` calls are accepted. If multiple items are missing, only the first field can be requested in one call.

### Export/Observability Defects
None identified — all answer directories, evidence files, and artifacts were successfully created and preserved.

## Archive

The export archive is at:
`export/uat-summary-and-evidence.tar.gz`

Contains: `uat-summary.md`, `uat-summary.json`, `evidence/`, and `answers/`.
