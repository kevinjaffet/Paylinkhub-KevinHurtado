from decimal import Decimal

from fastapi import APIRouter

from app.models.dashboard import Customer, Dashboard, ProvidersStatus, Transaction

router = APIRouter()


@router.get("/{customerId}", response_model=Dashboard)
def get_dashboard(customerId: str) -> Dashboard:
    return Dashboard(
        customer=Customer(
            id=customerId,
            full_name="Ana Perez",
            email="ana.perez@example.com",
            phone="+57 300 000 0000",
        ),
        transactions=[
            Transaction(
                id="tx-1001",
                products=["payment-link", "fx-conversion"],
                quantity=2,
                total_usd=Decimal("150.75"),
            )
        ],
        partial=False,
        warnings=[],
        providers=ProvidersStatus(core="ok", pagos="ok", fx="ok"),
    )
