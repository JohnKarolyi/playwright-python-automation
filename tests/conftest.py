import pytest
import os
import time
import gc
import allure
import json

# ==========================================
# 1. MEGLÉVŐ FIXTURE-ÖK (DB, LASSÍTÁS, VIDEÓ)
# ==========================================

@pytest.fixture(scope="function", autouse=True)
def manage_db_files():
    """SQLite adatbázis takarítása minden teszt után."""
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
def browser_type_launch_args(browser_type_launch_args):
    """Böngésző lassítása – optimalizált érték az időtúllépés (Timeout) elkerülésére."""
    return {
        **browser_type_launch_args,
        "slow_mo": 300  # 300 ms-ra optimalizálva a stabilabb futásért
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Videófelvétel beállításai."""
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Videó automatikus csatolása az Allure riporthoz a teszt lefutása után."""
    outcome = yield
    report = outcome.get_result()
    
    # A 'call' fázis végén mentünk, amikor a teszt lefutott, így elkerüljük az Event loop hibát
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                video_path = page.video.path()
                if video_path and os.path.exists(video_path):
                    allure.attach.file(
                        video_path,
                        name="Failure_Video.webm",
                        attachment_type=allure.attachment_type.WEBM
                    )
            except Exception:
                pass

# ==========================================
# 2. ÚJ FIXTURE-ÖK AZ API AUTOMATIKUS NAPLÓZÁSHOZ (ÉLES ÜZEMMÓD)
# ==========================================

@pytest.fixture(scope="session")
def api_context(playwright):
    """Playwright APIRequestContext létrehozása a gyakorló oldal tiszta domainjével."""
    context = playwright.request.new_context(base_url="https://practicetestautomation.com")
    yield context
    context.dispose()

@pytest.fixture(scope="function")
def logged_api(api_context):
    """Wrapper kliens, ami transzparensen Allure riportba ment minden API kérést és választ."""
    class LoggedAPIClient:
        def request(self, method: str, url: str, **kwargs):
            method_upper = method.upper()
            step_name = f"API {method_upper} ➔ {url}"
            
            with allure.step(step_name):
                # 1. Kérés adatainak (Payload/Params) mentése az Allure-ba
                if "data" in kwargs:
                    allure.attach(
                        json.dumps(kwargs["data"], indent=2, ensure_ascii=False),
                        name="📤 Request Body (Payload)",
                        attachment_type=allure.attachment_type.JSON
                    )
                elif "params" in kwargs:
                    allure.attach(
                        json.dumps(kwargs["params"], indent=2, ensure_ascii=False),
                        name="📤 Request URL Params",
                        attachment_type=allure.attachment_type.JSON
                    )

                # 2. A tényleges API hívás végrehajtása a háttérben
                response = api_context.fetch(url, method=method_upper, **kwargs)

                # 3. Válasz státuszkód mentése az Allure-ba
                allure.attach(
                    str(response.status),
                    name="🔢 Response Status Code",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # 4. Válasz body mentése az Allure-ba (JSON vagy szöveg)
                try:
                    allure.attach(
                        json.dumps(response.json(), indent=2, ensure_ascii=False),
                        name="📥 Response Body (JSON)",
                        attachment_type=allure.attachment_type.JSON
                    )
                except Exception:
                    if response.text():
                        allure.attach(
                            response.text(),
                            name="📥 Response Body (Raw Text)",
                            attachment_type=allure.attachment_type.TEXT
                        )

                return response

    return LoggedAPIClient()
