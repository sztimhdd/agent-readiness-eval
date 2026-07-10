# Output Requirements — Task 004

Create: `task-id.txt`, `final-answer.md`, `run-metadata.json`, `artifacts/reconciliation-report.json`

## `task-id.txt`
Exactly: `task-004`

## `final-answer.md`
Must include: Executive Summary, Methodology (which files read first, how mapping was used), Discrepancy Report (per account with system identifiers, discrepancies, values), Summary Table (discrepancy counts by type).

## `artifacts/reconciliation-report.json`
```json
{
  "task_id": "task-004",
  "total_accounts_reviewed": 0,
  "discrepancy_count": 0,
  "discrepancies_by_type": { "amount_mismatch": 0, "status_mismatch": 0, "missing_record": 0 },
  "findings": []
}
```
Each finding: `{ "account_identifiers": { "crm", "billing", "support" }, "discrepancy_type", "description", "crm_value", "billing_value" }`.

## `run-metadata.json`
Copy from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
