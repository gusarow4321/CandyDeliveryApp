import os
import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import create_engine
from alembic.command import upgrade

from httpx import AsyncClient

from candy.api.__main__ import create_app
from candy.utils.db import DEFAULT_DB_URL, make_alembic_config


PG_URL = os.getenv('CI_DB_URL', DEFAULT_DB_URL)


@pytest.fixture
def postgres():
    """
    Создает временную БД для запуска теста.
    """
    tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    tmp_url = PG_URL + tmp_name
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic', db_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    """
    Возвращает URL к БД с примененными миграциями.
    """
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
async def api_client(migrated_postgres):
    app = create_app(migrated_postgres)
    client = AsyncClient(app=app, base_url="http://test")

    try:
        yield client
    finally:
        await client.aclose()


@pytest.fixture
def migrated_postgres_connection(migrated_postgres):
    """
    Синхронное соединение со смигрированной БД.
    """
    engine = create_engine(migrated_postgres)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()
