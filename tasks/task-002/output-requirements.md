# Output Requirements

Create these files in your answer directory under
`<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/answer/`:

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root.

```text
answer/task-id.txt
answer/final-answer.md
answer/decision-log.md
answer/run-metadata.json
answer/artifacts/investigation-summary.json
```

## `answer/task-id.txt`

Must contain exactly:

```text
task-002
```

## `answer/final-answer.md`

Must include the following sections:

### Executive Summary
One paragraph describing what happened, when, and the impact.

### Incident Timeline
A chronological list of key events with timestamps and source file
references. Include at least: first symptom, escalation, deployment events,
and resolution.

### Root Cause Analysis
- Most likely root cause with reasoning.
- A **causal chain** showing how the initiating event led to the observed
  symptoms, supported by **at least 3 independent sources**.
- Why the issue was not caught earlier.
- How cross-source conflicts (if any) were resolved.

### Confirmed Facts
Bullet list of facts that are supported by multiple independent sources.
For each fact, list which source files corroborate it.

### Inferences
Bullet list of conclusions that are logically derived but not explicitly
stated in any single file.

### Resolved Conflicts
Bullet list of each cross-source conflict identified, how it was resolved,
and which sources were involved. Include the reasoning used to decide which
source's account to accept.

### Distractor Rejection
Bullet list of each distractor file or section identified and why it was
excluded from the investigation.

### Unknowns
Bullet list of information gaps — things the available files do not cover,
or where sources conflict without clear resolution.

### Recommended Actions
Three prioritized actions the team should take, ordered by urgency. Each
action must include a brief justification.

### Confidence & Information Gaps

A brief section that must include:

- A list of specific information gaps — data or logs that are not present
  in the provided files but would strengthen the analysis.
- An overall confidence estimate for the root cause conclusion, expressed
  as a qualitative level (High / Medium / Low) with a brief justification.
  Example: "Confidence: Medium. The timing correlation between v2.3.1
  deployment and the error spike is strong, but we are missing auth-service
  write logs that would confirm the exact failure path."

## `answer/decision-log.md`

Document your reasoning process and key decisions made during the
investigation. This file helps evaluators understand how you arrived at
your conclusions.

Must include at least:

```markdown
# Decision Log

## Source Selection
- Which files were considered relevant and why
- Which files were excluded as distractors and why

## Conflict Resolution
- Each conflict identified between sources
- How each conflict was resolved (or why it remains unresolved)

## Causal Chain Construction
- How the causal links were established
- Which independent sources support each link

## Confidence Assessment
- Factors that increase confidence
- Factors that decrease confidence
- What additional data would resolve remaining uncertainties
```

## `answer/artifacts/investigation-summary.json`

Must be valid JSON with this shape:

```json
{
  "task_id": "task-002",
  "incident_id": "INC-2025-0612",
  "relevant_sources": [],
  "distractor_exclusion": [],
  "resolved_conflicts": [],
  "unresolved_conflicts": [],
  "timeline": [],
  "causal_chain_sources": [],
  "confirmed_facts": [],
  "likely_root_cause": "",
  "supporting_evidence": [],
  "inferences": [],
  "unknowns": [],
  "recommended_actions": [],
  "confidence_level": "",
  "information_gaps": []
}
```

Field guidance:

| Field | Type | Description |
|-------|------|-------------|
| `relevant_sources` | array of strings | File paths that contain evidence relevant to the incident. Exclude unrelated files. |
| `distractor_exclusion` | array of objects | Each entry: `{ "file": "filename", "reason": "why excluded" }` |
| `resolved_conflicts` | array of objects | Each entry: `{ "sources": ["file1", "file2"], "resolution": "how resolved", "reasoning": "why this resolution is correct" }` |
| `unresolved_conflicts` | array of objects | Each entry: `{ "sources": ["file1", "file2"], "issue": "what they disagree on", "gap": "what evidence is missing to resolve" }` |
| `timeline` | array of objects | Each entry: `{ "time": "HH:MM UTC", "event": "...", "source": "filename" }` |
| `causal_chain_sources` | array of strings | File paths of the **3 or more independent sources** that independently corroborate the causal chain. |
| `confirmed_facts` | array of strings | Facts supported by ≥2 independent sources |
| `likely_root_cause` | string | Single sentence describing the root cause |
| `supporting_evidence` | array of strings | Specific evidence entries (file + record ID or line reference) |
| `inferences` | array of strings | Logical conclusions not explicitly stated |
| `unknowns` | array of strings | Information gaps or unresolved conflicts |
| `recommended_actions` | array of strings | Three prioritized actions |
| `confidence_level` | string | One of "High", "Medium", "Low" |
| `information_gaps` | array of strings | Specific data/logs that are missing and would improve the analysis |

## `answer/run-metadata.json`

Copy the fields from `templates/run-metadata.json`. Use `UNAVAILABLE` when
the harness cannot observe a value. Do not estimate token counts.
