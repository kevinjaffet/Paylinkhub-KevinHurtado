from decimal import Decimal, InvalidOperation
from typing import Any

from app.models.dashboard import Customer, ExchangeRates, Transaction


def map_customer(payload: Any) -> Customer | None:
    if not isinstance(payload, dict) or not payload:
        return None

    first_name = _text(payload.get("firstName"))
    last_name = _text(payload.get("lastName"))
    full_name = " ".join(part for part in (first_name, last_name) if part)

    return Customer(
        id=_text(payload.get("id")),
        full_name=full_name,
        email=_text(payload.get("email")),
        phone=_text(payload.get("phone")),
    )


def map_exchange_rates(payload: Any) -> ExchangeRates | None:
    if not isinstance(payload, dict):
        return None

    base = payload.get("base")
    rates = payload.get("rates")
    if not isinstance(base, str) or not base.strip() or not isinstance(rates, dict):
        return None

    eur = _rate(rates.get("EUR"))
    gbp = _rate(rates.get("GBP"))
    if eur is None or gbp is None:
        return None

    return ExchangeRates(base=base.strip(), EUR=eur, GBP=gbp)


def map_transactions(payload: Any) -> list[Transaction]:
    if not isinstance(payload, dict):
        return []

    carts = payload.get("carts")
    if not isinstance(carts, list):
        return []

    return [_map_cart(cart) for cart in carts if isinstance(cart, dict)]


def _map_cart(cart: dict[str, Any]) -> Transaction:
    products = cart.get("products")
    names: list[str] = []
    quantity = 0
    total = Decimal("0")

    if isinstance(products, list):
        for product in products:
            if not isinstance(product, dict):
                continue
            name = _text(product.get("title"))
            if name:
                names.append(name)
            item_quantity = _as_int(product.get("quantity"))
            quantity += item_quantity
            total += _as_decimal(product.get("price")) * item_quantity

    return Transaction(
        id=_text(cart.get("id")),
        products=names,
        quantity=quantity,
        total_usd=total,
    )


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, bool) or value is None:
        return ""
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    return ""


def _as_int(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            number = Decimal(value.strip())
        except InvalidOperation:
            return 0
        if number == number.to_integral_value():
            return int(number)
    return 0


def _rate(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    if not isinstance(value, (int, float, Decimal, str)):
        return None
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    return number


def _as_decimal(value: Any) -> Decimal:
    if isinstance(value, bool) or value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float, str)):
        try:
            return Decimal(str(value).strip())
        except InvalidOperation:
            return Decimal("0")
    return Decimal("0")
