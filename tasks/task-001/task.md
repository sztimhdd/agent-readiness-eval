# Task 001: Customer Ticket Triage

You are given synthetic customer-support tickets in `inputs/data.json`.

Additionally, the `inputs/` directory contains supporting documents that set authority and context:

- `severity-policy.md` — Defines severity levels and source-authority precedence rules.
- `ticket-update-log.md` — Timestamped updates that may supersede the initial `severity` field in `data.json`.

Your answer must not call any hidden grading code. Use your harness's normal tools to inspect the input and create the requested artifacts.

## Work Required

1. Read every file under `inputs/`.
2. Group tickets by severity and product area. When determining severity, consult `ticket-update-log.md` first: an update that reclassifies severity supersedes the initial label in `data.json`. Apply the source-authority precedence rules from `severity-policy.md`.
3. Identify stale severity labels — tickets whose `severity` field in `data.json` no longer reflects the latest update entry. Report which labels are stale and what the correct current severity is.
4. Identify the top operational risk with evidence from the tickets and the update log. Tickets in the same product area may or may not share a root cause — identify correlations only when supported by specific evidence.
5. Recommend the first three actions the team should take. Where the update log provides resolution information, state whether the action has already been taken.
6. Write the required files listed in `output-requirements.md`.
