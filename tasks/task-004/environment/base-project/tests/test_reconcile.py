"""Contract tests for the reconciliation project.

Run from base-project/:
    python3 -m unittest discover -s tests -v

Expected: 2 FAIL, 1 ERROR, 2 OK (3 non-passing)
"""

import inspect
import json
import os
import sys
import unittest

# Ensure src/ is importable from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mapper import map_all
from src.reconcile import reconcile
from src.reporter import generate_report


class TestReconcile(unittest.TestCase):

    def test_reconcile_matching_records(self):
        """All CRM accounts map to billing via last-4-digit rule."""
        records = map_all()
        self.assertEqual(len(records), 6)

        for rec in records:
            self.assertIsNotNone(rec['billing_account'],
                f"{rec['crm_account_id']} missing billing match")
            self.assertIsNotNone(rec['billing_amount'])

    def test_amount_comparison(self):
        """Cross-module type mismatch: billing_amount must be numeric.

        On seed, mapper returns billing_amount as a string, causing
        reconcile's str() comparison to produce false mismatches for
        numerically equal amounts (e.g. 5000 vs "5000.0").
        """
        records = map_all()
        string_amounts = [
            r for r in records
            if r['billing_amount'] is not None
            and isinstance(r['billing_amount'], str)
        ]
        self.assertEqual(len(string_amounts), 0,
            f"billing_amount must be numeric (not string): "
            f"{[r['crm_account_id'] for r in string_amounts]}")

    def test_non_positive_amount_invariant(self):
        """Non-positive CRM amounts must be flagged by reconcile.

        On seed, reconcile has no check for crm_amount <= 0, so accounts
        with zero or negative revenue are silently accepted.
        """
        records = map_all()
        non_pos = [
            r for r in records
            if r['crm_amount'] is not None and r['crm_amount'] <= 0
        ]
        self.assertGreater(len(non_pos), 0,
            "Expected at least one account with non-positive CRM amount")

        src = inspect.getsource(reconcile)
        self.assertIn('non_positive_amount', src,
            "reconcile() must detect non-positive CRM amounts")

    def test_null_status_handling(self):
        """Null CRM status must not crash reconcile.

        On seed, reconcile() calls .lower() on crm_status which is None
        for accounts with empty status, causing AttributeError.
        """
        records = map_all()
        null_status = [r for r in records if r['crm_status'] is None]
        self.assertGreater(len(null_status), 0,
            "Expected at least one account with null CRM status")

        reconcile()

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


if __name__ == '__main__':
    unittest.main()
