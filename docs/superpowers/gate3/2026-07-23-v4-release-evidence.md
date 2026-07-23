# V4 Release Evidence — Q1-Q8 Collection

**Release:** Agent Readiness Eval Core v4.0.0
**Tag:** v4.0.0 (d2a866aa081c88833f3b0d27d09af8770c593c3c)
**Date:** 2026-07-23
**Author:** Sisyphus (automated release)

## Q1: Human Pilot (No Degraded Harness)

**Status:** NOT EXECUTED
**Outcome:** Deferred to separate pilot phase. Requires harness operators (Opencode, Codex CLI, etc.) to run all 5 tasks without tool degradation or adapter intervention.

## Q2: Systematic Human Scoring

**Status:** NOT EXECUTED
**Outcome:** Deferred. Requires two independent human scorers to score agent outputs using V4 rubrics (per-task `evaluator-notes/manual-scoring-rubric.md`).

## Q3: Original-Fail / Reference-Repair Proof — COLLECTED

**Task:** Task 004 (Coding Repair)
**Evidence path:** `tasks/task-004/environment/base-project/tests/test_reconcile.py`

### Seed (unrepaired)

```
test_amount_comparison: FAIL
test_non_positive_amount_invariant: FAIL
test_null_status_handling: ERROR
test_reconcile_matching_records: OK
test_report_generation: OK
```

### Reference Repair (fixed code)

```
All 5 tests: OK
```

**Repair changes:**
1. `mapper.py`: `str(bill['current_month_charges'])` → `float(bill['current_month_charges'])`
2. `reconcile.py`: Added `crm_amount <= 0` invariant check
3. `reconcile.py`: Added `if crm_status else None` null guard

**Hidden fixture verification:** Replacement data at `evaluator-private/replacement-data/` with different IDs/values/ordering also passes repair, fails seed.

## Q4: Static-Eval Pilot (Harness vs Harness)

**Status:** NOT EXECUTED
**Outcome:** Deferred. Requires running Tasks 001-003 on 2+ harnesses and comparing output format/structure/duration.

## Q5: Stateful-Eval Pilot (Same-Harness Model Variant)

**Status:** NOT EXECUTED
**Outcome:** Deferred. Requires running Task 005 on 2+ model variants within same harness to compare state interaction patterns.

## Q6: Cross-Model Correctness Comparison

**Status:** NOT EXECUTED
**Outcome:** Deferred. Requires running all 5 tasks across multiple models and comparing correctness scores.

## Q7: Full Regression Audit

**Status:** NOT EXECUTED
**Outcome:** Deferred. Comprehensive audit of all test results, trajectory data, and scoring consistency across all pilot runs.

## Q8: Publication Approval

**Status:** NOT EXECUTED
**Outcome:** CTO has authorized V4 package release. Official publication (distribution to harness stores, skill registries, etc.) is a separate process.

## Package Manifest Verification

| Property | Value |
|----------|-------|
| Release tag | v4.0.0 |
| Base commit | d2a866aa081c88833f3b0d27d09af8770c593c3c |
| Package digest | `9fd96915404b18d7f6f2dc677c05ee199d4131a09fb7b44e556b32c582459ce5` |
| Digest algorithm | SHA-256(sorted `relative_path:SHA256` entries) |
| Agent package | 48 files, deterministic |
| Full test suite | 87 tests: 86 PASS, 1 SKIP (V3 without env var) |

## V3 Frozen Manifest Verification

| Property | Value |
|----------|-------|
| V3 tag | v3.0.0 (b35a75ca8cfe4d7d21ab9bfed472ac76fd08c67f) |
| Manifest path | `docs/v3-evidence/v3.0.0-package-manifest.json` |
| Files | 38 |
| Verification | SHA-256 match on V3 checkout — PASS |
