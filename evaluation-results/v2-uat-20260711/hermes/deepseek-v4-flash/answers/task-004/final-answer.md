# Task 004: Coding & Repair — UAT Answer (v2.0.0)

## Executive Summary

The data reconciliation project maps CRM accounts to Billing records (last-4-digit rule) and Support tickets (account_id match), then cross-references amounts and statuses. Three injected bugs were identified and fixed: (1) support ticket matching used company_name instead of account_id, (2) amount comparison used string comparison causing type-mismatch false positives, and (3) null CRM status caused a crash on `.lower()`. After repair, all 5 tests pass and the reconciliation report is generated with 3 discrepancies found.

## Bug Report

| # | Test | Symptom | Root Cause | Fix |
|---|------|---------|-----------|-----|
| 1 | test_id_mapping | ACC-1500 not matched to ST-5004 | mapper.py line 55 compared customer_ref against company_name instead of account_id | Changed to match on account_id |
| 2 | test_amount_comparison | 5000 != 5000.0 false mismatch | mapper stored int vs float; reconcile compared as strings | Standardized to float in mapper; numeric comparison in reconcile |
| 3 | test_missing_value_handling | AttributeError on None.lower() | reconcile.py line 23 called .lower() unconditionally on nullable crm_status | Added `if crm_status` guard |

## Test Results

**Before repair:** 3 non-passing (2 FAIL, 1 ERROR) — confirmed in `artifacts/test-before.txt`
**After repair:** 5/5 passing — confirmed in `artifacts/test-after.txt`

```
test_amount_comparison ... ok
test_id_mapping ... ok
test_missing_value_handling ... ok
test_reconcile_matching_records ... ok
test_report_generation ... ok
```

## Reconciliation Summary

- **Total accounts reviewed:** 6
- **Total discrepancies found:** 3
- **By type:**
  - `missing_support_record`: 2 (ACC-1003 GlobalTrade Ltd., ACC-1006 SkyBridge Corp.)
  - `amount_mismatch`: 1 (ACC-1500 DataVault Systems — CRM 78,000 vs Billing 65,000)
  - `status_mismatch`: 0
