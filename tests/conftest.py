import pytest
import os
import time
import gc
import allure

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
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
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720},
        # GLOBÁLIS LASSÍTÁS: Minden művelet után vár 0.8 másodpercet
        "slow_mo": 800 
    }

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "teardown":
        page = item.funcargs.get("page")
        if page:
            try:
                video_path = page.video.path()
                if video_path and os.path.exists(video_path):
                    allure.attach.file(
                        video_path,
                        name="Execution_Video.webm",
                        attachment_type=allure.attachment_type.WEBM
                    )
            except Exception as e:
                print(f"Video attachment failed: {e}")