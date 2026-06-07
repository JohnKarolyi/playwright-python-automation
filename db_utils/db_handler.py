import sqlite3

class DBHandler:
    def __init__(self, db_name="database/test.db"):
        self.db_name = db_name

    def execute_query(self, query):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def fetch_data(self, query):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def save_user(self, name, age, birth_date, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users
                (name, age, birth_date, email)
                VALUES (?, ?, ?, ?)
            """, (name, age, birth_date, email))

            conn.commit()

    def get_user_by_email(self, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM users
                WHERE email = ?
            """, (email,))

            return cursor.fetchone()

    def delete_user(self, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM users
                WHERE email = ?
            """, (email,))

            conn.commit()