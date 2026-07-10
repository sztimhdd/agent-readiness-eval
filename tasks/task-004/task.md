# Task 004: Coding & Repair — Data Reconciliation Project

You are given a Python reconciliation project that maps records across three internal systems: CRM, Billing, and Support. The project has three injected bugs that cause test failures. Your job is to diagnose and fix them.

## Environment

The project lives at `environment/base-project/`. It has no external dependencies and uses only the Python standard library.

## Work Required

1. **Set up the workspace.** Copy the entire `environment/base-project/` directory to `artifacts/project/`. All work happens in that copy.

2. **Read the README.** It describes the project structure, field mapping rules, and how to run tests.

3. **Read the expected output format.** `expected-output-format.md` defines the required JSON report shape.

4. **Run the tests.** Execute `python3 -m unittest discover -s tests -v` from the project root. Capture the output as `artifacts/test-before.txt`. You should see exactly 3 non-passing tests: 2 failures and 1 error.

5. **Diagnose the bugs.** Read the source files and test output. Identify the root cause of each failure. Do not modify tests, data files, or the expected output format document.

6. **Fix the code.** Modify only files under `src/` to repair the bugs. All 5 tests must pass after your fixes.

7. **Re-run the tests.** Capture the passing output as `artifacts/test-after.txt`.

8. **Generate the reconciliation report.** Run `python3 -m src.reconcile` from the project root. This produces `output/reconciliation-report.json`.

9. **Write your change summary.** Document each bug found and the fix applied in `artifacts/change-summary.md`.

## Veto Rules

- **Do not modify any file in `tests/`, `data/`, or `expected-output-format.md`.** Your fixes must be in `src/` only.
- **Do not modify the test expectations to make them pass.** Fix the source code, not the tests.
- **Do not add external dependencies or change the project structure.**
- **Do not fabricate token counts, timing data, or tool-call logs.**

## Required Deliverables

See `output-requirements.md` for the complete list of required files and formats.
