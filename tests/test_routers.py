from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_page():
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["status"]

def test_create_book():
    # Test creating a book through the API
    book_data = {
        "title": "API Test",
        "author": "Test Author",
        "isbn": "978-3-16-148410-1",
        "published_date": "2023-01-01",
        "price": 15.99
    }
    response = client.post("/api/books/", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "API Test"