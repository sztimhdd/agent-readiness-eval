# Agent Readiness Eval V3 UAT Results

Date: 2026-07-14  
Repository/worktree: `/Users/hai/Projects/agent-readiness-eval/.worktrees/v3-evaluation-stabilization`  
Archive directory: `/Users/hai/Projects/agent-readiness-eval/evaluation-results/v3-uat-20260714`  
Source commit under test: `2da43b965c393ae7983200e834129b88f88b6787`  
Suite: Agent Readiness Eval Core V3, tasks `task-001` through `task-005`

## Executive Summary

Hermes and OpenCode both completed the full V3 suite and produced answer directories for all five tasks.

Hermes is the cleaner run: all five tasks are artifact-complete, JSON-valid, and semantically aligned with the expected task behavior. One non-blocking Hermes issue remains: shutdown prints `RuntimeError: Event loop is closed` after artifacts are written. Task 005 also contains one logged failed extra tool call caused by the state machine rejecting a second `request_information` transition; the final state is still correct.

OpenCode completed all five tasks, but two CTO-visible findings remain. First, `task-004` has an empty `artifacts/test-before.txt`, violating the output requirement that it capture the pre-fix test run with exactly 2 failures and 1 error. Second, `task-003` makes a weaker policy decision for `DAT-2025-008`: it records `HOLD` where Hermes correctly escalates the legal subpoena request to joint Legal + DPO review. OpenCode's code repair and stateful tool tasks otherwise completed successfully.

Overall recommendation: treat Hermes DeepSeek V4 Flash as PASS for this UAT round. Treat OpenCode DeepSeek V4 Pro as PARTIAL PASS: execution completed, but the evidence-capture defect in task-004 and policy judgment defect in task-003 should be fixed or re-run before CTO sign-off.

## Harness Matrix

| Harness | CLI Version | Model | Result | Notes |
|---|---:|---|---|---|
| Hermes | `0.18.2` | `deepseek-v4-flash` | PASS | 5/5 tasks complete; known benign shutdown error after run |
| OpenCode | `1.17.11` | `deepseek/deepseek-v4-pro` | PARTIAL PASS | 5/5 tasks complete; task-003 judgment issue, task-004 missing pre-fix evidence |

## Run Directory Index

### Hermes

| Task | Status | Answer Directory |
|---|---|---|
| task-001 | PASS | `hermes/deepseek-v4-flash/answers/task-001-hermes-deepseek-v4-flash-20260714T001901` |
| task-002 | PASS | `hermes/deepseek-v4-flash/answers/task-002-hermes-deepseek-v4-flash-20260714T001901` |
| task-003 | PASS | `hermes/deepseek-v4-flash/answers/task-003-hermes-deepseek-v4-flash-20260714T001901` |
| task-004 | PASS | `hermes/deepseek-v4-flash/answers/task-004-hermes-deepseek-v4-flash-20260713-212334-45626` |
| task-005 | PASS | `hermes/deepseek-v4-flash/answers/task-005-hermes-deepseek-v4-flash-20260713-212334-45626` |

### OpenCode

| Task | Status | Answer Directory |
|---|---|---|
| task-001 | PASS | `opencode/deepseek-v4-pro/answers/task-001-opencode-deepseek-v4-pro-20260713-220000` |
| task-002 | PASS | `opencode/deepseek-v4-pro/answers/task-002-opencode-deepseek-v4-pro-20260713-220100` |
| task-003 | PARTIAL | `opencode/deepseek-v4-pro/answers/task-003-opencode-deepseek-v4-pro-20260713-220200` |
| task-004 | PARTIAL | `opencode/deepseek-v4-pro/answers/task-004-opencode-deepseek-v4-pro-20260713-220300` |
| task-005 | PASS | `opencode/deepseek-v4-pro/answers/task-005-opencode-deepseek-v4-pro-20260713-220400` |

## Per-Task Evaluation

### Task 001 — Baseline Delivery

Result: PASS on both harnesses.

Both Hermes and OpenCode produced valid `artifacts/triage-summary.json` with the required keys:

- `task_id`
- `severity_counts`
- `area_counts`
- `top_risk`
- `supporting_ticket_ids`
- `recommended_actions`

Observed summary counts matched between harnesses:

| Metric | Hermes | OpenCode |
|---|---|---|
| Severity counts | critical 1, high 3, medium 1, low 1 | critical 1, high 3, medium 1, low 1 |
| Area counts | authentication 1, billing 2, agent-runtime 2, dashboard 1 | authentication 1, billing 2, agent-runtime 2, dashboard 1 |
| Top risk present | yes | yes |

### Task 002 — Multi-Source Investigation

Result: PASS on both harnesses.

Both harnesses produced valid `artifacts/investigation-summary.json` with the required investigation fields, including `timeline`, `confirmed_facts`, `likely_root_cause`, `supporting_evidence`, `inferences`, `unknowns`, `recommended_actions`, `confidence_level`, and `information_gaps`.

Both concluded the root cause was the `agent-runtime` v2.3.1 state ordering/write acknowledgement regression. Both reported high confidence.

### Task 003 — Policy-Constrained Decision

Result: Hermes PASS, OpenCode PARTIAL.

Hermes decisions:

| Request | Hermes Decision | Assessment |
|---|---|---|
| `PRC-2025-018` | HOLD | Correct: CFO approval still required; CEO exemption only waives bidding |
| `DAT-2025-007` | REJECT | Correct: requester refuses mandatory DPO approval/audit logging |
| `DAT-2025-008` | ESCALATE | Correct: subpoena requires joint Legal + DPO review |
| `TRV-2025-042` | APPROVE | Correct: all travel policy requirements satisfied |

OpenCode decisions:

| Request | OpenCode Decision | Assessment |
|---|---|---|
| `PRC-2025-018` | HOLD | Correct |
| `DAT-2025-007` | REJECT | Correct |
| `DAT-2025-008` | HOLD | Finding: should be ESCALATE for joint Legal + DPO review |
| `TRV-2025-042` | APPROVE | Correct |

Finding: OpenCode preserved artifact shape and completed the run, but the `DAT-2025-008` decision is semantically weaker than expected. The policy exception for legal compliance does not merely wait on missing paperwork; it requires joint Legal + DPO review, making escalation the better action.

### Task 004 — Coding & Repair

Result: Hermes PASS, OpenCode PARTIAL.

Both harnesses fixed the three injected bugs and achieved 5/5 passing tests after repair:

1. `mapper.py`: support matching used `company_name` instead of `account_id`.
2. `mapper.py` / `reconcile.py`: amount comparison mixed `int` and `float` string representations.
3. `reconcile.py`: `crm_status.lower()` crashed on missing status values.

Artifact evidence:

| Evidence | Hermes | OpenCode |
|---|---|---|
| `artifacts/test-before.txt` exists | yes, 3610 bytes | yes, but 0 bytes |
| `test-before.txt` shows 2 failures + 1 error | yes | no |
| `artifacts/test-after.txt` shows 5/5 passing | yes | yes |
| `artifacts/reconciliation-report.json` parses | yes | yes |
| Source repaired under `artifacts/project/src/` | yes | yes |

Finding: OpenCode ran the failing pre-fix tests, but captured output with shell redirection in the wrong order during the first attempt. The required `artifacts/test-before.txt` is empty. This violates Task 004 output requirements even though the repair itself succeeded.

### Task 005 — Stateful Tool Use

Result: PASS on both harnesses.

Final states matched exactly:

| Request | Expected/Observed Final State |
|---|---|
| `REQ-001` | approved |
| `REQ-002` | approved |
| `REQ-003` | information_requested |
| `REQ-004` | information_requested |
| `REQ-005` | rejected |
| `REQ-006` | escalated |

Hermes action log: 21 entries, 1 failed extra call.  
OpenCode action log: 18 entries, 0 failed calls.

Hermes attempted a second `request_information` call for `REQ-004` (`annual_review_clause`) after already requesting `cfo_approval`. The state machine rejected this because it does not allow transitioning from `information_requested` to `information_requested`. This is a useful design observation, but the required final state and documented rationale remain correct.

## Cross-Harness Findings

| Severity | Finding | Affected Harness | Recommendation |
|---|---|---|---|
| High | `task-004` pre-fix evidence file is empty | OpenCode | Re-run task-004 or patch CLI prompt/tooling to capture `stderr` and `stdout` correctly before CTO acceptance |
| Medium | `DAT-2025-008` should escalate, not hold | OpenCode | Improve policy exception reasoning for legal compliance workflows |
| Low | `suite_version` in `run-metadata.json` is `2.0.0` across both harnesses | Hermes, OpenCode | Update `templates/run-metadata.json` to `3.0.0` in V3 package |
| Info | Hermes prints `RuntimeError: Event loop is closed` after completion | Hermes | Track separately as Hermes shutdown cleanup; artifacts were already written |
| Info | Hermes task-005 logs one failed extra transition | Hermes | Consider tool API support for multi-field information requests or clarify task guidance |

## Sign-Off View

| Harness | Artifact Completion | Semantic Quality | Operational Stability | CTO Sign-Off Readiness |
|---|---|---|---|---|
| Hermes + DeepSeek V4 Flash | PASS | PASS | PASS with benign shutdown warning | Ready |
| OpenCode + DeepSeek V4 Pro | PARTIAL | PARTIAL | PASS | Needs task-003/task-004 remediation or accepted waiver |

## Notes For Reviewers

- This report does not self-grade offline scoring rubrics; it evaluates UAT execution, artifact completeness, schema validity, and visible decision quality.
- `runs/task-001-hermes-deepseek-v4-flash-20260713-1430` is an earlier single-task Hermes run and is not counted in the full-suite matrix.
- All listed answer directories are under the V3 stabilization worktree and can be inspected directly.
