import pytest
import allure
from playwright.sync_api import expect
from pages.login_page import LoginPage

@allure.epic("Bejelentkezési Folyamatok")
@allure.feature("Hibrid Bejelentkezés")
@allure.story("Sikeres bejelentkezés validálása előzetes API ellenőrzéssel")
def test_hybrid_login_flow(page, logged_api):
    """Hibrid teszt optimalizált időtúllépéssel és tiszta URL assertion-nel."""
    
    # 1. LÉPÉS: API Health Check
    with allure.step("1. API Ellenőrzés: Bejelentkező felület státuszának lekérése"):
        response = logged_api.request("GET", "/practice-test-login/")
        assert response.status == 200, f"A bejelentkező oldal nem érhető el! Státusz: {response.status}"

    # 2. LÉPÉS: UI POM alapú bejelentkezés
    login_page = LoginPage(page)
    
    with allure.step("2. UI Navigáció: Bejelentkező oldal megnyitása"):
        # Felemeljük a limitet 60 másodpercre, hogy a túlterhelt külső szerver se okozzon Timeout hibát
        page.set_default_timeout(60000)
        login_page.navigate()

    with allure.step("3. UI Interakció: Hitelesítési adatok megadása és belépés"):
        login_page.login("student", "Password123")

    with allure.step("4. UI Validáció: Sikeres átirányítás ellenőrzése"):
        # A pontos, perjellel végződő sikeres URL ellenőrzése
        expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")
        
        success_header = page.locator("h1.post-title")
        expect(success_header).to_have_text("Logged In Successfully")


@allure.epic("Bejelentkezési Folyamatok")
@allure.feature("Hibrid Bejelentkezés")
@allure.story("Sikertelen bejelentkezés validálása rossz jelszóval")
def test_hybrid_invalid_login_flow(page, logged_api):
    """Hibrid negatív teszt: API ellenőrzés után hibás jelszavas bejelentkezés validálása."""
    
    # 1. LÉPÉS: API Health Check (Ugyanúgy lefut, mint a pozitív tesztnél)
    with allure.step("1. API Ellenőrzés: Bejelentkező felület státuszának lekérése"):
        response = logged_api.request("GET", "/practice-test-login/")
        assert response.status == 200, f"A bejelentkező oldal nem érhető el! Státusz: {response.status}"

    # 2. LÉPÉS: UI POM példányosítás és navigáció
    login_page = LoginPage(page)
    
    with allure.step("2. UI Navigáció: Bejelentkező oldal megnyitása"):
        page.set_default_timeout(60000)
        login_page.navigate()

    # 3. LÉPÉS: UI Interakció HIBÁS adatokkal
    with allure.step("3. UI Interakció: Hibás jelszó megadása"):
        # Rossz jelszót adunk meg az elutasítás kiváltásához
        login_page.login("student", "RosszJelszo123")

    # 4. LÉPÉS: Negatív UI Validáció
    with allure.step("4. UI Validáció: Hibaüzenet megjelenésének ellenőrzése"):
        # Megvárjuk, amíg láthatóvá válik a piros hibaüzenet panel (#error)
        error_message = page.locator("#error")
        expect(error_message).to_be_visible()
        
        # Leellenőrizzük, hogy a rendszer a megfelelő hibaüzenetet írja-e ki
        expect(error_message).to_have_text("Your password is invalid!")
