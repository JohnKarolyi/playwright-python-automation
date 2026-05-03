import pytest
import os
import time
import gc

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
    temp_files = ["integration_test.db"]
    
    yield
    
    # Kényszerítsük a Python-t, hogy takarítsa el a lezáratlan objektumokat
    gc.collect()
    time.sleep(0.2) # Adjunk egy kis időt az OS-nek a fájl elengedésére
    
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"\n[Cleanup] {file} törölve.")
            except Exception as e:
                print(f"\n[Cleanup Error] Sikertelen törlés: {e}")