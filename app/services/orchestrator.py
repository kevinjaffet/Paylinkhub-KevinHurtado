import asyncio

from app.models.dashboard import Dashboard, ProvidersStatus
from app.services.mapper import map_customer, map_transactions
from app.services.providers import ProviderError, fetch_core, fetch_pagos


async def build_dashboard(customer_id: str) -> Dashboard:
    core_result, pagos_result = await asyncio.gather(
        fetch_core(customer_id),
        fetch_pagos(customer_id),
        return_exceptions=True,
    )

    warnings: list[str] = []

    if isinstance(core_result, ProviderError):
        customer = None
        core_status = "unavailable"
        warnings.append("CORE is unavailable")
    elif isinstance(core_result, Exception):
        raise core_result
    else:
        customer = map_customer(core_result)
        core_status = "ok"

    if isinstance(pagos_result, ProviderError):
        transactions = []
        pagos_status = "unavailable"
        warnings.append("PAGOS is unavailable")
    elif isinstance(pagos_result, Exception):
        raise pagos_result
    else:
        transactions = map_transactions(pagos_result)
        pagos_status = "ok"

    return Dashboard(
        customer=customer,
        transactions=transactions,
        partial=bool(warnings),
        warnings=warnings,
        providers=ProvidersStatus(
            core=core_status,
            pagos=pagos_status,
            fx="unavailable",
        ),
    )
