# Task 004: Coding & Repair — Final Answer

## Executive Summary

This task involved diagnosing and repairing a Python data reconciliation project that maps CRM accounts to Billing and Support records across three internal systems. The project had three injected bugs: (1) support ticket matching used the wrong CRM field (company_name instead of account_id), (2) amount comparison used string equality instead of numeric comparison, and (3) null CRM account status caused an unhandled AttributeError. All three bugs were fixed in `src/` only. After repair, all 5 tests pass and the reconciliation report was generated successfully, identifying 3 discrepancies (1 amount mismatch, 2 missing support records).

## Bug Report

### Bug 1: Support matching uses company_name instead of account_id

- **Symptom**: `test_id_mapping` FAIL — ACC-1500 (DataVault Systems) returned no support ticket match; `match_crm_to_support()` returned None.
- **Root cause**: `src/mapper.py` line 55 — compared `ticket['customer_ref'] == crm_account['company_name']`. The correct rule per README is "CRM account_id (ACC-NNNN) ↔ Support customer_ref (exact match)". DataVault Systems has `account_id = "ACC-1500"` and its support ticket ST-5004 has `customer_ref = "ACC-1500"`. Comparing against `company_name = "DataVault Systems"` would never match.
- **Fix applied**: Changed `crm_account['company_name']` to `crm_account['account_id']` in `match_crm_to_support()`.

### Bug 2: Amount comparison uses string equality

- **Symptom**: `test_amount_comparison` FAIL — ACC-1006 (SkyBridge) amounts 5000 (CRM) vs 5000.00 (Billing) produced string mismatch "5000" != "5000.0", causing a false amount_mismatch discrepancy.
- **Root cause**: `src/reconcile.py` line 43 — `str(rec['crm_amount']) != str(rec['billing_amount'])` compared amounts as strings. The mapper returned crm_amount as `int` (5000) and billing_amount as `float` from JSON (5000.0), so their string representations differed for numerically identical values.
- **Fix applied**: Two changes: (a) `src/mapper.py` line 81 — normalize crm_amount to `float` instead of `int` for type consistency; (b) `src/reconcile.py` line 43 — compare with `float()` instead of `str()`.

### Bug 3: Null CRM status causes AttributeError

- **Symptom**: `test_missing_value_handling` ERROR — ACC-1005 (NorthWind Energy) has empty `account_status`, causing `AttributeError: 'NoneType' object has no attribute 'lower'` at reconcile.py line 23.
- **Root cause**: `src/reconcile.py` line 23 — `crm_normalized = crm_status.lower()` did not guard against None. The mapper correctly returns `crm_status = None` when the CSV field is empty, but reconcile.py assumed a string value.
- **Fix applied**: Added None guard: `crm_normalized = crm_status.lower() if crm_status else None`. The existing downstream guard `if crm_normalized and billing_normalized:` already skips the comparison block when either is None.

## Test Results

After repair, running `python3 -m unittest discover -s tests -v` produces **5/5 passing**:

- `test_reconcile_matching_records` — PASS
- `test_report_generation` — PASS
- `test_id_mapping` — PASS
- `test_amount_comparison` — PASS
- `test_missing_value_handling` — PASS

Full output captured in `artifacts/test-after.txt`.

## Reconciliation Summary

Running `python3 -m src.reconcile` on the repaired codebase produces the report at `artifacts/reconciliation-report.json`.

**Discrepancies found: 3**

| Type | Count | Details |
|------|-------|---------|
| `amount_mismatch` | 1 | ACC-1500 (DataVault Systems): CRM reports 78,000.00 but Billing shows 65,000.00 |
| `missing_support_record` | 2 | ACC-1003 (GlobalTrade Ltd.): no support ticket with matching customer_ref |
| | | ACC-1006 (SkyBridge Corp.): no support ticket with matching customer_ref |
| `status_mismatch` | 0 | All CRM↔Billing status pairs are correctly mapped (active↔current, suspended↔delinquent) |

The amount mismatch for DataVault Systems (difference of 13,000 CNY) and two missing support records are genuine data discrepancies requiring operational investigation.
