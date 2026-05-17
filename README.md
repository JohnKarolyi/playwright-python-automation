# Python Playwright Automation Framework 🚀

# Playwright Python Automation Project
[Allure Report megnyitása](https://johnkarolyi.github.io/playwright-python-automation/)


Ez egy modern, Python-alapú automatizált tesztkeretrendszer, amely a **Playwright** könyvtárat használja a stabil és gyors UI teszteléshez.

## 🛠 Alkalmazott Technológiák
* **Nyelv:** Python 3.11+
* **Teszt keretrendszer:** Pytest
* **Automatizáló eszköz:** Playwright
* **Adatkezelés:** JSON és SQLite (SQL)
* **Architektúra:** Page Object Model (POM)

## ✨ Főbb Jellemzők
* **POM struktúra:** Tiszta, karbantartható kód felépítés.
* **Automatizált tesztek:** Bejelentkezési folyamatok validálása valós környezetben.
* **Cross-browser:** Több böngésző támogatása.
* **Adatvezérelt integráció:** JSON fájlokból történő automatikus adatkezelés.
* **Adatbázis validáció:** SQLite alapú SQL lekérdezések a tesztek ellenőrzéséhez.
 
## 🛠️ Technikai Kiemelések és Megoldások
### 🚀 Hibrid UI + API Architektúra (Mai fejlesztés)

#### 1. Hibrid UI + API Tesztelés (Flakiness Csökkentés)
A keretrendszer nem csupán elszigetelt UI teszteket futtat, hanem hibrid megközelítést alkalmaz. A nehézkes és lassú böngészős interakciók előtt a háttérben **API alapú egészségügyi ellenőrzést (Health Check)** végez. Amennyiben a backend vagy a vizsgált végpont nem érhető el (nem 200-as státuszkódot ad), a UI teszt el sem indul. Ez drasztikusan csökkenti a fals negatív (flaky) teszteredményeket és erőforrást spórol a CI/CD pipeline-ban.

#### 2. Transzparens Allure API Network Logging Wrapper
A `conftest.py` fájlban implementálásra került egy egyedi, újrafelhasználható **Playwright APIRequestContext Wrapper**. Ez a komponens teljesen automatikusan, transzparens módon naplózza és ágyazza be a tesztriportokba a hálózati forgalmat. Ha a teszt lefut, az Allure riportban fa-struktúrába rendezve, formázott JSON-ként megtekinthető:
* A küldött **HTTP Metódus és URL**
* A **Request Body (Payload)** vagy URL paraméterek
* A kapott **Response Status Code**
* A szerver által visszaadott **Response Body (JSON vagy Raw Text)**

#### 3. Komplett Üzleti Logika Lefedése (POM alapon)
A `LoginPage` Page Object Model struktúrát felhasználva a tesztek egyszerre fedik le a:
* **Happy Path (Pozitív ág)**: Sikeres bejelentkezés és átirányítás validálása.
* **Negatív ág (Hibakezelés)**: Sikertelen bejelentkezés ellenőrzése dinamikus hibaüzenet-validációval (`Your password is invalid!`).


## 🔄 End-to-End (E2E) Tesztfolyamat

A projekt tartalmaz egy komplex integrációs tesztet (`test_e2e_flow.py`), amely a következő lépéseken megy keresztül:

1. **Adat-előkészítés**: Beolvas egy felhasználói profilt egy `JSON` fájlból.
2. **Adatbázis integráció**: Az adatokat elmenti egy ideiglenes `SQLite` adatbázisba.
3. **UI Automatizálás**:
   - Elindít egy böngészőt a **Playwright** segítségével.
   - Navigál a bejelentkező oldalra.
   - Kezeli a felugró süti-ablakokat (JavaScript alapú eltávolítás).
   - Beírja az adatbázisból visszakért e-mail címet a bejelentkező mezőbe.
4. **Validáció**: Ellenőrzi, hogy a felületen megjelenő adat megegyezik-e az eredeti forrásadattal.
5. **Takarítás**: A teszt végeztével automatikusan törli az ideiglenes adatbázis fájlt.

Ebben a projektben egy komplex automatizálási folyamatot valósítottam meg, amely során több technikai kihívást is sikerült leküzdenem:

- **Teljes E2E Adatfolyam**: Megterveztem egy folyamatot, ahol a tesztadatok **JSON** fájlból indulnak, egy **SQLite** adatbázisba kerülnek, majd a **Playwright** segítségével egy webes felületen (UI) kerülnek ellenőrzésre.
- **Stabil UI Automatizálás**:
  - A makacs süti-banner (cookie banner) okozta kitakarási hibákat JavaScript injektálással (`evaluate` metódus) hárítottam el, így a teszt akkor is sikeres, ha a gombok nem láthatóak.
  - Nyelvfüggetlen technikai azonosítókat (ID-k) használtam, hogy a tesztek az oldal különböző nyelvű verzióin is stabilan fussanak.
- **Tiszta Tesztarchitektúra**:
  - A tesztek utáni automatikus takarítást (adatbázis fájlok törlése) a `conftest.py` fájlban központosítottam (teardown folyamat).
  - Különálló modulokat készítettem a fájlkezeléshez és az adatbázis-műveletekhez a könnyebb karbantarthatóság érdekében.
- **Operációs Rendszer Szintű Hibakezelés**: Megoldottam az SQLite fájlzárolási problémáit (WinError 32) a Python szemétgyűjtőjének (Garbage Collector) és időzítéseknek a finomhangolásával.

## 📁 Projekt Struktúra
* `pages/`: Page Object osztályok (Lokalizátorok és akciók)
* `tests/`: Tényleges tesztesetek
* `requirements.txt`: Függőségek listája

## 🚀 Telepítés és Futtatás
1. `pip install -r requirements.txt`
2. `playwright install`
3. `pytest --headed`

## 📊 Teszt Riportok (Allure)

A legfrissebb tesztfuttatási eredmények és videók megtekinthetők az alábbi linken:

👉 **[Allure Report megnyitása](https://JohnKarolyi.github.io/playwright-python-automation/)**

*(Megjegyzés: A riport minden sikeres GitHub Actions futtatás után automatikusan frissül.)*
![Playwright Tests](https://github.com/JohnKarolyi/playwright-python-automation/actions/workflows/playwright.yml/badge.svg)
