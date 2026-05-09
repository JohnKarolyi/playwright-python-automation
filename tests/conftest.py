import pytest
import os
import time
import gc
import allure

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
    temp_files = ["integration_test.db"]
    yield
    # Kényszerítsük a Python-t a takarításra, hogy a DB fájl elengedhető legyen
    gc.collect()
    time.sleep(0.2)
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"\n[Cleanup] {file} törölve.")
            except Exception as e:
                print(f"\n[Cleanup Error] Sikertelen törlés: {e}")

# VIDEÓ RÖGZÍTÉS BEÁLLÍTÁSA A BÖNGÉSZŐ KONTEXTUSBAN
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }

# VIDEÓ AUTOMATIKUS BECSATOLÁSA AZ ALLURE RIPORTBA
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Csak a teszt futási szakaszában (call) keressük a videót
    if report.when == "call":
        page = item.funcargs.get("page")
        if page:
            # Fontos: hagyjunk időt a Playwright-nak lezárni a videófájlt!
            time.sleep(1) 
            video_path = page.video.path()
            
            if video_path and os.path.exists(video_path):
                # A name="video.webm" segít az Allure-nek és a böngészőnek a felismerésben
                allure.attach.file(
                    video_path,
                    name="video.webm", 
                    attachment_type=allure.attachment_type.WEBM
                )