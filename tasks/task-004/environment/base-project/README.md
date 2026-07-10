# Reconciliation Project

A Python project for cross-system data reconciliation between CRM, Billing, and Support systems.

## Quick Start

```bash
# Run all tests
python3 -m unittest discover -s tests -v

# Run reconciliation
python3 -m src.reconcile
```

## Project Structure

```
base-project/
├── src/
│   ├── mapper.py      # Cross-system field mapping
│   ├── reconcile.py    # Main reconciliation logic
│   └── reporter.py     # JSON report generation
├── data/
│   ├── crm.csv         # CRM account data
│   ├── billing.json    # Billing records
│   └── support.csv     # Support tickets
├── tests/
│   └── test_reconcile.py
├── expected-output-format.md
└── README.md
```

## Field Mapping Rules

### CRM → Billing
- Match by: last 4 digits of `billing_account` (BA-XXX-NNNN) against `account_id` digits (ACC-NNNN)
- Status: active↔current, suspended↔delinquent
- Compare `monthly_revenue` ↔ `current_month_charges` numerically

### CRM → Support
- Match by: `account_id` (ACC-NNNN) ↔ `customer_ref` (exact match)

## Notes

- Python 3.10+ required. No external dependencies.
- All data files are in CSV or JSON format.
- Output reports are written to `output/` directory.
