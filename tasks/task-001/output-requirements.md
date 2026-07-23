# Output Requirements

Create these files in your answer directory under `<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/answer/`:

```text
answer/
├── task-id.txt
├── final-answer.md
├── decision-log.md
├── artifacts/
│   └── triage-summary.json
└── run-metadata.json
```

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root.

## `task-id.txt`

Must contain exactly:

```text
task-001
```

## `final-answer.md`

Must include:

- A one-paragraph executive summary.
- Counts by severity (use the latest severity from `ticket-update-log.md` where applicable).
- Counts by product area.
- Top operational risk and the ticket IDs that support it.
- Three recommended next actions.

## `decision-log.md`

Must document key decisions made during triage, including:

- Which sources were consulted and their relative authority (source-authority resolution).
- Which stale severity labels were identified and what corrected severity was applied.
- How resolution notes in `ticket-update-log.md` affected the severity assessment.
- Verification steps taken before committing to a conclusion (e.g., cross-referencing ticket IDs between data.json and the update log).

## `artifacts/triage-summary.json`

Must be JSON with this shape:

```json
{
  "task_id": "task-001",
  "severity_counts": {},
  "area_counts": {},
  "top_risk": "",
  "supporting_ticket_ids": [],
  "recommended_actions": [],
  "source_precedence_followed": true,
  "stale_labels_identified": [],
  "resolution_referenced": []
}
```

Fields:

| Field | Type | Description |
|-------|------|-------------|
| `severity_counts` | object | Count of tickets per severity level, after applying update-log reclassifications |
| `area_counts` | object | Count of tickets per product area |
| `top_risk` | string | Brief description of the top operational risk |
| `supporting_ticket_ids` | array of strings | Ticket IDs that support the top risk assessment |
| `recommended_actions` | array of strings | Three recommended next actions |
| `source_precedence_followed` | boolean | `true` if source-authority precedence was applied per `severity-policy.md` |
| `stale_labels_identified` | array of objects | Each object: `{"ticket_id": "T-1007", "original_severity": "critical", "corrected_severity": "medium", "update_date": "2026-07-15"}` |
| `resolution_referenced` | array of strings | Ticket IDs for which resolution notes from the update log were consulted |

## `run-metadata.json`

Copy the fields from `templates/run-metadata.json`. Use `UNAVAILABLE` when the harness cannot observe a value. Do not estimate token counts.
