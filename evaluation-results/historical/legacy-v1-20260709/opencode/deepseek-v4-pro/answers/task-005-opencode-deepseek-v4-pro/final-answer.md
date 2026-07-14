# Conflicting Requirements Resolution — Task 005

## Executive Summary
Four conflicts were identified between Product (REQ-PRD-2025-001) and Security (REQ-SEC-2025-001) requirements. All resolved using the project charter (CHTR-2025-003) priority rules. Security prevailed in three conflicts (API access, authentication, release window); Data Minimization governed retention. Performance requirements are aligned across both documents — no conflict.

## Conflict Register

### Conflict 1: Release Window
- Product: REQ-PRD-2025-001 §1 — business hours (09:00-18:00) for team availability
- Security: REQ-SEC-2025-001 §1 — maintenance window (02:00-05:00) for safety
- Resolution: Adopt maintenance window 02:00-05:00 per **Charter Rule 4 (Operational Safety)** — deployment safety takes precedence over team convenience
- Deprioritized: Product requirement for business-hours deployment

### Conflict 2: API Access
- Product: REQ-PRD-2025-001 §2 — public internet, no VPN
- Security: REQ-SEC-2025-001 §2 — VPN only, no public exposure
- Resolution: VPN-only access per **Charter Rule 1 (Security First)** — security requirements precede convenience
- Deprioritized: Product requirement for public internet API access

### Conflict 3: Authentication
- Product: REQ-PRD-2025-001 §3 — OAuth 2.0 + social login, password fallback
- Security: REQ-SEC-2025-001 §3 — MFA mandatory, social login prohibited
- Resolution: MFA mandatory, social login prohibited per **Charter Rule 1 (Security First)**. Password-based login insufficient — MFA non-negotiable.
- Deprioritized: Social login convenience; password-only fallback removed

### Conflict 4: Data Retention
- Product: REQ-PRD-2025-001 §4 — 12 months, full fidelity
- Security: REQ-SEC-2025-001 §4 — 90 days, anonymized only after
- Resolution: 90-day retention per **Charter Rule 3 (Data Minimization)** — shorter retention preferred absent business-critical reason. Note: Product analytics may constitute a business reason — flag for separate business case review.
- Deprioritized: 12-month full-fidelity retention

### Non-Conflict: Performance
Both documents require 10,000 concurrent users with <200ms P95 latency. Security adds rate limiting and penetration testing — these are additive requirements, not conflicts.

## Unified Requirements
1. Deployments: 02:00-05:00 maintenance window
2. API access: VPN only, no public exposure
3. Authentication: MFA mandatory, no social login
4. Data retention: 90 days, anonymized after; business case required for longer retention
5. Performance: 10K users, <200ms P95, + rate limiting + pen testing

## Prioritized Action Plan
1. Implement MFA — security-critical, addresses highest-risk gap
2. Configure VPN-only API access — prevents public exposure
3. Schedule deployments in maintenance window — operational safety
4. Set up 90-day data retention with anonymization pipeline — compliance
5. Conduct penetration testing before go-live — per security requirements
