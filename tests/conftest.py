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


@pytest.fixture()
def client():
    return TestClient(app)
