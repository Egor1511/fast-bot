import json

import redis.asyncio as aioredis

from app.config import get_redis_url

redis_url = get_redis_url()
redis = aioredis.from_url(redis_url, decode_responses=True)


async def get_cache(key: str):
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None


async def set_cache(key: str, value,
                    ex: int = 60):  # Используем ex вместо expire
    await redis.set(key, json.dumps(value, default=str), ex=ex)


async def clear_cache():
    await redis.flushdb()
