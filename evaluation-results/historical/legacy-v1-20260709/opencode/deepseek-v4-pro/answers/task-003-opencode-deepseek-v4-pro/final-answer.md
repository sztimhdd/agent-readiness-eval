# Policy Compliance Check — Task 003

## Executive Summary

Four requests were reviewed against three internal policies (Travel, Procurement, Data Handling). One request is non-compliant (TRV-2025-042 — missing VP approval for international travel exceeding 5,000 CNY), one is non-compliant with a specific finding (PRC-2025-018 — contract lacks required annual review clause despite correctly applying CEO competitive bidding exemption), one is non-compliant (DAT-2025-007 — missing DPO approval for Confidential PII export), and one is compliant via legal exemption (DAT-2025-008 — subpoena overrides standard DPO requirement). All policy references cite exact section numbers from the provided policy documents.

## Per-Request Compliance Report

### TRV-2025-042 (Travel Reimbursement)

**Type:** Travel
**Applicable Policies:** POL-TRV-2025
**Compliance Status:** Non-Compliant

**Findings:**
1. **POL-TRV-2025 §2 — Total exceeds 5,000 CNY without VP approval.** Total expenses: 18,500 CNY. Manager approved but VP approval is "Pending." VP-level approval is required for amounts > 5,000 CNY. Severity: High.
2. **POL-TRV-2025 §2 — International travel requires VP approval regardless of amount.** This is international travel (Paris). Even if the total were under 5,000 CNY, VP approval would still be required. Severity: High.

**Compliant items:** Flight is economy class (§3). Hotel 1,200 CNY/night is within international limit of 1,500 CNY/night (§3). Per diem 400 CNY/day matches international rate (§3). All expenses > 200 CNY have receipts (§4). No exemption applies — CEO approval is marked N/A.

### PRC-2025-018 (Procurement)

**Type:** Procurement
**Applicable Policies:** POL-PRC-2025
**Compliance Status:** Non-Compliant (partial — one exemption correctly applied, one finding remains)

**Findings:**
1. **POL-PRC-2025 §2 — Total > 50,000 CNY requires CFO approval + competitive bidding.** Total: 53,000 CNY. **Exemption applied: POL-PRC-2025 §5 — CEO written approval exempts from competitive bidding.** CEO Wang provided written approval on 2025-03-02. Competitive bidding requirement is waived. However, CFO approval is still required (CEO exemption only covers competitive bidding, not CFO approval). Severity: Medium.
2. **POL-PRC-2025 §4 — SaaS subscription > 12 months requires annual review clause.** Contract term is 12 months with auto-renewal. No annual review clause is present in the contract draft. Severity: Medium.

**Compliant items:** Vendor AnalyticsPro Inc. is on approved vendor list (§3). Software is license-compliant.

### DAT-2025-007 (Data Export)

**Type:** Data Export
**Applicable Policies:** POL-DAT-2025
**Compliance Status:** Non-Compliant

**Findings:**
1. **POL-DAT-2025 §2 — Confidential data export requires DPO approval.** Data classification is Confidential (customer PII: names, emails, payment history). DPO approval is "Not yet obtained." Severity: High.
2. **POL-DAT-2025 §3 — Bulk export >100 records requires DPO pre-approval and audit logging.** Estimated 50,000 records. DPO not approved. Severity: High.

**Compliant items:** Export specifies purpose, recipient, retention period (30 days), and deletion date (2025-04-30) (§3). Encrypted transfer requested (§3).

### DAT-2025-008 (Data Export — Legal)

**Type:** Data Export (Legal Compliance)
**Applicable Policies:** POL-DAT-2025
**Compliance Status:** Compliant (Exemption Applied)

**Findings:**
1. **POL-DAT-2025 §2 — Confidential data export normally requires DPO approval.** Data classification is Confidential (financial transaction records). DPO approval is "Requested but not yet obtained." **Exemption applied: POL-DAT-2025 §5 — Legal compliance requests (subpoena, court order) may override Confidential data restrictions.** A subpoena from Beijing Municipal Court (Case #BJ-2025-0287) is attached. The export is justified under the legal compliance exemption.
   **Note:** The §5 exemption requires joint review by Legal + DPO. DPO review is still pending and should be expedited given the 7-day court deadline.

## Summary Table

| Rank | Request ID | Finding | Policy Ref | Severity |
|:----:|------------|---------|------------|:--------:|
| 1 | DAT-2025-007 | Missing DPO approval for Confidential PII export (50,000 records) | POL-DAT-2025 §2, §3 | High |
| 2 | TRV-2025-042 | Missing VP approval for international travel exceeding 5,000 CNY | POL-TRV-2025 §2 | High |
| 3 | PRC-2025-018 | Contract lacks annual review clause (SaaS > 12 months) | POL-PRC-2025 §4 | Medium |
| 4 | PRC-2025-018 | CFO approval still required (CEO exemption covers bidding only) | POL-PRC-2025 §2 | Medium |
