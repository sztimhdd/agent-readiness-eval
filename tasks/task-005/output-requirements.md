# Output Requirements — Task 005

Create: `task-id.txt`, `final-answer.md`, `run-metadata.json`, `artifacts/resolution-analysis.json`

## `task-id.txt`
Exactly: `task-005`

## `final-answer.md`
Include: Executive Summary, Conflict Register (conflicting requirement IDs, nature, resolution, charter clause cited with rule number, deprioritized requirement), Unified Requirements, Prioritized Action Plan (3-5 actions ranked).

## `artifacts/resolution-analysis.json`
```json
{
  "task_id": "task-005",
  "total_conflicts_identified": 0,
  "conflicts": [],
  "unified_requirements": [],
  "escalated_to_cto": [],
  "action_plan": []
}
```
Each conflict: `{ "id", "topic", "product_requirement", "security_requirement", "nature", "resolution", "charter_clause", "deprioritized" }`.

## `run-metadata.json`
Copy from `templates/run-metadata.json`. Use `UNAVAILABLE`.
