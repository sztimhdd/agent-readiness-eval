# Task 002 — Manual Scoring Rubric

## Total Score: 100 points

### 1. Key Facts Extraction Correctness — 25 points

| Score | Condition |
|-------|-----------|
| 25 | All of the following are correctly stated: deploy v2.3.1 at 09:15, first alert at 09:28, hotfix at 11:30, alert cleared at 11:32, 8+ Pilot Bank A reports affected |
| 20 | One key fact missing or incorrect |
| 15 | Two key facts missing or incorrect |
| 10 | Three key facts missing or incorrect, OR dates/times confused |
| 5 | Major time gaps or only captures 1-2 facts |
| 0 | Completely wrong timeline |

**Partial credit**: If the agent gets the broad shape right (deployment caused the issue, hotfix resolved it) but gets specific timestamps slightly wrong, deduct max 5 points.

### 2. Multi-File Cross-Referencing — 20 points

| Score | Condition |
|-------|-----------|
| 20 | Correctly identifies all 4 relevant files (tickets, deployment-log, metrics, customer-email) AND the distractor section in team-notes; demonstrates cross-file connections (e.g., ticket time matches metrics spike matches deployment time) |
| 15 | Identifies 3 relevant files correctly; shows some cross-referencing |
| 10 | Identifies 2-3 relevant files; limited cross-referencing |
| 5 | Only references 1 file, or misses the deployment-log as the key piece |
| 0 | Uses wrong files or fails to connect any sources |

**Important**: Including the "Dashboard UI" section of team-notes as evidence for the incident root cause is a **serious error** and should receive max 10 points in this category.

### 3. Root Cause / Highest Risk Judgment — 20 points

| Score | Condition |
|-------|-----------|
| 20 | Correctly identifies the race condition in async completion reporting (v2.3.1) as the root cause, with specific evidence chain |
| 15 | Points to the deployment but describes the mechanism vaguely (e.g., "the deployment caused it" without explaining the race condition) |
| 10 | Identifies a secondary factor (e.g., "write latency") as the root cause while mentioning deployment as a factor |
| 5 | Wrong root cause (e.g., blames the dashboard, storage backend, or the distractor project) |
| 0 | No root cause identified, or blames an external factor not evident from the provided files |

**Acceptable root cause phrasings** (synonyms of the same root cause):
- "Async completion reporting race condition introduced in v2.3.1"
- "Status transition logic change in v2.3.1 — task reports complete before write confirms"
- "Race condition: task status set to completed before output artifact write acknowledgement"

### 4. Evidence Reference Accuracy — 15 points

| Score | Condition |
|-------|-----------|
| 15 | All evidence references are accurate: correct file names, correct ticket IDs (T-2001 through T-2004), correct metric names, correct deployment versions |
| 12 | One reference error (e.g., wrong ticket ID, wrong metric) |
| 9 | Two reference errors |
| 5 | Multiple reference errors, or cites non-existent records |
| 0 | No specific evidence references, or fabricated records |

### 5. Action Recommendations Specificity — 10 points

| Score | Condition |
|-------|-----------|
| 10 | Three concrete, prioritized actions with justifications. Example good actions: (1) "Add write-acknowledgement check before status transition in agent-runtime — prevents recurrence," (2) "Update smoke tests to verify artifact completeness after task completion — catches regression at deploy time," (3) "Notify Pilot Bank A with incident timeline and SLA impact assessment — addresses the active escalation." |
| 7 | Three actions but one is vague or unjustified |
| 5 | Two actions, or actions are generic ("fix the bug," "improve testing") |
| 3 | One action, or actions are not actionable |
| 0 | No actions recommended |

### 6. Required Output Files and Format — 10 points

| Score | Condition |
|-------|-----------|
| 10 | All 4 required files present; JSON is valid and follows schema; `task-id.txt` contains exactly `task-002`; `UNAVAILABLE` used correctly for unobservable metadata |
| 7 | All files present but one format issue (missing field, invalid JSON, wrong task ID) |
| 5 | Missing 1 required file, or multiple format issues |
| 3 | Missing 2 required files, or JSON is invalid |
| 0 | Missing 3+ files, or no answer directory structure |

## Deductions for Serious Issues

These are applied on top of the per-category score:

| Issue | Deduction |
|-------|-----------|
| Including the Dashboard UI section as incident root cause evidence | −15 points (treat as scoring category 2 failure) |
| Citing non-existent ticket IDs or records | −10 points |
| Presenting inferences as confirmed facts without caveat | −10 points |
| Missing required answer file | −10 points each |
| Fabricated token counts or timing | −20 points (automatic, per SKILL.md Rule 4) |
| Agent modifies `inputs/` directory | −20 points |

## Determining Overall Score

| Total | Grade | Interpretation |
|-------|-------|----------------|
| 90-100 | Excellent | Thorough investigation, correct root cause, strong evidence |
| 70-89 | Good | Solid analysis with minor gaps or imprecision |
| 50-69 | Fair | Partial analysis, missing key connections |
| 30-49 | Poor | Major gaps in investigation or wrong conclusions |
| 0-29 | Failing | Fundamental misunderstanding or rule violations |

## Valid Answer Variations

The following are NOT considered errors:
- Different wording for the same root cause description
- Alternative ordering of the three recommended actions (as long as all three are sensible)
- Including an additional minor "unknown" not listed in the reference analysis
- Slightly different timeline formatting (time format, grouping style)
- Writing style differences (formal vs. concise) — **do not deduct for tone**

## Scoring Evidence

Score ONLY the following files from the answer directory:
- `task-id.txt`
- `final-answer.md`
- `run-metadata.json`
- `artifacts/investigation-summary.json`

Do not score hidden chain-of-thought, intermediate notes, or self-evaluations the agent may leave in the answer directory.
