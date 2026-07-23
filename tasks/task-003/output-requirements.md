# Output Requirements — Task 003

Create these files in your answer directory under `<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/`:

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root.

```text
answer/task-id.txt
answer/final-answer.md
answer/decision-log.md
answer/run-metadata.json
answer/artifacts/approval-decision.json
```

## `answer/task-id.txt`
Must contain exactly: `task-003`

## `answer/final-answer.md`
Must include:

### Executive Summary
One paragraph summarizing the overall decision outcome across all requests.

### Per-Request Decision Report
For each request, list: Request ID, type, applicable policies, decision (APPROVE / HOLD / REJECT / ESCALATE), satisfied conditions, unmet conditions, applicable exceptions with scope, reason, and required next action.

## `answer/decision-log.md`
Contains concise source citations, decisions, verification steps, and declared recovery actions. Must not request or contain hidden chain of thought.

## `answer/artifacts/approval-decision.json`
Must be valid JSON conforming to this schema:

```json
{
  "task_id": "task-003",
  "decisions": [
    {
      "request_id": "TRV-2025-042",
      "decision": "APPROVE",
      "applicable_policies": ["POL-TRV-001"],
      "satisfied_conditions": ["VP approval obtained", "Budget within limit"],
      "unmet_conditions": [],
      "applicable_exceptions": [],
      "exception_scope": "",
      "reason": "All required conditions are satisfied including VP approval.",
      "required_next_action": ""
    }
  ]
}
```

Each decision entry MUST have all 10 fields. The `decision` field must be one of: `APPROVE`, `HOLD`, `REJECT`, `ESCALATE`.

Use `exception_scope` to describe the exact boundary of any exception that applies. Use `required_next_action` for HOLD and ESCALATE decisions to specify what must happen next.

## `answer/run-metadata.json`
Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
