# Output Requirements — Task 006

Create: `task-id.txt`, `final-answer.md`, `run-metadata.json`, `artifacts/executive-brief.json`

## `task-id.txt`
Exactly: `task-006`

## `final-answer.md`
Must include: Executive Summary, Key Trends (3-5 trends with source citations), Data Consistency Check (explicitly flag contradictory claims with source + value references), Risks (ranked), Recommended Actions (3 prioritized, each with data source + expected impact + caveats).

## `artifacts/executive-brief.json`
```json
{
  "task_id": "task-006",
  "period": "Q4 2025",
  "total_sources_reviewed": 0,
  "key_trends": [],
  "data_inconsistencies": [],
  "top_risks": [],
  "recommended_actions": []
}
```
Each inconsistency: `{ "source_a", "source_b", "claim", "conflict", "severity" }`.

## `run-metadata.json`
Copy from `templates/run-metadata.json`. Use `UNAVAILABLE`.
