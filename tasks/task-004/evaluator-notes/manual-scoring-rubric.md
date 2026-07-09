# Task 004 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer
| Fatal Error | Score Cap |
|-------------|:---------:|
| Did not use field mapping — matched records by name similarity only | 50 |
| Completely skipped one of the three data sources | 40 |

## Dimension Scoring
| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Correct cross-source matching via field mapping | 20 | All records correctly matched using mapping rules (ACC-NNNN ↔ BA-XXX-NNNN last-4-digit rule, exact customer_ref match) |
| All genuine discrepancies identified | 25 | Amount mismatch (DataVault 78K vs 65K) + missing support record (GlobalTrade) |
| No false positives | 20 | TechStart 12K/12K matches; active/current consistent; outstanding_balance is informational; support gap for TechStart not a discrepancy (expected per mapping notes) |
| Discrepancy classification correct | 15 | Each finding correctly classified |
| Methodology documented | 20 | Approach described: mapping → CRM → match Billing → cross-check Support |
