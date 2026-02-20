from contextlib import contextmanager
from datetime import datetime

import pytest
from apifast_vzero.apifast_vzero import app, database
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from apifast_vzero.models import table_registry


@pytest.fixture
def client():
    # Limpa o database antes de cada teste para garantir isolamento
    database.clear()
    return TestClient(app)


@pytest.fixture
def session():
    # Usando um banco de dados em memória para testes
    engine = create_engine('sqlite:///:memory:')

    # Cria as tabelas no banco de dados em memória
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1, 12, 0, 0)):
    def fake_time_hook(mapper, connection, target):
        # hasattr é usado para garantir que o modelo tenha o campo created_at
        #  antes de tentar setar o valor
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_update', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
