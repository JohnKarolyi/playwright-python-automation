import os
import sys
import time
import json
import socket
import subprocess
import pytest

# Gyökérkönyvtár hozzáadása a python path-hoz, hogy az importok működjenek
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Biztonságos import: ha a struktúrád eltér, igazítsd a projekthez
try:
    from pages.login_page import LoginPage
except ImportError:
    LoginPage = None

def is_server_running(port=5000):
    """Ellenőrzi, hogy fut-e már valami a megadott porton."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="session", autouse=True)
def start_local_server():
    """Automatikusan elindítja a háttérben a Flask szervert, ha még nem fut."""
    if is_server_running(5000):
        yield
        return

    # Flask alkalmazás indítása (feltételezve, hogy az app/app.py útvonalon van)
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/app.py"))
    
    process = subprocess.Popen(
        ["python", app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Várunk max 5 másodpercet a szerver indulására
    for _ in range(50):
        if is_server_running(5000):
            break
        time.sleep(0.1)
    else:
        process.terminate()
        raise RuntimeError("A Flask szerver nem indult el az 5000-es porton!")

    yield  # Itt futnak le a tesztek

    # Teszt session végén leállítjuk a szervert
    process.terminate()
    process.wait()

@pytest.fixture
def login_page(page):
    """Példányosítja és visszaadja a LoginPage objektumot a tesztek számára."""
    if LoginPage is None:
        raise ImportError("Nem sikerült importálni a LoginPage osztályt! Ellenőrizd a 'pages/login_page.py' útvonalat.")
    return LoginPage(page)

@pytest.fixture
def logged_api(page):
    """
    Transzparens Allure API Network Logging Wrapper, ami támogatja a hibrid fail-fast ellenőrzéseket.
    Megfelel a `logged_api.request(method, url)` hívási konvenciónak.
    """
    try:
        import allure
    except ImportError:
        allure = None

    # Eseménykezelők a UI-alapú hálózati forgalom naplózásához
    def handle_request(request):
        if "/api/" in request.url or "zippopotam" in request.url:
            if allure and request.post_data:
                try:
                    allure.attach(
                        body=json.dumps(json.loads(request.post_data), indent=2, ensure_ascii=False),
                        name=f"UI API Request JSON -> {request.method} {request.url}",
                        attachment_type=allure.attachment_type.JSON
                    )
                except Exception:
                    allure.attach(
                        body=str(request.post_data),
                        name=f"UI API Request Raw -> {request.method} {request.url}",
                        attachment_type=allure.attachment_type.TEXT
                    )

    def handle_response(response):
        if "/api/" in response.url or "zippopotam" in response.url:
            if allure:
                try:
                    body = response.json()
                    allure.attach(
                        body=json.dumps(body, indent=2, ensure_ascii=False),
                        name=f"UI API Response JSON <- {response.status} {response.url}",
                        attachment_type=allure.attachment_type.JSON
                    )
                except Exception:
                    try:
                        allure.attach(
                            body=response.text(),
                            name=f"UI API Response Text <- {response.status} {response.url}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    except Exception:
                        pass

    page.on("request", handle_request)
    page.on("response", handle_response)

    # Egy egyedi wrapper osztály, ami biztosítja a .request() metódust a tesztnek
    class LoggedAPIClient:
        def __init__(self, playwright_page):
            self._page = playwright_page
            self._request_context = playwright_page.context.request

        def request(self, method: str, url: str, **kwargs):
            """Generikus kérésindító, ami automatikusan naplóz Allure-be."""
            full_url = url if url.startswith("http") else f"http://127.0.0.1:5000{url}"
            
            response = self._request_context.fetch(full_url, method=method, **kwargs)
            
            if allure:
                if "data" in kwargs or "json" in kwargs:
                    payload = kwargs.get("json") or kwargs.get("data")
                    allure.attach(
                        body=json.dumps(payload, indent=2, ensure_ascii=False) if isinstance(payload, (dict, list)) else str(payload),
                        name=f"Hybrid Fail-Fast Request -> {method} {full_url}",
                        attachment_type=allure.attachment_type.JSON if isinstance(payload, (dict, list)) else allure.attachment_type.TEXT
                    )
                
                try:
                    allure.attach(
                        body=json.dumps(response.json(), indent=2, ensure_ascii=False),
                        name=f"Hybrid Fail-Fast Response <- {response.status} {full_url}",
                        attachment_type=allure.attachment_type.JSON
                    )
                except Exception:
                    allure.attach(
                        body=response.text(),
                        name=f"Hybrid Fail-Fast Response Text <- {response.status} {full_url}",
                        attachment_type=allure.attachment_type.TEXT
                    )
            
            return response

    return LoggedAPIClient(page)
