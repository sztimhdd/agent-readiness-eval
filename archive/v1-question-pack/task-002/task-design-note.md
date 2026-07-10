# Task 002 — Design Note

## What Task 002 Tests

Task 002 tests an agent's ability to conduct a multi-file incident investigation: discover relevant files, cross-reference information across sources, identify a distractor, reconcile conflicting information, distinguish facts from inferences from unknowns, and produce a structured incident report with evidence-backed conclusions.

## Compared to Task 001 — New Capabilities

| Capability | Task 001 | Task 002 |
|------------|----------|----------|
| Input files | 1 (single JSON) | 5 (JSON, Markdown, text) |
| File discovery | Not needed | Agent must scan `inputs/` and identify relevant subset |
| Information integration | Single source | Cross-file correlation required |
| Distractor handling | N/A | One explicit distractor (Dashboard UI section in team-notes) |
| Information conflict resolution | N/A | Customer email says "since 08:00" vs. metrics show 09:15 onset |
| Fact vs. inference vs. unknown | N/A | Agent must explicitly categorize |
| Evidence specificity | Ticket IDs | File names + record IDs + timestamps |
| Output format | 1 JSON + Markdown | 1 JSON + structured Markdown with 6 sections |

## Deliberately Not Tested

- Code writing or debugging
- Command execution beyond file reading/writing
- External API or network access
- Multi-turn conversation or user simulation
- Branching task paths
- Automated grading or verification
- Token or timing estimation
- Harness-specific tools

## Cross-Harness Fairness Analysis

**VitaClaw**: Can read directory with `ls`, read files with `Read`, write with `Edit`/`Write`. All tools available.

**OpenClaw**: Same tool set (Read/Write/Bash). Can cat/grep files freely.

**Hermes**: Read/Write tools available. Directory browsing via standard I/O operations.

**OpenCode**: Full read/write capability. Can use glob for discovery.

No harness has an inherent advantage because:
- All harnesses can read directory listings and file contents.
- No harness has exclusive tools that make the task easier.
- The task does not require speed, parallelism, or tool-use sophistication beyond basic file I/O.
- All harnesses can produce the required output files.

## Expected Completion Time

- Competent agent: 8–15 minutes
- Careful human: 10–20 minutes
- Rushed or weak agent: may exceed 20 minutes or miss key connections

## Common Failure Modes

1. **Missing the distractor**: Treating the Dashboard UI section as incident evidence, leading to wrong root cause.
2. **Single-file over-reliance**: Reading only one file (e.g., only `tickets.json`) and missing the deployment or metrics connection.
3. **Not distinguishing facts from inferences**: Stating "v2.3.1 caused the race condition" as fact without acknowledging this is inferred from correlated evidence — although this inference is so well-supported that deducting for it is not recommended.
4. **Missing the timeline conflict**: Not noticing the discrepancy between "since around 08:00" (email) and "first metric deviation at 09:28" (metrics).
5. **Incomplete evidence citation**: Making correct claims without citing specific files, ticket IDs, or metric names.
6. **Fabricated metadata**: Inventing token counts or timing instead of using `UNAVAILABLE`.

## How to Grade

See `evaluator-notes/manual-scoring-rubric.md`. A single human reviewer can score an answer in 5–10 minutes by checking:
1. Are the key facts correct?
2. Are the cross-file connections made?
3. Is the root cause reasonable and supported?
4. Are evidence references accurate?
5. Are recommendations concrete?
6. Are all required files present and correctly formatted?

## Future Variant Idea

**Variant direction**: Change the business domain from "AI platform incident" to "healthcare data pipeline incident" or "financial transaction reconciliation incident". The core mechanics stay the same — 5 files, one distractor, cross-file correlation, timeline construction — but the domain-specific terminology changes. To create a variant:
1. Replace customer names and product terminology.
2. Keep the same information distribution pattern (2 key fact files, 1 cross-reference file, 1 conflict file, 1 distractor).
3. Adjust metrics to the new domain.
4. Update the output JSON field names if needed.
5. Write a new scoring rubric specific to the domain's expected answers.
