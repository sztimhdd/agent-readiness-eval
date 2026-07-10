# Agent Readiness Eval v1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the full v1 benchmark: 6 tasks across 5 enterprise domains with veto-layer scoring.

**Architecture:** Content-only question pack. Each task is `task.md` + `inputs/` + `output-requirements.md` + `evaluator-notes/`. No code beyond contract tests.

**Tech Stack:** Python 3 stdlib (unittest, json, pathlib) for tests. All task content in Markdown, JSON, and plain text.

## Global Constraints

- No packaged execution engine, grading engine, child-agent control, result packaging, privacy scrubber, or token estimation.
- No hidden answer/grading files inside agent-visible task directories. `evaluator-notes/` is evaluator-only.
- No top-level execution-support directories (`runner`, `scorer`, `schemas`, `scripts`, `taskpacks`).
- Metadata uses literal string `UNAVAILABLE` for unobservable fields. Never estimate tokens, timings, or tool calls.
- Task trigger is `评测`. Trigger word unchanged across all tasks.
- All tasks must be completable with file read/write only — no code execution, no API calls, no browser.
- Crossing-harness fairness: no VitaClaw/OpenClaw/Hermes/OpenCode-specific tool references in any task.md.
- Veto-layer scoring: each task defines fatal errors that cap the total score regardless of other dimensions.

---

### Task 0: Extend Contract Tests to Cover All Tasks

**Files:**
- Modify: `tests/test_v3_contract.py`

**Interfaces:**
- Produces: Generalized `V3ContractTests` that validates all `tasks/task-*/` directories, not just `task-001`.

- [ ] **Step 1: Add helper to discover all task directories**

Replace hardcoded `task-001` references with a directory glob. Before line 28, add:

```python
ALL_TASKS = sorted(
    d for d in (ROOT / "tasks").iterdir()
    if d.is_dir() and d.name.startswith("task-")
)
```

- [ ] **Step 2: Generalize `test_task_has_question_pack_shape_without_hidden_answer_code`**

Replace the single-task test with a parameterized loop. Change lines 28-35 to:

```python
def test_each_task_has_question_pack_shape_without_hidden_answer_code(self) -> None:
    for task_dir in ALL_TASKS:
        with self.subTest(task=task_dir.name):
            self.assertTrue((task_dir / "task.md").is_file(),
                f"{task_dir.name}: missing task.md")
            self.assertTrue((task_dir / "inputs").is_dir(),
                f"{task_dir.name}: missing inputs/")
            self.assertTrue((task_dir / "output-requirements.md").is_file(),
                f"{task_dir.name}: missing output-requirements.md")
            # evaluator-notes/ is allowed (not in FORBIDDEN_NAMES)
            forbidden_names = {"ver" + "ifier.py", "solution.py", "answer.json", "ground_truth.json"}
            actual_names = {path.name for path in task_dir.rglob("*")}
            overlap = forbidden_names & actual_names
            self.assertTrue(len(overlap) == 0,
                f"{task_dir.name}: forbidden files found: {overlap}")
```

- [ ] **Step 3: Add test that `skill.json` tasks match on-disk task directories**

Add after the existing tests:

```python
def test_skill_json_tasks_match_on_disk_directories(self) -> None:
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    declared = set(manifest.get("tasks", []))
    on_disk = {d.name for d in ALL_TASKS}
    missing_from_manifest = on_disk - declared
    extra_in_manifest = declared - on_disk
    self.assertTrue(len(missing_from_manifest) == 0,
        f"Tasks on disk not in skill.json: {missing_from_manifest}")
    self.assertTrue(len(extra_in_manifest) == 0,
        f"Tasks in skill.json not on disk: {extra_in_manifest}")
```

- [ ] **Step 4: Verify existing tests still pass**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest discover tests -v
```
Expected: 4 existing tests PASS; the new test may FAIL if `skill.json` still only lists `task-001`.

- [ ] **Step 5: Commit**

```bash
git add tests/test_v3_contract.py
git commit -m "test: generalize contract tests to validate all tasks and skill.json alignment"
```

---

### Task 1: Update skill.json

**Files:**
- Modify: `skill.json`

- [ ] **Step 1: Add all task IDs**

Change `"tasks"` from `["task-001"]` to include all planned tasks:

```json
{
  "id": "agent-readiness-eval",
  "name": "Agent Readiness Eval",
  "version": "3.0.0",
  "description": "Portable question-pack skill for native harness execution and offline answer review.",
  "entrypoints": {
    "skill": "SKILL.md"
  },
  "tasks": [
    "task-001",
    "task-002",
    "task-003",
    "task-004",
    "task-005",
    "task-006"
  ]
}
```

- [ ] **Step 2: Verify test passes**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest tests.test_v3_contract.V3ContractTests.test_skill_json_tasks_match_on_disk_directories -v
```
Expected: PASS after all task directories exist (will fail for 003-006 until they're created in later tasks).

- [ ] **Step 3: Commit**

```bash
git add skill.json
git commit -m "feat: register task-002 through task-006 in skill.json manifest"
```

---

### Task 2: Revise Task 001 — Add Mixed-Severity Ticket

**Files:**
- Modify: `tasks/task-001/inputs/data.json`

- [ ] **Step 1: Add the mixed-severity ticket T-1006 to data.json**

Insert after T-1005 in the `tickets` array:

```json
    {
      "id": "T-1006",
      "severity": "high",
      "area": "billing",
      "customer": "pilot-bank-c",
      "summary": "Payment processing fails intermittently for premium-tier customers; additionally, customer reports confusing UI labels on the same checkout page.",
      "impact": "Revenue loss for premium accounts (estimated 15 affected transactions). UI confusion is non-blocking but generates support volume."
    }
```

(Note: severity is "high" due to the payment failure aspect; the UI label issue is minor. Agent must classify this as high based on the payment impact, not be confused by the UI mention.)

- [ ] **Step 2: Verify existing tests still pass**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest discover tests -v
```
Expected: All 5 tests PASS (including generalized task-shape test since task-001 still satisfies the contract).

- [ ] **Step 3: Commit**

```bash
git add tasks/task-001/inputs/data.json
git commit -m "feat(task-001): add mixed-severity ticket T-1006 to test ambiguity handling"
```

---

### Task 3: Revise Task 002 — Add Confidence Estimation

**Files:**
- Modify: `tasks/task-002/output-requirements.md`

- [ ] **Step 1: Add "Confidence & Information Gaps" section to output requirements**

Insert a new subsection in `final-answer.md` requirements, after "Recommended Actions" and before the JSON section:

```markdown
### Confidence & Information Gaps

A brief section that must include:

- A list of specific information gaps — data or logs that are not present in the provided files but would strengthen the analysis.
- An overall confidence estimate for the root cause conclusion, expressed as a qualitative level (High / Medium / Low) with a brief justification. Example: "Confidence: Medium. The timing correlation between v2.3.1 deployment and the error spike is strong, but we are missing auth-service write logs that would confirm the exact failure path."
```

- [ ] **Step 2: Add `confidence_level` and `information_gaps` fields to JSON schema**

Update the `artifacts/investigation-summary.json` schema table to include:

```markdown
| `confidence_level` | string | One of "High", "Medium", "Low" |
| `information_gaps` | array of strings | Specific data/logs that are missing and would improve the analysis |
```

- [ ] **Step 3: Verify tests pass**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest discover tests -v
```
Expected: All tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tasks/task-002/output-requirements.md
git commit -m "feat(task-002): add confidence estimation and information gap requirements"
```

---

### Task 4: Create Task 003 — Policy Compliance Check (Directory + task.md)

**Files:**
- Create: `tasks/task-003/task.md`

**Interfaces:**
- Produces: Task prompt for the policy compliance check scenario.

- [ ] **Step 1: Create directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-003/inputs
```

- [ ] **Step 2: Write task.md**

```markdown
# Task 003: Enterprise Policy Compliance Check

Your company has three internal policies governing employee requests. You receive several requests that must be checked against all applicable policies.

Use your harness's normal tools to read the policy documents and request forms in `inputs/`. Identify any compliance issues, cite the specific policy clause violated, and flag edge cases where exceptions apply.

Do not call any external grading or verification code.

## Work Required

1. Read all policy documents in `inputs/`.
2. Read all request forms in `inputs/`.
3. For each request, determine which policies apply.
4. For each applicable policy, check whether the request complies with every relevant clause.
5. Pay special attention to exception clauses — some policies have exemptions under specific conditions.
6. Flag all non-compliant items with the exact policy reference (document name + clause/section number).
7. Do NOT flag items as non-compliant if an exemption clause applies.
8. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- All compliance judgments must be supported by explicit policy text from the provided documents.
- Do not modify or write to the `inputs/` directory.
```

- [ ] **Step 3: Verify task.md exists and is readable**

```bash
cat /Users/hai/Projects/agent-readiness-eval/tasks/task-003/task.md | head -5
```
Expected: First 5 lines of the task document.

- [ ] **Step 4: Commit**

```bash
git add tasks/task-003/task.md
git commit -m "feat(task-003): add policy compliance check task prompt"
```

---

### Task 5: Create Task 003 Inputs

**Files:**
- Create: `tasks/task-003/inputs/policy-travel.md`
- Create: `tasks/task-003/inputs/policy-procurement.md`
- Create: `tasks/task-003/inputs/policy-data.md`
- Create: `tasks/task-003/inputs/request-travel-001.md`
- Create: `tasks/task-003/inputs/request-procurement-001.md`
- Create: `tasks/task-003/inputs/request-data-export-001.md`
- Create: `tasks/task-003/inputs/request-data-export-002.md`

- [ ] **Step 1: Write policy-travel.md**

```markdown
# Travel Expense Policy (POL-TRV-2025)

## 1. Scope
Applies to all employees requesting business travel reimbursement.

## 2. Approval Thresholds
- Expenses ≤ 5,000 CNY: Manager approval sufficient.
- Expenses > 5,000 CNY: VP-level approval required.
- Any international travel: VP approval required regardless of amount.

## 3. Allowable Expenses
- Economy-class flights only. Business class requires VP pre-approval.
- Hotel: max 800 CNY/night (domestic), 1,500 CNY/night (international).
- Per diem: 200 CNY/day (domestic), 400 CNY/day (international).

## 4. Receipt Requirements
- Receipts required for all expenses > 200 CNY.
- Digital receipts accepted. Scanned physical receipts must be legible.

## 5. Exemptions
- CEO-approved travel projects are exempt from the 5,000 CNY VP threshold.
- Emergency travel (defined as travel booked <24 hours before departure) waives the receipt requirement for expenses ≤ 500 CNY.
```

- [ ] **Step 2: Write policy-procurement.md**

```markdown
# Procurement Policy (POL-PRC-2025)

## 1. Scope
Applies to all software, hardware, and service purchases > 2,000 CNY.

## 2. Approval Thresholds
- 2,000 – 10,000 CNY: Department head approval.
- 10,001 – 50,000 CNY: VP approval + procurement committee review.
- > 50,000 CNY: CFO approval + competitive bidding required.

## 3. Vendor Requirements
- All vendors must be on the approved vendor list.
- New vendors require a 30-day security review before purchase.
- Single-source purchases > 20,000 CNY require written justification.

## 4. Software Licensing
- All software must be license-compliant. Free/open-source software requires legal review.
- SaaS subscriptions > 12 months require annual review clause in contract.

## 5. Exemptions
- Purchases approved in writing by the CEO are exempt from competitive bidding requirements.
- Emergency procurement (business continuity) waives the vendor security review but requires post-purchase audit within 14 days.
```

- [ ] **Step 3: Write policy-data.md**

```markdown
# Data Handling Policy (POL-DAT-2025)

## 1. Scope
Applies to all employee requests involving customer data access, export, or processing.

## 2. Data Classification
- **Public**: Marketing materials, press releases. No restrictions.
- **Internal**: Employee records, operational metrics. Manager approval required for export.
- **Confidential**: Customer PII, financial records. Data Protection Officer (DPO) approval required.
- **Restricted**: Authentication keys, encryption secrets. CTO approval required. Never exportable.

## 3. Export Rules
- Any data export must specify: purpose, recipient, retention period, deletion date.
- Exports of Confidential data must use encrypted transfer.
- Bulk exports (>100 records) require DPO pre-approval and audit logging.

## 4. Third-Party Sharing
- Sharing Confidential data with third parties requires a Data Processing Agreement (DPA).
- Sharing Restricted data with third parties is prohibited.

## 5. Exemptions
- No exemptions for Restricted data handling.
- Legal compliance requests (subpoena, court order) may override Confidential data restrictions — must be reviewed by Legal + DPO jointly.
```

- [ ] **Step 4: Write request-travel-001.md**

```markdown
# Travel Reimbursement Request — TRV-2025-042

**Employee:** Li Wei, Senior Engineer
**Department:** Platform Engineering
**Purpose:** Attend KubeCon Europe 2025 (Paris)
**Dates:** 2025-03-18 to 2025-03-22

## Expense Summary

| Item | Amount (CNY) | Receipt |
|------|-------------|---------|
| Round-trip flight (economy) | 8,200 | Attached |
| Hotel (4 nights × 1,200 CNY) | 4,800 | Attached |
| Conference registration | 3,500 | Attached |
| Per diem (5 days × 400 CNY) | 2,000 | N/A |
| **Total** | **18,500** | |

## Approvals

- Manager: Approved (Zhang Wei, 2025-02-20)
- VP: Pending
- CEO: N/A

## Notes
This is international travel. Hotel is within international rate limit (1,500 CNY/night).
```

- [ ] **Step 5: Write request-procurement-001.md**

```markdown
# Procurement Request — PRC-2025-018

**Requester:** Chen Mei, Marketing Director
**Department:** Marketing
**Purpose:** Annual subscription to AnalyticsPro SaaS platform
**Vendor:** AnalyticsPro Inc. (on approved vendor list)

## Purchase Details

| Item | Amount (CNY) |
|------|-------------|
| AnalyticsPro Enterprise Plan (12-month subscription) | 45,000 |
| Onboarding and training package | 8,000 |
| **Total** | **53,000** |

## Contract Details
- Term: 12 months (auto-renewal unless cancelled 30 days prior)
- No annual review clause currently in contract draft.

## Approvals
- Department Head: Approved (Chen Mei, 2025-03-01)
- VP: Pending
- Procurement Committee: Not yet convened
- CEO: A written approval note is attached — "Approved. Expedite. — CEO Wang, 2025-03-02"

## Notes
This is the third year using AnalyticsPro. Previous contracts were under 50K (price increased this year).
```

- [ ] **Step 6: Write request-data-export-001.md**

```markdown
# Data Export Request — DAT-2025-007

**Requester:** Liu Fang, Data Analyst
**Department:** Business Intelligence
**Purpose:** Generate Q1 customer churn analysis report
**Data Requested:** Customer subscription history, last 12 months, all active accounts
**Estimated Records:** ~50,000
**Classification:** Confidential (contains customer PII: names, emails, payment history)

## Export Details

| Field | Value |
|-------|-------|
| Format | CSV |
| Recipient | Liu Fang (internal) |
| Retention Period | 30 days (until report delivery) |
| Deletion Date | 2025-04-30 |
| Encrypted Transfer | Requested |
| DPO Approval | Not yet obtained |

## Notes
This is a bulk export (>100 records). Report delivery date is 2025-04-15.
```

- [ ] **Step 7: Write request-data-export-002.md**

```markdown
# Data Export Request — DAT-2025-008

**Requester:** Wang Peng, Legal Counsel
**Department:** Legal
**Purpose:** Respond to subpoena from Beijing Municipal Court (Case #BJ-2025-0287)
**Data Requested:** Full transaction history for 3 specific customer accounts (IDs: CUS-8842, CUS-9120, CUS-7761)
**Estimated Records:** ~2,000
**Classification:** Confidential (financial transaction records)

## Export Details

| Field | Value |
|-------|-------|
| Format | PDF (encrypted) |
| Recipient | Wang Peng (internal), then to court |
| Retention Period | Until case resolution (estimated 90 days) |
| Deletion Date | Not yet determined |
| Encrypted Transfer | Required |
| DPO Approval | Requested but not yet obtained |

## Attachments
- Subpoena document (scanned PDF): attached
- Court case reference: BJ-2025-0287

## Notes
This is a legal compliance request. Standard DPO approval process applies but timeline is court-mandated (due in 7 days).
```

- [ ] **Step 8: Commit**

```bash
git add tasks/task-003/inputs/
git commit -m "feat(task-003): add policy documents and 4 request forms with CEO exemption edge case"
```

---

### Task 6: Create Task 003 Output Requirements + Evaluator Notes

**Files:**
- Create: `tasks/task-003/output-requirements.md`
- Create: `tasks/task-003/evaluator-notes/reference-analysis.md`
- Create: `tasks/task-003/evaluator-notes/manual-scoring-rubric.md`

- [ ] **Step 1: Create evaluator-notes directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-003/evaluator-notes
```

- [ ] **Step 2: Write output-requirements.md**

```markdown
# Output Requirements — Task 003

Create these files in your answer directory:

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/compliance-report.json
```

## `task-id.txt`

Must contain exactly:

```text
task-003
```

## `final-answer.md`

Must include:

### Executive Summary
One paragraph summarizing overall compliance status across all requests.

### Per-Request Compliance Report
For each request form, list:
- Request ID and type
- Applicable policies (referenced by document name)
- Compliance status: "Compliant", "Non-Compliant", or "Compliant (Exemption Applied)"
- For non-compliant items: specific policy clause violated and why
- For exemptions: which exemption clause was applied and the evidence (e.g., CEO approval note)

### Summary Table
A table listing all non-compliant items ranked by risk severity (highest first).

## `artifacts/compliance-report.json`

Must be valid JSON:

```json
{
  "task_id": "task-003",
  "requests": [],
  "total_requests": 0,
  "compliant_count": 0,
  "non_compliant_count": 0,
  "exemption_applied_count": 0,
  "findings": []
}
```

Each entry in `requests`:

```json
{
  "request_id": "TRV-2025-042",
  "type": "travel",
  "compliance_status": "Non-Compliant",
  "applicable_policies": ["POL-TRV-2025"],
  "findings": []
}
```

Each finding:

```json
{
  "policy_ref": "POL-TRV-2025 §2",
  "description": "Total exceeds 5,000 CNY without VP approval",
  "severity": "High",
  "exemption_applied": false,
  "exemption_clause": null
}
```

## `run-metadata.json`

Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
```

- [ ] **Step 3: Write reference-analysis.md**

```markdown
# Task 003 — Reference Analysis (Evaluator Only)

## TRV-2025-042: NON-COMPLIANT
- Total 18,500 CNY > 5,000 CNY → VP approval required (§2)
- VP approval is "Pending" → not obtained
- International travel → VP approval required regardless of amount (§2)
- Hotel and per diem within policy limits

## PRC-2025-018: COMPLIANT (Exemption Applied)
- Total 53,000 CNY > 50,000 CNY → normally requires CFO + competitive bidding (§2)
- BUT: CEO written approval note attached → competitive bidding exempt (§5 exemption)
- SaaS 12-month contract → needs annual review clause (§4) → **NON-COMPLIANT** — contract draft lacks this clause
- Vendor is on approved list → compliant
- Net: one non-compliant finding (missing annual review clause)

## DAT-2025-007: NON-COMPLIANT
- Confidential data (customer PII) → DPO approval required (§2)
- DPO approval "Not yet obtained" → non-compliant
- Bulk export >100 records → DPO pre-approval + audit logging (§3)
- Encrypted transfer requested but DPO not approved → blocks the export

## DAT-2025-008: COMPLIANT (Exemption Applied)
- Confidential data (financial records) → DPO approval required (§2)
- BUT: legal compliance request (subpoena) → §5 exemption applies
- Requires Legal + DPO joint review (§5) — DPO approval requested but not yet obtained
- This is partially compliant: the subpoena justifies the export, but joint DPO review still needed
- Classify as: Compliant (Exemption Applied) for the export itself, with note that DPO joint review is still pending

## Scoring Notes
- TRV-2025-042: key finding is the missing VP approval + international travel trigger
- PRC-2025-018: Agent MUST recognize the CEO exemption for competitive bidding BUT must also catch the missing annual review clause
- DAT-2025-007: straightforward DPO requirement violation
- DAT-2025-008: Agent must recognize the subpoena as a legal compliance trigger that changes the rules
```

- [ ] **Step 4: Write manual-scoring-rubric.md**

```markdown
# Task 003 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Misses PII/data compliance issue entirely (no DPO flagging on DAT-2025-007) | 40 |
| Misses the missing annual review clause on PRC-2025-018 while correctly applying CEO exemption | 60 |
| Treats DAT-2025-008 (subpoena) as standard non-compliant without recognizing legal exemption | 60 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Correct policy clause identification | 20 | Each finding cites correct policy document + section number |
| Edge case / exemption handling | 20 | CEO exemption on PRC-2025-018 correctly applied; subpoena exemption on DAT-2025-008 correctly applied; exemption does NOT leak to non-exempt requests |
| Conditional logic correctness | 20 | International travel triggers VP regardless of amount; >50K triggers CFO + bidding; all thresholds applied correctly |
| No missed findings | 20 | All non-compliant items across all 4 requests identified |
| No false positives | 10 | Compliant items not incorrectly flagged |
| Format compliance | 10 | JSON valid and follows schema; Markdown has all required sections |
```

- [ ] **Step 5: Commit**

```bash
git add tasks/task-003/output-requirements.md tasks/task-003/evaluator-notes/
git commit -m "feat(task-003): add output requirements, reference analysis, and scoring rubric"
```

---

### Task 7: Create Task 004 — Cross-System Reconciliation (task.md + inputs)

**Files:**
- Create: `tasks/task-004/task.md`
- Create: `tasks/task-004/inputs/crm-accounts.json`
- Create: `tasks/task-004/inputs/billing-records.json`
- Create: `tasks/task-004/inputs/support-tickets.json`
- Create: `tasks/task-004/inputs/field-mapping.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-004/inputs
```

- [ ] **Step 2: Write task.md**

```markdown
# Task 004: Cross-System Data Reconciliation

Three internal systems (CRM, Billing, and Support) hold customer account data exported at the same point in time. The systems use different field names and data formats. Your job is to reconcile them.

A field-mapping document is provided to help you understand how records relate across systems. Use your harness's tools to read all files, then identify inconsistencies.

Do not call any external grading or verification code.

## Work Required

1. Read all files in `inputs/`.
2. Use the field-mapping document to understand how to match records across systems.
3. Compare all customer records across the three systems.
4. Identify every inconsistency: amount mismatches, status mismatches, records present in one system but missing from another.
5. Categorize each inconsistency by type.
6. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- Use the field-mapping document as the authoritative guide for cross-system matching. Do not guess field relationships.
- Do not modify or write to the `inputs/` directory.
```

- [ ] **Step 3: Write crm-accounts.json**

```json
{
  "system": "CRM",
  "export_date": "2025-06-15",
  "accounts": [
    {
      "account_id": "ACC-1001",
      "company_name": "Pilot Bank A",
      "account_status": "active",
      "plan": "enterprise",
      "monthly_revenue": 45000,
      "primary_contact": "li.wei@pilotbanka.com"
    },
    {
      "account_id": "ACC-1002",
      "company_name": "TechStart Inc.",
      "account_status": "active",
      "plan": "professional",
      "monthly_revenue": 12000,
      "primary_contact": "chen.mei@techstart.com"
    },
    {
      "account_id": "ACC-1003",
      "company_name": "GlobalTrade Ltd.",
      "account_status": "suspended",
      "plan": "enterprise",
      "monthly_revenue": 0,
      "primary_contact": "wang.fang@globaltrade.com"
    },
    {
      "account_id": "ACC-1004",
      "company_name": "DataVault Systems",
      "account_status": "active",
      "plan": "enterprise",
      "monthly_revenue": 78000,
      "primary_contact": "zhang.min@datavault.com"
    }
  ]
}
```

- [ ] **Step 4: Write billing-records.json**

```json
{
  "system": "Billing",
  "export_date": "2025-06-15",
  "records": [
    {
      "billing_account": "BA-PBA-001",
      "customer_name": "Pilot Bank A",
      "status": "current",
      "current_month_charges": 45000,
      "outstanding_balance": 0,
      "payment_method": "wire"
    },
    {
      "billing_account": "BA-TSI-002",
      "customer_name": "TechStart Inc.",
      "status": "current",
      "current_month_charges": 12000,
      "outstanding_balance": 3500,
      "payment_method": "credit_card"
    },
    {
      "billing_account": "BA-GTL-003",
      "customer_name": "GlobalTrade Ltd.",
      "status": "delinquent",
      "current_month_charges": 0,
      "outstanding_balance": 18000,
      "payment_method": "wire"
    },
    {
      "billing_account": "BA-DVS-004",
      "customer_name": "DataVault Systems",
      "status": "current",
      "current_month_charges": 65000,
      "outstanding_balance": 0,
      "payment_method": "wire"
    }
  ]
}
```

(Key inconsistency: DataVault CRM monthly_revenue = 78,000, Billing current_month_charges = 65,000 — a 13,000 discrepancy.)

- [ ] **Step 5: Write support-tickets.json**

```json
{
  "system": "Support",
  "export_date": "2025-06-15",
  "tickets": [
    {
      "ticket_id": "ST-5001",
      "customer_ref": "ACC-1001",
      "issue_type": "performance",
      "status": "resolved",
      "priority": "medium",
      "opened_date": "2025-06-10"
    },
    {
      "ticket_id": "ST-5002",
      "customer_ref": "ACC-1002",
      "issue_type": "billing",
      "status": "open",
      "priority": "high",
      "opened_date": "2025-06-14"
    },
    {
      "ticket_id": "ST-5004",
      "customer_ref": "ACC-1004",
      "issue_type": "onboarding",
      "status": "open",
      "priority": "low",
      "opened_date": "2025-06-01"
    }
  ]
}
```

(Key inconsistencies: ACC-1003/GlobalTrade has no support ticket — missing record. CRM says "suspended", Billing says "delinquent" — status mismatch.)

- [ ] **Step 6: Write field-mapping.md**

```markdown
# Cross-System Field Mapping

## CRM → Billing

| CRM Field | Billing Field | Match Type |
|-----------|---------------|------------|
| `account_id` (ACC-NNNN) | `billing_account` (BA-XXX-NNNN) | Partial: last 4 digits of billing_account match CRM account_id digits |
| `company_name` | `customer_name` | Exact text match |
| `account_status` | `status` | Value mapping: active↔current, suspended↔delinquent |
| `monthly_revenue` | `current_month_charges` | Direct numeric comparison |

## CRM → Support

| CRM Field | Support Field | Match Type |
|-----------|---------------|------------|
| `account_id` | `customer_ref` | Exact match |

## Notes
- Billing `outstanding_balance` has no CRM equivalent — for information only.
- Support system may have gaps (not all CRM accounts have support tickets).
- Billing `payment_method` has no CRM equivalent — for information only.
```

- [ ] **Step 7: Commit**

```bash
git add tasks/task-004/
git commit -m "feat(task-004): add cross-system reconciliation task with CRM/billing/support data and field mapping"
```

---

### Task 8: Create Task 004 Output Requirements + Evaluator Notes

**Files:**
- Create: `tasks/task-004/output-requirements.md`
- Create: `tasks/task-004/evaluator-notes/reference-analysis.md`
- Create: `tasks/task-004/evaluator-notes/manual-scoring-rubric.md`

- [ ] **Step 1: Create evaluator-notes directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-004/evaluator-notes
```

- [ ] **Step 2: Write output-requirements.md**

```markdown
# Output Requirements — Task 004

Create these files in your answer directory:

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/reconciliation-report.json
```

## `task-id.txt`

Must contain exactly:

```text
task-004
```

## `final-answer.md`

Must include:

### Executive Summary
One paragraph describing the reconciliation scope and high-level findings.

### Methodology
Describe your approach: which files you read first, how you used the field-mapping document to match records, and how you verified results.

### Discrepancy Report
For each customer account, list:
- Account identifiers across all three systems
- All discrepancies found (amount mismatch, status mismatch, missing records)
- Type of each discrepancy
- The specific values from each system that conflict

### Summary Table
Count of discrepancies by type.

## `artifacts/reconciliation-report.json`

Must be valid JSON:

```json
{
  "task_id": "task-004",
  "total_accounts_reviewed": 0,
  "discrepancy_count": 0,
  "discrepancies_by_type": {
    "amount_mismatch": 0,
    "status_mismatch": 0,
    "missing_record": 0
  },
  "findings": []
}
```

Each finding:

```json
{
  "account_identifiers": {
    "crm": "ACC-1001",
    "billing": "BA-PBA-001",
    "support": "ST-5001"
  },
  "discrepancy_type": "amount_mismatch",
  "description": "CRM monthly_revenue=78000 vs Billing current_month_charges=65000",
  "crm_value": "78000",
  "billing_value": "65000"
}
```

## `run-metadata.json`

Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
```

- [ ] **Step 3: Write reference-analysis.md**

```markdown
# Task 004 — Reference Analysis (Evaluator Only)

## Expected Discrepancies (4 total)

### 1. DataVault Systems — Amount Mismatch
- CRM monthly_revenue: 78,000
- Billing current_month_charges: 65,000
- Discrepancy: 13,000
- Severity: High (affects financial reporting)

### 2. GlobalTrade Ltd. — Status Mismatch
- CRM account_status: "suspended"
- Billing status: "delinquent"
- Mapping says suspended↔delinquent should match — these ARE consistent per the mapping
- BUT: No support ticket for ACC-1003 → this is a Missing Record discrepancy
- Severity: Medium (missing support record for a suspended/delinquent account)

### 3. TechStart Inc. — Missing Record
- Support: no ticket with customer_ref "ACC-1002" → not a discrepancy (gaps expected per field-mapping notes)
- Billing: outstanding_balance 3,500 BUT payment expected 12,000 → not a discrepancy (outstanding_balance has no CRM equivalent — for info only)
- **Actually no discrepancy here** — correctly identified as no issue

### 4. Support ticket ST-5002 (TechStart) — open billing issue
- This is a legitimate support ticket but does not constitute a data discrepancy — it's operational context
- Agent should NOT flag this as a reconciliation issue

## Expected Non-Issues (NO discrepancy)
- Pilot Bank A: clean match (45,000 both sides, active/current, support ticket exists)
- TechStart amount match: 12,000 both sides
- TechStart status mismatch? CRM=active, Billing=current → mapping says they match → no discrepancy
- Support gaps are expected per field-mapping notes — not discrepancies
```

- [ ] **Step 4: Write manual-scoring-rubric.md**

```markdown
# Task 004 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Did not use field mapping — matched records by name similarity only | 50 |
| Completely skipped one of the three data sources | 40 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Correct cross-source matching via field mapping | 20 | All records correctly matched using mapping rules. ACC-1001↔BA-PBA-001 via last-4-digit rule; ACC-1004↔BA-DVS-004; etc. |
| All genuine discrepancies identified | 25 | Amount mismatch (DataVault 78K vs 65K) + status mismatch (GlobalTrade suspended vs delinquent = expected per mapping, NOT a discrepancy) + missing support record for GlobalTrade |
| No false positives | 20 | TechStart amount 12K/12K matches; status active/current matches; billing outstanding_balance is informational only; support gap for TechStart not a discrepancy (mapping says gaps expected) |
| Discrepancy classification correct | 15 | Each finding correctly classified as amount_mismatch, status_mismatch, or missing_record |
| Methodology documented | 20 | Describes approach: read mapping first → understand matching rules → read CRM → match to Billing → cross-check Support |
```

- [ ] **Step 5: Commit**

```bash
git add tasks/task-004/output-requirements.md tasks/task-004/evaluator-notes/
git commit -m "feat(task-004): add output requirements, reference analysis, and scoring rubric"
```

---

### Task 9: Create Task 005 — Conflict Resolution (task.md + inputs)

**Files:**
- Create: `tasks/task-005/task.md`
- Create: `tasks/task-005/inputs/product-requirements.md`
- Create: `tasks/task-005/inputs/security-requirements.md`
- Create: `tasks/task-005/inputs/project-charter.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-005/inputs
```

- [ ] **Step 2: Write task.md**

```markdown
# Task 005: Conflicting Requirements Resolution

Two departments have submitted requirements for the same system upgrade. The requirements conflict in several areas. A project charter defines how to resolve conflicts.

Your job is to identify every conflict, apply the charter's priority rules to resolve each one, and produce a unified requirements document.

Do not call any external grading or verification code.

## Work Required

1. Read all files in `inputs/`.
2. Identify every point where the two requirement documents contradict each other.
3. For each conflict, determine the resolution using the project charter's priority rules.
4. For each resolution, clearly state which charter clause was applied and which requirement was deprioritized.
5. Produce a prioritized action plan based on the resolved requirements.
6. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- All resolutions must be traceable to a specific charter clause. Do not make judgment calls unsupported by the charter.
- Do not modify or write to the `inputs/` directory.
```

- [ ] **Step 3: Write product-requirements.md**

```markdown
# Product Department — System Upgrade Requirements

**Document:** REQ-PRD-2025-001
**Author:** Product Team
**Date:** 2025-06-01

## 1. Release Window
The upgrade must be deployed during business hours (09:00-18:00 Beijing time) to ensure maximum team availability for post-deployment validation.

## 2. API Access
All internal APIs should be accessible over the public internet to simplify integration with third-party partner tools. No VPN requirement.

## 3. Authentication
Implement OAuth 2.0 with social login providers (Google, GitHub) for user convenience. Password-based login should remain available as fallback.

## 4. Data Retention
User activity logs should be retained for a minimum of 12 months for product analytics purposes. Full fidelity logs required.

## 5. Performance
System must support 10,000 concurrent users with <200ms P95 latency. Auto-scaling preferred over manual capacity planning.
```

- [ ] **Step 4: Write security-requirements.md**

```markdown
# Security Department — System Upgrade Requirements

**Document:** REQ-SEC-2025-001
**Author:** Security Team
**Date:** 2025-06-03

## 1. Release Window
All production deployments must occur during the maintenance window (02:00-05:00 Beijing time) to minimize user impact and allow rollback before business hours.

## 2. API Access
All internal APIs must be accessible only through the corporate VPN. No public internet exposure under any circumstances.

## 3. Authentication
Multi-Factor Authentication (MFA) must be mandatory for all users. Social login providers introduce third-party risk and should be prohibited. Password-based login is insufficient — MFA is non-negotiable.

## 4. Data Retention
User activity logs must be purged after 90 days to comply with data minimization principles. Only aggregated, anonymized data may be retained beyond 90 days.

## 5. Performance
System must support 10,000 concurrent users with <200ms P95 latency. Must pass penetration testing before go-live. Rate limiting must be enforced at API gateway level.
```

- [ ] **Step 5: Write project-charter.md**

```markdown
# Project Charter — System Upgrade v3

**Document:** CHTR-2025-003
**Approved by:** CTO Office
**Date:** 2025-05-15

## Priority Rules

When requirements from different departments conflict, apply these rules in order:

### Rule 1: Security First
Security requirements take precedence over convenience and user experience. If a security requirement conflicts with a product requirement, the security requirement governs.

### Rule 2: Compliance Over Features
Regulatory and compliance requirements override feature requests. If a compliance requirement conflicts with any other requirement, the compliance requirement governs.

### Rule 3: Data Minimization
Where security and compliance do not dictate otherwise, minimize data collection and retention. Shorter retention periods are preferred when no business-critical reason demands longer retention.

### Rule 4: Operational Safety
Deployment and operational safety requirements (including maintenance windows) take precedence over team convenience.

### Rule 5: CTO Final Decision
If Rules 1-4 do not resolve a conflict, the CTO makes the final decision. In this case, flag the conflict as "escalated to CTO" in your output.

### Rule 6: Tiebreakers
When two requirements of equal priority under the above rules conflict, prefer the one that maximizes user safety, then system reliability, then development velocity.
```

- [ ] **Step 6: Commit**

```bash
git add tasks/task-005/
git commit -m "feat(task-005): add conflict resolution task with product/security requirements and project charter"
```

---

### Task 10: Create Task 005 Output Requirements + Evaluator Notes

**Files:**
- Create: `tasks/task-005/output-requirements.md`
- Create: `tasks/task-005/evaluator-notes/reference-analysis.md`
- Create: `tasks/task-005/evaluator-notes/manual-scoring-rubric.md`

- [ ] **Step 1: Create evaluator-notes directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-005/evaluator-notes
```

- [ ] **Step 2: Write output-requirements.md**

```markdown
# Output Requirements — Task 005

Create these files in your answer directory:

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/resolution-analysis.json
```

## `task-id.txt`

Must contain exactly:

```text
task-005
```

## `final-answer.md`

Must include:

### Executive Summary
One paragraph describing the conflict resolution process and outcome.

### Conflict Register
For each identified conflict:
- Conflicting requirement IDs (from product and security docs)
- Nature of the conflict
- Resolution applied
- Charter clause cited (e.g., "Charter Rule 1: Security First")
- Which requirement was deprioritized and why

### Unified Requirements
The final, conflict-free set of requirements, organized by topic area.

### Prioritized Action Plan
Three to five actions ranked by priority, with dependencies noted.

## `artifacts/resolution-analysis.json`

Must be valid JSON:

```json
{
  "task_id": "task-005",
  "total_conflicts_identified": 0,
  "conflicts": [],
  "unified_requirements": [],
  "escalated_to_cto": [],
  "action_plan": []
}
```

Each conflict entry:

```json
{
  "id": "conflict-1",
  "topic": "Release Window",
  "product_requirement": "REQ-PRD-2025-001 §1",
  "security_requirement": "REQ-SEC-2025-001 §1",
  "nature": "Product requires business hours deployment; Security requires maintenance window.",
  "resolution": "Adopt Security requirement: maintenance window 02:00-05:00.",
  "charter_clause": "Charter Rule 4: Operational Safety",
  "deprioritized": "Product requirement for business hours deployment"
}
```

## `run-metadata.json`

Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
```

- [ ] **Step 3: Write reference-analysis.md**

```markdown
# Task 005 — Reference Analysis (Evaluator Only)

## Expected Conflicts (5 total)

### Conflict 1: Release Window
- Product: Business hours (09:00-18:00) — team availability
- Security: Maintenance window (02:00-05:00) — user impact minimization
- Resolution: Security wins per Rule 4 (Operational Safety) — maintenance window
- Deprioritized: Product requirement

### Conflict 2: API Access
- Product: Public internet access — simplify integration
- Security: VPN only — no public exposure
- Resolution: Security wins per Rule 1 (Security First)
- Deprioritized: Product requirement for public access

### Conflict 3: Authentication
- Product: OAuth 2.0 + social login + password fallback
- Security: MFA mandatory, no social login
- Resolution: Security wins per Rule 1 (Security First). MFA mandatory. Social login prohibited.
- Deprioritized: Social login convenience

### Conflict 4: Data Retention
- Product: 12 months, full fidelity
- Security: 90 days, anonymized only after
- Resolution: Apply Rule 3 (Data Minimization) — shorter retention preferred. 90 days. BUT note: product analytics is a business reason — flag this as potentially needing CTO input if business case is strong
- Expected answer: 90 days per Rule 3. Optionally flag business case for longer retention as requiring separate approval.

### Conflict 5: No Conflict
- Performance: Both require <200ms P95 latency, 10K concurrent users. No conflict. Security adds rate limiting and pen testing — these are additive, not conflicting.

## Expected Non-Conflict
- Performance requirements are aligned (both say 10K users, <200ms). Agent should note this, not fabricate a conflict.
```

- [ ] **Step 4: Write manual-scoring-rubric.md**

```markdown
# Task 005 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Did not identify any conflicts (treated both docs as consistent) | 30 |
| Resolved a conflict against the charter's explicit priority | 50 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| All conflicts identified | 20 | All 4 genuine conflicts found; no conflict invented on performance topic |
| Correct charter clause applied | 20 | Each resolution cites the correct Rule number (1, 3, 4) |
| Neutrality statements | 15 | Each resolution states which requirement was deprioritized + charter justification |
| Action plan prioritized correctly | 15 | Plan respects dependencies and charter-mandated safety-first ordering |
| No false conflicts | 15 | Performance requirements correctly identified as non-conflicting, additive |
| Format compliance | 15 | JSON valid with all required fields; Markdown readable |
```

- [ ] **Step 5: Commit**

```bash
git add tasks/task-005/output-requirements.md tasks/task-005/evaluator-notes/
git commit -m "feat(task-005): add output requirements, reference analysis, and scoring rubric"
```

---

### Task 11: Create Task 006 — Multi-Source Report Synthesis (task.md + inputs)

**Files:**
- Create: `tasks/task-006/task.md`
- Create: `tasks/task-006/inputs/weekly-reports.md`
- Create: `tasks/task-006/inputs/customer-satisfaction.json`
- Create: `tasks/task-006/inputs/competitor-brief.md`
- Create: `tasks/task-006/inputs/kpi-data.json`
- Create: `tasks/task-006/inputs/partner-growth-brief.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-006/inputs
```

- [ ] **Step 2: Write task.md**

```markdown
# Task 006: Q4 Business Review — Multi-Source Report Synthesis

Your company's Q4 business review is approaching. You have five documents covering the quarter's performance from different angles.

Your job is to synthesize these into a coherent executive brief. Pay attention to data consistency — not all sources may agree.

Do not call any external grading or verification code.

## Work Required

1. Read all files in `inputs/`.
2. Extract key information from each source.
3. Cross-check data claims across sources. Flag any inconsistencies you find.
4. Identify the most important trends, risks, and opportunities.
5. Recommend three data-backed actions for the next quarter.
6. Write the required files listed in `output-requirements.md`.

## Important Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from the provided files.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- Every trend claim and recommendation must cite at least one specific data source.
- Do not perform statistical analysis beyond what is directly stated in the provided files.
- Do not modify or write to the `inputs/` directory.
```

- [ ] **Step 3: Write weekly-reports.md**

```markdown
# Q4 Weekly Business Reports — Summary

## Week 40 (Oct 1-7)
- Revenue: 2.1M CNY (on target)
- New enterprise accounts: 4
- Churn: 2 accounts (0.8% of base)
- Key win: Signed Pilot Insurance Co. (est. annual value 1.8M CNY)

## Week 41 (Oct 8-14)
- Revenue: 2.3M CNY (+9.5% WoW)
- New enterprise accounts: 3
- Churn: 1 account
- Key issue: Billing system outage for 4 hours on Oct 12. 12 invoices delayed.

## Week 42 (Oct 15-21)
- Revenue: 2.0M CNY (-13% WoW, attributed to billing delay catch-up)
- New enterprise accounts: 5
- Churn: 0 accounts
- Key milestone: Enterprise plan v3 launched. Migration started for 3 pilot accounts.

## Week 43 (Oct 22-28)
- Revenue: 2.4M CNY (+20% WoW)
- New enterprise accounts: 6 (record week)
- Churn: 1 account (non-enterprise)
- Customer satisfaction survey conducted this week (see separate report).

## Trend Summary
Q4 is trending above Q3 average (1.9M CNY/week). Enterprise segment growing faster than SMB. Churn stable.
```

- [ ] **Step 4: Write customer-satisfaction.json**

```json
{
  "survey": "Q4 2025 Customer Satisfaction",
  "fielded": "2025-10-22 to 2025-10-28",
  "respondents": 142,
  "response_rate_pct": 38,
  "overall_nps": 42,
  "previous_quarter_nps": 38,
  "scores_by_segment": {
    "enterprise": {
      "nps": 55,
      "satisfaction_pct": 88,
      "top_pain_point": "Onboarding time too long (avg 6 weeks)"
    },
    "professional": {
      "nps": 35,
      "satisfaction_pct": 72,
      "top_pain_point": "Reporting features lack custom dashboards"
    },
    "starter": {
      "nps": 28,
      "satisfaction_pct": 65,
      "top_pain_point": "API documentation incomplete"
    }
  }
}
```

- [ ] **Step 5: Write competitor-brief.md**

```markdown
# Competitive Intelligence Brief — Q4 2025

**Analyst:** Market Research Team
**Date:** 2025-10-30

## Competitor A (Market Leader)
- Launched AI-powered analytics module in September. Early reviews positive.
- Pricing: 20-30% above our enterprise tier.
- Weakness: No on-premise deployment option.

## Competitor B (Direct Rival)
- Released custom dashboard builder in October — directly addresses our top enterprise pain point.
- Pricing: Roughly at parity with our professional tier.
- Weakness: Limited API integrations compared to our platform.

## Competitor C (New Entrant)
- Launched in August. Open-source core, paid enterprise features.
- Pricing: 40-60% below our starter tier.
- Weakness: Very small customer base (<50 accounts), no enterprise references.

## Market Trends
- AI/ML features becoming table stakes in our segment.
- Custom reporting is the #1 feature request across competitor review sites.
- Open-core model gaining traction among SMB buyers.
```

- [ ] **Step 6: Write kpi-data.json**

```json
{
  "period": "2025-Q4",
  "generated": "2025-11-01",
  "metrics": {
    "total_revenue_q4_to_date": 8800000,
    "revenue_by_week": [2100000, 2300000, 2000000, 2400000],
    "enterprise_revenue_share_pct": 68,
    "total_active_accounts": 248,
    "enterprise_accounts": 42,
    "professional_accounts": 89,
    "starter_accounts": 117,
    "net_new_accounts_q4": 18,
    "churned_accounts_q4": 4,
    "net_revenue_retention_pct": 104,
    "average_time_to_onboard_days": {
      "enterprise": 42,
      "professional": 14,
      "starter": 5
    }
  }
}
```

- [ ] **Step 7: Write partner-growth-brief.md**

```markdown
# Partner Channel Growth Brief — Q4 2025

**Prepared by:** Strategic Partnerships Team
**For:** Q4 Business Review
**Date:** 2025-10-31

## Executive Summary

Our partner channel now represents **35% of total company revenue** in Q4, up from 22% in Q3. Partner-sourced revenue reached 1.74M CNY this quarter, confirming partnerships as our primary growth engine.

## Key Metrics

| Metric | Q3 2025 | Q4 2025 | Change |
|--------|---------|---------|--------|
| Partner-sourced revenue | 1.2M CNY | 1.74M CNY | +45% |
| Share of total revenue | 22% | 35% | +13pp |
| Active partners | 8 | 12 | +50% |
| Partner-sourced deals | 14 | 22 | +57% |

## Top Performing Partners

1. CloudServe Solutions — 8 deals closed, primarily enterprise segment
2. DataBridge Consulting — 5 deals, professional and enterprise
3. TechAlliance Group — 4 deals, mixed segments

## Recommendations

1. Double partner incentive bonuses for Q1 2026.
2. Hire 2 additional partner managers.
3. Launch co-marketing program with top 3 partners.

## Note
All revenue figures are unaudited. Final reconciliation with finance team pending for year-end close.
```

- [ ] **Step 8: Commit**

```bash
git add tasks/task-006/
git commit -m "feat(task-006): add report synthesis task with 5 sources including false-trend partner brief"
```

---

### Task 12: Create Task 006 Output Requirements + Evaluator Notes

**Files:**
- Create: `tasks/task-006/output-requirements.md`
- Create: `tasks/task-006/evaluator-notes/reference-analysis.md`
- Create: `tasks/task-006/evaluator-notes/manual-scoring-rubric.md`

- [ ] **Step 1: Create evaluator-notes directory**

```bash
mkdir -p /Users/hai/Projects/agent-readiness-eval/tasks/task-006/evaluator-notes
```

- [ ] **Step 2: Write output-requirements.md**

```markdown
# Output Requirements — Task 006

Create these files in your answer directory:

```text
task-id.txt
final-answer.md
run-metadata.json
artifacts/executive-brief.json
```

## `task-id.txt`

Must contain exactly:

```text
task-006
```

## `final-answer.md`

Must include:

### Executive Summary
One paragraph synthesizing Q4 performance across all sources.

### Key Trends
Three to five trends, each supported by at least one data source citation.

### Data Consistency Check
A section explicitly checking for inconsistencies across sources. Flag any contradictory claims with the specific sources and values that conflict.

### Risks
Top risks identified, ranked by severity.

### Recommended Actions
Three prioritized actions for Q1 2026, each with:
- Specific data source(s) supporting the recommendation
- Expected impact
- Any assumptions or caveats

## `artifacts/executive-brief.json`

Must be valid JSON:

```json
{
  "task_id": "task-006",
  "period": "Q4 2025",
  "total_sources_reviewed": 0,
  "key_trends": [],
  "data_inconsistencies": [],
  "top_risks": [],
  "recommended_actions": []
}
```

Each inconsistency entry:

```json
{
  "source_a": "partner-growth-brief.md",
  "source_b": "kpi-data.json",
  "claim": "Partner share is 35% of total revenue",
  "conflict": "Partner revenue 1.74M CNY / total revenue 8.8M CNY = 19.8%, not 35%",
  "severity": "High"
}
```

## `run-metadata.json`

Copy fields from `templates/run-metadata.json`. Use `UNAVAILABLE` for unobservable fields.
```

- [ ] **Step 3: Write reference-analysis.md**

```markdown
# Task 006 — Reference Analysis (Evaluator Only)

## Expected Key Trends
1. Enterprise segment driving growth (68% of revenue, NPS 55, 42 accounts)
2. Customer satisfaction improving overall (NPS 38→42), but onboarding pain persists (6 weeks enterprise)
3. Competitive pressure from custom dashboards (Competitor B) and open-core (Competitor C)
4. Churn stable and low (4 accounts = 1.6% of 248)

## Expected Data Inconsistency (THE KEY FINDING)
- Partner brief: claims 35% share of total Q4 revenue, with 1.74M CNY partner revenue
- KPI data: total Q4 revenue = 8.8M CNY
- Math check: 1.74M / 8.8M = 19.8%, NOT 35%
- Conclusion: The 35% claim is mathematically inconsistent with the KPI data
- Impact: Partner budget recommendations (double bonuses, hire 2 managers) are based on inflated metrics. These recommendations should be tabled pending finance reconciliation.
- Note: Partner brief itself says "Final reconciliation with finance team pending" — agent should flag this as the likely explanation

## Expected Non-Issues
- NPS and satisfaction survey data is consistent with other sources
- Revenue figures in weekly reports align with KPI data
- Competitor intelligence is qualitative and does not require numerical validation

## Recommended Actions (example acceptable set)
1. Table partner budget decisions pending finance reconciliation of partner revenue share claim
2. Prioritize onboarding time reduction for enterprise (6 weeks → target 4 weeks) — directly addresses #1 pain point and competitive threat
3. Accelerate custom dashboard development — Competitor B's release creates urgency
```

- [ ] **Step 4: Write manual-scoring-rubric.md**

```markdown
# Task 006 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer

| Fatal Error | Score Cap |
|-------------|:---------:|
| Did not detect the partner brief 35% vs KPI data mathematical contradiction | 40 |
| All trend claims lack data source citations | 50 |

## Dimension Scoring

| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Cross-source theme extraction | 20 | Key trends from all 5 sources captured without omission |
| Data inconsistency detection | 20 | Specifically identifies the 35% vs 19.8% math contradiction; explains the mismatch with precise figures |
| Trend claims supported by data | 20 | Each trend cites a specific source and value; no unsupported claims |
| Recommended actions are data-backed | 20 | Each action has a data citation and addresses a real finding from the sources |
| No fabricated inferences | 10 | Does not make causal claims or predictions beyond what data supports |
| Format compliance | 10 | JSON valid; Markdown has all required sections |
```

- [ ] **Step 5: Commit**

```bash
git add tasks/task-006/output-requirements.md tasks/task-006/evaluator-notes/
git commit -m "feat(task-006): add output requirements, reference analysis, and scoring rubric"
```

---

### Task 13: Update README.md to reflect full v1

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update package shape diagram to show all 6 tasks**

Replace the tasks section of the diagram:

```markdown
├── tasks/
│   ├── task-001/       # Customer Ticket Triage
│   ├── task-002/       # AI Platform Incident Investigation
│   ├── task-003/       # Policy Compliance Check
│   ├── task-004/       # Cross-System Data Reconciliation
│   ├── task-005/       # Conflicting Requirements Resolution
│   └── task-006/       # Multi-Source Report Synthesis
```

- [ ] **Step 2: Add task overview table**

Insert after the "How to Run" section:

```markdown
## Task Catalog

| Task | Domain | Difficulty | Key Capability |
|------|--------|------------|----------------|
| 001 — Customer Ticket Triage | Financial Services | Basic | Single-source info extraction, risk sorting |
| 002 — AI Platform Incident Investigation | Technical Operations | Intermediate | Multi-file correlation, confidence estimation |
| 003 — Policy Compliance Check | Enterprise Compliance | Intermediate | Conditional reasoning, edge case handling |
| 004 — Cross-System Data Reconciliation | Finance / Operations | Advanced | Heterogeneous source alignment, discrepancy detection |
| 005 — Conflicting Requirements Resolution | Project Management | Intermediate | Ambiguity resolution, constraint-based decision making |
| 006 — Multi-Source Report Synthesis | Business Intelligence | Advanced | Multi-source synthesis, critical data evaluation |
```

- [ ] **Step 3: Verify all tests pass**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest discover tests -v
```
Expected: All tests PASS (contract tests + skill.json alignment).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README with full v1 task catalog and package shape"
```

---

### Task 14: Final Integration — Run All Tests

- [ ] **Step 1: Run full test suite**

```bash
cd /Users/hai/Projects/agent-readiness-eval && python3 -m unittest discover tests -v
```
Expected: All tests PASS.

- [ ] **Step 2: Verify directory structure**

```bash
find /Users/hai/Projects/agent-readiness-eval/tasks -type f | sort
```
Expected: All 6 task directories with task.md, inputs/, output-requirements.md, and evaluator-notes/ (where applicable).

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: complete v1 benchmark — 6 tasks across 5 domains with veto-layer scoring"
```
