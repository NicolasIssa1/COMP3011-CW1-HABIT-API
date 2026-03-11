import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import engine


@pytest.fixture(scope="session", autouse=True)
def _setup_test_db():
    # Create tables in a fresh DB for tests.
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class AuthenticatedTestClient(TestClient):
    """Test client that automatically adds API key to all requests."""
    
    def request(self, *args, **kwargs):
        """Override request to add API key header."""
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        elif kwargs["headers"] is None:
            kwargs["headers"] = {}
        
        kwargs["headers"]["X-API-Key"] = "test-api-key-12345"
        return super().request(*args, **kwargs)


@pytest.fixture()
def client():
    """Create a test client with API key authentication header."""
    return AuthenticatedTestClient(app)
