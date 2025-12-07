import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("SELECT gov_user_id, username, credential_id, email, full_name, is_active, created_at FROM GovUser WHERE username='gov_admin'")
row = cur.fetchone()
print('GovUser row:', row)
if row:
    credential_id = row[2]
    cur.execute("SELECT credential_id, hashed_password, created_at FROM Credential WHERE credential_id=?", (credential_id,))
    cred = cur.fetchone()
    print('Credential row:', cred)
conn.close()
