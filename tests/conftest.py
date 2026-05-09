import pytest
import os
import time
import gc

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

# VIDEÓ RÖGZÍTÉS KONFIGURÁCIÓJA
# A Playwright automatikusan a 'videos/' mappába ment, 
# az Allure pedig automatikusan beszippantja onnan, ha a keretrendszer kéri.
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }