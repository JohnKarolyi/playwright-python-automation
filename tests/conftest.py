import pytest
import os
import time
import gc
import allure

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
    temp_files = ["integration_test.db"]
    yield
    # Kényszerítsük a Python-t a takarításra
    gc.collect()
    time.sleep(0.2)
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"\n[Cleanup] {file} törölve.")
            except Exception as e:
                print(f"\n[Cleanup Error] Sikertelen törlés: {e}")

# VIDEÓ RÖGZÍTÉS BEÁLLÍTÁSA
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }

# VIDEÓ BECSATOLÁSA AZ ALLURE RIPORTBA
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Csak a teszt futási fázisában ("call") nézzük
    if report.when == "call":
        # Megkeressük a 'page' objektumot a tesztben
        page = item.funcargs.get("page")
        if page:
            # Megvárjuk, amíg a videó fájl elérhetővé válik a lemezre írás után
            # Nem zárunk context-et kézzel, mert az törölheti a fájlt!
            time.sleep(0.5) 
            video_path = page.video.path()
            
            if video_path and os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name="Test_Execution_Video",
                    attachment_type=allure.attachment_type.WEBM
                )