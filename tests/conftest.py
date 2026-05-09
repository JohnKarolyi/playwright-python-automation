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

# VIDEÓ AUTOMATIKUS BECSATOLÁSA - STABILIZÁLT FIXTURE
@pytest.fixture(autouse=True)
def attach_video_on_completion(request):
    yield
    # Ez a rész a teszt lefutása UTÁN hajtódik végre
    page = request.node.funcargs.get("page")
    if page:
        try:
            # Megszerezzük a videó elérési útját
            video_path = page.video.path()
            
            # Várunk egy kicsit, hogy a Playwright a háttérben lezárja a fájlt
            # Nem zárunk context-et kézzel, hogy ne ütközzünk a Pytest-tel!
            time.sleep(1) 
            
            if video_path and os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name="Test_Execution_Video.webm", 
                    attachment_type=allure.attachment_type.WEBM
                )
        except Exception as e:
            # Ha nincs videó (pl. API tesztnél), csendben továbblépünk
            print(f"\n[Video Attachment Info] {e}")