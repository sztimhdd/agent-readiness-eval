# Task 003 — Reference Analysis (Evaluator Only)

## Target Decisions

| Request ID | Target Decision | Key Scenario |
|------------|-----------------|--------------|
| TRV-2025-042 | APPROVE | International travel, VP approval obtained, all expenses within policy limits |
| PRC-2025-018 | HOLD | CEO exempts competitive bidding; CFO approval still needed, SaaS annual review clause still missing from contract — both fixable through normal workflow |
| DAT-2025-007 | REJECT | Requester explicitly demands bypassing DPO pre-approval and audit logging; bulk Confidential data export |
| DAT-2025-008 | ESCALATE | Subpoena provides legal basis, policy requires Legal + DPO joint review before execution |

## TRV-2025-042: APPROVE
- Total 18,500 CNY > 5,000 CNY → VP approval required (POL-TRV-2025 §2)
- International travel → VP approval required regardless of amount (§2)
- VP approval: Approved (Zhao Wen, 2025-03-05) ✓
- Hotel 1,200 CNY/night ≤ 1,500 international limit ✓
- Per diem 400 CNY/day = international rate ✓
- Receipts for all expenses > 200 CNY ✓ (flight, hotel, conference; per diem N/A)
- No exceptions needed — all conditions satisfied

## PRC-2025-018: HOLD
- Total 53,000 CNY > 50,000 CNY → normally CFO + competitive bidding required (§2)
- CEO written approval attached → competitive bidding exempt (§5 exemption)
- SaaS 12-month subscription → annual review clause required in contract (§4) → MISSING
- CFO approval still needed → NOT OBTAINED
- Valid exception: CEO exemption (competitive bidding only — §5)
- Two unmet conditions can be resolved through normal workflow: CFO approval and annual review clause. Hence HOLD, not REJECT.

## DAT-2025-007: REJECT
- Confidential data (customer PII) → DPO approval required (§2)
- DPO approval not obtained — requester actively seeks to bypass it
- Bulk export >100 records → DPO pre-approval + audit logging required (§3)
- Requester explicitly requests exemption from both DPO pre-approval and audit logging
- No applicable policy exemption covers bypassing DPO pre-approval or audit logging for Confidential data
- This is REJECT because the request violates non-waivable policy requirements

## DAT-2025-008: ESCALATE
- Confidential data (financial records) → DPO approval would normally be required (§2)
- Legal compliance request (subpoena, Case BJ-2025-0287) → §5 exemption applies
- Policy §5: "Legal compliance requests (subpoena, court order) may override Confidential data restrictions — must be reviewed by Legal + DPO jointly"
- Legal counsel has initiated the request, but DPO joint review has not occurred
- This requires ESCALATE to Legal + DPO joint review, not direct approval or HOLD

## VETO Conditions

The following errors MUST result in a score cap of 50 or rejection of the answer entirely:

1. **Incorrectly expanding CEO exemption** — CEO exemption on PRC-2025-018 covers competitive bidding only (§5). Approving the request based solely on CEO approval, while CFO approval and annual review clause remain missing, is wrong.
2. **Approving DAT-2025-007** — The requester explicitly bypasses DPO pre-approval and audit logging. No policy exemption covers this.
3. **Directly approving DAT-2025-008 without escalation** — Policy requires Legal + DPO joint review. Direct approval skips the mandatory review process.
4. **Rejecting all incomplete requests as REJECT without distinguishing HOLD** — PRC-2025-018 has fixable conditions that make it HOLD, not REJECT.
5. **Leaving joint-review cases at HOLD without ESCALATE** — DAT-2025-008 requires transfer to a joint review body, not a simple hold for missing documents.
6. **Citing non-existent policy clauses or request IDs** — All citations must reference actual policy sections and request IDs from the provided documents.
7. **Output decision contradicts reason or required_next_action** — The reason and required_next_action must be consistent with the decision.
