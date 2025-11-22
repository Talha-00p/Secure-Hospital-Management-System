import sqlite3
from datetime import datetime
from pathlib import Path
from security import hash_password

# Database initialization script for Hospital Management System
# Use an absolute path based on this file so scripts running from other
# working directories still find the same database file.
BASE_DIR = Path(__file__).parent.resolve()
DB_NAME = str(BASE_DIR / 'hospital.db')

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    # Patients table
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        anonymized_name TEXT,
        anonymized_contact TEXT,
        date_added TEXT NOT NULL,
        deleted_at TEXT
    )''')
    # Logs table
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        action TEXT,
        timestamp TEXT,
        details TEXT,
        log_hash TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    # Consents table for GDPR
    c.execute('''CREATE TABLE IF NOT EXISTS consents (
        consent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        consent_ts TEXT,
        details TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Sample users
    users = [
        ('admin', 'admin123', 'admin'),
        ('Dr. Bob', 'doc123', 'doctor'),
        ('Alice_recep', 'rec123', 'receptionist')
    ]
    for username, password, role in users:
        try:
            # store hashed password
            pw_hash = hash_password(password)
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, pw_hash, role))
        except sqlite3.IntegrityError:
            pass
    # Sample patients
    patients = [
        ('John Doe', '123-456-7890', 'Flu', None, None, datetime.now().isoformat()),
        ('Jane Smith', '987-654-3210', 'Diabetes', None, None, datetime.now().isoformat())
    ]
    for name, contact, diagnosis, anon_name, anon_contact, date_added in patients:
        c.execute('INSERT INTO patients (name, contact, diagnosis, anonymized_name, anonymized_contact, date_added) VALUES (?, ?, ?, ?, ?, ?)',
                  (name, contact, diagnosis, anon_name, anon_contact, date_added))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    insert_sample_data()
    print('Database and sample data created.')
