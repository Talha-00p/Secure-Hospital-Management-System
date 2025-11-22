import sqlite3
import json
import db_init

def main():
    conn = sqlite3.connect(db_init.DB_NAME)
    c = conn.cursor()
    rows = list(c.execute('SELECT user_id, username, password, role FROM users'))
    conn.close()
    print(json.dumps(rows, indent=2))

if __name__ == '__main__':
    main()
