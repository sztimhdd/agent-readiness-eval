# Decision Summary — Task 005

| Request | Title | Amount | Decision | Status | Key Rationale | Policy Cited |
|---------|-------|--------|----------|--------|---------------|-------------|
| REQ-001 | Standard Office Supply Order | 3,200 | APPROVE | approved | Under 5K, dept_head + procurement approved, valid cost center | POL-PRC-001 §1 |
| REQ-002 | Marketing Event Catering | 4,500 | APPROVE | approved | Under 5K, dept_head + procurement approved, valid cost center, vendor quotes attached | POL-PRC-001 §1 |
| REQ-003 | Server Hardware Upgrade | 85,000 | HOLD (request info) | information_requested | Over 5K needs CFO approval — not yet obtained. Competitive bidding satisfied (3 quotes). Dept head + procurement approved. | POL-PRC-001 §2 |
| REQ-004 | SaaS Platform Renewal | 120,000 | HOLD (request info) | information_requested | Over 5K needs CFO approval. CEO exemption waives bidding only (POL-PRC-002 §2). SaaS requires annual review clause in contract (POL-PRC-002 §3). Both requirements need to be addressed. Note: second information request (annual_review_clause) failed because request is already in information_requested state. | POL-PRC-001 §2, POL-PRC-002 §2-4 |
| REQ-005 | Emergency Equipment Purchase | 75,000 | REJECT | rejected | Requester explicitly demands bypass of mandatory CFO approval (POL-PRC-001 §2). Requester who refuses to comply with mandatory policy requirements is REJECT-eligible. | POL-PRC-001 §2 |
| REQ-006 | Cross-Department Training Platform | 35,000 | ESCALATE | escalated | Budget drawn from 3 departments (HR, Engineering, Marketing). POL-PRC-003 requires mandatory escalation to Cross-Department Budget Committee. Direct approval prohibited. | POL-PRC-003 §1-4 |
