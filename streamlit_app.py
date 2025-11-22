import streamlit as st
st.markdown("""
<style>
:root {
  --primary: #7C4DFF;      /* Deep Purple */
  --secondary: #00BFA5;    /* Teal */
  --accent: #FF4081;       /* Pink */
  --bg: #0F172A;           /* Slate-900 */
  --text: #E5E7EB;         /* Gray-200 */
  --muted: #9CA3AF;        /* Gray-400 */
  --surface: #111827;      /* Gray-900 */
  --elev-1: 0 1px 2px rgba(0,0,0,0.40);
  --elev-2: 0 8px 24px rgba(0,0,0,0.50);
}
.stTabs [role='tab'] {
  padding: 0.6rem 1rem;
  border-radius: 8px 8px 0 0;
  background: var(--surface);
  box-shadow: var(--elev-1);
  color: var(--muted);
  border-bottom: 2px solid transparent;
}
.stTabs [aria-selected='true'] {
  color: var(--primary);
  box-shadow: var(--elev-2);
  border-bottom-color: var(--accent);
}
div.stButton>button {
  border-radius: 8px;
  border: 1px solid rgba(124,77,255,0.35);
  background: linear-gradient(180deg, #8E64FF 0%, #7C4DFF 100%);
  color: #F8FAFC;
  box-shadow: var(--elev-1);
}
div.stButton>button:hover {
  transform: translateY(-1px);
  box-shadow: var(--elev-2);
}
.stApp { background: var(--bg); color: var(--text); }
.alert-amber {
  background: linear-gradient(180deg, #3a2a00 0%, #2a1f00 100%);
  border: 1px solid rgba(255,193,7,0.35);
  color: #FFE082;
  padding: 12px 14px;
  border-radius: 12px;
  box-shadow: var(--elev-1);
}
.alert-amber h4 { margin: 0 0 8px; color: #FFC107; }
</style>
""", unsafe_allow_html=True)
import sqlite3
from datetime import datetime
import time
import io
import os
from security import get_fernet, verify_password

# Set page config for better UI
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🩺",
    layout="wide"
)

DB_NAME = 'hospital.db'
FERNET_KEY_FILE = 'fernet.key'

# Fernet key management
APP_START_TIME = time.time()

def authenticate_user(username, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT user_id, password, role FROM users WHERE username=?', (username,))
        row = c.fetchone()
        conn.close()
        if row and verify_password(password, row[1]):
            return {'user_id': row[0], 'role': row[2]}
    except Exception:
        return None
    return None

def log_action(user_id, role, action, details):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    # compute chained HMAC log_hash using previous log_hash
    prev_hash = None
    try:
        c.execute('SELECT log_hash FROM logs ORDER BY log_id DESC LIMIT 1')
        row = c.fetchone()
        prev_hash = row[0] if row and row[0] else ''
    except Exception:
        prev_hash = ''
    try:
        from security import load_or_create_hmac_key, compute_hmac
        hkey = load_or_create_hmac_key()
        msg = f'{prev_hash}|{user_id}|{role}|{action}|{timestamp}|{details}'
        log_hash = compute_hmac(hkey, msg)
    except Exception:
        log_hash = None
    c.execute('INSERT INTO logs (user_id, role, action, timestamp, details, log_hash) VALUES (?, ?, ?, ?, ?, ?)',
              (user_id, role, action, timestamp, details, log_hash))
    conn.commit()
    conn.close()

def main():
    st.markdown(
        f"""
        <style>
        :root {{
            --primary: #7C4DFF;
            --primary-light: #B388FF;
            --accent: #00BFA5;
            --bg: #0F172A;
        }}
        body {{ background: var(--bg); }}
        .split-card {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: stretch;
            gap: 20px;
            width: 90%;
            margin: 24px auto 0 auto;
        }}
        .left-panel {{
            background: linear-gradient(135deg, #1E1B4B 0%, var(--primary) 100%);
            color: #E5E7EB;
            border-radius: 24px;
            padding: 28px 24px;
            flex: 1 1 420px;
            min-width: 300px;
            box-shadow: 0 6px 28px rgba(124,77,255,0.35);
        }}
        .right-panel {{
            background: var(--surface);
            border-radius: 24px;
            padding: 28px 24px;
            flex: 1 1 520px;
            min-width: 320px;
            box-shadow: 0 6px 28px rgba(124,77,255,0.30);
        }}
        .dashboard-title {{color: var(--primary); font-size: 2rem; font-weight: 700; margin-bottom: 12px;}}
        .feature-list {{margin-top: 16px;}}
        .feature-list li {{margin-bottom: 10px; font-size: 16px; color: #CBD5E1;}}
        .login-title {{color: var(--primary); font-size: 1.5rem; font-weight: 700; margin-bottom: 12px;}}
        .footer {{text-align:center; color: var(--secondary); font-size:14px; margin-top:16px;}}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar code fully removed for clean layout

    st.markdown('<div style="width:90%;margin:24px auto 8px auto;background:#111827;border-radius:32px;box-shadow:0 6px 28px rgba(124,77,255,0.35);padding:24px 16px;text-align:center;">\n<h1 style="color:#7C4DFF;font-size:2.25rem;font-weight:800;margin:0;">Hospital Management System</h1>\n<div style="color:#00BFA5;margin-top:4px;">GDPR-Compliant • Privacy-Centric</div>\n</div>', unsafe_allow_html=True)

    if 'role' not in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="split-card">', unsafe_allow_html=True)
        st.markdown('''<div class="left-panel">
            <h2 style="font-size:2rem; font-weight:700; margin-bottom:16px;">Employer<br>Medical Portal</h2>
            <ul class="feature-list">
                <li>Data Analytics</li>
                <li>Online Scheduling</li>
                <li>Resulting</li>
                <li>OSHA Surveillance</li>
                <li>Invoicing</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.markdown('''<div class="right-panel">
            <div style="text-align:center; margin-bottom:16px;">
                <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" width="48" style="margin-bottom:8px;" />
                <div class="login-title">Login</div>
            </div>
        ''', unsafe_allow_html=True)
        with st.form('login_form'):
            username = st.text_input('Username', placeholder='Enter your username')
            password = st.text_input('Password', type='password', placeholder='Enter your password')
            login_clicked = st.form_submit_button('Login')
        if login_clicked:
            user = authenticate_user(username, password)
            if user:
                st.success(f'Logged in as {username} ({user["role"]})')
                log_action(user['user_id'], user['role'], 'login', f'User {username} logged in.')
                st.session_state['user_id'] = user['user_id']
                st.session_state['role'] = user['role']
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error('Invalid credentials. Please try again.')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        role = st.session_state['role']
        # Helper to assert role before performing sensitive actions
        def require_role(allowed_roles):
            # allowed_roles: list or tuple
            ar = allowed_roles if isinstance(allowed_roles, (list, tuple)) else [allowed_roles]
            current = st.session_state.get('role')
            if current in ar:
                return True
            # log unauthorized attempt
            try:
                uid = st.session_state.get('user_id')
                log_action(uid if uid else None, current if current else 'unknown', 'unauthorized_attempt', f'Attempted action requiring {ar}')
            except Exception:
                pass
            st.error('You do not have permission to perform this action.')
            return False
        # Show consent banner if no consent record for this user
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('SELECT consent_id FROM consents WHERE user_id=?', (st.session_state['user_id'],))
            consent_row = c.fetchone()
            conn.close()
        except Exception:
            consent_row = None
        # consider session flag (if we just recorded consent) as well
        consent_given = bool(consent_row) or st.session_state.get('consent_accepted', False)
        if not consent_given:
            # Block rendering of dashboard until user accepts consent so it is not missed
            with st.container():
                st.warning('We use this dashboard to process patient data for healthcare purposes. By continuing you give consent to process your account data for this demo.')
                if st.button('I Accept', key='accept_consent'):
                    # record consent; if DB write fails show error, but don't fail on rerun
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        ts = datetime.now().isoformat()
                        c.execute('INSERT INTO consents (user_id, role, consent_ts, details) VALUES (?, ?, ?, ?)',
                                  (st.session_state['user_id'], role, ts, 'User accepted consent banner'))
                        conn.commit()
                        conn.close()
                        log_action(st.session_state['user_id'], role, 'consent_given', 'User accepted consent banner')
                        st.success('Consent recorded. Thank you.')
                        # mark in session so the current request continues without needing a reload
                        st.session_state['consent_accepted'] = True
                        # try to rerun silently if available
                        try:
                            if hasattr(st, 'experimental_rerun'):
                                st.experimental_rerun()
                        except Exception:
                            pass
                    except Exception as e:
                        st.error(f'Consent recording failed: {e}')
                else:
                    st.info('Please accept to continue.')
                    st.stop()
        # Sidebar: user status and quick actions
        with st.sidebar:
            st.markdown('**User**')
            st.write(st.session_state.get('username', ''))
            st.markdown('**Role**')
            st.write(role)
            uptime = int(time.time() - APP_START_TIME)
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.caption(f'Uptime {hours:02d}:{minutes:02d}:{seconds:02d}')
            try:
                mtime = os.path.getmtime(DB_NAME)
                last_sync = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                st.caption(f'Last DB update: {last_sync}')
            except Exception:
                st.caption('Last DB update: unknown')
            if st.button('Logout'):
                st.session_state.clear()
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="split-card">', unsafe_allow_html=True)
        # Left panel: role info/features
        if role == 'admin':
            st.markdown('''<div class="left-panel">
                <h2 class="dashboard-title">Admin Dashboard</h2>
                <ul class="feature-list">
                    <li>Full access to patient data</li>
                    <li>Trigger anonymization</li>
                    <li>View audit logs</li>
                    <li>Export data</li>
                </ul>
            </div>''', unsafe_allow_html=True)
        elif role == 'doctor':
            st.markdown('''<div class="left-panel">
                <h2 class="dashboard-title">Doctor Dashboard</h2>
                <ul class="feature-list">
                    <li>View anonymized patient data</li>
                    <li>Review diagnoses</li>
                    <li>Monitor patient status</li>
                </ul>
            </div>''', unsafe_allow_html=True)
        elif role == 'receptionist':
            st.markdown('''<div class="left-panel">
                <h2 class="dashboard-title">Receptionist Dashboard</h2>
                <ul class="feature-list">
                    <li>Add/edit patient records</li>
                    <li>Schedule appointments</li>
                    <li>Basic patient info only</li>
                </ul>
            </div>''', unsafe_allow_html=True)
        # Right panel: dashboard actions
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:#7C4DFF;">Welcome, {st.session_state["username"]}!</h3>', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#00BFA5;">Dashboard</h4>', unsafe_allow_html=True)
        # Logout button
        if st.button('Logout', key='logout_btn'):
            st.session_state.clear()
            st.rerun()
        if role == 'admin':
            overview_tab, patients_tab, anon_tab, logs_tab, retention_tab, activity_tab = st.tabs([
                'Overview', 'Patients', 'Anonymization', 'Logs', 'Retention', 'Activity'
            ])

            with overview_tab:
                st.caption('Tip: Quick metrics and recent activity overview.')
                st.write('Quick actions and system overview.')
                try:
                    import pandas as pd
                    conn = sqlite3.connect(DB_NAME)
                    logs_df = pd.read_sql_query('SELECT timestamp FROM logs', conn)
                    conn.close()
                    if not logs_df.empty:
                        last_week_cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
                        last7 = logs_df[pd.to_datetime(logs_df['timestamp']) >= last_week_cutoff]
                        st.metric('Actions last 7 days', int(last7.shape[0]))
                    else:
                        st.metric('Actions last 7 days', 0)
                except Exception:
                    st.metric('Actions last 7 days', 0)

            with patients_tab:
                st.caption('Tip: Browse raw patient data and export CSV.')
                colA, colB = st.columns([1,1])
                with colA:
                    if st.button('View Raw Patient Data'):
                        conn = sqlite3.connect(DB_NAME)
                        try:
                            import pandas as pd
                            df = pd.read_sql_query("SELECT * FROM patients WHERE deleted_at IS NULL OR deleted_at=''", conn)
                            st.dataframe(df, use_container_width=True)
                        except Exception as e:
                            st.error(f'Error: {e}')
                        finally:
                            conn.close()
                with colB:
                    if st.button('Export Patients CSV'):
                        try:
                            import pandas as pd
                            conn = sqlite3.connect(DB_NAME)
                            df = pd.read_sql_query('SELECT * FROM patients', conn)
                            conn.close()
                            csv = df.to_csv(index=False)
                            st.download_button('Download Patients CSV', data=csv, file_name='patients.csv', mime='text/csv')
                        except Exception as e:
                            st.error(f'Export error: {e}')

            with anon_tab:
                st.caption('Tip: Apply masking or encryption, decrypt, and view anonymized data.')
                st.write('Mask, encrypt, decrypt, and view anonymized patient data.')
                fernet = get_fernet()
                c1, c2 = st.columns([1,1])
                with c1:
                    if st.button('Anonymize Patient Data (Mask)'):
                        if not require_role(['admin']):
                            pass
                        else:
                            conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute('SELECT patient_id, name, contact FROM patients')
                        for pid, name, contact in c.fetchall():
                            anon_name = f'ANON_{pid}'
                            anon_contact = f'XXX-XXX-{contact[-4:]}'
                            c.execute('UPDATE patients SET anonymized_name=?, anonymized_contact=? WHERE patient_id=?',
                                      (anon_name, anon_contact, pid))
                        conn.commit()
                        conn.close()
                        log_action(st.session_state['user_id'], role, 'anonymization', 'Admin triggered masking.')
                        st.success('Patient data masked.')
                with c2:
                    if st.button('Anonymize Patient Data (Encrypt)'):
                        if not require_role(['admin']):
                            pass
                        else:
                            conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute('SELECT patient_id, name, contact FROM patients')
                        for pid, name, contact in c.fetchall():
                            enc_name = fernet.encrypt(name.encode()).decode()
                            enc_contact = fernet.encrypt(contact.encode()).decode()
                            c.execute('UPDATE patients SET anonymized_name=?, anonymized_contact=? WHERE patient_id=?',
                                      (enc_name, enc_contact, pid))
                        conn.commit()
                        conn.close()
                        log_action(st.session_state['user_id'], role, 'anonymization', 'Admin triggered encryption.')
                        st.success('Patient data encrypted.')
                if st.button('Decrypt Patient Data'):
                    if not require_role(['admin']):
                        pass
                    else:
                        conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute('SELECT patient_id, anonymized_name, anonymized_contact FROM patients')
                    for pid, enc_name, enc_contact in c.fetchall():
                        try:
                            dec_name = fernet.decrypt(enc_name.encode()).decode()
                            dec_contact = fernet.decrypt(enc_contact.encode()).decode()
                            c.execute('UPDATE patients SET anonymized_name=?, anonymized_contact=? WHERE patient_id=?',
                                      (dec_name, dec_contact, pid))
                        except Exception:
                            continue
                    conn.commit()
                    conn.close()
                    log_action(st.session_state['user_id'], role, 'decryption', 'Admin decrypted patient data.')
                    st.success('Patient data decrypted.')
                if st.button('View Anonymized Patient Data'):
                    conn = sqlite3.connect(DB_NAME)
                    try:
                        import pandas as pd
                        df = pd.read_sql_query("SELECT patient_id, anonymized_name, anonymized_contact, diagnosis, date_added FROM patients WHERE deleted_at IS NULL OR deleted_at=''", conn)
                        st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f'Error: {e}')
                    finally:
                        conn.close()

            with logs_tab:
                st.caption('Tip: Review audit logs and export for compliance.')
                colL, colR = st.columns([1,1])
                with colL:
                    if st.button('View Audit Log'):
                        conn = sqlite3.connect(DB_NAME)
                        try:
                            import pandas as pd
                            df = pd.read_sql_query('SELECT * FROM logs', conn)
                            st.dataframe(df, use_container_width=True)
                        except Exception as e:
                            st.error(f'Error: {e}')
                        finally:
                            conn.close()
                with colR:
                    if st.button('Export Logs CSV'):
                        try:
                            import pandas as pd
                            conn = sqlite3.connect(DB_NAME)
                            df = pd.read_sql_query('SELECT * FROM logs', conn)
                            conn.close()
                            csv = df.to_csv(index=False)
                            st.download_button('Download Logs CSV', data=csv, file_name='logs.csv', mime='text/csv')
                        except Exception as e:
                            st.error(f'Export error: {e}')

            with retention_tab:
                st.markdown("<div class='alert-amber'><h4>Retention Warning</h4><div>Soft-deleting removes access to patient records. Export CSV before purging. Permanent delete cannot be undone.</div></div>", unsafe_allow_html=True)
                st.markdown('**Danger Zone**')
                perm_confirm = st.checkbox('I understand this will permanently delete soft-deleted patient records', key='perm_confirm')
                if st.button('Permanently delete soft-deleted patients'):
                    if not perm_confirm:
                        st.warning('Please check the confirmation box to enable permanent delete.')
                    else:
                        try:
                            conn = sqlite3.connect(DB_NAME)
                            c = conn.cursor()
                            c.execute("SELECT patient_id FROM patients WHERE deleted_at IS NOT NULL AND deleted_at<>''")
                            rows = c.fetchall()
                            ids = [r[0] for r in rows]
                            if not ids:
                                st.info('No soft-deleted patients to remove.')
                            else:
                                import pandas as pd
                                placeholders = ','.join('?' for _ in ids)
                                c.execute(f'SELECT patient_id, name, contact, diagnosis, date_added, deleted_at FROM patients WHERE patient_id IN ({placeholders})', tuple(ids))
                                rows = c.fetchall()
                                df = pd.DataFrame(rows, columns=['patient_id', 'name', 'contact', 'diagnosis', 'date_added', 'deleted_at'])
                                csv = df.to_csv(index=False)
                                st.download_button('Download archive CSV (permanent delete)', data=csv, file_name='permanent_deleted_patients.csv', mime='text/csv')
                                c.execute(f'DELETE FROM patients WHERE patient_id IN ({placeholders})', tuple(ids))
                                conn.commit()
                                conn.close()
                                log_action(st.session_state['user_id'], role, 'permanent_delete', f'Permanently deleted {len(ids)} soft-deleted patients')
                                st.success(f'Permanently deleted {len(ids)} patients. Archive CSV available for download above.')
                        except Exception as e:
                            st.error(f'Permanent delete failed: {e}')
                if st.button('Generate demo old patients (for retention test)'):
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        import pandas as pd
                        old_ts = (pd.Timestamp.now() - pd.Timedelta(days=400)).isoformat()
                        demo = [
                            ('Old Patient A', '000-000-0001', 'Test', None, None, old_ts),
                            ('Old Patient B', '000-000-0002', 'Test', None, None, old_ts)
                        ]
                        c.executemany('INSERT INTO patients (name, contact, diagnosis, anonymized_name, anonymized_contact, date_added) VALUES (?, ?, ?, ?, ?, ?)', demo)
                        conn.commit()
                        conn.close()
                        st.success('Inserted demo old patients dated 400 days ago.')
                    except Exception as e:
                        st.error(f'Insert failed: {e}')
                st.markdown('**Data Retention (Admin)**')
                retention_days = st.number_input('Retention days (soft-delete patients older than this). Use 0 to purge all', min_value=0, value=365)
                if st.button('Purge (soft-delete) patients older than retention'):
                    try:
                        import pandas as pd
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        if int(retention_days) == 0:
                            c.execute("SELECT patient_id, name, contact, diagnosis, date_added FROM patients WHERE (deleted_at IS NULL OR deleted_at='')")
                            rows = c.fetchall()
                        else:
                            cutoff = (datetime.now() - pd.Timedelta(days=int(retention_days))).isoformat()
                            c.execute("SELECT patient_id, name, contact, diagnosis, date_added FROM patients WHERE (deleted_at IS NULL OR deleted_at='') AND date(date_added) < date(?)", (cutoff,))
                            rows = c.fetchall()
                        if not rows:
                            st.info('No patients older than retention period.')
                        else:
                            df = pd.DataFrame(rows, columns=['patient_id', 'name', 'contact', 'diagnosis', 'date_added'])
                            csv = df.to_csv(index=False)
                            st.download_button('Download archive CSV of purged patients', data=csv, file_name='purged_patients.csv', mime='text/csv')
                            nowts = datetime.now().isoformat()
                            ids = [r[0] for r in rows]
                            c.executemany('UPDATE patients SET deleted_at=? WHERE patient_id=?', [(nowts, pid) for pid in ids])
                            conn.commit()
                            conn.close()
                            log_action(st.session_state['user_id'], role, 'data_retention_purge', f'Purged {len(ids)} patients older than {retention_days} days')
                            st.success(f'Soft-deleted {len(ids)} patients and provided CSV archive.')
                    except Exception as e:
                        st.error(f'Purge failed: {e}')

            with activity_tab:
                st.caption('Tip: Filter and visualize actions over time.')
                try:
                    import pandas as pd
                    import altair as alt
                    conn = sqlite3.connect(DB_NAME)
                    logs_df = pd.read_sql_query('SELECT timestamp, action, role FROM logs', conn)
                    conn.close()
                    if logs_df.empty:
                        st.info('No activity logs available yet.')
                    else:
                        logs_df['date'] = pd.to_datetime(logs_df['timestamp']).dt.date
                        min_date = logs_df['date'].min()
                        max_date = logs_df['date'].max()
                        start_date = st.date_input('Start date', value=min_date)
                        end_date = st.date_input('End date', value=max_date)
                        actions = sorted(logs_df['action'].unique().tolist())
                        sel_actions = st.multiselect('Action types', actions, default=actions)
                        mask = (logs_df['date'] >= start_date) & (logs_df['date'] <= end_date) & (logs_df['action'].isin(sel_actions))
                        filtered = logs_df.loc[mask]
                        if filtered.empty:
                            st.warning('No logs for the selected range/filters.')
                        else:
                            agg = filtered.groupby(['date', 'action']).size().reset_index(name='count')
                            chart = alt.Chart(agg).mark_bar().encode(
                                x=alt.X('date:T', title='Date'),
                                y=alt.Y('count:Q', title='Actions'),
                                color=alt.Color('action:N', title='Action'),
                                tooltip=['date', 'action', 'count']
                            ).properties(height=350)
                            st.altair_chart(chart, use_container_width=True)
                            last_week_cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
                            last7 = logs_df[pd.to_datetime(logs_df['timestamp']) >= last_week_cutoff]
                            st.metric('Actions last 7 days', int(last7.shape[0]))
                except Exception as e:
                    st.error(f'Activity graph error: {e}')

        elif role == 'doctor':
            (patients_tab,) = st.tabs(['Patients'])
            with patients_tab:
                if st.button('View Anonymized Patient Data'):
                    conn = sqlite3.connect(DB_NAME)
                    try:
                        import pandas as pd
                        df = pd.read_sql_query("SELECT patient_id, anonymized_name, anonymized_contact, diagnosis, date_added FROM patients WHERE deleted_at IS NULL OR deleted_at=''", conn)
                        st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f'Error: {e}')
                    finally:
                        conn.close()

        elif role == 'receptionist':
            add_tab, edit_tab = st.tabs(['Add Patient', 'Edit Patients'])
            with add_tab:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                with st.form('add_patient_form'):
                    name = st.text_input('Patient Name')
                    contact = st.text_input('Contact')
                    diagnosis = st.text_input('Diagnosis')
                    submitted = st.form_submit_button('Add Patient')
                    if submitted:
                        date_added = datetime.now().isoformat()
                        c.execute('INSERT INTO patients (name, contact, diagnosis, date_added) VALUES (?, ?, ?, ?)',
                                  (name, contact, diagnosis, date_added))
                        conn.commit()
                        log_action(st.session_state['user_id'], role, 'add_patient', f'Receptionist added patient {name}.')
                        st.success('Patient added successfully.')
                conn.close()
            with edit_tab:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT patient_id, anonymized_name, anonymized_contact, diagnosis FROM patients WHERE deleted_at IS NULL OR deleted_at=''")
                patients = c.fetchall()
                for pid, anon_name, anon_contact, diagnosis in patients:
                    display_name = anon_name if anon_name else 'REDACTED'
                    display_contact = anon_contact if anon_contact else 'REDACTED'
                    with st.expander(f'Edit {display_name} ({pid})'):
                        st.write(f'Contact: {display_contact}')
                        new_name = st.text_input(f'New Name for {pid} (will overwrite if provided)', value='', key=f'name_{pid}')
                        new_contact = st.text_input(f'New Contact for {pid} (will overwrite if provided)', value='', key=f'contact_{pid}')
                        new_diag = st.text_input(f'New Diagnosis for {pid}', value=diagnosis, key=f'diag_{pid}')
                        if st.button(f'Update {pid}'):
                            updates = []
                            params = []
                            if new_name.strip():
                                updates.append('name=?')
                                params.append(new_name.strip())
                            if new_contact.strip():
                                updates.append('contact=?')
                                params.append(new_contact.strip())
                            if new_diag.strip() and new_diag.strip() != diagnosis:
                                updates.append('diagnosis=?')
                                params.append(new_diag.strip())
                            if updates:
                                params.append(pid)
                                sql = f"UPDATE patients SET {', '.join(updates)} WHERE patient_id=?"
                                try:
                                    c.execute(sql, tuple(params))
                                    conn.commit()
                                    log_action(st.session_state['user_id'], role, 'edit_patient', f'Receptionist edited patient {pid}.')
                                    st.success('Patient record updated.')
                                except Exception as e:
                                    st.error(f'Update failed: {e}')
                conn.close()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Footer with uptime
    uptime = int(time.time() - APP_START_TIME)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    st.markdown(f'<div class="footer">System Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)
    # Show last DB modification time for synchronization info
    try:
        mtime = os.path.getmtime(DB_NAME)
        last_sync = datetime.fromtimestamp(mtime).isoformat()
        st.markdown(f'<div class="footer">Last DB update: {last_sync}</div>', unsafe_allow_html=True)
    except Exception:
        pass

if __name__ == '__main__':
    main()
