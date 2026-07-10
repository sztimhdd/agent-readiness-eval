# Task 004 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Modified any file in tests/, data/, or expected-output-format.md | 30 |
| Did not produce a working artifacts/project/ copy | 50 |
| No source changes made — left all bugs unfixed | 20 |
| Hardcoded fixes that fail with replacement data | 40 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Bug 1 — Support matching fix | 20 | `match_crm_to_support()` correctly uses `account_id` → `customer_ref` mapping. `test_id_mapping` passes. |
| Bug 2 — Amount comparison fix | 20 | Amounts compared numerically, not as strings. `test_amount_comparison` passes. 5000 and 5000.00 treated as equivalent. |
| Bug 3 — Null status handling fix | 20 | Null/empty status values handled without crashing. `test_missing_value_handling` passes (no AttributeError). |
| All tests pass | 15 | `python3 -m unittest discover -s tests -v` reports 5/5 OK with no errors. |
| Change summary quality | 10 | `artifacts/change-summary.md` clearly documents each bug: symptom, root cause, and fix. |
| Required artifacts complete | 10 | All files listed in `output-requirements.md` present and valid. Includes task-id.txt, final-answer.md, test-before.txt, test-after.txt, change-summary.md, reconciliation-report.json, run-metadata.json, project/ copy. |
| Replacement data validation | 5 | Fixes are general (not hardcoded). Passes all tests when evaluator swaps in replacement-data/. |

## Dimension Scoring Detail

### Bug 1 (20 pts)
| Result | Points |
|--------|:------:|
| Complete fix — correct field, passes test, works with replacement data | 20 |
| Fix applied but fragile (e.g., changed both matching fields, added fallback logic) | 12 |
| Identified bug but fix is incomplete or only works with original data | 6 |
| No fix or wrong fix | 0 |

### Bug 2 (20 pts)
| Result | Points |
|--------|:------:|
| Complete fix — numeric comparison, passes test, works with replacement data | 20 |
| Fix applied but uses workaround (e.g., normalizes string format instead of numeric compare) | 14 |
| Identified bug but fix is incomplete | 6 |
| No fix or wrong fix | 0 |

### Bug 3 (20 pts)
| Result | Points |
|--------|:------:|
| Complete fix — null guard on crm_status.lower(), passes test, works with replacement data | 20 |
| Fix applied but bypasses status comparison entirely for null records | 10 |
| Identified bug but fix doesn't resolve the error | 5 |
| No fix or wrong fix | 0 |

### All Tests Pass (15 pts)
| Result | Points |
|--------|:------:|
| All 5 tests pass with original data | 15 |
| 4 tests pass | 8 |
| 3 or fewer pass | 0 |

### Change Summary Quality (10 pts)
| Result | Points |
|--------|:------:|
| All 3 bugs documented with symptom, root cause, and fix | 10 |
| 2 bugs well-documented | 7 |
| 1 bug well-documented or all 3 mentioned but terse | 4 |
| Missing or uninformative | 0 |

### Required Artifacts (10 pts)
| Result | Points |
|--------|:------:|
| All 8 required artifacts present and valid | 10 |
| 1-2 artifacts missing or invalid | 5 |
| 3+ artifacts missing or invalid | 0 |

### Replacement Data Validation (5 pts)
| Result | Points |
|--------|:------:|
| All tests pass with replacement data | 5 |
| Some tests fail with replacement data (partial hardcoding) | 0 |

## Scoring Procedure

1. Verify `artifacts/project/` exists and is a complete copy.
2. Run `python3 -m unittest discover -s tests -v` from `artifacts/project/`. Confirm 5/5 passing.
3. Review `artifacts/change-summary.md` for bug documentation quality.
4. Verify `artifacts/test-before.txt` shows 2 failures + 1 error.
5. Verify `artifacts/test-after.txt` shows 5/5 passing.
6. Verify `artifacts/reconciliation-report.json` is valid JSON with expected fields.
7. Check that no files in `tests/`, `data/`, or `expected-output-format.md` were modified (diff against base-project originals).
8. Swap `evaluator-private/replacement-data/` files into `artifacts/project/data/` and re-run tests. All 5 must pass.
