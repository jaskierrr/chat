from chat.container import main_container
from chat.config import config
from chat.const import REDIS
import redis


async def create_redis_pool():
    redis_pool = redis.Redis(
        host=config.cache.host, port=config.cache.port, db=config.cache.db
    )
    main_container[REDIS] = redis_pool


async def close_redis_pool():
    if redis_pool := main_container.get(REDIS):
        await redis_pool.close()
