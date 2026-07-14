# Task 003: Policy-Constrained Decision Report

## Executive Summary

Four requests were evaluated against three internal policies (Travel POL-TRV-2025, Procurement POL-PRC-2025, Data Handling POL-DAT-2025). One request (TRV-2025-042) is approved — all travel policy conditions are satisfied including VP approval for international travel. One procurement request (PRC-2025-018) is on HOLD — the CEO exemption waives competitive bidding but CFO approval, VP approval, and procurement committee review remain outstanding and are remediable. One data export (DAT-2025-007) is REJECTED — the requester explicitly refuses mandatory DPO approval and demands audit logging be disabled, which constitutes a non-waivable policy violation. One legal compliance data export (DAT-2025-008) is on HOLD — the subpoena exemption applies but joint Legal+DPO review is still required per §5 of the data policy.

## Per-Request Decision Report

### TRV-2025-042 — Travel Reimbursement (Li Wei, KubeCon Europe)

- **Type:** International travel reimbursement
- **Applicable Policies:** POL-TRV-2025
- **Decision:** APPROVE
- **Satisfied Conditions:**
  - International travel → VP approval required (§2): VP Zhao Wen approved 2025-03-05 ✓
  - Expenses >5,000 CNY → VP approval required (§2): same VP approval covers both ✓
  - Economy-class flights only (§3): economy flight at 8,200 CNY ✓
  - Hotel within international limit of 1,500 CNY/night (§3): 1,200 CNY/night ✓
  - Per diem within international limit of 400 CNY/day (§3): exactly 400 CNY/day ✓
  - Receipts attached for all expenses >200 CNY (§4): flight, hotel, conference registration receipts attached ✓
  - Manager approval: Zhang Wei approved 2025-02-20 ✓
- **Unmet Conditions:** None
- **Applicable Exceptions:** None
- **Reason:** All required conditions under POL-TRV-2025 are satisfied. VP approval is obtained. All expenses fall within policy limits. Receipts are attached for all required items.
- **Required Next Action:** None — request can proceed.

### PRC-2025-018 — Procurement (Chen Mei, AnalyticsPro SaaS)

- **Type:** Software procurement >50,000 CNY
- **Applicable Policies:** POL-PRC-2025
- **Decision:** HOLD
- **Satisfied Conditions:**
  - Vendor on approved vendor list (§3): AnalyticsPro Inc. is listed ✓
  - Department head approval: Chen Mei self-approved ✓
  - CEO written approval attached: waives competitive bidding per §5 exemption ✓
- **Unmet Conditions:**
  - CFO approval required for purchases >50,000 CNY (§2): not obtained
  - VP approval required for purchases 10,001-50,000 CNY (§2): pending
  - Procurement committee review required for purchases 10,001-50,000 CNY (§2): not yet convened
  - Note: the >50,000 CNY threshold is the governing tier, so CFO approval is the primary missing requirement
- **Applicable Exceptions:** CEO written approval (§5): exempts from competitive bidding requirements only. Does not waive CFO approval, VP approval, or procurement committee review.
- **Exception Scope:** Competitive bidding only — the CEO exemption explicitly states "Purchases approved in writing by the CEO are exempt from competitive bidding requirements." It does not extend to any other §2 requirements.
- **Reason:** The total exceeds 50,000 CNY, triggering CFO approval. VP approval is pending and procurement committee has not convened. These are all remediable prerequisites obtainable through normal workflow. The contract term is 12 months (not >12 months), so the annual review clause requirement (§4) does not trigger.
- **Required Next Action:** Obtain CFO approval, complete VP approval, and convene procurement committee review. Competitive bidding is waived by CEO exemption.

### DAT-2025-007 — Data Export (Liu Fang, Customer Churn Analysis)

- **Type:** Bulk confidential data export (~50,000 records)
- **Applicable Policies:** POL-DAT-2025
- **Decision:** REJECT
- **Satisfied Conditions:**
  - Export parameters specified (§3): purpose, recipient, retention period, deletion date ✓
  - Encrypted transfer requested (§3) ✓
- **Unmet Conditions:**
  - DPO approval required for Confidential data (§2): DPO has been consulted and declined
  - Bulk export (>100 records) requires DPO pre-approval + audit logging (§3): requester explicitly demands audit logging be disabled
- **Applicable Exceptions:** None. §5 provides no exemption for deadline pressure or analyst workflow preferences.
- **Exception Scope:** N/A
- **Reason:** The requester explicitly acknowledges the DPO approval and audit logging requirements under POL-DAT-2025 §§2-3 but refuses to comply, demanding both DPO approval bypass and audit logging disablement. The DPO has been consulted and has declined to approve without proper review. Per the role boundary: a requester who acknowledges a policy requirement and explicitly refuses to comply is submitting a REJECT-eligible request, not a HOLD case. No VP or CISO override authorization is attached. Data policy §5 provides no relevant exemption.
- **Required Next Action:** Requester must obtain DPO approval with proper review and accept audit logging as mandatory. A revised submission may be considered separately.

### DAT-2025-008 — Data Export (Wang Peng, Court Subpoena Response)

- **Type:** Legal compliance data export (~2,000 records, subpoena)
- **Applicable Policies:** POL-DAT-2025
- **Decision:** HOLD
- **Satisfied Conditions:**
  - Export parameters specified (§3): purpose, recipient, retention period (estimated) ✓
  - Encrypted transfer required (§3) ✓
  - Subpoena document attached (scanned PDF) for verification ✓
  - Legal review: requester is Legal Counsel (Wang Peng) ✓
- **Unmet Conditions:**
  - DPO approval for Confidential data (§2): requested but not yet obtained
  - Joint Legal+DPO review required by §5 exemption: Legal side covered, DPO side pending
- **Applicable Exceptions:** POL-DAT-2025 §5: "Legal compliance requests (subpoena, court order) may override Confidential data restrictions — must be reviewed by Legal + DPO jointly."
- **Exception Scope:** The exemption overrides standard Confidential data restrictions (§§2-3) for this subpoena response, but the joint Legal+DPO review process itself remains mandatory. The exemption does not waive the review requirement — it redirects it through a different channel.
- **Reason:** The subpoena from Beijing Municipal Court triggers the legal compliance exemption under §5. The requester is Legal Counsel, satisfying the Legal review component. However, DPO review is still required as part of the joint review process mandated by the exemption. DPO approval has been requested but not yet obtained. This is a remediable prerequisite — the DPO review can be completed through normal workflow. The court deadline (7 days) adds urgency but does not waive the DPO requirement.
- **Required Next Action:** Expedite DPO review to complete the joint Legal+DPO assessment required by §5. The court-mandated timeline should be communicated to the DPO for priority handling.
