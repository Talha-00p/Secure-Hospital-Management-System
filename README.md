```markdown
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

5. Run the app locally:

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

## Deployment

This project can be deployed in several ways. Below are recommended options and exact steps.

1) Deploy to Streamlit Community Cloud (recommended for demos)
- Push your repo to GitHub, then go to https://streamlit.io/cloud and "New app" → connect your GitHub repo → point to `streamlit_app.py` and the branch. Streamlit Cloud will automatically install `requirements.txt`.

2) Deploy with Docker (recommended for Render, Railway, or self-hosting)
- Build locally:

```powershell
docker build -t hospital-dashboard:latest .
docker run -p 8501:8501 hospital-dashboard:latest
```

3) Deploy to Render / Railway
- Push to GitHub and connect to Render or Railway; set the start command to:

```
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

4) GitHub Actions CI
- The repository includes a basic CI workflow (`.github/workflows/python-app.yml`) that installs dependencies and runs a syntax check on push/PR.

## Security & Secrets
- Do NOT commit `fernet.key` or `hmac.key` — they are included in `.gitignore`.
- For production, store keys as GitHub Secrets or use a secrets manager.

## How to push this project to GitHub (example)
Open PowerShell in the repository root then run:

```powershell
git init
git add .
git commit -m "Initial commit: hospital management dashboard"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

After pushing, connect the repo to Streamlit Cloud or your chosen host.

## CI / Additional automation
- The CI workflow performs dependency install and syntax checks. If you want style checks or tests add `pytest`/`flake8` to `requirements.txt` and update the workflow.

```
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