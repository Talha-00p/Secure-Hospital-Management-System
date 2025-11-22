"""Schema migration helper: adds `deleted_at` to patients (if missing) and creates `consents` table.
Run with the venv Python to update an existing DB in-place.
"""
import sqlite3

DB = 'hospital.db'

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cursor.fetchall()]
    return column in cols

def migrate():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # add deleted_at if missing
    if not column_exists(c, 'patients', 'deleted_at'):
        try:
            c.execute('ALTER TABLE patients ADD COLUMN deleted_at TEXT')
            print('Added deleted_at column to patients')
        except Exception as e:
            print('Could not add deleted_at:', e)
    # add log_hash to logs if missing
    if not column_exists(c, 'logs', 'log_hash'):
        try:
            c.execute('ALTER TABLE logs ADD COLUMN log_hash TEXT')
            print('Added log_hash column to logs')
        except Exception as e:
            print('Could not add log_hash:', e)
    # create consents table if not exists
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
    print('Migration finished.')

if __name__ == '__main__':
    migrate()
