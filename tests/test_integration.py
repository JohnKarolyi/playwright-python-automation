import pytest
import os
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler

def test_file_to_db_integration():
    # 1. Adatok beolvasása JSON fájlból
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)
    
    name = user_data["name"]
    email = user_data["email"]

    # 2. Adatbázis előkészítése (SQLite fájl alapú DB)
    db = DBHandler("integration_test.db")
    db.execute_query("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    
    # Biztonság kedvéért ürítsük ki a táblát, hogy tiszta legyen a teszt
    db.execute_query("DELETE FROM users")

    # 3. Adat mentése az adatbázisba
    db.execute_query(f"INSERT INTO users VALUES ('{name}', '{email}')")

    # 4. Ellenőrzés
    result = db.fetch_data(f"SELECT * FROM users WHERE email = '{email}'")
    
    assert len(result) > 0, "Nem található adat az adatbázisban!"
    # Az első sor első két elemét ellenőrizzük
    assert result[0][0] == name
    assert result[0][1] == email
    
    print(f"\n✅ Sikeres teszt! '{name}' bekerült az adatbázisba a JSON fájlból.")
