import sqlite3

class DBHandler:  # <--- Ennek pontosan így kell szerepelnie
    def __init__(self, db_name="test_database.db"):
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