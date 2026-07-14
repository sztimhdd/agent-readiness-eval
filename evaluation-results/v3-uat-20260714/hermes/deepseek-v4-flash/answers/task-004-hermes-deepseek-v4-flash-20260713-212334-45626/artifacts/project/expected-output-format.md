# Expected Output Format

The reconciliation report must be a JSON file at `output/reconciliation-report.json`:

```json
{
  "task_id": "task-004",
  "total_accounts_reviewed": <number>,
  "discrepancy_count": <number>,
  "discrepancies_by_type": {
    "amount_mismatch": <number>,
    "status_mismatch": <number>,
    "missing_support_record": <number>
  },
  "findings": [
    {
      "account_id": "<ACC-NNNN>",
      "discrepancy_type": "<amount_mismatch|status_mismatch|missing_support_record>",
      "crm_amount": <number>,
      "billing_amount": <number>
    }
  ]
}
```

Each finding object must include `account_id` and `discrepancy_type`.
Amount-related findings must include `crm_amount` and `billing_amount`.
Status-related findings must include `crm_status` and `billing_status`.
Missing-support findings need only `account_id` and `discrepancy_type`.
