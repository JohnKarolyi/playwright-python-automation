from db_utils.db_handler import DBHandler

db = DBHandler()

db.execute_query("DELETE FROM users")

print("Database cleaned successfully")