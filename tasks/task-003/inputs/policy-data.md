# Data Handling Policy (POL-DAT-2025)

## 1. Scope
Applies to all employee requests involving customer data access, export, or processing.

## 2. Data Classification
- **Public**: Marketing materials, press releases. No restrictions.
- **Internal**: Employee records, operational metrics. Manager approval required for export.
- **Confidential**: Customer PII, financial records. Data Protection Officer (DPO) approval required.
- **Restricted**: Authentication keys, encryption secrets. CTO approval required. Never exportable.

## 3. Export Rules
- Any data export must specify: purpose, recipient, retention period, deletion date.
- Retention periods for exports containing Confidential data must be >= 12 months from export date.
- Exports of Confidential data must use encrypted transfer.
- Bulk exports (>100 records) require DPO pre-approval and audit logging.

## 4. Third-Party Sharing
- Sharing Confidential data with third parties requires a Data Processing Agreement (DPA).
- Sharing Restricted data with third parties is prohibited.

## 5. Exemptions
- No exemptions for Restricted data handling.
- Legal compliance requests (subpoena, court order) may override Confidential data restrictions — must be reviewed by Legal + DPO jointly.
