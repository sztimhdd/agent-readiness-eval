# Ticket Update Log

This log records post-filing updates to tickets. Entries are additive and may supersede the corresponding fields in `data.json`. Per the severity policy, the latest entry for a given ticket takes precedence over the ticket's initial severity label.

---

## 2026-07-15

### T-1007: Passwordless login flow fails silently

**Update:** Investigation determined the issue is limited to a single mobile browser version (Safari 17 on iOS). A known browser cache behavior causes the silent failure. A server-side workaround is being deployed to clear stale cache entries. The root cause is not in the authentication service.

**Severity Reclassification:** `critical` → `medium`

**Reason:** Issue is browser-specific, affects only a subset of mobile users, and has a deployed workaround. Not a systemic authentication failure.

---

## 2026-07-17

### T-1008: Agent session does not persist across browser tabs

**Update:** Root cause identified — session cookie `SameSite` attribute misconfiguration on the load balancer. Hotfix deployed to all environments. Confirmed resolved in staging. Monitoring shows no recurrence in 24 hours.

**Severity Reclassification:** `high` → `low`

**Reason:** Root cause identified, hotfix deployed, and no ongoing impact. Residual work is documentation-only (cookie attribute guidance).

---

## 2026-07-18

### T-1009: Invoice PDFs contain incorrect VAT calculations

**Resolution Note:** Engineering investigation confirmed that the PDF rendering template displays incorrect VAT figures, but the underlying stored values and tax filing reports are correct. This is a display-only rendering bug. No regulatory exposure exists. Corrected PDFs will be regenerated from the already-correct data.

**Severity Reclassification:** `high` → `low`

**Reason:** The apparent financial compliance impact was a UI rendering issue only. Actual calculations and filing data are accurate. No customer-facing financial harm or regulatory risk occurred.
