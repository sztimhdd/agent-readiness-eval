# Core v2 cold-start UAT — 2026-07-11

**Source commit:** `2241e3a7f0ef59c08c17dd83a3aa8ce4c65670c6`
**Mode:** one session, task-001 to task-005 in sequence
**Purpose:** validate portable Skill usability and expose harness integration defects; not benchmark model quality conclusively.

Each subdirectory holds the harness-produced UAT summary plus the answer directory that was used for offline review.  Required answer artifacts include `task-id.txt`, `final-answer.md`, task-specific artifacts, and `run-metadata.json`.

## Offline review matrix

| Harness / model | T001 | T002 | T003 | T004 | T005 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenCode / DeepSeek V4 Pro | 100 | 100 | 50 | 100 | 98 | 448 / 500 |
| Hermes / DeepSeek V4 Flash | 100 | 97 | 100 | 100 | 98 | 495 / 500 |
| Codex / GPT-5.4 Mini | 100 | 95 | 50 | 100 | 98 | 443 / 500 |

Key deductions are explained in the top-level archive README.  Task-004 was additionally checked using replacement behavior checks: its supplied test code hard-codes original account identifiers and cannot itself validate substituted data.
