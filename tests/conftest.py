from functools import partial
import uuid
import pytest
from redis import Redis
from sqlalchemy.pool import NullPool
import sqlalchemy_utils


from backend.config import Config
from aiohttp import request
from sqlalchemy.ext.asyncio import create_async_engine
from backend.adapter.db.postgres import Base
import sqlalchemy as sa
from yarl import URL
from typing import Any
from faker import Faker



@pytest.fixture(scope='session')
def config():
    return Config()

@pytest.fixture(scope='session')
def sa_engine_db(config: Config) -> Any:
    """
    На основе опыта Yandex
    http://www.moscowpython.ru/meetup/69/talk-from-yandex/
    """
    database_name = f'{uuid.uuid4().hex}.pytest'
    database_url = str(URL(config.db.dsn).with_scheme('postgresql').with_path(database_name))

    sqlalchemy_utils.create_database(database_url)

    engine = sa.create_engine(
        database_url,
        connect_args={'application_name': 'pytest', 'options': '-c timezone=utc'},
        isolation_level='AUTOCOMMIT',
        poolclass=NullPool,
        # json_serializer=json_dumps,
    )
    Base.metadata.create_all(bind=engine, tables=Base.metadata.sorted_tables)
    config.db.dsn = database_url

    try:
        yield engine
    finally:
        engine.dispose()
        sqlalchemy_utils.drop_database(database_url)


@pytest.fixture
def db_engine(sa_engine_db: Any) -> Any:
    try:
        yield sa_engine_db
    finally:
        with sa_engine_db.connect() as connection:
            tables = ','.join(str(table) for table in Base.metadata.sorted_tables)
            connection.execute(sa.text(f'TRUNCATE TABLE {tables}'))


@pytest.fixture
async def db_session(sa_engine_db: Any, config: Any) -> Any:
    dsn = URL(str(sa_engine_db.url)).with_password(sa_engine_db.url.password).with_scheme('postgresql+asyncpg')
    try:
        conn = create_async_engine(str(dsn))
        async with conn.connect() as session:
            yield session
    finally:
        with sa_engine_db.connect() as connection:
            tables = ','.join(str(table) for table in Base.metadata.sorted_tables)
            connection.execute(sa.text(f'TRUNCATE TABLE {tables}'))


@pytest.fixture
def redis_client_sync(config):
    redis = Redis.from_url(config.redis.dsn)
    yield redis
    redis.flushall()
    redis.close()


@pytest.fixture
async def client():
    class _Client:
        def __getattribute__(self, item):
            return partial(request, method=item)

    return _Client()


@pytest.fixture()
def fake():
    return Faker('ru_Ru')
