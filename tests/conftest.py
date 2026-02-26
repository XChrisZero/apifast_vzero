from contextlib import contextmanager
from datetime import datetime

import pytest
from apifast_vzero.apifast_vzero import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from apifast_vzero.database import get_session
from apifast_vzero.models import User, table_registry


@pytest.fixture
def client(session):
    # Limpa o database antes de cada teste para garantir isolamento
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Usando um banco de dados em memória para testes
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

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
        # Seta created_at apenas se o objeto for novo
        if hasattr(target, 'created_at'):
            target.created_at = time

        # Seta updated_at sempre (na criação e na atualização)
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    # Registra para os dois eventos: inserção e atualização
    event.listen(model, 'before_insert', fake_time_hook)
    event.listen(model, 'before_update', fake_time_hook)

    yield time

    # Remove os hooks após o uso do context manager
    event.remove(model, 'before_insert', fake_time_hook)
    event.remove(model, 'before_update', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    user = User()
    user.username = 'testuser'
    user.email = 'testuser@example.com'
    user.password = '123'
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
