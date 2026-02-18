import pytest
from apifast_vzero.apifast_vzero import app, database
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Limpa o database antes de cada teste para garantir isolamento
    database.clear()
    return TestClient(app)
