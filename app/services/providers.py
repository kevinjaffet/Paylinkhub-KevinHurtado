import logging
from typing import Any
from urllib.parse import quote

import httpx
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

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


def _before_sleep(retry_state: RetryCallState) -> None:
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    provider = exc.provider if isinstance(exc, ProviderError) else "provider"
    status_code = exc.status_code if isinstance(exc, ProviderError) else None
    logger.warning(
        "%s attempt %s failed (status=%s)",
        provider,
        retry_state.attempt_number,
        status_code if status_code is not None else "timeout",
    )


@retry(
    retry=retry_if_exception(_is_retryable),
    wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
    stop=stop_after_attempt(MAX_ATTEMPTS),
    reraise=True,
    before_sleep=_before_sleep,
)
async def _get_json(provider: str, url: str, timeout: httpx.Timeout) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
    except httpx.TimeoutException as exc:
        logger.warning("%s request timed out (%s)", provider, type(exc).__name__)
        raise ProviderError(provider, "timeout", retryable=True) from exc
    except httpx.RequestError as exc:
        logger.warning("%s connection failed (%s)", provider, type(exc).__name__)
        raise ProviderError(provider, "connection failed") from exc

    if response.status_code >= 500:
        logger.warning("%s returned HTTP %s", provider, response.status_code)
        raise ProviderError(
            provider,
            f"HTTP {response.status_code}",
            status_code=response.status_code,
            retryable=True,
        )

    if response.status_code != 200:
        logger.warning("%s returned HTTP %s", provider, response.status_code)
        raise ProviderError(
            provider,
            f"HTTP {response.status_code}",
            status_code=response.status_code,
        )

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
