"""Reconciliation orchestrator.

Maps CRM → Billing → Support, then compares amounts and reports discrepancies.
"""

import sys
from src.mapper import map_all
from src.reporter import generate_report


def reconcile():
    records = map_all()
    discrepancies = []

    for rec in records:
        crm_id = rec['crm_account_id']

        # Status comparison (CRM ↔ Billing)
        crm_status = rec['crm_status']
        billing_status = rec['billing_status']

        # Status mapping: active↔current, suspended↔delinquent
        crm_normalized = crm_status.lower() if crm_status else None
        billing_normalized = billing_status.lower() if billing_status else None

        if crm_normalized and billing_normalized:
            status_ok = (
                (crm_normalized == 'active' and billing_normalized == 'current')
                or (crm_normalized == 'suspended' and billing_normalized == 'delinquent')
                or crm_normalized == billing_normalized
            )

            if not status_ok:
                discrepancies.append({
                    'account_id': crm_id,
                    'type': 'status_mismatch',
                    'crm_status': crm_status,
                    'billing_status': billing_status,
                })

        # Amount comparison (CRM ↔ Billing)
        if rec['crm_amount'] is not None and rec['billing_amount'] is not None:
            if float(rec['crm_amount']) != float(rec['billing_amount']):
                discrepancies.append({
                    'account_id': crm_id,
                    'type': 'amount_mismatch',
                    'crm_amount': rec['crm_amount'],
                    'billing_amount': rec['billing_amount'],
                })

        # Support gap detection
        if rec['support_ticket'] is None:
            discrepancies.append({
                'account_id': crm_id,
                'type': 'missing_support_record',
            })

    report_path = generate_report(records, discrepancies)
    print(f"Reconciliation complete. {len(discrepancies)} discrepancies found.")
    print(f"Report written to {report_path}")

    if discrepancies:
        print("\nDiscrepancy summary:")
        for d in discrepancies:
            print(f"  {d['account_id']}: {d['type']} {d.get('crm_amount', '')} {d.get('billing_amount', '')}")

    return 0


if __name__ == '__main__':
    sys.exit(reconcile())
