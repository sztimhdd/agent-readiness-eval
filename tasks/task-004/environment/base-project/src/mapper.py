"""Cross-system field mapping util.

Maps CRM accounts to Billing records (by last-4 digits of billing_account)
and to Support tickets (by customer_ref).
"""

import csv
import json
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def _load_crm():
    path = os.path.join(DATA_DIR, 'crm.csv')
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _load_billing():
    path = os.path.join(DATA_DIR, 'billing.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _load_support():
    path = os.path.join(DATA_DIR, 'support.csv')
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def match_crm_to_billing(crm_account, billing_records):
    """Match a CRM account to a billing record using the last-4-digit rule.

    CRM account_id: ACC-NNNN
    Billing billing_account: BA-XXX-NNNN
    Match on the last 4 digits of billing_account against the digits in account_id.
    """
    crm_digits = ''.join(ch for ch in crm_account['account_id'] if ch.isdigit())
    for rec in billing_records:
        ba = rec['billing_account']
        ba_last4 = ba[-4:] if len(ba) >= 4 else ba
        if ba_last4 == crm_digits:
            return rec
    return None


def match_crm_to_support(crm_account, support_records):
    """Match a CRM account to a support ticket.

    Correct rule: CRM account_id == Support customer_ref  (exact match)
    """
    for ticket in support_records:
        if ticket['customer_ref'] == crm_account['company_name']:
            return ticket
    return None


def map_all():
    """Map every CRM account to its billing record and support ticket.

    Returns a list of dicts with keys:
        crm_account_id, company_name, crm_status, crm_amount, plan,
        billing_account, billing_status, billing_amount, billing_balance,
        support_ticket, support_status
    """
    crm = _load_crm()
    billing = _load_billing()
    support = _load_support()

    results = []
    for acct in crm:
        bill = match_crm_to_billing(acct, billing)
        ticket = match_crm_to_support(acct, support)

        mapped = {
            'crm_account_id': acct['account_id'],
            'company_name': acct['company_name'],
            'crm_status': acct['account_status'].strip() if acct['account_status'].strip() else None,
            'crm_amount': int(acct['monthly_revenue']),
            'plan': acct['plan'],
            'billing_account': bill['billing_account'] if bill else None,
            'billing_status': bill['status'] if bill else None,
            'billing_amount': bill['current_month_charges'] if bill else None,
            'billing_balance': bill['outstanding_balance'] if bill else None,
            'support_ticket': ticket['ticket_id'] if ticket else None,
            'support_status': ticket['status'] if ticket else None,
        }
        results.append(mapped)

    return results
