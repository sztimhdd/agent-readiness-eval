# Output Requirements

Create these files in your answer directory under `<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/`:

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root.

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/investigation-summary.json
```

## `task-id.txt`

Must contain exactly:

```text
task-002
```

## `final-answer.md`

Must include the following sections:

### Executive Summary
One paragraph describing what happened, when, and the impact.

### Incident Timeline
A chronological list of key events with timestamps and source file references. Include at least: first symptom, escalation, deployment events, and resolution.

### Root Cause Analysis
- Most likely root cause with reasoning
- Supporting evidence: which files and specific records support this conclusion
- Why the issue was not caught earlier

### Confirmed Facts
Bullet list of facts that are supported by multiple independent sources.

### Inferences
Bullet list of conclusions that are logically derived but not explicitly stated in any single file.

### Unknowns
Bullet list of information gaps — things the available files do not cover, or where sources conflict without resolution.

### Recommended Actions
Three prioritized actions the team should take, ordered by urgency. Each action must include a brief justification.

### Confidence & Information Gaps

A brief section that must include:

- A list of specific information gaps — data or logs that are not present in the provided files but would strengthen the analysis.
- An overall confidence estimate for the root cause conclusion, expressed as a qualitative level (High / Medium / Low) with a brief justification. Example: "Confidence: Medium. The timing correlation between v2.3.1 deployment and the error spike is strong, but we are missing auth-service write logs that would confirm the exact failure path."

## `artifacts/investigation-summary.json`

Must be valid JSON with this shape:

```json
{
  "task_id": "task-002",
  "incident_id": "INC-2025-0612",
  "relevant_sources": [],
  "timeline": [],
  "confirmed_facts": [],
  "likely_root_cause": "",
  "supporting_evidence": [],
  "inferences": [],
  "unknowns": [],
  "recommended_actions": []
}
```

Field guidance:

| Field | Type | Description |
|-------|------|-------------|
| `relevant_sources` | array of strings | File paths that contain evidence relevant to the incident. Exclude unrelated files. |
| `timeline` | array of objects | Each entry: `{ "time": "HH:MM UTC", "event": "...", "source": "filename" }` |
| `confirmed_facts` | array of strings | Facts supported by ≥2 independent sources |
| `likely_root_cause` | string | Single sentence describing the root cause |
| `supporting_evidence` | array of strings | Specific evidence entries (file + record ID or line reference) |
| `inferences` | array of strings | Logical conclusions not explicitly stated |
| `unknowns` | array of strings | Information gaps or unresolved conflicts |
| `recommended_actions` | array of strings | Three prioritized actions |
| `confidence_level` | string | One of "High", "Medium", "Low" |
| `information_gaps` | array of strings | Specific data/logs that are missing and would improve the analysis |

## `run-metadata.json`

Copy the fields from `templates/run-metadata.json`. Use `UNAVAILABLE` when the harness cannot observe a value. Do not estimate token counts.
