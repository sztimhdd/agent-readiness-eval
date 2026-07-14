# AI Platform Incident Investigation — INC-2025-0612

## Executive Summary

On 2025-06-12 at 09:15 UTC, a deployment of agent-runtime v2.3.1 introduced an async task completion optimization that reordered the status transition lifecycle — tasks were marked "completed" before the artifact write confirmation completed, with no validation that the write actually succeeded. This caused a surge of completed-without-artifact tasks starting at 09:15, peaking between 10:00-10:30 UTC at 6.2/min, directly affecting Pilot Bank A's compliance review agents. At least 8 empty compliance reports were ingested into their downstream audit pipeline before detection. A hotfix (v2.3.2) was deployed at 11:30 UTC, reverting the async optimization and restoring the write-ack-first-then-complete ordering. Error rates returned to baseline by 11:45 UTC.

## Incident Timeline

| Time (UTC) | Event | Source |
|---|---|---|
| 09:15 | agent-runtime v2.3.1 deployed to production (async completion reporting optimization, reduced DB write lock contention, updated status transition logic) | deployment-log.md |
| 09:15 | `completed_without_artifact` metric begins rising (0.2 → 1.1/min) | system-metrics.txt |
| 09:28 | CRITICAL alert: `completed_without_artifact` > 3.0/min; WARN: write_confirmation_latency_p99 > 1000ms | system-metrics.txt |
| 09:35 | On-call engineer Alex picks up alert, initially suspects storage latency | team-notes.md |
| 09:50 | Status-ordering bug identified: tasks transition to "completed" without actual artifact write | team-notes.md |
| 10:00-10:30 | Anomaly peak: 6.2/min completed_without_artifact; 33/min total completions (suspiciously high); write_confirmation_latency_p99 at 2100ms | system-metrics.txt |
| 10:15 | T-2003 filed: Pilot Bank A compliance team flagged 8 empty reports, customer escalation active | tickets.json |
| 10:30 | Engineering confirms correlation with v2.3.1 deployment — "reports complete first, then writes asynchronously with no success check" | team-notes.md |
| 10:45 | Customer escalation email from Sarah Chen (VP Compliance, Pilot Bank A): urgent SLA concern, 8+ empty reports | customer-email.txt |
| 11:00 | Hotfix decision made, v2.3.2 preparation begins | team-notes.md |
| 11:15 | Fix ready: status transition logic changed back to write-ack-first-then-complete | team-notes.md |
| 11:30 | v2.3.2 hotfix deployed to all 8 nodes, reverting async completion changes | deployment-log.md |
| 11:32 | Alerts cleared: `completed_without_artifact` and `write_confirmation_latency_p99` return to baseline | system-metrics.txt |
| 11:45 | Post-hotfix verification: all nodes healthy, three sample agent runs confirmed successful | deployment-log.md |

## Root Cause Analysis

**Most likely root cause**: agent-runtime v2.3.1 introduced a status transition reordering where tasks were marked "completed" before the asynchronous artifact write completed, with no validation that the write actually succeeded.

**Supporting evidence**:
- `deployment-log.md`: v2.3.1 change log explicitly lists "Optimized async task completion reporting pipeline" and "Updated status transition logic for long-running agent tasks"
- `system-metrics.txt`: The `completed_without_artifact` rate starts rising at 09:15 (the exact deployment minute), surges to 6.2/min at peak, then returns to 0.3/min after the 11:30 hotfix — a perfect temporal correlation
- `system-metrics.txt`: `write_confirmation_latency_p99` spikes from 312ms to 2100ms in the same window, indicating the async writes are completing slowly (or failing) after the status transition already fired
- `team-notes.md`: Engineering explicitly diagnosed the ordering bug — "the new optimization reports complete first, then writes asynchronously — but there's no check that the async write actually succeeded"
- `customer-email.txt`: Pilot Bank A confirms the impact — compliance reports showed "completed" but contained no data

**Why the issue was not caught earlier**: The v2.3.1 smoke tests passed on the canary node but did not validate artifact write completion. According to team-notes.md, a future dashboard improvement (DASH-102) plans to only show "completed" after backend confirms write — suggesting this validation gap was already known internally but not yet addressed in the runtime itself.

## Confirmed Facts

- v2.3.1 was deployed at 09:15 UTC on 2025-06-12 (deployment-log.md, system-metrics.txt timing correlation)
- The `completed_without_artifact` anomaly began at 09:15 and subsided after the 11:30 hotfix (system-metrics.txt, team-notes.md)
- The root cause was a status-ordering bug: tasks marked complete before async write confirmation (team-notes.md confirmed this, system-metrics.txt corroborated with latency data)
- v2.3.2 hotfix reverted the async optimization and restored write-ack-first ordering (deployment-log.md + team-notes.md)
- Pilot Bank A was the customer affected, with at least 8 empty compliance reports (customer-email.txt, tickets.json T-2003)
- The incident was resolved and error rates returned to baseline by 11:45 UTC (deployment-log.md, system-metrics.txt)

## Inferences

- The "async completion reporting optimization" in v2.3.1 was designed to improve throughput by not blocking task completion on slow writes, but the implementation lacked a compensating check (retry on write failure, or a "completed_with_data" vs "completed_pending_write" distinction)
- The `write_confirmation_latency_p99` spike from 312ms to 2100ms suggests the async writes were not just slow — some may have been silently failing, corroborated by `completed_without_artifact` reaching 6.2/min
- The suspiciously high total completion rate (33/min vs baseline 24/min) during the anomaly window is consistent with tasks being marked complete prematurely — tasks that would normally be in-progress (waiting for write) were instead counted as completed
- The smoke test for v2.3.1 verified canary health but did not test the artifact write path — the validation gap extended into deployment practices
- This likely constitutes an SLA breach for Pilot Bank A, since 8+ tasks out of their normal volume likely falls below 99.95% reliability, though exact total task count is unknown

## Unknowns

- Whether any customer data was exposed or misrouted as a result of the failed writes (customer-email.txt asks this, no file answers it)
- The total number of affected tasks across all customers (only Pilot Bank A's count is known: 8+ reports; metrics show ~6/min anomaly rate over ~2.25 hours which would be hundreds of tasks)
- Whether the async writes that failed were due to timeouts, resource contention, or outright exceptions (team notes mention "no check that async write actually succeeded" but don't specify the failure mode)
- Exact SLA breach calculation — Pilot Bank A's total task volume on 2025-06-12 is not available
- The customer-email.txt reports symptoms "since around 08:00" but the deployment was at 09:15 — this 75-minute discrepancy is unresolved (possible causes: customer's approximate recollection, unrelated pre-existing issue, or timezone confusion)
- Whether the "4 of 8 nodes rolling update" for v2.3.1 meant some nodes still ran v2.3.0 during the incident window (scope mismatch between deployment and hotfix which was "all 8 nodes")

## Recommended Actions

1. **Immediate: Audit all tasks from the incident window (09:15-11:30 UTC)** — Identify every task that shows "completed" status but has no artifact. Re-run affected tasks and notify impacted customers. Priority: urgent. The metrics indicate potentially hundreds of affected tasks beyond Pilot Bank A's reported 8.

2. **Short-term: Add write-completion gating to the status transition logic** — Before any task can transition to "completed", require a confirmed artifact write. If the v2.3.2 hotfix already restored this, add a post-write audit check that catches zero-byte or missing artifacts. This prevents the same class of bug recurring. Priority: high. The team-notes indicate DASH-102 plans similar validation at the UI layer, but it belongs in the runtime.

3. **Medium-term: Expand canary validation to include end-to-end artifact verification** — The v2.3.1 smoke test passed but did not catch the empty-artifact regression. Canary deployment validation should include a synthetic task that produces a known artifact and confirms its presence and non-zero size before proceeding to the full rollout. Priority: high. The current canary practice has a documented blind spot.

## Confidence and Information Gaps

**Information Gaps**:
- Auth-service or agent-runtime write-side logs — these would confirm whether the async writes were failing (timeout, exception, silent drop) or succeeding but with empty payloads
- Per-customer task completion rates during the incident window — needed to calculate SLA breach for Pilot Bank A and identify other affected customers
- The full list of tasks affected — metrics show aggregate anomaly rates but not individual task IDs
- Post-mortem on why the async optimization was designed without a success check — process improvement opportunity
- The discrepancy between customer's "since 08:00" timing and the 09:15 deployment — agent logs or task start timestamps would clarify

**Confidence: High**. The temporal correlation between the 09:15 deployment and the anomaly onset is precise to the minute in system-metrics.txt. The engineering diagnosis in team-notes.md names the exact mechanism (status transition ordering bug, no write success check). The hotfix confirms the root cause by reverting the exact change and resolving the issue. The customer impact is corroborated by both customer-email.txt and tickets.json T-2003. Four independent sources (deployment-log, system-metrics, team-notes, customer-email) converge on the same conclusion. The only gap is the precise failure mode of the async writes (timeout vs exception vs silent drop), which would require write-side logs not present in the provided files.
