# Change Summary — Task 004

## Bug 1: Wrong field in support matching

- **Failing test:** `test_id_mapping`
- **Root cause:** `src/mapper.py:55` — `match_crm_to_support()` compared `ticket['customer_ref']` against `crm_account['company_name']` instead of `crm_account['account_id']`.
- **Fix:** Changed `crm_account['company_name']` to `crm_account['account_id']` on line 55.

## Bug 2: Type mismatch in amount comparison

- **Failing test:** `test_amount_comparison`
- **Root cause:** `src/mapper.py:81` — `crm_amount` stored as `int()` while billing amounts are floats from JSON. `str(5000)` produces "5000" but `str(5000.0)` produces "5000.0".
- **Fix:** Changed `int(acct['monthly_revenue'])` to `float(acct['monthly_revenue'])` on line 81. Also changed `src/reconcile.py:43` from string comparison `str()` to numeric `float()` comparison for robustness.

## Bug 3: Null status crash in reconciliation

- **Failing test:** `test_missing_value_handling` (Error: AttributeError)
- **Root cause:** `src/reconcile.py:23` — `crm_status.lower()` called unconditionally. NorthWind Energy (ACC-1005) has empty `account_status` → mapper stores `crm_status` as `None` → `.lower()` raises AttributeError.
- **Fix:** Changed `crm_status.lower()` to `crm_status.lower() if crm_status else None` on line 23.
