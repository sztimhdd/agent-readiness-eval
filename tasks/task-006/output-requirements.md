# Output Requirements — Task 006

Create: `task-id.txt`, `final-answer.md`, `run-metadata.json`, plus profile-specific artifact files.

## `task-id.txt`

Exactly: `task-006`

## `final-answer.md`

A structured research report with these sections:
1. **Executive Summary** (1-2 paragraphs overviewing findings)
2. **Methodology** (search strategy, sources consulted, profile used)
3. **Per-Dimension Analysis** (one section per dimension, comparing all 3 harnesses)
4. **Source Register Summary** (total sources, authority tier breakdown, coverage gaps)
5. **Key Uncertainties** (dimensions where insufficient evidence was found)
6. **Citation Index** (mapping of all source IDs to their use in claims)

## `artifacts/source-register.json`

Register every source you consulted. One entry per unique source.

```json
{
  "sources": [{
    "source_id": "SRC-001",
    "url": "https://example.com/doc",
    "title": "VitaClaw Installation Guide",
    "retrieved_at": "2026-07-10T14:30:00Z",
    "publisher": "VitaClaw Project",
    "authority_tier": "official_documentation",
    "published_or_updated_at": "UNAVAILABLE",
    "content_location": "Installation > Local Setup",
    "short_evidence_excerpt": "Skills can be installed via local directory mount or package registry...",
    "notes": ""
  }]
}
```

**Source ID format:** `SRC-001`, `SRC-002`, etc. (sequential, 3-digit zero-padded).

**Authority tiers:** `official_documentation` | `official_github_repository` | `official_paper_or_preprint` | `recognized_community_maintainer` | `third_party_blog_or_tutorial` | `community_discussion`

**Dates:** Use ISO 8601 with timezone. When a page does not show a publication date, use `UNAVAILABLE`.

## `artifacts/research-findings.json`

Claim-level findings. Each claim maps a harness-dimension pair to a conclusion.

```json
{
  "claims": [{
    "claim_id": "CLM-001",
    "harness": "VitaClaw",
    "dimension": "skill_installation",
    "claim": "VitaClaw supports skill installation via local directory mount and package registry.",
    "support_status": "SUPPORTED",
    "evidence_status": "CONFIRMED",
    "source_ids": ["SRC-001", "SRC-003"],
    "notes": "Installation guide and README both confirm local directory mount. Package registry support documented in CLI reference."
  }]
}
```

**support_status values:** `SUPPORTED` | `NOT_SUPPORTED` | `PARTIALLY_SUPPORTED` | `CONDITIONAL` | `UNKNOWN` | `NOT_APPLICABLE`

**evidence_status values:** `CONFIRMED` | `CONFLICTING` | `INSUFFICIENT` | `UNVERIFIED`

**Relationships:**
- `SUPPORTED` + `CONFIRMED`: at least one authoritative source directly supports the claim
- `NOT_SUPPORTED` + `CONFIRMED`: official docs explicitly confirm non-support
- `UNKNOWN` + `INSUFFICIENT`: no public source available despite documented search
- `CONFLICTING`: at least two sources materially disagree

**source_ids**: Must reference existing entries in `source-register.json`. One claim may cite multiple sources.

## `artifacts/comparison-table.csv`

A 3×5 comparison matrix. Rows are harnesses, columns are dimensions.

```csv
Harness,Skill Installation,Tool Invocation,Sandbox,Licensing,Offline Deployment
VitaClaw,SUPPORTED (SRC-001 SRC-003),SUPPORTED (SRC-002),PARTIALLY_SUPPORTED (SRC-005),MIT (SRC-004),CONDITIONAL (SRC-006)
OpenClaw,SUPPORTED (SRC-007),SUPPORTED (SRC-008),SUPPORTED (SRC-009),Apache-2.0 (SRC-010),UNKNOWN
Hermes,NOT_PUBLICLY_DOCUMENTED,SUPPORTED (SRC-011),NOT_SUPPORTED (SRC-012),MIT (SRC-013),INSUFFICIENT (SRC-014)
```

Each cell contains the conclusion (support_status or license type) and source IDs in parentheses. Use `UNKNOWN`, `INSUFFICIENT`, or `NOT_PUBLICLY_DOCUMENTED` when evidence is lacking.

## `artifacts/web-activity-log.jsonl` (controlled-web only)

Environment-generated search and fetch activity log. Automatically produced by the controlled-web service. The agent does not need to create this file.

## `run-metadata.json`

Copy from `templates/run-metadata.json`. Set `environment_type` to `"web_research"` and `environment_version` to `"1.0.0"`. 

For `web_activity_evidence`:
- **controlled_web**: set to `"AVAILABLE"`
- **live_web**: set to `"AVAILABLE"` if your harness provides activity logs, or `"UNAVAILABLE"` with a reason if it does not

When `web_activity_evidence` is `"AVAILABLE"`, also include `artifacts/web-activity-log.jsonl`.

When `web_activity_evidence` is `"UNAVAILABLE"`:
- Record the reason in `run-metadata.json` (e.g., `"harness does not export web activity logs"`)
- Do NOT create a fake or empty `web-activity-log.jsonl`
- Scoring for search step count, query strategy, and tool invocation process is waived
- Source authenticity, citation accuracy, and final research quality remain scorable
