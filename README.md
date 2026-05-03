# Python Playwright Automation Framework 🚀

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

## 📁 Projekt Struktúra
* `pages/`: Page Object osztályok (Lokalizátorok és akciók)
* `tests/`: Tényleges tesztesetek
* `requirements.txt`: Függőségek listája

## 🚀 Telepítés és Futtatás
1. `pip install -r requirements.txt`
2. `playwright install`
3. `pytest --headed`
