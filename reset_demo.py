"""
reset_demo.py

Resets demo state for presentations/tests:
- Deletes all rows from `logs` and `consents`.
- Removes patient records that are not part of the default sample set
  (keeps one record for each default patient name).

It will NOT delete `users` or modify their passwords.

Usage:
    python reset_demo.py
"""
import sqlite3
from pathlib import Path

DB = 'hospital.db'

# Names of default patients inserted by db_init.py
DEFAULT_PATIENT_NAMES = ['John Doe', 'Jane Smith']

def reset():
    if not Path(DB).exists():
        print('Database file not found:', DB)
        return
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Clear logs
    c.execute('DELETE FROM logs')
    print('Deleted all logs')

    # Clear consents
    c.execute('DELETE FROM consents')
    print('Deleted all consents')

    # Patients: keep one record per default name (lowest patient_id), delete others
    kept_ids = set()
    for name in DEFAULT_PATIENT_NAMES:
        c.execute('SELECT patient_id FROM patients WHERE name=? ORDER BY patient_id ASC', (name,))
        row = c.fetchone()
        if row:
            kept_ids.add(row[0])

    # Delete patients that are not in kept_ids
    if kept_ids:
        placeholders = ','.join('?' for _ in kept_ids)
        sql = f'DELETE FROM patients WHERE patient_id NOT IN ({placeholders})'
        c.execute(sql, tuple(kept_ids))
        print(f'Kept patient IDs: {sorted(list(kept_ids))}; deleted other patients.')
    else:
        # If no defaults found, do not delete any patients but reset anonymization/deleted flags
        print('No default patients found; leaving patient rows intact.')

    # Reset anonymized fields and deleted_at for kept patients
    for pid in kept_ids:
        c.execute('UPDATE patients SET anonymized_name=NULL, anonymized_contact=NULL, deleted_at=NULL WHERE patient_id=?', (pid,))

    conn.commit()
    conn.close()
    print('Reset complete.')

if __name__ == '__main__':
    reset()
