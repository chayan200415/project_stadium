from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StadiumGPT API"}

def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert "summary" in response.json()

def test_chat():
    response = client.post("/api/chat/", json={"message": "hello", "language": "English"})
    assert response.status_code == 200
    assert "response" in response.json()
