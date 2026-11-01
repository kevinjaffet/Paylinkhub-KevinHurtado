from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

ProviderState = Literal["ok", "degraded", "unavailable"]


class Customer(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str


class Transaction(BaseModel):
    id: str
    products: list[str]
    quantity: int
    total_usd: Decimal


class ProvidersStatus(BaseModel):
    core: ProviderState
    pagos: ProviderState
    fx: ProviderState


class Dashboard(BaseModel):
    customer: Customer | None
    transactions: list[Transaction]
    partial: bool
    warnings: list[str]
    providers: ProvidersStatus
