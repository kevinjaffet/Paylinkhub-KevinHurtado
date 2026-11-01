from fastapi import APIRouter

from app.models.dashboard import Dashboard
from app.services.orchestrator import build_dashboard

router = APIRouter()


@router.get("/{customerId}", response_model=Dashboard)
async def get_dashboard(customerId: str) -> Dashboard:
    return await build_dashboard(customerId)
