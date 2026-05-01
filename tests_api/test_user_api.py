import pytest

def test_get_post_details(page):
    # Itt egy létező bejegyzést kérünk le (az 1-es ID-jűt)
    response = page.request.get("https://jsonplaceholder.typicode.com/posts/1")
    
    # 200 OK ellenőrzése
    assert response.status == 200
    
    response_body = response.json()
    
    # Ellenőrizzük, hogy megkaptuk-e az adatokat (például az id-t)
    assert response_body["id"] == 1
    assert "userId" in response_body

def test_create_post(page):
    # Új bejegyzés létrehozása (POST kérés)
    payload = {
        "title": "Tanulás",
        "body": "API tesztelés Playwright-tal",
        "userId": 1
    }
    
    response = page.request.post("https://jsonplaceholder.typicode.com/posts", data=payload)
    
    # 201 Created ellenőrzése
    assert response.status == 201
    
    response_body = response.json()
    assert response_body["title"] == "Tanulás"
