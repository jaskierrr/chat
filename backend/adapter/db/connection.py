from backend.container import main_container
from backend.config import config
from backend.const import POSTGRES_ENGINE, POSTGRES_CONN
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


async def create_session():
    engine = create_async_engine(config.db.dsn.unicode_string())
    connection = async_sessionmaker(engine, expire_on_commit=False)

    main_container[POSTGRES_ENGINE] = engine
    main_container[POSTGRES_CONN] = connection


async def close_session():
    if connection := main_container.get(POSTGRES_ENGINE):
        await connection.dispose()
