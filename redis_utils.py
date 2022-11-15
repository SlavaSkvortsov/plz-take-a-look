from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio.client import Redis


@asynccontextmanager
async def get_redis_client() -> AsyncGenerator[Redis, None]:
    client = await Redis.from_url(
        'redis://localhost',
    )
    try:
        yield client
    finally:
        client.close()

