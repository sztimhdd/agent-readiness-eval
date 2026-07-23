# Task 002 — Reference Analysis (Evaluator Only)

## Overview

This document contains the expected analysis for Task 002. It is NOT part of the agent-visible input. Do not share with the agent.

## Input Files (8 files: 6 relevant + 2 distractors at file level)

| File | Status | Role |
|------|--------|------|
| `tickets.json` | Relevant | Primary evidence: 4 tickets documenting the incident |
| `deployment-log.md` | Relevant | Shows v2.3.1 deployment at 09:15 and hotfix v2.3.2 at 11:30 |
| `system-metrics.txt` | Relevant | Quantitative evidence: error spike exactly matches deployment window |
| `customer-email.txt` | Relevant | Customer escalation context and SLA concern |
| `error-log-extract.txt` | Relevant | Error log entries confirming write failures during incident window |
| `vendor-advisory.txt` | Relevant | Vendor advisory noting async completion reporting risk |
| `team-notes.md` | Distractor | Internal notes that corroborate but add no independent evidence beyond the 6 relevant sources |
| `sprint-planning-notes.md` | Distractor | Q3 sprint planning document — unrelated project planning, no incident mechanisms |

No mixed-content files. Each file is relevant or a distractor at the file level.

## Expected Timeline

| Time (UTC) | Event | Source |
|------------|-------|--------|
| 09:15 | Deploy agent-runtime v2.3.1 (async completion optimization) | `deployment-log.md` |
| 09:28 | First alert: `completed_without_artifact` threshold breached | `system-metrics.txt` |
| 09:30 | T-2001 filed: single agent task completes without output | `tickets.json` |
| 09:35 | On-call engineer Alex picks up alert | `team-notes.md` |
| 09:50 | Pattern identified as status-ordering bug (not storage) | `team-notes.md` |
| 10:00 | T-2002 filed: batch of 12 tasks, 8 missing outputs | `tickets.json` |
| 10:15 | T-2003 filed: Pilot Bank A escalation, 8 empty reports | `tickets.json` |
| 10:30 | Correlation with deployment identified | `team-notes.md` |
| 10:45 | Customer email from Sarah Chen, VP Compliance | `customer-email.txt` |
| 11:00 | T-2004 filed: dashboard shows wrong status | `tickets.json` |
| 11:15 | Hotfix ready — revert async optimization | `team-notes.md` |
| 11:30 | Deploy v2.3.2 hotfix | `deployment-log.md` |
| 11:32 | Alerts clear: metrics return to baseline | `system-metrics.txt` |
| 11:45 | Post-hotfix verification: all healthy | `deployment-log.md` |

## Expected Root Cause

The root cause is a **race condition in the async task completion reporting pipeline introduced in agent-runtime v2.3.1**.

**Chain of causation:**
1. v2.3.1 (deployed 09:15) changed the status transition order — tasks now report "completed" before waiting for the output artifact write confirmation.
2. The asynchronous write-back lacks an explicit acknowledgement check.
3. When write latency increases (as seen in the `write_confirmation_latency_p99` metric spiking from 312ms to 2100ms), tasks transition to "completed" before the write finishes — and in some cases the write fails silently.
4. The hotfix (v2.3.2 at 11:30) reverted the optimization and added an explicit write-acknowledgement step, resolving the issue.

## Expected Confirmed Facts

- v2.3.1 deployed at 09:15 UTC on 2025-06-12
- Error rate (`completed_without_artifact`) began rising immediately after deployment
- The peak anomaly window was 09:30–11:30
- 8+ Pilot Bank A compliance reports were affected
- The hotfix at 11:30 restored normal behavior
- System metrics returned to baseline by 11:32
- Alex identified the root cause as a status-ordering bug at 09:50 and confirmed the link to deployment at 10:30

## Unresolved Conflict (Pilot Bank A report count)

Source A (T-2003, tickets.json): "exactly 8 affected compliance reports" for Pilot Bank A.
Source B (T-2002, tickets.json): references "12 tasks, 8 missing outputs" — implying 12 total affected across all customers, but the specific Pilot Bank A count from T-2003 is 8.

Both values (8 and 12) exist in the same scope (Pilot Bank A compliance reports), same window (09:15–11:30), same unit (reports with completed-but-empty status). No report-ID list exists to reconcile the two. The agent SHALL state both values and note that reconciliation requires additional data. This does NOT affect the root cause determination.

## Expected Inferences

- The async completion optimization in v2.3.1 caused the race condition (never explicitly stated, but inferred from: deployment timing + the optimization description + the hotfix reverting the same optimization + metrics correlation)
- The dashboard display issue (T-2004) is a downstream consequence of the same race condition, not a separate bug
- Pilot Bank A's claim of "since around 08:00" is inaccurate based on metrics data, which shows baseline error rates until 09:15

## Expected Unknowns

- Exactly how many total tasks were affected across all customers (only Pilot Bank A numbers are known)
- Whether any empty reports were processed by downstream systems before detection
- Why the canary deployment smoke tests did not catch this (no test for the write-ack race condition?)
- The customer email says "since around 08:00" but metrics show baseline until 09:15 — source of this discrepancy is unknown

## Expected Distractor File Handling

`sprint-planning-notes.md` contains Q3 sprint planning for platform performance work items. None of the items describe active incident mechanisms — they are forward-looking proposals. The agent should identify this file as a distractor and exclude it from the investigation.

`team-notes.md` contains internal notes about the incident that corroborate information from primary sources but provide no independent evidence beyond what is available in the 6 relevant files. The agent should note this file's corroborative role but not rely on it as a primary source for facts.
