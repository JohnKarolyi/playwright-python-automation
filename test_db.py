from db_utils.db_handler import DBHandler

db = DBHandler()

user = db.get_user_by_email("peter@test.com")

print(user)