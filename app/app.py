from flask import Flask, render_template, request

from db_utils.db_handler import DBHandler

app = Flask(__name__)

db = DBHandler()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        birth_date = request.form.get("birth_date")
        email = request.form.get("email")

        db.save_user(
            name,
            age,
            birth_date,
            email
        )

        return "User saved successfully!"

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)