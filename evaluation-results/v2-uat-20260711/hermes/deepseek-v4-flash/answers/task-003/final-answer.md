# Task 003: Policy-Constrained Decision — UAT Answer (v2.0.0)

## Executive Summary

Four requests were evaluated against three internal policies (POL-DAT-2025, POL-PRC-2025, POL-TRV-2025). One request is APPROVED (travel to KubeCon), one is HELD (procurement needs CFO approval), one is REJECTED (data export requester explicitly refuses DPO approval and audit logging), and one is ESCALATED (subpoena response requires joint Legal + DPO review under the legal compliance exemption).

## Per-Request Decision Report

---

### Request: DAT-2025-007 — Customer Churn Data Export (Liu Fang, BI)

| Field | Value |
|-------|-------|
| **Request ID** | DAT-2025-007 |
| **Type** | Data Export (Confidential, Bulk) |
| **Applicable Policies** | POL-DAT-2025 §§2, 3, 5 |
| **Decision** | REJECT |
| **Satisfied Conditions** | Purpose specified, recipient specified, encrypted transfer requested |
| **Unmet Conditions** | DPO pre-approval not obtained and explicitly refused; audit logging demanded to be disabled; DPO consulted and declined to approve |
| **Applicable Exceptions** | None applicable — legal compliance exemption (POL-DAT-2025 §5) requires subpoena/court order; this is a business analytics request |
| **Exception Scope** | N/A |
| **Reason** | The requester acknowledges that DPO pre-approval and audit logging are mandatory under §3, but explicitly states they will not obtain DPO approval and requests audit logging be disabled. This is a non-waivable policy violation — the requester is not requesting an extension or help with prerequisites; they are demanding bypass of mandatory compliance controls. Per the decision framework, a requester who acknowledges a policy requirement and explicitly refuses to comply is submitting a REJECT-eligible request. Additionally, the DPO has already been consulted and has declined. |
| **Required Next Action** | The requester may submit a revised request that complies with DPO pre-approval and audit logging requirements. This is not a HOLD because the current submission explicitly and knowingly refuses mandatory policy conditions. |

---

### Request: DAT-2025-008 — Subpoena Response (Wang Peng, Legal)

| Field | Value |
|-------|-------|
| **Request ID** | DAT-2025-008 |
| **Type** | Data Export (Confidential, Legal Compliance) |
| **Applicable Policies** | POL-DAT-2025 §§3, 5 |
| **Decision** | ESCALATE |
| **Satisfied Conditions** | Purpose (subpoena response), recipient, encrypted transfer, subpoena document attached |
| **Unmet Conditions** | DPO pre-approval not yet obtained; deletion date not determined |
| **Applicable Exceptions** | POL-DAT-2025 §5: Legal compliance requests (subpoena, court order) may override Confidential data restrictions |
| **Exception Scope** | The exemption overrides Confidential data handling restrictions (DPO approval for Confidential data access) for subpoena compliance, but the exemption itself requires "reviewed by Legal + DPO jointly." The joint review has not occurred. The standard DPO pre-approval process from §3 is superseded by the joint-review process in §5 when a legal compliance request is involved. |
| **Reason** | This is a bona fide subpoena with attached court documentation. The legal compliance exemption in §5 applies, which overrides the Confidential data restrictions and replaces the standard DPO pre-approval with a Legal + DPO joint review. The joint review has not been completed. The 7-day court deadline creates time sensitivity but does not waive the joint review requirement. |
| **Required Next Action** | Escalate to joint Legal + DPO review. The Legal department (Wang Peng) should convene a joint review with the DPO to approve the export under the legal compliance exemption. Timeline should be expedited due to the 7-day court deadline. |

---

### Request: PRC-2025-018 — AnalyticsPro SaaS Subscription (Chen Mei, Marketing)

| Field | Value |
|-------|-------|
| **Request ID** | PRC-2025-018 |
| **Type** | Procurement (SaaS Subscription > 50,000 CNY) |
| **Applicable Policies** | POL-PRC-2025 §§2, 3, 4, 5 |
| **Decision** | HOLD |
| **Satisfied Conditions** | Vendor on approved vendor list (✓ §3), Department head approved (✓ §2), CEO written approval attached (✓ — activates §5 exemption for competitive bidding) |
| **Unmet Conditions** | CFO approval not yet obtained (required for > 50,000 CNY under §2); Procurement committee not yet convened (implied by CFO approval process) |
| **Applicable Exceptions** | POL-PRC-2025 §5: CEO written approval exempts from competitive bidding requirements |
| **Exception Scope** | The CEO exemption waives only the competitive bidding requirement (§2, bullet 3). It does NOT waive CFO approval (§2, bullet 3), the vendor security review (§3), the legal review for FOSS (§4), or the annual review clause for SaaS contracts (§4). The 12-month subscription term does not trigger the "> 12 months" annual review clause, but the auto-renewal provision could extend the term beyond 12 months — this ambiguity should be clarified in the contract. |
| **Reason** | The CEO's written approval exempts competitive bidding but CFO approval is still required by policy for expenditures > 50,000 CNY. The 8,000 CNY onboarding/training package is part of the total 53,000 CNY. The auto-renewal clause may trigger the annual review requirement under §4 for subscriptions extending beyond 12 months. |
| **Required Next Action** | Obtain CFO approval. Clarify whether the auto-renewal provision creates an effective term > 12 months, and if so, add an annual review clause to the contract. |

---

### Request: TRV-2025-042 — KubeCon Europe 2025 (Li Wei, Engineering)

| Field | Value |
|-------|-------|
| **Request ID** | TRV-2025-042 |
| **Type** | Travel (International) |
| **Applicable Policies** | POL-TRV-2025 §§2, 3, 4, 5 |
| **Decision** | APPROVE |
| **Satisfied Conditions** | VP approval obtained for international travel (✓ §2); Economy flight (✓ §3, no business class issue); Hotel 1,200/night ≤ 1,500 international limit (✓ §3); Per diem 400/day = international rate (✓ §3); Receipts for all items > 200 CNY (✓ §4 — flight, hotel, registration all have receipts; per diem is N/A as it's a daily allowance not a reimbursable expense requiring receipt); Manager approval (✓) |
| **Unmet Conditions** | None |
| **Applicable Exceptions** | None needed — all conditions satisfied under standard policy |
| **Exception Scope** | N/A |
| **Reason** | All conditions of POL-TRV-2025 are satisfied for this international business trip. VP approval is present (required for international travel and for > 5,000 CNY). Receipts are provided for all items exceeding the 200 CNY receipt threshold. Hotel and per diem are within the international limits. No exemptions needed. |
| **Required Next Action** | Process reimbursement. |
