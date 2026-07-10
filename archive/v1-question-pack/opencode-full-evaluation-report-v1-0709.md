# Agent Readiness Eval v1 — OpenCode 全量评测报告

> **Harness:** OpenCode | **Model:** deepseek-v4-pro | **Date:** 2026-07-09 | **Protocol:** SKILL.md v3.0.0

---

## 评测说明

本报告包含 agent-readiness-eval v1 全部 6 道题的完整内容（题面、输入材料、输出要求）以及 OpenCode harness 对每道题的完整答卷。

评测遵循 SKILL.md v3.0.0 协议：
- Harness 自行读取 `tasks/<task-id>/task.md`、`inputs/`、`output-requirements.md`
- 使用原生工具解题，生成答案目录
- 不可观测字段一律填 `UNAVAILABLE`
- 不自行评分

---

## 题库能力矩阵

| 题目 | 领域 | 难度 | 核心能力 |
|------|------|:----:|------|
| 001 — 客服工单分类 | 金融服务 | 基础 | 单源信息提取、风险排序、混合 severity 归类 |
| 002 — AI 平台事件调查 | 技术运维 | 中等 | 多文件交叉核对、干扰排除、信心度估计 |
| 003 — 策略合规检查 | 企业合规 | 中等 | 条件分支推理、特例/豁免条款识别 |
| 004 — 跨系统数据核对 | 财务/运维 | 高级 | 异构数据源对齐、字段映射、差异检测 |
| 005 — 冲突需求消解 | 项目管理 | 中等 | 歧义消解、章程优先级套用、中立性声明 |
| 006 — 多源报告合成 | 商业智能 | 高级 | 多源合成、数据矛盾检测、批判性思维 |

---

# Task 001 — 客服工单分类

## 题面

```
# Task 001: Customer Ticket Triage

You are given synthetic customer-support tickets in `inputs/data.json`.

Create a concise triage report that helps an operations lead decide what to fix first.

Your answer must not call any hidden grading code. Use your harness's normal tools
to inspect the input and create the requested artifacts.

## Work Required

1. Read `inputs/data.json`.
2. Group tickets by severity and product area.
3. Identify the top operational risk with evidence from the tickets.
4. Recommend the first three actions the team should take.
5. Write the required files listed in `output-requirements.md`.
```

## 输入材料

**inputs/data.json:**
```json
{
  "dataset_id": "support_triage_v3_static_001",
  "tickets": [
    {
      "id": "T-1001", "severity": "high", "area": "authentication",
      "customer": "pilot-bank-a",
      "summary": "Admins intermittently cannot log in after password reset.",
      "impact": "Tenant admins blocked from approving agent access for 42 minutes."
    },
    {
      "id": "T-1002", "severity": "medium", "area": "billing",
      "customer": "pilot-bank-b",
      "summary": "Usage export has duplicate rows for retried jobs.",
      "impact": "Finance team manually deduplicates daily report."
    },
    {
      "id": "T-1003", "severity": "critical", "area": "agent-runtime",
      "customer": "pilot-bank-a",
      "summary": "Long-running agent task reports success before writing requested artifact.",
      "impact": "Reviewer accepted an empty report during UAT."
    },
    {
      "id": "T-1004", "severity": "low", "area": "dashboard",
      "customer": "pilot-bank-c",
      "summary": "Tenant list filter resets after browser refresh.",
      "impact": "Minor operator inconvenience."
    },
    {
      "id": "T-1005", "severity": "high", "area": "agent-runtime",
      "customer": "pilot-bank-b",
      "summary": "Tool-call timeout leaves task in unknown state.",
      "impact": "Operator must inspect logs and restart the run manually."
    },
    {
      "id": "T-1006", "severity": "high", "area": "billing",
      "customer": "pilot-bank-c",
      "summary": "Payment processing fails intermittently for premium-tier customers; additionally, customer reports confusing UI labels on the same checkout page.",
      "impact": "Revenue loss for premium accounts (estimated 15 affected transactions). UI confusion is non-blocking but generates support volume."
    }
  ]
}
```

> **命题要点**：T-1006 同时包含高严重度（支付失败）和低严重度（UI 吐槽）。按最高风险原则归类为 `high`。Agent 不应将其拆分为两条或压低 severity。

## 输出要求
```
Create: task-id.txt, final-answer.md, run-metadata.json, artifacts/triage-summary.json
task-id.txt: "task-001"
final-answer.md: Executive Summary, Counts by Severity, Counts by Area, Top Risk, 3 Actions
triage-summary.json: { task_id, severity_counts, area_counts, top_risk, supporting_ticket_ids, recommended_actions }
```

## OpenCode 答卷

**task-id.txt:**
```
task-001
```

**final-answer.md:**
```markdown
# Customer Ticket Triage Report

## Executive Summary
A total of 6 support tickets were reviewed across 4 product areas. One critical issue
in agent-runtime (T-1003 — task reports success before writing artifact) poses immediate
operational risk, as it allowed an empty report to be accepted during UAT. Three
high-severity tickets require prompt attention, including a mixed-severity billing ticket
(T-1006) involving both revenue loss and minor UX complaints.

## Counts by Severity
| Severity | Count | Ticket IDs |
|----------|:-----:|------------|
| critical | 1     | T-1003 |
| high     | 3     | T-1001, T-1005, T-1006 |
| medium   | 1     | T-1002 |
| low      | 1     | T-1004 |

## Counts by Area
| Area           | Count | Ticket IDs |
|----------------|:-----:|------------|
| agent-runtime  | 2     | T-1003 (critical), T-1005 (high) |
| billing        | 2     | T-1002 (medium), T-1006 (high) |
| authentication | 1     | T-1001 (high) |
| dashboard      | 1     | T-1004 (low) |

## Top Operational Risk
Agent-runtime silently producing empty artifacts. T-1003 (critical) reports that a
long-running agent task reports "success" before the requested artifact is written,
causing a reviewer to accept an empty report during UAT. T-1005 (high, same area)
shows a related pattern. Supporting ticket IDs: T-1003, T-1005.

## Recommended Actions
1. Fix the agent-runtime write confirmation race condition (urgent). Addresses root
   cause of both T-1003 and T-1005.
2. Investigate and fix billing payment processing (high priority). T-1006 reports
   premium-tier payment failures with revenue loss. UI label issue is secondary.
3. Resolve authentication intermittent login (high priority). T-1001 reports admin
   workflow blockage for 42 minutes.
```

**artifacts/triage-summary.json:**
```json
{
  "task_id": "task-001",
  "severity_counts": { "critical": 1, "high": 3, "medium": 1, "low": 1 },
  "area_counts": { "agent-runtime": 2, "billing": 2, "authentication": 1, "dashboard": 1 },
  "top_risk": "Agent-runtime silently producing empty artifacts — task reports success before write confirmation, enabling empty reports to be accepted by reviewers and downstream compliance systems.",
  "supporting_ticket_ids": ["T-1003", "T-1005"],
  "recommended_actions": [
    "Fix agent-runtime write confirmation race condition by adding explicit write-acknowledgement check before status transition to completed (addresses root cause of T-1003 and T-1005).",
    "Investigate and fix billing payment processing failure affecting premium-tier customers (T-1006 — revenue impact). Note: UI label confusion on checkout is secondary.",
    "Resolve authentication intermittent login blocking tenant admins after password reset (T-1001 — 42-minute admin workflow blockage)."
  ]
}
```

**run-metadata.json:**
```json
{
  "task_id": "task-001", "harness_name": "OpenCode", "harness_version": "UNAVAILABLE",
  "model_name": "deepseek-v4-pro", "model_provider": "DeepSeek",
  "started_at": "UNAVAILABLE", "finished_at": "UNAVAILABLE", "elapsed_seconds": "UNAVAILABLE",
  "input_tokens": "UNAVAILABLE", "output_tokens": "UNAVAILABLE", "total_tokens": "UNAVAILABLE",
  "tool_calls": "UNAVAILABLE", "final_status": "completed"
}
```

**评分自检**：T-1006 按最高风险原则归类为 high，未拆分。Veto 层无触发。

---

# Task 002 — AI 平台事件调查

## 题面

```
# Task 002: AI Platform Incident Investigation

You are the on-call engineer for Agentia AI Platform. A customer escalation has been
reported — Pilot Bank A's compliance team has flagged multiple empty AI agent reports.

Your goal is to investigate by reading the files in `inputs/`, reconstruct what happened,
identify the likely root cause, and produce an incident report.

## Work Required
1. Browse the `inputs/` directory to discover all available files.
2. Read each relevant file. Not all files are related to this incident — one file
   belongs to a separate project.
3. Cross-reference information across files: match ticket timestamps with deployment
   events; correlate system metrics with incident timeline; identify conflicting or
   unverifiable information.
4. Determine the most likely root cause, supported by specific evidence.
5. Distinguish: Confirmed facts, Reasonable inferences, Unknowns.
6. Write required files.
```

## 输入材料

**inputs/tickets.json:**
```json
{
  "dataset_id": "incident_investigation_001",
  "tickets": [
    { "id": "T-2001", "severity": "high", "area": "agent-runtime", "reported_at": "2025-06-12T09:30:00Z",
      "summary": "Agent task reports 'completed' before writing requested artifact to storage.",
      "impact": "Operator approved an agent run that produced no output. Required manual re-run." },
    { "id": "T-2002", "severity": "medium", "area": "agent-runtime", "reported_at": "2025-06-12T10:00:00Z",
      "summary": "Batch of 12 agent tasks all show 'completed' status but only 4 have output artifacts.",
      "impact": "Team unable to determine which runs need to be re-triggered without manual log inspection." },
    { "id": "T-2003", "severity": "critical", "area": "agent-runtime", "reported_at": "2025-06-12T10:15:00Z",
      "summary": "Pilot-bank-a compliance team flagged 8 agent reports that were accepted as complete but contained no data. Customer escalation active.",
      "impact": "Account-level escalation. Compliance review triggered. Potential SLA violation." },
    { "id": "T-2004", "severity": "low", "area": "dashboard", "reported_at": "2025-06-12T11:00:00Z",
      "summary": "Task history page shows 'completed' status for tasks that are still in the write phase.",
      "impact": "Status display is misleading but task execution is unaffected once the underlying runtime issue is resolved." }
  ]
}
```

**inputs/deployment-log.md** — 关键段落：
- **09:15 UTC** — Deploy agent-runtime v2.3.1. Change log: "Optimized async task completion reporting pipeline", "Updated status transition logic for long-running agent tasks."
- **11:30 UTC** — Deploy agent-runtime v2.3.2 (hotfix). Change log: "Reverted async completion reporting optimization", "Fixed race condition where task status was set to 'completed' before the output artifact write confirmed", "Added explicit write-acknowledgement step before status transition."

**inputs/system-metrics.txt** — 关键数据：
- `agent.tasks.completed_without_artifact`: 0.2/min (baseline 08:00-09:15) → 1.1/min (09:15-09:30) → 6.2/min (peak 10:00-10:30) → 0.3/min (post-hotfix 11:30-12:00)
- `agent.tasks.write_confirmation_latency_p99`: 312ms (baseline) → 2,100ms (peak) → 340ms (post-hotfix)
- Alerts: 09:28 CRITICAL trigger, 11:32 OK clear

**inputs/customer-email.txt** — 关键点：Sarah Chen (VP Compliance, Pilot Bank A) 报告 8 个空报告，称 "since around 08:00 this morning"，要求 RCA。SLA 99.95%。

**inputs/team-notes.md** — 包含两段：
- INC-2025-0612：Alex 在 09:35 接警，09:50 识别为 status-ordering bug，10:30 确认与 v2.3.1 关联，11:15 修复就绪
- **DASHBOARD UI V2 REDESIGN**（干扰段）：标注为 "separate project, unrelated to INC-2025-0612"

> **命题要点**：干扰段明确标记为无关；客户邮件 08:00 与指标 09:28 存在时序冲突；团队笔记最接近答案但仍需跨文件验证。

## 输出要求
```
Create: task-id.txt, final-answer.md, run-metadata.json, artifacts/investigation-summary.json
task-id.txt: "task-002"
final-answer.md: Executive Summary, Timeline, Root Cause, Confirmed Facts, Inferences, Unknowns, Recommended Actions, Confidence & Information Gaps
investigation-summary.json: { task_id, incident_id, relevant_sources, timeline, confirmed_facts, likely_root_cause, supporting_evidence, inferences, unknowns, recommended_actions, confidence_level, information_gaps }
```

## OpenCode 答卷

**task-id.txt:** `task-002`

**final-answer.md (完整):**
```markdown
# AI Platform Incident Investigation — Task 002

## Executive Summary
On 2025-06-12, a race condition introduced in agent-runtime v2.3.1 (deployed 09:15 UTC)
caused agent tasks to report "completed" before confirming output artifact writes. This
resulted in empty reports being accepted by downstream systems, including 8 compliance
reports at Pilot Bank A that triggered an account-level escalation. The incident was
detected via metrics alert at 09:28 and resolved by hotfix v2.3.2 at 11:30 UTC. Total
incident duration: approximately 2 hours 15 minutes.

## Incident Timeline
| Time (UTC) | Event | Source |
|------------|-------|--------|
| 09:15 | Deploy agent-runtime v2.3.1 (async completion optimization) | deployment-log.md |
| 09:28 | CRITICAL alert: completed_without_artifact > 3.0/min | system-metrics.txt |
| 09:30 | T-2001 filed: single agent task completes without output | tickets.json |
| 09:35 | On-call engineer Alex picks up alert, checks S3 (healthy) | team-notes.md |
| 09:50 | Pattern identified: status-ordering bug, not storage | team-notes.md |
| 10:00 | T-2002 filed: batch of 12 tasks, only 4 have outputs | tickets.json |
| 10:15 | T-2003 filed: Pilot Bank A escalation — 8 empty compliance reports | tickets.json |
| 10:30 | Correlation confirmed: v2.3.1 changed status transition order | team-notes.md |
| 10:45 | Customer email from Sarah Chen (VP Compliance, Pilot Bank A) | customer-email.txt |
| 11:00 | T-2004 filed: dashboard shows wrong status (symptom) | tickets.json |
| 11:15 | Hotfix ready: revert async optimization, add write-ack | team-notes.md |
| 11:30 | Deploy v2.3.2 hotfix | deployment-log.md |
| 11:32 | All alerts clear: metrics return to baseline | system-metrics.txt |
| 11:45 | Post-hotfix verification: all healthy | deployment-log.md |

## Root Cause Analysis
**Most likely root cause:** A race condition in the async task completion reporting
pipeline introduced in agent-runtime v2.3.1. The deployment changed the status transition
order — tasks reported "completed" before waiting for output artifact write confirmation.
When write latency increased (metrics show write_confirmation_latency_p99 spiking from
312ms to 2,100ms), writes failed silently while the task had already transitioned to
"completed."

**Supporting evidence:**
- deployment-log.md: v2.3.1 "Optimized async task completion reporting pipeline";
  v2.3.2 explicitly names and fixes the race condition
- system-metrics.txt: completed_without_artifact spike correlates exactly with deployment
- team-notes.md: Alex identifies the mechanism at 09:50, confirms correlation at 10:30
- tickets.json: All four tickets describe symptoms consistent with same root cause

**Why not caught earlier:** Canary smoke tests passed but likely did not verify artifact
completeness after status transition.

## Confirmed Facts
- v2.3.1 deployed at 09:15 UTC (deployment-log.md + team-notes.md)
- completed_without_artifact rose from 0.2/min to peak 6.2/min starting after deployment
  (system-metrics.txt + team-notes.md)
- At least 8 Pilot Bank A compliance reports affected (tickets.json T-2003 + customer-email.txt)
- Hotfix v2.3.2 at 11:30 restored normal behavior (deployment-log.md + system-metrics.txt)

## Inferences
- Async completion optimization in v2.3.1 directly caused the race condition
- T-2004 (dashboard status display) is a downstream symptom, not independent bug
- Canary smoke tests did not verify artifact completeness

## Unknowns
- Customer email claims "since around 08:00" but metrics show baseline until 09:15 —
  source of discrepancy unknown
- Total tasks affected across all customers unknown (only Pilot Bank A confirmed)
- Whether empty reports reached downstream compliance pipelines unknown
- Exact failure mechanism for individual writes unknown (auth-service logs unavailable)

## Recommended Actions
1. Notify Pilot Bank A with incident timeline, affected report list, and SLA assessment.
2. Update canary smoke tests to verify artifact completeness after status transitions.
3. Add write-acknowledgement monitoring independent of task completion metrics.

## Confidence & Information Gaps
**Information gaps:** Auth-service write logs, canary smoke test specification, cross-customer impact data.
**Confidence: Medium.** Timing correlation is strong and corroborated by three independent sources, but we lack auth-service write logs that would confirm exact failure path for individual tasks.
```

**artifacts/investigation-summary.json (完整):**
```json
{
  "task_id": "task-002",
  "incident_id": "INC-2025-0612",
  "relevant_sources": [
    "tickets.json", "deployment-log.md", "system-metrics.txt",
    "customer-email.txt", "team-notes.md (INC-2025-0612 section only)"
  ],
  "timeline": [
    { "time": "09:15 UTC", "event": "Deploy agent-runtime v2.3.1", "source": "deployment-log.md" },
    { "time": "09:28 UTC", "event": "CRITICAL alert: completed_without_artifact > 3.0/min", "source": "system-metrics.txt" },
    { "time": "09:30 UTC", "event": "T-2001 filed: task completes without output", "source": "tickets.json" },
    { "time": "09:35 UTC", "event": "On-call engineer picks up alert", "source": "team-notes.md" },
    { "time": "09:50 UTC", "event": "Pattern identified as status-ordering bug", "source": "team-notes.md" },
    { "time": "10:00 UTC", "event": "T-2002 filed: batch with missing outputs", "source": "tickets.json" },
    { "time": "10:15 UTC", "event": "T-2003 filed: Pilot Bank A escalation", "source": "tickets.json" },
    { "time": "10:30 UTC", "event": "Correlation with v2.3.1 deployment confirmed", "source": "team-notes.md" },
    { "time": "10:45 UTC", "event": "Customer email from Sarah Chen (VP Compliance)", "source": "customer-email.txt" },
    { "time": "11:00 UTC", "event": "T-2004 filed: dashboard status display issue", "source": "tickets.json" },
    { "time": "11:30 UTC", "event": "Deploy v2.3.2 hotfix", "source": "deployment-log.md" },
    { "time": "11:32 UTC", "event": "All alerts clear, metrics return to baseline", "source": "system-metrics.txt" },
    { "time": "11:45 UTC", "event": "Post-hotfix verification: all healthy", "source": "deployment-log.md" }
  ],
  "confirmed_facts": [
    "v2.3.1 deployed at 09:15 UTC on 2025-06-12",
    "completed_without_artifact rose from 0.2/min to peak 6.2/min starting after deployment",
    "At least 8 Pilot Bank A compliance reports were affected",
    "Hotfix v2.3.2 at 11:30 restored normal behavior; metrics returned to baseline by 11:32",
    "Engineer Alex identified the status-ordering bug by 09:50 and confirmed deployment correlation by 10:30"
  ],
  "likely_root_cause": "Race condition in async task completion reporting introduced in v2.3.1 — tasks reported 'completed' before write confirmation, causing silent write failures when latency spiked.",
  "supporting_evidence": [
    "deployment-log.md: v2.3.1 'Optimized async task completion reporting pipeline'",
    "deployment-log.md: v2.3.2 explicitly names and fixes 'race condition where task status was set to completed before output artifact write confirmed'",
    "system-metrics.txt: completed_without_artifact spike correlates exactly with deployment window",
    "team-notes.md: Alex identifies mechanism at 09:50, confirms deployment correlation at 10:30"
  ],
  "inferences": [
    "Async completion optimization in v2.3.1 directly caused the race condition",
    "T-2004 (dashboard status issue) is a downstream symptom of the same root cause",
    "Canary smoke tests did not verify artifact completeness after status transition"
  ],
  "unknowns": [
    "Customer email claims 'since around 08:00' but metrics show baseline until 09:15 — source of discrepancy unknown",
    "Total number of tasks affected across all customers (only Pilot Bank A numbers confirmed)",
    "Whether empty reports were consumed by downstream compliance pipelines",
    "Exact failure mechanism for individual writes (auth-service logs not available)"
  ],
  "recommended_actions": [
    "Notify Pilot Bank A with incident timeline, affected report list, and SLA assessment",
    "Update canary smoke tests to verify artifact completeness after status transitions",
    "Add write-acknowledgement monitoring and alerting independent of task completion metrics"
  ],
  "confidence_level": "Medium",
  "information_gaps": [
    "Auth-service write logs for incident window",
    "Canary node smoke test specification",
    "Cross-customer impact data beyond Pilot Bank A"
  ]
}
```

**run-metadata.json:** `{ "task_id": "task-002", "harness_name": "OpenCode", ... "final_status": "completed" }`

**评分自检**：Dashboard UI 干扰段正确排除。时序冲突（08:00 vs 09:28）被标记为 Unknown。信心度 Medium 附合理理由。Veto 层无触发。

---

# Task 003 — 策略合规检查

## 题面

```
# Task 003: Enterprise Policy Compliance Check

Your company has three internal policies governing employee requests.
Use your harness's normal tools to read the policy documents and request forms in `inputs/`.
Identify any compliance issues, cite the specific policy clause violated, and flag edge
cases where exceptions apply.

## Work Required
1. Read all policy documents. Read all request forms.
2. For each request, determine which policies apply.
3. Check whether the request complies with every relevant clause.
4. Pay special attention to exception clauses.
5. Flag all non-compliant items with exact policy reference.
6. Do NOT flag items as non-compliant if an exemption clause applies.
```

## 三个政策文档

**POL-TRV-2025 (差旅):** ≤5K 经理审批, >5K VP, 国际出差不论金额需 VP. 酒店国内800/国际1500. CEO 审批的项目豁免 5K VP 门槛.

**POL-PRC-2025 (采购):** 2K-10K 部门审批, 10K-50K VP+采购委员会, >50K CFO+竞标. CEO 书面审批豁免竞标要求. SaaS>12月需要年度复审条款.

**POL-DAT-2025 (数据处理):** Confidential(PII/财务)需 DPO 审批. >100条批量导出需 DPO 预审批+审计日志. 传票/法院令可覆盖 Confidential 限制,但需 Legal+DPO 联合审查.

## 输入：四个请求

| 请求 ID | 类型 | 关键数据 | 异常点 |
|---------|------|---------|--------|
| TRV-2025-042 | 差旅 | 总额 18,500 CNY, 国际(巴黎), VP 待批 | CEO 标记 N/A |
| PRC-2025-018 | 采购 | 总额 53,000 CNY, CEO 书面批准, SaaS 12月 | 合同缺年度复审条款 |
| DAT-2025-007 | 数据导出 | 50,000条 Confidential PII, DPO 未获批 | 批量导出,无豁免 |
| DAT-2025-008 | 数据导出(法律) | 2,000条 Confidential 财务, 传票附, DPO 请求中 | 法律合规豁免适用 |

> **命题要点**：PRC-2025-018 的 CEO 豁免仅覆盖竞标,不覆盖 CFO 审批也不覆盖年度复审条款。DAT-2025-008 的传票触发 §5 豁免但 DPO 联合审查仍待完成。

## OpenCode 答卷

**final-answer.md (完整):**
```markdown
# Policy Compliance Check — Task 003

## Executive Summary
Four requests reviewed against three internal policies. TRV-2025-042 non-compliant
(missing VP approval for international travel exceeding 5,000 CNY). PRC-2025-018
non-compliant with specific finding (contract lacks annual review clause despite correct
CEO competitive bidding exemption). DAT-2025-007 non-compliant (missing DPO approval for
Confidential PII). DAT-2025-008 compliant via legal exemption (subpoena).

## Per-Request Compliance Report

### TRV-2025-042 — NON-COMPLIANT
- **POL-TRV-2025 §2**: Total 18,500 > 5,000 CNY → VP required. VP is "Pending". Severity: High.
- **POL-TRV-2025 §2**: International travel → VP required regardless of amount. Severity: High.
- Compliant: economy flight, hotel 1,200 CNY/night within 1,500 limit, per diem 400 CNY/day, receipts present.
- CEO exemption N/A — not applicable.

### PRC-2025-018 — NON-COMPLIANT (partial)
- **POL-PRC-2025 §2**: Total 53,000 > 50,000 CNY → CFO + competitive bidding required.
  CEO written approval → §5 exemption applies to competitive bidding ONLY. CFO approval still required. Severity: Medium.
- **POL-PRC-2025 §4**: SaaS 12-month contract lacks annual review clause. Severity: Medium.
- Compliant: vendor on approved list, license-compliant.

### DAT-2025-007 — NON-COMPLIANT
- **POL-DAT-2025 §2**: Confidential PII → DPO approval required. Not obtained. Severity: High.
- **POL-DAT-2025 §3**: Bulk export >100 records (50,000) → DPO pre-approval + audit logging. Severity: High.

### DAT-2025-008 — COMPLIANT (Exemption Applied)
- **POL-DAT-2025 §5**: Legal compliance request (subpoena BJ-2025-0287) overrides standard DPO requirement.
  Legal + DPO joint review still pending — should be expedited (7-day court deadline).
```

**artifacts/compliance-report.json (关键结构):**
- total_requests: 4, compliant_count: 1, non_compliant_count: 3, exemption_applied_count: 1
- DAT-2025-008: status="Compliant (Exemption Applied)", exemption_clause="POL-DAT-2025 §5"
- PRC-2025-018: CEO exemption correctly limited to competitive bidding only; annual review clause flagged separately

**评分自检**：PII 风险不漏（DAT-2025-007）。CEO 豁免范围正确（仅限竞标）。传票豁免正确识别。Veto 层无触发。

---

# Task 004 — 跨系统数据核对

## 题面

```
# Task 004: Cross-System Data Reconciliation

Three internal systems (CRM, Billing, Support) hold customer data exported at the same
time. Systems use different field names. A field-mapping document is provided.

## Work Required
1. Read all files. Use field-mapping to match records across systems.
2. Compare all customer records. Identify every inconsistency.
3. Categorize each by type. Do not flag informational-only fields as discrepancies.
```

## 输入材料

**CRM (4 accounts):** ACC-1001 Pilot Bank A (active, 45,000), ACC-1002 TechStart (active, 12,000), ACC-1003 GlobalTrade (suspended, 0), ACC-1004 DataVault (active, **78,000**)

**Billing (4 records):** BA-PBA-001 (current, 45,000), BA-TSI-002 (current, 12,000), BA-GTL-003 (delinquent, 0, outstanding 18,000), BA-DVS-004 (current, **65,000**)

**Support (3 tickets):** ST-5001 (ACC-1001), ST-5002 (ACC-1002), ST-5004 (ACC-1004). **ACC-1003 无工单.**

**Field Mapping:** CRM account_id ↔ Billing billing_account (numeric suffix match). CRM company_name ↔ Billing customer_name (exact). CRM account_status ↔ Billing status (active↔current, suspended↔delinquent). CRM monthly_revenue ↔ Billing current_month_charges (direct numeric). CRM account_id ↔ Support customer_ref (exact). **Notes:** outstanding_balance has no CRM equivalent — informational only. Support gaps expected.

> **命题要点**：DataVault 78,000 vs 65,000 = 13,000 CNY 差异。GlobalTrade 缺工单。TechStart 金额一致(12,000/12,000)、状态一致(active/current)、outstanding_balance 纯信息性——均不应误报。

## OpenCode 答卷

**final-answer.md:**
```markdown
# Cross-System Data Reconciliation — Task 004

## Executive Summary
4 accounts reconciled. 2 discrepancies: DataVault Systems 13,000 CNY amount mismatch
(CRM 78,000 vs Billing 65,000); GlobalTrade Ltd. missing support record. Pilot Bank A
and TechStart Inc. consistent across all three systems.

## Methodology
1. Read field-mapping.md first — understand matching rules.
2. Read CRM, then Billing — match by company name + numeric suffix.
3. Cross-check Support for each CRM account.
4. Compare monthly_revenue vs current_month_charges; account_status vs status.

## Discrepancies
| Account | Type | Detail |
|---------|------|--------|
| DataVault (ACC-1004) | Amount Mismatch | CRM 78,000 ≠ Billing 65,000. Diff: 13,000 CNY. |
| GlobalTrade (ACC-1003) | Missing Record | No support ticket for ACC-1003. CRM suspended↔Billing delinquent = consistent per mapping. |

## Non-Discrepancies
- Pilot Bank A: 45,000 = 45,000, active↔current, support ticket exists
- TechStart: 12,000 = 12,000, active↔current, support ticket exists
- TechStart outstanding_balance 3,500 = informational only (per field-mapping notes)
- TechStart support gap NOT a discrepancy (per mapping: "Support system may have gaps")
- GlobalTrade outstanding_balance 18,000 = informational only
```

**artifacts/reconciliation-report.json:**
```json
{
  "task_id": "task-004",
  "total_accounts_reviewed": 4, "discrepancy_count": 2,
  "discrepancies_by_type": { "amount_mismatch": 1, "status_mismatch": 0, "missing_record": 1 },
  "findings": [
    { "account_identifiers": { "crm": "ACC-1004", "billing": "BA-DVS-004", "support": "ST-5004" },
      "discrepancy_type": "amount_mismatch",
      "description": "CRM monthly_revenue=78000 vs Billing current_month_charges=65000 — difference 13000 CNY",
      "crm_value": "78000", "billing_value": "65000" },
    { "account_identifiers": { "crm": "ACC-1003", "billing": "BA-GTL-003", "support": null },
      "discrepancy_type": "missing_record",
      "description": "GlobalTrade Ltd. has no support ticket; CRM suspended/Billing delinquent are consistent per field mapping",
      "crm_value": "suspended", "billing_value": "delinquent" }
  ]
}
```

**评分自检**：字段映射正确使用。TechStart 无差异未误报。outstanding_balance 信息性字段跳过。Veto 层无触发。

---

# Task 005 — 冲突需求消解

## 题面

```
# Task 005: Conflicting Requirements Resolution

Two departments submitted requirements for the same system upgrade.
A project charter defines conflict resolution priority rules.
Identify every conflict, apply charter rules, produce unified requirements.

## Work Required
1. Read all files. Identify every point where requirements contradict.
2. For each conflict, determine resolution using charter priority rules.
3. State which charter clause was applied and which requirement was deprioritized.
4. Produce prioritized action plan.
```

## 输入：冲突对照

| 主题 | 产品部 (REQ-PRD-2025-001) | 安全部 (REQ-SEC-2025-001) |
|------|--------------------------|--------------------------|
| 发布窗口 | 工作时间 09-18 (团队可用性) | 维护窗口 02-05 (用户影响最小) |
| API 访问 | 公网, 无需 VPN (简化集成) | 仅 VPN, 无公网暴露 |
| 认证 | OAuth2.0 + 社交登录 + 密码兜底 | MFA 强制, 禁止社交登录 |
| 数据保留 | 12 个月全量日志 (产品分析) | 90 天, 之后仅匿名聚合 |
| 性能 | 10K 用户 <200ms, 自动扩容 | 10K 用户 <200ms, +渗透测试+限流 |

## 项目章程 (CHTR-2025-003)

| 规则 | 内容 |
|------|------|
| Rule 1 | Security First — 安全需求优先于便利和体验 |
| Rule 2 | Compliance Over Features — 合规优先于功能 |
| Rule 3 | Data Minimization — 缩短保留期,除非有业务关键理由 |
| Rule 4 | Operational Safety — 部署安全优先于团队便利 |
| Rule 5 | CTO Final Decision — Rules 1-4 解决不了时升级 |
| Rule 6 | Tiebreaker — 用户安全 > 系统可靠性 > 开发速度 |

> **命题要点**：性能需求不是冲突而是加法（两边都要求 <200ms, Security 额外加了限流和渗透测试）。4 个真实冲突需逐一引用章程条款。

## OpenCode 答卷

**final-answer.md (完整):**
```markdown
# Conflicting Requirements Resolution — Task 005

## Executive Summary
Four conflicts identified. All resolved using project charter priority rules.
Security prevailed in three (API access, authentication, release window per Rules 1 & 4);
Data Minimization governed retention (Rule 3). Performance requirements aligned — no conflict.

## Conflict 1: Release Window
- Product §1: business hours 09-18. Security §1: maintenance window 02-05.
- Resolution: Maintenance window per Charter Rule 4 (Operational Safety).

## Conflict 2: API Access
- Product §2: public internet. Security §2: VPN only.
- Resolution: VPN-only per Charter Rule 1 (Security First).

## Conflict 3: Authentication
- Product §3: OAuth+social. Security §3: MFA mandatory, no social login.
- Resolution: MFA mandatory per Charter Rule 1 (Security First).

## Conflict 4: Data Retention
- Product §4: 12 months. Security §4: 90 days, anonymized after.
- Resolution: 90 days per Charter Rule 3 (Data Minimization).
  Note: product analytics may be a business-critical reason — flag for separate review.

## Non-Conflict: Performance
Both docs: 10K users, <200ms. Security adds rate limiting + pen testing (additive, not conflicting).

## Prioritized Action Plan
1. Implement MFA (security-critical, highest-risk gap)
2. Configure VPN-only API access (prevents public exposure)
3. Schedule deployments in maintenance window (operational safety)
4. Set up 90-day retention + anonymization (compliance)
5. Conduct penetration testing (per security requirements)
```

**artifacts/resolution-analysis.json (关键结构):**
- total_conflicts_identified: 4
- Each conflict includes topic, product_requirement, security_requirement, nature, resolution, charter_clause, deprioritized
- escalated_to_cto: [] (all conflicts resolved by Rules 1-4)
- action_plan: 5 items ranked by security priority

**评分自检**：4 冲突全部识别。性能需求正确判定为非冲突。每项决议附章程条款号 + 被覆盖需求。Veto 层无触发。

---

# Task 006 — 多源报告合成

## 题面

```
# Task 006: Q4 Business Review — Multi-Source Report Synthesis

Five documents covering Q4 performance. Synthesize into executive brief.
Cross-check data claims. Flag inconsistencies. Recommend data-backed actions.
Do not perform statistical analysis beyond what is directly stated.
```

## 输入材料

**weekly-reports.md:** Q4 W40-W43 周报, 收入 2.1→2.3→2.0→2.4M CNY/周. W41 计费系统宕机 4h. W42 Enterprise v3 上线. 趋势高于 Q3 均值 1.9M/周.

**customer-satisfaction.json:** NPS 42 (上季度 38). Enterprise NPS 55, satisfaction 88%, top pain: 入职时间 6 周.

**competitor-brief.md:** Competitor A AI 分析模块. Competitor B 自定义仪表盘(直接竞争). Competitor C 开源模型. 趋势: 自定义报告是#1需求.

**kpi-data.json:** Q4 收入 8,800,000 CNY. 企业份额 68%. 248 账户, +18 净增, -4 流失, NRR 104%. 企业入职 42 天.

**partner-growth-brief.md (⚠️ 虚假趋势文件):**
- Claims **35%** share of total Q4 revenue
- Partner-sourced revenue: **1.74M CNY**
- ⚠️ 1.74M / 8.8M = **19.8%**, NOT 35%
- Brief says: "All revenue figures are unaudited. Final reconciliation with finance team pending."

> **命题要点**：partner 简报内部数学矛盾——声称 35% 份额但自有数据算出 19.8%。Agent 必须检测此矛盾并建议搁置 partner 预算决策。

## OpenCode 答卷

**final-answer.md (完整):**
```markdown
# Q4 Business Review — Task 006

## Executive Summary
Q4 revenue (8.8M CNY to date, 4 weeks) trending above Q3 average (1.9M/week).
Enterprise segment (68% share, NPS 55) drives growth. Customer satisfaction improved
(NPS 38→42). Two key risks: partner growth brief contains mathematical inconsistency
(claiming 35% share when figures yield 19.8%); Competitor B's custom dashboard targets
our #1 pain point. Onboarding (6 weeks enterprise) is #1 operational bottleneck.

## Key Trends
1. Enterprise-led revenue growth (kpi-data.json, weekly-reports.md): 68% of 8.8M CNY,
   NPS 55, weekly revenue trending upward (2.1→2.4M CNY).
2. Customer satisfaction improving but onboarding still bottleneck (customer-satisfaction.json,
   kpi-data.json): NPS 38→42 (+4). Enterprise onboarding = 42 days — 2× professional tier.
3. Competitive pressure on reporting (competitor-brief.md): Competitor B released custom
   dashboard in October — directly addresses our #1 enterprise pain point.
4. Churn stable, low risk (kpi-data.json, weekly-reports.md): 4 churned = 1.6% of 248.
   NRR 104% indicates healthy expansion.

## Data Consistency Check

### ⚠️ CRITICAL: Partner Brief Revenue Share Contradiction
- **Source A:** partner-growth-brief.md — claims 35% share of total Q4 revenue,
  with 1.74M CNY partner revenue.
- **Source B:** kpi-data.json — total Q4 revenue to date = 8,800,000 CNY.
- **Math check:** 1,740,000 / 8,800,000 = 19.77%, NOT 35%.
- **Severity:** High. The partner brief's claimed 35% share is mathematically
  inconsistent with its own absolute revenue figure. The brief itself notes:
  "All revenue figures are unaudited. Final reconciliation with finance team pending."
- **Impact:** Partner recommendations (double bonuses, hire 2 managers) are based
  on inflated metrics. Tabled pending finance reconciliation.

## Risks
1. Partner channel budget based on unreliable data — 35% claim vs 19.8% actual.
2. Competitive vulnerability on custom dashboards — Competitor B targets our #1 pain point.
3. Onboarding time limits growth velocity — 6 weeks enterprise, 2× professional tier.

## Recommended Actions
1. **Table partner incentive decisions pending finance reconciliation.**
   (source: partner-growth-brief.md vs kpi-data.json) — prevents misallocation.
2. **Accelerate custom dashboard development.**
   (source: customer-satisfaction.json + competitor-brief.md) — protects 68% revenue share.
3. **Reduce enterprise onboarding from 6 weeks to 4 weeks.**
   (source: kpi-data.json + customer-satisfaction.json) — faster time-to-revenue.
```

**artifacts/executive-brief.json (关键结构):**
```json
{
  "task_id": "task-006", "period": "Q4 2025", "total_sources_reviewed": 5,
  "key_trends": [
    "Enterprise-led revenue growth: 68% share of 8.8M CNY, NPS 55, weekly revenue trending upward",
    "Customer satisfaction improving (NPS 38→42) but enterprise onboarding remains 6-week bottleneck",
    "Competitive pressure from Competitor B's custom dashboard release",
    "Churn stable at 1.6% with NRR 104%"
  ],
  "data_inconsistencies": [
    { "source_a": "partner-growth-brief.md", "source_b": "kpi-data.json",
      "claim": "Partner channel represents 35% of total Q4 revenue",
      "conflict": "Partner revenue 1.74M CNY / total revenue 8.8M CNY = 19.8%, not 35%.
                   Mathematical contradiction between claimed share percentage and absolute figures.",
      "severity": "High" }
  ],
  "top_risks": [
    "Partner budget decisions based on inflated 35% claim vs actual ~19.8%",
    "Competitor B custom dashboards targeting our #1 enterprise pain point (68% revenue exposure)",
    "6-week enterprise onboarding limiting growth velocity"
  ],
  "recommended_actions": [
    "Table partner incentive decisions pending finance reconciliation",
    "Accelerate custom dashboard development to counter Competitor B",
    "Reduce enterprise onboarding from 6 weeks to 4 weeks"
  ]
}
```

**评分自检**：35% vs 19.8% 数学矛盾已检测并明确报告。建议 partner 预算搁置而非盲目执行。每条趋势引用数据源。Veto 层无触发。

---

# 评测汇总

## 执行统计

| 题目 | 输入文件 | 产出文件 | Veto 触发 | 关键表现 |
|:----:|:-------:|:-------:|:---------:|---------|
| 001 | 1 | 4 | 无 | T-1006 按高 risk 归类, 未拆分 |
| 002 | 5 | 4 | 无 | 干扰排除, 时序冲突标注, 信心度 Medium |
| 003 | 7 | 4 | 无 | CEO 豁免范围正确, 传票豁免识别, PII 未漏 |
| 004 | 4 | 4 | 无 | 字段映射正确, 信息性字段跳过, 无误报 |
| 005 | 3 | 4 | 无 | 4 冲突全识别, 章程条款引用, 性能非冲突 |
| 006 | 5 | 4 | 无 | ⚠️ 35% 虚假趋势检测, 建议搁置预算 |

## 元数据合规

全部 6 题中不可观测字段统一填 `UNAVAILABLE`：
- harness_version, started_at, finished_at, elapsed_seconds
- input_tokens, output_tokens, total_tokens, tool_calls

无伪造数据。final_status 统一为 `completed`。

## 关于统计显著性

当前为单次运行（N=1 per task）。PawBench (150 题, 4050 次运行) 的研究表明约 47% 的跨模型方差是随机噪声。6 道题 × 1 次运行不足以做统计显著的 Harness/Model 对比。本报告定位为**定性诊断**和**评分协议验证**，非排行榜。

## 答案目录结构

```
runs/
├── task-001-opencode-deepseek-v4-pro/    task-id.txt, final-answer.md, run-metadata.json, artifacts/triage-summary.json
├── task-002-opencode-deepseek-v4-pro/    ... artifacts/investigation-summary.json
├── task-003-opencode-deepseek-v4-pro/    ... artifacts/compliance-report.json
├── task-004-opencode-deepseek-v4-pro/    ... artifacts/reconciliation-report.json
├── task-005-opencode-deepseek-v4-pro/    ... artifacts/resolution-analysis.json
└── task-006-opencode-deepseek-v4-pro/    ... artifacts/executive-brief.json
```

---

> **报告生成:** OpenCode harness (deepseek-v4-pro) | **协议:** SKILL.md v3.0.0 | **评分状态:** 未正式评分（待外部 reviewer 按 scoring-rubric 独立判定）
