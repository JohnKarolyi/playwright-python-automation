import pytest
import os
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler

def test_file_to_db_integration():
    db_name = "integration_test.db"
    
    # 1. Adatok beolvasása
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)
    
    # 2. Adatbázis műveletek
    db = DBHandler(db_name)
    db.execute_query("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    db.execute_query(f"INSERT INTO users VALUES ('{user_data['name']}', '{user_data['email']}')")

    # 3. Ellenőrzés
    result = db.fetch_data(f"SELECT * FROM users WHERE email = '{user_data['email']}'")
    
    assert len(result) > 0
    assert result[0][0] == user_data["name"]
    
    print(f"\n✅ Teszt kész, a conftest.py most törli a fájlt...")