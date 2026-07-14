# Change Summary — Task 004

## Bug 1: Support matching uses wrong field

- **Test failed**: `test_id_mapping` — ACC-1500 failed to match support ticket ST-5004
- **Root cause**: `src/mapper.py` line 55 — `match_crm_to_support()` compared `ticket['customer_ref'] == crm_account['company_name']` instead of `ticket['customer_ref'] == crm_account['account_id']`
- **Fix applied**: Changed `crm_account['company_name']` to `crm_account['account_id']`. The README specifies "CRM → Support: Match by account_id (ACC-NNNN) ↔ customer_ref (exact match)". The support.csv has `customer_ref` values like "ACC-1500" which correspond to CRM `account_id`, not `company_name`.

## Bug 2: Amount comparison uses string equality

- **Test failed**: `test_amount_comparison` — ACC-1006 (SkyBridge) CRM monthly_revenue=5000 vs Billing current_month_charges=5000.00 produced string mismatch "5000" != "5000.0"
- **Root cause**: `src/reconcile.py` line 43 — `str(rec['crm_amount']) != str(rec['billing_amount'])` compared amounts as strings. Since mapper returned crm_amount as `int` (5000) and billing_amount as `float` from JSON (5000.0), `str()` gave different representations for the same numeric value.
- **Fix applied**: Two changes:
  1. `src/mapper.py` line 81 — changed `int(acct['monthly_revenue'])` to `float(acct['monthly_revenue'])` to ensure consistent numeric type across CRM and Billing amounts.
  2. `src/reconcile.py` line 43 — changed `str()` comparison to `float()` comparison: `float(rec['crm_amount']) != float(rec['billing_amount'])`. Numerically equivalent values (e.g., 5000 and 5000.00) are now correctly treated as equal.

## Bug 3: Null CRM status causes AttributeError

- **Test failed**: `test_missing_value_handling` — ACC-1005 (NorthWind Energy) has empty `account_status`, causing `AttributeError: 'NoneType' object has no attribute 'lower'`
- **Root cause**: `src/reconcile.py` line 23 — `crm_normalized = crm_status.lower()` assumed `crm_status` was always a string. The mapper correctly sets `crm_status = None` when `account_status` is empty (line 80), but reconcile.py did not guard against None.
- **Fix applied**: Changed `crm_normalized = crm_status.lower()` to `crm_normalized = crm_status.lower() if crm_status else None`. The existing guard `if crm_normalized and billing_normalized:` already skips the status comparison block when either is None, so no additional changes were needed downstream.
