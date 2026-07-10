# Task 003 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer
| Fatal Error | Score Cap |
|-------------|:---------:|
| Approves a request that clearly violates non-waivable policy requirements (e.g., approving DAT-2025-007 without DPO pre-approval and audit logging) | 40 |
| Incorrectly expands CEO exemption beyond competitive bidding to cover CFO approval or annual review clause on PRC-2025-018 | 50 |
| Directly approves DAT-2025-008 (subpoena) without requiring Legal + DPO joint review | 50 |
| Rejects all incomplete requests as REJECT without using HOLD | 50 |
| Leaves a mandatory joint-review case at HOLD instead of ESCALATE | 50 |

## Dimension Scoring
| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Correct policy clause identification | 20 | Each finding cites correct policy document + section number |
| Decision reasoning correctness | 20 | Each decision follows from the policy text and conditions present |
| Decision framework accuracy | 20 | APPROVE / HOLD / REJECT / ESCALATE used correctly per definitions in task.md |
| Exception scoping accuracy | 15 | CEO exemption correctly scoped to competitive bidding only; subpoena exemption correctly identified but scoped to joint review requirement |
| No missed conditions | 10 | All applicable policies checked for each request; all conditions evaluated |
| No false positives | 5 | Compliant items not incorrectly flagged; decisions match actual conditions |
| Format compliance | 10 | JSON valid and follows schema with all 10 fields; Markdown has all required sections |
