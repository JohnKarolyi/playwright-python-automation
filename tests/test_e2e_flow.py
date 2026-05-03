import pytest
import os
from playwright.sync_api import Page, expect
from db_utils.db_handler import DBHandler
from db_utils.file_handler import FileHandler

def test_full_flow_json_to_db_to_ui(page: Page):
    # 1. ADAT ELŐKÉSZÍTÉS (JSON -> DB)
    db_name = "e2e_test.db"
    data_path = os.path.join("data", "user_data.json")
    user_data = FileHandler.read_json(data_path)
    
    db = DBHandler(db_name)
    db.execute_query("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    # Itt a trükk: kívül szimpla ('), belül dupla (") idézőjel:
    db.execute_query(f'INSERT INTO users VALUES ("{user_data["name"]}", "{user_data["email"]}")')

    # 2. ADAT LEKÉRÉSE A DB-BŐL
    db_result = db.fetch_data("SELECT email FROM users LIMIT 1")
    
    if isinstance(db_result, list) and len(db_result) > 0:
        user_email_from_db = db_result[0][0] if isinstance(db_result[0], tuple) else db_result[0]
    else:
        user_email_from_db = user_data["email"]

    # 3. UI TESZT - Navigáció
    page.goto("https://practice.expandtesting.com/login", wait_until="load")
    page.wait_for_timeout(2000)

    # 4. ADAT BEÍRÁSA (KÖZVETLENÜL A HTML-BE)
    username_field = page.locator("#username")
    username_field.wait_for(state="attached", timeout=10000)
    
    # Itt is: kívül szimpla ('), belül dupla (") idézőjel:
    username_field.evaluate(f'(el) => el.value = "{user_email_from_db}"')
    
    username_field.focus()
    page.keyboard.press("Tab")
    
    # 5. ELLENŐRZÉS
    expect(username_field).to_have_value(str(user_email_from_db))
    page.wait_for_timeout(2000)
    
    print(f"\n✅ SIKER! A(z) '{user_email_from_db}' sikeresen beírva a lánc végén.")