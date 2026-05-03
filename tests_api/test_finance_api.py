import pytest
import time

def test_hungarian_zip_code(page):
    response = page.request.get("https://api.zippopotam.us/hu/1051")
    assert response.status == 200
    
    response_body = response.json()
    assert response_body["country"] == "Hungary"
    
    # Itt volt a hiba: a places egy lista [], annak az első elemét [0] kell nézni
    place_name = response_body["places"][0]["place name"]
    print(f"\nAz irányítószám városa: {place_name}")
    assert "Budapest" in place_name

def test_api_speed(page):
    start_time = time.time()
    response = page.request.get("https://api.zippopotam.us/hu/1051")
    duration = time.time() - start_time
    
    assert response.status == 200
    assert duration < 1.0 
    print(f"API válaszidő: {duration:.2f} másodperc")