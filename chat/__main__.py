import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from chat.adapter.cache.connection import close_redis_pool, create_redis_pool
from chat.config import config

from adapter.db.connection import create_session, close_session
from chat.entrypoint.api_v1.router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_session()
    print("start lifespan")
    await create_redis_pool()
    yield
    await close_session()
    await close_redis_pool()


app = FastAPI(lifespan=lifespan)


app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.server.port)
