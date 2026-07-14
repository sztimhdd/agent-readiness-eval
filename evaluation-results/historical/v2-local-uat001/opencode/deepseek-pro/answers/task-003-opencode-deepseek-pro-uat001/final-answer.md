# Task 003: Policy-Constrained Decision — Final Answer

## Executive Summary

Four employee requests were evaluated against three internal policies (Data Handling POL-DAT-2025, Procurement POL-PRC-2025, Travel POL-TRV-2025). One request (TRV-2025-042) fully satisfies all policy conditions and is APPROVED. Two requests (DAT-2025-007, PRC-2025-018) are placed on HOLD due to missing approvals that are remediable through normal workflow. One request (DAT-2025-008) is ESCALATED because the legal compliance exemption in POL-DAT-2025 §5 requires mandatory joint review by Legal and DPO before any execution decision can be made — this is a policy-mandated boundary the first-line reviewer cannot cross. No requests are REJECTED, though DAT-2025-007's claimed exemption from DPO pre-approval is denied as having no policy basis.

## Per-Request Decision Report

### TRV-2025-042 — Travel Reimbursement (Li Wei)

- **Decision**: APPROVE
- **Applicable Policies**: POL-TRV-2025
- **Satisfied Conditions**: Manager approved; VP approved (required for international travel and expenses >5,000 CNY); economy-class flight used; hotel within international rate limit (1,200 CNY/night ≤ 1,500 CNY/night); per diem at standard international rate (400 CNY/day); receipts attached for flight, hotel, and conference registration.
- **Unmet Conditions**: None
- **Applicable Exceptions**: None
- **Reason**: All policy conditions are met. VP approval satisfies both the international travel requirement and the >5,000 CNY threshold. All expenses are within allowable limits with required receipts.

### DAT-2025-007 — Data Export (Liu Fang)

- **Decision**: HOLD
- **Applicable Policies**: POL-DAT-2025
- **Satisfied Conditions**: Purpose specified; recipient identified (internal); retention period specified (30 days); deletion date specified (2025-04-30); encrypted transfer requested.
- **Unmet Conditions**: DPO approval not obtained (required for Confidential data); DPO pre-approval not obtained (required for bulk export >100 records); audit logging not arranged (required for bulk export).
- **Applicable Exceptions**: None — the requester's claimed exemption from DPO pre-approval citing tight reporting deadlines has no basis in POL-DAT-2025 §5. Exemptions exist only for legal compliance requests and Restricted data has none.
- **Reason**: Bulk export of Confidential data (~50,000 records) requires DPO pre-approval and audit logging under §3. The requested exemption is denied — policy provides no business-deadline exemption for Confidential data exports. The underlying export is potentially allowable once the three missing prerequisites are supplied through normal workflow.
- **Required Next Action**: Requester must obtain DPO pre-approval, arrange audit logging, and secure DPO approval before resubmitting. Exemption request is denied.

### DAT-2025-008 — Data Export (Wang Peng, Legal Counsel)

- **Decision**: ESCALATE
- **Applicable Policies**: POL-DAT-2025
- **Satisfied Conditions**: Purpose specified (court subpoena); recipient identified; encrypted transfer required; subpoena document attached; court case reference provided; deletion date rationale stated (until case resolution).
- **Unmet Conditions**: DPO approval not yet obtained; deletion date not yet determined; Data Processing Agreement (DPA) may be required for third-party sharing with the court.
- **Applicable Exceptions**: POL-DAT-2025 §5 — legal compliance requests (subpoena, court order) may override Confidential data restrictions, subject to mandatory Legal + DPO joint review.
- **Exception Scope**: The exemption covers Confidential data restrictions that would normally require standalone DPO pre-approval. However, it does not waive the joint review requirement itself — policy explicitly mandates that Legal + DPO review the case jointly before any override takes effect.
- **Reason**: This is a valid legal compliance request (subpoena) that may qualify for the §5 exemption. However, the policy-boundary rule is explicit: Legal + DPO must review jointly. The first-line reviewer lacks authority to approve, reject, or hold this request; it must be transferred to the joint review authority.
- **Required Next Action**: ESCALATE to Legal + DPO joint review. They must determine: (1) whether the subpoena is valid and complete, (2) whether the export scope is proportionate to the court order, (3) whether a DPA with the court is required, (4) appropriate data retention and deletion timeline, and (5) final approval for encrypted transfer to the court.

### PRC-2025-018 — Procurement (Chen Mei, Marketing Director)

- **Decision**: HOLD
- **Applicable Policies**: POL-PRC-2025
- **Satisfied Conditions**: Department head approved (Chen Mei, 2025-03-01); vendor on approved vendor list (AnalyticsPro Inc.); CEO written approval waives competitive bidding requirement (POL-PRC-2025 §5); third year using vendor (no new vendor security review needed).
- **Unmet Conditions**: VP approval pending (required for purchases >10,000 CNY); procurement committee review not convened (required for purchases 10,001-50,000 CNY); CFO approval not obtained (required for purchases >50,000 CNY). Contract includes auto-renewal without annual review clause — policy §4 requires annual review clause for subscriptions >12 months; contract term is exactly 12 months, so not strictly required, but flagged for review given auto-renewal mechanism.
- **Applicable Exceptions**: CEO written approval exempts from competitive bidding (POL-PRC-2025 §5).
- **Exception Scope**: The CEO waiver applies strictly to competitive bidding. It does not waive VP approval, procurement committee review, or CFO approval — these remain required under their respective threshold tiers (§2).
- **Reason**: Total purchase of 53,000 CNY triggers three approval tiers. The CEO waiver covers competitive bidding only. All other missing approvals are remediable through the normal procurement workflow.
- **Required Next Action**: Requester must obtain: (1) VP approval for the 10K-50K tier, (2) convene procurement committee for review, (3) CFO approval for the >50K tier. Recommend adding annual review clause to contract given auto-renewal language.
