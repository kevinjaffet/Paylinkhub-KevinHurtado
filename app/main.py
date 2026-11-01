import logging
from pathlib import Path

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes.dashboard import router as dashboard_router

settings = get_settings()
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"


def configure_provider_logging() -> None:
    provider_logger = logging.getLogger("app.services.providers")
    provider_logger.setLevel(logging.INFO)
    provider_logger.propagate = False
    if provider_logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    provider_logger.addHandler(handler)


configure_provider_logging()

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


app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="frontend")
