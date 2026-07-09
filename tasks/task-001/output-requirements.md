# Output Requirements

Create these files in your answer directory:

```text
final-answer.md
artifacts/triage-summary.json
run-metadata.json
task-id.txt
```

## `task-id.txt`

Must contain exactly:

```text
task-001
```

## `final-answer.md`

Must include:

- A one-paragraph executive summary.
- Counts by severity.
- Counts by product area.
- Top operational risk and the ticket IDs that support it.
- Three recommended next actions.

## `artifacts/triage-summary.json`

Must be JSON with this shape:

```json
{
  "task_id": "task-001",
  "severity_counts": {},
  "area_counts": {},
  "top_risk": "",
  "supporting_ticket_ids": [],
  "recommended_actions": []
}
```

## `run-metadata.json`

Copy the fields from `templates/run-metadata.json`. Use `UNAVAILABLE` when the harness cannot observe a value. Do not estimate token counts.
