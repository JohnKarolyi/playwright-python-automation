# tests/UI/test_login.py
import json
import os
import re  # Szükséges a részstring alapú URL illesztéshez (regex)
import pytest
from playwright.sync_api import expect

def load_test_data():
    """
    Segédfüggvény a JSON tesztadatok dinamikus beolvasásához.
    Senior megközelítés: Az adatokat a dedikált data/ mappából töltjük be.
    """
    # Megkeressük a projekt gyökérmappáját a fájl elhelyezkedése alapján
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # Összeállítjuk a pontos útvonalat a data/user_data.json fájlhoz
    json_path = os.path.join(base_dir, "data", "user_data.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# A pytest.mark.parametrize dinamikusan legenerálja a teszteseteket a JSON alapján.
@pytest.mark.parametrize("data", load_test_data(), ids=lambda d: d["test_case"])
def test_hybrid_login_flow(page, login_page, logged_api, data):
    """
    Intelligens hibrid login teszt:
    Adatvezérelt megközelítés, amely ötvözi az API előszűrést a gyors UI végrehajtással.
    Kizárólag a Playwright natív eseményvezérelt auto-waiting mechanizmusára támaszkodik.
    """
    
    # -------------------------------------------------------------
    # 1. SZAKASZ: API ELŐSZŰRÉS ÉS INTEGRÁCIÓS ELLENŐRZÉS (Hibrid réteg)
    # -------------------------------------------------------------
    # Végrehajtunk egy hálózati health check-et az API kliensünkkel a UI teszt indítása előtt (Fail-Fast).
    health_check = logged_api.request("GET", "/practice-test-login/")
    assert health_check.status == 200, f"Az oldal nem érhető el! Státusz: {health_check.status}"

    # -------------------------------------------------------------
    # 2. SZAKASZ: NATÍV PLAYWRIGHT UI VÉGREHAJTÁS (Eseményvezérelt)
    # -------------------------------------------------------------
    login_page.navigate()
    
    # Megvárjuk, amíg a hálózati kérések lecsendesednek a betöltés után.
    page.wait_for_load_state("networkidle")

    # Adatok bevitele dinamikusan a JSON fájlból
    login_page.login(data["username"], data["password"])
    
    # -------------------------------------------------------------
    # 3. SZAKASZ: DINAMIKUS KIÉRTÉKELÉS (ASSERTIONS)
    # -------------------------------------------------------------
    if data["should_succeed"]:
        # Sikeres ág (Happy Path) ellenőrzése
        page.wait_for_load_state("networkidle")
        
        # Senior tipp: A re.compile() segítségével biztosítjuk, hogy a Playwright 
        # részstringként (substring) is sikeresen illessze a kívánt URL szakaszt.
        expect(page).to_have_url(re.compile(data["expected_url_contains"]))
    else:
        # Sikertelen ág (Negatív esetek) ellenőrzése
        page.wait_for_load_state("domcontentloaded")
        
        # A hibaüzenet elem ellenőrzése a Playwright beépített intelligens várakozásával
        error_locator = page.locator("#error")
        expect(error_locator).to_be_visible()
        expect(error_locator).to_have_text(data["expected_error"])
