# Output Requirements — Task 005

Create these files in your answer directory under `<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/`:

Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root.

```text
task-id.txt
final-answer.md
artifacts/final-state.json
artifacts/environment-action-log.jsonl
artifacts/decision-summary.md
run-metadata.json
```

## `task-id.txt`

Must contain exactly:

```text
task-005
```

## `final-answer.md`

Must include:

- **Executive Summary**: One paragraph summarizing your approach and results.
- **Policy Summary**: For each policy, a brief summary of key rules applied.
- **Per-Request Decisions**: For each request (REQ-001 through REQ-006):
  - Request ID, title, submitter, amount
  - Applicable policies identified
  - Decision (approve / request_information / reject / escalate)
  - Rationale with specific policy clause citations
  - Resulting status
- **Evidence Integrity Statement**: Confirm that `final-state.json` and `environment-action-log.jsonl` were exported by the environment (`get_final_state` / `get_action_log`), not fabricated by the agent.

## `artifacts/final-state.json`

**Evaluator-exported.** Obtain by calling `get_final_state` and saving the output verbatim.

```json
{
  "task_id": "task-005",
  "source": "environment_export",
  "export_tool": "get_final_state",
  "final_state": []
}
```

The `final_state` array contains `{"request_id": "...", "status": "..."}` for each request.

## `artifacts/environment-action-log.jsonl`

**Evaluator-exported.** Obtain by calling `get_action_log` and saving the `action_log` array as JSONL (one JSON object per line). Do not modify, filter, or reorder entries.

## `artifacts/decision-summary.md`

Per-request summary table:

| Request | Title | Amount | Decision | Status | Key Rationale | Policy Cited |
|---------|-------|--------|----------|--------|---------------|-------------|
| REQ-001 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |

## `run-metadata.json`

Copy the fields from `templates/run-metadata.json`. Set `profile` to `"controlled_tool"`. Use `UNAVAILABLE` for unobservable fields. Do not estimate tokens, timings, or tool calls.
