import pytest
from data.excel_reader import get_test_data
from db_utils.db_handler import DBHandler
from tests.utils.safe_fill import safe_fill

db = DBHandler()


def test_valid_users_e2e(page):

    for name, age, birth_date, email in get_test_data():

        page.goto("http://127.0.0.1:5000")

        safe_fill(page, "#name", name)
        safe_fill(page, "#age", age)
        safe_fill(page, "#birth_date", birth_date)
        safe_fill(page, "#email", email)

        page.click("#save-btn")

        # ✔ DB ellenőrzés
        user = db.get_user_by_email(email)

        assert user is not None, f"User not saved: {email}"