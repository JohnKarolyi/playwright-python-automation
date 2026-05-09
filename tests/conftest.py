import pytest
import os
import time
import gc

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
    # SQLite adatbázis fájl takarítása tesztek között
    temp_files = ["integration_test.db"]
    yield
    gc.collect()
    time.sleep(0.2)
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception:
                pass

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Itt adjuk meg, hova kerüljenek a videók a futás során
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }
