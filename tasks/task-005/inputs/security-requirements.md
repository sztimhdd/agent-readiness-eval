# Security Department — System Upgrade Requirements

**Document:** REQ-SEC-2025-001
**Author:** Security Team
**Date:** 2025-06-03

## 1. Release Window
All production deployments must occur during the maintenance window (02:00-05:00 Beijing time) to minimize user impact and allow rollback before business hours.

## 2. API Access
All internal APIs must be accessible only through the corporate VPN. No public internet exposure under any circumstances.

## 3. Authentication
Multi-Factor Authentication (MFA) must be mandatory for all users. Social login providers introduce third-party risk and should be prohibited. Password-based login is insufficient — MFA is non-negotiable.

## 4. Data Retention
User activity logs must be purged after 90 days to comply with data minimization principles. Only aggregated, anonymized data may be retained beyond 90 days.

## 5. Performance
System must support 10,000 concurrent users with <200ms P95 latency. Must pass penetration testing before go-live. Rate limiting must be enforced at API gateway level.
