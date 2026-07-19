"""
Comprehensive API tests for StadiumGPT backend.

Tests all endpoints including health check, crowd intelligence,
transport, sustainability, navigation, dashboard, chat, and incidents.
Includes edge cases, input validation, and security header checks.
"""

import pytest
from fastapi.testclient import TestClient
from backend.database import Base, engine
from backend.main import app

# Ensure tables exist before tests
Base.metadata.create_all(bind=engine)
client = TestClient(app)


# ==================== Health Check ====================

class TestHealthCheck:
    """Tests for the root health check endpoint."""

    def test_read_root_returns_200(self):
        """Root endpoint should return 200 with welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to StadiumGPT API"}

    def test_read_root_response_type(self):
        """Root endpoint should return JSON content type."""
        response = client.get("/")
        assert "application/json" in response.headers["content-type"]


# ==================== Security Headers ====================

class TestSecurityHeaders:
    """Tests for security headers on all responses."""

    def test_x_frame_options_header(self):
        """All responses should include X-Frame-Options: DENY."""
        response = client.get("/")
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_x_content_type_options_header(self):
        """All responses should include X-Content-Type-Options: nosniff."""
        response = client.get("/")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_strict_transport_security_header(self):
        """All responses should include HSTS header."""
        response = client.get("/")
        assert "max-age=" in response.headers.get("Strict-Transport-Security", "")

    def test_x_xss_protection_header(self):
        """All responses should include X-XSS-Protection header."""
        response = client.get("/")
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_referrer_policy_header(self):
        """All responses should include Referrer-Policy header."""
        response = client.get("/")
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_permissions_policy_header(self):
        """All responses should include Permissions-Policy header."""
        response = client.get("/")
        assert "camera=()" in response.headers.get("Permissions-Policy", "")

    def test_content_security_policy_header(self):
        """All responses should include Content-Security-Policy header."""
        response = client.get("/")
        csp = response.headers.get("Content-Security-Policy", "")
        assert "default-src 'self'" in csp


# ==================== Crowd Intelligence ====================

class TestCrowdEndpoints:
    """Tests for crowd intelligence endpoints."""

    def test_get_crowd_data_returns_list(self):
        """Crowd endpoint should return a list of zone data."""
        response = client.get("/api/crowd/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_crowd_data_has_required_fields(self):
        """Each crowd data item should have location and occupancy_percent."""
        response = client.get("/api/crowd/")
        data = response.json()
        for item in data:
            assert "location" in item
            assert "occupancy_percent" in item
            assert isinstance(item["occupancy_percent"], (int, float))

    def test_crowd_occupancy_in_valid_range(self):
        """Occupancy should be between 0 and 100."""
        response = client.get("/api/crowd/")
        data = response.json()
        for item in data:
            assert 0 <= item["occupancy_percent"] <= 100

    def test_crowd_insight_returns_insight(self):
        """Crowd insight endpoint should return an insight string."""
        response = client.get("/api/crowd/insight")
        assert response.status_code == 200
        data = response.json()
        assert "insight" in data
        assert isinstance(data["insight"], str)
        assert len(data["insight"]) > 0


# ==================== Transport ====================

class TestTransportEndpoints:
    """Tests for transportation hub endpoints."""

    def test_get_transport_returns_list(self):
        """Transport endpoint should return a list of route statuses."""
        response = client.get("/api/transport/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_transport_data_has_required_fields(self):
        """Each transport item should have route and status."""
        response = client.get("/api/transport/")
        data = response.json()
        for item in data:
            assert "route" in item
            assert "status" in item

    def test_transport_has_multiple_options(self):
        """Transport should return data for multiple routes."""
        response = client.get("/api/transport/")
        data = response.json()
        assert len(data) >= 3


# ==================== Sustainability ====================

class TestSustainabilityEndpoints:
    """Tests for sustainability dashboard endpoints."""

    def test_get_sustainability_data(self):
        """Sustainability endpoint should return all metrics."""
        response = client.get("/api/sustainability/")
        assert response.status_code == 200
        data = response.json()
        assert "power_usage_kw" in data
        assert "water_usage_l" in data
        assert "waste_generation_kg" in data
        assert "surplus_food_portions" in data

    def test_sustainability_values_are_positive(self):
        """All sustainability values should be positive numbers."""
        response = client.get("/api/sustainability/")
        data = response.json()
        assert data["power_usage_kw"] > 0
        assert data["water_usage_l"] > 0
        assert data["waste_generation_kg"] > 0
        assert data["surplus_food_portions"] > 0

    def test_sustainability_insight_returns_insight(self):
        """Sustainability insight should return AI recommendations."""
        response = client.get("/api/sustainability/insight")
        assert response.status_code == 200
        data = response.json()
        assert "insight" in data
        assert isinstance(data["insight"], str)


# ==================== Navigation ====================

class TestNavigationEndpoints:
    """Tests for indoor navigation endpoints."""

    def test_navigation_with_valid_params(self):
        """Navigation should return route data with valid parameters."""
        response = client.get("/api/navigation/", params={"start": "Gate A", "end": "Section 112"})
        assert response.status_code == 200
        data = response.json()
        assert data["start"] == "Gate A"
        assert data["end"] == "Section 112"
        assert "steps" in data
        assert "estimated_time_mins" in data
        assert "accessible_route" in data

    def test_navigation_has_steps(self):
        """Navigation should return step-by-step directions."""
        response = client.get("/api/navigation/", params={"start": "Gate B", "end": "VIP Lounge"})
        data = response.json()
        assert len(data["steps"]) > 0
        assert len(data["accessible_route"]) > 0

    def test_navigation_missing_params(self):
        """Navigation should return 422 when parameters are missing."""
        response = client.get("/api/navigation/")
        assert response.status_code == 422

    def test_navigation_estimated_time_is_positive(self):
        """Estimated time should be a positive number."""
        response = client.get("/api/navigation/", params={"start": "Gate A", "end": "Gate B"})
        data = response.json()
        assert data["estimated_time_mins"] > 0


# ==================== Dashboard ====================

class TestDashboardEndpoints:
    """Tests for the dashboard summary endpoint."""

    def test_dashboard_summary_returns_summary(self):
        """Dashboard summary should return an AI-generated summary."""
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert isinstance(data["summary"], str)
        assert len(data["summary"]) > 0


# ==================== Chat ====================

class TestChatEndpoints:
    """Tests for the AI chat assistant endpoint."""

    def test_chat_with_valid_message(self):
        """Chat should return a response for a valid message."""
        response = client.post(
            "/api/chat/",
            json={"message": "Where is Gate A?", "language": "English"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)

    def test_chat_with_default_language(self):
        """Chat should work with only a message (default language)."""
        response = client.post(
            "/api/chat/",
            json={"message": "Hello"}
        )
        assert response.status_code == 200
        assert "response" in response.json()

    def test_chat_empty_message_rejected(self):
        """Chat should reject empty messages with 422."""
        response = client.post(
            "/api/chat/",
            json={"message": "", "language": "English"}
        )
        assert response.status_code == 422

    def test_chat_missing_message_field(self):
        """Chat should reject requests without a message field."""
        response = client.post("/api/chat/", json={"language": "English"})
        assert response.status_code == 422

    def test_chat_message_too_long(self):
        """Chat should reject messages exceeding max length."""
        response = client.post(
            "/api/chat/",
            json={"message": "x" * 1001, "language": "English"}
        )
        assert response.status_code == 422


# ==================== Incidents ====================

class TestIncidentEndpoints:
    """Tests for incident management endpoints."""

    def test_create_incident(self):
        """Should create a new incident with AI plan."""
        response = client.post(
            "/api/incident/",
            json={
                "type": "Medical",
                "location": "Gate A",
                "description": "Fan fainted near entrance"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "Medical"
        assert data["location"] == "Gate A"
        assert "ai_plan" in data
        assert "id" in data

    def test_get_incidents_returns_list(self):
        """Get incidents should return a list."""
        response = client.get("/api/incident/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_incident_invalid_type_rejected(self):
        """Incident with special characters in type should be rejected."""
        response = client.post(
            "/api/incident/",
            json={
                "type": "<script>alert('xss')</script>",
                "location": "Gate A",
                "description": "Test incident description here"
            }
        )
        assert response.status_code == 422

    def test_incident_short_description_rejected(self):
        """Incident with too-short description should be rejected."""
        response = client.post(
            "/api/incident/",
            json={
                "type": "Medical",
                "location": "Gate A",
                "description": "Hi"
            }
        )
        assert response.status_code == 422

    def test_incident_missing_fields_rejected(self):
        """Incident with missing required fields should be rejected."""
        response = client.post(
            "/api/incident/",
            json={"type": "Medical"}
        )
        assert response.status_code == 422


# ==================== 404 ====================

class TestNotFound:
    """Tests for non-existent endpoints."""

    def test_invalid_endpoint_returns_404(self):
        """Non-existent endpoint should return 404."""
        response = client.get("/api/nonexistent/")
        assert response.status_code == 404
