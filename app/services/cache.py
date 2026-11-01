import asyncio
import time
from typing import Any

from app.config import get_settings
from app.services.providers import ProviderError, fetch_fx


class FxCache:
    def __init__(self) -> None:
        self._payload: dict[str, Any] | None = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    def clear(self) -> None:
        self._payload = None
        self._expires_at = 0.0

    async def get(self) -> dict[str, Any]:
        cached = self._fresh_payload()
        if cached is not None:
            return cached

        async with self._lock:
            cached = self._fresh_payload()
            if cached is not None:
                return cached

            payload = await fetch_fx()
            if not _has_rates(payload):
                raise ProviderError("fx", "invalid response")

            self._payload = payload
            self._expires_at = time.monotonic() + get_settings().fx_cache_ttl_seconds
            return payload

    def _fresh_payload(self) -> dict[str, Any] | None:
        if self._payload is not None and time.monotonic() < self._expires_at:
            return self._payload
        return None


def _has_rates(payload: dict[str, Any]) -> bool:
    rates = payload.get("rates")
    if not isinstance(rates, dict) or not rates:
        return False
    return all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in rates.values())


fx_cache = FxCache()


async def get_fx_rates() -> dict[str, Any]:
    return await fx_cache.get()
