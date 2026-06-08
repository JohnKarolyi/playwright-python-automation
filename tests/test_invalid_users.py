from data.excel_reader import get_invalid_test_data
from tests.utils.safe_fill import safe_fill


def test_invalid_users_e2e(page):

    for name, age, birth_date, email in get_invalid_test_data():

        page.goto("http://127.0.0.1:5000")

        safe_fill(page, "#name", name)
        safe_fill(page, "#age", age)
        safe_fill(page, "#birth_date", birth_date)
        safe_fill(page, "#email", email)

        page.click("button[type=submit]")