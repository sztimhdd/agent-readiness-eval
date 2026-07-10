# Task 003: Policy-Constrained Decision

Your company has three internal policies governing employee requests. You receive four requests that must be evaluated against all applicable policies.

## Decision Framework

You are the first-line policy reviewer. For each request, issue ONE decision:

**APPROVE** — All necessary conditions are satisfied. The request can proceed.

**HOLD** — The request is potentially allowable, but missing documents, approvals, or remediable prerequisites that can be supplied through normal workflow.

**REJECT** — The request violates non-waivable policy requirements in its current form. A revised submission may be considered separately.

**ESCALATE** — Policy requires transfer to another authority, joint review body, or discretionary decision-maker before any execution decision can be made.

## Role Boundary

Use HOLD when the request could become executable after the requester supplies a missing document, approval, or remediable prerequisite through the normal workflow.

Use REJECT when the request as currently submitted contains a non-waivable policy violation. A revised submission may be considered separately — but the current form cannot proceed. A requester who acknowledges a policy requirement and explicitly refuses to comply (e.g., demanding bypass of mandatory DPO approval) is not making a HOLD case; they are submitting a REJECT-eligible request.

Use ESCALATE when the policy requires the case to be transferred to another authority, joint review body, or discretionary decision-maker before any execution decision can be made.

Decisions apply to the request as currently submitted, not to whether the underlying business need may ever be permitted.

## Work Required

1. Read all policy documents in `inputs/`.
2. Read all request forms in `inputs/`.
3. For each request, determine which policies apply.
4. For each applicable policy, check whether the request satisfies every relevant clause.
5. Pay special attention to exception clauses — some policies have exemptions under specific conditions.
6. If an exemption applies, note its exact scope — do not extend it beyond what the policy authorizes.
7. Write the required files listed in `output-requirements.md`.
