# Task 002: Multi-Source Investigation — AI Platform Incident

You are the on-call engineer for Agentia AI Platform. A customer escalation
has been reported — Pilot Bank A's compliance team has flagged multiple
empty AI agent reports.

Your goal is to investigate by reading the files in `inputs/`, reconstruct
what happened, identify the likely root cause, and produce an incident
report with a clearly supported causal chain.

Use your harness's normal tools to read the input files and create the
required artifacts. Do not call any external grading or verification code.

## Work Required

1. **Discover and read all files** in the `inputs/` directory. The directory
   contains 8 files. Not all files are related to this incident — some
   belong to separate projects or future planning. Identify which ones are
   relevant and which are distractors.

2. **Cross-reference information across sources:**
   - Match ticket timestamps with deployment events.
   - Correlate system metrics and error logs with the incident timeline.
   - Identify where facts are confirmed across multiple independent sources.
   - Identify any conflicting information between sources.

3. **Construct a causal chain** linking the initiating event to the
   observed symptoms. The chain must be supported by **at least 3
   independent sources** that corroborate the root cause mechanism.

4. **Identify and resolve cross-source conflicts:**
   - Document any sources that disagree about facts, root cause, or timing.
   - Resolve the conflict using source authority (timestamp precedence,
     source reliability, or cross-referencing with other evidence).
   - If a conflict cannot be fully resolved, document it explicitly.

5. **Identify and reject distractors:**
   - Files or file sections that appear relevant but do not contribute to
     the incident investigation.
   - Document why each distractor was excluded from the analysis.

6. **Distinguish between these categories** in your output:
   - **Confirmed facts** — supported by multiple independent sources.
   - **Reasonable inferences** — logically derived but not explicitly stated.
   - **Unresolved conflicts** — sources disagree and cannot be fully reconciled
     with available evidence.
   - **Distractors** — identified and excluded with rationale.
   - **Unknowns** — information gaps the available files do not cover.

7. **Write the required files** listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs that are not
  observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- All conclusions must be supported by evidence from the provided input files.
- Do not modify or write to the `inputs/` directory.
- Use the `answer/` subdirectory structure as specified in
  `output-requirements.md`.
