import pytest
import os
from playwright.sync_api import Page
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler
from pages.login_page import LoginPage

def test_full_flow_json_to_db_to_ui(page: Page):
    # 1. ADAT ELŐKÉSZÍTÉS (JSON -> DB)
    db_name = "e2e_test.db"
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)

    db = DBHandler(db_name)
    db.execute_query("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    
    # Itt a trükk: kívül szimpla ('), belül dupla (") idézőjel:
    db.execute_query(f"INSERT INTO users VALUES ('{user_data['name']}', '{user_data['email']}')")

    # 2. ADAT LEKÉRDEZÉS A DB-BŐL
    db_result = db.fetch_data("SELECT email FROM users LIMIT 1")

    if isinstance(db_result, list) and len(db_result) > 0:
        # Ha tuple-t kapunk vissza, kivesszük az első elemét
        user_email_from_db = db_result[0][0] if isinstance(db_result[0], tuple) else db_result[0]
    else:
        user_email_from_db = user_data["email"]

    # 3. UI TESZT - POM (Page Object Model) használatával
    login_page = LoginPage(page)
    
    # Navigáció az oldalra
    login_page.navigate()
    
    # Várakozás (opcionális, a POM-ba is tehető, de itt hagytam a vizualitás miatt)
    page.wait_for_timeout(1000)

    # 4. ADAT BEÍRÁSA ÉS ELLENŐRZÉS
    # Meghívjuk a POM-ban definiált metódusokat
    login_page.fill_username_custom(user_email_from_db)
    
    # 5. ELLENŐRZÉS (Assertion)
    login_page.verify_username(user_email_from_db)

    page.wait_for_timeout(2000)
    print(f"\n SIKER! A(z) '{user_email_from_db}' sikeresen beírva a lánc végén, POM struktúrával.")