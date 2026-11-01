import logging
from typing import Any
from urllib.parse import quote

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = httpx.Timeout(10.0)


class ProviderError(Exception):
    def __init__(self, provider: str, message: str, *, status_code: int | None = None) -> None:
        self.provider = provider
        self.status_code = status_code
        super().__init__(f"{provider}: {message}")


def _provider_url(base_url: str, customer_id: str) -> str:
    return f"{base_url.rstrip('/')}/{quote(str(customer_id), safe='')}"


async def _get_json(provider: str, url: str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=REQUEST_TIMEOUT)
    except httpx.RequestError as exc:
        logger.warning("%s connection failed (%s)", provider, type(exc).__name__)
        raise ProviderError(provider, "connection failed") from exc

    if response.status_code != 200:
        logger.warning("%s returned HTTP %s", provider, response.status_code)
        raise ProviderError(provider, f"HTTP {response.status_code}", status_code=response.status_code)

    try:
        payload = response.json()
    except ValueError as exc:
        logger.warning("%s returned a non-JSON response", provider)
        raise ProviderError(provider, "invalid response") from exc

    if not isinstance(payload, dict):
        logger.warning("%s returned an unexpected JSON type", provider)
        raise ProviderError(provider, "invalid response")

    return payload


async def fetch_core(customer_id: str) -> dict[str, Any]:
    settings = get_settings()
    return await _get_json("core", _provider_url(settings.core_base_url, customer_id))


async def fetch_pagos(customer_id: str) -> dict[str, Any]:
    settings = get_settings()
    return await _get_json("pagos", _provider_url(settings.pagos_base_url, customer_id))
