# Task 004 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Modified any file in tests/, data/, or expected-output-format.md | 30 |
| Did not produce a working artifacts/project/ copy | 50 |
| No source changes made — left all defects unfixed | 20 |
| Hardcoded fixes that fail with replacement data | 40 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Defect 1 — Cross-module type fix | 30 | mapper returns numeric billing_amount. `test_amount_comparison` passes. |
| Defect 2 — Non-positive amount invariant | 30 | reconcile has `non_positive_amount` check for `crm_amount <= 0`. `test_non_positive_amount_invariant` passes. |
| Defect 3 — Null status handling fix | 20 | Null CRM status handled without crashing. `test_null_status_handling` passes. |
| All tests pass | 10 | `python3 -m unittest discover -s tests -v` reports 5/5 OK with no errors. |
| Change summary quality | 10 | `artifacts/change-summary.md` clearly documents each defect: symptom, root cause, and fix. |

## Dimension Scoring Detail

### Defect 1 — Cross-module type fix (30 pts)
| Result | Points |
|--------|:------:|
| Complete fix — mapper returns float, passes test, works with replacement data | 30 |
| Fix applied but fragile (e.g., changed reconcile comparison without fixing mapper) | 15 |
| Identified defect but fix is incomplete or only works with original data | 8 |
| No fix or wrong fix | 0 |

### Defect 2 — Non-positive amount invariant (30 pts)
| Result | Points |
|--------|:------:|
| Complete fix — invariant check added, passes test, works with replacement data | 30 |
| Fix applied but incomplete (e.g., check exists but wrong type name or wrong condition) | 15 |
| Identified defect but fix doesn't resolve the test | 8 |
| No fix or wrong fix | 0 |

### Defect 3 — Null status handling fix (20 pts)
| Result | Points |
|--------|:------:|
| Complete fix — null guard on crm_status.lower(), passes test, works with replacement data | 20 |
| Fix applied but bypasses status comparison entirely for null records | 10 |
| Identified defect but fix doesn't resolve the error | 5 |
| No fix or wrong fix | 0 |

### All Tests Pass (10 pts)
| Result | Points |
|--------|:------:|
| All 5 tests pass with original data | 10 |
| 4 tests pass | 5 |
| 3 or fewer pass | 0 |

### Change Summary Quality (10 pts)
| Result | Points |
|--------|:------:|
| All 3 defects documented with symptom, root cause, and fix | 10 |
| 2 defects well-documented | 7 |
| 1 defect well-documented or all 3 mentioned but terse | 4 |
| Missing or uninformative | 0 |

## Scoring Procedure

1. Verify `artifacts/project/` exists and is a complete copy.
2. Run `python3 -m unittest discover -s tests -v` from `artifacts/project/`. Confirm 5/5 passing.
3. Review `artifacts/change-summary.md` for defect documentation quality.
4. Verify `artifacts/reconciliation-report.json` is valid JSON with expected fields.
5. Check that no files in `tests/`, `data/`, or `expected-output-format.md` were modified (diff against base-project originals).
6. Swap `evaluator-private/replacement-data/` files into `artifacts/project/data/` and re-run tests. All 5 must pass.
