import pytest
import os
from pages.login_page import LoginPage
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler
from playwright.sync_api import expect

def test_full_flow_json_to_db_to_ui(page):
    # 1. ADAT ELŐKÉSZÍTÉS (JSON -> DB)
    db_name = "e2e_test.db"
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)

    db = DBHandler(db_name)
    # Tábla létrehozása és a korábbi adatok törlése
    db.execute_query("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    db.execute_query("DELETE FROM users")
    
    # Adat beszúrása az adatbázisba (dinamikus string összefűzéssel)
    insert_query = f"INSERT INTO users VALUES ('{user_data['name']}', '{user_data['email']}')"
    db.execute_query(insert_query)

    # 2. ADAT LEKÉRDEZÉS A DB-BŐL
    db_result = db.fetch_data("SELECT email FROM users LIMIT 1")
    
    # Az SQLite általában listában lévő tuple-ként adja vissza az adatot: [('email@test.com',)]
    user_email_from_db = None
    if db_result and len(db_result) > 0:
        # Kinyerjük az első sor első elemét
        first_row = db_result[0]
        user_email_from_db = first_row[0] if isinstance(first_row, tuple) else first_row

    # 3. UI TESZT - POM használatával
    login_page = LoginPage(page)
    login_page.navigate()

    # 4. ADAT BEÍRÁSA ÉS ELLENŐRZÉS
    if user_email_from_db:
        # A LoginPage-ben definiált modern lokátort használjuk
        login_page.username_field.fill(user_email_from_db)
        
        # Ellenőrizzük, hogy a mező értéke megegyezik-e az adatbázisból kapottal
        expect(login_page.username_field).to_have_value(user_email_from_db)

    # A db.close() hívást töröltük, mert a DBHandler osztályod nem tartalmazza ezt a metódust.