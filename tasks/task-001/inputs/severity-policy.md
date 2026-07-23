# Severity Policy

## Severity Levels

| Level | Definition | Examples | Target Response |
|-------|-----------|----------|-----------------|
| Critical | Complete system failure, active data loss, security breach, regulatory violation | Auth system down, PII leak, payment pipeline failure | Within 1 hour |
| High | Major feature broken, significant revenue impact, broad user blockage | Login failure for a subset, incorrect billing for enterprise accounts | Within 4 hours |
| Medium | Feature partially broken, acceptable workaround exists, non-critical data issue | Export with minor errors, UI glitch with manual workaround | Within 24 hours |
| Low | Cosmetic issue, minor inconvenience, enhancement request | Filter resets on refresh, non-blocking UI confusion | Next release cycle |

## Source Authority & Precedence

When multiple sources provide information about a ticket, apply the following precedence (highest to lowest):

1. **Resolution Notes** in `ticket-update-log.md` — A final resolution finding overrides all prior severity labels for that ticket. If a resolution note establishes that a symptom had no functional impact, that finding is authoritative.

2. **Latest Update Entry** in `ticket-update-log.md` — The most recent timestamped entry for a given ticket supersedes the `severity` field in `data.json`. The entry's reclassification, if present, replaces the original severity.

3. **Current Ticket Fields** in `data.json` — The `severity` and `impact` fields as filed initially. These are the default when no update log entry exists for a ticket.

4. **Description Text** — Implicit severity inferred from ticket description alone. Lowest authority; use only when no other source is available.

## Rules

- An update entry that explicitly reclassifies severity supersedes the `severity` field in `data.json`.
- If multiple entries exist for the same ticket ID, the entry with the most recent date wins.
- A resolution note that identifies a root cause as cosmetic, display-only, or non-functional supersedes any earlier "high" or "critical" severity label — regardless of the original impact description.
- When severity cannot be determined from any authoritative source, default to the most conservative level supported by available evidence.
- Entries are additive: an update does not delete a ticket; it supplements or overrides specific fields.
