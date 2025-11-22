# Hospital Management Dashboard — Project Report

**Title:** GDPR-Compliant Hospital Management Dashboard

**Authors:** [Student A] & [Student B]

**Date:** (fill date)

---

## Executive Summary

Provide a concise summary (150-250 words) of the system, objectives, and outcomes. Explain how the dashboard meets confidentiality, integrity, and availability requirements and aligns with GDPR principles.

## System Overview (Architecture)

- Brief architecture diagram: describe components (Streamlit frontend, SQLite DB, security helpers). Insert diagram image here.

![Architecture Diagram](images/architecture_diagram.png)

## Features and Mapping to CIA & GDPR

- Confidentiality: data masking, Fernet encryption, RBAC — describe and reference code locations.
- Integrity: activity logs with HMAC chaining, audit trail, role checks.
- Availability: error handling, CSV exports/backups, uptime display.

## Screenshots (take and replace the placeholders)

1. Login screen

   ![Login screen](images/screenshot_login.png)

2. Admin dashboard (show anonymization buttons)

   ![Admin dashboard](images/screenshot_admin.png)

3. Anonymized patient table (mask/ENCRYPT example)

   ![Anonymized patients](images/screenshot_anonymized.png)

4. Activity graphs and audit logs

   ![Activity graphs](images/screenshot_graphs.png)

5. GDPR features: Consent banner and Retention UI

   ![Consent banner](images/screenshot_consent.png)

## Implementation Details

- Languages & frameworks: Python 3.11, Streamlit, SQLite, cryptography, passlib, pandas, altair.
- Files of interest: `streamlit_app.py`, `db_init.py`, `security.py`, `schema_migrate.py`, `reset_demo.py`.
- Database schema summary:

  - `users(user_id, username, password, role)`
  - `patients(patient_id, name, contact, diagnosis, anonymized_name, anonymized_contact, date_added, deleted_at)`
  - `logs(log_id, user_id, role, action, timestamp, details, log_hash)`
  - `consents(consent_id, user_id, role, consent_ts, details)`

## Security Considerations

- Password storage: pbkdf2_sha256 hashing via `passlib`.
- Encryption: Fernet (symmetric) for reversible anonymization; `fernet.key` stored locally for demo.
- Log integrity: HMAC chain stored in `log_hash` — stored in `hmac.key` (gitignored).
- Recommendations for production: use secrets manager for keys, use TLS, proper user management, stronger DB access controls.

## Testing & Verification Checklist

Follow these steps to verify the system:

- [ ] Run `python db_init.py` to (re)create DB and sample data.
- [ ] Start the app and test login with sample accounts.
- [ ] Verify role-based views (Admin/Doctor/Receptionist).
- [ ] Trigger anonymization (mask + encrypt) and decrypt; verify logs contain entries with `log_hash` values.
- [ ] Test consent flow (first login), retention purge and permanent delete with CSV archive.
- [ ] Run `reset_demo.py` to clear logs/consents and prepare demo state.

## How to build the PDF report (optional)

Install `pandoc` and a PDF engine (e.g., wkhtmltopdf or LaTeX). Then run (PowerShell):

```powershell
pandoc report_template.md -o report.pdf --from markdown -V geometry:margin=1in
```

Alternatively, export the notebook or use any Markdown→PDF tool.

## Appendix

- Important code references and snippets (copy/paste small examples here).

---

Replace the `images/*.png` placeholders with real screenshots before exporting to PDF.
