import asyncio

import pytest

from app.services.orchestrator import build_dashboard
from app.services.providers import ProviderError

CORE_PAYLOAD = {
    "id": "7",
    "firstName": "Ana",
    "lastName": "Perez",
    "email": "ana@example.com",
    "phone": "300",
}
PAGOS_PAYLOAD = {
    "carts": [
        {
            "id": 9,
            "products": [{"title": "Link", "price": 10, "quantity": 2}],
        }
    ]
}


@pytest.fixture
def providers(monkeypatch):
    async def fake_core(customer_id):
        return {**CORE_PAYLOAD, "id": customer_id}

    async def fake_pagos(customer_id):
        return PAGOS_PAYLOAD

    monkeypatch.setattr("app.services.orchestrator.fetch_core", fake_core)
    monkeypatch.setattr("app.services.orchestrator.fetch_pagos", fake_pagos)
    return monkeypatch


def _dashboard(monkeypatch, fx_result):
    async def fake_fx():
        if isinstance(fx_result, Exception):
            raise fx_result
        return fx_result

    monkeypatch.setattr("app.services.orchestrator.get_fx_rates", fake_fx)
    return asyncio.run(build_dashboard("7"))


def test_fx_available(providers):
    dashboard = _dashboard(
        providers,
        {"base": "USD", "rates": {"EUR": 0.92, "GBP": 0.78}},
    )
    payload = dashboard.model_dump(mode="json")

    assert dashboard.partial is False
    assert dashboard.warnings == []
    assert dashboard.providers.fx == "ok"
    assert payload["exchange_rates"] == {"base": "USD", "EUR": 0.92, "GBP": 0.78}
    assert payload["customer"]["id"] == "7"
    assert payload["transactions"][0]["id"] == "9"


def test_fx_unavailable(providers):
    dashboard = _dashboard(providers, ProviderError("fx", "connection failed"))
    payload = dashboard.model_dump(mode="json")

    assert payload["exchange_rates"] is None
    assert dashboard.partial is True
    assert dashboard.warnings == ["FX is unavailable"]
    assert dashboard.providers.fx == "unavailable"
    assert dashboard.providers.core == "ok"
    assert dashboard.providers.pagos == "ok"
    assert payload["customer"]["full_name"] == "Ana Perez"
    assert payload["transactions"][0]["quantity"] == 2


def test_fx_invalid_response(providers):
    dashboard = _dashboard(providers, {"base": "USD", "rates": {"JPY": 150}})
    payload = dashboard.model_dump(mode="json")

    assert payload["exchange_rates"] is None
    assert dashboard.partial is True
    assert dashboard.warnings == ["FX is unavailable"]
    assert dashboard.providers.fx == "unavailable"
    assert payload["customer"]["id"] == "7"
    assert len(payload["transactions"]) == 1
