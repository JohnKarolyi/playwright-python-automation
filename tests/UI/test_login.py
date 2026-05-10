import pytest

def test_successful_login(page, login_page):
    # 1. Oldal megnyitása
    login_page.navigate()
    
    # 2. Bejelentkezés a hivatalos adatokkal
    login_page.login("student", "Password123")
    
    # 3. Ellenőrzés: Megvárjuk, amíg az URL megváltozik a sikeres oldalra
    page.wait_for_url("**/logged-in-successfully/")
    
    # 4. Assertion-ök (Hogy biztosan zöld legyen a teszt)
    assert "logged-in-successfully" in page.url
    
    # Opcionális: Ellenőrizzük a sikeres üzenet megjelenését is
    success_message = page.locator(".post-title")
    assert success_message.is_visible()
    assert "Logged In Successfully" in success_message.text_content()