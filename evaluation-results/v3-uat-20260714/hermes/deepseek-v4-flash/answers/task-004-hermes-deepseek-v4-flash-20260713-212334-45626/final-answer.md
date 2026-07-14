# Task 004 Final Answer

## Executive Summary

The Data Reconciliation Project maps CRM accounts to Billing records (via last-4-digit match) and Support tickets (via account_id match), then compares statuses and amounts to detect discrepancies. Three injected bugs caused 2 test failures and 1 error. All fixes were applied to `src/` only. After repair, all 5 tests pass and the reconciliation report was generated successfully.

## Bug Report

### Bug 1: Wrong field in support matching

**Symptom:** `test_id_mapping` failed — ACC-1500 (DataVault Systems) returned no support ticket match despite ST-5004 having `customer_ref = "ACC-1500"`.

**Root cause:** `src/mapper.py:55` — `match_crm_to_support()` compared `ticket['customer_ref']` against `crm_account['company_name']` ("DataVault Systems") instead of `crm_account['account_id']` ("ACC-1500").

**Fix:** Changed comparison to `ticket['customer_ref'] == crm_account['account_id']`.

### Bug 2: Type mismatch in amount comparison

**Symptom:** `test_amount_comparison` failed — SkyBridge (ACC-1006) CRM amount 5000 (int) vs Billing amount 5000.00 (float) produced different string representations.

**Root cause:** `src/mapper.py:81` — `crm_amount` was stored as `int()` while billing amounts are floats loaded from JSON. `str(5000) == "5000"` but `str(5000.0) == "5000.0"`.

**Fix:** Changed `int(acct['monthly_revenue'])` to `float(acct['monthly_revenue'])` so both amounts share the same type. Also changed the comparison in `src/reconcile.py:43` from string to numeric comparison using `float()`.

### Bug 3: Null status crash in reconciliation

**Symptom:** `test_missing_value_handling` errored — calling `reconcile()` raised `AttributeError: 'NoneType' object has no attribute 'lower'`.

**Root cause:** `src/reconcile.py:23` — `crm_status.lower()` was called unconditionally, but NorthWind Energy (ACC-1005) has an empty `account_status`, which `mapper.py` stores as `None`.

**Fix:** Changed to `crm_status.lower() if crm_status else None`.

## Test Results

After repair:
```
test_amount_comparison ............. ok
test_id_mapping ................... ok
test_missing_value_handling ....... ok
test_reconcile_matching_records ... ok
test_report_generation ............ ok
----------------------------------------------------------------------
Ran 5 tests in 0.001s
OK
```

## Reconciliation Summary

Total accounts reviewed: 6
Discrepancies found: 3

| Type | Count | Details |
|------|-------|---------|
| missing_support_record | 2 | ACC-1003 (GlobalTrade Ltd.), ACC-1006 (SkyBridge Corp.) have no support ticket |
| amount_mismatch | 1 | ACC-1500 (DataVault Systems): CRM=78000.0 vs Billing=65000.0 |
