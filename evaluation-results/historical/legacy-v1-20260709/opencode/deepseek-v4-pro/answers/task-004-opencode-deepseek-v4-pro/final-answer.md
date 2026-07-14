# Cross-System Data Reconciliation — Task 004

## Executive Summary
Reconciled 4 customer accounts across CRM, Billing, and Support systems. Two discrepancies found: DataVault Systems has a 13,000 CNY amount mismatch between CRM and Billing; GlobalTrade Ltd. has no support ticket record. Pilot Bank A and TechStart Inc. show consistent data across all three systems.

## Methodology
1. Read field-mapping.md first to understand cross-system matching rules (CRM account_id ↔ Billing billing_account via numeric suffix, CRM account_id ↔ Support customer_ref via exact match).
2. Read CRM data, then Billing data. Matched records by company name (exact) and validated via numeric suffix.
3. Cross-checked Support system for each CRM account.
4. Compared CRM monthly_revenue vs Billing current_month_charges; CRM account_status vs Billing status (using value mapping).

## Discrepancy Report

### DataVault Systems — Amount Mismatch
- CRM (ACC-1004): monthly_revenue = 78,000 CNY, status = active
- Billing (BA-DVS-004): current_month_charges = 65,000 CNY, status = current
- Support (ST-5004): onboarding issue, open, low priority
- Discrepancy: CRM monthly_revenue (78,000) ≠ Billing current_month_charges (65,000). Difference: 13,000 CNY. Type: amount_mismatch.

### GlobalTrade Ltd. — Missing Support Record
- CRM (ACC-1003): monthly_revenue = 0, status = suspended
- Billing (BA-GTL-003): current_month_charges = 0, status = delinquent (matches suspended per mapping), outstanding_balance = 18,000 CNY (informational only)
- Support: No ticket with customer_ref = "ACC-1003"
- Discrepancy: No support ticket exists for this account. Type: missing_record.

### Pilot Bank A — No Discrepancy
CRM 45,000 = Billing 45,000; active↔current; Support ST-5001 exists.

### TechStart Inc. — No Discrepancy
CRM 12,000 = Billing 12,000; active↔current; Support ST-5002 exists (billing issue is operational, not data discrepancy). Billing outstanding_balance 3,500 is informational only per field mapping notes.

## Summary Table
| Type | Count |
|------|:-----:|
| Amount Mismatch | 1 |
| Missing Record | 1 |
| **Total** | **2** |
