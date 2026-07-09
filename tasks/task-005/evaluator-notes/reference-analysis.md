# Task 005 — Reference Analysis (Evaluator Only)

## Expected Conflicts (4 total)

1. Release Window: Product (business hours) vs Security (maintenance window 02-05). Resolution: Security wins per Charter Rule 4 (Operational Safety).

2. API Access: Product (public internet) vs Security (VPN only). Resolution: Security per Rule 1 (Security First).

3. Authentication: Product (OAuth + social login) vs Security (MFA mandatory, no social login). Resolution: Security per Rule 1.

4. Data Retention: Product (12 months) vs Security (90 days). Resolution: Rule 3 (Data Minimization) → 90 days. Optional: flag business case for longer retention as needing approval.

## Non-Conflict
Performance requirements are aligned (both say 10K users, <200ms). Security adds rate limiting and pen testing — additive, not conflicting.
