# Project Charter — System Upgrade v3

**Document:** CHTR-2025-003
**Approved by:** CTO Office
**Date:** 2025-05-15

## Priority Rules

When requirements from different departments conflict, apply these rules in order:

### Rule 1: Security First
Security requirements take precedence over convenience and user experience. If a security requirement conflicts with a product requirement, the security requirement governs.

### Rule 2: Compliance Over Features
Regulatory and compliance requirements override feature requests. If a compliance requirement conflicts with any other requirement, the compliance requirement governs.

### Rule 3: Data Minimization
Where security and compliance do not dictate otherwise, minimize data collection and retention. Shorter retention periods are preferred when no business-critical reason demands longer retention.

### Rule 4: Operational Safety
Deployment and operational safety requirements (including maintenance windows) take precedence over team convenience.

### Rule 5: CTO Final Decision
If Rules 1-4 do not resolve a conflict, the CTO makes the final decision. In this case, flag the conflict as "escalated to CTO" in your output.

### Rule 6: Tiebreakers
When two requirements of equal priority under the above rules conflict, prefer the one that maximizes user safety, then system reliability, then development velocity.
