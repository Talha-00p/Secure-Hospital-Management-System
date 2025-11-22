import sqlite3
from security import hash_password

def migrate():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    rows = list(c.execute('SELECT user_id, password FROM users'))
    updated = 0
    for uid, pw in rows:
        if not pw or not pw.startswith('$pbkdf2-sha256$'):
            new_pw = hash_password(pw)
            c.execute('UPDATE users SET password=? WHERE user_id=?', (new_pw, uid))
            updated += 1
    conn.commit()
    conn.close()
    print(f'Migrated {updated} passwords to hashed format.')

if __name__ == '__main__':
    migrate()
