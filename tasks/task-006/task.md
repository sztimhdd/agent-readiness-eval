# Task 006: Web Research — Harness Capability Comparison

Your task is to research and compare three agent harnesses across five capability dimensions using official first-party sources. This task measures your ability to search proactively, evaluate source authority, cross-reference claims, and produce a structured evidence-based report.

Do not call any external grading or verification code.

## Profiles

This task supports two profiles. The evaluator will tell you which to use.

### Profile A: Controlled Web (`controlled_web`)

You have access to a controlled search corpus containing snapshots of official documentation, GitHub repositories, and release notes for each harness. Use the provided search and fetch tools — do not access the open internet or read the private corpus directory directly.

**Tools available:**
- `search_corpus(query)` — search the corpus; returns doc IDs, titles, snippets, and relevance scores
- `fetch_document(doc_id)` — retrieve the full content of a document by its ID

### Profile B: Live Web (`live_web`)

Use your harness's native web search and page-fetch capabilities. Retrieve sources during this run and record the retrieval timestamp. Do not use pre-cached or training-memory content as primary evidence.

If your harness cannot export web activity logs, set `web_activity_evidence` to `UNAVAILABLE` in `run-metadata.json` and record the reason. Do not create a fake placeholder log file.

## Research Scope

Compare these three agent harnesses:

1. **VitaClaw** — agent framework with skill system and SaaS deployment
2. **OpenClaw** — open-source agent harness with sandbox and tool ecosystem
3. **Hermes** — agent runtime with plugin architecture

Across these five dimensions:

1. **Skill Installation**: How skills/packages are installed (local directory, package manager, workspace scope, restart requirements, third-party format support)
2. **Tool Invocation**: Native tool schema, MCP support, shell/exec capability, custom tool extension, tool permission/approval mechanisms
3. **Sandbox**: Existence of sandboxing, default enablement, isolation type (Docker / process-level / other), workspace mount mode, network and filesystem restrictions
4. **Licensing**: Repository license, license file source, version/commit at retrieval, per-component license differences
5. **Offline Deployment**: Core harness offline operation, skill installation network requirements, model inference cloud API dependency, optional feature degradation, distinction between initial install and post-install offline

## Workflow

1. Plan your research. For each harness-dimension pair, identify what you need to discover.
2. Search proactively. Use multiple queries per dimension. Refine queries based on initial results.
3. Retrieve and read full source pages. Do not rely only on search result snippets.
4. For each source, record its metadata: URL, title, retrieval timestamp, publisher, authority tier.
5. Evaluate source authority. Distinguish official documentation from community discussion and third-party content.
6. For each claim about a harness-dimension, assign two independent labels:
   - **support_status**: SUPPORTED | NOT_SUPPORTED | PARTIALLY_SUPPORTED | CONDITIONAL | UNKNOWN | NOT_APPLICABLE
   - **evidence_status**: CONFIRMED | CONFLICTING | INSUFFICIENT | UNVERIFIED
7. If a dimension is not publicly documented for a harness, record `NOT_PUBLICLY_DOCUMENTED` truthfully rather than fabricating a conclusion.
8. Cross-check all claims against source citations. Every claim in `research-findings.json` must reference valid `source_id` entries in `source-register.json`.
9. Produce the required output files (see `output-requirements.md`).

## Source Authority Tiers

Assign every source one of these tiers:

| Tier | Description |
|---|---|
| `official_documentation` | Official project docs site, README, or wiki maintained by the project |
| `official_github_repository` | Source code, LICENSE, CONTRIBUTING, or release notes in the official repo |
| `official_paper_or_preprint` | Published paper or preprint from the project authors |
| `recognized_community_maintainer` | Well-known community member or maintainer's post |
| `third_party_blog_or_tutorial` | Third-party blog, tutorial, or review site |
| `community_discussion` | Forum post, issue comment, or social media — must be explicitly labeled as non-official |

## Veto Layer

The following will cap your score:

- All claims from model training memory with zero web search
- Fabricating source URLs, GitHub repos, or official-looking documents
- Presenting community content as official without labeling
- Citing only search snippets without accessing original pages
- Claiming NOT_SUPPORTED from absence of evidence without documenting search scope
- Source register empty or contains only search snippet URLs
- Source register and comparison table cannot be cross-referenced
- Conclusion contradicts the cited page content

## Rules

- Do not fabricate token counts, timing data, or tool-call logs not observable from your environment.
- If a metadata field is unavailable, write `UNAVAILABLE` — do not estimate.
- Every claim in the comparison table must cite at least one source.
- Comparison table cells may be `UNKNOWN` or `INSUFFICIENT` — document why.
- Do not modify files under `evaluator-notes/` or `evaluator-private/`.
- Controlled web: do not read the private corpus directory directly — use only `search_corpus` and `fetch_document`.
