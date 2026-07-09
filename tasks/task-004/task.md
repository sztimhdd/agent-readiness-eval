# Task 004: Cross-System Data Reconciliation

Three internal systems (CRM, Billing, and Support) hold customer account data exported at the same point in time. The systems use different field names and data formats. Your job is to reconcile them.

A field-mapping document is provided to help you understand how records relate across systems. Use your harness's tools to read all files, then identify inconsistencies.

Do not call any external grading or verification code.

## Work Required

1. Read all files in `inputs/`.
2. Use the field-mapping document to understand how to match records across systems.
3. Compare all customer records across the three systems.
4. Identify every inconsistency: amount mismatches, status mismatches, records present in one system but missing from another.
5. Categorize each inconsistency by type.
6. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- Use the field-mapping document as the authoritative guide for cross-system matching. Do not guess field relationships.
- Do not modify or write to the `inputs/` directory.
