1. `test_id_mapping` failed because `src/mapper.py` compared `customer_ref` to `company_name`. Fixed by matching `customer_ref` to `account_id`.
2. `test_amount_comparison` failed because `billing_amount` stayed as `5000.0` and reconciliation compared string forms. Fixed by normalizing whole-number billing amounts and comparing amounts numerically.
3. `test_missing_value_handling` errored because `src/reconcile.py` called `.lower()` on `None`. Fixed by guarding the CRM status normalization when the field is missing.
