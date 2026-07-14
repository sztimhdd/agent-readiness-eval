# Task 003: Policy-Constrained Decision — Final Answer

## Executive Summary

Four requests were evaluated against three policies (POL-DAT-2025, POL-PRC-2025, POL-TRV-2025). One request was APPROVED (TRV-2025-042 — international travel with all conditions met), two were placed on HOLD (DAT-2025-008 — pending joint Legal + DPO review for a legal subpoena; PRC-2025-018 — pending CFO approval for a purchase exceeding 50K CNY with CEO competitive-bidding exemption), and one was REJECTED (DAT-2025-007 — the requester explicitly refused to obtain mandatory DPO approval and demanded audit logging be disabled after the DPO declined to approve).

## Per-Request Decision Report

### DAT-2025-007 — Data Export (Churn Analysis)

- **Request ID:** DAT-2025-007
- **Type:** Confidential data export, bulk (>100 records)
- **Applicable Policies:** POL-DAT-2025
- **Decision:** REJECT
- **Satisfied Conditions:** Export details specified (purpose, recipient, retention, deletion); encrypted transfer requested
- **Unmet Conditions:** DPO approval not obtained (required for Confidential data per §2); bulk export DPO pre-approval missing (§3); audit logging not enabled (§3)
- **Applicable Exceptions:** None
- **Exception Scope:** N/A
- **Reason:** The requester acknowledges that DPO pre-approval and audit logging are mandatory under POL-DAT-2025 §3 but explicitly refuses to comply with both requirements and demands audit logging be disabled. The DPO has been consulted and declined to approve. Per the decision framework, a requester who acknowledges a policy requirement and explicitly refuses to comply is submitting a REJECT-eligible request, not a HOLD case.
- **Required Next Action:** Submit a revised request with DPO approval obtained and audit logging enabled.

### DAT-2025-008 — Data Export (Legal Subpoena)

- **Request ID:** DAT-2025-008
- **Type:** Confidential data export, legal compliance (subpoena)
- **Applicable Policies:** POL-DAT-2025
- **Decision:** HOLD
- **Satisfied Conditions:** Export details specified (purpose, recipient, retention); encrypted transfer required; subpoena document attached
- **Unmet Conditions:** Joint Legal + DPO review not yet completed (§5 exemption pathway); deletion date not specified
- **Applicable Exceptions:** POL-DAT-2025 §5 — Legal compliance requests (subpoena, court order) may override Confidential data restrictions, subject to joint Legal + DPO review
- **Exception Scope:** The subpoena from Beijing Municipal Court (Case #BJ-2025-0287) triggers the §5 legal compliance exemption. This overrides the standard DPO-only approval requirement for Confidential data, replacing it with a joint Legal + DPO review. The exemption does not eliminate the review requirement — it changes who must participate.
- **Reason:** Valid legal compliance request supported by a court subpoena. The §5 exemption applies, modifying the approval path to a joint Legal + DPO review. DPO approval has been requested but the joint review has not been completed.
- **Required Next Action:** Complete joint Legal + DPO review per §5. Specify deletion date for the export. Court deadline is 7 days.

### PRC-2025-018 — Procurement (AnalyticsPro SaaS)

- **Request ID:** PRC-2025-018
- **Type:** Software procurement, 53,000 CNY total
- **Applicable Policies:** POL-PRC-2025
- **Decision:** HOLD
- **Satisfied Conditions:** Department head approval obtained; vendor on approved list; CEO written approval attached (exempts competitive bidding per §5)
- **Unmet Conditions:** CFO approval required for purchases >50,000 CNY (§2)
- **Applicable Exceptions:** POL-PRC-2025 §5 — CEO-written approval exempts from competitive bidding requirements
- **Exception Scope:** CEO written approval exempts competitive bidding only. It does not exempt CFO approval for the >50,000 CNY threshold. The exemption scope is limited to the competitive bidding clause in §2.
- **Reason:** Total purchase (53,000 CNY) exceeds 50,000 CNY threshold, requiring CFO approval. CEO exemption covers competitive bidding but does not substitute for CFO approval. SaaS subscription is exactly 12 months, not exceeding the >12-month threshold for mandatory annual review clause.
- **Required Next Action:** Obtain CFO approval for the 53,000 CNY purchase.

### TRV-2025-042 — Travel Reimbursement (KubeCon Europe)

- **Request ID:** TRV-2025-042
- **Type:** International business travel reimbursement
- **Applicable Policies:** POL-TRV-2025
- **Decision:** APPROVE
- **Satisfied Conditions:** VP approval obtained (required for international travel and >5,000 CNY total); manager approval obtained; economy-class flight booked; hotel 1,200 CNY/night within international rate limit (1,500 CNY/night); per diem 400 CNY/day at international rate limit; receipts provided for all individual expenses >200 CNY
- **Unmet Conditions:** None
- **Applicable Exceptions:** None
- **Exception Scope:** N/A
- **Reason:** All policy conditions satisfied. International travel with VP approval, all expenses within applicable rate limits, and receipts provided for reimbursable items above the 200 CNY threshold.
- **Required Next Action:** N/A
