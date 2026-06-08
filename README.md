# Python Playwright Automation Framework 🚀

# Playwright Python Automation Project

[![Playwright Tests with Allure](https://github.com)](https://github.com)

📊 **Éles Tesztriport:** [👉 Allure Report megnyitása](https://github.io)

Ez egy modern, Python-alapú automatizált tesztkeretrendszer, amely a Playwright könyvtárat használja a stabil és gyors UI teszteléshez, ötvözve az API szintű validációval és SQL adatbázis-kezeléssel.

---

## 🛠 Alkalmazott Technológiák

* **Nyelv:** Python 3.12+ (Optimalizálva a legújabb verziókra, kompatibilis a Python 3.14-gyel is)
* **Teszt keretrendszer:** Pytest (v9.0.2)
* **Automatizáló eszköz:** Playwright Python
* **Adatkezelés:** JSON, Excel (OpenPyXL) és SQLite3 (`e2e_test.db`)
* **Architektúra:** Page Object Model (POM)

---

## ✨ Főbb Jellemzők

* **POM struktúra:** Tiszta, jól elkülönített, könnyen karbantartható kód felépítés.
* **Automatizált tesztek:** Bejelentkezési és összetett üzleti E2E folyamatok teljes körű validálása.
* **Cross-browser & CI/CD:** GitHub Actions pipeline automatikus háttér-szerver indítással és tiszta, gyorsítótár nélküli böngésző-telepítéssel.
* **Adatvezérelt integráció:** Külső JSON és Excel fájlokból történő dinamikus adatkezelés (`pytest.mark.parametrize`).
* **Adatbázis validáció:** SQLite alapú SQL lekérdezések a tesztek valós idejű ellenőrzéséhez.

---

## 🛠️ Technikai Kiemelések és Megoldások

### 🚀 Eseményvezérelt Hibrid UI + API Architektúra

#### 1. 0 ms Slow_Mo & Eseményvezérelt Működés
A keretrendszer felszámolta a hagyományos tesztautomatizálási anti-patterneket: nem használunk mesterséges lassításokat (`slow_mo`) vagy merev időzítéseket (`time.sleep()`) a UI tesztek stabilizálására. A maximális futási sebesség mellett a stabilitást a Playwright natív Actionability Checks mechanizmusa, valamint a hálózati és DOM állapotfigyelők (`networkidle`, `domcontentloaded`) garantálják.

#### 2. Intelligens Hibrid Adatvezérlés és Optimalizálás
A bejelentkezési tesztek adatai teljesen le vannak választva a tesztlogikáról a `data/user_data.json` fájlba. A Pytest dinamikusan generálja a teszteseteket (Happy Path és Negatív ágak).
* **Fail-Fast API Elv:** A teszt végrehajtása előtt a háttérben egy API alapú egészségügyi ellenőrzést (Health Check) végzünk a gyökér (`/`) útvonalon. Amennyiben a végpont nem érhető el, a költségesebb UI teszt el sem indul.
* **Hálózati Timeout Védelem:** A külső tesztkörnyezetek ingadozásai ellen a `LoginPage` navigációs rétege `wait_until="domcontentloaded"` optimalizálást kapott, így a teszt immunissá vált a harmadik féltől származó lassú scriptek vagy hirdetések miatti 30 másodperces időtúllépési (`TimeoutError`) hibákra.

#### 3. Transzparens Allure API Network Logging Wrapper
A `conftest.py` fájlban implementálásra került egy egyedi, újrafelhasználható Playwright APIRequestContext Wrapper. Ez a komponens teljesen automatikusan, transzparens módon naplózza és ágyazza be a tesztriportokba a hálózati forgalmat. Ha a teszt lefut, az Allure riportban formázott JSON-ként megtekinthető:
* A küldött HTTP Metódus és URL
* A Request Body (Payload) vagy URL paraméterek
* A kapott Response Status Code
* A szerver által visszaadott Response Body (JSON vagy Raw Text)

#### 4. HTML5 Szigorú Mezők Kezelése és Robusztus Kitöltési Stratégia
A tesztadatok sokszínűsége (pl. Excelből érkező érvénytelen tesztkarakterek vagy nyers dátum-időbélyegek) miatt a natív `page.fill()` metódusok köré egy intelligens `safe_fill` wrapper került bevezetésre:
* **Dátum normalizálás:** Az Excelből érkező óra/perc/másodperces időbélyegeket automatikusan `ÉÉÉÉ-HH-NN` formátumra csonkolja, megfelelve a `<input type="date">` elvárásainak.
* **Típus-kényszerítés billentyűleütéssel:** Ha a negatív tesztek szándékosan érvénytelen szöveget (pl. `"abc"` vagy hibás dátumot, pl. `"2025-99-99"`) akarnak beírni szigorú `type="number"` vagy `type="date"` mezőkbe, a függvény átvált natív billentyűleütés-szimulációra (`.type()`), áthidalva a Playwright `.fill()` biztonsági korlátozásait és a *Malformed value* hibákat.

#### 5. Nyilvános API-k Finomhangolt Hibatűrése
A külső pénzügyi/földrajzi API-k (Zippopotam API) terheltségi ingadozásait egyedi, 10 másodperces kérésalapú időkorlátokkal és reálisabb válaszidő-asszertációkkal (`duration < 5.0`) kezeli a keretrendszer, minimalizálva a hamis negatív riasztásokat.

---

### 🔄 End-to-End (E2E) Tesztfolyamat (SQLite Integráció)

A projekt tartalmaz egy komplex integrációs tesztet (`test_e2e_flow.py`), amely a következő lépéseken megy keresztül:
1. **Adat-előkészítés:** Beolvas egy felhasználói profilt egy JSON fájlból. A rendszer fel van készítve az összetett listás és objektum-alapú JSON struktúrák kezelésére is, szükség esetén dinamikus fallback adatgenerálással (pl. hiányzó e-mail címek automatikus pótlása).
2. **Adatbázis integráció (Dinamikus Életciklus):** Az adatokat elmenti egy ideiglenes SQLite adatbázisba. A séma-ütközések elkerülése érdekében a teszt minden futás előtt teljesen törli és tiszta lappal újraépíti a táblákat (`DROP TABLE IF EXISTS users`), így az oszlopváltoztatások nem okoznak adatbázis-zárolást vagy futási hibát.
3. **UI Automatizálás:**
   * Elindít egy böngészőt a Playwright segítségével.
   * Navigál a bejelentkező oldalra.
   * Kezeli a felugró süti-ablakokat (JavaScript alapú eltávolítás).
   * Beírja az adatbázisból visszakért adatokat a megfelelő mezőkbe.
4. **Validáció:** Ellenőrzi, hogy a felületen megjelenő adat megegyezik-e az adatbázisból visszakért forrásadattal.
5. **Takarítás:** A teszt végeztével automatikusan törli az ideiglenes adatbázis fájlt.

#### A folyamat során az alábbi technikai kihívások kerültek megoldásra:
* **Stabil UI Automatizálás:** A makacs süti-bannerek okozta kitakarási hibákat JavaScript injektálással (`evaluate` metódus) hárítottam el. Nyelvfüggetlen technikai azonosítókat (ID-k) használtam a stabilitásért.
* **Tiszta Tesztarchitektúra:** A tesztek utáni automatikus takarítást (adatbázis fájlok törlése) a `conftest.py` fájlban központosítottam (teardown folyamat).
* **Operációs Rendszer Szintű Hibakezelés:** Megoldottam az SQLite fájlzárolási problémáit (`WinError 32`) a Python szemétgyűjtőjének (*Garbage Collector*) finomhangolásával.

---

## 📁 Projekt Struktúra

```text
playwright-python-automation/
│
├── .github/workflows/   # GitHub Actions CI/CD pipeline konfigurációk
├── app/                 # A tesztelt helyi Flask webalkalmazás
├── data/                # Külső tesztadatok (user_data.json, Excel fájlok)
├── db_utils/            # Adatbázis kezelők és SQL segédfüggvények
├── pages/               # Page Object osztályok (Lokalizátorok és UI akciók)
├── tests/               # Pytest tesztesetek (különválasztott UI, API és E2E rétegek)
├── pytest.ini           # Globális Pytest konfigurációs fájl
└── requirements.txt     # Python függőségek listája
```

---

## 🚀 Telepítés és Futtatás

### 1. Függőségek telepítése
```bash
pip install -r requirements.txt
```

### 2. Playwright böngészők letöltése
```bash
playwright install
```

### 3. A teljes tesztcsomag (15/15 teszteset) futtatása és Allure adatok generálása
```bash
python -m pytest tests --alluredir=allure-results --clean-alluredir
```

### 4. Grafikus Allure riport megnyitása helyileg
```bash
allure serve allure-results
```

---

## 📊 Teszt Riportok (Allure)

A legfrissebb tesztfuttatási eredmények, hálózati logok és hibák esetén mentett adatok elérhetők online:

👉 [Allure Report megnyitása és megtekintése](https://github.io)

*(Megjegyzés: A riport minden sikeres GitHub Actions futtatás után automatikusan frissül a gh-pages ágon.)*
