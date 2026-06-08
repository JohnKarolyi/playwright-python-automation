import os
import json
import pytest
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler


def test_full_flow_json_to_db_to_ui(page):

    db_name = "e2e_test.db"
    data_path = os.path.join("data", "user_data.json")

    # 1. JSON betöltés
    with open(data_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    # Mivel a fájl egy lista, kivesszük az első elemet ("Happy Path")
    if isinstance(user_data, list):
        user_data = user_data[0]

    # Csak a "username"-et ellenőrizzük, mert az biztosan benne van a JSON-ben
    if "username" not in user_data:
        raise ValueError("Missing key in JSON: username")
        
    # Mivel a JSON-ben nincs email mező, generálunk egyet a "student" néből
    test_email = f"{user_data['username']}@example.com"

    # 2. DB előkészítés
    db = DBHandler(db_name)
    # Töröljük a régi sémájú táblát, hogy az új oszlopok érvényesüljenek
    db.execute_query("DROP TABLE IF EXISTS users")  
    db.execute_query("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT)")
    db.execute_query("DELETE FROM users")

    # Beszúrjuk az adatbázisba a nevet és a generált emailt
    insert_query = f"INSERT INTO users (username, email) VALUES ('{user_data['username']}', '{test_email}')"
    db.execute_query(insert_query)

    # 3. UI ellenőrzés
    page.goto("http://127.0.0.1:5000")

    # Kitöltjük az oldalon a mezőket a böngészőben
    page.fill("#name", user_data["username"])
    page.fill("#email", test_email)