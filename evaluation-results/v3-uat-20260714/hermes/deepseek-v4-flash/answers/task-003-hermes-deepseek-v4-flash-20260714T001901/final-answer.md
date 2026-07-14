# Policy-Constrained Decision Report

## Executive Summary

Four employee requests were evaluated against three company policies (Procurement, Data Handling, Travel). One request is approved (travel to KubeCon Europe), one is held pending additional approval (procurement missing CFO sign-off), one is rejected for explicit refusal to comply with mandatory data protection requirements, and one is escalated for joint Legal + DPO review under a legal compliance exemption.

---

## Per-Request Decision Report

### Request 1: PRC-2025-018 — AnalyticsPro SaaS Subscription

| Field | Value |
|-------|-------|
| **Request ID** | PRC-2025-018 |
| **Type** | Software procurement |
| **Applicable Policies** | POL-PRC-2025 (Procurement) |
| **Decision** | **HOLD** |
| **Satisfied Conditions** | Department head approval obtained; vendor on approved list; CEO written approval waives competitive bidding |
| **Unmet Conditions** | CFO approval still required (>50,000 tier, POL-PRC-2025 §2) |
| **Applicable Exceptions** | POL-PRC-2025 §5 — CEO approval exempts competitive bidding; limited to that requirement only |
| **Reason** | Total 53,000 CNY exceeds the 50,000 threshold, triggering CFO approval + competitive bidding. The CEO exemption waives competitive bidding but does not waive CFO approval per §2. CFO sign-off must be obtained before proceeding. |
| **Required Next Action** | Obtain CFO approval with the CEO note attached. |

### Request 2: DAT-2025-007 — Customer Churn Data Export

| Field | Value |
|-------|-------|
| **Request ID** | DAT-2025-007 |
| **Type** | Bulk Confidential data export |
| **Applicable Policies** | POL-DAT-2025 (Data Handling) |
| **Decision** | **REJECT** |
| **Satisfied Conditions** | Purpose, recipient, retention period, deletion date specified; encrypted transfer requested |
| **Unmet Conditions** | DPO pre-approval not obtained and explicitly refused; audit logging requested to be disabled; DPO already declined |
| **Applicable Exceptions** | None |
| **Reason** | The requester acknowledges mandatory DPO pre-approval and audit logging requirements under POL-DAT-2025 §3 but explicitly refuses to comply (will not obtain DPO approval, requests audit logging disabled). The DPO has been consulted and has declined. Per the decision framework, a requester who acknowledges policy requirements and explicitly refuses to comply is submitting a REJECT-eligible submission. |
| **Required Next Action** | Reject current submission. Requester may submit a new request that complies with DPO pre-approval and audit logging. |

### Request 3: DAT-2025-008 — Subpoena Compliance Export

| Field | Value |
|-------|-------|
| **Request ID** | DAT-2025-008 |
| **Type** | Legal compliance data export (subpoena) |
| **Applicable Policies** | POL-DAT-2025 (Data Handling) |
| **Decision** | **ESCALATE** |
| **Satisfied Conditions** | Purpose (court order), recipient (Legal then court), encrypted PDF format; subpoena document attached |
| **Unmet Conditions** | DPO approval requested but not yet obtained |
| **Applicable Exceptions** | POL-DAT-2025 §5 — Legal compliance requests may override Confidential restrictions but require joint Legal + DPO review |
| **Reason** | This is a legal compliance request (subpoena) for Confidential financial records (~2,000 records). Under §5, standard DPO-only pre-approval is supplemented by a joint Legal + DPO review. The requester (Legal Counsel) fulfills the Legal side, but DPO review is still pending. The court-mandated 7-day deadline adds urgency and requires escalation to ensure timely joint review. |
| **Required Next Action** | Escalate to the joint Legal + DPO review body with the subpoena and 7-day deadline flagged. |

### Request 4: TRV-2025-042 — KubeCon Europe Travel Reimbursement

| Field | Value |
|-------|-------|
| **Request ID** | TRV-2025-042 |
| **Type** | International travel reimbursement |
| **Applicable Policies** | POL-TRV-2025 (Travel) |
| **Decision** | **APPROVE** |
| **Satisfied Conditions** | VP approval (required for international travel and for >5,000); economy flight; hotel within international limit (1,200 ≤ 1,500); per diem at correct rate (400/day); receipts for all >200 items |
| **Unmet Conditions** | None |
| **Applicable Exceptions** | None |
| **Reason** | All policy conditions are met. International travel to KubeCon Europe (Paris) at 18,500 CNY total. VP approval obtained. Economy flight. Hotel 1,200/night within the 1,500 international cap. Per diem at 400/day matches the international rate. Receipts provided for all expenses >200 CNY (flight, hotel, conference). Per diem is a daily allowance and does not require a receipt. |
| **Required Next Action** | Process reimbursement. |
