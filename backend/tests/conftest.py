import asyncio
import pytest
from httpx import AsyncClient
from fasatpi.testclient import TestClient

@pytest.fixture(scope="session")
def event_loop():
    pass

@pytest.fixture(scope="session")
def test_app():
    pass

