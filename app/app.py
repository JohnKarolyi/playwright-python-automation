import sys
import os
import re
from datetime import datetime
from flask import Flask, render_template, request

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db_utils.db_handler import DBHandler


app = Flask(__name__)
db = DBHandler()


def write_error_log(message):
    os.makedirs("logs", exist_ok=True)

    with open("logs/validation_errors.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name", "")
        age = request.form.get("age", "")
        birth_date = request.form.get("birth_date", "")
        email = request.form.get("email", "")

        try:

            # NAME
            if not name.isalpha():
                write_error_log(f"Invalid name: {name}")
                return "Invalid name"

            # AGE
            if not str(age).isdigit():
                write_error_log(f"Invalid age: {age}")
                return "Invalid age"

            # DATE
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                write_error_log(f"Invalid date: {birth_date}")
                return "Invalid date"

            # EMAIL
            email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_pattern, email):
                write_error_log(f"Invalid email: {email}")
                return "Invalid email"

            db.save_user(name, int(age), birth_date, email)

            return "User saved successfully!"

        except Exception as e:
            write_error_log(f"Error: {str(e)}")
            return "Validation failed"

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)