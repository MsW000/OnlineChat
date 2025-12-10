import psycopg2

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='zero42', 
    host='localhost',
    port='5432'
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT            
)
""")

conn.commit()