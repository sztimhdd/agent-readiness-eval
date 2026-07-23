# Task 004 — Reference Analysis (Evaluator Only)

## Overview

The base project contains 3 injected defects in a Python stdlib reconciliation project.
The agent must diagnose and fix all 3 without modifying tests, data files, or `expected-output-format.md`.
Tests are ID-agnostic and pass with both the original data and evaluator replacement data.

## Defect Catalog

### Defect 1 — Cross-module type mismatch: billing_amount returned as string

- **File**: `src/mapper.py`, function `map_all()` — line with `billing_amount`
- **Symptom**: `test_amount_comparison` fails — billing_amount values are strings instead of numeric.
- **Root cause**: The mapping wraps `bill['current_month_charges']` in `str()`, producing string values like `"5000.0"`. Since `crm_amount` remains an integer (e.g. `5000`), reconcile's `str()` comparison on line 43 of `reconcile.py` produces false mismatches: `str(5000)` is `"5000"` but `str("5000.0")` is `"5000.0"`.
- **Expected fix**: Change `str(bill['current_month_charges']) if bill else None` to `float(bill['current_month_charges']) if bill else None`. This makes billing_amount numeric, matching `crm_amount`'s type.
- **Test**: `test_amount_comparison` — asserts billing_amount is not a string. On seed, all 6 records have string billing_amount and the test fails. On repair, billing_amount is float and the test passes.

### Defect 2 — Missing non-positive amount invariant

- **File**: `src/reconcile.py`, `reconcile()` function — after the amount comparison block
- **Symptom**: `test_non_positive_amount_invariant` fails — the reconcile source code does not contain a `non_positive_amount` check.
- **Root cause**: reconcile has no check for accounts where `crm_amount <= 0`. Accounts with zero revenue (e.g. suspended accounts) are silently accepted instead of being flagged.
- **Expected fix**: After the amount comparison block (before the support gap check), add:

```python
# Non-positive amount invariant
if rec['crm_amount'] is not None and rec['crm_amount'] <= 0:
    discrepancies.append({
        'account_id': crm_id,
        'type': 'non_positive_amount',
        'crm_amount': rec['crm_amount'],
    })
```

- **Test**: `test_non_positive_amount_invariant` — inspects the reconcile source code for the string `non_positive_amount`. On seed, the source has no such check and the test fails. On repair, the source includes the invariant check and the test passes.

### Defect 3 — Null CRM status causes AttributeError

- **File**: `src/reconcile.py`, `reconcile()` function — line 23
- **Symptom**: `test_null_status_handling` errors with `AttributeError: 'NoneType' object has no attribute 'lower'`.
- **Root cause**: `crm_status.lower()` is called unconditionally on `rec['crm_status']`, which is `None` for accounts with empty status (e.g. NorthWind Energy/ACC-1005, Epsilon Retail/ACC-2005 in replacement data). There is no null guard before calling `.lower()`.
- **Expected fix**: Change line 23 from `crm_normalized = crm_status.lower()` to `crm_normalized = crm_status.lower() if crm_status else None`.
- **Test**: `test_null_status_handling` — calls `reconcile()` which should complete without crashing. On seed, the call raises AttributeError and the test errors. On repair, the null guard prevents the crash and the test passes.

## Anti-Hardcoding Procedure

When evaluating agent fixes, verify that the agent did NOT:

1. **Modify tests to match broken code.** Changing the test assertion instead of fixing the bug is invalid.
2. **Modify data files** (`data/crm.csv`, `data/billing.json`, `data/support.csv`) to avoid triggering defects.
3. **Hardcode specific account IDs or amounts.** The fix should be general — e.g., proper type conversion in mapper, a general null guard in reconcile, a general invariant check — not a special case for specific accounts.
4. **Delete or skip the failing tests.** All 5 tests must remain and pass.
5. **Remove the str() comparison in reconcile without fixing the mapper.** The defect is cross-module: the mapper returns strings AND reconcile compares as strings. Fixing only reconcile (changing to numeric comparison) without fixing the mapper leaves the root cause intact. The agent must fix both the mapper (return numeric) and reconcile (null guard + non-positive invariant).

To verify, swap the data files with `evaluator-private/replacement-data/` (which has different account IDs, amounts, company names, and null-status accounts) and re-run the tests. A valid fix will pass with the replacement data. A hardcoded fix will fail.

## Replacement Data Validation

After swapping in `evaluator-private/replacement-data/` files:
- `test_reconcile_matching_records`: must still find all 6 billing matches.
- `test_amount_comparison`: billing_amount must be numeric (not string) for all 6 accounts.
- `test_non_positive_amount_invariant`: reconcile source must contain `non_positive_amount` check.
- `test_null_status_handling`: ACC-2005 (null status) must not crash reconcile.
- All 5 tests must pass with replacement data.

## Scoring Notes

- The three defects are interdependent: Defect 3 (null crash) blocks execution of reconcile, which means the agent cannot run `python3 -m src.reconcile` to verify their other fixes until Defect 3 is fixed first. This is intentional — it tests the agent's ability to reason about code without execution feedback.
- Fixing the defect by writing code that works differently from the reference fix is acceptable IF it passes all tests and the replacement data swap.
- Partial fixes receive proportional credit per the rubric.
- An agent that modifies tests/data/expected-output-format.md receives 0 for all corresponding dimensions.
- An agent that fixes only reconcile's comparison (e.g., changing `str()` to `float()`) without fixing the mapper's type bug has not fully resolved the cross-module defect. The type system inconsistency remains. Score accordingly per the rubric.
