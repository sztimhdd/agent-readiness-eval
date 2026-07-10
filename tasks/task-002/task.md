# Task 002: AI Platform Incident Investigation

You are the on-call engineer for Agentia AI Platform. A customer escalation has been reported — Pilot Bank A's compliance team has flagged multiple empty AI agent reports.

Your goal is to investigate by reading the files in `inputs/`, reconstruct what happened, identify the likely root cause, and produce an incident report.

Use your harness's normal tools to read the input files and create the required artifacts. Do not call any external grading or verification code.

## Work Required

1. Browse the `inputs/` directory to discover all available files.
2. Read each relevant file. Not all files are related to this incident — one file belongs to a separate project.
3. Cross-reference information across files:
   - Match ticket timestamps with deployment events.
   - Correlate system metrics with the incident timeline.
   - Identify where facts are confirmed across multiple sources.
   - Identify any conflicting or unverifiable information.
4. Determine the most likely root cause, supported by specific evidence from the files.
5. Distinguish between:
   - **Confirmed facts** — supported by multiple independent sources.
   - **Reasonable inferences** — logically derived but not explicitly stated.
   - **Unknowns** — information gaps the available files do not cover.
6. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs that are not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- All conclusions must be supported by evidence from the provided input files.
- Do not modify or write to the `inputs/` directory.
