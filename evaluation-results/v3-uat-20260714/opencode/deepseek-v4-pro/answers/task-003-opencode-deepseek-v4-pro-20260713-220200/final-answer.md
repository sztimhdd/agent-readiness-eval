# Task 003: Policy-Constrained Decision — Final Answer

## Executive Summary

Four employee requests were evaluated against three company policies (Data Handling POL-DAT-2025, Procurement POL-PRC-2025, Travel POL-TRV-2025). One request (TRV-2025-042, international travel) was APPROVED as all conditions are satisfied. Two requests (DAT-2025-008, legal subpoena data export; PRC-2025-018, procurement with pending approvals) were placed on HOLD pending missing documents and approvals. One request (DAT-2025-007, data export with explicit refusal to comply with mandatory DPO approval) was REJECTED for non-waivable policy violation. No requests required escalation.

## Per-Request Decision Report

### DAT-2025-007 — Data Export (Liu Fang, Business Intelligence)

- **Request Type**: Data export — Confidential customer PII
- **Applicable Policies**: POL-DAT-2025
- **Decision**: **REJECT**
- **Satisfied Conditions**: Purpose specified (Q1 churn analysis); recipient specified (internal); format and retention period defined; encrypted transfer requested
- **Unmet Conditions**: DPO approval not obtained and requester explicitly refuses to obtain it (POL-DAT-2025 §3 — bulk exports >100 records require DPO pre-approval); audit logging demanded to be disabled by requester (POL-DAT-2025 §3 — bulk exports require audit logging)
- **Applicable Exceptions**: None. Legal compliance exemption (POL-DAT-2025 §5) does not apply — this is not a subpoena or court order. No other exemption in POL-DAT-2025 covers this request.
- **Exception Scope**: N/A
- **Reason**: The request is a bulk export of 50,000 Confidential records. POL-DAT-2025 §3 requires DPO pre-approval and audit logging for bulk exports. The requester acknowledges these requirements but explicitly refuses to comply, demanding both that DPO approval be bypassed and that audit logging be disabled. The DPO has already consulted and declined to approve. Under the REJECT criteria: "A requester who acknowledges a policy requirement and explicitly refuses to comply (e.g., demanding bypass of mandatory DPO approval) is not making a HOLD case; they are submitting a REJECT-eligible request." A revised submission with proper DPO approval may be considered separately.
- **Required Next Action**: Requester must obtain DPO approval and agree to audit logging before resubmitting.

### DAT-2025-008 — Data Export (Wang Peng, Legal)

- **Request Type**: Data export — Confidential financial records, legal subpoena response
- **Applicable Policies**: POL-DAT-2025
- **Decision**: **HOLD**
- **Satisfied Conditions**: Purpose specified (subpoena response, case #BJ-2025-0287); recipient specified (internal then to court); retention period defined (until case resolution); encrypted transfer required; subpoena document attached
- **Unmet Conditions**: DPO approval is requested but not yet obtained (POL-DAT-2025 §3 — bulk export >100 records requires DPO pre-approval; estimated 2,000 records)
- **Applicable Exceptions**: POL-DAT-2025 §5 — Legal compliance requests (subpoena, court order) may override Confidential data restrictions, but must be reviewed by Legal + DPO jointly. Deletion date is not yet determined (acceptable given pending case resolution).
- **Exception Scope**: The Legal compliance exemption allows this export to proceed despite being classified as Confidential data. However, the exemption explicitly requires joint review by Legal + DPO — it does not bypass the DPO entirely. The DPO is not approving content restrictions; they are part of the required joint review process.
- **Reason**: The subpoena provides a valid legal basis for the export under POL-DAT-2025 §5. However, the joint Legal + DPO review required by the exemption has not yet been completed — DPO approval is still pending. All other elements (purpose, encrypted transfer, subpoena documentation) are in order. The 7-day court deadline allows time for the required approvals to be obtained through normal workflow.
- **Required Next Action**: Complete the joint Legal + DPO review and obtain DPO approval. Deletion date should be confirmed once case resolution timeline is determined.

### PRC-2025-018 — Procurement (Chen Mei, Marketing Director)

- **Request Type**: Procurement — AnalyticsPro SaaS subscription
- **Applicable Policies**: POL-PRC-2025
- **Decision**: **HOLD**
- **Satisfied Conditions**: Department head approval obtained; vendor is on approved vendor list; purchase purpose specified
- **Unmet Conditions**: (1) CFO approval required — total 53,000 CNY exceeds 50,000 CNY threshold (POL-PRC-2025 §2); (2) VP approval still pending (POL-PRC-2025 §2); (3) Contract lacks annual review clause — SaaS subscription with auto-renewal requires annual review clause (POL-PRC-2025 §4)
- **Applicable Exceptions**: CEO written approval exempts from competitive bidding requirements only (POL-PRC-2025 §5: "Purchases approved in writing by the CEO are exempt from competitive bidding requirements"). The CEO's "Approved. Expedite." note does not extend to waiving CFO approval or VP approval — the exemption scope is explicitly limited to competitive bidding.
- **Exception Scope**: CEO exemption waives competitive bidding requirement. It does not waive: CFO approval for >50K purchases, VP approval for 10K-50K purchases, or contract review clause requirements.
- **Reason**: The CEO exemption removes the competitive bidding obligation but does not substitute for the separately required CFO approval (POL-PRC-2025 §2). VP approval remains pending, and the contract must be amended to include an annual review clause as required by POL-PRC-2025 §4 for SaaS subscriptions exceeding 12 months. All three gaps are remediable through normal workflow.
- **Required Next Action**: Obtain VP approval; obtain CFO approval; amend contract to include annual review clause per POL-PRC-2025 §4.

### TRV-2025-042 — Travel Reimbursement (Li Wei, Senior Engineer)

- **Request Type**: Travel reimbursement — International conference (KubeCon Europe, Paris)
- **Applicable Policies**: POL-TRV-2025
- **Decision**: **APPROVE**
- **Satisfied Conditions**: International travel — VP approval obtained (POL-TRV-2025 §2); total expenses >5,000 CNY — VP approval obtained (POL-TRV-2025 §2); economy-class flight (POL-TRV-2025 §3); hotel at 1,200 CNY/night, within international limit of 1,500 CNY/night (POL-TRV-2025 §3); per diem at 400 CNY/day, within international limit (POL-TRV-2025 §3); receipts provided for flight, hotel, and conference registration — all >200 CNY (POL-TRV-2025 §4); manager approval obtained
- **Unmet Conditions**: None
- **Applicable Exceptions**: None needed — all standard policy conditions are met
- **Exception Scope**: N/A
- **Reason**: All required conditions are met under POL-TRV-2025. International travel VP approval obtained. Total amount (18,500 CNY) properly approved at VP level. All expenses within policy limits. All required receipts attached.
- **Required Next Action**: None — request may proceed.
