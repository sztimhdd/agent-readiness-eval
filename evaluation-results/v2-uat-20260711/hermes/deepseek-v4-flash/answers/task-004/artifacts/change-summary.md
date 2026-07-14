# Change Summary — Task 004

## Bug 1: Support ticket matching uses wrong field

**Failed test:** `test_id_mapping`
**Symptom:** DataVault Systems (ACC-1500) should match support ticket ST-5004 (customer_ref = 'ACC-1500'), but `match_crm_to_support()` returned `None`.

**Root cause:** `src/mapper.py`, line 55 — the matching logic compares `ticket['customer_ref'] == crm_account['company_name']`. ACC-1500's company_name is "DataVault Systems", which does not equal the customer_ref "ACC-1500". The correct match rule (per README.md) is CRM account_id == Support customer_ref (exact match).

**Fix:** Changed the comparison to `ticket['customer_ref'] == crm_account['account_id']` so that CSV account_id values ("ACC-1500") match support CSV customer_ref values ("ACC-1500").

---

## Bug 2: Amount comparison uses string comparison

**Failed test:** `test_amount_comparison`
**Symptom:** SkyBridge Corp (ACC-1006) CRM monthly_revenue = 5000 (int), Billing = 5000.00 (float). String comparison "5000" != "5000.0" falsely flags as a mismatch.

**Root cause (two parts):**
1. `src/mapper.py`, line 81 — `'crm_amount': int(acct['monthly_revenue'])` stores CRM amounts as `int`, while billing amounts remain `float` from JSON (`5000.00`).
2. `src/reconcile.py`, line 43 — `str(rec['crm_amount']) != str(rec['billing_amount'])` uses string comparison, so "5000" != "5000.0".

**Fixes:**
- `src/mapper.py`: Changed `int()` to `float()` so CRM amounts match the float type used by billing records.
- `src/reconcile.py`: Changed `str() != str()` to `float() != float()` for numeric comparison.

---

## Bug 3: Null CRM status causes AttributeError on .lower()

**Failed test:** `test_missing_value_handling`
**Symptom:** `reconcile()` crashes with `AttributeError: 'NoneType' object has no attribute 'lower'` when processing NorthWind Energy (ACC-1005).

**Root cause:** `src/reconcile.py`, line 23 — `crm_normalized = crm_status.lower()` is called unconditionally on `crm_status`, but `crm_status` can be `None` when the CRM account has an empty `account_status` field. The mapper (`src/mapper.py`, line 80) converts empty status to `None` via `acct['account_status'].strip() if acct['account_status'].strip() else None`.

**Fix:** Changed to `crm_normalized = crm_status.lower() if crm_status else None`, matching the pattern already used for `billing_normalized` on line 24.
