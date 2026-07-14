# Task 004: Coding & Repair — Data Reconciliation Project

## Executive Summary

The reconciliation project maps CRM accounts to Billing and Support systems across three data sources (CRM CSV, Billing JSON, Support CSV) and identifies discrepancies. Three injected bugs were diagnosed and repaired: (1) support records were matched by company name instead of account ID, (2) amounts were compared as strings causing false mismatches for numerically identical values, and (3) null CRM status values caused an AttributeError crash during normalization. All three bugs are now fixed, and all 5 tests pass (`python3 -m unittest discover -s tests -v` shows 5/5 OK).

## Bug Report

### Bug 1: Support ID Mapping Uses Wrong Field
- **Symptom:** `test_id_mapping` failed — ACC-1500 returned no support ticket match.
- **Root Cause:** `src/mapper.py:55` — `match_crm_to_support()` compared `ticket['customer_ref']` to `crm_account['company_name']` instead of `crm_account['account_id']`.
- **Fix:** Changed line 55 to compare against `crm_account['account_id']`. ST-5004's `customer_ref` is `'ACC-1500'`, matching the CRM `account_id` exactly.

### Bug 2: Amount Comparison Uses String Equality
- **Symptom:** `test_amount_comparison` failed — ACC-1006 (SkyBridge) with CRM 5000 and Billing 5000.00 flagged as mismatch (`"5000" != "5000.0"`).
- **Root Cause:** Two-fold: (a) `src/mapper.py:85` passed raw JSON float through without normalization; (b) `src/reconcile.py:43` used `str()` comparison.
- **Fix:** (a) Normalize `billing_amount` in mapper via `int(float(...))`; (b) Compare numerically via `float()` in reconcile.

### Bug 3: Null CRM Status Crashes Reconciliation
- **Symptom:** `test_missing_value_handling` errored — `AttributeError: 'NoneType' object has no attribute 'lower'` on ACC-1005.
- **Root Cause:** `src/reconcile.py:23` — `crm_normalized = crm_status.lower()` had no None guard.
- **Fix:** Added `if crm_status else None` guard, matching the existing billing_status guard on line 24.

## Test Results

After repair, `python3 -m unittest discover -s tests -v` produces:

```
test_amount_comparison ... ok
test_id_mapping ... ok
test_missing_value_handling ... ok
test_reconcile_matching_records ... ok
test_report_generation ... ok

Ran 5 tests in 0.001s — OK
```

## Reconciliation Summary

The repaired reconciliation identified **3 discrepancies** across 6 accounts:

| Account | Discrepancy | Details |
|---------|------------|---------|
| ACC-1003 | missing_support_record | No support ticket found |
| ACC-1500 | amount_mismatch | CRM: 78,000 CNY vs Billing: 65,000 CNY |
| ACC-1006 | missing_support_record | No support ticket found |

By type: 2 missing support records, 1 amount mismatch.
