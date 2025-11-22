# Hospital Management Dashboard (GDPR-focused)

This Streamlit app demonstrates a privacy-centric hospital management dashboard fulfilling confidentiality, integrity, and availability (CIA) requirements.

## Quick start (Windows PowerShell)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Initialize the database (creates `hospital.db` with sample users):

```powershell
python db_init.py
```

4. (Optional) If you previously had plaintext passwords, run migration:

```powershell
python migrate_passwords.py
```

5. Run the app:

```powershell
streamlit run .\streamlit_app.py
```

6. Sample credentials:
- admin / admin123
- Dr. Bob / doc123
- Alice_recep / rec123

## Main features implemented
- Role-based access control (Admin, Doctor, Receptionist)
- Password hashing (pbkdf2_sha256)
- Data masking and reversible encryption (Fernet)
- Consent banner and consent recording
- Activity logging with HMAC chaining (tamper-evident)
- Admin audit logs and CSV export
- Real-time activity graphs (Altair)
- Data retention (soft-delete) and permanent delete (with CSV archive)

## Developer notes
- Fernet key stored in `fernet.key` (created automatically). For demo it's OK, but in production use a secure secrets store.
- HMAC key stored in `hmac.key` (gitignored). Keep it secret.
- Use `reset_demo.py` before recording demos to get a clean state.

## Files of interest
- `streamlit_app.py` — main Streamlit app
- `db_init.py` — DB creation and sample data
- `schema_migrate.py` — schema migration helper
- `migrate_passwords.py` — migrate plaintext to hashed passwords
- `reset_demo.py` — clears logs/consents and preserves default patients
- `security.py` — Fernet & password/HMAC helpers