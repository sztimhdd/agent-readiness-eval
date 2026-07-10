# Task 004 — Reference Analysis (Evaluator Only)

## Expected Discrepancies (2 total)

### 1. DataVault Systems — Amount Mismatch
- CRM monthly_revenue: 78,000
- Billing current_month_charges: 65,000
- Discrepancy: 13,000 CNY. Severity: High.

### 2. GlobalTrade Ltd. — Missing Support Record
- CRM account_status: "suspended"
- Billing status: "delinquent" — mapping says these ARE consistent (suspended↔delinquent)
- Support: No ticket for ACC-1003 (customer_ref field) → Missing Record
- Severity: Medium

## Expected Non-Issues
- Pilot Bank A: clean match (45,000 both sides, active/current, support ticket exists)
- TechStart amount match: 12,000 both sides
- TechStart status: active/current = consistent per mapping
- Billing outstanding_balance has no CRM equivalent — informational only (per field-mapping notes)
- Support gaps are expected where noted in mapping — not discrepancies unless a record should exist
