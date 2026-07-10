# Task 004 — Reference Analysis (Evaluator Only)

## Overview

The base project contains 3 injected bugs in a Python stdlib reconciliation project.
The agent must diagnose and fix all 3 without modifying tests, data files, or `expected-output-format.md`.

## Bug Catalog

### Bug 1 — Support matching uses wrong field

- **File**: `src/mapper.py`, function `match_crm_to_support()`
- **Symptom**: `test_id_mapping` fails — support tickets are not found for CRM accounts that should have them.
- **Root cause**: The function matches `ticket['customer_ref']` against `crm_account['company_name']` instead of `crm_account['account_id']`. The correct mapping rule (from README) is CRM `account_id` ↔ Support `customer_ref` (exact match).
- **Expected fix**: Change `crm_account['company_name']` to `crm_account['account_id']` in the comparison expression.
- **Test**: `test_id_mapping` — asserts that ACC-1500 (DataVault Systems) matches support ticket ST-5004 via customer_ref 'ACC-1500'. Before fix the function returns None.

### Bug 2 — Amount comparison uses string equality

- **File**: `src/reconcile.py`, `reconcile()` function — amount comparison block
- **Symptom**: `test_amount_comparison` fails — numerically identical amounts (5000 vs 5000.00) are flagged as discrepancies.
- **Root cause**: Amounts are compared using `str()`: `str(rec['crm_amount']) != str(rec['billing_amount'])`. This produces `"5000" != "5000.0"` for integer 5000 vs float 5000.0.
- **Expected fix**: Compare amounts numerically instead of as strings — change to `float(rec['crm_amount']) != float(rec['billing_amount'])` or equivalent numeric comparison.
- **Test**: `test_amount_comparison` — asserts that string representations of equivalent amounts match, which fails under string comparison.

### Bug 3 — Null status causes AttributeError

- **File**: `src/reconcile.py`, `reconcile()` function — status normalization block
- **Symptom**: `test_missing_value_handling` errors with `AttributeError: 'NoneType' object has no attribute 'lower'`. The test suite aborts on the error.
- **Root cause**: `crm_status.lower()` is called unconditionally on `rec['crm_status']`, which is `None` for accounts with empty status (ACC-1005 NorthWind Energy). There is no null guard before calling `.lower()`.
- **Expected fix**: Add a null check before calling `.lower()` on `crm_status`. The simplest fix: `crm_status.lower() if crm_status else None` instead of bare `crm_status.lower()`.
- **Test**: `test_missing_value_handling` — calls `reconcile()` which should complete without crashing on null status.

## Anti-Hardcoding Procedure

When evaluating agent fixes, the reviewer should verify that the agent did NOT:

1. **Modify tests to match broken code.** Changing the test assertion instead of fixing the bug is invalid.
2. **Modify data files** (`data/crm.csv`, `data/billing.json`, `data/support.csv`) to avoid triggering bugs.
3. **Hardcode specific account IDs or amounts** in reconciliation logic. The fix should be general (e.g., proper string→numeric conversion, proper null guard), not a special case for ACC-1006 or ACC-1005.
4. **Delete or skip the failing tests.** All 5 tests must remain and pass.

To verify, swap the data files with `evaluator-private/replacement-data/` (which has different account IDs, amounts, company names, and null-status accounts) and re-run the tests. A valid fix will pass with the replacement data. A hardcoded fix will fail.

## Replacement Data Validation

After swapping in `evaluator-private/replacement-data/` files:
- `test_reconcile_matching_records`: must still find all 6 billing matches.
- `test_id_mapping`: ACC-2500 must match ST-6004 via customer_ref.
- `test_amount_comparison`: Zeta Services (ACC-2006: CRM 22000, Billing 22000.00) must not produce false mismatch.
- `test_missing_value_handling`: ACC-2005 (null status) must not crash.
- All 5 tests must pass with replacement data.

## Scoring Notes

- Fixing the bug by writing new code that works differently from the intended fix is acceptable IF it passes all tests and the replacement data swap.
- Partial fixes (e.g., fixing bugs 1 and 3 but not 2) receive proportional credit per the rubric.
- An agent that modifies tests/data/expected-output-format.md receives 0 for the corresponding dimension.
