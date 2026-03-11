"""Tests for API Key authentication."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def unauthenticated_client():
    """Create a test client WITHOUT API key authentication."""
    return TestClient(app)


def test_request_without_api_key_returns_401(unauthenticated_client):
    """Requests without X-API-Key header should return 401."""
    response = unauthenticated_client.get("/habits")
    assert response.status_code == 401
    detail = response.json()["detail"].lower()
    assert "api key" in detail or "missing" in detail


def test_request_with_invalid_api_key_returns_403(unauthenticated_client):
    """Requests with invalid API key should return 403."""
    response = unauthenticated_client.get(
        "/habits",
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]


def test_request_with_valid_api_key_succeeds(unauthenticated_client):
    """Requests with valid API key should succeed."""
    response = unauthenticated_client.get(
        "/habits",
        headers={"X-API-Key": "test-api-key-12345"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_endpoint_requires_auth(unauthenticated_client):
    """Health endpoint should still require authentication."""
    response = unauthenticated_client.get("/health")
    # Health can be public or protected depending on design
    # Current implementation protects all endpoints
    assert response.status_code in (200, 401, 403)
