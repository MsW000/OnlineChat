from backend.db_connect import cur, conn

cur.executed("SELECT * FROM users")
print(cur.fetchall())

cur.close()
conn.close()