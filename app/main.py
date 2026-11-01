from fastapi import FastAPI, status

from app.config import get_settings
from app.routes.dashboard import router as dashboard_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(
    dashboard_router,
    prefix=f"{settings.api_prefix}/dashboard",
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    return {
        "status": "operational",
        "service": settings.app_name,
    }
