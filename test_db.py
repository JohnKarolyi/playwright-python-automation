from db_utils.db_handler import DBHandler

db = DBHandler()

db.save_user(
    "John",
    35,
    "1990-01-01",
    "john@test.com"
)

user = db.get_user_by_email("john@test.com")

print(user)