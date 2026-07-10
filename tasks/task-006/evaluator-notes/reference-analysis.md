# Task 006 — Reference Analysis (Evaluator Only)

## Task Summary

The agent must research and compare three agent harnesses (VitaClaw, OpenClaw, Hermes) across five dimensions (Skill Installation, Tool Invocation, Sandbox, Licensing, Offline Deployment) using either the controlled-web corpus or live-web search. The agent must produce source-register.json (source metadata), research-findings.json (claims with evidence mapping), comparison-table.csv (3×5 matrix), and final-answer.md (structured report).

## Expected Research Coverage

The agent should cover all 15 harness-dimension cells (3 harnesses × 5 dimensions). Not every cell requires a definitive answer — some dimensions may legitimately be NOT_PUBLICLY_DOCUMENTED, UNKNOWN, or INSUFFICIENT. What matters is that the agent documents what it searched, what it found, and the authority of each source.

## Key Quality Signals

### High-Quality Work
- Discovers official documentation, GitHub README files, and LICENSE files for each harness
- Correctly distinguishes between official sources and community discussion / third-party content
- Uses `support_status` and `evidence_status` separately: e.g., `NOT_SUPPORTED / CONFIRMED` for explicit non-support, `UNKNOWN / INSUFFICIENT` when no sources found
- Cross-references claims with source register — every claim has valid source_ids
- Documents search scope when information is not found (rather than fabricating conclusions)
- Labels community/forum content with `authority_tier: community_discussion`
- Records `NOT_PUBLICLY_DOCUMENTED` truthfully

### Low-Quality Work
- Produces claims without any source citations
- Assigns all sources the same authority tier without differentiation
- Confuses `support_status` with `evidence_status` (e.g., using CONFIRMED when support_status is just an inference from a single blog)
- Fabricates source URLs or content
- Cites search snippets as primary evidence without accessing pages

## Corpus Overview (for Controlled-Web Reviewer Reference)

The controlled-web corpus contains real first-party source snapshots for each harness. Reviewers should be familiar with:

- Which documents are official vs community-sourced
- Which dimensions have strong official coverage vs gaps
- The authority tier assignments in the corpus manifest

## Live-Web Review Notes

For live-web runs:
- Source availability may vary over time — this is expected and not scored against the agent
- If `web_activity_evidence` is `UNAVAILABLE`, reviewer cannot assess search strategy quality, only final output quality
- Citation accuracy and source authenticity remain scorable even when activity logs are unavailable
