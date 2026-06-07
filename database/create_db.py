import sqlite3

conn = sqlite3.connect("database/test.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    birth_date TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully.")