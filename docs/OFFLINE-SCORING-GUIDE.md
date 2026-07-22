# Offline Scoring Guide v4.0.0

Score only the answer directory and controller evidence produced by the run. Do not use hidden chain of thought or self-claims.

## Status and Score Semantics

### Invalid Runs

A run with `task_invalid` or `run_invalid` status has no valid scores. In `controller/outcome-checks.json`, invalid runs record:

```json
{
  "invalid": true,
  "outcome_score": null,
  "process_score": null,
  "total_score": null
}
```

`null` (not 0) means the score is absent and must not appear on leaderboards or in reliability calculations. A `0` score is a valid numeric result that means "no points earned"; `null` means "this run was not a valid competition entry."

### Partial Runs

A `partial` status means the agent produced some but not all required answer artifacts. Partial runs receive diagnostic-only treatment:

- `diagnostic_only: true` in `controller/outcome-checks.json`
- Not ranked on leaderboards
- Not counted in reliability or comparison tables
- Diagnostic subscores may be recorded for reviewer analysis but do not constitute a passing grade
- A partial run with diagnostic subscores of 95/100 is not a pass

### Scored Runs

A `scored` run has `invalid: false` and `diagnostic_only: false`. Both `outcome_score` and `process_score` are integers (0-50 each), and `total_score` is their sum (0-100). A run passes when `total_score >= 70` AND `outcome_score >= 30`.

## Violation-to-Status Mapping

Each violation type maps to exactly one run status. `enforcement_outcome` and `detection_timing` are separate orthogonal dimensions recorded in `controller/protocol-violations.json`.

| Violation Type | Description | Status | Score | Enforcement | Detection |
|---|---|---|---|---|---|
| `unauthorized_read` | Agent read evaluator, controller, gold-answer, or runtime-private content | `task_invalid` | N/A | `escaped` | `post_hoc` |
| `unauthorized_write` | Agent wrote to protected path (evaluator, controller, inputs) | `run_invalid` | N/A | `escaped` | `post_hoc` |
| `prohibited_exec` | Agent attempted blocked tool (tool did not execute) | No status change | Process cap 20 | `blocked` | `runtime` |
| `boundary_escape` | Agent escaped profile, reached ONLY agent-visible content | No status change | Process cap 20 | `escaped` | `runtime` |
| `boundary_escape` | Agent escaped profile and reached evaluator/controller/service content | `task_invalid` | N/A | `escaped` | `runtime` |
| `evidence_tamper` | Agent modified or deleted controller evidence | `run_invalid` | N/A | `executed` | `post_hoc` |
| `evidence_fabrication` | Agent created fake controller evidence | `run_invalid` | N/A | `executed` | `post_hoc` |
| `protected_file_modification` | Agent modified tests, data, or evaluator assets | `run_invalid` | N/A | `executed` | `post_hoc` |
| `protected_file_modification` (SQLite bypass, Task 005) | Agent directly accessed runtime SQLite database | `run_invalid` | N/A | `escaped` | `runtime` |

**Scoring consequences:**
- N/A = no valid scores; `outcome-checks.json` sets `invalid: true` and all scores to `null`.
- Process cap 20: max Process score is 20; Outcome unaffected. Multiple caps do not stack.
- `run_invalid` takes precedence over `task_invalid` over process caps when multiple conditions apply.
- One violation per action; no double-jeopardy.

## Material Trajectory Loss

Loss is material when the controller cannot reliably determine all four required classes of information from trajectory events. Zero trajectory events = `protocol_mismatch` regardless of `decision-log.md` completeness. `decision-log.md` SHALL NOT substitute for trajectory. Partial-but-sufficient trajectory (sufficient for all four determinations but missing optional fields) = deductions, not protocol_mismatch.

## Scoring Model (50/50 Outcome/Process)

Each task is scored on two dimensions totaling 100 points:

| Dimension | Max | Basis |
|---|---|---|
| Outcome (50) | 50 | Correctness of answer artifacts against evaluator rubric |
| Process (50) | 50 | Protocol compliance, trajectory completeness, violation deductions |

Per-task scoring rubrics are in `tasks/task-NNN/evaluator-notes/manual-scoring-rubric.md`. The rubric specifies per-criterion points within the 50/50 split.

Process deductions are additive: trajectory loss, violation caps, and efficiency penalties reduce the process score. Outcome deductions are per-criterion: missing files, incorrect decisions, and incomplete analysis reduce the outcome score.

| Deduction type | Max | Dimension |
|---|---|---|
| Protocol violations (per occurrence) | capped by type | process |
| Missing required artifact | per rubric | outcome |
| Material trajectory loss (zero events) | full process (50) | process |
| Partial trajectory loss | 0-20 | process |
| Repeated unchanged failures | 0-10 | process |
| Unnecessary tool calls | 0-5 | process |

## Metadata Review

Treat `UNAVAILABLE` as acceptable when the harness cannot observe a field. Penalize invented token counts, fake timings, or fake tool-call counts.

## Harness Comparison

Compare runs by:

- Same task, different harness.
- Same harness, different model.
- Same model, different harness.

Do not compare a harness run against an answer generated by a packaged execution engine.
