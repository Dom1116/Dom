from fastapi import FastAPI

from app.api.v1.deals import router as deals_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(deals_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
