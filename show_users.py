import sqlite3
import json

def main():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    rows = list(c.execute('SELECT user_id, username, password, role FROM users'))
    conn.close()
    print(json.dumps(rows, indent=2))

if __name__ == '__main__':
    main()
