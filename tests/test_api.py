"""
Root-level API tests for StadiumGPT.

Integration tests covering all major API endpoints, data validation,
security headers, and error handling scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from backend.database import Base, engine
from backend.main import app

# Ensure tables exist before tests
Base.metadata.create_all(bind=engine)
client = TestClient(app)


# ==================== Health Check ====================

def test_read_root():
    """Root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StadiumGPT API"}


# ==================== Crowd ====================

def test_crowd_data():
    """Crowd endpoint returns a list with location data."""
    response = client.get("/api/crowd/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "location" in data[0]
    assert "occupancy_percent" in data[0]


def test_crowd_data_values():
    """Crowd occupancy values should be within valid range."""
    response = client.get("/api/crowd/")
    data = response.json()
    for item in data:
        assert 0 <= item["occupancy_percent"] <= 100


def test_crowd_insight():
    """Crowd insight should return an AI-generated string."""
    response = client.get("/api/crowd/insight")
    assert response.status_code == 200
    assert "insight" in response.json()


# ==================== Transport ====================

def test_transport_data():
    """Transport endpoint returns list with route data."""
    response = client.get("/api/transport/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "route" in data[0]
    assert "status" in data[0]


def test_transport_multiple_options():
    """Transport should return multiple route options."""
    response = client.get("/api/transport/")
    data = response.json()
    assert len(data) >= 3


# ==================== Sustainability ====================

def test_sustainability_data():
    """Sustainability endpoint returns all environmental metrics."""
    response = client.get("/api/sustainability/")
    assert response.status_code == 200
    data = response.json()
    assert "power_usage_kw" in data
    assert "water_usage_l" in data
    assert "waste_generation_kg" in data
    assert "surplus_food_portions" in data


def test_sustainability_positive_values():
    """All sustainability metrics should be positive."""
    response = client.get("/api/sustainability/")
    data = response.json()
    for key, value in data.items():
        assert value > 0, f"{key} should be positive"


def test_sustainability_insight():
    """Sustainability insight should return AI recommendations."""
    response = client.get("/api/sustainability/insight")
    assert response.status_code == 200
    assert "insight" in response.json()


# ==================== Navigation ====================

def test_navigation_valid():
    """Navigation with valid params should return route steps."""
    response = client.get("/api/navigation/", params={"start": "Gate A", "end": "Gate B"})
    assert response.status_code == 200
    data = response.json()
    assert "steps" in data
    assert "accessible_route" in data
    assert data["estimated_time_mins"] > 0


def test_navigation_missing_params():
    """Navigation without required params should return 422."""
    response = client.get("/api/navigation/")
    assert response.status_code == 422


# ==================== Dashboard ====================

def test_dashboard_summary():
    """Dashboard summary should return AI-generated text."""
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert "summary" in response.json()


# ==================== Chat ====================

def test_chat():
    """Chat should return an AI response."""
    response = client.post("/api/chat/", json={"message": "hello", "language": "English"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_empty_message():
    """Chat should reject empty messages."""
    response = client.post("/api/chat/", json={"message": "", "language": "English"})
    assert response.status_code == 422


def test_chat_missing_message():
    """Chat should reject requests without message field."""
    response = client.post("/api/chat/", json={})
    assert response.status_code == 422


# ==================== Incidents ====================

def test_create_incident():
    """Creating an incident should return the incident with AI plan."""
    response = client.post(
        "/api/incident/",
        json={"type": "Security", "location": "Gate C", "description": "Unauthorized person detected"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Security"
    assert "ai_plan" in data


def test_get_incidents():
    """Getting incidents should return a list."""
    response = client.get("/api/incident/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_incident_validation_rejects_xss():
    """Incident should reject input with special characters (XSS attempt)."""
    response = client.post(
        "/api/incident/",
        json={
            "type": "<script>alert(1)</script>",
            "location": "Gate A",
            "description": "Test incident"
        }
    )
    assert response.status_code == 422


def test_incident_short_description():
    """Incident should reject descriptions that are too short."""
    response = client.post(
        "/api/incident/",
        json={"type": "Medical", "location": "Gate A", "description": "Hi"}
    )
    assert response.status_code == 422


# ==================== Security Headers ====================

def test_security_headers_present():
    """All security headers should be present in responses."""
    response = client.get("/")
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "max-age=" in response.headers.get("Strict-Transport-Security", "")
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


# ==================== 404 ====================

def test_nonexistent_endpoint():
    """Non-existent endpoint should return 404."""
    response = client.get("/api/does_not_exist/")
    assert response.status_code == 404
