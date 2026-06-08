import pytest
from tests.utils.safe_fill import safe_fill
# Beimportáljuk az Excel adatkezelő függvényt (feltételezve, hogy a tests.test_excel_e2e-ben vagy hasonló helyen van)
from tests.test_excel_e2e import get_invalid_test_data 

def test_invalid_users_not_saved(playwright):
    for row in get_invalid_test_data():

        name, age, birth_date, email = row

        # Elindítjuk a böngészőt
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto("http://127.0.0.1:5000")

        # Biztonságos kitöltés a javított safe_fill függvénnyel
        safe_fill(page, "#name", name)
        safe_fill(page, "#age", age)
        safe_fill(page, "#birth_date", birth_date)
        safe_fill(page, "#email", email)
        
        # Elküldjük az űrlapot (megnyomjuk a gombot)
        page.click("button[type='submit']") # vagy amilyen szelektorod itt volt eredetileg
        
        # Bezárjuk a böngészőt a ciklus végén, hogy ne fogyjon el a memória
        browser.close()
