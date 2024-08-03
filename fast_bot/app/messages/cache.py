import json

import redis.asyncio as aioredis

from config import get_redis_url

redis_url = get_redis_url()
redis = aioredis.from_url(redis_url, decode_responses=True)


async def get_cache(key: str):
    """
    Asynchronously retrieves the value associated with the given key from the Redis cache.

    Args:
        key (str): The key to retrieve the value for.

    Returns:
        The value associated with the given key, or None if the key is not found in the cache.
    """
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None


async def set_cache(key: str, value,
                    ex: int = 60):
    """
    Asynchronously sets a value in the Redis cache with the given key.
    Args:
        key (str): The key to set the value for.
        value: The value to set. It will be serialized to JSON before being stored.
        ex (int, optional): The expiration time of the key in seconds. Defaults to 60.
    Returns:
        None
    """
    await redis.set(key, json.dumps(value, default=str), ex=ex)


async def clear_cache():
    """
    Asynchronously clears the entire Redis cache by flushing all keys.
    This function uses the `flushdb()` method of the Redis client to remove all keys from the cache.
    Returns:
        None
    """
    await redis.flushdb()
