from __future__ import annotations

from functools import lru_cache
from typing import Optional

import redis

from core.config.settings import AppSettings
from core.logging.logger import logger


@lru_cache()
def get_redis_client() -> Optional[redis.Redis]:
    """
    Get a singleton Redis client.

    Returns None if REDIS_URL is not configured or Redis client creation fails.
    """
    redis_url = getattr(AppSettings, "REDIS_URL", None)
    if not redis_url:
        return None

    try:
        return redis.Redis.from_url(redis_url, decode_responses=True)
    except Exception as e:
        logger.warning(f"Failed to initialize Redis client: {e}")
        return None

