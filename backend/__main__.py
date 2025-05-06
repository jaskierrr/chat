import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.adapter.cache.connection import close_redis_pool, create_redis_pool
from backend.config import config

from adapter.db.connection import create_session, close_session
from backend.entrypoints.api_v1.router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_session()
    await create_redis_pool()
    yield
    await close_session()
    await close_redis_pool()

app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.server.host, port=config.server.port)
