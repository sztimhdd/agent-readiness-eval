# AI Platform Incident Investigation — Task 002

## Executive Summary

On 2025-06-12, a race condition introduced in agent-runtime v2.3.1 (deployed 09:15 UTC) caused agent tasks to report "completed" before confirming output artifact writes. This resulted in empty reports being accepted by downstream systems, including 8 compliance reports at Pilot Bank A that triggered an account-level escalation. The incident was detected via metrics alert at 09:28 and resolved by hotfix v2.3.2 at 11:30 UTC. Total incident duration: approximately 2 hours 15 minutes.

## Incident Timeline

| Time (UTC) | Event | Source |
|------------|-------|--------|
| 09:15 | Deploy agent-runtime v2.3.1 (async completion optimization) | `deployment-log.md` |
| 09:28 | CRITICAL alert: `completed_without_artifact > 3.0/min` | `system-metrics.txt` |
| 09:30 | T-2001 filed: single agent task completes without output | `tickets.json` |
| 09:35 | On-call engineer Alex picks up alert, checks S3 (healthy) | `team-notes.md` |
| 09:50 | Pattern identified: status-ordering bug, not storage | `team-notes.md` |
| 10:00 | T-2002 filed: batch of 12 tasks, only 4 have outputs | `tickets.json` |
| 10:15 | T-2003 filed: Pilot Bank A escalation — 8 empty compliance reports | `tickets.json` |
| 10:30 | Correlation confirmed: v2.3.1 changed status transition order | `team-notes.md` |
| 10:45 | Customer email: Sarah Chen (VP Compliance, Pilot Bank A) demands RCA | `customer-email.txt` |
| 11:00 | T-2004 filed: dashboard shows wrong status (symptom) | `tickets.json` |
| 11:15 | Hotfix ready: revert async optimization, add write-ack | `team-notes.md` |
| 11:30 | Deploy v2.3.2 hotfix | `deployment-log.md` |
| 11:32 | All alerts clear: metrics return to baseline | `system-metrics.txt` |
| 11:45 | Post-hotfix verification: all healthy | `deployment-log.md` |

## Root Cause Analysis

**Most likely root cause:** A race condition in the async task completion reporting pipeline introduced in agent-runtime v2.3.1. The deployment changed the status transition order — tasks now reported "completed" before waiting for the output artifact write confirmation. When write latency increased (metrics show `write_confirmation_latency_p99` spiking from 312ms to 2,100ms), writes failed silently while the task had already transitioned to "completed."

**Supporting evidence:**
- `deployment-log.md`: v2.3.1 change log explicitly states "Optimized async task completion reporting pipeline" and "Updated status transition logic." The hotfix v2.3.2 notes directly confirm the fix: "reverted async completion reporting optimization" and "Fixed race condition where task status was set to 'completed' before the output artifact write confirmed."
- `system-metrics.txt`: `completed_without_artifact` rises from 0.2/min (baseline) to 6.2/min at peak, beginning immediately after 09:15 deployment and returning to baseline after 11:30 hotfix. `write_confirmation_latency_p99` mirrors this pattern.
- `team-notes.md`: Engineer Alex identifies the mechanism at 09:50 ("write confirmation never fires but the task still transitions to completed") and confirms the correlation with v2.3.1 at 10:30.
- `tickets.json`: All four tickets (T-2001 through T-2004) describe symptoms consistent with the same root cause.

**Why the issue was not caught earlier:** The deployment smoke tests passed on the canary node. The smoke tests likely did not include a check for artifact completeness after task completion — they validated the status transition but not the write confirmation.

## Confirmed Facts

- v2.3.1 was deployed at 09:15 UTC on 2025-06-12 (confirmed by `deployment-log.md` and `team-notes.md`)
- The `completed_without_artifact` metric rose immediately after deployment, from 0.2/min to a peak of 6.2/min (confirmed by `system-metrics.txt` and `team-notes.md` — alert timestamp matches)
- At least 8 Pilot Bank A compliance reports were affected (confirmed by `tickets.json` T-2003 and `customer-email.txt`)
- The hotfix v2.3.2 at 11:30 restored normal behavior (confirmed by `deployment-log.md`, `system-metrics.txt` — alerts cleared at 11:32, and `tickets.json` — no further tickets after 11:00)
- Alex identified the root cause as a status-ordering bug by 09:50 and confirmed the link to v2.3.1 by 10:30 (confirmed by `team-notes.md`)

## Inferences

- The async completion optimization in v2.3.1 directly caused the race condition. While no single file states this explicitly, the deployment timing + the optimization description + the team-notes analysis + the hotfix reversing the same optimization + the metrics correlation form a coherent chain.
- T-2004 (dashboard displaying wrong status) is a downstream symptom of the same race condition, not an independent bug.
- The canary node smoke tests did not include artifact-completeness verification.

## Unknowns

- **Timing discrepancy in customer report:** The customer email states symptoms began "since around 08:00 this morning," but `system-metrics.txt` shows baseline error rates (0.2/min) until 09:15 and the alert only triggered at 09:28. The source of the 08:00 claim is unknown — it may reference a different issue or a timing confusion by the customer.
- **Total number of affected tasks:** Only Pilot Bank A's numbers (8 reports) are confirmed. The total number of tasks affected across all customers is unknown.
- **Whether empty reports were processed by downstream systems:** Unknown — no data on whether any downstream audit or compliance pipeline consumed the empty reports before detection.
- **Root cause of the write confirmation failure:** The exact mechanism by which the async write failed is not documented — data is missing from auth-service write logs.

## Recommended Actions

1. **Notify Pilot Bank A with incident timeline and impact assessment.** Detail which reports were affected, confirm no data exposure, and assess SLA breach status. Provides the immediate regulatory response the customer requested.

2. **Update canary deployment smoke tests to verify artifact completeness.** Add a check that task output artifacts are non-empty after status transitions to "completed." Prevents this class of race condition from reaching production again.

3. **Add write-acknowledgement monitoring and alerting.** Instrument the write-confirmation path so that write failures produce alerts independently of task completion metrics. Ensures future regressions are detected regardless of status transition logic.

## Confidence & Information Gaps

**Information gaps:**
- Auth-service write logs for the incident window — would confirm the exact failure path for each affected task
- Canary node smoke test specification — would reveal why the bug passed verification
- Cross-customer impact data — would show whether Pilot Bank A was uniquely affected or part of a broader pattern

**Confidence: Medium.** The timing correlation between v2.3.1 deployment and the error spike is strong and corroborated by three independent sources (deployment log, system metrics, team notes). The hotfix explicitly names and fixes the same mechanism. However, we lack auth-service write logs that would confirm the exact failure path for individual tasks, which prevents a High confidence rating.
