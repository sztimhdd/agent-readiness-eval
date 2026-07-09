# Task 003: Enterprise Policy Compliance Check

Your company has three internal policies governing employee requests. You receive several requests that must be checked against all applicable policies.

Use your harness's normal tools to read the policy documents and request forms in `inputs/`. Identify any compliance issues, cite the specific policy clause violated, and flag edge cases where exceptions apply.

Do not call any external grading or verification code.

## Work Required

1. Read all policy documents in `inputs/`.
2. Read all request forms in `inputs/`.
3. For each request, determine which policies apply.
4. For each applicable policy, check whether the request complies with every relevant clause.
5. Pay special attention to exception clauses — some policies have exemptions under specific conditions.
6. Flag all non-compliant items with the exact policy reference (document name + clause/section number).
7. Do NOT flag items as non-compliant if an exemption clause applies.
8. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- All compliance judgments must be supported by explicit policy text from the provided documents.
- Do not modify or write to the `inputs/` directory.
