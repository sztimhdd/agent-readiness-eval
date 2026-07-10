# Task 003 — Manual Scoring Rubric

## Total Score: 100 points

## Veto Layer
| Fatal Error | Score Cap |
|-------------|:---------:|
| Misses PII/data compliance issue entirely (no DPO flagging on DAT-2025-007) | 40 |
| Misses the missing annual review clause on PRC-2025-018 while correctly applying CEO exemption | 60 |
| Treats DAT-2025-008 (subpoena) as standard non-compliant without recognizing legal exemption | 60 |

## Dimension Scoring
| Dimension | Points | Criteria |
|-----------|:------:|----------|
| Correct policy clause identification | 20 | Each finding cites correct policy document + section number |
| Edge case / exemption handling | 20 | CEO exemption correctly applied; subpoena exemption correctly applied; exemption does NOT leak to non-exempt requests |
| Conditional logic correctness | 20 | International travel triggers VP regardless of amount; >50K triggers CFO + bidding; all thresholds applied correctly |
| No missed findings | 20 | All non-compliant items across all 4 requests identified |
| No false positives | 10 | Compliant items not incorrectly flagged |
| Format compliance | 10 | JSON valid and follows schema; Markdown has all required sections |
