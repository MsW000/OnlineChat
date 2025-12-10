from backend.db_connect import conn, cur

cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 25))
conn.commit()

cur.close()
conn.close()