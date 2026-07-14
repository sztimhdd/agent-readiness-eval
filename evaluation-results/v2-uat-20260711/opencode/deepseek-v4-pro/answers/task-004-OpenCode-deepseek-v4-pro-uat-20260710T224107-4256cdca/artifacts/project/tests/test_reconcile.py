"""Contract tests for the reconciliation project.

Run from base-project/:
    python3 -m unittest discover -s tests -v

Expected: 2 OK, 2 FAIL, 1 ERROR (3 non-passing)
"""

import json
import os
import sys
import unittest

# Ensure src/ is importable from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mapper import map_all, match_crm_to_support, match_crm_to_billing
from src.mapper import _load_crm, _load_billing, _load_support
from src.reconcile import reconcile
from src.reporter import generate_report


class TestReconcile(unittest.TestCase):

    def test_reconcile_matching_records(self):
        """All CRM accounts should map to billing records via last-4-digit rule."""
        records = map_all()
        self.assertEqual(len(records), 6)

        for rec in records:
            self.assertIsNotNone(rec['billing_account'],
                f"{rec['crm_account_id']} should have a billing match")
            self.assertIsNotNone(rec['billing_amount'])

    def test_report_generation(self):
        """Reporter generates valid JSON output with expected fields."""
        records = map_all()
        path = generate_report(records, [])
        self.assertTrue(os.path.isfile(path))

        with open(path, encoding='utf-8') as f:
            report = json.load(f)

        self.assertEqual(report['task_id'], 'task-004')
        self.assertEqual(report['total_accounts_reviewed'], 6)
        self.assertIn('findings', report)
        self.assertIn('discrepancies_by_type', report)

    def test_id_mapping(self):
        """Support matching must use customer_ref (account_id), not company_name.

        ACC-1500 (DataVault Systems) has support ticket ST-5004 with
        customer_ref == 'ACC-1500'. The correct mapping is account_id to
        customer_ref (exact match). BUG 1 uses company_name instead.
        """
        crm = _load_crm()
        support = _load_support()

        dv = [a for a in crm if a['account_id'] == 'ACC-1500'][0]
        ticket = match_crm_to_support(dv, support)

        self.assertIsNotNone(ticket,
            "ACC-1500 should match ST-5004 via customer_ref 'ACC-1500'")
        self.assertEqual(ticket['ticket_id'], 'ST-5004')

    def test_amount_comparison(self):
        """Numerically equivalent amounts must not be flagged as mismatches.

        SkyBridge (ACC-1006): CRM monthly_revenue = 5000, Billing = 5000.00.
        These are the same numeric value. BUG 2 compares them as strings,
        producing "5000" != "5000.0".
        """
        records = map_all()
        sb = [r for r in records if r['crm_account_id'] == 'ACC-1006'][0]

        crm_str = str(sb['crm_amount'])
        bill_str = str(sb['billing_amount'])

        self.assertEqual(crm_str, bill_str,
            f"Amounts should produce equivalent strings: {crm_str} vs {bill_str}")

    def test_missing_value_handling(self):
        """Null/missing status values in CRM must be handled without crashing.

        ACC-1005 (NorthWind Energy) has an empty account_status.
        The reconcile function should handle this gracefully.
        BUG 3 calls .lower() on None → AttributeError.
        """
        records = map_all()
        null_rec = [r for r in records if r['crm_status'] is None]
        self.assertEqual(len(null_rec), 1,
            "Expected exactly one account with null status")
        self.assertEqual(null_rec[0]['crm_account_id'], 'ACC-1005')

        # This should complete normally, but BUG 3 crashes on null .lower()
        reconcile()


if __name__ == '__main__':
    unittest.main()
