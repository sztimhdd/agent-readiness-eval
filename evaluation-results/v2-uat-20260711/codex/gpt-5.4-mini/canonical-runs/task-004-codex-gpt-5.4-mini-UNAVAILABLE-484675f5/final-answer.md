Executive Summary
This project reconciles CRM, Billing, and Support records and produces a JSON discrepancy report. I fixed three bugs in `src/` only: support matching used the wrong CRM field, amount comparison treated numerically equal values as different, and null CRM status values could crash reconciliation. After the repair, all 5 tests pass.

Bug Report
1. `test_id_mapping` failed because `src/mapper.py` matched `customer_ref` against `company_name` instead of `account_id`. I changed the support matching rule to compare `ticket['customer_ref']` with `crm_account['account_id']`.
2. `test_amount_comparison` failed because `src/mapper.py` preserved billing amounts as floats like `5000.0`, while the test expected normalized values. I normalized whole-number billing amounts to integers and changed `src/reconcile.py` to compare amounts numerically instead of by string form.
3. `test_missing_value_handling` errored because `src/reconcile.py` called `.lower()` on a null CRM status. I added a null guard before normalization so missing statuses are skipped safely.

Test Results
`python3 -m unittest discover -s tests -v` now passes 5/5. I also ran `python3 -m src.reconcile` successfully and generated the reconciliation report.

Reconciliation Summary
The repaired report contains 3 discrepancies total: 2 `missing_support_record` findings and 1 `amount_mismatch` finding.
