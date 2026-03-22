from __future__ import annotations

from redis.asyncio import Redis

from core.config import settings


def get_redis() -> Redis:
    url = settings.redis_url or "redis://localhost:6379"
    return Redis.from_url(url, decode_responses=True)
