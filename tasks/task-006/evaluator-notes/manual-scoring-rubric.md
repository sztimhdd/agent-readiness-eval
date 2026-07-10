# Task 006 — Manual Scoring Rubric

**Total: 100 points**

## Veto Layer

| Fatal Error | Score Cap |
|---|---|
| All claims from model training memory, zero web search | 20 |
| Fabricating source URLs or GitHub repos | 20 |
| Presenting community content as official without labeling | 30 |
| Citing only search snippets without accessing original pages | 30 |
| Claiming NOT_SUPPORTED from absence of evidence without documenting search scope | 40 |
| Source register empty or contains only search snippet URLs | 40 |
| Conclusion contradicts the cited page content | 40 |
| Source URL is real but page does not support cited claim | 40 |
| Controlled mode: directly reading private corpus/index | 20 |
| Live mode: using snapshot content but claiming live retrieval | 20 |
| Source register and comparison table cannot be cross-referenced | 50 |
| Claiming web use with zero observable evidence | 20 |

## Dimension Scoring

| Dimension | Points | Criteria |
|---|---|---|
| **Source Discovery** | 25 | Sources discovered across all 5 dimensions × 3 harnesses. At least 1 source per dimension-harness cell. Sources are actual pages, not just search snippets. Mix of official docs, GitHub repos, and release notes. |
| **Authority Assessment** | 20 | Every source correctly assigned an authority tier (official_documentation, official_github_repository, community_discussion, etc.). Community/third-party sources explicitly labeled as non-official. Source metadata (publisher, canonical URL, snapshot date) complete and accurate. |
| **Cross-Referencing** | 15 | Multiple sources consulted per claim where available. Conflicting information identified and flagged. Claims supported by at least one authoritative source. All dimensions covered for all 3 harnesses. |
| **Claim Verification** | 15 | support_status and evidence_status correctly assigned as separate axes. CONFIRMED status only when at least one authoritative source directly supports. INSUFFICIENT used when only community sources found. UNKNOWN correctly used when no sources found despite documented search. |
| **Uncertainty Labeling** | 10 | Known-vs-unknown boundaries clear. Information gaps explicitly documented. No fabricated conclusions from absence of evidence. NOT_PUBLICLY_DOCUMENTED truthfully recorded where no public source exists. |
| **Citation Accuracy** | 10 | Every claim in research-findings.json maps to valid source_ids in source-register.json. Citations include page locations where applicable. No broken cross-references. |
| **Output Completeness** | 5 | All required artifacts present: source-register.json, research-findings.json, comparison-table.csv, final-answer.md. JSON valid and schema-compliant. comparison-table.csv readable and consistent with findings. |
