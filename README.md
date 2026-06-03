# Python Playwright Automation Framework 🚀

# Playwright Python Automation Project
[Allure Report megnyitása](https://johnkarolyi.github.io/playwright-python-automation/)

Ez egy modern, Python-alapú automatizált tesztkeretrendszer, amely a **Playwright** könyvtárat használja a stabil és gyors UI teszteléshez, ötvözve az API szintű validációval és SQL adatbázis-kezeléssel.

## 🛠 Alkalmazott Technológiák
* **Nyelv:** Python 3.11+
* **Teszt keretrendszer:** Pytest
* **Automatizáló eszköz:** Playwright
* **Adatkezelés:** JSON és SQLite (SQL)
* **Architektúra:** Page Object Model (POM)

## ✨ Főbb Jellemzők
* **POM struktúra:** Tiszta, karbantartható kód felépítés.
* **Automatizált tesztek:** Bejelentkezési és összetett üzleti folyamatok validálása.
* **Cross-browser:** Több böngésző támogatása CI/CD környezetben.
* **Adatvezérelt integráció:** Külső JSON fájlokból történő dinamikus adatkezelés (`pytest.mark.parametrize`).
* **Adatbázis validáció:** SQLite alapú SQL lekérdezések a tesztek ellenőrzéséhez.
 
## 🛠️ Technikai Kiemelések és Megoldások

### 🚀 Eseményvezérelt Hibrid UI + API Architektúra

#### 1. 0 ms Slow_Mo & Eseményvezérelt Működés (Új)
A keretrendszer felszámolta a hagyományos tesztautomatizálási anti-patterneket: **nem használunk mesterséges lassításokat (`slow_mo`) vagy merev időzítéseket (`time.sleep()`)** a UI tesztek stabilizálására. A maximális futási sebesség mellett a stabilitást a Playwright natív *Actionability Checks* mechanizmusa, valamint a hálózati és DOM állapotfigyelők (`networkidle`, `domcontentloaded`) garantálják.

#### 2. Intelligens Hibrid Adatvezérlés (Új)
A bejelentkezési tesztek adatai teljesen le vannak választva a tesztlogikáról a `data/user_data.json` fájlba. A Pytest dinamikusan generálja a teszteseteket (Happy Path és Negatív ágak). A teszt végrehajtása előtt a háttérben egy **API alapú egészségügyi ellenőrzést (Health Check)** végzünk. Amennyiben a végpont nem érhető el, a drágább UI teszt el sem indul (Fail-Fast elv).

#### 3. Transzparens Allure API Network Logging Wrapper
A `conftest.py` fájlban implementálásra került egy egyedi, újrafelhasználható **Playwright APIRequestContext Wrapper**. Ez a komponens teljesen automatikusan, transzparens módon naplózza és ágyazza be a tesztriportokba a hálózati forgalmat. Ha a teszt lefut, az Allure riportban formázott JSON-ként megtekinthető:
* A küldött **HTTP Metódus és URL**
* A **Request Body (Payload)** vagy URL paraméterek
* A kapott **Response Status Code**
* A szerver által visszaadott **Response Body (JSON vagy Raw Text)**

---

## 🔄 End-to-End (E2E) Tesztfolyamat (SQLite Integráció)

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

A folyamat során az alábbi technikai kihívások kerültek megoldásra:
- **Stabil UI Automatizálás**: A makacs süti-bannerek okozta kitakarási hibákat JavaScript injektálással (`evaluate` metódus) hárítottam el. Nyelvfüggetlen technikai azonosítókat (ID-k) használtam a stabilitásért.
- **Tiszta Tesztarchitektúra**: A tesztek utáni automatikus takarítást (adatbázis fájlok törlése) a `conftest.py` fájlban központosítottam (teardown folyamat).
- **Operációs Rendszer Szintű Hibakezelés**: Megoldottam az SQLite fájlzárolási problémáit (WinError 32) a Python szemétgyűjtőjének (Garbage Collector) finomhangolásával.

---

## 📁 Projekt Struktúra
* `data/`: Külső tesztadatok (pl. `user_data.json` az adatvezérléshez)
* `pages/`: Page Object osztályok (Lokalizátorok és akciók)
* `tests/`: Tényleges tesztesetek (különválasztott UI és API rétegek)
* `requirements.txt`: Függőségek listája

---

## 🚀 Telepítés és Futtatás
1. Függőségek telepítése:
   ```bash
   pip install -r requirements.txt
   ```
2. Playwright böngészők letöltése:
   ```bash
   playwright install
   ```
3. Tesztek futtatása részletes (verbose) módban:
   ```bash
   pytest tests/UI/test_login.py -v
   ```

---

## 📊 Teszt Riportok (Allure)

A legfrissebb tesztfuttatási eredmények és hibák esetén automatikusan rögzített videók megtekinthetők az alábbi linken:

👉 **[Allure Report megnyitása](https://JohnKarolyi.github.io/playwright-python-automation/)**

*(Megjegyzés: A riport minden sikeres GitHub Actions futtatás után automatikusan frissül.)*

![Playwright Tests](https://github.com/JohnKarolyi/playwright-python-automation/actions/workflows/playwright.yml/badge.svg)
