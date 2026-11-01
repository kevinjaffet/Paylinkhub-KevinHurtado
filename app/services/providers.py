import json
import logging
import time
from typing import Any
from urllib.parse import quote

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from app.config import get_settings

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3


class ProviderError(Exception):
    def __init__(
        self,
        provider: str,
        message: str,
        *,
        status_code: int | None = None,
        retryable: bool = False,
    ) -> None:
        self.provider = provider
        self.status_code = status_code
        self.retryable = retryable
        super().__init__(f"{provider}: {message}")


def _provider_url(base_url: str, customer_id: str) -> str:
    return f"{base_url.rstrip('/')}/{quote(str(customer_id), safe='')}"


def _is_retryable(exc: BaseException) -> bool:
    return isinstance(exc, ProviderError) and exc.retryable


def _log_provider(
    provider: str,
    started: float,
    result: str,
    status_code: int | None,
) -> None:
    logger.info(
        json.dumps(
            {
                "provider": provider,
                "duration_ms": round((time.perf_counter() - started) * 1000),
                "result": result,
                "status_code": status_code,
            },
            separators=(",", ":"),
        )
    )


@retry(
    retry=retry_if_exception(_is_retryable),
    wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
    stop=stop_after_attempt(MAX_ATTEMPTS),
    reraise=True,
)
async def _get_json(provider: str, url: str, timeout: httpx.Timeout) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
    except httpx.TimeoutException as exc:
        _log_provider(provider, started, "timeout", None)
        raise ProviderError(provider, "timeout", retryable=True) from exc
    except httpx.RequestError as exc:
        _log_provider(provider, started, "failure", None)
        raise ProviderError(provider, "connection failed") from exc

    if response.status_code >= 500:
        _log_provider(provider, started, "failure", response.status_code)
        raise ProviderError(
            provider,
            f"HTTP {response.status_code}",
            status_code=response.status_code,
            retryable=True,
        )

    if response.status_code != 200:
        _log_provider(provider, started, "failure", response.status_code)
        raise ProviderError(
            provider,
            f"HTTP {response.status_code}",
            status_code=response.status_code,
        )

    try:
        payload = response.json()
    except ValueError as exc:
        _log_provider(provider, started, "failure", response.status_code)
        raise ProviderError(provider, "invalid response") from exc

    if not isinstance(payload, dict):
        _log_provider(provider, started, "failure", response.status_code)
        raise ProviderError(provider, "invalid response")

    _log_provider(provider, started, "success", response.status_code)
    return payload


async def fetch_core(customer_id: str) -> dict[str, Any]:
    settings = get_settings()
    return await _get_json(
        "core",
        _provider_url(settings.core_base_url, customer_id),
        httpx.Timeout(settings.core_timeout_seconds),
    )


async def fetch_pagos(customer_id: str) -> dict[str, Any]:
    settings = get_settings()
    return await _get_json(
        "pagos",
        _provider_url(settings.pagos_base_url, customer_id),
        httpx.Timeout(settings.pagos_timeout_seconds),
    )


async def fetch_fx() -> dict[str, Any]:
    settings = get_settings()
    return await _get_json(
        "fx",
        settings.fx_url,
        httpx.Timeout(settings.fx_timeout_seconds),
    )
