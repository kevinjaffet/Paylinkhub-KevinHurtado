from fastapi import FastAPI, status

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Future API routers are registered here under settings.api_prefix.


@app.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    return {
        "status": "operational",
        "service": settings.app_name,
    }
