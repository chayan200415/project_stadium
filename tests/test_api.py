from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StadiumGPT API"}

def test_crowd_data():
    response = client.get("/api/crowd/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "location" in data[0]

def test_transport_data():
    response = client.get("/api/transport/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "route" in data[0]
