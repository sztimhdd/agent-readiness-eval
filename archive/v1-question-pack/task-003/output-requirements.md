# Output Requirements — Task 003

Create these files in your answer directory:

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/compliance-report.json
```

## `task-id.txt`
Must contain exactly: `task-003`

## `final-answer.md`
Must include:

### Executive Summary
One paragraph summarizing overall compliance status across all requests.

### Per-Request Compliance Report
For each request form, list: Request ID, type, applicable policies, compliance status ("Compliant", "Non-Compliant", or "Compliant (Exemption Applied)"), non-compliant items with policy clause references, and exemption details where applied.

### Summary Table
A table listing all non-compliant items ranked by risk severity (highest first).

## `artifacts/compliance-report.json`
Must be valid JSON:
```json
{
  "task_id": "task-003",
  "requests": [],
  "total_requests": 0,
  "compliant_count": 0,
  "non_compliant_count": 0,
  "exemption_applied_count": 0,
  "findings": []
}
```
Each `requests` entry: `{ "request_id", "type", "compliance_status", "applicable_policies", "findings": [] }`.
Each finding: `{ "policy_ref", "description", "severity", "exemption_applied", "exemption_clause" }`.

## `run-metadata.json`
Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
