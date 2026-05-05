import pytest
from playwright.sync_api import Page, expect

def test_playwright_is_working(page: Page):
    # 1. Navigáljunk a Google-re
    page.goto("https://google.com")
    
    # 2. Elfogadjuk a sütiket (ha megjelenik a gomb)
    # Ez fontos, mert a gomb felirata nyelvenként eltérhet (pl. "Accept all")
    accept_button = page.get_by_role("button").filter(has_text="Összes elfogadása")
    if accept_button.is_visible():
        accept_button.click()

    # 3. Ellenőrizzük, hogy a keresőmező ott van-e
    search_box = page.get_by_role("combobox")
    expect(search_box).to_be_visible()
    
    print("\n✅ Playwright sikeresen elindult és látja az oldalt!")