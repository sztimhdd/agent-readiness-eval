# Cross-System Field Mapping

## CRM → Billing

| CRM Field | Billing Field | Match Type |
|-----------|---------------|------------|
| `account_id` (ACC-NNNN) | `billing_account` (BA-XXX-NNNN) | Partial: last 4 digits of billing_account match CRM account_id digits |
| `company_name` | `customer_name` | Exact text match |
| `account_status` | `status` | Value mapping: active↔current, suspended↔delinquent |
| `monthly_revenue` | `current_month_charges` | Direct numeric comparison |

## CRM → Support

| CRM Field | Support Field | Match Type |
|-----------|---------------|------------|
| `account_id` | `customer_ref` | Exact match |

## Notes
- Billing `outstanding_balance` has no CRM equivalent — for information only.
- Support system may have gaps (not all CRM accounts have support tickets).
- Billing `payment_method` has no CRM equivalent — for information only.
