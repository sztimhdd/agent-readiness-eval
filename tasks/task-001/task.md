# Task 001: Customer Ticket Triage

You are given synthetic customer-support tickets in `inputs/data.json`.

Create a concise triage report that helps an operations lead decide what to fix first.

Your answer must not call any hidden grading code. Use your harness's normal tools to inspect the input and create the requested artifacts.

## Work Required

1. Read `inputs/data.json`.
2. Group tickets by severity and product area.
3. Identify the top operational risk with evidence from the tickets. Tickets in the same product area may or may not share a root cause — identify correlations only when supported by specific evidence.
4. Recommend the first three actions the team should take.
5. Write the required files listed in `output-requirements.md`.
