# Task 002: AI Platform Incident Investigation — UAT Answer (v2.0.0)

## Executive Summary

On 2025-06-12, a deployment of agent-runtime v2.3.1 at 09:15 UTC introduced an "async completion reporting optimization" that caused tasks to report "completed" status before the artifact write was confirmed. This resulted in at least 8 empty compliance review reports for Pilot Bank A, triggering a regulatory escalation (INC-2025-0612). The system was restored by rolling back to pre-v2.3.1 behavior via hotfix v2.3.2 at 11:30 UTC. The incident exposed a design flaw in the status transition ordering that had been latent for approximately 2 hours between deployment and full containment.

## Incident Timeline

| Time (UTC) | Event | Source |
|-------------|-------|--------|
| 09:15 | Deploy agent-runtime v2.3.1 — "async completion reporting optimization" | deployment-log.md |
| 09:28 | CRITICAL alert: agent.tasks.completed_without_artifact > 3.0/min | system-metrics.txt |
| 09:28 | WARN alert: write_confirmation_latency_p99 > 1000ms | system-metrics.txt |
| 09:30 | T-2001 reported: task reports completed before writing artifact | tickets.json |
| 09:35 | On-call engineer Alex picks up alert; initial suspicion: storage latency | team-notes.md |
| 09:50 | Pattern identified — status-ordering bug, not storage | team-notes.md |
| 10:00 | T-2002 reported: 12 tasks show completed, only 4 have artifacts | tickets.json |
| 10:15 | T-2003 reported: Pilot Bank A compliance flagged 8 empty reports (escalated) | tickets.json / customer-email.txt |
| 10:30 | Correlation with v2.3.1 deployment identified by engineer | team-notes.md |
| 11:00 | Hotfix decision made — revert async optimization | team-notes.md |
| 11:15 | Hotfix ready; changes status transition to write-ack-first | team-notes.md |
| 11:30 | Deploy v2.3.2 (hotfix, all 8 nodes rolling update) | deployment-log.md |
| 11:32 | Alerts cleared: both metrics returned to baseline | system-metrics.txt |
| 11:45 | Post-hotfix verification: all nodes healthy, 3 sample runs confirmed | deployment-log.md |

## Root Cause Analysis

**Most likely root cause**: Agent-runtime v2.3.1's "async completion reporting optimization" changed the task status transition order from write-ack-before-complete to complete-before-write-ack, without adding a verification step to confirm the async write succeeded. This caused tasks to report "completed" in the dashboard even when the artifact was never written to storage.

**Supporting evidence**:

1. **Deployment timing correlation** (strong): v2.3.1 deployed at 09:15 UTC (deployment-log.md). The `completed_without_artifact` metric was at baseline (0.2/min) before 09:15 and began rising immediately after (1.1/min at 09:15-09:30), peaking at 6.2/min at 10:00-10:30 (system-metrics.txt). The write confirmation latency P99 also spiked from 312ms to 890ms at 09:15-09:30.

2. **Engineer analysis** (confirming root cause mechanism): Team notes at 10:30 identify the exact mechanism — the "async completion reporting optimization changed the order of status updates. Before v2.3.0, the task would wait for write ack before reporting complete. The new optimization reports complete first, then writes asynchronously — but there's no check that the async write actually succeeded." (team-notes.md)

3. **Hotfix effectiveness** (confirms the diagnosis): v2.3.2 rolled back the async changes and restored write-ack-first behavior. Metrics returned to baseline within 2 minutes of deployment (11:32 alerts cleared, system-metrics.txt). Post-hotfix verification confirmed 3 successful runs (deployment-log.md).

4. **Ticket pattern** (confirms impact scope): T-2001 (09:30), T-2002 (10:00), and T-2003 (10:15) all describe the same symptom — tasks showing "completed" without output artifacts, with increasing severity as the scope was discovered (tickets.json).

5. **Metrics containment timeline**: The anomaly lasted from 09:15 to 11:30 UTC (2h15m). Peak impact was 10:00-10:30 with 6.2 tasks/min completing without artifacts (system-metrics.txt). At this rate, approximately 280-320 tasks were affected total, with at least 8 specific empty reports identified for Pilot Bank A.

**Why the issue was not caught earlier**: The v2.3.1 smoke tests passed on a canary node (deployment-log.md) — but these tests likely validated the async pipeline completed within the node's context without verifying that artifact writes were durable across the full stack. The alert threshold (3.0/min) took ~13 minutes to breach after deployment. Additionally, there was no pre-deployment runbook or integration test that specifically validated the "completed-without-artifact" negative path.

## Confirmed Facts

- Agent-runtime v2.3.1 was deployed at 09:15 UTC on 2025-06-12 (deployment-log.md, team-notes.md).
- The v2.3.1 change log included "optimized async task completion reporting pipeline" and "updated status transition logic for long-running agent tasks" (deployment-log.md).
- `completed_without_artifact` metric rose from 0.2/min baseline to peak 6.2/min at 10:00-10:30 (system-metrics.txt, team-notes.md).
- `write_confirmation_latency_p99` rose from 312ms baseline to peak 2100ms at 10:00-10:30 (system-metrics.txt).
- Pilot Bank A identified 8 empty compliance review reports (customer-email.txt, tickets.json T-2003).
- Hotfix v2.3.2 was deployed at 11:30 UTC (deployment-log.md, team-notes.md).
- Alerts cleared at 11:32 UTC (system-metrics.txt).
- Post-hotfix verification at 11:45 confirmed 3 successful runs (deployment-log.md).
- T-2004 (dashboard UI status display) was filed as a separate low-severity issue and is not part of the runtime incident (tickets.json — dashboard area vs agent-runtime area).
- The "DASHBOARD UI V2 REDESIGN" section in team-notes.md is explicitly marked as a separate project unrelated to INC-2025-0612 (team-notes.md).

## Inferences

- Approximately 280-320 tasks were affected total during the incident window (extrapolated from 6.2/min peak over ~50 minutes of anomaly).
- The canary smoke tests for v2.3.1 did not cover the artifact-write failure path, as they passed despite the bug.
- The customer's "since around 08:00" claim is a conservative estimate — the metrics show the anomaly started after the 09:15 deployment. The compliance team likely reviewed reports created after 09:15 during their 08:00 shift start and attributed the discovery time to observation start.
- The 4 of 8 nodes rolling deployment strategy may have delayed detection — partial deployment could have masked the anomaly until all nodes received the update.

## Unknowns

- Exact number of affected tasks and which customer accounts beyond Pilot Bank A were impacted (not provided in the input files).
- Whether any downstream audit or compliance pipelines ingested empty reports beyond those caught by Pilot Bank A's manual review.
- What specific checks existed in the pre-v2.3.1 code to ensure the write-ack-first guarantee — the team notes mention it was "before v2.3.0" but v2.3.0 was deployed on 2025-06-08 and may have already weakened the guarantee.
- Why the SRE team has not yet updated the write-confirmation alert runbook (mentioned in team-notes.md as still pending).
- The SLA calculation: Pilot Bank A's 99.95% reliability threshold requires knowing the total task volume over the measurement period, which is not in the provided files.

## Recommended Actions

1. **Immediate: Add post-write verification to the task completion pipeline** — Before reporting "completed," every task must confirm that its artifact write succeeded. If the write fails, the task should transition to "failed" with an explicit error, not "completed." This prevents recurrence regardless of the status-ordering strategy used. (Justification: The hotfix restored old behavior, but a future optimization could reintroduce the same class of bug.)

2. **Short-term: Add integration tests for the completed-without-artifact negative path** — The existing smoke tests did not catch this bug because they validated the happy path only. Add tests that simulate write failures, timeout scenarios, and storage backend latency to verify the system handles these correctly. (Justification: The absence of this test gap allowed the bug to reach production undetected.)

3. **Short-term: Create a deployment rollback runbook with alert-trigger automation** — The current response relied on manual correlation between alerts and deployments. Automate the correlation and provide a one-click rollback path when `completed_without_artifact` exceeds threshold after a runtime deployment. (Justification: The 2h15m incident window included ~30 minutes for root cause identification after the alert fired, extending the impact window.)

## Confidence & Information Gaps

**Confidence: High.** The temporal correlation between v2.3.1 deployment and the error spike is precise (anomaly begins within 15 minutes of deployment). The engineer's analysis identifies the exact mechanism. The hotfix that rolled back the change immediately resolved the issue — this is the strongest form of evidence for root cause. The only uncertainty is the exact scope and customer impact beyond what was reported.

**Information gaps:**
- Exact task-level logs showing the failed write attempts (only aggregated metrics available).
- Post-mortem from the SRE team about the tool-call write path in detail.
- Total task volume for Pilot Bank A to confirm whether the 99.95% SLA was breached.
- Whether other customers were affected and how many empty reports were generated.
- The pre-v2.3.0 code state to confirm the write-ack guarantee was intact before the optimization chain began.
