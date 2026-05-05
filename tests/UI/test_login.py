import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage

def test_successful_login(page):
    # 1. Oldal objektum példányosítása
    login_page = LoginPage(page)
    
    # 2. Lépések végrehajtása
    login_page.navigate()
    # Itt az ExpandTesting oldalhoz valódi adatok kellenek:
    login_page.login("practice", "SuperSecretPassword!")
    
    # 3. Ellenőrzések (Assert-ek a tesztben - 6. kérdés javítása)
    # Ellenőrizzük, hogy az URL tartalmazza-e a 'secure' szót a belépés után
    assert "/secure" in page.url
    
    # Ellenőrizzük, hogy látható-e a sikeres belépést jelző üzenet
    success_message = page.locator("#flash")
    expect(success_message).to_be_visible()
    assert "You logged into a secure area!" in success_message.inner_text() 