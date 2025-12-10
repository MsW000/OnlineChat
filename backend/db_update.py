from backend.db_connect import conn, cur

cur.execute("UPDATE users SET age = %s WHERE name = %s", (30, "Alice"))
conn.commit()

cur.close()
conn.close()