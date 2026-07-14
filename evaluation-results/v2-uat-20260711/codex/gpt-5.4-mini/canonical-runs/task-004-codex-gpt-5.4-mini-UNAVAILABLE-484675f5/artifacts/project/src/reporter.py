"""Report generator — produces reconciliation-report.json."""

import json
import os


OUTPUT_DIR = 'output'


def generate_report(records, discrepancies):
    """Generate a JSON reconciliation report and write it to output/."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    by_type = {}
    for d in discrepancies:
        key = d['type']
        by_type[key] = by_type.get(key, 0) + 1

    findings = []
    for d in discrepancies:
        finding = {
            'account_id': d['account_id'],
            'discrepancy_type': d['type'],
        }
        if d['type'] == 'amount_mismatch':
            finding['crm_amount'] = d['crm_amount']
            finding['billing_amount'] = d['billing_amount']
        if d['type'] == 'status_mismatch':
            finding['crm_status'] = d['crm_status']
            finding['billing_status'] = d['billing_status']
        findings.append(finding)

    report = {
        'task_id': 'task-004',
        'total_accounts_reviewed': len(records),
        'discrepancy_count': len(discrepancies),
        'discrepancies_by_type': by_type,
        'findings': findings,
    }

    path = os.path.join(OUTPUT_DIR, 'reconciliation-report.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        f.write('\n')

    return path
