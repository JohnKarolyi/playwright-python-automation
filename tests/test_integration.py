import pytest
import os
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler

@pytest.mark.database
def test_file_to_db_integration():
    db_name = "integration_test.db"
    
    # 1. Adatok beolvasása
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)
    
    # FIX: Ha a beolvasott adat egy lista, vegyük az első elemet
    if isinstance(user_data, list):
        user_data = user_data[0]
    
    # FIX: Mivel a JSON-ben nincs email mező, generálunk egyet a username alapján
    test_email = f"{user_data['username']}@example.com"
    
    # 2. Adatbázis műveletek
    db = DBHandler(db_name)
    db.execute_query("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT)")
    db.execute_query("DELETE FROM users")  # Biztos ami biztos, takarítsunk beillesztés előtt
    
    # Biztonságosabb beszúrás a generált email használatával
    db.execute_query(f"INSERT INTO users (username, email) VALUES ('{user_data['username']}', '{test_email}')")

    # 3. Ellenőrzés (a generált email alapján keresünk)
    result = db.fetch_data(f"SELECT * FROM users WHERE email = '{test_email}'")
    
    assert len(result) > 0
    assert result[0][0] == user_data["username"]
    assert result[0][1] == test_email
    
    print(f"\n✅ Teszt kész, a conftest.py most törli a fájlt...")
