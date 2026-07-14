# Change Summary — Task 004

## Bug 1: Support Record ID Mapping (Wrong Field)

- **Failed test:** `test_id_mapping` — ACC-1500 (DataVault Systems) should match support ticket ST-5004 via `customer_ref`, but matching against `company_name` returned no match.
- **Root cause:** `src/mapper.py` line 55: `match_crm_to_support` compared `ticket['customer_ref']` against `crm_account['company_name']` instead of `crm_account['account_id']`. The README specifies that CRM `account_id` (e.g. ACC-1500) maps to Support `customer_ref` via exact match, not company name.
- **Fix:** Changed `crm_account['company_name']` to `crm_account['account_id']` on line 55 of `src/mapper.py`. The support ticket ST-5004 has `customer_ref == 'ACC-1500'`, which now correctly matches CRM account ACC-1500.

## Bug 2: Amount Comparison (String Comparison)

- **Failed test:** `test_amount_comparison` — ACC-1006 (SkyBridge) has CRM revenue 5000 and Billing charge 5000.00. String comparison produced "5000" != "5000.0", falsely flagging a mismatch.
- **Root cause:** Two locations needed fixing:
  1. `src/mapper.py` line 85: `billing_amount` was stored as the raw JSON value (float `5000.0`) while `crm_amount` was normalized to `int(5000)`. This caused string representations to differ.
  2. `src/reconcile.py` line 43: Amount comparison used `str()` comparison instead of numeric comparison, which would have continued to produce false mismatches for any future float/int pairings.
- **Fix:**
  1. In `src/mapper.py` line 85: Changed `bill['current_month_charges']` to `int(float(bill['current_month_charges']))` to normalize billing amounts to integers, matching the CRM amount normalization.
  2. In `src/reconcile.py` line 43: Changed `str(rec['crm_amount']) != str(rec['billing_amount'])` to `float(rec['crm_amount']) != float(rec['billing_amount'])` for robust numeric comparison.

## Bug 3: Missing Value Handling (Null Status Crash)

- **Failed test:** `test_missing_value_handling` — ACC-1005 (NorthWind Energy) has an empty `account_status` field, which the mapper stores as `None`. Calling `.lower()` on `None` raises `AttributeError`, crashing the reconciliation.
- **Root cause:** `src/reconcile.py` line 23: `crm_normalized = crm_status.lower()` had no guard for `None` values. The mapper correctly stores `None` for empty status fields (line 80 of `src/mapper.py`), but the reconcile function did not handle this case.
- **Fix:** Changed line 23 from `crm_normalized = crm_status.lower()` to `crm_normalized = crm_status.lower() if crm_status else None`. This mirrors the existing guard on line 24 for `billing_status`.
