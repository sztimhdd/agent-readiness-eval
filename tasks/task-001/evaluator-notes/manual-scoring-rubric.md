# Task 001 — Manual Scoring Rubric

## Total Score: 100 points

### 1. Source Authority Resolution — 20 points

| Score | Condition |
|-------|-----------|
| 20 | Correctly applies `ticket-update-log.md` > `data.json` precedence for all tickets; demonstrates understanding of resolution notes as highest authority |
| 15 | Applies precedence correctly for most tickets but misses one reclassification |
| 10 | Relies primarily on `data.json` severity without consulting update log |
| 5 | Ignores update log entirely |
| 0 | Wrong source precedence |

### 2. Severity Counts Correctness — 20 points

| Score | Condition |
|-------|-----------|
| 20 | All severity counts correct after reclassification: critical=1, high=3, medium=3, low=3 |
| 15 | One count incorrect |
| 10 | Two counts incorrect |
| 5 | Three+ counts incorrect |
| 0 | No severity counts provided or completely wrong |

### 3. Stale Label Identification — 15 points

| Score | Condition |
|-------|-----------|
| 15 | All three stale labels correctly identified (T-1007, T-1008, T-1009) with correct corrected severity |
| 10 | Two of three identified correctly |
| 5 | One identified correctly |
| 0 | None identified or wrong labels |

### 4. Top Risk Identification — 15 points

| Score | Condition |
|-------|-----------|
| 15 | Identifies agent-runtime reliability as top risk with T-1003 and T-1005 as supporting evidence |
| 10 | Identifies agent-runtime but only cites one ticket or vague evidence |
| 5 | Identifies a secondary risk area as primary |
| 0 | No risk identified or completely wrong |

### 5. Action Recommendations — 15 points

| Score | Condition |
|-------|-----------|
| 15 | Three concrete actions covering critical fix, second agent-runtime issue, and systemic improvement; notes resolution status where available |
| 10 | Three actions but one is vague, or missing resolution status notes |
| 5 | Two actions or actions are generic |
| 0 | No actions or completely generic ("fix bugs") |

### 6. Output Files and Format — 15 points

| Score | Condition |
|-------|-----------|
| 15 | All 5 required files present; JSON valid and follows schema; `task-id.txt` contains exactly `task-001`; `UNAVAILABLE` used correctly |
| 10 | All files present but one format issue |
| 5 | Missing 1 required file |
| 0 | Missing 2+ files or invalid structure |

## Valid Answer Variations

The following are NOT considered errors:
- Different wording for actions (as long as the three categories are covered)
- Alternative ordering of recommended actions
- Different prose style in executive summary
- Slightly different area grouping presentation

## Scoring Evidence

Score ONLY: `task-id.txt`, `final-answer.md`, `decision-log.md`, `run-metadata.json`, `artifacts/triage-summary.json`.
