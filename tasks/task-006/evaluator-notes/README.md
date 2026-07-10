# Evaluator Notes — Task 006 (Web Research)

These evaluator notes are for human reviewers only. Do not include them in agent-visible packages.

## Directory Structure

```
evaluator-notes/
├── README.md                    # This file
├── manual-scoring-rubric.md     # 100-point scoring rubric
└── reference-analysis.md        # Expected findings and reference analysis

evaluator-private/
└── reference-sources.yaml       # Known authoritative sources (guidance, NOT whitelist)
```

## Reviewer Responsibilities

1. Score the agent's research output against the rubric in `manual-scoring-rubric.md`.
2. Compare findings against `reference-analysis.md` for expected discoveries.
3. Use `evaluator-private/reference-sources.yaml` as guidance for source quality — but do not penalize agents for discovering additional legitimate sources.
4. Cross-check citations: every claim in `research-findings.json` must reference valid entries in `source-register.json`.
5. Verify source authenticity: spot-check URLs, publisher names, and authority tier assignments.
6. For live-web runs: if `web_activity_evidence` is `AVAILABLE`, review the web-activity-log for search strategy quality.
7. For controlled-web runs: verify the agent used `search_corpus` and `fetch_document` (not direct corpus reads).
