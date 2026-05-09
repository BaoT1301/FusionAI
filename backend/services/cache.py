import hashlib
import json
import logging
import time
from typing import Any

from config import get_settings
from services.text import normalize_query

logger = logging.getLogger("fusionai.cache")


class ResearchCache:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = None
        self._memory: dict[str, tuple[float, dict[str, Any]]] = {}
        if self.settings.redis_url:
            try:
                import redis

                self._client = redis.from_url(self.settings.redis_url, decode_responses=True)
            except Exception:
                self._client = None

    @property
    def status(self) -> str:
        if self._client:
            return "redis"
        if self.settings.local_cache_enabled:
            return "memory"
        return "disabled"

    def key_for(self, query: str, mode: str = "research") -> str:
        normalized = normalize_query(query)
        digest = hashlib.sha256(f"{mode}:{normalized}".encode("utf-8")).hexdigest()
        return f"fusionai:{mode}:{digest}"

    def get(self, query: str, mode: str = "research") -> dict[str, Any] | None:
        key = self.key_for(query, mode)
        if not self._client:
            if not self.settings.local_cache_enabled:
                return None
            expires_at, payload = self._memory.get(key, (0, {}))
            if expires_at <= time.time():
                self._memory.pop(key, None)
                return None
            return payload

        try:
            raw = self._client.get(key)
        except Exception as exc:
            logger.warning("Redis get failed, falling back to miss: %s", exc)
            return None
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def set(self, query: str, payload: dict[str, Any], mode: str = "research") -> None:
        key = self.key_for(query, mode)
        if not self._client:
            if self.settings.local_cache_enabled:
                self._memory[key] = (time.time() + self.settings.cache_ttl_seconds, payload)
            return
        try:
            self._client.setex(
                key,
                self.settings.cache_ttl_seconds,
                json.dumps(payload),
            )
        except Exception as exc:
            logger.warning("Redis set failed, skipping cache write: %s", exc)

    def clear(self) -> None:
        self._memory.clear()
